import ipywidgets as widgets
from IPython.display import display
import time
import subprocess
from .utils import logprint, configurate_motor


class MotorsMonitor(widgets.Button):
    
    def __init__(self, config, *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        
        # Text box to write the motors
        self.text = widgets.Textarea(
            value='',
            placeholder='Example: IOC:m1 IOC:m3 LNLS:TEST:motor_g3',
            description='',
            disabled=False
        )
        
        # class Button values for MotorsMonitor
        self.description='Start Motor Monitoring'
        self.disabled=False
        self.button_style='success'
        self.tooltip='Click me'
        self.icon=''
        self.layout = widgets.Layout(width='300px')
        
        # Boxes
        self.motors_values = {}
        
        # Motors
        self.motors_list = []
        
        # Set callback function for click event
        self.monitoring_status = False
        self.on_click(self._monitor_button)
        
        # Main widget
        self.main_box = widgets.VBox([self, self.text])
        self.output = widgets.Output()
        
    @staticmethod
    def _monitor_button(b):
        # Clear previous logs outputs
        b.output.clear_output()
        
        # with statement to output logs in stdou (if this option is enabled)
        with b.output:
            # Disabel button to avoid double commands
            b.disabled=True

            if b.monitoring_status:
                # Change button appearence
                b.description='Start Motor Monitoring'
                b.button_style='success'

                # Stop displaying the motors widgets, show only button and text box
                b.main_box.children = (b.main_box.children[0], b.text,)

                logprint("Stopped monitoring motors " + ', '.join([motor.pvName for motor in b.motors_list]), config=b.config)

                # Reset motor list
                b.motors_list = []      
            else:
                # Change button appearence
                b.description='Stop Motor Monitoring'
                b.button_style = 'danger'

                # Stop displaying text box
                b.main_box.children = (b.main_box.children[0],)

                # Get motors PV names from the text box
                motor_list_names = b.text.value.split(' ')
                logprint("Started monitoring motors " + ', '.join(motor_list_names), config=b.config)

                # Create motors and add a monitor callback to them
                # Also add these motor values as children of main_box widget
                try:
                    b.motors_list = [configurate_motor(name, ''.join(name.split(':')[-2:])) for name in motor_list_names]

                    for motor in b.motors_list:
                        index = motor.motor.add_callback('RBV', b._monitor_callback)

                        rbv = motor.getRealPosition()
                        b.motors_values[motor.pvName + ".RBV"] = (rbv, str(rbv))

                        b.main_box.children += (widgets.HBox([widgets.Label(motor.pvName + ".RBV"), widgets.Label(str(rbv))]),)

                    logprint("Monitoring motors " + ', '.join(motor_list_names), config=b.config)        

                except Exception as e:
                    # If any error occurs, log that but dont stop code exection
                    logprint("Error in monitoring motors " + ', '.join(motor_list_names), "[ERROR]", config=b.config)
                    logprint(str(e), "[ERROR]", config=b.config)

            # Re enable button
            b.disabled=False

            # Switch status
            b.monitoring_status = not b.monitoring_status
               

    def _monitor_callback(self, pvname='', value=0, char_value='', **kw):
        self.motors_values[pvname] = (value, char_value)
        
        if self.monitoring_status:
            for widget in self.main_box.children[1:]:
                if widget.children[0].value == pvname:
                    widget.children[1].value = char_value


    def display(self):
        display(self.main_box, self.output)
