from flask import Flask, render_template, url_for, redirect, session, jsonify, request
from models import db
from routes.employees import employees_bp
from routes.sections import sections_bp
from routes.teams import teams_bp
from routes.tasks import tasks_bp
from routes.team_memberships import team_memberships_bp
from routes.progress import progress_bp
import generate_data

    
def create_app():
    app = Flask(__name__)
    app.secret_key = 'tajny-klucz'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)

    
    generate_data.create_sample_data(app)

    app.register_blueprint(employees_bp, url_prefix="/api/employees")
    app.register_blueprint(sections_bp, url_prefix="/api/sections")
    app.register_blueprint(teams_bp, url_prefix="/api/teams")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(team_memberships_bp, url_prefix="/api/team_memberships")
    app.register_blueprint(progress_bp, url_prefix="/api/progress")

    #obsługa sesji
    @app.route('/api/session/set', methods=['POST'])
    def api_set_session():
        try:
            data = request.json

            for key, value in data.items():
                session[key] = value
            
            return jsonify({
                'status': 'success',
                'message': 'Dane zapisane w sesji',
                'saved_keys': list(data.keys()),
            })
            
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        
    @app.route('/api/session/clear', methods=['POST'])
    def api_clear_session():
        session.clear()
        return jsonify({
            'status': 'success',
            'message': 'Sesja wyczyszczona'
        })
    #strona początkowa
    @app.route('/')
    def index():
        return render_template("index.html")

    with app.app_context():
        db.create_all()

    #main pages
    @app.route('/chief')
    def chief():
        return render_template("chief/chief.html")
    
    @app.route('/section-manager')
    def section_manager():
        return render_template("section-manager/section-manager.html")

    @app.route('/team-manager')
    def team_manager():
        return render_template("team-manager/team-manager.html")

    @app.route('/employee')
    def employee():
        return render_template("employee/employee.html")
    

    #employee pages
    @app.route('/your-data')
    def your_data():
        return render_template("employee/personal-data.html")
    
    @app.route('/your-tasks')
    def your_tasks():
        return render_template("employee/personal-tasks.html")
    
    #team manager pages
    @app.route('/team-tasks')
    def team_tasks():
        return render_template("team-manager/team-tasks.html")
    
    @app.route('/team-employees')
    def team_employees():
        return render_template("team-manager/team-employees.html")
    
    @app.route('/team-employees/tasks')
    def team_employees_tasks():
        return render_template("team-manager/team-employees-tasks.html")

    #section manager pages
    @app.route('/section-tasks')
    def section_tasks():
        return render_template("section-manager/section-tasks.html")
    
    @app.route('/section-teams')
    def section_teams():
        return render_template("section-manager/section-teams.html")
    
    #chief pages
    @app.route('/all-employees')
    def allemployees():
        return render_template("chief/all-employees.html")
    
    @app.route('/sections')
    def sections():
        return render_template("chief/sections.html")
    
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

