from flask import Flask
from app_tools.routes import init_routes

def create_app():
    app = Flask(__name__)    
    app = init_routes(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)