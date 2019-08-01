import yaml
import os

# Widgets
import ipywidgets as widgets
from IPython.display import display

# scan-utils
import scan_utils.configuration as scan_utils


class Configuration():
    def __init__(self, xpra=True):
        """
        The Configuration class provides runtime information for the Jupy4Syn classes.
        Such information are:
        - Printing log in the output cell
        - Notebook's name
        - Display settings
        - Plot information
        """
        self.xpra = xpra

        self.checkbox_logprint_in_cell = widgets.Checkbox(
            value=False,
            description="Print log in Notebook's cells",
            disabled=False,
            style={'description_width': 'initial'},
        )

        self.notebook_name = widgets.Text(
            value='',
            placeholder="Type the notebook's name without file format",
            description="",
            disabled=False,
            layout=widgets.Layout(width="300px")
        )

        self.config = {"log_cell": self.checkbox_logprint_in_cell}
        self.plots_list = []

        self.output = widgets.Output()

        self.yml_motors = scan_utils.Configuration()['motors']
        self.yml_counters = scan_utils.Configuration()['counters']

        try:
            user = os.environ["JUPYTERHUB_USER"]
        except KeyError:
            user = os.environ["HOME"].split("/")[-1]

        if self.xpra:
            with open("/etc/jupyterhub-displays/users_displays.yaml", "r") as file:
                data = yaml.safe_load(file)
        
            try:
                self.display_number = str(data[user])
            except KeyError:
                print("User '" + user + "' not defined in display users. Please, contact support.")

        else:
            self.display_number = '0'


    def display(self):
        """
        Display method
        """
        display(self.checkbox_logprint_in_cell,
                widgets.HBox([widgets.Label("Notebook's name: "), self.notebook_name]),
                self.output)
