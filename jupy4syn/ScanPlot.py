# Plotly
import plotly.graph_objs as go

# Py4Syn
import py4syn.utils.scan as sc


class ScanPlot():
    def __init__(self, name, *args, **kwargs):
        # Scan figure widget that will be displayed
        self.figure = go.FigureWidget()
      

    def add_scatter(self, initial_x, initial_y, name, mode='lines+markers'):
        self.figure.add_traces([go.Scatter(x=initial_x,
                                          y=initial_y,
                                          mode=mode,
                                          name=name)])
        
        
    def plot(self, x, y, label):
        for trace in self.figure['data']:
            if trace['name'] == label:
                trace['x'] = x
                trace['y'] = y
    
    
    def display(self):
        return self.figure
