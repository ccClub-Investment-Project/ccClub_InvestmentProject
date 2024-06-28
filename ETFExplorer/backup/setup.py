from setuptools import setup, find_packages

setup(
    name="ccClub_InvestmentProject",  # 專案名稱
    version="0.1",  # 專案版本
    packages=find_packages(),  # 自動尋找所有包
    install_requires=[  # 列出專案的依賴
        # 在這裡添加你的依賴，例如：
        'pandas',
        'sqlalchemy',
        'psycopg2',
        'flask',
        'tqdm',
        # 添加更多依賴...
    ],
)
