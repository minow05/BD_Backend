from flask import Flask
from models import db

from routes.employees import employees_bp
from routes.sections import sections_bp
from routes.teams import teams_bp
from routes.tasks import tasks_bp

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(employees_bp, url_prefix="/api/employees")
    app.register_blueprint(sections_bp, url_prefix="/api/sections")
    app.register_blueprint(teams_bp, url_prefix="/api/teams")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")

    @app.route("/")
    def index():
        return {"status": "API is running"}

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

