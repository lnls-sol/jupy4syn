import yaml
import os

# Widgets
import ipywidgets as widgets
from IPython.display import display

# scan-utils
import scan_utils.configuration as scan_utils


class Configuration():
    def __init__(self):
        """
        The Configuration class provides runtime information for the Jupy4Syn classes.
        Such information are:
        - Printing log in the output cell
        - Notebook's name
        - Display settings
        - Plot information
        """
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

        # Test if execution is in a JupyterHub environment, a local Jupyter environment
        if 'JUPYTERHUB_USER' in os.environ.keys():
            user = os.environ['JUPYTERHUB_USER']
            jupyterhub = True
        else:
            jupyterhub = False

        if jupyterhub:
            with open("/etc/jupyterhub-displays/users_displays.yml", "r") as file:
                data = yaml.safe_load(file)

                # yaml.safe_load returns a NoneType object if the file is empty
                if data is None:
                    data = {}
            try:
                self.display_number = str(data[user])
            except KeyError as error:
                raise "User '" + user + "' not defined in display users.\
                      Please, contact support.\n" + str(error)

        else:
            self.display_number = ':0.0'

    def display(self):
        """
        Display method
        """
        display(self.checkbox_logprint_in_cell,
                widgets.HBox([widgets.Label("Notebook's name: "), self.notebook_name]),
                self.output)
