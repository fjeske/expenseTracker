"""this cli tool enables the user to track his/her expenses.

useful features:
- track expenses with category
- add comment
- add date
- get statistics of the expenses (api calls)
- make predictions based on the expense history
- also track income
- track net worth
- make investment projections
- display time to retirement based on expenses income and current net worth
- send a monthly report to a given mail address
"""
import os
import sqlite3 as db
from datetime import datetime

DIR_PATH = os.path.dirname(__file__)

def get_table_name(option):
    """this function gets the cashflow option and returns a str with the table name"""
    if option.lower() == "e":
        cf_type = "expenses"
    elif option.lower() == "i":
        cf_type = "income"
    else:
        raise ValueError("option for cash flow not defined...")

    return cf_type

def init():
    """initialize a database to store expenditures"""
    conn = db.connect(os.path.join(DIR_PATH, "db.db"))
    cur = conn.cursor()
    sql = """
    CREATE TABLE if not exists expenses (
    amount number,
    category string,
    message string,
    date string
    )
    """
    cur.execute(sql)
    sql_2 = """
            CREATE TABLE if not exists income (
            amount number,
            category string,
            message string,
            date string
            )
            """
    cur.execute(sql_2)
    conn.commit()
    cur.close()
    conn.close()

def log(option, amount, category, message="", date=None):
    """
    logs the expenditure in the database
    amount: number
    category: str
    message: (optional) str
    """
    cf_type = get_table_name(option=option)
    if not date:
        date = str(datetime.now())
    conn = db.connect(os.path.join(DIR_PATH, "db.db"))
    cur = conn.cursor()
    sql = f"""
        INSERT into {cf_type} values (
        {amount},
        \"{category}\",
        \"{message}\",
        \"{date}\"
        )
        """
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def view(option, category=None):
    """
    this functions allows the user to get all entries from the database
    when a existing category is given this functions gives back the expenses for this category
    """
    cf_type = get_table_name(option=option)
    conn = db.connect(os.path.join(DIR_PATH, "db.db"))
    cur = conn.cursor()
    if category:
        sql = f"""
            select * from {cf_type} where category = \"{category}\"
            """
    else:
        sql = f"select * from {cf_type}"

    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def main():
    init()
    while True:
        print("Expense tracker...start your financial journey now!")
        print("Enter key to select an option:")
        print("\t (l) for log a new entry.")
        print("\t (v) to view your entries.")
        print("\t (q) to quit")

        selection = input(">>> ")

        if selection.lower() == "q":
            break
        elif selection.lower() == "l":
            print("Select category to log to:")
            print("\t (e) for expenses.")
            print("\t (i) for income.")
            cashflow_type = input(">>> ")

            amount = float(input("Enter the amount: "))
            category = str(input("Which category do you want to log? "))
            message = str(input("Enter a message for your entry. "))
            date = str(input("Enter a date (YYYY-MM-DD) if you want, otherwise today will be entered automatically. "))
            if date.strip() == "":
                log(option=cashflow_type, amount=amount, category=category, message=message)
            else:
                log(option=cashflow_type, amount=amount, category=category, message=message, date=date)
                # log(125.47, "food", "dinner at a restaurant")
        elif selection.lower() == "v":
            print("Select category to view:")
            print("\t (e) for expenses.")
            print("\t (i) for income.")
            cashflow_type = input(">>> ")

            results = view(option=cashflow_type)
            for result in results:
                print(result)
            input("Press Enter to get back to the main menu. ")


if __name__ == "__main__":
    main()