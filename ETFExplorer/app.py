from flask import Flask

def create_app():
    app = Flask(__name__)
    from app_tools.routes import init_routes
    init_routes(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)