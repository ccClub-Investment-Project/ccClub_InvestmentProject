from flask import Flask

app = Flask(__name__)  # noqa E402

from ccClub_InvestmentProject.ETFExplorer.app.app_3 import routes
