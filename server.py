from flask import Flask, render_template, redirect, url_for, request
from database import Database

database = Database()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    page, next_page = get_pages_numbers(request)

    records = database.getPaginationNews(page, 10)
    return render_template('index.html', records=records, nextPage=next_page)

@app.route('/change_shedule', methods=['POST'])
def change_shedule():
    return redirect(url_for('index'))


@app.route('/tonality', methods=['GET'])
def get_tonality():
    page, next_page = get_pages_numbers(request)

    records = database.getPaginationPhrases(page, 10)

    return render_template(
        'tonality.html', records=records, next_page=next_page)


def get_pages_numbers(request):
    page = request.args.get('page', 1)
    next_page = int(page) + 1

    return page, next_page


if __name__ == "__main__":
    app.run()