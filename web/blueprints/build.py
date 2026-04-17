from flask import Blueprint, request
from web.controllers.build_controller import get_build, create_new_build, delete_build, download_build

build_bp = Blueprint('build', __name__)


@build_bp.route('/<project_id>/<version>', methods=['GET', 'DELETE'])
def index(project_id: int, version: str):
    # project_version = request.get_json()['version']

    if project_id is None or version is None:
        return {"status": False, "Message": "project_id and version are required!"}

    match request.method:
        case "GET":
            return download_build(project_id, version)
        case "DELETE":
            return delete_build(project_id, version)


@build_bp.route('/<pid>/<version>')
def download(pid: int, version: str):
    return get_build(pid, version)