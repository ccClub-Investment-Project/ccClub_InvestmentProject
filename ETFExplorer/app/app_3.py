
from utils import setup_project_root
setup_project_root()

from flask import Flask
from routes import init_routes

app = Flask(__name__)
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
