import os
import subprocess

from jupy4syn.Configuration import Configuration
from jupy4syn.commands.ICommand import ICommand


class ScanGuiCommand(ICommand):

    def __init__(self, config=Configuration()):
        self.config = config

    def exec(self, parameters):
        subprocess.Popen(["scan_gui"], env=dict(os.environ, DISPLAY=self.config.display_number))

    def args(self, initial_args):
        return initial_args

    def text_box(self, initial_args):
        return False, False
