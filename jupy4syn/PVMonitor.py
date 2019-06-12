# Widgets
import ipywidgets as widgets
from IPython.display import display

# EPICS and Py4Syn
from epics import PV, caget

# Jupy4Syn
from jupy4syn.utils import logprint
from jupy4syn.Configuration import Configuration


class PVMonitor(widgets.Button):
    def __init__(self, config=Configuration(), *args, **kwargs):
        """ The PVMonitor uses Jupyter button widgets to monitore PV values
        
        Keyword Arguments:
            config {[Configuration]} -- Configuration object that contains Jupyter Notebook runtime information
            (default: {Configuration()})
        """
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        
        # Text box to write the PV's
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
        
        # PVs
        self.pv_list = []
        self.pv_values = {}
        
        # Set callback function for click event
        self.monitoring_status = False
        self.on_click(self._monitor_button)
        
        # Main widget
        self.main_box = widgets.VBox([self.text, self])
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
                b.main_box.children = (b.text, b)

                logprint("Stopped monitoring PVs " + ', '.join([pv.pvname for pv in b.pv_list]), config=b.config)

                # Reset motor list
                b.pv_list = []      
            else:
                # Change button appearence
                b.description='Stop PV Monitoring'
                b.button_style = 'danger'

                # Stop displaying text box
                b.main_box.children = (b,)

                # Get motors PV names from the text box
                # Filter names
                pv_list_names = []
                names_comma_space_ent = []
                names_space = b.text.value.split(' ')
                for name in names_space:
                    names_comma_space = name.split(",")

                    for name_wout_comma in names_comma_space:
                        names_comma_space_ent.append(name_wout_comma.split("\n"))

                lin_names = sum(names_comma_space_ent, [])
                pv_list_names = [name for name in lin_names if name != "" and name != "\n"]
                
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


    def display(self):
        display(self.main_box, self.output)
