#This file has methods for studentgraderapp.py, studnentmailapp.py and studentresultapp.py

#TODO: integrate this to nbgrader/api.py ?

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
from ..api import Assignment, SubmittedAssignment, SubmittedNotebook, Grade


#: superclass for database representation classes
Base = declarative_base()

#: default database url. See init_database
db_url = 'sqlite:///gradebook.db'
session = None


def init_database(db_url=db_url, echo=False):
    global session
    """
    Initialise the database:
    Connect to database with given url
    creates new table 'groupmember' if not exists
    :param db_url: url of database. See sqlalchemie create_engine. default 'sqlite:///gradebook.db'
    :param debug_mode: see sqlalchemie creat_engine :param echo:. Default False
    :return: session for connected database (see sqlalchemy Session)
    """
    engine = create_engine(db_url, echo=echo)
    Session = sessionmaker(bind=engine)
    session = Session()

    #Add table 'groupmember' if not exist
    metadata = MetaData()
    groupemember = Table('groupmember', metadata,
                         Column('sub_notebook_id', String, primary_key=True),
                         Column('groupmember_id', String, primary_key=True),
                         Column('mail', String))
    metadata.create_all(engine)
    return session

init_database()


#TODO manage foreign keys with sqlalchemie


class Groupmember(Base):
    """
    Database representation of a group member for a submitted assignment
    """
    __tablename__ = 'groupmember'

    #: Unique id of :attr:`~nbgrader.api.SubmittedAssignment.id`
    sub_notebook_id = Column(String, primary_key=True)

    #: Unique identifier for a student (not for
    #: :attr:`~nbgrader.api.Student.id`, that is just an account
    #: to login). i.e.: Matrikel Number (german university)
    #: it is used to connect all submitted assignments from that
    #: student to that student. a groupmember id can just be connected
    #: to one submission each assignment
    groupmember_id = Column(String, primary_key=True)

    #: an email address for a result email for that assignment.
    #: can change for one student each assignment
    mail = Column(String)

    def __repr__(self):
        return "<Groupmember(identifier='%s', notebook=%s, mail='%s')>" \
               % (self.groupmember_id, self.sub_notebook_id, self.mail)


def get_assignment_id(assignment_name):
    """
    Returns the id of the assignment to the given name
    :param assignment_name: :attr: ´~nbgrader.api.Assignment.name´
    :return: :attr: ´~nbgrader.api.Assignment.id´
    """
    return session.query(Assignment.id).filter(Assignment.name == assignment_name).first()[0]


def get_assignment_name(assignment_id):
    """
    Returns the name of the assignment to the given id
    :param assignment_id: :attr: ´~nbgrader.api.Assignment.id´
    :return: :attr: ´~nbgrader.api.Assignment.name´
    """
    return session.query(Assignment.name).filter(Assignment.id == assignment_id).first()[0]


def get_assignment_id_from_sub_ass_id(submitted_assignment_id):
    """
    Returns the assignment id to a given submitted assignment id
    :param submitted_assignment_id: unique :attr: ´~nbgrader.api.SubmittedAssignment.id´
    :return: :attr: ´~nbgrader.api.SubmittedAssignment.assignment_id´ unique id of
        an assignment :attr: ´~nbgrader.api.Assignment.id´
    """
    return session.query(SubmittedAssignment.assignment_id).filter(
        SubmittedAssignment.id == submitted_assignment_id).first()[0]


def get_submitted_nb_id(assignment_id):
    """
    Returns the Notebook id for an given assignment id. Require exact one notebook
    for that assignment. otherwise returns the notebook id of one notebook of that assignment
    :param assignment_id: :attr: ´~nbgrader.api.SubmittedNotebook.assignment_id´ unique id
        of ´~nbgrader.api.Assignment´
    :return: :attr: ´~nbgrader.api.SubmittedNotebook.id´
    """
    return session.query(SubmittedNotebook.id).filter(
        SubmittedNotebook.assignment_id == assignment_id).first()[0]


def get_assignment_list():
    """
    Returns a list of all assignment names
    :return: List of all :attr: ´~nbgrader.api.Assignment.name´
    """
    return list(map(lambda x: x[0], session.query(Assignment.name).all()))


def get_points(sub_notebook_id):
    """
    Returns the sum of graded points in grade cells for the submitted notebook with given id.
    Manual graded points count higher then auto graded points
    :param sub_notebook_id: :attr: ´~nbgrader.api.Grade.notebook_id´ unique id of
        :attr: ´~nbgrader.api.SubmittedNotebook.id´
    :return:
    """
    grades = session.query(Grade).filter(Grade.notebook_id == sub_notebook_id)
    res = 0
    for g in grades:
        if g.auto_score is None:
            res += g.manual_score
        elif g.manual_score is None:
            res += g.auto_score
        elif g.auto_score is None and g.manual_score is None:
            pass
        else:
            res += min(g.auto_score, g.manual_score)
    return res


def get_student_list_point():
    """
    Returns a dict with all students an theit graded points in all their submitted notebooks.
    Return a dict with :attr: ´~nbgrader.apps.studentapi.Groupmember.groupmember_id´ as keys.
    Values are dicts with :attr: ´~nbgrader.api.Assignment.name´ as keys and values
    ´~nbgrader.apps.studentapi.get_points`with param :attr:
    ´~nbgrader.apps.studentapi.Groupmember.groupmember_id´ for the notebook of that assignment.
    :return: a dict. For example
        {'1234567': {'aufg1': 0, 'ps2': 0, 'ps_test': 0, 'ps1': 0, 'hb2': '1.5'},
        '7007607': {'aufg1': 0, 'ps2': 0, 'ps_test': 0, 'ps1': 0, 'hb2': '1.5'}}
    """
    res = dict()
    ass_list = get_assignment_list()
    for p in session.query(Groupmember).all():
        if p.groupmember_id not in res:
            res[p.groupmember_id] = dict(zip(ass_list, [0 for _ in ass_list]))
        res[p.groupmember_id][get_assignment_name(get_assignment_id_from_sub_ass_id(p.sub_notebook_id))] = \
            get_points(get_submitted_nb_id(p.sub_notebook_id))
    return res


def get_student_list_mail():
    """
    Return a dict with :attr: ´~nbgrader.apps.studentapi.Groupmember.groupmember_id´ as keys.
    Values are dicts with :attr: ´~nbgrader.api.Assignment.name´ as keys and values
    ´~nbgrader.apps.studentapi.get_points`with param :attr:
    ´~nbgrader.apps.studentapi.Groupmember.email´ for the notebook of that assignment.
    :return: a dict. For example:
        {'7007607': {'aufg1': '', 'ps2': '', 'ps1': '', 'ps_test': '', 'hb2': 'jharbig@mail.upb.de'},
        '1234567': {'aufg1': '', 'ps2': '', 'ps1': '', 'ps_test': '', 'hb2': 'studnet@mail.upb.de'}}
    """
    res = dict()
    ass_list = get_assignment_list()
    for p in session.query(Groupmember).all():
        if p.groupmember_id not in res:
            res[p.groupmember_id] = dict(zip(ass_list, ["" for _ in ass_list]))
        res[p.groupmember_id][get_assignment_name(get_assignment_id_from_sub_ass_id(p.sub_notebook_id))] = \
            p.mail
    return res