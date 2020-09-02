#!/usr/bin/env python3

import os
from flask import Flask, redirect, url_for, jsonify, request, render_template
from flask_dance.contrib.google import make_google_blueprint, google
from flask_cors import CORS
import json
import requests

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = Flask(
    __name__,
    static_url_path='',
    static_folder='display/static',
    template_folder='display/templates')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

google_bp = make_google_blueprint(
    client_id=app.config["GOOGLE_OAUTH_CLIENT_ID"],
    client_secret=app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
    scope=['profile', 'email'],
    offline=True,
    redirect_url='http://esdosmessaging.tk:9001/login/callback')
app.register_blueprint(google_bp, url_prefix="/login")

from models import User

CORS(app)

# this index page is required to ensure that the user is logged in on Google
# and to ensure that our app's OAuth Client has the access token to obtain the user's info from Google (checked by google.authorized)
# else redirect the user to the Google login page and get the OAuth access token with flask-dance
# if the user is logged in, the flask endpoint should serve the html file for the UI to the client.
@app.route("/index")
def index():
    if not google.authorized:
        print("no access token")
        return redirect(url_for("google.login"))

    try:
        # insert code to serve html file for UI
        resp = google.get("/oauth2/v1/userinfo")
        assert resp.ok, resp.text
        user_id = resp.json()["id"]
        return render_template('index.html', user_id=user_id)

    except Exception as e:
        return "There was an error retrieving your data from the Google API.<br>" + str(e)


@app.route('/login')
def login():
    return redirect(url_for("google.login"))

@app.route('/login/current-user')
def get_current_user():
    if not google.authorized:
        # return jsonify({"message": "Access token has expired"}), 500
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v1/userinfo")
        assert resp.ok, resp.text
    except Exception as e:
        print(e)
        return jsonify({"message": "Unable to retrieve user data"}), 500
    return jsonify({ 
        "userID": resp.json()["id"], 
        "username": resp.json()["email"].split("@")[0], 
        "fullname": resp.json()["name"], 
        "picture": resp.json()["picture"]})


@app.route('/login/callback')
def callback():
    if not google.authorized:
        print("no access token")
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v1/userinfo")
        assert resp.ok, resp.text
    except Exception as e:
        return jsonify({"message": "Unable to retrieve user data", "error": str(e)}), 500

    usergoogleid = resp.json()["id"]
    username = resp.json()["email"].split("@")[0]
    fullname = resp.json()["name"]
    picture = resp.json()["picture"]
    
    user_res = requests.get('http://esdosmessaging.tk:8000/api/user/' + usergoogleid)
    
    if user_res.status_code not in [200,404]:
        return jsonify({"message": "Error accessing user database"}), 500

    if not (user_res.ok):
        try:
            user_info = {"userID": usergoogleid, "username": username, "fullname": fullname, "picture": picture}
            res = requests.post('http://esdosmessaging.tk:8000/api/user' + usergoogleid, json=user_info)

            if not res.ok:
                return jsonify(json.loads(res.text))
            
            return "<head><title>ESDOS Registration</title></head><body>ESDOS account created! You may now close this tab.</body>"
        except Exception as e:
            return str(e) + " 500"
    else:
        user = json.loads(user_res.text)
        
        # Update user's profile picture if it has changed
        if user["picture"] != picture:
            try:
                picture_res = requests.post('http://esdosmessaging.tk:8000/api/user/picture/' + usergoogleid, json={"picture": picture})
                if not picture_res.ok:
                    return jsonify(json.loads(picture_res.text))
            except Exception as e:
                return str(e) + " 500"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001, debug=True)
#rmb to change back to 9001 after local testing