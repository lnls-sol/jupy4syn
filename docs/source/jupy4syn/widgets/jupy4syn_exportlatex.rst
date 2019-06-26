==============
Latex Exporter
==============

.. module:: jupy4syn.ExportButtonLatex
   :synopsis: Python class for Jupy4Syn Latex Exporter

The ExportButtonLatex class provides an ipywidgets interface to help exporting
the notebook in Latex format. It shows:

- a button to export

.. figure::  ../../images/exportlatex_example_1.png
   :align:   center

   ExportButtonLatex example in a Jupyter notebook.

.. warning::
   In order to export the notebook, the user MUST write the notebook's name in the correspondent
   Configuration text box as shown in the example bellow:

   .. figure::  ../../images/configuration_example_1.png
      :align:   center

      Notebook's name in Configuration text box.

   See :class:`jupy4syn.Configuration` for more details.

Using Jupy4Syn Latex Exporter module
====================================

Usage of Python class using basic Latex Exporter fields.

.. autoclass:: ExportButtonLatex
   :members:
