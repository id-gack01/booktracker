
import click
import sqlite3

from flask import current_app, g

#g is a special object that's unique for each request.
# It's used to store data that might be accessed by multiple functions during the request
#this whole file has a similar concept to the db.js file from a MEAN stack or MERN stack javascript app
#sets the database connections


"""
this is the db connection file that lets my app communicate with the database i created in schema.sql
"""


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            #current_app is a special object that points to the Flask application handling the request
            #get_db will be called when application has been created and handling a request, so current_app can be used
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #tells connection to return rows the behave like dicts, allowing accessing columns by name
        g.db.row_factory = sqlite3.Row
    return g.db


#functions to run the sql commands seen in schema.sql file
def init_db():
    #get_db (defined above) returns a database connection
    db = get_db()
    #open_resource opens a resource file relative to root_path for reading.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


#click command defines a command line command called init-db that calls init_db function and shows a success message
# to the user. Remember the same concept as the javascript apps I made
# afterward run the " flask --app booktracker init-db" command in the directory that contains the booktracker directory
@click.command('init-db')
def init_db_command():
    # Clear the existing data and create new tables.
    #the init_db function written above is executed here
    init_db()
    click.echo('Initialized the database. ')


#close_db and init_db functions need to be registered with the app instance to be used by the application
# i need to write a function that takes an application and does the registration
def init_app(app):
    app.teardown_appcontext(close_db)  # tells Flask to call that function when cleaning up after returning response
    app.cli.add_command(init_db_command)  # adds a new command that can be called with the flask command


#checks if connection was created by checking if db was set
#this gets passed to the app.teardown method located in the init_app function below
def close_db(e=None):
    db = g.pop('db', None)
    #if connection exists, it is closed
    if db is not None:
        db.close()


