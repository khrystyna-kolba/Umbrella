# AS simeple as possbile flask google oAuth 2.0
from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
# decorator for routes that should be accessible only by logged in users
#from auth_decorator import login_required

# dotenv setup
from dotenv import load_dotenv


# App config
app = Flask(__name__)
# Session config
app.secret_key = "rjgkrsenlekrjghn4onke"
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config["SESSION_PERMANENT"] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    prompt = "consent"
)

from routes import *
if __name__ == '__main__':
    from fastapi.templating import Jinja2Templates

    templatess = Jinja2Templates(directory="templates")


    def clever_function():
        return u'HELLO'


    templatess.env.globals.update(clever_function=clever_function)
    load_dotenv()
    app.run(debug=True)