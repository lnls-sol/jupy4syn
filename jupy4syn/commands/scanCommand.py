import subprocess

from jupy4syn.commands.ICommand import ICommand

class scanCommand(ICommand):
    def __init__(self):
        pass

    def exec(self, parameters):
        subprocess.Popen(["scan_gui"])

    def args(self, initial_args):
        return initial_args

    def show(self, initial_args):
        return False
