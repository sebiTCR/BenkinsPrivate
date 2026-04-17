from dataclasses import asdict

from flask import Blueprint, request, jsonify
from persistance.database import db
from persistance.models import Project
from web.controllers.project_controller import (get_projects, create_project, get_project, update_project_param, delete_project, set_project_build_status)

project_bp = Blueprint('project_bp', __name__)

@project_bp.route('/all', methods=["GET"])
def list_projects():
    return get_projects()

@project_bp.route('/<id>', methods=["GET", "POST", "DELETE"])
def project_methods(id: int):
    match request.method:
        case 'GET':
            return asdict(get_project(id))

        case 'POST':
            return update_project_param(Project.name, id, "")

        case "DELETE":
            return delete_project(id)

        case _:
            return "unimplemented method"


@project_bp.route('/<id>/status', methods=["GET", "PATCH"])
def update_status(id):
    match request.method:
        case 'PATCH':
            code = request.get_json()['status']
            return set_project_build_status(id, code)

@project_bp.route("/", methods=["POST"])
def create_project_r():
    data: dict = request.get_json()
    return create_project(data)