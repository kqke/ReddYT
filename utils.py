from const import *
from argparse import ArgumentParser

import praw


from moviepy.editor import VideoFileClip, concatenate_videoclips


def default_compile_func(clips, transition=None, intro=None, middle=None, outro=None, output_dir='/'):

    to_concatenate = []
    output_file = output_dir + '/to_upload.mp4'

    if intro:
        to_concatenate.append(VideoFileClip(intro))

    added_mid = False if middle else True

    for i in range(len(clips)):
        if not added_mid and i > (len(clips) >> 1):
            to_concatenate.append(VideoFileClip(middle))
            added_mid = True
        to_concatenate.append(VideoFileClip(clips[i]))
        if transition:
            to_concatenate.append(VideoFileClip(transition))

    if outro:
        to_concatenate.append(VideoFileClip(outro))

    final_clip = concatenate_videoclips(to_concatenate)
    final_clip.write_videofile(output_file)

    return output_file


def default_pick_func():
    a = 'https://www.reddit.com/r/dataisbeautiful/comments/m6jkut/frequency_of_pi_digits_as_a_pie_chart_oc/?utm_source=share&utm_medium=web2x&context=3'
    b = 'https://www.reddit.com/r/WildernessBackpacking/comments/m6q84l/just_got_back_from_my_first_backpacking_trip_in/?utm_source=share&utm_medium=web2x&context=3'
    return [b, a]


def parse_args():
    parser = ArgumentParser(description=DESC, epilog=EPILOG)
    parser.add_argument(YT_LOGIN, metavar=META_YT_LOGIN, help=YT_HELP)
    parser.add_argument(PICKER, metavar=META_PICKER, help=PICKER_HELP)
    parser.add_argument(COMPILER, metavar=META_COMPILER, help=COMPILER_HELP)
    return vars(parser.parse_args())
