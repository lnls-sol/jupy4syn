import os
from pathlib import Path
import subprocess
import time

# Auxiliar packages
import numpy as np
import pandas as pd

# Widgets
import ipywidgets as widgets
from IPython.display import display

# Plotly
import plotly.graph_objs as go
from plotly import tools

# Jupy4Syn
from jupy4syn.JupyScan import JupyScan
from jupy4syn.utils import logprint


class EnergyScanButton(widgets.Button):
    
    def __init__(self, config, *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        
        # Text box to write the motors to move
        self.text_motors = widgets.Textarea(
            value='',
            placeholder='Motors names from config.yml\nExample: solm3 gap2',
            description='',
            disabled=False
        )
        
        # Text box to write the configuration file
        self.text_config = widgets.Textarea(
            value='',
            placeholder='Name of the yml configuration file\nExample: default\n(PS: write "default" to load config.default.yml file)',
            description='',
            disabled=False
        )
        
        # Text box for start
        self.text_start = widgets.Text(
            value='',
            placeholder='Example for 2 motors: [1, 3], [7, 8]',
            description='',
            disabled=False
        )
        
        # Text box for end
        self.text_end = widgets.Text(
            value='',
            placeholder='Example for 2 motors: [2, 4], [8, 8.5]',
            description='',
            disabled=False
        )
        
        # Text box for step or points
        self.text_step_points = widgets.Text(
            value='',
            placeholder='Example for 2 motors: [1, 1], [0.5, 0.25]',
            description='',
            disabled=False
        )
        
        # Text box for time
        self.text_time = widgets.Text(
            value='',
            placeholder='Example for 2 motors: [1], [0.4]',
            description='',
            disabled=False
        )
        
        # Text box for output
        self.text_output = widgets.Text(
            value='',
            placeholder='Output file name, if left empty, file name will be the default name, "test"',
            description='',
            disabled=False
        )
        
        # Text box for optimum
        self.text_optimum = widgets.Text(
            value='',
            placeholder="Move motor to the optimal point according to \
                         this counter after scan. Leave empty for no move.",
            description='',
            disabled=True
        )
        
        # Optimum checkbox
        self.checkbox_optimum = widgets.Checkbox(
            value=False,
            description="",
            disabled=False,
            style={'description_width': 'initial'},
            layout = widgets.Layout(width='36px')
        )     

        self.checkbox_optimum.observe(self._change_checkbox_optimum, names=['value'])
        
        # class Button values for EnergyScanButton
        self.description='Start Energy Scan'
        self.disabled=False
        self.button_style='success'
        self.tooltip='Click me'
        self.icon=''
        self.layout = widgets.Layout(width='300px')

        # Set callback function for click event
        self.on_click(self._scan_button)
        
        # PV's Values
        self.pv_values = {}
        
        # Motor list
        self.motor_list = []

        self.scan_names = []
        
        # Callback flags
        self.on_scan = False
        self.scan_ended = False
        self.config_loaded = False

        self.fig = go.FigureWidget()
        self.fig_box = widgets.Box()
        
        # Main widget
        self.main_box = widgets.VBox([widgets.HBox([widgets.Label("Motors names", layout=widgets.Layout(width='150px')), self.text_motors]),
                                      widgets.HBox([widgets.Label("Configuration file name", layout=widgets.Layout(width='150px')), self.text_config]),
                                      widgets.HBox([widgets.Label("Start points", layout=widgets.Layout(width='150px')), self.text_start]),
                                      widgets.HBox([widgets.Label("End points", layout=widgets.Layout(width='150px')), self.text_end]),
                                      widgets.HBox([widgets.Label("Step or Points", layout=widgets.Layout(width='150px')), self.text_step_points]), 
                                      widgets.HBox([widgets.Label("Time", layout=widgets.Layout(width='150px')), self.text_time]),
                                      widgets.HBox([self.checkbox_optimum,
                                                    widgets.Label("Go to optimum of: ", layout=widgets.Layout(width='110px')),
                                                    self.text_optimum]),
                                      widgets.HBox([widgets.Label("Output file name", layout=widgets.Layout(width='150px')), self.text_output]),
                                      self])
        self.output = widgets.Output()

    
    def _change_checkbox_optimum(self, change):
        self.text_optimum.disabled = not change.new
    
        
    @staticmethod
    def _scan_button(b):
        # Clear previous logs outputs
        b.output.clear_output()
        
        # with statement to output logs in stdout (if this option is enabled)
        with b.output:
            # Change button appearence
            b.description = 'Scanning'
            b.button_style = ''

            # Disable button to avoid double commands
            b.disabled = True

            # Disable box edition to avoid erros
            boxes = [b.text_motors, b.text_config, b.text_start, b.text_end, 
                    b.text_step_points, b.text_time, b.text_optimum, b.text_output]

            for box in boxes:
                box.disabled = True

            # Reset motor list
            b.motor_list = []

            # Get motors names from the text box
            names_comma_space_ent = []
            motor_list_names = b.text_motors.value.split(' ')
            for name in motor_list_names:
                    names_comma_space = name.split(",")

                    for name_wout_comma in names_comma_space:
                        names_comma_space_ent.append(name_wout_comma.split("\n"))

            lin_names = sum(names_comma_space_ent, [])
            motor_list_names = [name for name in lin_names if name != "" and name != "\n"]
            logprint("Scanning on motors" + ', '.join(motor_list_names), config=b.config)

            # Get config file name from the text box
            config_name = b.text_config.value
            logprint("YML config file: " + config_name, config=b.config)

            # Load scan parameters
            start = []
            end = []
            step_or_points = []
            time = []
            try:
                # Get lists from text boxes
                start = b.text_start.value
                end = b.text_end.value
                step_or_points = b.text_step_points.value
                time = b.text_time.value

                logprint("Loaded 'start, end, step or points, time' scan parameters", config=b.config)
            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error loading 'start, end, step or points, time' scan parameters", "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            # Get output file name
            output = b.text_output.value if b.text_output.value != '' else 'test'
            
            # Get absolute path to file, and create a scans directory if the directory doesn't exist
            mypath = Path().absolute() / 'scans'
            if not mypath.is_dir():
                mypath.mkdir()
            
            # Put the path to the output
            output = str(mypath) + '/' + output

            # Edge
            edge = 0.0
            # Initiate scan
            try:
                command = "/usr/local/SOL/scan-utils/energy-scan" + \
                          " -c " + config_name + \
                          " -o " + output + \
                          " --motor " + ' '.join(motor_list_names) + \
                          " --start " + start + \
                          " --end " + end + \
                          " --step-or-points " + step_or_points + \
                          " --time " + time + \
                          " --edge " + str(edge)
                
                subprocess.run([command],shell=True, check=True)
                logprint("Started scan, output saved in file " + output, config=b.config)

            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in trying to energy scan", "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            b.scan_names = b.get_scan_name(output, 1)

            dfs = []
            dfs.append(pd.DataFrame())
            while dfs[0].empty:
                label = []
                dfs, label = b.update_pd(b.scan_names, label)

            number_motors = len(motor_list_names)

            b.create_figure(len(dfs[0].columns) - number_motors)

            # Plot
            try:
                for i in range(len(dfs)):
                    if dfs[i].empty:
                        continue

                    diff_df = dfs[i].diff().dropna()
                    diff_diff_df = diff_df[i].diff().dropna()

                    for j in range(len(dfs[i].columns) - number_motors):
                        # Plot function
                        b.fig['data'][i + j*len(dfs) + j]['x'] = dfs[i].index.values
                        b.fig['data'][i + j*len(dfs) + j]['y'] = dfs[i][dfs[i]. columns[number_motors + j]].values

                        # Plot First Diff function
                        b.fig['data'][i + 1 + j*len(dfs) + j]['x'] = diff_df.index.values
                        b.fig['data'][i + 1 + j*len(dfs) + j]['y'] = (diff_df[diff_df.columns[number_motors + j]] / diff_df[0]).values

                        # Plot Second Diff function
                        b.fig['data'][i + 2 + j*len(dfs) + j]['x'] = diff_diff_df.index.values
                        b.fig['data'][i + 2 + j*len(dfs) + j]['y'] = (diff_diff_df[diff_diff_df.columns[number_motors + j]] / diff_df[0]).values

            except Exception as e:
                logprint("Error in trying to plot energy scan", "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            # Change button appearence
            b.description = 'Start Energy Scan'
            b.button_style = 'success'

            # Re enable button
            b.disabled = False

            # Re enable box edition 
            for box in boxes:
                box.disabled = False
               
    def get_scan_name(self, fileName, number_repeats):
        # Waits for file to be written by scan writter
        time.sleep(1.0)

        scan_names = []

        leadingZeros = 4
        newName = ""
        cont = 0
        while(True):
            cont += 1
            newName = fileName + "_" + str(cont).zfill(leadingZeros)
            if(os.path.isfile(newName)):
                continue
            else:
                for i in range(number_repeats):
                    scan_names.append(fileName + "_" + str(cont - 1 + i).zfill(leadingZeros))
                break
                
        return scan_names

    def update_pd(self, default_names, label):
        dfs = []
        number_non_empty = len(default_names)

        for default_name in default_names:
            try:
                dfs.append(pd.read_csv(default_name, sep=' ', comment='#', header=None))
            except:
                dfs.append(pd.DataFrame())
                number_non_empty -= 1

        if number_non_empty == 0:
            return dfs, label

        filtered_label = label
        if not label:
            labels = []
            with open(default_names[0]) as file:
                for i, line in enumerate(file):
                    if i == 6:
                        self.number_reads = (int(line.split(' ')[1]))
                    elif i == 8:
                        labels = line.split(' ')[1:]
                        break

            labels = list(filter(lambda x: x != '', labels))

            for item in labels:
                filtered_label.append(item.rstrip('\n'))

            label = filtered_label

        for df in dfs:
            if not df.empty:
                df.columns = pd.Index(filtered_label, dtype='object')
        
        return dfs, label

    def create_figure(self, number_traces):
        self.traces = []
        
        self.fig = go.FigureWidget(tools.make_subplots(rows=number_traces, cols=1, print_grid=False))
        
        for i in range(1, number_traces + 1):
            self.traces.append([])

            for _ in range(len(self.scan_names)):
                trace = go.Scatter(
                    x=[], y=[], # Data
                    mode='lines+markers', name='f' + str(i), showlegend=True
                )

                diff_trace = go.Scatter(
                    x=[], y=[], # Data
                    mode='lines+markers', name='df' + str(i), showlegend=True
                )

                diff_diff_trace = go.Scatter(
                    x=[], y=[], # Data
                    mode='lines+markers', name='ddf' + str(i), showlegend=True
                )

                self.traces[i-1].append(trace)
                self.fig.append_trace(trace, i, 1) # using i + 1 because plot index starts at 1
                self.fig.append_trace(diff_trace, i, 1) # using i + 1 because plot index starts at 1
                self.fig.append_trace(diff_diff_trace, i, 1) # using i + 1 because plot index starts at 1

                self.fig['data'][3*(i-1)+1].update(yaxis="y"+str(number_traces+i*2))
                self.fig['data'][3*(i-1)+2].update(yaxis="y"+str(number_traces+i*2 + 1))
                
                self.fig['layout']['yaxis'+str(number_traces+i*2)] = dict(overlaying="y"+str(i), anchor="x"+str(i), side="right")
                self.fig['layout']['yaxis'+str(number_traces+i*2 + 1)] = dict(overlaying="y"+str(i), anchor="x"+str(i), side="right")                

        self.fig['layout'].update(title='Scan', plot_bgcolor='rgb(230, 230, 230)')
        self.fig_box.children = (self.fig,)

    def display(self):
        display(self.main_box, self.fig_box, self.output)
