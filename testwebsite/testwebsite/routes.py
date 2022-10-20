from flask import render_template, flash, redirect, url_for, request
from testwebsite.forms import LoginForm, RegisterForm, BalanceForm, AddExpenseCategoryForm, AddIncomeCategoryForm, \
    AddIncomeTransactionForm, AddExpenseTransactionForm
from testwebsite.models import User, ExpenseCategories, IncomeCategories, StartingBalance, IncomeTransactions, \
    ExpenseTransactions
from testwebsite import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError as Err
from datetime import date
import calendar

today = date.today()
end_of_month = calendar.monthrange(date.today().year, date.today().month)[1]


# resets all transactions for all users once the end of the month comes
# todo throws error:SAWarning: Multiple rows returned with uselist=False for lazily-loaded attribute
#  'ExpenseTransactions.exp_category_name'
def reset_transactions(today_date, eom):
    if today_date == eom:
        stmt = db.session.query(User).all()
        for user in stmt:
            exp_tx = db.session.query(ExpenseTransactions). \
                filter(ExpenseTransactions.user_id == user.id).all()
            for tx in exp_tx:
                db.session.delete(tx)
                db.session.commit()
        return "Transactions Reset"


def show_categories(key):
    totals = {}
    query2 = [ExpenseCategories.query.filter_by(user_id=current_user.id).all() if key == 'expense' else
              IncomeCategories.query.filter_by(user_id=current_user.id).all()]
    query = [ExpenseTransactions.query.filter_by(user_id=current_user.id).all() if key == 'expense' else
             IncomeTransactions.query.filter_by(user_id=current_user.id).all()]
    for category_name in query2[0]:
        totals[category_name.name] = 0
        for instance in query[0]:
            if instance.category == category_name.name:
                totals[category_name.name] += instance.amount
    return totals


