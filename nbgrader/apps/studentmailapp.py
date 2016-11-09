from .baseapp import NbGrader
from .studentapi import *
import os
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
            d["points"] = points[p][assignment_name]
            d["matrikelnr"] = p
            self.send_mail_to(d)

    def send_mail_to(self, d):
        d["body"] = "Matrikel Nr: %s, Punkte in %s: %.1f" % (
            d["matrikelnr"], d["assignment"], d["points"])
        d["head"] = "Ergebniss %s" % (d["assignment"])
        d["group"] = get_student_id(d["matrikelnr"], d["assignment"])
        #TODO send mail
        d["html"] = "feedback/%s/%s/%s.html" % (d["group"], d["assignment"], d["assignment"])

        # Dies ist nur zu testzwecken vorhanden
        if d["assignment"] == "SHK_Test":
            d["html"] = "feedback/%s/%s/%s.html" % (d["group"], d["assignment"], "hueT")

        if d["mail"] is not "" and d["group"] is not None:
            if not os.path.exists(d["html"]):
                print("No HTML File in Group", d["group"])
                return
            print("Send mail", d["mail"], d["group"], d["html"], d["head"],  d["body"])
        else:
            print("None", d["matrikelnr"])