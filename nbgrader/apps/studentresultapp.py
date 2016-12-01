from .baseapp import NbGrader
from .studentapi import *

aliases = {}
flags = {}


class StudentResultApp(NbGrader):

    name = u'nbgrader-studentmail'
    description = u'Send mails with results to given mailadress from student'

    aliases = aliases
    flags = flags

    examples = """
        Returns the results for all students an all assignments.

        For example:

            nbgrader studentresult

        prints

            Results:
            1234567 {'hb2': 1.5, 'ps2': 0, 'ps1': 0, 'ps_test': 0, 'aufg1': 0}
            7007607 {'hb2': 1.5, 'ps2': 0, 'ps1': 0, 'ps_test': 0, 'aufg1': 0}
        """

    def _classes_default(self):
        classes = super(StudentResultApp, self)._classes_default()
        classes.append(StudentResultApp)
        return classes

    def start(self):
        super(StudentResultApp, self).start()

        print('---')
        print('submit_details:')
        students = get_student_list_summery()
        if len(self.extra_args) > 0:
            tmp_students = dict()
            for arg in self.extra_args:
                if arg in students:
                    tmp_students[arg] = students[arg]
            students = tmp_students
        for p in sorted(students):
            print(' - matrikelnr: "', p, '"', sep='')
            print('   assignments: ')
            for assignment in sorted(students[p]):
                print('   - assignment: "', assignment, '"', sep='')
                print('     ', 'point', ': ', students[p][assignment]['point'], sep='')
                if not students[p][assignment]['group'] is None:
                    print('     ', 'group', ': "', students[p][assignment]['group'],'"', sep='')
                else:
                    print('     ', 'group', ': ', 'None', sep='')#
                if not students[p][assignment]['mail'] == "":
                    print('     ', 'mail', ': "', students[p][assignment]['mail'], '"', sep='')
                else:
                    print('     ', 'mail', ': ', 'None', sep='')
        print('...')
        #TODO return results for all students as JSON
        # (identifier, points_asignment01, points_asignment02, ..., points_sum)
