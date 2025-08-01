from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db 
from config import Config

auth_bp = Blueprint('auth', __name__)

#Admin Login Route
@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']  # Get Username from form
        password = request.form['password']  # Get password from form
        if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:  # checking the credentials is correct that set in config.py
            session['is_admin_logged_in'] = True # initialized the session to true
            flash("Welcome, admin!", "success")
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template("auth/admin_login.html")

# User Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']  # Get Username from form
        password = request.form['password']  # Get Password from form
        user = User.query.filter_by(username=username).first()  # Searching the user in database
        if user and check_password_hash(user.password, password):   
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for('user.user_dashboard'))
        flash("Invalid credentials", "danger")
    return render_template('auth/login.html')

# User Registration Route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']  # Get Username from form
        password = generate_password_hash(request.form['password'])  # Get Hashed Password from form
        existing_user = User.query.filter_by(username=username).first() # Searching Is user exist in database
        if existing_user:
            flash("Username already exists", "danger")
            return redirect(url_for('auth.register'))
        user = User(username=username, password=password)  # Geting the entered credentials by user 
        db.session.add(user) 
        db.session.commit()  # Commiting the credentials 
        flash("Registration successful. Please login.", "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

# Logout Route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('is_admin_logged_in', None)  # Clear admin session
    flash("Logged out", "info")
    return redirect(url_for('auth.login')) 