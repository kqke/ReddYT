from redvid import Downloader
import warnings


DOWNLOAD_EXCEPTION = 'Wasn\'t able to download video at:\n%s\nWith the following exception message:\n%s'
MOVING_ON = 'Moving on to next clip...'


def download(
                    urls,
                    directory="",
                    max_s=1e1000,
                    max_d=1e1000,
                    max_q=False,
                    min_q=False,
                    auto_max=True
                    ):
    """
    Downloads the Reddit videos specified by urls to the directory specified by directory.
    :param urls: (List(str)) An iterable containing urls to Reddit posts with video hosted on Reddit.
    :param directory: (str) A directory for saving the clips.
    :param max_s: (int) Maximum size of video to be downloaded.
    :param max_d: (int) Maximum duration of video to be downloaded.
    :param max_q: (bool) Get video with maximum quality.
    :param min_q: (bool) Get video with minimum quality.
    :param auto_max: (bool) Should the maximum available quality be used automatically?
    :return: A list of the path names of the downloaded files.
    """
    downloaded = []

    for url in urls:
        reddit = Downloader(url=url,
                            path=directory,
                            max_q=max_q,
                            min_q=min_q,
                            max_d=max_d,
                            max_s=max_s,
                            auto_max=auto_max)
        try:
            file_path = reddit.download()
            downloaded.append(file_path)
        except Exception as exception:
            print(DOWNLOAD_EXCEPTION % (url, exception))
            warnings.warn(DOWNLOAD_EXCEPTION % (url, exception))
            print(MOVING_ON)
            continue

    return downloaded
