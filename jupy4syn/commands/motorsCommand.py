import os
import subprocess

from jupy4syn.Configuration import Configuration
from jupy4syn.commands.ICommand import ICommand

class motorsCommand(ICommand):
    def __init__(self, config=Configuration()):
        self.config = config

    def exec(self, parameters):
        if self.check_parameters(parameters):
            pvs_parameters = [self.config.yml_motors[motor]['pv'] for motor in [item for item in parameters.split() if item != '--user']]
            if '--user' in parameters:
                pvs_parameters.append('--user')

            subprocess.Popen(["motors_gui"] + parameters.split(), env=dict(os.environ, DISPLAY=self.config.display_number))
        else:
            raise ValueError("Invalid parameter")

    def args(self, initial_args):
        if not initial_args:
            return "<m1> <m2> <m3> <m4> <m5>"
        else:
            if isinstance(initial_args, str):
                return initial_args
            elif isinstance(initial_args, (list, tuple)):
                return ' '.join(initial_args)
            elif isinstance(initial_args, dict):
                parsed_args = []
                # if "m1" in initial_args and "m2" in initial_args and "m3" in initial_args and "m4" in initial_args and "m5" in initial_args:
                #     parsed_args = [initial_args["m1"], initial_args["m2"], initial_args["m3"], initial_args["m4"], initial_args["m5"]]
                # elif "m1" in initial_args and "m2" in initial_args and "m3" in initial_args and "m4":
                #     parsed_args = [initial_args["m1"], initial_args["m2"], initial_args["m3"], initial_args["m4"]]
                # elif "m1" in initial_args and "m2" in initial_args and "m3":
                #     parsed_args = [initial_args["m1"], initial_args["m2"], initial_args["m3"]]
                # elif "m1" in initial_args and "m2":
                #     parsed_args = [initial_args["m1"], initial_args["m2"]]
                # elif "m1" in initial_args:
                #     parsed_args = [initial_args["m1"]]

                valid_keys = ['m1', 'm2', 'm3', 'm4', 'm5']
                for key in [valid_key for valid_key in initial_args.keys() if valid_key in valid_keys]:
                    parsed_args.append(initial_args[key])

                if 'user' not in initial_args or ('user' in initial_args and not initial_args['user']):
                    parsed_args.append('--user')

                return ' '.join(parsed_args)

                

    def show(self, initial_args):
        if not initial_args:
            return True
        else:
            return False 

    def check_parameters(self, parameters):
        if isinstance(parameters, str):
            if len(parameters.split()) <= 5:
                return True
            elif len(parameters.split()) == 6 and '--user' in parameters:
                return True
        elif isinstance(parameters, (list, tuple)):
            if len(parameters) <= 5:
                return True
            elif len(parameters) == 6 and '--user' in parameters:
                return True
        elif isinstance(parameters, dict):
            if "m1" in parameters and "m2" in parameters and "m3" in parameters and "m4" in parameters and "m5" in parameters:
                return True

        # Otherwise
        return False
        