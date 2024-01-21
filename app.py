from flask import Flask,render_template,redirect,jsonify
from flask_migrate import Migrate
from  routes.UserRoutes import router
from models.Models import db,User
from flask_login import LoginManager,login_required

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
import joblib
import pandas as pd



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


class UploadForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['txt', 'csv', 'pdf'], 'Allowed file types are txt, csv, pdf, png, jpg, jpeg, gif')
    ])



@app.route('/',methods=['GET','POST'])
@login_required
def mainpage():
    form = UploadForm()

    if form.validate_on_submit():
        file = form.file.data
        upload_file(file)
        
        
        
        
        # Do something with the uploaded file (e.g., save it to disk, process it)

        

    return render_template('home.html', form=form)



def upload_file(file):
    model = joblib.load('naive_bayes.pkl')
    data=pd.read_csv(file)
    prediction = model.predict(data[:200])
    print(prediction)
    return jsonify({'prediction': prediction.tolist()})




    return render_template("result.html")
    
    






if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)