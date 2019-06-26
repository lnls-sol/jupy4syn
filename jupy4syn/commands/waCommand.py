from scan_utils import wa

from jupy4syn.commands.ICommand import ICommand

class waCommand(ICommand):
    def __init__(self):
        pass

    def exec(self, parameters):
        return wa.main()

    def args(self, initial_args):
        return initial_args

    def show(self, initial_args):
        return False
