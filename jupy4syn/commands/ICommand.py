from abc import ABC, abstractmethod

class ICommand(ABC):

    @abstractmethod
    def exec(self, parameters):
        """
        Abstract method to execute the command.

        Parameters
        ----------
        parameters: `str` or `list`
            The parameters that will be sent to execution as a shell argument

        Returns
        -------
        None
        """

        raise NotImplementedError

    @abstractmethod
    def args(self, initial_args):
        """
        Abstract method to get initial arguments of the command. These arguments will be
        show at the text box (if the text box is enabled for this command, see :method:show).

        Parameters
        ----------
        initial_args: `str` or `list`
            The initial arguments that will be show in the text box and will be sent to execution as shell arguments

        Returns
        -------
        out : `str`
            Returns a single string with the arguments or its representation
        """

        raise NotImplementedError

    @abstractmethod
    def show(self, initial_args):
        """
        Abstract method check if the command will need a text box.

        Parameters
        ----------
        initial_args: `str` or `list`
            The initial arguments that will be used to check if a text box will be needed

        Returns
        -------
        out : `bool`
            Returns True if a text box will be needed, False otherwise.
        """

        raise NotImplementedError
