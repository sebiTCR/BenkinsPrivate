import os
from flask import Flask, url_for, render_template
from flask_cors import CORS
from web.blueprints.project import project_bp
from dotenv import load_dotenv
from web.blueprints.frontend import frontend_bp
from web.blueprints.build import build_bp
from web.controllers import project_controller

app = Flask(__name__, template_folder='./web/templates', static_folder='./web/static')
CORS(app, resources={r"/project/*": {"origins": ["http://localhost:3000", "http://localhost:5173"]}})
# app.register_blueprint(frontend_bp)
load_dotenv()

app.register_blueprint(project_bp,  url_prefix="/project")
app.register_blueprint(build_bp, url_prefix="/build")

app.register_blueprint(frontend_bp, url_prefix="/app")

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    project_controller.initialize()

@app.route('/')
def root():
    return render_template("index.html")