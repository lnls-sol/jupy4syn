import ipywidgets as widgets
from IPython.display import display

class Configuration():
    def __init__(self):
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

    def display(self):
        display(self.checkbox_logprint_in_cell,
                widgets.HBox([widgets.Label("Notebook's name: "), self.notebook_name]), self.output)
