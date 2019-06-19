import time
import subprocess

# Widgets
import ipywidgets as widgets
from IPython.display import display

# scan-utils
from scan_utils import move

# Jupy4Syn
from jupy4syn.Configuration import Configuration
from jupy4syn.utils import logprint


class moveButton(widgets.Button):
    
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
        >>> move = moveButton(config)
            move.display()
        """

        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        
        # class Button values for MonitorScanSave
        self.description = 'Execute move'
        self.disabled = False
        self.button_style = 'success'
        self.tooltip = 'Click me'
        self.icon = ''
        self.layout = widgets.Layout(width='300px')

        # Bounded float text associated to the button
        self.bounded_text = widgets.Text(
                                value="",
                                description="arguments",
                                disabled=False
                              )
               
        # Logging
        self.output_1 = widgets.Output()
        self.output_2 = widgets.Output()
        
        # Set callback function for click event
        self.on_click(self._start_button)
        
        # Widgets displays
        self.start_button = widgets.VBox([self])
    
    @staticmethod
    def _start_button(b):
        # Clear previous logs outputs
        b.output_1.clear_output()
        b.output_2.clear_output()
        
        # With statement to output logs in Jupyter stdout (if this option is enabled)
        # Change button to a "clicked status"
        b.disabled = True
        b.button_style = ''
        b.description='Executing...'

        try:
            logprint("Executing move", config=b.config)
            # TODO: call move main from another thread
            move.main(b.bounded_text.value.split(), b.output_1, b.output_2)

            logprint("Finished executing move", config=b.config)
        except SystemExit as e:
            pass
        except Exception as e:
            # If any error occurs, log that but dont stop code exection
            logprint("Error in executing move", "[ERROR]", config=b.config)
            logprint(str(e), "[ERROR]", config=b.config)

        # We should sleep for some time to give some responsiveness to the user
        time.sleep(1.0)

        # Change button layout monitoring
        b.disabled = False
        b.button_style = 'success'
        b.description = 'Execute move'
    
    def display(self):
        display(self.bounded_text, self.start_button, self.output_1, self.output_2)
