import subprocess

from jupy4syn.commands.ICommand import ICommand

class motorsCommand(ICommand):
    def __init__(self, config):
        self.config = config

    def exec(self, parameters):
        if self.check_parameters(parameters):
            pvs_parameters = [self.config.yml_motors[motor]["pv"] for motor in parameters]

            subprocess.Popen(["slits"] + pvs_parameters)
        else:
            raise ValueError("Invalid parameter")

    def args(self, initial_args):
        if not initial_args:
            return "<m1> <m2> <m3> <m4> <m5>"
        else:
            if isinstance(initial_args, str):
                return initial_args.split()
            elif isinstance(initial_args, (list, tuple)):
                return initial_args
            elif isinstance(initial_args, dict):
                if "m1" in initial_args and "m2" in initial_args and "m3" in initial_args and "m4" in initial_args and "m5" in initial_args:
                    return [initial_args["m1"], initial_args["m2"], initial_args["m3"], initial_args["m4"], initial_args["m5"]]

    def show(self, initial_args):
        if not initial_args:
            return True
        else:
            return False 

    def check_parameters(self, parameters):
        if isinstance(parameters, str):
            if len(parameters.split()) == 5:
                return True
        elif isinstance(parameters, (list, tuple)):
            if len(parameters) == 5:
                return True
        elif isinstance(parameters, dict):
            if "m1" in parameters and "m2" in parameters and "m3" in parameters and "m4" in parameters and "m5" in parameters:
                return True

        # Otherwise
        return False
        