import pickle
import time
import os
def get_absolute_path(filename):
    # 獲取當前腳本文件的絕對目錄
    current_path = os.path.dirname(os.path.abspath(__file__))
    etfexplorer_path = os.path.join(current_path, '..')
    # 構建絕對路徑
    return os.path.join(etfexplorer_path, 'preload', f'{filename}.pkl')

def save_data(data, filename):
    path = get_absolute_path(filename)

    # path = f'preload/{filename}.pkl'
    with open(path, 'wb') as file:
        pickle.dump(data, file)

def load_data(filename):
    path = get_absolute_path(filename)

    # path = f'preload/{filename}.pkl'
    with open(path, 'rb') as file:
        return pickle.load(file)


