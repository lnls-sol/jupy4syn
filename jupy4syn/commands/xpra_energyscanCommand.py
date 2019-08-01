import subprocess
import os

from jupy4syn.commands.ICommand import ICommand

class xpra_energyscanCommand(ICommand):
    def __init__(self, config):
        self.config = config

    def exec(self, parameters):
        subprocess.Popen(["energy_scan_gui", parameters], env=dict(os.environ, DISPLAY=":"+self.config.display_number))

    def args(self, initial_args):
        if not initial_args:
            return "<motor>"
        else:
            return initial_args

    def show(self, initial_args):
        if not initial_args:
            return True
        else:
            return False 
