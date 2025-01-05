from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# files
import user_management as dbHandler
import sanitize_and_validate as vs
# import factor_authentication.py as vs

# Code snippet for logging a message
# app.logger.critical("message")

from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import pyqrcode
import os
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]

        # sanitization
        feedback = make_web_safe(feedback)

        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")


@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # password check
        if not check_password(password):
            return "-"

        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)

        if isLoggedIn:

            user_secret = pyotp.random_base32() #generate the one-time passcode
            #return redirect(url_for('enable_2fa')) #redirect to 2FA page

            totp = pyotp.TOTP(user_secret)
            otp_uri = totp.provisioning_uri(name=username,issuer_name="YourAppName")
            qr_code = pyqrcode.create(otp_uri)
            stream = BytesIO()
            qr_code.png(stream, scale=5)
            qr_code_b64 = base64.b64encode(stream.getvalue()).decode('utf-8')
            
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")


# 9-12, 3 numbers, 4 letters
def check_password(password):
    if not isinstance(password, str):
        return False
    if not (1 <= len(password) <= 9):
        return False
    if not re.match("^[a-zA-Z0-9]*$", password):
        return False

    # alpha and num
    digits = sum(c.isdigit() for c in password)
    letters = sum(c.isalpha() for c in password)
    
    if digits < 3:
        return False
    if letters < 4:
        return False

    return True

# the library thing
def make_web_safe(string: str) -> str:
    return html.escape(string)


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000) ## left in debug mode
