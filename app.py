from flask import Flask, render_template, url_for, redirect, request, session
from authlib.integrations.flask_client import OAuth
from flask_session import Session
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
oauth = OAuth(app)

app.config['SECRET_KEY'] = "FKJKDKJHGb23243555jknnn3hb4hj5bdk3bdhjsbj4bdsbchjsbjh2bj"
app.config['GOOGLE_CLIENT_ID'] = "187307842474-0d8fq5ngu1lskgblk5r8riodrnemu3og.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"

google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'email profile'},
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs"
)



# Default route
@app.route('/')
def index():
  return render_template('index.html')


# Google login route
@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    session["name"] = resp["name"]
    print(f"\n{resp}\n")
    return redirect('/protected')

# Google authorize route
@app.route('/protected')
def protected():
    if session.get("name"):
        print(session.get("name"))
    return "you can be here only if you logged in"

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

if __name__ == '__main__':
  app.run(debug=True)