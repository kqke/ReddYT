from moviepy.editor import VideoFileClip, concatenate_videoclips


def clip_compiler(clip_paths, transition=None, intro=None, middle=None, outro=None, output_dir='/'):
    """
    Default compiler func for ReddYT.
    Concatenates the clips to each other,
    with optional intro, transition, halfway point, and outro clips added to the final output.
    :param clip_paths: (List(str)) An iterable containing the file paths of the clips to be compiled.
    :param transition: (str) A filepath to the transition clip.
    :param intro: (str) A filepath to the intro clip.
    :param middle: (str) A filepath to the halfway point clip,
    will be concatenated to the compilation once more than half of the clips have been processed.
    :param outro: (str) A filepath to the outro clip.
    :param output_dir: (str) A filepath to the directory in which the output file should be saved.
    :return: A filepath to the output file.
    """
    to_concatenate = []
    output_file = output_dir + '/to_upload.mp4'

    if intro:
        to_concatenate.append(VideoFileClip(intro))

    transition_clip = VideoFileClip(transition) if transition else None

    added_mid = False if middle else True

    for i in range(len(clip_paths)):
        if not added_mid and i > (len(clip_paths) >> 1):
            to_concatenate.append(VideoFileClip(middle))
            added_mid = True
        to_concatenate.append(VideoFileClip(clip_paths[i]))
        if transition:
            to_concatenate.append(transition_clip)

    if outro:
        to_concatenate.append(VideoFileClip(outro))

    final_clip = concatenate_videoclips(to_concatenate)
    final_clip.write_videofile(output_file)

    return output_file
