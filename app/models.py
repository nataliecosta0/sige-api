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
    __table_args__ = {'extend_existing': True}
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    @staticmethod
    def get_one_permission(user_id):
        return UserPermission.query.filter_by(user_id=user_id).first()


class Permission(db.Model):
    """ Permission Model """

    ___tablename___ = "permission"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

class InternRecord(db.Model):
    """ Intern Model """

    ___tablename___ = "intern_record"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    ra = db.Column(db.BigInteger, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    birth_date = db.Column(db.String(45), nullable=False)
    mother_name = db.Column(db.String(45), nullable=False)
    spouse_name = db.Column(db.String(45), nullable=True)
    course_name = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    residential_address = db.Column(db.String(100), nullable=False)
    residential_city = db.Column(db.String(100), nullable=False)
    residential_neighbourhood = db.Column(db.String(100), nullable=True)
    residential_cep = db.Column(db.String(100), nullable=True)
    residential_phone_number = db.Column(db.String(45), nullable=True)
    phone_number = db.Column(db.String(45), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, data):
        """
        Class constructor
        """
        self.ra = data.get('ra')
        self.name = data.get('name')
        self.birth_date = data.get('birth_date')
        self.mother_name = data.get('mother_name')
        self.spouse_name = data.get('spouse_name')
        self.course_name = data.get('course_name')
        self.period = data.get('period')
        self.email = data.get('email')
        self.residential_address = data.get('residential_address')
        self.residential_city = data.get('residential_city')
        self.residential_neighbourhood = data.get('residential_neighbourhood')
        self.residential_cep = data.get('residential_cep')
        self.residential_phone_number = data.get('residential_phone_number')
        self.phone_number = data.get('phone_number')
        self.user_id = data.get('user_id')
        #self.created_at = datetime.datetime.utcnow()
        #self.modified_at = datetime.datetime.utcnow()
        # 

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        self.name = data.get('name')
        self.birth_date = data.get('birth_date')
        self.mother_name = data.get('mother_name')
        self.spouse_name = data.get('spouse_name')
        self.course_name = data.get('course_name')
        self.period = data.get('period')
        self.email = data.get('email')
        self.residential_address = data.get('residential_address')
        self.residential_city = data.get('residential_city')
        self.residential_neighbourhood = data.get('residential_neighbourhood')
        self.residential_cep = data.get('residential_cep')
        self.residential_phone_number = data.get('residential_phone_number')
        self.phone_number = data.get('phone_number')
        self.user_id = data.get('user_id')
        
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_intern_by_ra(value):
        return InternRecord.query.filter_by(ra=value).first()

    @staticmethod
    def get_all_interns():
        return InternRecord.query.all()

    @staticmethod
    def get_one_intern(id):
        return InternRecord.query.get(id)


class InternSchema(Schema):

    id = fields.Int(dump_only=True)
    ra = fields.Int(required=True)
    name = fields.Str(required=True)
    birth_date = fields.Str(required=True)
    mother_name = fields.Str(required=True)
    spouse_name = fields.Str(required=False, allow_none=True)
    course_name = fields.Str(required=True)
    period = fields.Str(required=True)
    email = fields.Email(required=True)
    residential_address = fields.Str(required=True)
    residential_city = fields.Str(required=True)
    residential_neighbourhood = fields.Str(required=False, allow_none=True)
    residential_cep = fields.Str(required=False, allow_none=True)
    residential_phone_number = fields.Str(required=False, allow_none=True)
    phone_number = fields.Str(required=False, allow_none=True)
    user_id = fields.Int(required=True)
