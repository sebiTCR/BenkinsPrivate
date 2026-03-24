from flask import Flask, url_for, render_template
from flask_cors import CORS
from web.blueprints.project import project_bp
from dotenv import load_dotenv
from web.blueprints.frontend import frontend_bp

app = Flask(__name__, template_folder='./web/templates', static_folder='./web/static')
CORS(app, resources={r"/project/*": {"origins": ["http://localhost:3000", "http://localhost:5000"]}})
# app.register_blueprint(frontend_bp)
load_dotenv()

app.register_blueprint(project_bp,  url_prefix="/project")
app.register_blueprint(frontend_bp, url_prefix="/app")

print("Startin FLASK")

@app.route('/')
def root():
    return render_template("index.html")