from scan_utils import wm
from jupy4syn.commands.ICommand import ICommand


class WmCommand(ICommand):

    def __init__(self):
        pass

    def exec(self, parameters):
        return wm.main(parameters.split())

    def args(self, initial_args):
        arg_str = ""

        if not initial_args:
            arg_str = "<motor1> <motor2> [...]"
        else:
            if isinstance(initial_args, (list, tuple)):
                for motor in initial_args:
                    arg_str += motor + " "
            else:
                arg_str += initial_args

        return arg_str

    def text_box(self, initial_args):
        if not initial_args:
            return True, True

        return False, False
