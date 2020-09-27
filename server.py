from flask import Flask

# create flask app that does nothing
app = Flask(__name__)
app.run(environ.get('PORT'))
