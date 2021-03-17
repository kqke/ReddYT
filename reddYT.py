from utils import *

from YT_upload import upload
from reddit_download import download

from tempfile import TemporaryDirectory
import os

# TODO:
#  1. Make program run in a framework-like manner i.e. the client can import the module,
#     define picker and compiler functions, and run the script


def run_reddit(pick_func):
    """
    Runs the reddit components of the script
    :param pick_func: Function to be used for picking clips. A default function will be used if not provided.
    :return: An iterable (? TODO) containing urls of the clips to be downloaded.
    """

    if not pick_func:
        pick_func = default_pick_func

    clip_urls = pick_func()

    # TODO - check for max len

    return clip_urls


def run_compile(compile_func, paths, output_dir):
    if not compile_func:
        compile_func = default_compile_func

    upload_path = compile_func(paths, output_dir=output_dir)

    if not os.path.exists(upload_path):
        exit(INVALID_FILE)

    return upload_path


def run(youtube_client_secret, pick_func=None, compile_func=None, download_args=None, upload_args=None):

    # Pick clips from reddit
    clip_urls = run_reddit(pick_func)

    # Get a temporary directory for the clips
    temp_dir = TemporaryDirectory()

    try:
        # Download clips
        if not download_args:
            download_args = {}
        downloaded_paths = download(urls=clip_urls, directory=temp_dir.name, **download_args)

        # Compile clips
        upload_path = run_compile(compile_func, downloaded_paths, temp_dir.name)

        # Upload compiled clip
        if not upload_args:
            upload_args = {}
        upload(upload_path, youtube_client_secret, **upload_args)

    finally:
        # Clean up temporary directory
        temp_dir.cleanup()


if __name__ == "__main__":
    run(**parse_args())
