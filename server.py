import os

from flask import Flask

# create flask app that does nothing
app = Flask(__name__)
app.run(debug=False, host='0.0.0.0', port=os.environ.get('PORT'))
