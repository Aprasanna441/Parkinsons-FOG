from flask import Flask,render_template
from flask_migrate import Migrate
from  routes.UserRoutes import router
from models.Models import db,User
from flask_login import LoginManager,login_required





def create_app():
    app = Flask(__name__,template_folder='templates')  # flask app object
   
    app.config.from_object('config')  # Configuring from Python Files
    db.init_app(app)
   
    app.register_blueprint(router, url_prefix='/account')

    login_manager = LoginManager()
    login_manager.login_view = 'routes.login_signup' 
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
     return User.query.get(user_id)
    
    migrate = Migrate(app, db)
    
    return app

app = create_app()

@app.route('/')
@login_required
def mainpage():
   return render_template("home.html")
# migrate = Migrate(app, db)  # Initializing the migration




if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)