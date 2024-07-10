from flask import Flask
from flask_caching import Cache
from app_tools.routes import init_routes

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
init_routes(app, cache)


if __name__ == '__main__':
    app.run(debug=True)