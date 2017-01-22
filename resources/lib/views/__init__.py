import sys


def register_exception_hooks(cls):
    def add_exception_hook(name):
        existing = getattr(cls, name, None)

        def exc_hook(self, *args, **kw):
            if existing is not None:
                try:
                    return existing(self, *args, **kw)
                except Exception, e:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    sys.excepthook(exc_type, exc_value, exc_tb)
            raise AttributeError(name)

        try:
            setattr(cls, name, exc_hook)
        except (AttributeError, TypeError):
            pass

    class_methods = [name for name in dir(cls) if not name.startswith('__') and not name.endswith('__')]
    for method_name in class_methods:
        add_exception_hook(method_name)
    return cls
