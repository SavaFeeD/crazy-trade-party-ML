from flask import Flask
from router import route

app = Flask(__name__, static_url_path='/static/')

route(app)

if __name__ == '__main__':
    app.run(debug=True)
