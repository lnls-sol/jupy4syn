import argparse


class ScanParser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Perform a scan with \
                                        specified devices (e.g.: motors) and the list of counters provided by the \
                                        configuration file.")

        self.parser.add_argument('-l', '--list-configurations',
                            help='list configurations instead of scanning',
                            action='store_true')

        self.parser.add_argument('-c', '--configuration',
                            help='choose a counter configuration file',
                            default='default')

        self.parser.add_argument('--optimum',
                            help='move motor to the optimal point according to \
                            this counter after scan')

        self.parser.add_argument('--repeat',
                            help='scan multiple times',
                            type=int,
                            default=1)

        self.parser.add_argument('--sleep',
                            help='sleep time before each acquisition',
                            type=float,
                            default=0)

        self.parser.add_argument('-m', '--message',
                            help='string of comments to put in output file header')

        self.parser.add_argument('-o', '--output',
                            help='output data to file output-prefix/<fileprefix>_nnnn')

        self.parser.add_argument('-s', '--sync',
                            help='write to the output file after each point',
                            action='store_true')

        self.parser.add_argument('--snake',
                            help='snake scan mode',
                            action='store_true')

        self.parser.add_argument('--motor',
                            help='list of motors',
                            nargs='+')

        self.parser.add_argument('--xlabel',
                            help='motor which position is shown in x axis \
                            (if not set, point index is shown instead)',
                            default='points')

        # Arguments describing a run
        group_run = self.parser.add_argument_group(
                            description="Arguments for describing a given run \
                            (define this set of arguments again for each new run):")

        group_run.add_argument('--start',
                            help='list of start positions of each device',
                            nargs='+',
                            action='append',
                            type=float)

        group_run.add_argument('--end',
                            help='list of end positions of each device',
                            nargs='+',
                            action='append',
                            type=float)

        group_run.add_argument('--step-or-points',
                            help='list of step size (or number of points) for each device',
                            nargs='+',
                            action='append',
                            type=float)

        group_run.add_argument('--time',
                            help='acquisition time',
                            nargs=1,
                            action='append',
                            type=float)

        group_run.add_argument('-f',
                            help='ipython test',
                            nargs=1,
                            action='append',
                            type=str)
