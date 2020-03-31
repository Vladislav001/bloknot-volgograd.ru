from flask import Flask, render_template, redirect, url_for, request
from database import Database

database = Database()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    page = request.args.get('page')
    if page == None:
        nextPage = 2
        page = 1
    else:
        nextPage = int(page) + 1

    records = database.getPaginationRecords(page, 10)
    return render_template('index.html', records=records, nextPage=nextPage)

@app.route('/change_shedule', methods=['POST'])
def change_shedule():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()