import os
import stat
import sys
from output_viewer.build import build_viewer
from output_viewer.utils import rechmod
from output_viewer.index import OutputIndex, OutputPage, OutputFile, OutputRow, OutputGroup
from acme_diags.acme_parameter import ACMEParameter


class OutputViewer(object):
    def __init__(self, path, index_name='Results'):
        self.path = os.path.abspath(path)
        self.index = OutputIndex(index_name)
        self.group = None
        self.page = None

    def add_page(self, name, cols):
        self.page = OutputPage(name, cols)
        self.index.addPage(self.page)

    def add_row(self, var_name, description):
        ''' Adds a description and all of the files in self.path to an 
        OutputRow, which is then added to the current page'''
        cols = []
        cols.append('Some description for %s' % description)

        files_in_path = [fnm for fnm in os.listdir(self.path) if '.png' in fnm]
        for f in files_in_path:
            cols.append(OutputFile(f))

        if self.group is None:
            self.group = OutputGroup('Variables for this data set')
        if self.page is not None:
            row = OutputRow(var_name, cols)
            self.page.addGroup(self.group)
            self.page.addRow(row, 0)
        else:
            raise RuntimeError('You need to add a page with add_page() before calling add_row()')

    def generate_viewer(self):
        print 'os.path.join(self.path, "index.json"):'
        print os.path.join(self.path, "index.json")

        self.index.toJSON(os.path.join(self.path, "index.json"))

        default_mask = stat.S_IMODE(os.stat(self.path).st_mode)
        rechmod(self.path, default_mask)

        if os.access(self.path, os.W_OK):
            default_mask = stat.S_IMODE(os.stat(self.path).st_mode)  # mode of files to be included
            build_viewer(os.path.join(self.path, "index.json"), diag_name="ACME Diagnostics", default_mask=default_mask)

        if os.path.exists(os.path.join(self.path, "index.html")):
            should_open = raw_input("Viewer HTML generated at %s/index.html. Would you like to open in a browser? y/[n]: " % self.path)
            if should_open and should_open.lower()[0] == "y":
                import webbrowser
                webbrowser.open("file://" + os.path.join(self.path, "index.html"))
        else:
            raise RuntimeError("Failed to generate the viewer.")
