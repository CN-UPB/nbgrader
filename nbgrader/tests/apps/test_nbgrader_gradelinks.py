'''
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


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TestNbGraderStudentgrade(BaseTestApp):

    def test_help(self):
        """Does the help display without error?"""
        run_nbgrader(["gradelinks", "--help-all"])

    def test_no_assignment_id(self):
        """Is the help displayed when no course id is given?"""
        run_nbgrader(["gradelinks"], retcode=1)


#TODO: automate test for output
    def test_in_example_db(self, course_dir):
        """Is the table 'groupmembers' created and the first entry done in an empty default database"""
        self._copy_file(join("files", "generate_links_test.yaml"), join(course_dir, "tutor.yaml"))
        self._copy_file(join("files", "generate_links_test.db"), join(course_dir, "gradebook.db"))
        #run_nbgrader(["studentgrade", "ps1", "--db", "sqlite:///" + join(course_dir, "gradebook.db")])
        print(bcolors.OKGREEN, "Output should be:",
              "https://gp1test.cs.upb.de:8000/hub/nbgrader/gp1test/submissions/01036da386544236a2971a2564c4d802",
              "and two other links", bcolors.ENDC, end="#################################\n", sep="\n")
        run_nbgrader(["gradelinks", "SHK_Test", "jonas", "--course-dir", course_dir])

        print(bcolors.OKGREEN, "Output should be:",
              "https://gp1test.cs.upb.de:8000/hub/nbgrader/gp1test/submissions/7e281d1bc7fd4da1854670a1ac48bfd5",
              "and one other link", bcolors.ENDC, end="#################################\n", sep="\n")
        run_nbgrader(["gradelinks", "SHK_Test", "thomas", "--course-dir", course_dir])
        print(bcolors.OKGREEN, "Output should be:",
              "https://gp1test.cs.upb.de:8000/hub/nbgrader/gp1test/submissions/a856a07072694dcbb1c3925bb2a261be",
              "and two other links", bcolors.ENDC, end="#################################\n", sep="\n")
        run_nbgrader(["gradelinks", "SHK_Test", "None", "--course-dir", course_dir])
        print(bcolors.OKGREEN, "Output should be:",
              "The links above grouped by tutors", bcolors.ENDC, end="#################################\n", sep="\n")
        run_nbgrader(["gradelinks", "SHK_Test", "--course-dir", course_dir])


# Will generate two links for two notebooks and group by notebooks\
'''