from datetime import datetime

from flask import current_app, request

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager
from . import db



class User(UserMixin, db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime(), default= datetime.utcnow)

    is_admin = db.Column(db.Boolean, default=False)
    
    assigned = db.relationship('Inventory', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User,self).__init__(**kwargs)
        # Super admins are able to assign mini_admins
        if not self.is_admin:
            if self.email == current_app.config['INVENTORY_ADMIN']:
                self.is_admin = True

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")   

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)          
        

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False

        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    @property
    def assets(self):
        return Assign.query.filter_by(requested_by=self)

    @property
    def assigned(self):
        return Inventory.query.filter_by(assigned_to=self)


    def __repr__(self):
        return '<User %r>' % self.name
# log in, tokens  generation end here

class Asset(db.Model):
    __tablename__ ='assets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    inventory = db.relationship('Inventory', backref='asset', lazy='dynamic')

    def __repr__(self):
        return '<Asset %s>' % self.name


class Inventory(db.Model):
    __tablename__ = 'inventories'

    id = db.Column(db.Integer, primary_key=True)

    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id])

    serial_code  = db.Column(db.String(255), nullable=False)
    serial_no    = db.Column(db.Integer, nullable=False)
    asset_name  = db.Column(db.String(255), nullable=False)
    description  = db.Column(db.String(255), nullable=False)
    date_bought  = db.Column(db.DateTime(), nullable=True)
    confirmed    = db.Column(db.Boolean, default=False)
    assigned     = db.Column(db.Boolean,default=False)
    revolved     = db.Column(db.Boolean,default=False)
    date_assigned = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    date_returned = db.Column(db.DateTime(), nullable=True, default=datetime.utcnow)

    def __init__(self,*args,**kwargs):
        super(Inventory,self).__init__(*args,**kwargs)

    def __repr__(self):
        return "<Assign {!r:.15}{} Assigned On: {:%a %b %d %H:%M:%S %Y} >".format(
            self.serial_code,
            "...'" if len(self.description) > 15 else '',
            self.date_assigned
        )    
class Report_lost(db.Model):
    __tablename__ = 'lost'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    serial_code = db.Column(db.String(255), nullable=False)
    asset_name  = db.Column(db.String(255), nullable=False)
    lost        = db.Column(db.Boolean,default=False)
   
    def __init__(self,*args,**kwargs):
        super(Report_lost,self).__init__(*args,**kwargs)

    def __repr__(self):
        return '<Report_lost %s>' % self.lost

    