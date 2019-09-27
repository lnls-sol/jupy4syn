import pandas as pd
import matplotlib.pyplot as plt
import IPython
from jupy4syn.commands.ICommand import ICommand


class PlotCommand(ICommand):

    def __init__(self, show_header):
        self.show_header = show_header

    def exec(self, parameters):
        parsed_parameters = parameters.split(" ")

        labels = None
        e_line = d_line = c_line = ''
        with open(parsed_parameters[0]) as file:
            for _, line in enumerate(file):
                if line[0:3] == "#L ":
                    labels = line.split(' ')[1:]
                    labels = [label.rstrip('\n') for label in labels if label != '']
                elif line[0:3] == "#E ":
                    e_line = (line.split(' ', maxsplit=1)[-1]).strip('\n')
                elif line[0:3] == "#D ":
                    d_line = (line.split(' ', maxsplit=1)[-1]).strip('\n')
                elif line[0:3] == "#C ":
                    c_line = (line.split(' ', maxsplit=1)[-1]).strip('\n')

            if self.show_header:
                print('#E', e_line)
                print('#D', d_line)
                print('#C', c_line)
                print('#L', str(labels))

        data_frame = pd.read_csv(parsed_parameters[0], sep=' ', comment='#', header=None)
        data_frame.columns = pd.Index(labels, dtype='object')

        plt.figure()

        for i in range(int(parsed_parameters[1])):
            plt.subplot(int(parsed_parameters[1]), 1, i + 1)

            plt.xlabel(parsed_parameters[2])
            plt.ylabel(parsed_parameters[2 + i + 1])

            plt.plot(parsed_parameters[2], parsed_parameters[2 + i + 1], data=data_frame)

        plt.show()

    def args(self, initial_args):
        arg_str = ""
        parameters = initial_args

        if not initial_args:
            arg_str = "<filename> <number_of_yaxis> <xaxis> <yaxis1> <yaxis2> [...]"
        else:
            if isinstance(parameters, str):
                parameters = parameters.split(" ")

            if isinstance(parameters, (list, tuple)):
                if not isinstance(parameters[0], str):
                    raise ValueError("Invalid parameter")
                if not isinstance(int(parameters[1]), int):
                    raise ValueError("Invalid parameter")
                if len(parameters) < 4:
                    raise ValueError("Invalid parameter")
                arg_str = ' '.join(parameters)

            elif isinstance(parameters, dict):
                arg_str += parameters['filename'] + ' '
                arg_str += parameters['number_of_yaxis'] + ' '
                arg_str += parameters['xaxis'] + ' '
                for yaxis in parameters['yaxe']:
                    arg_str += yaxis + ' '
            else:
                raise ValueError("Invalid parameter")

        return arg_str

    def text_box(self, initial_args):
        if not initial_args:
            return True, True

        return False, False
