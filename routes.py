from main import app, oauth, db
from models import *
import requests
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request, session
from auth_decorator import login_required
from datetime import datetime
#from models import db
#from wtforms.validators import DataRequired, Length, ValidationError, InputRequired
import forms
import re
import googlemaps
import os
from timezonefinder import TimezoneFinder
import pytz





def get_city_data(city):
    url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={key}"
    obj = TimezoneFinder()
    gmaps = googlemaps.Client(key=os.getenv('api_google'))
    r = gmaps.geocode(city)
    if len(r) > 0:
        address = r[0]["formatted_address"]
        lat = r[0]["geometry"]["location"]["lat"]
        lng = r[0]["geometry"]["location"]["lng"]
        x = re.findall(".*(?=,\s\d*)", address)
        if len(x) > 0:
            address = x[0]

        timezone = obj.timezone_at(lng=lng, lat=lat)
        timezone = pytz.timezone(timezone)
        print(timezone)
        time = datetime.now(timezone)
        time_h = time.hour
        time_m = time.minute
        time = "{h}:{m}".format(h=time_h, m=time_m)
        if time_m < 10:
            time = "{h}:0{m}".format(h=time_h, m=time_m)
        weather = requests.get(url.format(lat=lat, lon=lng, key=os.getenv('api_openweathermap'))).json()
        print(weather)
        description = weather["weather"][0]["description"]
        icon = weather["weather"][0]["icon"]
        temp = weather["main"]["temp"]
        print(temp)
        wind = weather["wind"]["speed"]
        humidity = weather["main"]["humidity"]
        pressure = weather["main"]["pressure"]
    else:
        pressure = 0
        address = "unknown"
        temp = 0
        description = "nothing to say",
        wind = 0
        humidity = 0
        time = "00:00"
        icon = "10d"
    return address, time, temp, description, wind, humidity,pressure, icon



# Default route
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/add_city', methods=["GET","POST"])
@login_required
def add_city():
    cities = City.query.filter_by(username=dict(session)['profile']['email']).order_by(City.id.desc())
    #cities= reversed(cities)
    weathers={}
    for city in cities:
        weathers[city.id] = get_city_data(city.cityname)
    form = forms.AddCityForm()
    if form.validate_on_submit():
        t = City(cityname=form.city.data, username = dict(session)['profile']['email'])
        db.session.add(t)
        db.session.commit()
        return redirect(url_for("add_city"))
    return render_template("add_city.html", form = form, cities=cities, weathers=weathers)

@app.route('/delete_city/<int:city_id>', methods=["GET","POST"])
@login_required
def delete_city(city_id):
    city = City.query.get(city_id)
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for('add_city'))


@app.route('/protected', methods=["GET","POST"])
@login_required
def protected():
    email = dict(session)['profile']['email']
    print("hello {}".format(email))
    form = forms.EnterCityForm()
    url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={key}"
    if form.validate_on_submit():
        obj = TimezoneFinder()
        city = form.city.data
        gmaps = googlemaps.Client(key=os.getenv('api_google'))
        r = gmaps.geocode(city)
        address = ""
        weather = {}
        if len(r) > 0:
            address = r[0]["formatted_address"]
            lat = r[0]["geometry"]["location"]["lat"]
            lng = r[0]["geometry"]["location"]["lng"]
            x = re.findall(".*(?=,\s\d*)", address)
            if len(x) > 0:
                address = x[0]

            timezone = obj.timezone_at(lng=lng, lat=lat)
            timezone = pytz.timezone(timezone)
            print(timezone)
            time = datetime.now(timezone)
            time_h = time.hour
            time_m = time.minute
            time = "{h}:{m}".format(h=time_h, m=time_m)
            if time_m < 10:
                time = "{h}:0{m}".format(h=time_h, m=time_m)
            weather = requests.get(url.format(lat=lat, lon=lng, key=os.getenv('api_openweathermap'))).json()
            print(weather)
            description = weather["weather"][0]["description"]
            icon = weather["weather"][0]["icon"]
            temp = weather["main"]["temp"]
            print(temp)
            wind = weather["wind"]["speed"]
            humidity = weather["main"]["humidity"]
            pressure = weather["main"]["pressure"]
        else:
            flash("error while searching the city, try again")
            return render_template("profile_home.html", pressure=0, form=form, name="unknown", temp=0, descr="nothing to say",
                                   wind=0, hum=0, time="00:00", icon="10d")
        print(r)

        # print(name_n, lat_n, lng_n, country_n)
        # print(name, lat, lon, country, state)
        return render_template('profile_home.html', icon=icon, pressure=pressure, form=form, name=address, temp=temp,
                               descr=description, wind=wind, hum=humidity, time=time)
    return render_template('profile_home.html', form=form, icon="10d", name="Your city")


@app.route('/login')
def google_login():
    u = dict(session).get('profile', None)
    if u:
        session["profile"] = None
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/login/google/authorize')
def authorize():
    u = dict(session).get('profile', None)
    if u:
        session["profile"] = None
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/protected')


@app.route('/logout')
def logout():
    #for key in list(session.keys()):
    #    session.pop(key)
    #    print(dict(session)['profile']['email')
    session["profile"]=None
    return redirect('/')




