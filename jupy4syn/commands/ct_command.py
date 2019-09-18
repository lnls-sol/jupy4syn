from scan_utils import ct

from jupy4syn.commands.ICommand import ICommand


class CtCommand(ICommand):

    def __init__(self):
        pass

    def exec(self, parameters):
        return ct.main(parameters.split())

    def args(self, initial_args):
        return initial_args

    def text_box(self, initial_args):
        if not initial_args:
            return True, True

        return False, False
