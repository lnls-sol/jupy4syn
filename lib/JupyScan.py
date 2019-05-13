import argparse
from IPython.display import display
from scan_utils.scan import ScanOperationCLI
from scan_utils import cleanup, die
from py4syn.utils import scan as scanModule


class JupyScan(ScanOperationCLI):
    def __init__(self, motor, start, end, stepOrPoints, time, configuration='default',
            optimum=False, sync=False, output=None, message=None, repeat=1, sleep=0,
            waitPlotter=True, plotXFactor=1, snake=False, xlabel='points'):
        
        super().__init__(motor, start, end, stepOrPoints, time, configuration,
            optimum, sync, output, message, repeat, sleep,
            waitPlotter, plotXFactor, snake, xlabel)
        
        
    def plot(self, plotter, scan, pos, idx):
        data = scanModule.getScanData()
        user = scanModule.getUserDefinedDataFields()
        position = data[self.xlabel][-1]

        for counter in self.configuration.runtime:
            c = self.configuration['counters'][counter]
            
            label = c['label']
            if c.get('plot', True):
                plotter.plot(data[self.xlabel], data[label], label)
            elif counter in user:
                data[label].append(processUserField(c))

    # Override default plot procedure
    def configurePlot(self):
        from py4syn.utils.plotter import Plotter
        scanModule.setPlotGraph(False)

        if self.configuration.somePlot() :
            p = ScanPlott(self.output or 'Scan')
            
            for counter in self.configuration.runtime:
                c = self.configuration['counters'][counter]
                label = c['label']
                
                p.add_scatter([0], [0], label)
                
            
            scanModule.setPostOperationCallback(lambda **kw: self.plot(p, **kw))
        else:
            p = None

        return p


    def run(self):
        self.onOperationBegin()
        plotter = self.configurePlot()

        # Display plot using IPython display widget
        IPython.display.display(plotter.display())

#         if plotter is not None:
#             axes = self.generateAxes(plotter)

        # Build arguments for scan method
        scan_args = []
        for i in range(len(self.motor)):
            scan_args.append(self.motor[i])
            scan_args.append(self.points[i])
        scan_args.append(len(self.points[0]))
        scan_args.append(self.times)
        scan_args = tuple(scan_args)

        print('\nEstimated time: ' + str(self.getEstimatedTime(self.times)) + '\n')

        for i in range(self.repeat):
            self.onScanBegin()

#             if plotter is not None:
#                 next(axes)

            try:
                scanModule.scan(*scan_args)
            except Exception as e:
                raise RuntimeError('Error executing scan: ' + str(e))

            self.onScanEnd()

            self.fitValues()

        if self.optimum:
            self.goToOptimum()

        cleanup()
        self.onOperationEnd()
#         if self.waitPlotter:
#             plotter.plot_process.join()


def parseCommandLine():
    parser = argparse.ArgumentParser(description="Perform a scan with \
    specified devices (e.g.: motors) and the list of counters provided by the \
    configuration file.")

    parser.add_argument('-l', '--list-configurations',
                        help='list configurations instead of scanning',
                        action='store_true')

    parser.add_argument('-c', '--configuration',
                        help='choose a counter configuration file',
                        default='default')

    parser.add_argument('--optimum',
                        help='move motor to the optimal point according to \
                        this counter after scan')

    parser.add_argument('--repeat',
                        help='scan multiple times',
                        type=int,
                        default=1)

    parser.add_argument('--sleep',
                        help='sleep time before each acquisition',
                        type=float,
                        default=0)

    parser.add_argument('-m', '--message',
                        help='string of comments to put in output file header')

    parser.add_argument('-o', '--output',
                        help='output data to file output-prefix/<fileprefix>_nnnn')

    parser.add_argument('-s', '--sync',
                        help='write to the output file after each point',
                        action='store_true')

    parser.add_argument('--snake',
                        help='snake scan mode',
                        action='store_true')

    parser.add_argument('--motor',
                        help='list of motors',
                        nargs='+')

    parser.add_argument('--xlabel',
                        help='motor which position is shown in x axis \
                        (if not set, point index is shown instead)',
                        default='points')

    # Arguments describing a run
    group_run = parser.add_argument_group(
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

    args = parser.parse_args()
    if args.list_configurations:
        listConfigurations()
        raise SystemExit(1)

    # Just for args name compatibility
    args.stepOrPoints = args.step_or_points
    del(args.step_or_points)
    del(args.list_configurations)

    args_dict = vars(args)
    return args_dict


    def runScan():
        args = parseCommandLine()

        try:
            scan = ScanOperationCLI(**args)

            scan.run()
        except (OSError, RuntimeError) as e:
            die(e)

