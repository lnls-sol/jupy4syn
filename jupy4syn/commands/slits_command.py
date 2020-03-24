import os
import subprocess

from epics import PV
from jupy4syn.Configuration import Configuration
from jupy4syn.commands.ICommand import ICommand


class SlitsCommand(ICommand):
    def __init__(self, config=Configuration()):
        self.config = config

    def exec(self, parameters):
        if self.check_parameters(parameters):
            pvs_parameters = []
            for param in [item for item in parameters.split()]:
                if param[0] != '-':
                    try:
                        pvs_parameters.append(self.config.yml_motors[param]['pv'])
                    except KeyError:
                        pv = PV(param)
                        if not pv.wait_for_connection():
                            print("Invalid parameter:", param)

                        pvs_parameters.append(param)
                else:
                    pvs_parameters.append(param)

            # pvs_parameters = [self.config.yml_motors[motor]['pv'] for motor
            #                   in [item for item in parameters.split() if item != '--user']]

            subprocess.Popen(["slits_gui"] + pvs_parameters,
                             env=dict(os.environ, DISPLAY=self.config.display_number))
        else:
            raise ValueError("Invalid parameter")

    def args(self, initial_args):
        if not initial_args:
            return "-t <TOP> -b <BOTTOM> -l <LEFT> -r <RIGHT>"

        if isinstance(initial_args, str):
            return initial_args
        if isinstance(initial_args, (list, tuple)):
            return ' '.join(initial_args)

    def check_parameters(self, parameters):
        # if isinstance(parameters, str):
        #     if len(parameters.split()) <= 4:
        #         return True
        #     if len(parameters.split()) == 5 and '--user' in parameters:
        #         return True
        # elif isinstance(parameters, (list, tuple)):
        #     if len(parameters) <= 4:
        #         return True
        #     if len(parameters) == 5 and '--user' in parameters:
        #         return True
        # elif isinstance(parameters, dict):
        #     if "left" in parameters and "right" in parameters \
        #        and "top" in parameters and "bottom" in parameters:
        #         return True

        # # Otherwise
        # return False
        return True

    def text_box(self, initial_args):
        if not initial_args:
            return True, True

        return False, False
