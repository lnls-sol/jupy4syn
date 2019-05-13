import ipywidgets as widgets
from IPython.display import display
import time


class ExportButtonPDF(widgets.Button):
    def __init__(self, config, plots_list, *args, **kwargs):
        widgets.Button.__init__(self, *args, **kwargs)
        
        # Config
        self.config = config
        self.description='Export Notebook to PDF'
        self.disabled=False
        self.button_style='warning' # 'success', 'info', 'warning', 'danger' or ''
        self.tooltip='Click me'
        self.icon=''
        self.layout = widgets.Layout(width='300px')
    
        self.on_click(self._export_button)
        
        self.plots_list = plots_list
    
    @staticmethod
    def _export_button(b):
        # Change button to a "clicked status"
        b.disabled = True
        b.button_style = ''
        b.description='Exporting...'

        # We should sleep for some time to give some responsiveness to the user
        time.sleep(0.5)
        
        try:
            from IPython.display import Javascript
    
            year_month_day = time.strftime("%Y-%m-%d", ts)
            time_stamp = time.strftime("%Y-%m-%d-%H:%M:%S", ts)
            output_file = time_stamp + "-main_notebook"

            display(Javascript('IPython.notebook.save_checkpoint();'))
            
            time.sleep(3)
            
            os.system("python3 -m nbconvert main_notebook.ipynb --output-dir=./exports --output=" + output_file + " --to pdf")
            
            for plot in b.plots_list:
                plot[0].export = False
        except:
            pass
        
        # Reenable button
        b.disabled = False
        b.button_style = 'warning'
        b.description='Export Notebook to PDF'
        
    def display_export_button(self):
        display(self)
                    