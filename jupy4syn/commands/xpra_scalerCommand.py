import subprocess

from jupy4syn.commands.ICommand import ICommand

class xpra_scalerCommand(ICommand):
    def __init__(self):
        pass

    def exec(self, parameters):
        p = subprocess.Popen(["DISPLAY=:100", "scaler -m " + parameters], stdout=subprocess.PIPE)
        stdout = p.communicate()[0]
        print(stdout)

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
