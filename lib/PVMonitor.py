import ipywidgets as widgets
from IPython.display import display
import time
import subprocess
from .utils import logprint, configurate_motor
from epics import PV


class PVMonitor(widgets.Button):
    
    def __init__(self, config, *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        
        # Text box to write the motors
        self.text = widgets.Textarea(
            value='',
            placeholder='Example: IOC:m1.DMOV IOC:m3.RBV LNLS:ANEL:corrente.VAL',
            description='',
            disabled=False
        )
        
        # class Button values for PVMonitor
        self.description='Start PV Monitoring'
        self.disabled=False
        self.button_style='success'
        self.tooltip='Click me'
        self.icon=''
        self.layout = widgets.Layout(width='300px')
        
        # Boxes
        self.pv_values = {}
        
        # PVs
        self.pv_list = []
        
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
                b.description='Start PV Monitoring'
                b.button_style='success'

                # Stop displaying the motors widgets, show only button and text box
                b.main_box.children = (b.main_box.children[0], b.text,)

                logprint("Stopped monitoring PVs " + ', '.join([pv.pvname for pv in b.pv_list]), config=b.config)

                # Reset motor list
                b.pv_list = []      
            else:
                # Change button appearence
                b.description='Stop PV Monitoring'
                b.button_style = 'danger'

                # Stop displaying text box
                b.main_box.children = (b.main_box.children[0],)

                # Get motors PV names from the text box
                pv_list_names = b.text.value.split(' ')
                logprint("Started monitoring PVs " + ', '.join(pv_list_names), config=b.config)

                # Create PVs and add a monitor callback to them
                # Also add these PVs values as children of main_box widget
                try:
                    b.pv_list = [PV(name) for name in pv_list_names]

                    for pv in b.pv_list:
                        pv.add_callback(b._monitor_callback)

                        value = pv.get()
                        b.pv_values[pv.pvname] = (value, str(value))

                        b.main_box.children += (widgets.HBox([widgets.Label(pv.pvname), widgets.Label(str(value))]),)

                    logprint("Monitoring PVs " + ', '.join(pv_list_names), config=b.config)        

                except Exception as e:
                    # If any error occurs, log that but dont stop code exection
                    logprint("Error in monitoring PVs " + ', '.join(pv_list_names), "[ERROR]", config=b.config)
                    logprint(str(e), "[ERROR]", config=b.config)

            # Re enable button
            b.disabled=False

            # Switch status
            b.monitoring_status = not b.monitoring_status
               

    def _monitor_callback(self, pvname='', value=0, char_value='', **kw):
        self.pv_values[pvname] = (value, "{:.3f}".format(value))
        
        for widget in self.main_box.children[1:]:
            if widget.children[0].value == pvname:
                widget.children[1].value = "{:.3f}".format(value)


    def display_monitor_pvs(self):
        display(self.main_box, self.output)
