import sys


def register_exception_hooks(cls):
    def add_exception_hook(name):
        existing = getattr(cls, name, None)

        def exc_hook(self, *args, **kwargs):
            if existing is not None:
                try:
                    return existing(self, *args, **kwargs)
                except Exception as e:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    sys.excepthook(exc_type, exc_value, exc_tb)

        try:
            # Don't replace anything but methods
            if callable(existing):
                setattr(cls, name, exc_hook)
        except (AttributeError, TypeError):
            pass

    class_methods = [name for name in dir(cls) if not name.startswith('__') and not name.endswith('__')]

    for method_name in class_methods:
        add_exception_hook(method_name)

    return cls
