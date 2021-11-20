class BasePicker:

    def __init__(self):
        pass

    def pick(self, *args, **kwargs):
        raise NotImplementedError("You must implement this method")

    def __call__(self, *args, **kwargs):
        return self.pick(*args, **kwargs)

