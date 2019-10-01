import pandas as pd
import matplotlib.pyplot as plt


class SpecPlot():

    def __init__(self, parameters, show_header=False):
        self.show_header = show_header
        parsed_parameters = self.parse_args(parameters).split(" ")

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

        self.data_frame = pd.read_csv(parsed_parameters[0], sep=' ', comment='#', header=None)
        self.data_frame.columns = pd.Index(labels, dtype='object')

        self.diff_data_frame = self.data_frame.copy()
        self.diff_data_frame.iloc[:, 1:] = self.diff_data_frame.iloc[:, 1:].diff().fillna(0)

        plt.figure()

        for i in range(int(parsed_parameters[1])):
            plt.subplot(int(parsed_parameters[1]), 1, i + 1)

            plt.xlabel(parsed_parameters[2])
            plt.ylabel(parsed_parameters[2 + i + 1])

            plt.plot(parsed_parameters[2], parsed_parameters[2 + i + 1], data=self.data_frame)
            plt.plot(parsed_parameters[2], parsed_parameters[2 + i + 1], data=self.diff_data_frame)

        plt.show()

    def parse_args(self, initial_args):
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
