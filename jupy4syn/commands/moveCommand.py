from scan_utils import move

from jupy4syn.commands.ICommand import ICommand

class moveCommand(ICommand):
    def __init__(self):
        pass

    def exec(self, parameters):
        return move.main(parameters.split())

    def args(self, initial_args):
        arg_str = ""

        if not initial_args:
            arg_str = "<motor1> <value1> <motor2> <value2> [...]"
        else:
            if isinstance(initial_args, (list, tuple)):
                for i in range(1, len(initial_args) + 1):
                    arg_str += initial_args[i - 1] + (" <value%d> " % i)
            else:
                arg_str += initial_args + " <value>"

        return arg_str

    def show(self, initial_args):
        return True
