from utils import *

from downloaders.reddit_download import download
from clip_compiler import clip_compiler as default_compile_func
from YT_upload import upload

from tempfile import TemporaryDirectory
from functools import partial
import os


# TODO - Make runnable from command-line, with user providing inputs via commandline or config file.
# TODO - Make runnable as a library/framework


def run(args):
    download_compile_upload(**args)


def download_compile_upload(youtube_client_secret,
                            reddit_clips,
                            compile_func=None,
                            compile_args=None,
                            download_args=None,
                            upload_args=None):
    """
    Runs the different components of the ReddYT script.
    :param youtube_client_secret: (str) Path to the json file containing the client secret of the YT account
    to which the final clip will be uploaded to.
    :param reddit_clips: (list(str)) An iterable containing urls to Reddit posts.
    :param compile_func: (func) Reference to a function that compiles clips together to one compilation.
    Must have the following arguments:
    - "clip_paths" : accepts an iterable of file paths
    - "output_dir" : path to the directory in which the compiled output should be saved
    Must output the pathname of the file to which the compiled clip has been saved.
    :param compile_args: (dict) Arguments of the default compile func, specified in README (TODO)
    :param download_args: (dict) Arguments of the download function, specified in README (TODO)
    :param upload_args: (dict) Arguments of the upload function, specified in README (TODO)
    """

    # Get a temporary directory for the clips
    with TemporaryDirectory() as temp_dir:

        # Download clips from reddit
        if not download_args:
            download_args = {}
        downloaded_paths = download(urls=reddit_clips, directory=temp_dir.name, **download_args)

        # Compile clips
        if not compile_func:
            compile_func = partial(default_compile_func, **compile_args)
        upload_path = compile_func(clip_paths=downloaded_paths, output_dir=temp_dir.name)
        if not os.path.exists(upload_path):
            exit(INVALID_FILE)

        # Upload compiled clip
        if not upload_args:
            upload_args = {}
        upload(upload_path, youtube_client_secret, **upload_args)


if __name__ == "__main__":
    run(**parse_args())
