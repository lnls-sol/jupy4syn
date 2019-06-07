import ipywidgets as widgets
from IPython.display import display
import time
import py4syn.epics.MotorClass
from .utils import logprint
from epics import PV, caget
from .Configuration import Configuration


# Class MotorSetValueButton encapsulates a bounded float text with a button to a provided motor
# This class connects the button to the bouded float value and set the motor position
class PVSetter(widgets.Button):
    
    def __init__(self, pv_name, config=Configuration(), *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        
        # Motor associated to the button
        self.pv = PV(pv_name)
        self.pv_desc = caget(pv_name + ".DESC")
        self.pv_name = pv_name
        
        # Bounded float text associated to the button
        self.bounded_text = widgets.Text(
                                value=str(self.pv.value),
                                description=self.pv_desc,
                                disabled=False
                              )
        
        # class Button values for MotorSetValueButton
        self.description = 'Set "' + self.pv_desc + '" value'
        self.disabled = False
        self.button_style = 'success'
        self.tooltip = 'Click me'
        self.icon = ''    
        
        # Set callback function for click event
        self.on_click(self._set_val_button)
        
        # Widgets Boxes
        self.output = widgets.Output()
        
    @staticmethod
    def _set_val_button(b):
        # Clear previous logs outputs
        b.output.clear_output()
        
        # with statement to output logs in stdou (if this option is enabled)
        with b.output:
            # Change button to a "clicked status"
            b.disabled = True
            b.button_style = ''

            logprint("Setting PV " + b.pv_name + " to value " + b.bounded_text.value, config=b.config)
            try:
                # Move the motor to target absolute position
                b.pv.put(b.bounded_text.value, wait=False)
                logprint("Set value " + b.bounded_text.value + " to PV " + b.pv_name, config=b.config)
            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in setting value " + b.bounded_text.value + " to PV " + b.pv_name, "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            # Change button layout back to normal
            b.disabled = False
            b.button_style = 'success'
        

    def box_pv_button(self):
        return widgets.HBox([self.bounded_text, self])    
    
    def display(self):
        display(self.box_pv_button(), self.output)
