import json

from .studentapi import init_database, get_assignment_id
from ..api import SubmittedAssignment, Groupmember

from .baseapp import (
    NbGrader, nbgrader_aliases, nbgrader_flags)

import os

import re


aliases = {'tutor-file': 'GradelinksApp.tutor_file'}
aliases.update(nbgrader_aliases)
flags = {}
flags.update(nbgrader_flags)


class GradelinksApp(NbGrader):

    name = u'nbgrader-gradelinks'
    description = u'Outputs links for Formgrader'

    aliases = aliases
    flags = flags

    examples = """
        Gradelinks output links to Submitted Notebooks in Formgrader for given Tutor and Assignment.

            `nbgrader gradelinks <assignment id> <tutor>`

        If use without tutor or tutor is `all`, it outputs it for all tutors, grouped by tutor.

            `nbgrader gradelinks <assignment id>`

        If tutor is `None`, it outputs all links froum students without a tutor.

        Connection Tutor and Student must be given in yaml file (`--tutor-file <file path>`, default in course-dir root
        named `tutor.yaml`.
        Example:

                ---
                mainobject:
                  path: https://gp1test.cs.upb.de:8000/hub/nbgrader/
                  balance: -1
                  tutors:
                    -  jonas:
                        work: 100
                        email: jo2c5a5r2v2@temp.mailbox.org
                        students:
                          - boerding
                          - mfeldma2
                          - jharbig
                    -  thomas:
                        work: 50
                        email: k018kj8dh01@temp.mailbox.org
                        students:
                          - thomask2
                          - jrossel

        Tutor names must be unique and not be `all` or `None`. Every student has maximal one tutor.
        The variable `balance` in `mainobject` is to balance the students to correct between the tutors.
        If it contains something less than `0`, no balancing is done. Else, the balance number gives the allowed
        difference on students between a tutors students and the average of tutors students, wighted with variable
        `work` relative to 100 (a tutor may have balance*(work/100) as difference to average*(work/100)). The average is
        also computed wighted with `work` relative to 100.
            average = (sum of [for each tutor: number of students for that tutor / (work/100) ]
                + num students without tutor ) / number of tutors
        If a tutor has more than allowed number of students, the odd students are new allocated.
        All students, that has to be allocated, are allocated to tutors with less than average students
        (pseudo random as fair as possible). It is deterministic, so (without saving the result)
        every command for the same assignment and tutor (without deleting/adding submissions or tutors or change
        any association between tutor and student in mean time) will return the exact same list of links.
        After re allocating it is possible, to have less than allowed number of students (of most of tutors have more
        than average), but not to have more than allowed.
            `balance: -1` use for no allocation.
            `balance: 0` is recommended for fair allocation.
            `balance` > [number of all students] (maybe 7,000,000,000) use for only allocate students without tutor.
            `work` should be analogous to payed working hours of that tutor.

        Submitted Notebooks are default group by sub assignments. To change use flag -group-by-student



        """

    tutor_file = Unicode(
        '',
        config=True,
        help=dedent(
            """
            The yaml file for tutor-student-relationship.
            Default to <course dir>/tutor.yaml
            """
        )
    )
    def _classes_default(self):
        classes = super(GradelinksApp, self)._classes_default()
        classes.append(GradelinksApp)
        return classes

    def start(self):
        super(GradelinksApp, self).start()

        if len(self.extra_args) not in [1, 2]:
            self.fail("Assignment id not provided. Usage: nbgrader gradelinks assinment_id")
        self.session = init_database(db_url=self.db_url)
        assignment = self.extra_args[0]
        if len(self.extra_args) != 2:
            tutor = 'all'
        else:
            tutor = self.extra_args[1]
        rootpath = os.path.join(self.course_directory, "autograded")
        notepath = self.get_notepath(assignment, rootpath)
        #print("notepath", notepath)
        for p in notepath:
            note = json.load(open(p["file"]))
            id_note = note["cells"][0]["source"]
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

