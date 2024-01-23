from flask import Flask,render_template,redirect,jsonify
from flask_migrate import Migrate
from  routes.UserRoutes import router
from models.Models import db,User
from flask_login import LoginManager,login_required

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SelectField
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
    mlmodel = SelectField('Select Model', choices=[('NaiveBayes', 'Naive Bayes'), ('DecisionTree', 'Decision Tree'), ('KNearest', 'KNearest'),('svm', 'svm')])




@app.route('/',methods=['GET','POST'])
@login_required
def mainpage():
    form = UploadForm()

    if form.validate_on_submit():
        
        file = form.file.data
        modelDict={
            "DecisionTree":"decisiontree.pkl",
            "KNearest":"final_naive_bayes.pkl",
            "NaiveBayes":"naive_bayes.pkl",
            "svm":"svm.pkl"
        }
        
        selected_model=modelDict[form.mlmodel.data]
        print(selected_model)


        image,prediction=upload_file(file,selected_model)
       
        return render_template('result.html',  image_path=image,prediction=prediction)
        

        


        

    return render_template('home.html', form=form)
import os
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
def upload_file(file,mlmodel):
    #prediction part
    model = joblib.load(mlmodel)
    data=pd.read_csv(file)
    prediction = model.predict(data[:1000])    
    classes=classes=["StartHesitation","Turn","Walk"]
    
    decoded_classes = []

    #decoding [0,0,1] type
    for i in prediction:
        class_index = np.argmax(i)
        decoded_class = classes[class_index]
        decoded_classes.append(decoded_class)
    print(decoded_classes)
    
 

    #plotting graph
    time = data['Time']
    acc_ap = data['AccV']
    acc_ml = data['AccML']
    acc_v = data['AccAP']
    plt.figure(figsize=(10, 6))

# Plotting AccAp
    fig, ax = plt.subplots()
    ax.plot(time, acc_ap, label='AccAP')
    ax.plot(time, acc_ml, label='AccML')
    ax.plot(time, acc_v, label='AccV')
 

    ax.set_xlabel('Time')
    ax.set_ylabel('Acceleration')
    ax.set_title('Accelerometer Data with Heartbeat-Like Pattern')
    ax.legend()


    # Display the plot
    # plt.show()
    buf = BytesIO() 
    fig.savefig(buf, format='png')
    buf.seek(0)

    image_path = os.path.join(app.root_path, 'static', 'accelerometer_graph.png')
    with open(image_path, 'wb') as f:
        f.write(buf.getvalue())


    return  image_path,decoded_classes
   
   
        
    
    




    
    
    






if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)