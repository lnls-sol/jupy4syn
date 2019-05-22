import ipywidgets as widgets
from IPython.display import display
import time
import subprocess
from .utils import logprint


class ScalerButton(widgets.Button):
    
    def __init__(self, config, *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        
        # class Button values for MonitorScanSave
        self.description = 'Start Scaler GUI'
        self.disabled = False
        self.button_style = 'success'
        self.tooltip = 'Click me'
        self.icon = ''
        self.layout = widgets.Layout(width='300px')

        # Macro textbox
        self.macro = widgets.Text(
            value='',
            placeholder="Type the macro",
            description="",
            disabled=False,
            layout=widgets.Layout(width="300px")
        )
               
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
            b.description='Scaling...'

            try:
                logprint("Starting Scaler", config=b.config)
                subprocess.Popen(["pydm -m \"" + b.macro.value + "\" /usr/local/SOL/GUI/Scaler_GUI/scaler.py"],
                                 shell=True)

                logprint("Finished openning Scaler", config=b.config)
            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in openning Scaler", "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            # We should sleep for some time to give some responsiveness to the user
            time.sleep(1.0)

            # Change button layout monitoring
            b.disabled = False
            b.button_style = 'success'
            b.description = 'Start Scaler GUI'
    
    def display(self):
        display(self.macro, self.start_button, self.output)
