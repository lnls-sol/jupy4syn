from epics import PV, caget
from jupy4syn.commands.ICommand import ICommand


class PutCommand(ICommand):

    def __init__(self, config):
        self.config = config
        self.name = ""
        self.pv_desc = ""
        self.pv = ""
        self.pv_name = ""
        self.pv_is_enum = False

    def exec(self, parameters):
        self.pv.put(parameters, wait=False)

    def args(self, initial_args):
        if not isinstance(initial_args, str):
            if not initial_args:
                raise ValueError("Argument list can not be empty.")
            if not isinstance(initial_args, list) and len(initial_args) > 2:
                raise ValueError("Argument must be a list with at most two elements. The PV and \
                                  the optional value to set.")
            # Parameter checking
            if not initial_args[0]:
                raise ValueError("PV name or mnemonic can not be empty.")
            if not isinstance(initial_args[0], str):
                raise ValueError("PV name or mnemonic must be a string.")

            self.name = initial_args[0]
        else:
            if not initial_args:
                raise ValueError("PV name or mnemonic can not be empty.")

            self.name = initial_args
            initial_args = [initial_args]

        self.pv = PV(self.name)

        if not self.pv.wait_for_connection():
            if self.name in self.config.yml_motors:
                try:
                    self.pv = PV(self.config.yml_motors[self.name]['pv'])
                except KeyError:
                    raise ValueError('Motor %s doesn\'t have pv field' % self.name)
            elif self.name in self.config.yml_counters:
                try:
                    self.pv = PV(self.config.yml_counters[self.name]['pv'])
                except KeyError:
                    raise ValueError('Counter %s doesn\'t have pv field' % self.name)
            else:
                raise ValueError("Invalid name. Name provided is neither a conencted PV neither a \
                                  config.yml mnemonic")

            # Check if PV is finally connected
            if not self.pv.wait_for_connection():
                raise Exception("Valid name, but PV connection not possible")

        self.pv_desc = caget(self.pv.pvname + ".DESC")
        self.pv_name = self.pv.pvname

        if len(initial_args) == 2:
            return str(initial_args[1])
        if len(initial_args) == 1:
            # If PV is an enum, when its value is get, we get it with "as_string" set to True, so we
            # get the enum string value, not the enum int value
            self.pv_is_enum = (self.pv.type == "enum" or self.pv.type == "time_enum")
            return str(self.pv.get(as_string=self.pv_is_enum))

    def text_box(self, initial_args):
        if isinstance(initial_args, (list, tuple)) and len(initial_args) == 2:
            return True, False

        return True, True
