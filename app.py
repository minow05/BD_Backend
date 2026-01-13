from flask import Flask, render_template, url_for, redirect
from models import db
from routes.employees import employees_bp
from routes.sections import sections_bp
from routes.teams import teams_bp
from routes.tasks import tasks_bp
import generate_data

    
def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    
    generate_data.create_sample_data(app)

    app.register_blueprint(employees_bp, url_prefix="/api/employees")
    app.register_blueprint(sections_bp, url_prefix="/api/sections")
    app.register_blueprint(teams_bp, url_prefix="/api/teams")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    

    @app.route('/')
    def index():
        return render_template("index.html")

    with app.app_context():
        db.create_all()

    @app.route('/check-user/<role>/<id>')
    def check(role,id):
        if role == "szefstudia":
            return redirect(url_for('szef', myid = id))
        elif role == "kierowniksekcji":
            return redirect(url_for('sekcja',myid = id))
        elif role == "kierownikzespolu":
            return redirect(url_for('zespol',myid = id))
        else:
            return redirect(url_for('pracownik',myid = id))
        
    @app.route('/szef/<myid>')
    def szef(myid):
        return render_template("szefstudia.html", id = myid)
    
    @app.route('/sekcja/<myid>')
    def sekcja(myid):
        return render_template("kierowniksekcji.html", id = myid)

    @app.route('/zespol/<myid>')
    def zespol(myid):
        return render_template("kierownikzespolu.html", id = myid)

    @app.route('/pracownik/<myid>')
    def pracownik(myid):
        return render_template("pracownik.html", id = myid)
    
    @app.route('/your-data/<myid>')
    def your_data(myid):
        return render_template("personaldata.html", id = myid)
    
    @app.route('/your-tasks/<myid>')
    def your_tasks(myid):
        return render_template("personaltasks.html", id = myid)
    
    
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

