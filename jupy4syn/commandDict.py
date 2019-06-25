import time
import subprocess

# scan-utils
from scan_utils import wa, ct, wm, move

# Jupy4Syn
from jupy4syn.Configuration import Configuration
from jupy4syn.utils import logprint


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
        self.exec_dict = {
            "ct": self.ctExec,
            "wa": self.waExec,
            "wm": self.wmExec,
            "move": self.moveExec,
            "scaler": self.scalerExec,
            "scan_gui": self.scan_guiExec,
            "energy_scan_gui": self.energy_scan_guiExec,
            "vortex": self.vortexExec,
            "pymca": self.pymcaExec
        }

        self.args_dict = {
            "ct": self.ctArgs,
            "wa": self.waArgs,
            "wm": self.wmArgs,
            "move": self.moveArgs,
            "scaler": self.scalerArgs,
            "scan_gui": self.scan_guiArgs,
            "energy_scan_gui": self.energy_scan_guiArgs,
            "vortex": self.vortexArgs,
            "pymca": self.pymcaArgs
        }

        self.show_box = {
            "ct": self.ctShow,
            "wa": self.waShow,
            "wm": self.wmShow,
            "move": self.moveShow,
            "scaler": self.scalerShow,
            "scan_gui": self.scan_guiShow,
            "energy_scan_gui": self.energy_scan_guiShow,
            "vortex": self.vortexShow,
            "pymca": self.pymcaShow
        }

    def execute(self, command, parameters):
        return self.exec_dict[command](parameters)

    def textbox_args(self, command, initial_args):
        return self.args_dict[command](initial_args)

    def show_text_box(self, command, initial_args):
        return self.show_box[command](initial_args)

    def ctExec(self, parameters):
        return ct.main(parameters.split())

    def waExec(self, parameters):
        return wa.main()

    def wmExec(self, parameters):
        return  wm.main(parameters.split())

    def moveExec(self, parameters):
        return move.main(parameters.split())

    def scalerExec(self, parameters):
        subprocess.Popen(["scaler", "-m", parameters])

    def vortexExec(self, parameters):
        subprocess.Popen(["vortex", "-m", parameters])

    def scan_guiExec(self, parameters):
        subprocess.Popen(["scan_gui"])

    def energy_scan_guiExec(self, parameters):
        subprocess.Popen(["energy_scan_gui", parameters])

    def pymcaExec(self, parameters):
        subprocess.Popen(["pymca"])

    def ctArgs(self, initial_args):
        return initial_args

    def waArgs(self, initial_args):
        return initial_args

    def wmArgs(self, initial_args):
        arg_str = ""

        if initial_args == "":
            arg_str = "<motor1> <motor2> [...]"
        else:
            if isinstance(initial_args, (list, tuple)):
                for motor in initial_args:
                    arg_str += motor + " "
            else:
                arg_str += initial_args

        return arg_str

    def moveArgs(self, initial_args):
        arg_str = ""

        if initial_args == "":
            arg_str = "<motor1> <value1> <motor2> <value2> [...]"
        else:
            if isinstance(initial_args, (list, tuple)):
                for i in range(1, len(initial_args) + 1):
                    arg_str += initial_args[i - 1] + (" <value%d> " % i)
            else:
                arg_str += initial_args + " <value>"

        return arg_str

    def scalerArgs(self, initial_args):
        if not initial_args:
            return "P=<PV>"
        else:
            return initial_args

    def vortexArgs(self, initial_args):
        if not initial_args:
            return "P=<PV>"
        else:
            return initial_args

    def scan_guiArgs(self, initial_args):
        return initial_args

    def energy_scan_guiArgs(self, initial_args):
        if not initial_args:
            return "<motor>"
        else:
            return initial_args

    def pymcaArgs(self, initial_args):
        return initial_args

    def ctShow(self, initial_args):
        return True

    def waShow(self, initial_args):
        return False

    def wmShow(self, initial_args):
        if not initial_args:
            return True
        else:
            return False        

    def moveShow(self, initial_args):
        return True

    def scalerShow(self, initial_args):
        if not initial_args:
            return True
        else:
            return False  

    def scan_guiShow(self, initial_args):
        return False

    def energy_scan_guiShow(self, initial_args):
        if not initial_args:
            return True
        else:
            return False  

    def vortexShow(self, initial_args):
        if not initial_args:
            return True
        else:
            return False  

    def pymcaShow(self, initial_args):
        return False
