from flask import Blueprint, request
from web.controllers.build_controller import get_build, create_new_build, delete_build

build_bp = Blueprint('build', __name__)


@build_bp.route('/<project_id>', methods=['PUT', 'POST', 'DELETE'])
def index(project_id: int):
    project_version = request.get_json()['version']

    if project_id is None or project_version is None:
        return {"status": False, "Message": "project_id and version are required!"}

    match request.method:
        case "POST":
            return get_build(project_id, project_version)
        case "PUT":
            return create_new_build(project_id, project_version)
        case "DELETE":
            return delete_build(project_id, project_version)


@build_bp.route('/<pid>/<version>')
def download(pid: int, version: str):
    return get_build(pid, version)