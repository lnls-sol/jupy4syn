import ipywidgets as widgets
from IPython.display import display
import time
from .utils import logprint
import os


class ExportButtonLatex(widgets.Button):
    def __init__(self, config, *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        self.notebook_name = config.notebook_name.value
        self.plots_list = config.plots_list

        self.description='Export Notebook to Latex'
        self.disabled=False
        self.button_style='warning' # 'success', 'info', 'warning', 'danger' or ''
        self.tooltip='Click me'
        self.icon=''
        self.layout = widgets.Layout(width='300px')
    
        self.on_click(self._export_button)

        self.output = widgets.Output()
    
    @staticmethod
    def _export_button(b):
        with b.output:
            # Change button to a "clicked status"
            b.disabled = True
            b.button_style = ''
            b.description='Exporting...'

            # We should sleep for some time to give some responsiveness to the user
            time.sleep(0.5)

            # Get actual values
            b.notebook_name = b.config.notebook_name.value
            b.plots_list = b.config.plots_list
            
            try:
                for plot in b.plots_list:
                    plot.export = True
                
                from IPython.display import Javascript
        
                ts = time.gmtime()
                time_stamp = time.strftime("%Y-%m-%d-%H:%M:%S", ts)
                output_file = time_stamp + '-' + b.notebook_name

                time.sleep(1.0)

                display(Javascript('IPython.notebook.save_checkpoint();'))
                
                os.system("python3 -m nbconvert ./" + b.notebook_name + ".ipynb --template=nbextensions --output-dir=./exports --output=" + output_file + " --to latex")
                
                time.sleep(1.0)
                
                for plot in b.plots_list:
                    plot.export = False

            except Exception as e:
                logprint(str(e), "[ERROR]", config=b.config)
            
            # Reenable button
            b.disabled = False
            b.button_style = 'warning'
            b.description='Export Notebook to Latex'
        
    def display(self):
        display(self, self.output)
                    