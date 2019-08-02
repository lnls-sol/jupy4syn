import os
import subprocess

from jupy4syn.Configuration import Configuration
from jupy4syn.commands.ICommand import ICommand

class vortexCommand(ICommand):
    def __init__(self, config=Configuration()):
        self.config = config

    def exec(self, parameters):
        subprocess.Popen(["vortex", "-m", parameters], env=dict(os.environ, DISPLAY=self.config.display_number)) 

    def args(self, initial_args):
        if not initial_args:
            return "P=<PV>"
        else:
            return initial_args

    def show(self, initial_args):
        if not initial_args:
            return True
        else:
            return False  
