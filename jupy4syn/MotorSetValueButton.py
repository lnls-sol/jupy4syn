import time

# Widgets
import ipywidgets as widgets
from IPython.display import display

# Py4Syn
import py4syn.epics.MotorClass

# Jupy4Syn
from jupy4syn.Configuration import Configuration
from jupy4syn.utils import logprint


# Class MotorSetValueButton encapsulates a bounded float text with a button to a provided motor
# This class connects the button to the bouded float value and set the motor position
class MotorSetValueButton(widgets.Button):
    
    def __init__(self, motor, config=Configuration(), *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        
        # Motor associated to the button
        self.motor = motor
        if type(motor) != py4syn.epics.MotorClass.Motor:
            logprint("Passed to class MotorSetValueButton constructor a argument with wrong type. Expected py4syn.epics.MotorClass.Motor, received " + str(type(motor)), config=self.config)
            
            raise("Passed to class MotorSetValueButton constructor a argument with wrong type. Expected py4syn.epics.MotorClass.Motor, received " + str(type(motor)))
        
        # Bounded float text associated to the button
        self.bounded_float = widgets.BoundedFloatText(
                                value=motor.getRealPosition(),
                                min=motor.getLowLimitValue(),
                                max=motor.getHighLimitValue(),
                                step=0.01,
                                description=motor.motorDesc,
                                disabled=False
                              )
        
        # class Button values for MotorSetValueButton
        self.description = 'Set Target VAL'
        self.disabled = False
        self.button_style = 'success'
        self.tooltip = 'Click me'
        self.icon = ''    
        
        # Set callback function for click event
        self.on_click(self._motor_set_val_button)
        
        # Widgets Boxes
        self.output = widgets.Output()
        
    @staticmethod
    def _motor_set_val_button(b):
        # Clear previous logs outputs
        b.output.clear_output()
        
        # with statement to output logs in stdou (if this option is enabled)
        with b.output:
            # Change button to a "clicked status"
            b.disabled = True
            b.button_style = ''

            logprint("Starting motor " + b.motor.pvName + " movement to absolute value " + str(b.bounded_float.value), config=b.config)
            try:
                # Move the motor to target absolute position
                b.motor.setAbsolutePosition(b.bounded_float.value, waitComplete=False)
                logprint("Set absolute value " + str(b.bounded_float.value) + " for motor " + b.motor.pvName, config=b.config)
            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in setting absolute value " + str(b.bounded_float.value) + " for motor " + b.motor.pvName, "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

            # Change button layout back to normal
            b.disabled = False
            b.button_style = 'success'
        

    def box_motor_button(self):
        return widgets.HBox([self.bounded_float, self])    
    
    
    def box_motor_output(self):
        return self.output 
    
    
    def display(self):
        display(self.box_motor_button(), self.output)
