from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm
from ..models import User
from .. import bcrypt
from .. import mail

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("posts.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        user.save()
        msg = Message("Welcome to the Daily Food Blog website! ",
                  sender="daily.food.blogger123@gmail.com",
                  recipients=[user.email])
        msg.body = "Thanks for signing up. Here you can post either your homemade meals or meals you've tried at restaurants and cafes. Be sure to add descriptions to your posts and to comment on others."
        mail.send(message=msg)
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("posts.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user)
            return redirect(url_for("users.account"))
        else:
            flash("Login failed. Check your username and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("posts.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateUsernameForm()
    if form.validate_on_submit():
        current_user.modify(username=form.username.data)
        current_user.save()
        return redirect(url_for("users.account"))

    return render_template("account.html", title="Account", form=form)
