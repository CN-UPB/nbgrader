import os
import sys

import tempfile
import shutil
import pytest

from .. import run_nbgrader
from .base import BaseTestApp


def db_studentgrade(request):
    path = tempfile.mkdtemp()
    dbpath = os.path.join(path, "nbgrader_test.db")
    src = os.path.join("files", "test_studentgrade_db.db")
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

    def test_in_default_db(self, db):
        """Is the table 'groupmembers' created and the first entry done in an empty default database"""
        pass

    def test_double_studentgrade(self):
        """no error and no entry if an studentgraded notebook is again studentgraded"""

# two different notebooks for the same student and assignment will have an entry

# an normal entry  is done, if table "groupmember" already exists

# if a notebook contains wrong formatted identifier, no error and no entry happens

# if a notebook contains more than one indentifier, all identifier have entrys

# if a identifier is wrong in an notebook, the others will have correct entrys

# behavior if no submitted assignment

# behavior, if assignment does not exist
