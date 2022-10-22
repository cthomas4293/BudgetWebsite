import calendar
import pandas as pd
from datetime import datetime, date
from testwebsite.models import TimeStamps, User, ExpenseTransactions, IncomeTransactions
from testwebsite import db
from sqlalchemy.exc import SQLAlchemyError as Err


# resets all transactions for all users once the end of the month comes
# todo throws error:SAWarning: Multiple rows returned with uselist=False for lazily-loaded attribute
#  'ExpenseTransactions.exp_category_name'
# 1) create excel or CSV file for previous months txns
# 2) clear all txns for month
# 3) update expense categories to new month

# Preps the object data for writing to Excel sheet
def excel_prep(sql_obj):
    row_data = []
    for obj in sql_obj:
        val_list = [obj.__dict__['date'][0:10],
                    obj.__dict__['category'],
                    obj.__dict__['amount'],
                    obj.__dict__['description']]
        row_data.append(val_list)
    return row_data


def check_time_stamps(current_user):
    data = db.session.query(TimeStamps).filter(TimeStamps.user_id == current_user.id).all()[-1]
    # if there was a timestamp created today by "remove_transactions" then return
    if datetime.utcnow().day == data.timestamp.day:
        return
    # if today is start of the month then call remove_transactions
    elif calendar.monthrange(datetime.utcnow().year, datetime.utcnow().month)[0] == data.timestamp.day:
        remove_transactions('expense')
        remove_transactions('income')


def remove_transactions(key):
    stmt = db.session.query(User).all()
    for user in stmt:
        if key == 'expense':
            txn = db.session.query(ExpenseTransactions). \
                filter(ExpenseTransactions.user_id == user.id).all()
            for tx in txn:
                try:
                    db.session.delete(tx)
                    db.session.commit()
                    stmt = TimeStamps(timestamp=datetime.utcnow(), user_id=user.id)
                    db.session.add(stmt)
                    db.session.commit()
                    print(f"{user}: Transactions Cleared!")
                    return
                except Err as err:
                    print(f"SQL Error: {err}")
                    return
        else:
            txn = db.session.query(IncomeTransactions). \
                filter(IncomeTransactions.user_id == user.id).all()
            for tx in txn:
                try:
                    db.session.delete(tx)
                    db.session.commit()
                    stmt = TimeStamps(timestamp=datetime.utcnow(), user_id=user.id)
                    db.session.add(stmt)
                    db.session.commit()
                    print(f"{user}: Transactions Cleared!")
                    return
                except Err as err:
                    print(f"SQL Error: {err}")
                    return


def monthly_reset(u):
    # CREATE FILE FOR ALL TRANSACTIONS
    filename = f'Logs/Transaction Logs/{u.username}_october.xlsx'
    column_names = ["Date", "Category", "Amount", "Description"]
    sql_object = db.session.query(ExpenseTransactions).filter(ExpenseTransactions.user_id == 1).all()
    expense_obj = excel_prep(sql_object)
    sql_object2 = db.session.query(IncomeTransactions).filter(IncomeTransactions.user_id == 1).all()
    income_obj = excel_prep(sql_object2)
    expense_df = pd.DataFrame(data=expense_obj, columns=column_names)
    income_df = pd.DataFrame(data=income_obj, columns=column_names)
    inc_sheet = f"{date.today().year}_{str(date.today().month)[0:2]}_Income"
    exp_sheet = f"{date.today().year}_{str(date.today().month)[0:2]}_Expense"
    transaction_sheets = {inc_sheet: income_df, exp_sheet: expense_df}
    writer = pd.ExcelWriter(filename)
    for sheet_name in transaction_sheets.keys():
        transaction_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
    # CLEAR ALL TRANSACTIONS FOR ALL USERS
    remove_transactions('expense')
    remove_transactions('income')
    return
