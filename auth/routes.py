from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from extensions import db
from auth.models import User
from auth.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

# Define Blueprint for authentication routes
auth_bp = Blueprint("auth_bp", __name__)


# Helper function to hash password
def hash_password(password):
    return generate_password_hash(password)


# Helper function to check hashed password
def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)


@auth_bp.route("/")
def base():
    if current_user.is_authenticated:
        return redirect(url_for("chat_bp.chat"))

    return render_template(
        "base.html", register_form=RegistrationForm(), login_form=LoginForm()
    )


@auth_bp.post("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("chat_bp.chat"))

    form = RegistrationForm(request.form)

    if form.validate():
        # Hash the password and create a new user
        hashed_password = hash_password(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password,
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect("/")

    return render_template(
        "base.html", register_form=form, login_form=LoginForm(), action="register"
    )


@auth_bp.post("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("chat_bp.chat"))

    form = LoginForm(request.form)

    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()

        if user and verify_password(form.password.data, user.password_hash):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("chat_bp.chat"))
        else:
            flash("Invalid credentials.", "error")
            return redirect("/")
    return render_template(
        "base.html", login_form=form, register_form=RegistrationForm(), action="login"
    )


@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect("/")
