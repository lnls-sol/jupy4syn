import ipywidgets as widgets
from IPython.display import display
import time
from py4syn.epics.MotorClass import Motor
from .utils import logprint, configurate_motor
from .MotorSetValueButton import MotorSetValueButton


class StartMotorsButton(widgets.Button):
    
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
        
        # class Button values for StartMotorsButton
        self.description='Start Motor Initializaton'
        self.disabled=False
        self.button_style='success'
        self.tooltip='Click me'
        self.icon=''
        self.layout = widgets.Layout(width='300px')
        
        # Boxes
        self.motors_value_buttons = []
        
        # Motors
        self.motors_list = []
        
        # Set callback function for click event
        self.on_click(self._start_button)
        
        # Widgets displays
        self.start_button = widgets.VBox([self.text, self])
        self.target_value_buttons = widgets.VBox([widgets.Label("No motors initilized to be showed.")])
        
        # Logging
        self.output = widgets.Output()
        
        
    @staticmethod
    def _start_button(b):
        # Clear previous logs outputs
        b.output.clear_output()
        
        # with statement to output logs in stdou (if this option is enabled)
        with b.output:
            # Change button to a "clicked status"
            b.disabled = True
            b.button_style = ''
            b.description='Initializing...'
            # We should sleep for some time to give some responsiveness to the user
            time.sleep(0.5)

            # Get motors PV names from the text box
            # Filter names
            motor_list_names = []
            names_comma_space_ent = []
            names_space = b.text.value.split(' ')
            for name in names_space:
                names_comma_space = name.split(",")

                for name_wout_comma in names_comma_space:
                    names_comma_space_ent.append(name_wout_comma.split("\n"))

            lin_names = sum(names_comma_space_ent, [])
            motor_list_names = [name for name in lin_names if name != "" and name != "\n"]

            logprint("Starting motors " + ', '.join(motor_list_names) + " initialization", config=b.config)

            # Create motors and add a MotorSetValueButton to them
            try:
                b.motors_list = [configurate_motor(name, ' '.join(name.split(':')[-2:]), b.config) for name in motor_list_names]

                b.motors_value_buttons = [MotorSetValueButton(motor, b.config) for motor in b.motors_list]

                # Set Target Value Button Widget children to all initilized motors boxes
                widgets_boxes = [motor_button.box_motor_button() for motor_button in b.motors_value_buttons]
                widgets_target_outputs = [motor_button.box_motor_output() for motor_button in b.motors_value_buttons]
                b.target_value_buttons.children = tuple(widgets_boxes + widgets_target_outputs)

                logprint("Finished motors " + ', '.join(motor_list_names) + " initialization", config=b.config)              
            except Exception as e:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in initialziation of motors " + ', '.join(motor_list_names), "[ERROR]", config=b.config)
                logprint(str(e), "[ERROR]", config=b.config)

                # Reset Target Value Boxes to default Label
                b.target_value_buttons.children = (widgets.Label("No motors initilized to be showed."),)

            # Change button layout back to normal
            b.disabled = False
            b.button_style = 'success'
            b.description='Start Motor Initializaton'   
    
    
    def display_start_button(self):
        display(self.start_button, self.output)
    
    
    def display_motors_targ_buttons(self):
        display(self.target_value_buttons)
