import os
import plotly
from pkg_resources import resource_string


class ReportGenerator():
    report = '''
<html>
    <head>
        <link rel="stylesheet" href="bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <div class="container">
            <div class="col-md-10">'''

    def __init__(self, outputFolder):
        if not os.path.isdir(outputFolder):
            try:
                os.makedirs(outputFolder)
            except OSError:  # Guard against race condition
                raise
        self.outputFolder = outputFolder

    def addTitle(self, title):
        self.report += '\n<h1>' + title + '</h1>'

    def getObjectDoc(self, obj):
        return self.readResource(type(obj).__name__ + '.html')

    def addDoc(self, obj):
        doc = self.getObjectDoc(obj)
        self.report += '\n' + doc

    def addTable(self, table):
        table = table.replace('<table>', '<table class="table table-striped">')
        self.report += '\n' + table

    def addPlot(self, plot, name):
        self.report += '\n<h2>' + name + '</h2>'
        plotUrl = name + '.html'
        plotly.offline.plot(
            plot,
            filename=self.outputFolder + '/' + plotUrl,
            auto_open=False)
        self.report += '''
        <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
src="''' + plotUrl + '''"></iframe>'''

    def generateReport(self):
        self.report += '''
            </div>
        </div>
    </body>
</html>'''
        self.write('index.html', self.report)
        self.write(
            'bootstrap.min.css',
            resource_string('GageRnR.resources', 'bootstrap.min.css').decode("utf-8"))

    def write(self, filename, data):
        f = open(self.outputFolder + '/' + filename, 'w')
        f.write(data)
        f.close()

    def readResource(self, filename):
        return resource_string('GageRnR.resources', filename).decode("utf-8")
