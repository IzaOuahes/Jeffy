from househunt import app, db, login_manager
import datetime
import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Auth:
    CLIENT_ID = ('778475302479-3s6vnhomec0tlpfvmo9s7tk4vgst6rp7.apps.googleusercontent.com')
    CLIENT_SECRET = 'hGOip-TVHJkT0yfKsBbrPz1h'
    REDIRECT_URI = 'http://jeffy-dot-zinc-bucksaw-245306.appspot.com/home'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
class Config:
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret" 
class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")
class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")
config = {
"dev": DevConfig,
"prod": ProdConfig,
"default": DevConfig
}

class GoogleUser(db.Model):
    __tablename__ = "google_users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session( Auth.CLIENT_ID, state=state, redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session( Auth.CLIENT_ID, redirect_uri=Auth.REDIRECT_URI, scope=Auth.SCOPE)
    return oauth