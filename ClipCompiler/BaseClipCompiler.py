class BaseClipCompiler:

    def __init__(self):
        pass

    def compile(self, clip):
        raise NotImplementedError("BaseClipCompiler.compile()")

    def get_clip_type(self):
        raise NotImplementedError("BaseClipCompiler.get_clip_type()")

    def get_clip_name(self):
        raise NotImplementedError("BaseClipCompiler.get_clip_name()")

    def get_clip_description(self):
        raise NotImplementedError("BaseClipCompiler.get_clip_description()")
