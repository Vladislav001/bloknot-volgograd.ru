from flask import Flask, render_template
from database import Database

database = Database()
allRecords = database.getAllRecords()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', records=allRecords)

@app.route('/main')
def main():
    return 'main'

if __name__ == "__main__":
    app.run()