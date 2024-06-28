# 放置通用工具函數

import os
import sys


def setup_project_root():
    current_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_path, '..')
    sys.path.insert(0, project_root)
    os.chdir(project_root)



