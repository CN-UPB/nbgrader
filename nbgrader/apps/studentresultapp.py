from .baseapp import NbGrader
from .studentapi import *
import yaml
import sys

        
aliases = {}
flags = {}


#TODO Bitte ausprobieren und eventuell aendern:
# Ich bin mir nicht sicher, worauf genau die in der Datenbank Tabellen 'Groupmember' gespeicherte
# submitted_notebook_id verweist. moeglicherweise verwendet studentresult fuer die Berechnung der Punkte lediglich
# das eine Notebook, auf das verweisen wird, und nicht alle Notebooks, die fuer das Assignment abgegeben wurden. In
# dem Fall wird das das Notebook 'matrikelnummer.ipynb' sein und es muss noch geaedert werden, dass alle Notebooks
# des Assignments fuer die Berechnung der Punkte genutzt werden.





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

        students = get_student_list_summery()
        if len(self.extra_args) > 0:
            tmp_students = dict()
            for arg in self.extra_args:
                if arg in students:
                    tmp_students[arg] = students[arg]
            students = tmp_students

        sys.stderr.write("Dumping {} students\n".format(len(students)))
        
        # Old version, trying to create the yaml output manually
        # print('---')
        # print('submit_details:')
        # for p in sorted(students):
        #     print(' - matrikelnr: "', p, '"', sep='')
        #     print('   assignments: ')
        #     for assignment in sorted(students[p]):
        #         print('   - assignment: "', assignment, '"', sep='')
        #         print('     ', 'point', ': ', students[p][assignment]['point'], sep='')
        #         if not students[p][assignment]['group'] is None:
        #             print('     ', 'group', ': "', students[p][assignment]['group'],'"', sep='')
        #         else:
        #             print('     ', 'group', ': ', 'None', sep='')#
        #         if not students[p][assignment]['mail'] == "":
        #             print('     ', 'mail', ': "', students[p][assignment]['mail'], '"', sep='')
        #         else:
        #             print('     ', 'mail', ': ', 'None', sep='')
        # print('...')

        # new version: produce yaml via the module:
        print(yaml.dump(students, default_flow_style=False))
        
        #TODO return results for all students as JSON
        # (identifier, points_asignment01, points_asignment02, ..., points_sum)
