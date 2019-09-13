==========
putCommand
==========

.. module:: jupy4syn.commands.putCommand
   :synopsis: Python class for Jupy4Syn put Command

The putCommand is the analogue of pyepics caput, but using the ipywidgets
interface to set the PV value in a Jupyter Notebook.

The putCommand class extends its interface methods to execute, parse initial
arguments and display.
In order to use putCommand, one should call the :class:`jupy4syn.commandButton`
with the command 'put'. The arguments can be a string with the PV name or
mnemonic, or it can be a list with 2 strings, the PV name or mnemonic and the
value to be put when the button is clicked.

If the value to be put is provided, the text in the textbox will not be
editable.

If only the PV name or mnemonic is provided, the actual value of the PV will
be displayed in the textbox.

See the examples:

.. figure::  ../../images/putCommand_example_1.png
   :align:   center


.. figure::  ../../images/putCommand_example_2.png
   :align:   center

.. figure::  ../../images/putCommand_example_3.png
   :align:   center


Jupy4Syn putCommand module
==========================

.. autoclass:: putCommand
   :members:

