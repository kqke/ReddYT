from const import *
from argparse import ArgumentParser


def parse_args():
    # TODO
    parser = ArgumentParser(description=DESC, epilog=EPILOG)
    parser.add_argument(YT_LOGIN, metavar=META_YT_LOGIN, help=YT_HELP)
    parser.add_argument(PICKER, metavar=META_PICKER, help=PICKER_HELP)
    parser.add_argument(COMPILER, metavar=META_COMPILER, help=COMPILER_HELP)
    return vars(parser.parse_args())
