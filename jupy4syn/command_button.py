import time

# Widgets
import ipywidgets as widgets
from IPython.display import display

# Jupy4Syn
from jupy4syn.Configuration import Configuration
from jupy4syn.command_dict import CommandDict
from jupy4syn.utils import logprint


class CommandButton(widgets.Button):

    def __init__(self, command="", default_args="", config=Configuration()):
        """
        **Constructor**

        Parameters
        ----------
        command : :obj:`string`, optional
            Command that will be executed at the button click, by default an empty string
        default_args : :obj:`string`, optional
            If provided, command will be executed with these parameters and the textbox will not be displayed,
            by default an empty string
        config : :py:class:`Configuration <jupy4syn.Configuration.Configuration>`, optional
            Configuration object that contains Jupyter Notebook runtime information, by default Configuration()

        Examples
        ----------
        >>> config = Configuration()
            config.display()
        >>> command = commandButton("energy_scan_gui", "energy", config)
            command.display()
        """

        widgets.Button.__init__(self)

        # Config
        self.config = config

        # Command Dictionary
        self.command = command
        self.command_dict = CommandDict(config=self.config)

        self.parsed_args = self.command_dict.textbox_args(command, default_args)
        self.show_text_box, self.enable_text_box = self.command_dict.text_box(command, default_args)

        # class Button values for MonitorScanSave
        self.description = 'Execute Command ' + '"' + self.command + '"'
        self.disabled = False
        self.button_style = 'success'
        self.tooltip = 'Click me'
        self.icon = ''
        self.layout = widgets.Layout(width='300px')

        # Arguments textbox
        self.arguments = widgets.Text(
            value=str(self.parsed_args),
            placeholder="Type the arguments",
            description="",
            disabled=not self.enable_text_box,
            layout=widgets.Layout(width="300px")
        )

        # Logging
        self.output = widgets.Output()

        # Set callback function for click event
        self.on_click(self._start_button)

        # Widgets displays
        self.start_button = widgets.VBox([self])

    @staticmethod
    def _start_button(b):
        # Clear previous logs outputs
        b.output.clear_output()

        # with statement to output logs in stdou (if this option is enabled)
        with b.output:
            # Change button to a "clicked status"
            b.disabled = True
            b.button_style = ''
            b.description = 'Executing...'

            try:
                logprint("Executing command " + b.command, config=b.config)

                b.command_dict.execute(b.command, b.arguments.value)

                logprint("Finished executing command " + b.command, config=b.config)
            except Exception as error:
                # If any error occurs, log that but dont stop code exection
                logprint("Error in executing command " + b.command, "[ERROR]", config=b.config)
                logprint(str(error), "[ERROR]", config=b.config)
            except SystemExit as value:
                logprint("Finished executing command " + b.command +
                         " with SystemExit(" + str(value) + ")", config=b.config)

            # We should sleep for some time to give some responsiveness to the user
            time.sleep(1.0)

            # Change button layout monitoring
            b.disabled = False
            b.button_style = 'success'
            b.description = 'Execute Command ' + '"' + b.command + '"'

    def display(self):
        # Some commands needs arguments that will be acquired through a text box
        # For the commands that don't need such arguments, the text box will be omitted
        if self.show_text_box:
            display(self.arguments,
                    self,
                    self.output
                    )
        else:
            display(self,
                    self.output
                    )
