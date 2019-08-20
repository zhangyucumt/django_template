class EnumObject(object):

    @classmethod
    def choices(cls):
        choices = []
        for k, v in cls.__dict__.items():
            if not k.startswith('__'):
                choices.append([v, k])
        return choices

    @classmethod
    def dict(cls):
        data = {}
        for k, v in cls.__dict__.items():
            if not k.startswith('__'):
                data[k] = v
        return data

    @classmethod
    def reverse_dict(cls):
        data = {}
        for k, v in cls.__dict__.items():
            if not k.startswith('__'):
                data[v] = k
        return data

