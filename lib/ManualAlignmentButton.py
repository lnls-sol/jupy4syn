import ipywidgets as widgets
from IPython.display import display
import time
import subprocess
from .utils import logprint


class ManualAlignmentButton(widgets.Button):
    
    def __init__(self, config, *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        
        # class Button values for MonitorScanSave
        self.description = 'Start Manual Alignment'
        self.disabled = False
        self.button_style = 'success'
        self.tooltip = 'Click me'
        self.icon = ''
        self.layout = widgets.Layout(width='300px')
               
        # Logging
        self.output = widgets.Output()
        
        # Set callback function for click event
        self.on_click(self._start_button)
        
        # Widgets displays
        self.start_button = widgets.VBox([self])
        
    @staticmethod
    def _start_button(b):
        # Clear previous logs outputs
        b.output.clear_output()
        
        # with statement to output logs in stdou (if this option is enabled)
        with b.output:
            # Change button to a "clicked status"
            b.disabled = True
            b.button_style = ''
            b.description='Aligning...'

            # We should sleep for some time to give some responsiveness to the user
            time.sleep(0.5)

            # Stop thread to monitor the save file
            try:
                logprint("Starting manual alignment", config=b.config)
                subprocess.run(["pydm /usr/local/SOL/GUI/sol-widgets/examples/motor/slits.ui"],
                                 shell=True, check=True)

                logprint("Finished manual alignment", config=b.config)
            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in manual alignment", "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            # Change button layout monitoring
            b.disabled = False
            b.button_style = 'success'
            b.description='Start Manual Alignment'
    
    def display_start_button(self):
        display(self.start_button, self.output)
