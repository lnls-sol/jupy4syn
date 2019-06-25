import subprocess

from jupy4syn.commands.ICommand import ICommand

class pymcaCommand(ICommand):
    def __init__(self):
        pass

    def exec(self, parameters):
        subprocess.Popen(["pymca"])

    def args(self, initial_args):
        return initial_args

    def show(self, initial_args):
        return False
