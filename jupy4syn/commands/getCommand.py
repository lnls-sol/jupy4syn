from epics import PV, caget

from jupy4syn.commands.ICommand import ICommand

class getCommand(ICommand):
    def __init__(self, config):
        self.config = config

    def exec(self, parameters):
        print(self.pv_name, "\t\t", self.pv.get(as_string=self.pv_is_enum))

    def args(self, initial_args):
        # Parameter checking
        if not initial_args:
            raise ValueError("PV name or mnemonic can not be empty.")
        elif not isinstance(initial_args, str):
            raise ValueError("PV name or mnemonic must be a string.")

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
                raise ValueError("Invalid name. Name provided is neither a conencted PV neither a config.yml mnemonic")

            # Check if PV is finally connected
            if not self.pv.wait_for_connection():
                raise Exception("Valid name, but PV connection not possible")


        self.pv_desc = caget(self.pv.pvname + ".DESC")
        self.pv_name = self.pv.pvname

        # If PV is an enum, when its value is get, we get it with "as_string" set to True, so we get
        # the enum string value, not the enum int value
        self.pv_is_enum = True if self.pv.type == "enum" or self.pv.type == "time_enum" else False

        return ""

    def show(self, initial_args):
        return False
