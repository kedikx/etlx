
class RowX:
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        for seq in args:
            if isinstance(seq, dict):
                seq = seq.items()
            for key, value in seq:
                setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

