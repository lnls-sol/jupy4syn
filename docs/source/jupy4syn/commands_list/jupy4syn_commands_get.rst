==========
getCommand
==========

.. module:: jupy4syn.commands.getCommand
   :synopsis: Python class for Jupy4Syn get Command

The getCommand is the analogue of pyepics caget, but using the ipywidgets
interface to show the PV value in a Jupyter Notebook.

The getCommand class extends its interface methods to execute, parse initial
arguments and display.
In order to use getCommand, one should call the :class:`jupy4syn.commandButton`
with the command 'get'. The arguments can be a string with the PV name or
mnemonic, or it can be a list with 1 strings, the PV name or mnemonic.

See the examples:

.. figure::  ../../images/getCommand_example_1.png
   :align:   center


.. figure::  ../../images/getCommand_example_2.png
   :align:   center


Jupy4Syn getCommand module
==========================

.. autoclass:: getCommand
   :members:

