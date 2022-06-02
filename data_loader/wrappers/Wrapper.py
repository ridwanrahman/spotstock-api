class Wrapper(object):
    subclasses = {}

    def __init__(self):
        pass

    @classmethod
    def register_subclass(cls, wrapper_type):
        def decorator(subclass):
            cls.subclasses[wrapper_type] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, wrapper_type):
        if wrapper_type not in cls.subclasses:
            raise ValueError('Bad message type {}'.format(wrapper_type))

        return cls.subclasses[wrapper_type]()
