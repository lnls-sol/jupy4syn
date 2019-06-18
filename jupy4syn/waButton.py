import time
import subprocess

# Widgets
import ipywidgets as widgets
from IPython.display import display

# scan-utils
from scan_utils import wa

# Jupy4Syn
from jupy4syn.Configuration import Configuration
from jupy4syn.utils import logprint


class waButton(widgets.Button):
    
    def __init__(self, config=Configuration(), *args, **kwargs):
        """
        **Constructor**

        Parameters
        ----------
        config: `jupy4syn.Configuration`, optional
            Configuration object that contains Jupyter Notebook runtime information, by default Configuration()

        Examples
        ----------
        >>> config = Configuration()
            config.display()
        >>> wa = waButton(config)
            wa.display()
        """

        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        
        # class Button values for MonitorScanSave
        self.description = 'Execute wa'
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
                logprint("Executing wa", config=b.config)
                # TODO: call wa main from another thread
                wa.main()

                logprint("Finished executing wa", config=b.config)
            except SystemExit as e:
                pass
            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in executing wa", "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            # We should sleep for some time to give some responsiveness to the user
            time.sleep(1.0)

            # Change button layout monitoring
            b.disabled = False
            b.button_style = 'success'
            b.description = 'Execute wa'
    
    def display(self):
        display(self.start_button, self.output)
