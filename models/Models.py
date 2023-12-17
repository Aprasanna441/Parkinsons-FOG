from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin,db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    joined_on=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    is_admin=db.Column(db.Boolean,default=False)
    is_active=db.Column(db.Boolean,default=True)

    password = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return self.email
    
 
        


    


    
    

