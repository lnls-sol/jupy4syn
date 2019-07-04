import time

# Jupy4Syn
from jupy4syn.Configuration import Configuration
from jupy4syn.utils import logprint

from jupy4syn.commands.ctCommand import ctCommand
from jupy4syn.commands.moveCommand import moveCommand
from jupy4syn.commands.waCommand import waCommand
from jupy4syn.commands.wmCommand import wmCommand
from jupy4syn.commands.energyscanCommand import energyscanCommand
from jupy4syn.commands.scanCommand import scanCommand
from jupy4syn.commands.scalerCommand import scalerCommand
from jupy4syn.commands.vortexCommand import vortexCommand
from jupy4syn.commands.pymcaCommand import pymcaCommand
from jupy4syn.commands.putCommand import putCommand
from jupy4syn.commands.getCommand import getCommand
from jupy4syn.commands.slitsCommand import slitsCommand
from jupy4syn.commands.xpra_scalerCommand import xpra_scalerCommand
from jupy4syn.commands.xpra_scanCommand import xpra_scanCommand
from jupy4syn.commands.xpra_energyscanCommand import xpra_energyscanCommand
from jupy4syn.commands.xpra_vortexCommand import xpra_vortexCommand
from jupy4syn.commands.xpra_slitsCommand import xpra_slitsCommand

class commandDict():
    def __init__(self, config=Configuration(), *args, **kwargs):
        """
        **Constructor**

        Parameters
        ----------
        command: `string`
            Command that will be executed at the button click
        config: `jupy4syn.Configuration`, optional
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
            "ct": ctCommand(),
            "wa": waCommand(),
            "wm": wmCommand(),
            "move": moveCommand(),
            "scaler": scalerCommand(),
            "scan_gui": scanCommand(),
            "energy_scan_gui": energyscanCommand(),
            "vortex": vortexCommand(),
            "pymca": pymcaCommand(),
            "put": putCommand(config),
            "get": getCommand(config),
            "slits": slitsCommand(config),
            "xpra_scaler": xpra_scalerCommand(config),
            "xpra_scan_gui": xpra_scanCommand(config),
            "xpra_energy_scan_gui": xpra_energyscanCommand(config),
            "xpra_vortex": xpra_vortexCommand(config),
            "xpra_slits": xpra_slitsCommand(config)
        }

    def execute(self, command, parameters):
        return self.commands_dict[command].exec(parameters)

    def textbox_args(self, command, initial_args):
        return self.commands_dict[command].args(initial_args)

    def show_text_box(self, command, initial_args):
        return self.commands_dict[command].show(initial_args)
