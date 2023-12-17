from flask import render_template,redirect,request,flash,url_for,session
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  login_user, login_required, logout_user


from flask_bcrypt import Bcrypt
from models.Models import User,db
from flask_session import Session

bcrypt=Bcrypt()

def hash_password(password):
    pass 

def check_password():
    pass


@login_required
def home():
    return render_template("home.html")



def login_signup():
    return render_template('authentication.html')

def signup():
      if request.method=='POST':
        email=request.form.get("email")
        password=request.form.get("password")
        password_confirm=request.form.get("password_confirm")
        user = User.query.filter_by(email=email).first()

        if  not   user:
            if password ==password_confirm:
                password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                user=User(password=password_hash,email=email)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('routes.home'))

            else:
                flash("Password and Confirm Password doesnt match",'error') 
                return redirect(url_for('routes.login_signup'))    
        else:
            flash("User already exist.Please Proceed to Login",'error')
            return redirect(url_for('routes.login_signup'))


def login():
    email=request.form.get("email")
    passw =request.form.get("password")
    user=User.query.filter_by(email=email).first()
    
  

    if user: 
      
        if  bcrypt.check_password_hash(user.password, passw ):
             print("Logged in")
             login_user(user)           
             print("Logged in")
             return redirect(url_for('routes.home'))
        else:
             print("didnt hash")
             flash("Invalid Password",'error')
             return redirect(url_for('routes.login_signup'))
    else:
        flash("User doesnt exist",'error')
        return redirect(url_for('routes.login_signup'))
    
    


def logout():
    # logout_user()
    session.pop('email',None)
    logout_user()
    return redirect(url_for('routes.login_signup'))


#nice




@login_required
def dashboard():
    return  render_template("dashboard.html")


