# Define the admin credentials
import hashlib
from functools import wraps

from app.forms import LoginForm


ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = hashlib.sha256('1234'.encode()).hexdigest()

def verify_admin(username, password):
    """Verify if the provided username and password match the admin credentials."""
    return (username == ADMIN_USERNAME and 
            hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH)

from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if verify_admin(username, password):
            session['admin_logged_in'] = True
            flash(f'Logged in successfully! {session['admin_logged_in']}', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form = form)

@auth.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function



