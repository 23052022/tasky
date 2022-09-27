from sqlalchemy import Column, Integer, String, Numeric, Text
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = "account"
    id = Column(String(10), primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)
    currency_name = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            "self.user_id": self.user_id,
            'self.balance': self.balance,
            'self.currency_name': self.currency_name
        }


class Currency(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False)
    USD_relative_value = Column(Numeric, nullable=False)
    available_quantity = Column(Numeric, nullable=False)
    date = Column(String(10), nullable=False)

    def to_dict(self):
        return {
            "self.name": self.name,
            'self.USD_relative_value': self.USD_relative_value,
            'self.available_quantity': self.available_quantity,
            'self.date': self.date
        }


class Deposit(Base):
    __tablename__ = "deposit"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer(), nullable=False)
    opening_date = Column(Text, nullable=False)
    closing_date = Column(Text)
    balance = Column(Integer, nullable=False)
    interest_rate = Column(Numeric, nullable=False)
    conditions = Column(Text, nullable=False)

    def to_dict(self):
        return {
            "self.user_id": self.user_id,
            'self.opening_date': self.opening_date,
            'self.closing_date': self.closing_date,
            'self.balance': self.balance,
            "self.interest_rate": self.interest_rate,
            'self.conditions': self.conditions

        }


class Rating(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, nullable=False)
    currency_name = Column(Text, nullable=False)
    rating = Column(Integer(), nullable=False)
    comment = Column(Text, nullable=False)

    def to_dict(self):
        return {
            "self.currency_name": self.currency_name,
            'self.rating': self.rating,
            'self.comment': self.comment
        }


class TransactionHistory(Base):
    __tablename__ = "transaction_history"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Text, nullable=False)
    operation_type = Column(Text, nullable=False)
    currency_num_spent = Column(Text, nullable=False)
    currency_num_obtained = Column(Text, nullable=False)
    date_time = Column(Text, nullable=False)
    account_from_which_the_transaction = Column(Numeric, nullable=False)
    account_on_which_the_transaction = Column(Numeric, nullable=False)
    commission = Column(Numeric, nullable=False)
    queue_id = Column(Text, nullable=False)

    def to_dict(self):
        return {
            "self.user_id": self.user_id,
            'self.operation_type': self.operation_type,
            'self.currency_num_spent': self.currency_num_spent,
            'self.currency_num_obtained': self.currency_num_obtained,
            "self.date_time": self.date_time,
            'self.account_from_which_the_transaction': self.account_from_which_the_transaction,
            "self. account_on_which_the_transaction": self.account_on_which_the_transaction,
            'self. commission': self.commission,
            'self.queue_id': self.queue_id
        }


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    login = Column(Text, nullable=False)
    password = Column(Text, nullable=False)

    def to_dict(self):
        return {
            "self.login": self.login,
            'self.password': self.password
        }
