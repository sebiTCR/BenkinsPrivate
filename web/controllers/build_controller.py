from flask import send_file
from pygments.lexers import data
from sqlalchemy import select

from persistance.models import Build, Project
from persistance.database import db

def create_new_build(project: Project, version: str, path: str):
    build: Build = None

    if get_build_by_version(version):
        return {"Status": False, "Message": "Build version already created!"}

    build = Build(project_id=project.id, version=version, file_path=path)
    db.session.add(build)
    db.session.commit()

    return {"Status": True, "Message": "Build queued!"}


def get_build(project_id: int, project_version: str):
    # q = select(Build).where(Build.version == project_version and Build.project_id == project_id)
    # data: Build = db.session.execute(q).first()
    # return data.file_path
    return "unimplemented"


def download_build(project_id: int, project_version: str):
    print(project_id, project_version)
    q = select(Build).where(Build.project_id == project_id)
    data: Build = db.session.execute(q).first()
    if data is None:
        return "No build found!"
    return send_file(data[0].file_path)


def get_build_by_version(version: str):
    q = select(Build).where(Build.version == version)
    data = db.session.execute(q).first()

    if data is None:
        return None

    return data


# def download_build(project_id: int, version: str):
#     data: Build = get_build(project_id, version)
#     if data == None:
#         return None
#     return send_file(data.file_path)


def delete_build(project_id, project_version):
    db.session.delete(Build).where(Build.version == project_version and Build.project_id == project_id)
