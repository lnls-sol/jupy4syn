import subprocess
import time

# Widgets
import ipywidgets as widgets
from IPython.display import display

# scan-utils
import scan_utils.configuration as scan_utils

# Jupy4Syn
from jupy4syn.Configuration import Configuration
from jupy4syn.utils import logprint


class slitsButton(widgets.Button):
    
    def __init__(self, m1="", m2="", m3="", m4="", m5="", user_flag=False, config=Configuration(), *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        self.yml_config = scan_utils.Configuration()

        # Motors
        self.m1 = self.get_pv_by_name(m1)
        self.m2 = self.get_pv_by_name(m2)
        self.m3 = self.get_pv_by_name(m3)
        self.m4 = self.get_pv_by_name(m4)
        self.m5 = self.get_pv_by_name(m5)

        self.motors = [m1, m2, m3, m4, m5]
        self.motors = [motor for motor in self.motors if motor != ""]

        # Flags
        self.user_flag = "--user" if user_flag is True else ""
        
        # class Button values for MonitorScanSave
        self.description = 'Open Motors Interface'
        self.disabled = False
        self.button_style = 'success'
        self.tooltip = 'Click me'
        self.icon = ''
        self.layout = widgets.Layout(width='300px')
        
        # Set callback function for click event
        self.on_click(self._click_button)
        
        # Logging
        self.output = widgets.Output()

        # Widgets display box
        self.display_box = widgets.VBox([self, self.output])
        
    @staticmethod
    def _click_button(b):
        # Clear previous logs outputs
        b.output.clear_output()
        
        # with statement to output logs in stdou (if this option is enabled)
        with b.output:
            # Change button to a "clicked status"
            b.disabled = True
            b.button_style = ''
            b.description='Opening Interface...'

            # Create a subprocess with the motors script from sol-widgets
            try:
                logprint("Opening motors interface", config=b.config)
                subprocess.Popen(["motors_gui"] + b.motors + [b.user_flag], shell=True)

                logprint("Finished opening motors interface", config=b.config)
            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in opening motors interface", "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            # We should sleep for some time to give some responsiveness to the user
            time.sleep(1.0)

            # Reenable button
            b.disabled = False
            b.button_style = 'success'
            b.description = 'Open Motors Interface'
    
    def get_pv_by_name(self, name):
        motors = self.yml_config['motors']

        if name in motors:
            return motors[name]['pv']
        else: 
            return ""

    def display(self):
        display(self.display_box)
