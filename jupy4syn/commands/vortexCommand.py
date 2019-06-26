import subprocess

from jupy4syn.commands.ICommand import ICommand

class vortexCommand(ICommand):
    def __init__(self):
        pass

    def exec(self, parameters):
        subprocess.Popen(["vortex", "-m", parameters]) 

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
