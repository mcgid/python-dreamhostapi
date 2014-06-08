from dreamhostapi.exceptions import APIError


class Module(object):
    def __init__(self, name, call_function):
        self._name = name
        self._no_such_commands = []
        self._call = call_function

    def __getattr__(self, method_name):
        if method_name.startswith('__'):
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, method_name))

        if method_name in self._no_such_commands:
            raise AttributeError("API module '{}' has no command '{}'".format(self._name, method_name))

        def method(*args, **params):
            if args:
                raise TypeError('Parameters must be specified as keyword arguments')

            response = self._call(self._name + '-' + method_name, params)

            if response['result'] != 'success':
                if response['data'] == 'no_such_cmd':
                    self._no_such_commands.append(method_name)
                    delattr(self, method_name)
                    raise AttributeError("API module '{}' has no command '{}'".format(self._name, method_name))
                else:
                    raise APIError(response['data'])

            return response['data']

        setattr(self, method_name, method)

        return method

