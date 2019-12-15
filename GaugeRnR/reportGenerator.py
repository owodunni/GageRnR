import os
import plotly
from pkg_resources import resource_string, resource_listdir


class ReportGenerator():
    report = '''
<html>
    <head>
        <link rel="stylesheet" href="bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>'''

    def __init__(self,outputFolder):
        if not os.path.isdir(outputFolder):
            try:
                os.makedirs(outputFolder)
            except OSError as exc: # Guard against race condition
                    raise
        self.outputFolder = outputFolder

    def addTitle(self, title):
        self.report += '\n        <h1>' + title + '</h1>'
    
    def addTable(self, table):
        table = table.replace('<table>','<table class="table table-striped">')
        self.report += '\n' + table
    
    def addPlot(self, plot, name):
        plotUrl = name + '.html'
        plotly.offline.plot(
            plot,
            filename = self.outputFolder + '/' + plotUrl,
            auto_open=False)
        self.report += '''
        <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
src="''' + plotUrl + '''"></iframe>'''
    
    def generateReport(self):
        self.report += ''' 
    </body>
</html>'''
        self.write('index.html', self.report)
        self.write(
            'bootstrap.min.css',
            resource_string('GaugeRnR.resources','bootstrap.min.css').decode("utf-8"))
    
    def write(self, filename, data):
        f = open(self.outputFolder + '/' + filename,'w')
        f.write(data)
        f.close()

