# Jupy4Syn
from jupy4syn.Configuration import Configuration

from jupy4syn.commands.ct_command import CtCommand
from jupy4syn.commands.move_command import MoveCommand
from jupy4syn.commands.wa_command import WaCommand
from jupy4syn.commands.wm_command import WmCommand
from jupy4syn.commands.energy_scan_gui_command import EnergyScanGuiCommand
from jupy4syn.commands.scan_gui_command import ScanGuiCommand
from jupy4syn.commands.scaler_command import ScalerCommand
from jupy4syn.commands.vortex_command import VortexCommand
from jupy4syn.commands.pymca_command import PymcaCommand
from jupy4syn.commands.put_command import PutCommand
from jupy4syn.commands.get_command import GetCommand
from jupy4syn.commands.slits_command import SlitsCommand
from jupy4syn.commands.motors_command import MotorsCommand
from jupy4syn.commands.user_command import UserCommand


class CommandDict():

    def __init__(self, config=Configuration()):
        """
        **Constructor**

        Parameters
        ----------
        command : :obj:`string`
            Command that will be executed at the button click
        config : :py:class:`Configuration <jupy4syn.Configuration.Configuration>`, optional
            Configuration object that contains Jupyter Notebook runtime information, by default Configuration()

        Examples
        ----------
        >>> config = Configuration()
            config.display()
        >>> command = CommandButton(config)
            command.display()
        """

        # Config
        self.config = config

        # Dictionaries
        self.commands_dict = {
            "": UserCommand(config),
            "ct": CtCommand(),
            "wa": WaCommand(),
            "wm": WmCommand(),
            "move": MoveCommand(),
            "scaler": ScalerCommand(config),
            "scan_gui": ScanGuiCommand(config),
            "energy_scan_gui": EnergyScanGuiCommand(config),
            "vortex": VortexCommand(config),
            "pymca": PymcaCommand(config),
            "put": PutCommand(config),
            "get": GetCommand(config),
            "slits": SlitsCommand(config),
            "motors": MotorsCommand(config)
        }

    def execute(self, command, parameters):
        if command not in self.commands_dict.keys():
            return self.commands_dict[""].exec(command + ' ' + parameters)

        return self.commands_dict[command].exec(parameters)

    def textbox_args(self, command, initial_args):
        if command not in self.commands_dict.keys():
            return self.commands_dict[""].args(initial_args)

        return self.commands_dict[command].args(initial_args)

    def text_box(self, command, initial_args):
        if command not in self.commands_dict.keys():
            return self.commands_dict[""].text_box(initial_args)

        return self.commands_dict[command].text_box(initial_args)
