import os
from tempfile import TemporaryDirectory

from exceptions import *

from reddit_downloader import download
from clip_compiler import compile_clips
from YT_upload import upload


def yield_and_download(reddit_generator, directory, limit=10):

    if limit <= 0:
        raise ValueError('Please enter a positive limit')

    if not os.path.exists(directory):
        raise ValueError('Please enter an existing directory path')

    downloaded = []

    while limit:
        try:
            submission = next(reddit_generator)
            downloaded_submission = download(submission.url, directory, submission.id)
            downloaded.extend(downloaded_submission)
            limit -= len(downloaded_submission)
        except DownloadException:
            # Log the error and move to next clip
            continue
        except StopIteration:
            if not downloaded:
                raise RedditException('Reddit generator did not yield any valid submissions')
            break

    return downloaded


def download_compile_upload(youtube_client_secret,
                            reddit_generator,
                            reddit_limit=10,
                            compile_args=None,
                            upload_args=None):
    """
    Runs the different components of the ReddYT script.
    :param youtube_client_secret: (str) Path to the json file containing the client secret of the YT account
    to which the final clip will be uploaded to.
    :param reddit_generator: TODO
    :param reddit_limit: TODO
    :param compile_args: (dict) Arguments of the default compile func, specified in README (TODO)
    :param upload_args: (dict) Arguments of the upload function, specified in README (TODO)
    """

    # Get a temporary directory for the clips
    with TemporaryDirectory() as temp_dir:

        # Download clips from reddit
        downloaded_paths = yield_and_download(reddit_generator, temp_dir, reddit_limit)

        # Compile clips
        if not compile_args:
            compile_args = {}
        upload_path = compile_clips(clip_paths=downloaded_paths, output_dir=temp_dir, **compile_args)

        # Upload compiled clip
        if not upload_args:
            upload_args = {}
        upload(upload_path, youtube_client_secret, **upload_args)


if __name__ == "__main__":
    pass
    # run(**parse_args())
