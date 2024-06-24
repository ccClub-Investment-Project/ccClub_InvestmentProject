from flask import Flask

app = Flask(__name__)  # noqa E402

from app import routes
