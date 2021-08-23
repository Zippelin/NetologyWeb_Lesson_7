
from datetime import datetime
import hashlib

from gino import Gino

SALT = 'fmksjoifn23j4jmls,fs'

db = Gino()


class BaseModelMixin:
    date_creation = db.Column(db.DateTime, default=datetime.now())


class User(db.Model, BaseModelMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_superuser = db.Column(db.Boolean, default=False)
    
    async def save(self):
        self.password = self.password + SALT
        self.password = hashlib.md5(self.password.encode()).hexdigest()
        await super(User, self).save()

    async def authenticate(self, password):
        password = password + SALT
        return self.password == hashlib.md5(password.encode()).hexdigest()

    async def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser
        }


class Advert(db.Model, BaseModelMixin):
    __tablename__ = 'advert'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), index=True, nullable=False)
    description = db.Column(db.String(), index=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    async def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'owner': self.owner,
        }


class Token(db.Model, BaseModelMixin):
    __tablename__ = 'token'
    user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    key = db.Column(db.String(), index=True, nullable=True)

    async def create(self, *args, **kwargs):
        user = await User.get(self.user)
        self.key = hashlib.md5(str(user.username + user.email).encode()).hexdigest()
        await super().create(*args, **kwargs)