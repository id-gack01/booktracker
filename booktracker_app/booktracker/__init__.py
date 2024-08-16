from flask import Flask

import os

# pip install flask werkzeug

# run
# flask --app booktracker init-db
# in the same directory as booktracker (so in booktracker_app)

# then run...
# flask --app __init__.py run
# to run the project --debug will help

#this is the create_app factory method
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    # below sets some default app configuration
    app.config.from_mapping(
        # data safety mechanism
        #os.path.join takes multiple paths and combines the two of them together
        #the config,py path is combined with the path to the instance,
        SECRET_KEY=os.path.join(app.instance_path, 'config.py'),
        # DATABASE is the path where the SQLite database file will be saved
        DATABASE=os.path.join(app.instance_path, 'booktracker.sqlite'),
    )


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route("/testapp")
    def testapp():
        return "App is at least running"

    

    #import db configuration
    from . import db
    #initialize the database
    db.init_app(app)

    #import auth blueprint
    from . import auth
    #register auth blueprint
    app.register_blueprint(auth.bp)

    #import book blueprint
    from . import book
    #register book blueprint
    app.register_blueprint(book.bp)


    #associate the book blueprint with the index for the app
    app.add_url_rule('/', endpoint='index')

    return app
