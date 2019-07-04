import os
import subprocess

from jupy4syn.commands.ICommand import ICommand

class xpra_slitsCommand(ICommand):
    def __init__(self, config):
        self.config = config

    def exec(self, parameters):
        if self.check_parameters(parameters):
            pvs_parameters = [self.config.yml_motors[motor]["pv"] for motor in parameters]

            subprocess.Popen(["slits"] + pvs_parameters, env=dict(os.environ, DISPLAY=":"+self.config.display_number))
        else:
            raise ValueError("Invalid parameter")

    def args(self, initial_args):
        if not initial_args:
            return "<m-left> <m-right> <m-top> <m-bot>"
        else:
            if isinstance(initial_args, str):
                return initial_args.split()
            elif isinstance(initial_args, (list, tuple)):
                return initial_args
            elif isinstance(initial_args, dict):
                if "left" in initial_args and "right" in initial_args and "top" in initial_args and "bottom" in initial_args:
                    return [initial_args["left"], initial_args["right"], initial_args["top"], initial_args["bottom"]]

    def show(self, initial_args):
        if not initial_args:
            return True
        else:
            return False 

    def check_parameters(self, parameters):
        if isinstance(parameters, str):
            if len(parameters.split()) == 4:
                return True
        elif isinstance(parameters, (list, tuple)):
            if len(parameters) == 4:
                return True
        elif isinstance(parameters, dict):
            if "left" in parameters and "right" in parameters and "top" in parameters and "bottom" in parameters:
                return True

        # Otherwise
        return False
        