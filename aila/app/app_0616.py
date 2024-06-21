# cd ccClub_InvestmentProject/aila
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
# def index():
#     return render_template('app_0619_merge.html')
def index():
    return render_template('app_0619_merge.html')


if __name__ == '__main__':
    app.run(debug=True)
