from celery import Celery
import datetime
import database
import models

app = Celery('celery_worker', broker='pyamqp://guest@localhost//')


def course_ups1_to_ups2(currency_UPS1, currency_UPS2):
    date_now = datetime.datetime.now().strftime("%d-%m-%Y")
    res = models.Currency.query.filter_by(name=currency_UPS1, date=date_now).first()
    res1 = models.Currency.query.filter_by(name=currency_UPS2, date=date_now).first()
    if res is None or res1 is None:
        return 'Error! No currency for trade.'
    return {
        'exchange': f'{res.USD_relative_value / res1.USD_relative_value}',
        'status': 'ok'
    }


@app.task
def task1(user_id, currency_UPS1, currency_UPS2, amount, queue_id):
    database.init_db()
    date_now = datetime.datetime.now().strftime("%d-%m-%Y")
    user_balance1 = models.Account.query.filter_by(user_id=user_id, currency_name=currency_UPS1).first()
    user_balance2 = models.Account.query.filter_by(user_id=user_id, currency_name=currency_UPS2).first()
    cur1_USD_relative_value = models.Currency.query.filter_by(name=currency_UPS1, date=date_now).first()
    cur2_USD_relative_value = models.Currency.query.filter_by(name=currency_UPS2, date=date_now).first()
    need_cur2 = amount * float(cur1_USD_relative_value.USD_relative_value) / float(
        cur2_USD_relative_value.USD_relative_value)

    if user_balance2.balance > need_cur2 and cur1_USD_relative_value.available_quantity > amount:
        user_balance2.balance = user_balance2.balance - need_cur2
        cur1_USD_relative_value.available_quantity = float(cur1_USD_relative_value.available_quantity) + need_cur2
        cur2_USD_relative_value.available_quantity = float(cur2_USD_relative_value.available_quantity) - amount
        user_balance1.balance = user_balance1.balance + amount
        try:
            database.db_session.add(user_balance2)
            database.db_session.add(cur1_USD_relative_value)
            database.db_session.add(cur2_USD_relative_value)
            database.db_session.add(user_balance1)
            database.db_session.commit()
        except Exception:
            return 'Data Base Error'

        money_operation = models.TransactionHistory(
            user_id=user_id,
            operation_type='exchange',
            currency_num_spent=need_cur2,
            currency_num_obtained=currency_UPS1,
            date_time=date_now,
            account_from_which_the_transaction=user_balance1.id,
            account_on_which_the_transaction=user_balance2.id,
            commission=0,
            queue_id=queue_id
        )
        try:
            database.db_session.add(money_operation)
            database.db_session.commit()

        except Exception:
            return 'Data Base Error'
    else:
        return 'Error'

    return True
