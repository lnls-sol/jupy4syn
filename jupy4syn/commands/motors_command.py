import os
import subprocess

from epics import PV
from jupy4syn.Configuration import Configuration
from jupy4syn.commands.ICommand import ICommand


class MotorsCommand(ICommand):
    def __init__(self, config=Configuration()):
        self.config = config

    def exec(self, parameters):
        if self.check_parameters(parameters):
            pvs_parameters = []
            for motor in [item for item in parameters.split() if item[0:1] != '--']:
                try:
                    pvs_parameters.append(self.config.yml_motors[motor]['pv'])
                except KeyError:
                    pv = PV(motor)
                    if not pv.wait_for_connection():
                        raise ValueError("Invalid parameter")

                    pvs_parameters.append(motor)

            flags = [item for item in parameters.split() if item[0:1] == '--']
            for flag in flags:
                pvs_parameters.append(flag)

            subprocess.Popen(["motors_gui"] + pvs_parameters,
                             env=dict(os.environ, DISPLAY=self.config.display_number))
        else:
            raise ValueError("Invalid parameter")

    def args(self, initial_args):
        if not initial_args:
            return "<m1> <m2> <m3> <m4> ..."

        if isinstance(initial_args, str):
            return initial_args
        if isinstance(initial_args, (list, tuple)):
            return ' '.join(initial_args)

    def check_parameters(self, parameters):
        # if isinstance(parameters, str):
        #     if len(parameters.split()) <= 5:
        #         return True
        #     if len(parameters.split()) == 6 and '--user' in parameters:
        #         return True
        # elif isinstance(parameters, (list, tuple)):
        #     if len(parameters) <= 5:
        #         return True
        #     if len(parameters) == 6 and '--user' in parameters:
        #         return True

        # # Otherwise
        # return False
        return True

    def text_box(self, initial_args):
        if not initial_args:
            return True, True

        return False, False
