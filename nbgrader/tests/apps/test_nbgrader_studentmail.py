import os
import sys

import tempfile
import shutil
import pytest
import sqlalchemy

from os.path import join, isfile

from .. import run_nbgrader
from .base import BaseTestApp
from .conftest import notwindows


def db_studentgrade(request):
    path = tempfile.mkdtemp()
    dbpath = os.path.join(path, "Studentgradetest")
    src = os.path.join("files", "Studentgradetest")
    def fin():
        rmtree(path)
    request.addfinalizer(fin)

    shutil.copy(src, dbpath)
    return "sqlite:///" + dbpath



class TestNbGraderStudentmail(BaseTestApp):

    def test_help(self):
        """Does the help display without error?"""
        run_nbgrader(["studentmail", "--help-all"])

    def test_no_assignment_id(self):
        """Is the help displayed when no course id is given?"""
        run_nbgrader(["studentmail"], retcode=1)

    def test_in_default_db(self, course_dir):
        """Is the table 'groupmembers' created and the first entry done in an empty default database"""
        self._copy_file(join("files", "studentgrade.ipynb"), join(course_dir, "autograded", "onlytest", "ps1", "matrikelnummer.ipynb"))
        self._copy_file(join("files", "studentgradetest.db"), join(course_dir, "gradebook.db"))
        #run_nbgrader(["studentgrade", "ps1", "--db", "sqlite:///" + join(course_dir, "gradebook.db")])
        run_nbgrader(["studentgrade", "ps1", "--course-dir", course_dir])
        run_nbgrader(["studentmail", "ps1", "--course-dir", course_dir])
