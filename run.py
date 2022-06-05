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

def init():
    """initialize a database to store expenditures"""
    conn = db.connect("expenses.db")
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
    conn.commit()
    cur.close()
    conn.close()

def log(amount, category, message=""):
    """
    logs the expenditure in the database
    amount: number
    category: str
    message: (optional) str
    """
    date = str(datetime.now())
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    sql = f"""
        INSERT into expenses values (
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

def view(category=None):
    """
    this functions allows the user to get all entries from the database
    when a existing category is given this functions gives back the expenses for this category
    """
    conn = db.connect("expenses.db")
    cur = conn.cursor()
    if category:
        sql = f"""
            select * from expenses where category = \"{category}\"
            """
    else:
        sql = "select * from expenses"

    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def main():
    print("Expense tracker...start your financial journey now!")
    init()
    # test query
    #log(120, "transport", "commuting to work")
    print(view())


if __name__ == "__main__":
    main()