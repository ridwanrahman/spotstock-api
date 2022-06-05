class Wrapper(object):
    """
    This class will load other classes that have the register_subclass decorator.
    """
    subclasses = {}

    def __init__(self):
        pass

    @classmethod
    def register_subclass(cls, wrapper_type):
        """
        register_subclass function will enter the different classes that have the register_subclass
        into the subclasses dict
        """
        def decorator(subclass):
            cls.subclasses[wrapper_type] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, wrapper_type):
        """
        Create function will create the different wrapper classes that are called by their
        register_subclass name
        """
        if wrapper_type not in cls.subclasses:
            raise ValueError('Bad message type {}'.format(wrapper_type))

        return cls.subclasses[wrapper_type]()
