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
        assignment_name = self.extra_args[0]

        for p in points:
            d = dict()
            d["assignment"] = assignment_name
            d["mail"] = mail[p][assignment_name]
            d["points"] = round(points[p][assignment_name], 2)
            d["matrikelnr"] = p
            self.send_mail_to(d)

    def send_mail_to(self, d):
        d["body"] = "Matrikel Nr: %s, Punkte in %s: %f" % (
            d["matrikelnr"], d["assignment"], d["points"])
        d["head"] = "Ergebniss %s" % (d["assignment"])
        d["group"] = get_student_id(d["matrikelnr"], d["assignment"])
        #TODO send mail
        # html_file =
        if adress is not "":
            print("Send mail", d["mail"], d["group"], d["head"],  d["bedy"])
        else:
            print("None", groupmember_id)