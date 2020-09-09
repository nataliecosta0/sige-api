from app import db, bcrypt
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema


class User(db.Model):
    """ User model"""

    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('user_status.id'))
    #created_at = db.Column(db.DateTime)
    #modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.status_id = data.get('status_id')
        #self.created_at = datetime.datetime.utcnow()
        #self.modified_at = datetime.datetime.utcnow()  

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(item)
            setattr(self, key, self.password)
       #self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_one_user(id):
        return User.query.get(id)
  
    @staticmethod
    def get_user_by_email(value):
        return User.query.filter_by(email=value).first()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)
  
    def __repr(self):
        return '<id {}>'.format(self.id)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    status_id = fields.Int(required=True)
    
    
class UserStatus(db.Model):
    """ User Status Model """
    __tablename__ = "user_status"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False)


class UserPermission(db.Model):
    """ User Permission Model """

    ___tablename___ = "user_permission"
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    @staticmethod
    def get_one_permission(user_id):
        return UserPermission.query.filter_by(user_id=user_id).first()


class Permission(db.Model):
    """ Permission Model """

    ___tablename___ = "permission"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
