import datetime
import uuid

from flask import Flask, request, render_template

import database
from models import Rating, Currency, TransactionHistory, User
from celery_worker import task1

app = Flask(__name__)



@app.route('/', methods=['GET'])
def index() -> str:
    """
     Start page display with instruction
    """
    return render_template('index.html', title='Change for you')


@app.get('/currency/<currency_UPS>')
def currency_list(currency_UPS):
    database.init_db()
    res = Currency.query.filter_by(name=currency_UPS).all()
    return [it.to_dict() for it in res]


@app.get('/currency/<currency_UPS>/rating')
def currency_rating(currency_UPS):
    database.init_db()
    res = Rating.query.filter_by(currency_name=currency_UPS).all()
    return [it.to_dict() for it in res]


@app.get('/currency')
def all_currency_rating():
    database.init_db()
    res = Currency.query.all()
    return [it.to_dict() for it in res]


@app.post('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def currency_trade_post(currency_UPS1: str, currency_UPS2: str) -> dict:
    req = request.json
    user_id = req['data']['id_user']
    amount = req['data']['amount']
    queue_id = uuid.uuid4()
    task_obj = task1.apply_async(args=[user_id, currency_UPS1, currency_UPS2, amount, queue_id])
    return {'task_id': str(task_obj)}








@app.get('/user/<user_id>')
def login_get(user_id):
    database.init_db()
    res = User.query.filter_by(login=user_id).first()
    return res


@app.post('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def exchange(currency_UPS1, currency_UPS2):
    database.init_db()
    req = request.json
    date_now = datetime.datetime.now().strftime("%d-%m-%Y")
    amount = req['data']['amount']
    user_id = 1

    celery_worker.task1.apply_async()
    return req['status']


@app.post('/currency/<name>/review')
def currency_review_post(name):
    database.init_db()
    req = request.json
    cur_name = req['data']['currency_name']
    rating = req['data']['rating']
    comment = req['data']['comment']

    review = Rating(currency_name=name, rating=rating, comment=comment)
    database.db_session.add(review)
    database.db_session.commit()
    return 'OK'


@app.put('/currency/<name>/review')
def currency_review_put(name):
    return f'Review currency {name}, PUT method'


@app.delete('/currency/<name>/review')
def currency_review_gelete(name):
    return f'Review currency {name}, DELETE method'


@app.post('/user/transfer')
def transfer():
    pass


@app.get('/user/<user>/history')
def user_history(user):
    database.init_db()
    res = TransactionHistory.query.filter_by(user_id=user).all()
    return [it.to_dict() for it in res]



@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
