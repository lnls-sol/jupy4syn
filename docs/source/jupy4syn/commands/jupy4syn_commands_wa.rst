
=========
WaCommand
=========

.. module:: jupy4syn.commands.WaCommand
   :synopsis: Python class for Jupy4Syn Commands WaCommand

The WaCommand is the analogue of SPEC "wa", but using the ipywidgets
interface to list all motors and their User and Dial positions.

The WaCommand class extends its interface methods to execute, parse initial
arguments and display.
In order to use WaCommand, one should call the :class:`jupy4syn.CommandButton`
with the command 'wa'. The WaCommand uses no extra arguments.

See the examples:

.. figure::  ../../images/WaCommand_example_1.png
   :align:   center

Using Jupy4Syn Commands WaCommand
=================================

Usage of Python class using basic WaCommand fields.

.. autoclass:: WaCommand
   :members:
