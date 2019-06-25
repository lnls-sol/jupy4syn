import time
import subprocess

# Widgets
import ipywidgets as widgets
from IPython.display import display

# Jupy4Syn
from jupy4syn.Configuration import Configuration
from jupy4syn.utils import logprint


class interfaceButton(widgets.Button):
    
    def __init__(self, interface, config=Configuration(), *args, **kwargs):
        """
        **Constructor**

        Parameters
        ----------
        config: `jupy4syn.Configuration`, optional
            Configuration object that contains Jupyter Notebook runtime information, by default Configuration()

        Examples
        ----------
        >>> config = Configuration()
        >>> config.display()
        >>> scaler = interfaceButton(config)
        >>> scaler.display()
        """

        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config

        # Interfaces
        self.interface = interface

        self.interfaces_list = ["pydm", "scaler", "vortex", "scan_gui", "energy_scan_gui", "pymca"]
        if interface not in self.interfaces_list:
            raise TypeError("Interface '" + interface + "' is not a valid option. Interfaces available are: " +
                            str(self.interfaces_list))
        
        if interface is "energy_scan_gui":
            macro_value = "energy"
        else:
            macro_value = ""

        
        
        # class Button values for MonitorScanSave
        self.description = 'Start ' + interface
        self.disabled = False
        self.button_style = 'success'
        self.tooltip = 'Click me'
        self.icon = ''
        self.layout = widgets.Layout(width='300px')

        # Macro textbox
        self.macro = widgets.Text(
            value=macro_value,
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
            b.description='Opening interface...'

            try:
                logprint("Starting " + b.interface, config=b.config)

                if b.macro.value is not "":
                    if b.interface is not "energy_scan_gui":
                        subprocess.Popen([b.interface, "-m", b.macro.value])
                    else:
                        subprocess.Popen([b.interface, b.macro.value])
                else:
                    subprocess.Popen([b.interface])

                logprint("Finished openning " + b.interface, config=b.config)
            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in openning " + b.interface, "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            # We should sleep for some time to give some responsiveness to the user
            time.sleep(1.0)

            # Change button layout monitoring
            b.disabled = False
            b.button_style = 'success'
            b.description = 'Start ' + b.interface
    
    def display(self):
        display(self.macro, self.start_button, self.output)
