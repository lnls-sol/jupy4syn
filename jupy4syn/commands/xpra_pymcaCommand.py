import subprocess
import os

from jupy4syn.commands.ICommand import ICommand

class pymcaCommand(ICommand):
    def __init__(self, config):
        self.config = config

    def exec(self, parameters):
        subprocess.Popen(["pymca"], env=dict(os.environ, DISPLAY=":"+self.config.display_number))

    def args(self, initial_args):
        return initial_args

    def show(self, initial_args):
        return False
