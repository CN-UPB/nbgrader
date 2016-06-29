#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

from nbconvert.nbconvertapp import DottedOrNone
from nbconvert.writers import FilesWriter

class NbGraderWriter(FilesWriter):
    """A writer that removes undesirable output"""

    def __init__(self, **kw):
        super(NbGraderWriter, self).__init__(**kw)

    def write(self, output, resources, notebook_name=None, **kw):
        """Basically just call baseclass write function
        after having stripped out needless content"""

        print("in NbGraderWriter")

        return super(NbGraderWriter, self).write(output, resources, notebook_name, **kw)