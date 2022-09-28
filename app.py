import datetime
import uuid

from flask import Flask, request, render_template, session

import celery_worker
import database
import models
from models import Rating, Currency, TransactionHistory, User
from celery_worker import task1

app = Flask(__name__)
app.secret_key = 'ghgfdghkljhgfdhk'





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

@app.get('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def init_transaction(currency_UPS1: str, currency_UPS2: str):
    if session.get('user_id') is not None:
        return"""
                <form  method="post">

  <div class="container">
    <label for="uname"><b>amount_currency</b></label>
    <input type="text" placeholder="Enter value" name="amount_currency" required>

    <button type="submit">Login</button>
   
  </div>

</form>
</html>
        """
    else:
        return 'ok'


@app.post('/currency/trade/<currency_UPS1>/<currency_UPS2>')
def currency_trade_post(currency_UPS1: str, currency_UPS2: str) -> dict:
    user_id = session.get('user_login')
    amount = float(request.form.get('amount_currency'))

    # req = request.json
    # user_id = req['data']['id_user']
    # amount = req['data']['amount']
    queue_id = uuid.uuid4()
    database.init_db()
    task_obj = task1.apply_async(args=[user_id, currency_UPS1, currency_UPS2, amount, queue_id])
    return {'task_id': str(task_obj)}


@app.route('/user', methods=['GET', 'POST'])
def get_user_info() -> (list, str):
    database.init_db()
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id is None:
            return """
            <html>
            <form  method="post">

  <div class="container">
    <label for="uname"><b>Username</b></label>
    <input type="text" placeholder="Enter Username" name="uname" required>

    <label for="psw"><b>Password</b></label>
    <input type="password" placeholder="Enter Password" name="psw" required>

    <button type="submit">Login</button>
   
  </div>

</form>
</html>
            """
        else:
            user_info = User.query.filter_by(login=user_id).all()
            if len(user_info) == 0:
                return 'No user'
            return [item.to_dict() for item in user_info]
    if request.method == 'POST':
        user_login = request.form.get('uname')
        user_password = request.form.get('psw')
        user_info_creds = models.User.query.filter_by(login=user_login, password=user_password).all()
        if user_info_creds:
            session['user_id'] = user_login
            return 'Ok'
        else:
            return 'Error'


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


@app.get('/user/<user>/history')
def user_history(user):
    database.init_db()
    user_id = session.get('user_id')
    if user_id is None:
        return """
                <html>
                <form  method="post">

      <div class="container">
        <label for="uname"><b>Username</b></label>
        <input type="text" placeholder="Enter Username" name="uname" required>

        <label for="psw"><b>Password</b></label>
        <input type="password" placeholder="Enter Password" name="psw" required>

        <button type="submit">Login</button>

      </div>

    </form>
    </html>
                """
    else:
        user_info = User.query.filter_by(login=user_id).all()
        if len(user_info) == 0:
            return 'No history'
        res = TransactionHistory.query.filter_by(user_id=user_id).all()
        return [it.to_dict() for it in res]



@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