@app.route("/")
@app.route("/home")
def home():
    title = "Home"
    return render_template(".///index.html", title=title)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f"Incorrect Login Credentials, Please Try Again!", 'danger')
    return render_template("./login.html", title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!, you are now able to login!', 'success')
        return redirect(url_for('login'))
    return render_template("./register.html", title="Register", form=form)


@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    exp_category_totals = show_categories('expense')
    inc_category_totals = show_categories('income')
    balance_form = BalanceForm()
    add_expense_category_form = AddExpenseCategoryForm()
    starting_balance = StartingBalance.query.filter_by(user_id=current_user.id).all()
    add_income_category_form = AddIncomeCategoryForm()
    expense_categories = [category for category in ExpenseCategories.query.filter_by(user_id=current_user.id)]
    income_categories = [category for category in IncomeCategories.query.filter_by(user_id=current_user.id)]
    expense_transaction_total = sum(
        [i.amount for i in ExpenseTransactions.query.filter_by(user_id=current_user.id).all()])
    income_transaction_total = sum(
        [i.amount for i in IncomeTransactions.query.filter_by(user_id=current_user.id).all()])
    expense_total = sum([amount.planned_amount for amount in expense_categories])
    income_total = sum([amount.planned_amount for amount in income_categories])
    if current_user.is_authenticated:
        if request.method == "POST":
            data = request.form.to_dict()
            # Updating Starting Balance
            if balance_form.validate_on_submit() and balance_form.starting_balance.data:
                try:
                    stmt = StartingBalance(user_id=current_user.id, starting_balance=balance_form.starting_balance.data)
                    db.session.add(stmt)
                    db.session.commit()
                    flash('Starting Balance Updated!', 'success')
                    return redirect(url_for('dashboard'))
                except Err as e:
                    print(f'SQLAlchemy Error: {e}')
                    return redirect(url_for('dashboard'))
            # Adding Expense Category
            elif add_expense_category_form.validate_on_submit() and add_expense_category_form.expense_name.data:
                category = ExpenseCategories(date=add_expense_category_form.data['expense_date'],
                                             user_id=current_user.id,
                                             name=add_expense_category_form.expense_name.data,
                                             planned_amount=add_expense_category_form.expense_planned.data)
                db.session.add(category)
                db.session.commit()
                flash('New Expense Category Added!', 'success')
                return redirect(url_for('dashboard'))
            # Removing Expense Category
            elif "RemoveExpense" in request.form.to_dict():
                try:
                    user = db.session.query(ExpenseCategories). \
                        filter(ExpenseCategories.user_id == current_user.id). \
                        filter(ExpenseCategories.name == data["RemoveExpense"]). \
                        first()
                    db.session.delete(user)
                    db.session.commit()
                    flash('Expense Category Removed', 'success')
                except Err as e:
                    print(f'SQLAlchemy Error: {e}')
                    return redirect(url_for('dashboard'))
                return redirect(url_for('dashboard'))
            # Adding Income Category
            elif add_income_category_form.validate_on_submit() and add_income_category_form.income_name.data:
                category = IncomeCategories(date=add_income_category_form.data['income_date'],
                                            user_id=current_user.id,
                                            name=add_income_category_form.income_name.data,
                                            planned_amount=add_income_category_form.income_planned.data)
                db.session.add(category)
                db.session.commit()
                flash('New Income Category Added!', 'success')
                return redirect(url_for('dashboard'))
            # Removing Income Category
            elif "RemoveIncome" in request.form.to_dict():
                try:
                    user = db.session.query(IncomeCategories). \
                        filter(IncomeCategories.user_id == current_user.id). \
                        filter(IncomeCategories.name == data["RemoveIncome"]). \
                        first()
                    db.session.delete(user)
                    db.session.commit()
                    flash('Income Category Removed!', 'success')
                except Err as e:
                    print(f'SQLAlchemy Error: {e}')
                    return redirect(url_for('dashboard'))
                return redirect(url_for('dashboard'))
            else:
                return render_template('./dashboard.html', title='Dashboard', balance_form=balance_form,
                                       add_expense_category_form=add_expense_category_form,
                                       add_income_category_form=add_income_category_form,
                                       expense_categories=expense_categories, income_categories=income_categories,
                                       expense_total=expense_total, income_total=income_total,
                                       starting_balance=starting_balance, exp_category_totals=exp_category_totals,
                                       expense_transaction_total=expense_transaction_total,
                                       income_transaction_total=income_transaction_total,
                                       inc_category_totals=inc_category_totals)
        # GET Request
        else:
            return render_template('./dashboard.html', title='Dashboard', balance_form=balance_form,
                                   add_expense_category_form=add_expense_category_form,
                                   add_income_category_form=add_income_category_form,
                                   expense_categories=expense_categories, income_categories=income_categories,
                                   expense_total=expense_total, income_total=income_total,
                                   starting_balance=starting_balance, exp_category_totals=exp_category_totals,
                                   expense_transaction_total=expense_transaction_total,
                                   income_transaction_total=income_transaction_total,
                                   inc_category_totals=inc_category_totals)


@app.route("/transactions", methods=['POST', 'GET'])
@login_required
def transactions():
    expense_form = AddExpenseTransactionForm()
    income_form = AddIncomeTransactionForm()
    expense_categories = [category for category in ExpenseCategories.query.filter_by(user_id=current_user.id)]
    income_categories = [category for category in IncomeCategories.query.filter_by(user_id=current_user.id)]
    expense_table_data = [row for row in ExpenseTransactions.query.filter_by(user_id=current_user.id)]
    income_table_data = [row for row in IncomeTransactions.query.filter_by(user_id=current_user.id)]
    if current_user.is_authenticated:
        if request.method == 'POST':
            form2 = request.form.to_dict()
            # Adding Expense Transaction
            if expense_form.validate_on_submit() and expense_form.exp_txn_description.data:
                try:
                    if len(form2.keys()) == 5:
                        stmt = ExpenseTransactions(user_id=current_user.id,
                                                   amount=expense_form.exp_txn_amount.data,
                                                   description=expense_form.exp_txn_description.data,
                                                   category=form2['tx_category'])
                    else:
                        flash('Please Enter a Category!', 'danger')
                        return redirect(url_for('transactions'))
                    db.session.add(stmt)
                    db.session.commit()
                    flash('New Expense Transaction Added!', 'success')
                    return redirect(url_for('transactions'))
                except Err as e:
                    print(f'SQLAlchemy Error: {e}')
                    return redirect(url_for('transactions'))
            # Removing Expense Transaction
            elif 'RemoveExpenseTransaction' in form2:
                try:
                    ExpenseTransactions.query.filter_by(trans_id=int(form2['RemoveExpenseTransaction'])) \
                        .delete()
                    db.session.commit()
                    flash('Removed Expense Transaction', 'success')
                    return redirect(url_for('transactions'))
                except Err as e:
                    print(f'SQLAlchemy Error: {e}')
                    return redirect(url_for('transactions'))
            # Adding Income Transaction
            if income_form.validate_on_submit() and income_form.inc_txn_description.data:
                try:
                    stmt = IncomeTransactions(user_id=current_user.id,
                                              amount=income_form.inc_txn_amount.data,
                                              description=income_form.inc_txn_description.data,
                                              category=request.form.to_dict()['tx_category'])
                    db.session.add(stmt)
                    db.session.commit()
                    flash('New Income Transaction Added!', 'success')
                    return redirect(url_for('transactions'))
                except Err as e:
                    print(f'SQLAlchemy Error: {e}')
                    return redirect(url_for('transactions'))
            # Removing Income Transaction
            elif 'RemoveIncomeTransaction' in form2:
                try:
                    IncomeTransactions.query.filter_by(trans_id=int(form2['RemoveIncomeTransaction'])) \
                        .delete()
                    db.session.commit()
                    flash('Removed Income Transaction', 'success')
                    return redirect(url_for('transactions'))
                except Err as e:
                    print(f'SQLAlchemy Error: {e}')
                    return redirect(url_for('transactions'))
            # Error
            else:
                flash(income_form.errors, 'danger')
                return redirect(url_for('transactions'))
        else:
            return render_template(".///transactions.html", title='Transactions', income_form=income_form,
                                   expense_form=expense_form,
                                   expense_categories=expense_categories,
                                   income_categories=income_categories, expense_table_data=expense_table_data,
                                   income_table_data=income_table_data)


@app.route("/about")
def about():
    return render_template("./about.html", title='About')
