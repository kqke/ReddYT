import re
import requests
import time
import bs4
import json
import youtube_dl
from tempfile import TemporaryDirectory
import os

from exceptions import NotADownloadableLinkError, BaseDownloaderException, ResourceNotFound, SiteDownloaderError

# TODO - missing downloaders:
# vimeo
# streamable


def save_content(content, file_name):
    with open(file_name, 'wb') as file:
        file.write(content)


def base_download(url, wait_time):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
            # logger.debug(f'Written file to {file_name}')
        elif response.status_code in (301, 401, 403, 404):
            raise BaseDownloaderException(
                f'Unrecoverable error requesting resource: HTTP Code {response.status_code}')
        else:
            raise requests.exceptions.ConnectionError(f'Response code {response.status_code}')
    except requests.exceptions.ConnectionError as e:
        # logger.warning(f'Error occured downloading from {url}, waiting {wait_time} seconds: {e}')
        time.sleep(wait_time)
        if wait_time < 300:
            return base_download(url, wait_time + 60)
        else:
            # logger.error(f'Max wait time exceeded for resource at url {url}')
            raise


def retrieve_url(url, cookies=None, headers=None):
    res = requests.get(url, cookies=cookies, headers=headers)
    if res.status_code != 200:
        raise ResourceNotFound(f'Server responded with {res.status_code} to {url}')
    return res


def imgur_get_data(url):
    if re.match(r'.*\.gifv$', url):
        url = url.replace('i.imgur', 'imgur')
        url = url.rstrip('.gifv')

    res = retrieve_url(url, cookies={'over18': '1', 'postpagebeta': '0'})
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    scripts = soup.find_all('script', attrs={'type': 'text/javascript'})
    scripts = [script.string.replace('\n', '') for script in scripts if script.string]

    script_regex = re.compile(r'\s*\(function\(widgetFactory\)\s*{\s*widgetFactory\.mergeConfig\(\'gallery\'')
    chosen_script = list(filter(lambda s: re.search(script_regex, s), scripts))
    if len(chosen_script) != 1:
        raise SiteDownloaderError(f'Could not read page source from {url}')

    chosen_script = chosen_script[0]

    outer_regex = re.compile(r'widgetFactory\.mergeConfig\(\'gallery\', ({.*})\);')
    inner_regex = re.compile(r'image\s*:(.*),\s*group')
    try:
        image_dict = re.search(outer_regex, chosen_script).group(1)
        image_dict = re.search(inner_regex, image_dict).group(1)
    except AttributeError:
        raise SiteDownloaderError(f'Could not find image dictionary in page source')

    try:
        image_dict = json.loads(image_dict)
    except json.JSONDecodeError as e:
        raise SiteDownloaderError(f'Could not parse received dict as JSON: {e}')

    return image_dict


def imgur_validate_extension(ext_suffix):
    possible_extensions = ('.mp4', '.gif')
    selection = [ext for ext in possible_extensions if ext == ext_suffix]
    if len(selection) == 1:
        return selection[0]
    else:
        raise SiteDownloaderError(f'"{ext_suffix}" is not recognized as a valid extension for Imgur')


def imgur_get_image_url(data):
    return 'https://i.imgur.com/' + data['hash'] + imgur_validate_extension(data['ext'])


def imgur_download(url):
    raw_data = imgur_get_data(url)
    ret = []
    if 'album_images' in raw_data:
        images = raw_data['album_images']
        for image in images['images']:
            try:
                image_url = imgur_get_image_url(image)
            except SiteDownloaderError:
                # Log error
                continue
            content = base_download(image_url, 1000), image['ext']
            ret.append(content)
    else:
        image_url = imgur_get_image_url(raw_data)
        content = base_download(image_url, 1000), raw_data['ext']
        ret.append(content)

    if not ret:
        raise SiteDownloaderError(f'Did not find any files with valid extension in this Imgur link: {url}')

    return ret


def gifdeliverynetwork_download(url):
    page = retrieve_url(url)

    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    content = soup.find('source', attrs={'id': 'mp4Source', 'type': 'video/mp4'})

    try:
        out = content['src']
        if not out:
            raise KeyError
    except KeyError:
        raise SiteDownloaderError('Could not find source link')

    content = base_download(out, 1000), '.mp4'
    return [content]


def gfycat_download(url):
    gfycat_id = re.match(r'.*/(.*?)/?$', url).group(1)
    url = 'https://gfycat.com/' + gfycat_id

    response = retrieve_url(url)
    if 'gifdeliverynetwork' in response.url:
        return gifdeliverynetwork_download(url)

    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    content = soup.find('script', attrs={'data-react-helmet': 'true', 'type': 'application/ld+json'})

    try:
        out = json.loads(content.contents[0])['video']['contentUrl']
    except (IndexError, KeyError) as e:
        raise SiteDownloaderError(f'Failed to download Gfycat link {url}: {e}')
    except json.JSONDecodeError as e:
        raise SiteDownloaderError(f'Did not receive valid JSON data: {e}')

    content = base_download(out, 1000), '.mp4'
    return [content]


def yt_dl_download(options, url):
    options['quiet'] = True
    with TemporaryDirectory() as temp_dir:
        options['outtmpl'] = temp_dir + '/' + 'test.%(ext)s'
        try:
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([url])
        except youtube_dl.DownloadError as e:
            raise SiteDownloaderError(f'Youtube download failed: {e}')

        downloaded_file = temp_dir + '/' + os.listdir(temp_dir)[0]
        _, extension = os.path.splitext(downloaded_file)
        with open(downloaded_file, 'rb') as file:
            content = file.read()
    return content, extension


def vreddit_download(url):
    out = yt_dl_download({}, url)
    return [out]


def youtube_download(url):
    ytdl_options = {
        'format': 'best',
        'playlistend': 1,
        'nooverwrites': True,
    }
    out = yt_dl_download(ytdl_options, url)
    return [out]


def download_by_url(url):
    url_beginning = r'\s*(https?://(www\.)?)'
    if re.match(url_beginning + r'(i\.)?imgur.*\.gifv$', url):
        return imgur_download(url)
    elif re.match(url_beginning + r'gfycat\.', url):
        return gfycat_download(url)
    elif re.match(url_beginning + r'gifdeliverynetwork', url):
        return gifdeliverynetwork_download(url)
    elif re.match(url_beginning + r'(m\.)?imgur.*', url):
        return imgur_download(url)
    elif re.match(url_beginning + r'v\.redd\.it', url):
        return vreddit_download(url)
    elif re.match(url_beginning + r'(m\.)?youtu\.?be', url):
        return youtube_download(url)
    else:
        raise NotADownloadableLinkError(f'No downloader module exists for url {url}')


def download(url, directory, filename):

    downloaded = download_by_url(url)
    ret = []

    for i, (content, ext) in enumerate(downloaded):
        filename = directory + '/' + filename + str(i) + ext
        save_content(content, filename)
        ret.append(filename)

    return ret
