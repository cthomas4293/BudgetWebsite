from testwebsite import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    expense_transactions = db.relationship('ExpenseTransactions', backref='exp_tx_user_id', lazy=True)
    income_transactions = db.relationship('IncomeTransactions', backref='inc_tx_user_id', lazy=True)
    expense_categories = db.relationship('ExpenseCategories', backref='exp_cat_user_id', lazy=True)
    income_categories = db.relationship('IncomeCategories', backref='inc_cat_user_id', lazy=True)
    starting_balance = db.relationship('StartingBalance', backref='id_balance', lazy=True)
    time_stamps = db.relationship('TimeStamps', backref='stamp_time', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class ExpenseCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    planned_amount = db.Column(db.Integer, nullable=False)
    expense_transactions = db.relationship('ExpenseTransactions', cascade='all, delete', backref='exp_category_name',
                                           lazy=True)

    def __repr__(self):
        return f"Expense Category('{self.name}', '{self.planned_amount}')"


class IncomeCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    planned_amount = db.Column(db.Integer, nullable=False)
    income_transactions = db.relationship('IncomeTransactions', cascade='all, delete', backref='inc_category_name',
                                          lazy=True)

    def __repr__(self):
        return f"Income Category('{self.name}', '{self.planned_amount}')"


class ExpenseTransactions(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trans_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), db.ForeignKey('expense_categories.name'), nullable=False,
                         default='Miscellaneous')
    date = db.Column(db.Integer, nullable=False, default=datetime.utcnow())
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Expense Transactions('{self.category}', '{self.date}', '{self.amount}', '{self.description}')"


class IncomeTransactions(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trans_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), db.ForeignKey('income_categories.name'), nullable=False,
                         default='Miscellaneous')
    date = db.Column(db.Integer, nullable=False, default=datetime.utcnow())
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Income Transactions('{self.category}', '{self.date}', '{self.amount}', '{self.description}')"


class StartingBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    starting_balance = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DATETIME, nullable=False, default=datetime.utcnow())


class TimeStamps(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DATETIME, nullable=False, primary_key=True)
