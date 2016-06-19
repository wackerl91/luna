class LazyProxy(object):
    def __init__(self, original_module, original_class, init_args):
        self._original_module = original_module
        self._original_class = original_class
        self._original_init_args = init_args
        self._instance = None

    def __getattr__(self, name):
        if self._instance is None:
            self.__init_class__()

        return getattr(self._instance, name)

    def __init_class__(self):
        import importlib
        module = importlib.import_module(self._original_module)
        class_ = getattr(module, self._original_class)

        if self._original_init_args is not None:
            for index, arg in enumerate(self._original_init_args):
                if arg[:1] == '@':
                    from resources.lib.di.requiredfeature import RequiredFeature
                    self._original_init_args[index] = RequiredFeature(arg[1:]).request()
            import inspect
            args = inspect.getargspec(class_.__init__)[0]
            if args[0] == 'self':
                args.pop(0)
            argument_dict = dict(zip(args, self._original_init_args))

            self._instance = class_(**argument_dict)
        else:
            self._instance = class_()
