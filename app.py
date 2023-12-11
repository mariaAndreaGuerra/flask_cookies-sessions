from flask import Flask, request, render_template, redirect
from flask import session, make_response

app = Flask(__name__)
app.config["SECRET_KEY"] = "4534gdghjk5d#$RGR^HDG"


@app.before_request
def print_cookies():
    """For every single request that comes in, print out request.cookies (printed to terminal)"""
    print("*********************")
    print(request.cookies)
    print("*********************")


@app.route("/")
def index():
    """Homepage."""
    return render_template("index.html")


@app.route("/demo")
def res_demo():
    content = "<h1>HELLO!!</h1>"
    res = make_response(content)
    res.set_cookie("jolly_rancher_flavor", "grape")
    return res

@app.route("/form-cookie")
def show_form():
    """Show form that prompts for favorite color."""

    return render_template("form-cookie.html")


@app.route("/handle-form-cookie")
def handle_form():
    """Return form response; include cookie for browser."""

    fav_color = request.args["fav_color"]
    html = render_template("response-cookie.html", fav_color=fav_color)
    resp = make_response(html)

    resp.set_cookie("fav_color", fav_color)

    return resp


@app.route("/later-cookie")
def later():
    """An example page that can use that cookie."""

    fav_color = request.cookies.get("fav_color", "<unset>")

    return render_template("later-cookie.html", fav_color=fav_color)


@app.route("/form-session")
def show_sessions_form():
    """Show form that prompts for nickname and lucky number."""

    return render_template("form-session.html")


@app.route("/handle-form-session")
def handle_sessions_form():
    """Return agreeable response and save to session."""

    session["nickname"] = request.args["nickname"]
    session["lucky_number"] = int(request.args["lucky_number"])

    return render_template("response-session.html")


@app.route("/later-session")
def session_later():
    """An example page that uses that session info."""

    nickname = session.get("nickname", "<no nickname>")

    return render_template("later-session.html", nickname=nickname)


@app.route("/login-form")
def show_login_form():
    """Show form that prompts users to enter the secret access code"""
    return render_template("login-form.html")


@app.route("/login")
def verify_secret_code():
    """
    Checks to see if the entered access code is correct

    - If the code is incorrect, redirect users back to the login form to try again

    - If the code is correct...
        - set session to indicate that user has access
        - redirect to the secret invite
    """
    SECRET = "chickenz_are_gr8"
    entered_code = request.args["secret_code"]
    if entered_code == SECRET:
        session["entered-pin"] = True
        return redirect("/secret-invite")
    else:
        return redirect("/login-form")


@app.route("/secret-invite")
def show_secret_invite():
    """
    Check to see if session contains 'entered-pin' (if user entered the correct secret code)

    - If it does, render the invite template

    - If session['entered-pin'] is missing or False, redirect user to the form to enter the secret code
    """
    if session.get("entered-pin", False):
        return render_template("invite.html")
    else:
        return redirect("/login-form")
