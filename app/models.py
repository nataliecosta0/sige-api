from app import db
from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
    """ User model"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    #status_id = db.Column(db.Integer, db.ForeignKey('user_status'))


class UserStatus(db.Model):
    """ User Status Model """

    ___tablename___ = "user_status"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False)


#class UserPermission(db.Model):
#    """ User Permission Model """
#
#    ___tablename___ = "user_permission"
#    permission_id = db.Column(db.Integer, db.ForeignKey('permission'))
#    user_id = db.Column(db.Integer, db.ForeignKey('user'))
#
#
#class Permission(db.Model):
#    """ Permission Model """
#
#    ___tablename___ = "permission"
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(10), nullable=False)
