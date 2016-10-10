from .baseapp import NbGrader
from .studentapi import *
aliases = {}
flags = {}


class StudentMailApp(NbGrader):

    name = u'nbgrader-studentmail'
    description = u'Send mails with results to given mail addresses from students'

    aliases = aliases
    flags = flags

    examples = """
        Sends mails to students to give them results to an assignment

        This command is running from the top-level folder of the course.
        This command must run after ´nbgrader studentgrade assignment01´

        For example

            nbgrader studentmail assignment01´

        to mail all students, who submitted an assignment of assignment01, a mail
        with their results.
        For example mail to ´studnet@mail.upb.de´: ´Matrikel Nr: 1234567, Punkte in hb2: 1.500000´
        """

    def _classes_default(self):
        classes = super(StudentMailApp, self)._classes_default()
        classes.append(StudentMailApp)
        return classes

    def start(self):
        super(StudentMailApp, self).start()
        if len(self.extra_args) != 1:
            self.fail("Assignment id not provided. Usage: nbgrader studentmail assinment_id")

        if self.extra_args[0] not in get_assignment_list():
            self.fail("Assingment id does not exist")

        points = get_student_list_point()
        mail = get_student_list_mail()

        for p in points:
            self.send_mail_to(mail[p][self.extra_args[0]], "Matrikel Nr: %s, Punkte in %s: %f" % (
                p, self.extra_args[0], points[p][self.extra_args[0]]))

    def send_mail_to(self, adress, message):
        #TODO send mail
        print("Send mail", adress, message)
