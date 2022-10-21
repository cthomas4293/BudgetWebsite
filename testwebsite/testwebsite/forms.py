from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField, DateField
from wtforms.validators import Length, InputRequired, DataRequired, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from testwebsite.models import User
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[InputRequired(), Length(min=8, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    password_confirm = PasswordField('Password Confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # check whether user already in database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists!')


class BalanceForm(FlaskForm):
    starting_balance = IntegerField('StartingBalance', validators=[InputRequired()])
    submit = SubmitField('Save')


class AddExpenseTransactionForm(FlaskForm):
    exp_txn_date = DateField('Date', validators=[DataRequired()], default=datetime.utcnow())
    exp_txn_amount = IntegerField('Amount', validators=[InputRequired()])
    exp_txn_description = StringField('Description', validators=[InputRequired(), Length(min=2, max=30)])
    exp_txn_submit_transaction = SubmitField('Submit')


class AddIncomeTransactionForm(FlaskForm):
    inc_txn_date = DateField('Date', validators=[DataRequired()], default=datetime.utcnow())
    inc_txn_amount = IntegerField('Amount', validators=[InputRequired()])
    inc_txn_description = StringField('Description', validators=[InputRequired(), Length(min=2, max=30)])
    inc_txn_submit_transaction = SubmitField('Submit')


class AddExpenseCategoryForm(FlaskForm):
    expense_date = DateField('Date')
    expense_name = StringField("Category", validators=[InputRequired(), Length(min=2, max=30)])
    expense_planned = IntegerField("Planned", validators=[InputRequired()])
    expense_submit = SubmitField('Save')


class AddIncomeCategoryForm(FlaskForm):
    income_name = StringField("Category", validators=[InputRequired(), Length(min=2, max=30)])
    income_planned = IntegerField("Planned", validators=[InputRequired()])
    income_submit = SubmitField('Save')
