from epics import PV, caget
from jupy4syn.commands.ICommand import ICommand


class GetCommand(ICommand):

    def __init__(self, config):
        self.config = config
        self.name = ""
        self.pv_desc = ""
        self.pv = ""
        self.pv_name = ""
        self.pv_is_enum = False

    def exec(self, parameters):
        print(self.pv_name, "\t\t", self.pv.get(as_string=self.pv_is_enum))

    def args(self, initial_args):
        # Parameter checking
        if not initial_args:
            raise ValueError("PV name or mnemonic can not be empty.")
        if not isinstance(initial_args, str):
            if isinstance(initial_args, (list, tuple)) and len(initial_args) == 1:
                initial_args = initial_args[0]
            else:
                raise ValueError("PV name or mnemonic must be a string or a list with a string.")

        self.name = initial_args
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
                raise ValueError("Invalid name. Name provided is neither a conencted PV neither \
                                  a config.yml mnemonic")

            # Check if PV is finally connected
            if not self.pv.wait_for_connection():
                raise Exception("Valid name, but PV connection not possible")

        self.pv_desc = caget(self.pv.pvname + ".DESC")
        self.pv_name = self.pv.pvname

        # If PV is an enum, when its value is get, we get it with "as_string" set to True, so we get
        # the enum string value, not the enum int value
        self.pv_is_enum = (self.pv.type == "enum" or self.pv.type == "time_enum")

        return ""

    def text_box(self, initial_args):
        return False, False
