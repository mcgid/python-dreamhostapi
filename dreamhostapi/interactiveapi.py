from dreamhostapi.api import DreamHostAPI
from dreamhostapi.exceptions import APIError

# Replacement __dir__ function for Modules
def _available_commands_dir(self):
    # Return a list of str objects instead of unicode objects
    commands = [c.encode(errors='ignore') for c in self._available_commands.iterkeys()]
    return sorted(commands)

class InteractiveAPI(DreamHostAPI):
    def __init__(self, key):
        super(InteractiveAPI, self).__init__(key)
        self._available_modules = self._get_available_modules()

    def __getattr__(self, module_name):
        if module_name not in self._available_modules:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, module_name))

        module = super(InteractiveAPI, self).__getattr__(module_name)

        module._available_commands = self._available_modules[module_name]

        # Replace the Module class's __dir__ method
        # Note: dir() seems to call the __dir__ method of the class, not the
        #       instance, even if the instance has its own bound __dir__.
        #       This isn't preferable, but I'm not sure what else to do.
        module.__class__.__dir__ = _available_commands_dir

        return module

    def __dir__(self):
        # Return a list of str objects instead of unicode objects
        modules = [m.encode(errors='ignore') for m in self._available_modules.iterkeys()]
        return sorted(modules)

    def _get_available_modules(self):
        available_modules = {}

        response = self._call('api-list_accessible_cmds')

        if response['result'] != 'success':
            # api-list_accessible_cmds should not ever fail
            raise APIError('Listing accessible commands failed: ' + response['data'])

        data = response['data']

        for command in data:
            module, command_name = command['cmd'].split('-')
            args = command['args']
            optargs = command['optargs']
            return_vals = command['order']

            if module not in available_modules:
                available_modules[module] = {}

            available_modules[module][command_name] = (args, optargs, return_vals)

        return available_modules
