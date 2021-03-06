from .baseapp import NbGrader
from .studentapi import *
import os
import subprocess
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

            ´nbgrader studentmail assignment01´

        to mail all students, who submitted an assignment of assignment01, a mail
        with their results.
        For example mail to ´studnet@mail.upb.de´:

            Hallo,

            im Anhang befindet sich eine HTML Datei mit Ihrem Ergebnis der Heimübung %s.
            Sie haben 10.0 Punkte erreicht.

            Bitte anworten Sie nicht auf diese Mail, sie ist automatisch generiert.
            Bei Rückfragen wenden Sie sich bitte an Ihren Tutor.

        To test it use

            ´nbgrader studentmail assignment01 test´
        """

    def _classes_default(self):
        classes = super(StudentMailApp, self)._classes_default()
        classes.append(StudentMailApp)
        return classes

    def start(self):
        super(StudentMailApp, self).start()
        if (len(self.extra_args) == 2 and self.extra_args[1] != "test") or len(self.extra_args) not in {1, 2}:
            self.fail("Assignment id not provided. Usage: nbgrader studentmail assinment_id")

        if self.extra_args[0] not in get_assignment_list():
            self.fail("Assingment id does not exist")

        test = len(self.extra_args) == 2

        points = get_student_list_point()
        mail = get_student_list_mail()
        assignment_name = self.extra_args[0]

        for p in points:
            d = dict()
            d["assignment"] = assignment_name
            d["mail"] = mail[p][assignment_name]
            d["points"] = points[p][assignment_name]
            d["matrikelnr"] = p
            self.send_mail_to(d, test)

    def send_mail_to(self, d, test=False):
        d["body"] = """Hallo,

im Anhang befindet sich eine HTML Datei mit Ihrem Ergebnis der Heimübung %s.
Sie haben %.1f Punkte erreicht.

Ihre Matrikelnr: %s

Bitte anworten Sie nicht auf diese Mail, sie ist automatisch generiert.
Bei Rückfragen oder falscher Matrikelnummer wenden Sie sich bitte an Ihren Tutor.""" % (
            d["assignment"], d["points"], d["matrikelnr"])
        d["head"] = "Ergebnis %s, GP1" % (d["assignment"])
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
            self.log.info("%s MtNr:%s Group:%s Mail: %s Point:%.1f" % ("[not send]" if test else "[send]", d["matrikelnr"], d["group"], d["mail"], d["points"]))
            if test:
                return
            d["command"] = 'echo "%s" | mutt -s "%s" -a %s -- %s' %(d["body"], d["head"], d["html"], d["mail"])
            command = subprocess.Popen(d["command"], shell=True)
            command.communicate()
            #print(d["command"])