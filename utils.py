from functools import wraps
from flask import session, flash, redirect, url_for

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print('admin_required called, session:', session.get('is_admin_logged_in'))
        if not session.get('is_admin_logged_in'):
            flash("Admin login required", "warning")
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function 