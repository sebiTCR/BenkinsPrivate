import os
from dataclasses import asdict

from flask import send_file
from pygments.lexers import data
from sqlalchemy import select

from persistance.models import Build, Project
from web.controllers.project_controller import get_project
from builder.builder import Builder
from persistance.database import db

def create_new_build(project_id: int, version: str):
    build: Build = None
    project = get_project(project_id)

    if project == None:
        return {"Status": False, "Message": "Project not found"}
    if get_build_by_version(version):
        return {"Status": False, "Message": "Build version already created!"}

    status, path = _compile_build(project)
    build = Build(project_id=project_id, version=version, file_path=path)
    db.session.add(build)
    db.session.commit()

    return {"Status": True, "Message": "Build queued!"}


def get_build(project_id: int, project_version: str):
    # q = select(Build).where(Build.version == project_version and Build.project_id == project_id)
    # data: Build = db.session.execute(q).first()
    # return data.file_path
    return "unimplemented"



def get_build_by_version(version: str):
    q = select(Build).where(Build.version == version)
    data = db.session.execute(q).first()

    if data is None:
        return None

    return data


def download_build(project_id: int, version: str):
    data: Build = get_build(project_id, version)
    if data == None:
        return None
    return send_file(data.file_path)


def delete_build(project_id, project_version):
    db.session.delete(Build).where(Build.version == project_version and Build.project_id == project_id)


#<editor-fold desc="Private Methods">
def _compile_build(project: Project) -> (bool, str):
    """
    Compiles a project
    :param project:
    :return: (Build status, The path to the build)
    """

    builder = Builder(f"{os.getenv("REPO_PATH")}/{project.id}/")
    #TODO: Actually compile the project
    return (True, f"{os.getenv("REPO_PATH")}/{project.id}/")


#/editor-fold>