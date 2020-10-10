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
            else:
                setattr(self, key, item)
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

    @staticmethod
    def get_status_user(status):
        return User.query.filter_by(status_id=status)

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


class PasswordRecovery(db.Model):
    """ User Status Model """
    __tablename__ = "password_recovery"
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, db.ForeignKey('user_status.id'), primary_key=True)
    code_id = db.Column(db.Integer, nullable=False)

    def __init__(self, data):
        """
        Class constructor
        """
        self.code_id = data.get('code_id')
        self.user_id = data.get('user_id')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_one_password_recovery(user_id):
        return PasswordRecovery.query.filter_by(user_id=user_id).first()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()


class UserPermission(db.Model):
    """ User Permission Model """

    ___tablename___ = "user_permission"
    __table_args__ = {'extend_existing': True}
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def __init__(self, data):
        """
        Class constructor
        """
        self.permission_id = data.get('permission_id')
        self.user_id = data.get('user_id')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_one_permission(user_id):
        return UserPermission.query.filter_by(user_id=user_id).first()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()


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

class Company(db.Model):
    """ Company Model """

    ___tablename___ = "company"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.BigInteger, nullable=False)
    company_name = db.Column(db.String(45), nullable=False)
    opening_date = db.Column(db.String(45), nullable=False)
    contact_email = db.Column(db.String(45), nullable=False)
    zip_code = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(45), nullable=False)
    contact_phone = db.Column(db.String(45), nullable=False)
    contact_person = db.Column(db.String(45), nullable=True)
    associated_since = db.Column(db.String(100), nullable=False)
    associated_until = db.Column(db.String(100), nullable=True)
    
    def __init__(self, data):
        """
        Class constructor
        """
        self.cnpj = data.get('cnpj')
        self.company_name = data.get('company_name')
        self.opening_date = data.get('opening_date')
        self.contact_email = data.get('contact_email')
        self.zip_code = data.get('zip_code')
        self.address = data.get('address')
        self.contact_phone = data.get('contact_phone')
        self.contact_person = data.get('contact_person')
        self.associated_since = data.get('associated_since')
        self.associated_until = data.get('associated_until')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_one_company(value):
        return Company.query.filter_by(company_name=value).first()

    @staticmethod
    def get_all_company():
        return Company.query.all()

class CompanySchema(Schema):

    id = fields.Int(dump_only=True)
    cnpj = fields.Int(required=True)
    company_name = fields.Str(required=True)
    opening_date = fields.Str(required=True)
    contact_email = fields.Str(required=True)
    zip_code = fields.Str(required=True)
    address = fields.Email(required=True)
    contact_phone = fields.Str(required=True)
    contact_person = fields.Str(required=False, allow_none=True)
    associated_since = fields.Str(required=True)
    associated_until = fields.Str(required=False, allow_none=True)

class Contracts(db.Model):
    """ Company Model """

    ___tablename___ = "contracts"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id')
    intern_ra = db.Column(db.Integer, db.ForeignKey('intern_record.ra')
    has_become_effective = db.Column(db.Integer, nullable=True)
    has_switched_companies = db.Column(db.Integer, nullable=True)

    def __init__(self, data):
        """
        Class constructor
        """
        self.company_id = data.get('company_id')
        self.intern_ra = data.get('intern_ra')
        self.has_become_effective = data.get('has_become_effective')
        self.has_switched_companies = data.get('has_switched_companies')
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_one_contract(value):
        return Company.query.filter_by(id=value).first()

    @staticmethod
    def get_all_contracts():
        return Company.query.all()

class ContractSchema(Schema):

    id = fields.Int(dump_only=True)
    company_id = fields.Int(required=True)
    intern_ra = fields.Int(required=True)
    has_become_effective = fields.Str(required=False, allow_none=True)
    has_switched_companies = fields.Str(required=False, allow_none=True)

class SubContracts(db.Model):
    """ Company Model """

    ___tablename___ = "sub_contracts"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    internship_contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id')
    start_date = db.Column(db.String(45), nullable=False)
    ending_date = db.Column(db.String(45), nullable=False)

    def __init__(self, data):
        """
        Class constructor
        """
        self.internship_contract_id = data.get('internship_contract_id')
        self.start_date = data.get('start_date')
        self.ending_date = data.get('ending_date')
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    #@staticmethod
    #def get_one_contract(value):
    #    return Company.query.filter_by(id=value).first()

    #@staticmethod
    #def get_all_contracts():
    #    return Company.query.all()

class ContractSchema(Schema):

    id = fields.Int(dump_only=True)
    internship_contract_id = fields.Int(required=True)
    start_date = fields.Int(required=True)
    ending_date = fields.Str(required=True)