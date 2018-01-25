from flask import render_template, flash, redirect, url_for
from doliapp import app
from doliapp.forms import LoginForm

@app.route('/')
@app.route("/index")
def index():
    user = {"username": "dolly"}
    posts = [
        {
            "author": {"username": "joão@mesquita.sms"},
            "body": "licitação nº3/2018"
        },
        {
            "author": {"username": "susana@mesquita.gp"},
            "body": "decreto nº27/2018"
        }
    ]
    return render_template("index.html", title="Home", user=user)

@app.route("/login", methods=['GET', 'POST'])
def login():
    formI = LoginForm()
    if formI.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(formI.username.data, formI.remember_me.data))
        return redirect(url_for("index"))
    return render_template("login.html", title="entrar", form=formI)
