import os
from dataclasses import asdict
from sqlalchemy import select, delete, update

from builder.builder import Builder
from core.scheduler.tasks import CloneTask, SetupTask
from persistance.database import db
from persistance.models import Project, BuildStatus
from core import log, fs
from core.scheduler.scheduler import scheduler


def get_projects():
    data = []

    for entry in db.session.query(Project).all():
        data.append(asdict(entry))

    return data


def get_project(id):
    data: Project = db.session.get(Project, id)
    if data is None:
        return None

    return data


def get_project_by_name(name: str):
    q = select(Project).where(Project.name == name)
    data = db.session.execute(q).first()

    if data is None:
        return None

    return data


def project_exists(name: str):
    q = select(Project).where(Project.name == name)
    data = db.session.execute(q).first()

    if data is None:
        return False
    return True

# TODO: Move cloning into a new thread!
def create_project(data: dict):
    if  project_exists(data["name"]):
        return {"status": False, "message": "Project exists!"}

    repo_url = data["repo_url"]
    repo_type = data["type"]
    repo_name = fs.get_repo_name(repo_url)
    project_path = f"{os.getenv('REPO_PATH')}/{repo_name}"
    p = Project(name=data["name"], version='0', status=0, path=project_path, type=repo_type, repo=repo_url)

    if(not os.path.exists(project_path)):
        os.makedirs(project_path)

    scheduler.register_task(CloneTask(p))
    scheduler.register_task(SetupTask(p))
    p.version = fs.get_latest_tag(project_path).name

    db.session.add(p)
    db.session.commit()
    return {"status": True, "data": asdict(p)}


def  update_project_param(param, id, val):
    return "Unimplemented"


def set_project_build_status(id: int, status_code: int):
    """
    Updates the build status of a project
    :param id: Project ID
    :param status_code: Build Code (NONE=0, SUCCESS=1, BUILDING=2, FAILED=3)
    :return:
    """
    q = update(Project).where(Project.id == id).values(status=status_code)
    db.session.execute(q)
    db.session.commit()
    return f"updated Project {id}"


def delete_project(id: int):
    q = delete(Project).where(Project.id == id)
    db.session.execute(q)
    db.session.commit()
    return f"deleted {id}"