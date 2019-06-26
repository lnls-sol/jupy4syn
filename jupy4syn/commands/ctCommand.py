from scan_utils import ct

from jupy4syn.commands.ICommand import ICommand

class ctCommand(ICommand):
    def __init__(self):
        pass

    def exec(self, parameters):
        return ct.main(parameters.split())

    def args(self, initial_args):
        return initial_args

    def show(self, initial_args):
        return True
