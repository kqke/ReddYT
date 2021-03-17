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
