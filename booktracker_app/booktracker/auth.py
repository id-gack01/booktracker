#the auth blueprint

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
#from flaskr/db import get_db
from .db import get_db

#authentication blueprint will have views to register new users (line 18) and to log in (line 57) and log out (line 105)
#i just took from the tutorial becasuse why not

#creates blueprint named auth, __name__ is passed, so it knows where it's defined,
# url_prefix ('/auth') will be prepended to all URLS associated with the blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')


#registers new users
#associates URL register with register view function
@bp.route('/register', methods=('GET', 'POST'))
def register():
    #if users submits funtion, request method is post, and input is validated
    if request.method == 'POST':
        #request.form special type of dict mapping submitted form keys and values
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        #if validiation success, insert new user data into the database
        if error is None:
            try:
                # the ?, ? are placeholders for user input, and they are placed into the sql below
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?,?)',
                    (username, generate_password_hash(password)),
                )
                #commit rears its ugly head
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                #after storing user, redirect to login page.url_for() generates URL for the login view based on its name
                return redirect(url_for("auth.login"))
        flash(error)  # flash an error if validation fails
    return render_template('auth/register.html')
    #When the user initially navigates to auth/register, or there was a validation error,
    # an HTML page with the registration form should be shown. render_template() will render a template
    # containing the HTML, which you’ll write in the next step of the tutorial.


#login function
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None  # None is absence of a value, the error will be filled if an error occures upon execution
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        #fetchone() returns one row from the query, if no results return, it returns None.
        if user is None:
            error = 'Incorrect username'
        # hashes submited password and compares to the stored password
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        if error is None:
            #session is a dict that stores data across requests, if valid, id is stored in a new session
            # data is stored in a cookie sent to the browser and browser sends it back with subsequent requests
            session.clear()
            session['user_id'] = user['id']  # user_id is assigned here
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')


#at the beginning of each request, if a user is logged in their information should be loaded and made available to other
# views

#this is a request hook
#registers a function that runs BEFORE the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    #checks if user id is stored in the session and gets that user's data from the database, storing it in g.user
    # this arrangement lasts for the length of the request
    user_id = session.get('user_id')

    #no user id, or it doesn't exist, g.user will be None
    if user_id is None:
        g.user = None
    else:
        # uses the user_id as a way to select that user from the database of users
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


#remove user_id from the session
@bp.route('/logout')
def logout():
    # clears the request session and sends the user back to the index
    session.clear()
    return redirect(url_for('index'))


#view function here is def wrapped_view(**kwargs)
#creating, editing, and deleting book posts requires a user to be logged in
# a decorator can be used to check this for each view it's applied to
#this decorater returns a new view function that wraps the original view it's applied to
# checks if user is loaded and redirects to the login page other
# if user is loaded, original view is called and continues normally.
# this decorate will be used when writing book views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view

#url_for() function generates the URL to a view based on a name and arguments
# name associated with a view is also called the endpoint, by default it's the same as the name of the view function
