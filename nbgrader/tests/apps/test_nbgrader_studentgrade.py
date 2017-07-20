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



class TestNbGraderStudentgrade(BaseTestApp):

    def test_help(self):
        """Does the help display without error?"""
        run_nbgrader(["studentgrade", "--help-all"])

    def test_no_assignment_id(self):
        """Is the help displayed when no course id is given?"""
        run_nbgrader(["studentgrade"], retcode=1)

    def test_in_default_db(self, course_dir):
        """Is the table 'groupmembers' created and the first entry done in an empty default database"""
        self._copy_file(join("files", "studentgrade.ipynb"), join(course_dir, "autograded", "onlytest", "ps1", "matrikelnummer.ipynb"))
        self._copy_file(join("files", "studentgradetest.db"), join(course_dir, "gradebook.db"))
        #run_nbgrader(["studentgrade", "ps1", "--db", "sqlite:///" + join(course_dir, "gradebook.db")])
        run_nbgrader(["studentgrade", "ps1", "--course-dir", course_dir])

    def test_double_studentgrade(self):
        """no error and no entry if an studentgraded notebook is again studentgraded"""
        pass

# two different notebooks for the same student and assignment will have an entry

# an normal entry  is done, if table "groupmember" already exists

# if a notebook contains wrong formatted identifier, no error and no entry happens

# if a notebook contains more than one indentifier, all identifier have entrys

# if a identifier is wrong in an notebook, the others will have correct entrys

# behavior if no submitted assignment

# behavior, if assignment does not exist
