from os import unlink
from subprocess import run

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from datamodel.eldamobase import EldamoBase
from parse_xml import parse_xml
from to_latex import write_latex


def create_db():
    unlink('new_eldamo.db')
    engine = create_engine('sqlite:///new_eldamo.db', echo=True)

    EldamoBase.metadata.create_all(engine)

    with Session(engine) as session:
        parse_xml('eldamo-data.xml', session)
        session.commit()


def make_latex():
    engine = create_engine('sqlite:///new_eldamo.db', echo=False)
    with Session(engine) as session:
        write_latex(session)

    run('cd latex && mytexmk main.tex clean', shell=True)


def in_memory():
    engine = create_engine('sqlite:///:memory:', echo=True)
    with Session(engine) as session:
        EldamoBase.metadata.create_all(engine)
        parse_xml('eldamo-data.xml', session)
        write_latex(session)
    run('cd latex && mytexmk main.tex clean', shell=True)


# create_db()
# make_latex()

in_memory()
