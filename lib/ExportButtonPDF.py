import ipywidgets as widgets
from IPython.display import display
import time
from .utils import logprint
import os


class ExportButtonPDF(widgets.Button):
    def __init__(self, config, notebook_name, plots_list, *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        self.notebook_name = notebook_name
        self.description='Export Notebook to PDF'
        self.disabled=False
        self.button_style='warning' # 'success', 'info', 'warning', 'danger' or ''
        self.tooltip='Click me'
        self.icon=''
        self.layout = widgets.Layout(width='300px')
    
        self.on_click(self._export_button)
        
        self.plots_list = plots_list

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
            
            try:
                from IPython.display import Javascript
        
                ts = time.gmtime()
                time_stamp = time.strftime("%Y-%m-%d-%H:%M:%S", ts)
                output_file = time_stamp + "-main_notebook"

                display(Javascript('IPython.notebook.save_checkpoint();'))
                
                time.sleep(3)
                
                os.system("python3 -m nbconvert main_notebook.ipynb --output-dir=./exports --output=" + output_file + " --to pdf")
                
                for plot in b.plots_list:
                    plot[0].export = False
            except Exception as e:
                logprint(str(e), "[ERROR]", config=b.config)
            
            # Reenable button
            b.disabled = False
            b.button_style = 'warning'
            b.description='Export Notebook to PDF'
        
    def display_export_button(self):
        display(self)
                    