import subprocess
import os

from jupy4syn.commands.ICommand import ICommand

class motorsCommand(ICommand):
    def __init__(self, config):
        self.config = config

    def exec(self, parameters):
        if self.check_parameters(parameters):
            subprocess.Popen(["motors"] + parameters.split(), env=dict(os.environ, DISPLAY=self.config.display_number))
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
                if "m1" in initial_args and "m2" in initial_args and "m3" in initial_args and "m4" in initial_args and "m5" in initial_args:
                    if 'user' in initial_args and initial_args['user']:
                        return ' '.join([initial_args["m1"], initial_args["m2"], initial_args["m3"], initial_args["m4"], initial_args["m5"], '--user'])
                    else:
                        return ' '.join([initial_args["m1"], initial_args["m2"], initial_args["m3"], initial_args["m4"], initial_args["m5"]])

    def show(self, initial_args):
        if not initial_args:
            return True
        else:
            return False 

    def check_parameters(self, parameters):
        if isinstance(parameters, str):
            if len(parameters.split()) == 5:
                return True
            elif len(parameters.split()) == 6 and '--user' in parameters:
                return True
        elif isinstance(parameters, (list, tuple)):
            if len(parameters) == 5:
                return True
            elif len(parameters) == 6 and '--user' in parameters:
                return True
        elif isinstance(parameters, dict):
            if "m1" in parameters and "m2" in parameters and "m3" in parameters and "m4" in parameters and "m5" in parameters:
                return True

        # Otherwise
        return False
        