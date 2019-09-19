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
            for motor in [item for item in parameters.split() if item != '--user']:
                try:
                    pvs_parameters.append(self.config.yml_motors[motor]['pv'])
                except KeyError:
                    pv = PV(motor)
                    if not pv.wait_for_connection():
                        raise ValueError("Invalid parameter")

                    pvs_parameters.append(motor)

            # pvs_parameters = [self.config.yml_motors[motor]['pv'] for motor
            #                   in [item for item in parameters.split() if item != '--user']]
            if '--user' in parameters:
                pvs_parameters.append('--user')

            subprocess.Popen(["slits"] + pvs_parameters,
                             env=dict(os.environ, DISPLAY=self.config.display_number))
        else:
            raise ValueError("Invalid parameter")

    def args(self, initial_args):
        if not initial_args:
            return "<m-left> <m-right> <m-top> <m-bot>"

        if isinstance(initial_args, str):
            return initial_args
        if isinstance(initial_args, (list, tuple)):
            return ' '.join(initial_args)
        if isinstance(initial_args, dict):
            valid_keys = ['left', 'right', 'top', 'bottom']
            parsed_args = []

            for key in valid_keys:
                parsed_args.append(initial_args[key])

            if 'user' in initial_args.keys() and initial_args['user']:
                parsed_args.append('--user')

            return ' '.join(parsed_args)

    def check_parameters(self, parameters):
        if isinstance(parameters, str):
            if len(parameters.split()) <= 4:
                return True
            if len(parameters.split()) == 5 and '--user' in parameters:
                return True
        elif isinstance(parameters, (list, tuple)):
            if len(parameters) <= 4:
                return True
            if len(parameters) == 5 and '--user' in parameters:
                return True
        elif isinstance(parameters, dict):
            if "left" in parameters and "right" in parameters \
               and "top" in parameters and "bottom" in parameters:
                return True

        # Otherwise
        return False

    def text_box(self, initial_args):
        if not initial_args:
            return True, True

        return False, False
