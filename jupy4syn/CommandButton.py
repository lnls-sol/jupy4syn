import time
import subprocess

# Widgets
import ipywidgets as widgets
from IPython.display import display

from scan_utils import ct

# Jupy4Syn
from jupy4syn.Configuration import Configuration
from jupy4syn.utils import logprint


class CommandButton(widgets.Button):
    
    def __init__(self, command, config=Configuration(), *args, **kwargs):
        """
        **Constructor**

        Parameters
        ----------
        command: `string`
            Command that will be executed at the button click
        config: `jupy4syn.Configuration`, optional
            Configuration object that contains Jupyter Notebook runtime information, by default Configuration()

        Examples
        ----------
        >>> config = Configuration()
            config.display()
        >>> command = CommandButton(config)
            command.display()
        """

        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config

        # Command
        self.command = command
        
        # class Button values for MonitorScanSave
        self.description = 'Execute Command ' + '"' + self.command + '"'
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
            b.description='Executing...'

            try:
                logprint("Executing command", config=b.config)
                process = subprocess.Popen([b.command], stdout=subprocess.PIPE, universal_newlines=True)
                
                # while True:
                #     output = process.stdout.readline()
                #     if output == '' and process.poll() is not None:
                #         break
                #     if output:
                #         print(output.strip())

                logprint("Finished executing command", config=b.config)
            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in executing command", "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            # We should sleep for some time to give some responsiveness to the user
            time.sleep(1.0)

            # Change button layout monitoring
            b.disabled = False
            b.button_style = 'success'
            b.description = 'Execute Command ' + '"' + b.command + '"'
    
    def display(self):
        display(self.start_button, self.output)
