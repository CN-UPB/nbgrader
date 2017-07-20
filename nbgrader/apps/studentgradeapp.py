import json

from .studentapi import init_database, get_assignment_id
from ..api import SubmittedAssignment, Groupmember

from .baseapp import (
    NbGrader, nbgrader_aliases, nbgrader_flags)

import os

import re



aliases = {}
aliases.update(nbgrader_aliases)
flags = {}
flags.update(nbgrader_flags)


class StudentgradeApp(NbGrader):

    name = u'nbgrader-studentgrade'
    description = u'Save connection between submitted assignments and students (with identifier)'

    aliases = aliases
    flags = flags

    examples = """
        Studentgrade connects the submitted assignments to the students that worked in a group.
        Each group has one group account. They must write the matrikelnumber in
        an additional notebook named 'matrikelnummer.ipynb'

        You can run `nbgrader studentgrade` just in the top-level course folder.
        This command must be run after ´nbgrader autograde assignment01´.

        To connect the students identifier for their submissions on asignment01 run:

            nbgrader studentgrade asignment01

        In the 'matrikelnummer.ipynb' notebook the matrikelnumbers bust be in cell two an following
        (in the first cell may be some instruction for students). Not more than 'StudendgradeApp.MAX_MATRIKEL_NUMBERS'
        matrikelnumbers in each assignment. If more matrikelnumbers are given, the fist ones will be saved.

        If the syntax is not correct in one cell, the other cells will not be effected.
        If there is no correct line, this call will not do anything.
        The matrikelnumber must only contain numbers. No letters, spaces or other signs.
        """

    MAX_MATRIKEL_NUMBERS = 4

    def _classes_default(self):
        classes = super(StudentgradeApp, self)._classes_default()
        classes.append(StudentgradeApp)
        return classes

    def start(self):
        super(StudentgradeApp, self).start()

        if len(self.extra_args) != 1:
            self.fail("Assignment id not provided. Usage: nbgrader studentgrade assinment_id")
        #self.session = init_database(db_url='sqlite:///gradebook.db')
        print(self.db_url)
        self.session = init_database(db_url=self.db_url)
        assignment = self.extra_args[0]
        rootpath = os.path.join(self.course_directory, "autograded")
        notepath = self.get_notepath(assignment, rootpath)
        #print("notepath", notepath)
        for p in notepath:
            note = json.load(open(p["file"]))
            #id_note = note["cells"][0]["source"]
            id_note = note["cells"][1:1 + self.MAX_MATRIKEL_NUMBERS]
            for item in self.extract_matrikel_mail(id_note):
                assignment_id = get_assignment_id(assignment)
                if not item[1] is None:
                    self.save_identifier(item[0], p["acc"], assignment_id, item[1])
                else:
                    self.save_identifier(item[0], p["acc"], assignment_id)
        self.session.commit()
        gr = self.session.query(Groupmember).all()
        print("len", len(gr))
        for g in self.session.query(Groupmember).all():
            print("saved ids", g)

    def save_identifier(self, identifier, account, assignment_id, mail=""):
        """
        Saves groupmeber entry to database. Database as to be connected with 'init_database'
        :param identifier: unique identifier of each groupmember (like matrikel number)
        :param account: name of the group account
        :param assignment_id: id of assignment where the groubmembers shell be collected
        :param mail: mail address of that groupmember (optional)
        :return:
        """
        #print("save id:", identifier, account)
        sub_ass = self.session.query(SubmittedAssignment).filter(
                SubmittedAssignment.assignment_id == assignment_id,
                SubmittedAssignment.student_id == account
            ).first()
        #print("sub_ass", sub_ass)
        if sub_ass is not None:
            if self.session.query(Groupmember).filter(
                            Groupmember.sub_notebook_id == sub_ass.id,
                            Groupmember.groupmember_id == identifier
            ).first() is not None:
                #print("exists", identifier, sub_ass.id)
                return
            new_mem = Groupmember(sub_notebook_id=sub_ass.id, groupmember_id=identifier, mail=mail)
            self.session.add(new_mem)

    def get_notepath(self, assignment, root_path):
        """
        :param assignment: assignment name
        :param root_path: path of folder were the accounts have their sub folders
        :return: a list of dicts with each two entry
            'acc': name of the student account
            'file': path of the notebook file where the students have written the identifier
                    and mail addresses of all group members of in that assignment
        """
        res = []
        for p in os.listdir(root_path):

            #if os.path.isdir(p):
                np = dict()
                np['acc'] = p
                assignment_dir = os.path.join(root_path, p, assignment)
                #print("assignment_dir", assignment_dir)
                if os.path.exists(os.path.join(assignment_dir, "matrikelnummer.ipynb")):
                    np['file'] = os.path.join(assignment_dir, "matrikelnummer.ipynb")
                    res += [np]
        return res

    def extract_matrikel_mail(self, id_note):
        r = []
        # actually new code:
        for i in id_note:
            matrikel = i["source"][0]

            email = None

            if matrikel.isnumeric():
                tmp_r = (matrikel,  email)
                r.append(tmp_r)
        print(r)
        return r
