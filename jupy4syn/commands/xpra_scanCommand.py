import subprocess

from jupy4syn.commands.ICommand import ICommand

class xpra_scanCommand(ICommand):
    def __init__(self):
        pass

    def exec(self, parameters):
        p = subprocess.Popen(["scan_gui"], env=dict(DISPLAY=":100"), stdout=subprocess.PIPE)
        stdout = p.communicate()[0]
        print(stdout)

    def args(self, initial_args):
        return initial_args

    def show(self, initial_args):
        return False
