import os  # noqa: E402
import sys  # noqa: E402
print(os.getcwd())  # noqa: E402
# 确保当前工作目录为项目的根目录
current_path = os.path.dirname(os.path.abspath(__file__))  # noqa: E402
project_root = os.path.join(current_path, '..')  # noqa: E402
sys.path.insert(0, project_root)  # noqa: E402
os.chdir(project_root)  # noqa: E402


from app.utils import setup_project_root

setup_project_root()  # noqa E402

from flask import Flask
from app.routes import init_routes

app = Flask(__name__)
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
