import subprocess

from jupy4syn.commands.ICommand import ICommand

class energyscanCommand(ICommand):
    def __init__(self):
        pass

    def exec(self, parameters):
        subprocess.Popen(["energy_scan_gui", parameters])

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
