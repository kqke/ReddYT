from utils import *

from YT_upload import upload
from reddit_download import download

from tempfile import TemporaryDirectory
import os


def run_reddit(pick_func=None):
    """
    Runs the reddit clip picker function.
    If pick_func is not specified, a default pick function will be used.
    :param pick_func: (func) Function to be used for picking clips.
    Must return an iterable containing urls to Reddit posts.
    :return: An iterable containing urls of the clips to be downloaded. (? TODO - iterable or something with max_len)
    """

    if not pick_func:
        pick_func = default_pick_func

    clip_urls = pick_func()

    return clip_urls


def run_compile(clip_paths, compile_func=None, output_dir='/'):
    """
    Runs the compilation function for a list of clips, specified by their path names.
    If no compile_func is not specified, a default compile function will be used.
    :param clip_paths: (List(str)) An iterable containing the path names to the clips to be compiled.
    :param compile_func: (func) Function to be used for compiling clips.
    Must have the following arguments:
    - "clip_paths" : accepts an iterable of file paths
    - "output_dir" : path to the directory in which the compiled output should be saved
    Must output the pathname of the file to which the compiled clip has been saved.
    :param output_dir: (str) Directory of the compiled output clip.
    :return: Pathname of the compiled output clip.
    """
    if not compile_func:
        compile_func = default_compile_func

    upload_path = compile_func(clip_paths=clip_paths, output_dir=output_dir)

    if not os.path.exists(upload_path):
        exit(INVALID_FILE)

    return upload_path


def run(youtube_client_secret, pick_func=None, compile_func=None, compile_args=None, download_args=None, upload_args=None):
    """
    Runs the different components of the ReddYT script.
    :param youtube_client_secret: (str) Path to the json file containing the client secret of the YT account
    to which the final clip will be uploaded to.
    :param pick_func: (func) Reference to a Reddit "picking" function,
    must return an iterable containing urls to Reddit posts.
    :param compile_func: (func) Reference to a function that compiles clips together to one compilation.
    Must have the following arguments:
    - "clip_paths" : accepts an iterable of file paths
    - "output_dir" : path to the directory in which the compiled output should be saved
    Must output the pathname of the file to which the compiled clip has been saved.
    :param compile_args: (dict) Arguments of the default compile func, specified in README (TODO)
    :param download_args: (dict) Arguments of the download function, specified in README (TODO)
    :param upload_args: (dict) Arguments of the upload function, specified in README (TODO)
    """
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
