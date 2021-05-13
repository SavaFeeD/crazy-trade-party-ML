from flask import Flask

from router import route
from config import conf

app = Flask(__name__, static_url_path='/static/')

conf(app)
route(app)

if __name__ == '__main__':
    app.run(debug=True)
