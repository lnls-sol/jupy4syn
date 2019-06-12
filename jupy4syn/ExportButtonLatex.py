import os
import time

# Widgets
import ipywidgets as widgets
from IPython.display import display, Javascript

# Jupy4Syn
from jupy4syn.utils import logprint


class ExportButtonLatex(widgets.Button):
    def __init__(self, config, *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        self.notebook_name = config.notebook_name.value
        self.plots_list = config.plots_list

        # class Button values for ExportButtonLatex
        self.description='Export Notebook to Latex'
        self.disabled=False
        self.button_style='warning' # 'success', 'info', 'warning', 'danger' or ''
        self.tooltip='Click me'
        self.icon=''
        self.layout = widgets.Layout(width='300px')
    
        # Set callback function for click event
        self.on_click(self._click_button)

        # Logging
        self.output = widgets.Output()

        # Widgets display box
        self.display_box = widgets.VBox([self, self.output])   
    
    @staticmethod
    def _click_button(b):
        with b.output:
            # Change button to a "clicked status"
            b.disabled = True
            b.button_style = ''
            b.description='Exporting...'

            # We should sleep for some time to give some responsiveness to the user
            time.sleep(0.5)

            # Get configuration run-time values
            b.notebook_name = b.config.notebook_name.value
            b.plots_list = b.config.plots_list

            # Check if notebook name is not empty, if it is, print an error message and
            # change button status temporarily to an error descripton. Then restart button.
            if b.notebook_name == "":
                logprint("Notebook name not defined in configuration cell", "[ERROR]", config=b.config)
                # Change button status to a "error status"
                b.disabled = True
                b.button_style = 'danger'
                b.description='ERROR. Notebook\'s name not set'

                time.sleep(2.0)

                # Reenable button
                b.disabled = False
                b.button_style = 'warning'
                b.description='Export Notebook to Latex'

                return
            
            try:
                # For every plot registered in the plots_list, we have to set these
                # plots export flag to True to start the export
                for plot in b.plots_list:
                    plot.export = True
                
                # Time sleep to the plot_list thread update the display
                time.sleep(1.0)
        
                # Get time stamp for the export name
                ts = time.gmtime()
                time_stamp = time.strftime("%Y-%m-%d-%H:%M:%S", ts)
                output_file = time_stamp + '-' + b.notebook_name

                # Save the notebook to display the static images
                display(Javascript('IPython.notebook.save_checkpoint();'))
                
                # Call nbconvert to do the export
                os.system("python3 -m nbconvert ./" + b.notebook_name + ".ipynb --template=nbextensions --output-dir=./exports --output=" + output_file + " --to latex")
                
                # For every plot registered in the plots_list, we have to set these
                # plots export flag to False to end the export
                for plot in b.plots_list:
                    plot.export = False

            except Exception as e:
                logprint(str(e), "[ERROR]", config=b.config)
            
            # Reenable button
            b.disabled = False
            b.button_style = 'warning'
            b.description='Export Notebook to Latex'
        
    def display(self):
        display(self.display_box)
                    