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






"""MongoDB database models that represent our collections."""

#from datetime import datetime
#
#from api.app import db
#
#
#class User(db.Document):
#    """Model of an API User MongoDB document."""
#
#    meta = {'collection': 'api_users'}
#
#    created_at = db.DateTimeField(required=True)
#    updated_at = db.DateTimeField(default=datetime.utcnow)
#    username = db.StringField(max_length=50, required=True, unique=True) #email
#    password = db.StringField(max_length=128, required=True)
#    is_admin = db.BooleanField(required=True, default=False)
#    project_md5 = db.StringField(max_length=32)
#    project_version = db.StringField(max_length=10)
#    last_access_at = db.DateTimeField()
#
#    def _init_(self, username: str, password: str, created_at,
#                 md5=None, version=None, *args, **kwargs):
#
#        super(User, self)._init_(*args, **kwargs)
#
#        self.username = username
#        self.password = password
#        self.created_at = created_at
#
#        if md5:
#            self.project_md5 = md5
#        if version:
#            self.project_version = version
#
#
#class ReputationFeed(db.Document):
#    """Model of the Reputation Feed MongoDB document."""
#
#    meta = {'collection': 'reputation_feed'}
#
#    created_at = db.DateTimeField(required=True)
#    updated_at = db.DateTimeField(default=datetime.utcnow)
#    ip_address = db.StringField(max_length=45, required=True)
#    enabled = db.BooleanField(required=True, default=True)
#    risk_score = db.DecimalField(precision=3, required=True)
#    risk_type = db.IntField(min_value=0, required=True)
#    last_occurrence_date = db.DateTimeField(required=True)
#    blacklisted_at = db.DateTimeField(required=True)
#    owner = db.StringField(max_length=10, required=True)
#
#
#class TokenBlacklist(db.Document):
#    """Model for the collection of Blacklisted Tokens."""
#
#    meta = {'collection': 'token_blacklist'}
#
#    blacklisted_at = db.DateTimeField(required=True)
#    token_id = db.StringField(max_length=500, required=True, unique=True)
#
#    def _init_(self, token_id, *args, **kwargs):
#        super(TokenBlacklist, self)._init_(*args, **kwargs)
#        self.token_id = token_id
#        self.blacklisted_at = datetime.utcnow()
#
#    def _repr_(self):
#        return f'<Token ID: {self.token}>'
#
#    @staticmethod
#    def check_blacklist(token_id: str) -> bool:
#        """Check if the token has been blacklisted."""
#
#        token_document = TokenBlacklist.objects(token_id=str(token_id)).first()
#        return bool(token_document)