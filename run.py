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

def log(amount, category, message="", date=None):
    """
    logs the expenditure in the database
    amount: number
    category: str
    message: (optional) str
    """
    if not date:
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
    init()
    while True:
        print("Expense tracker...start your financial journey now!")
        print("Enter key to select an option:")
        print("\t (l) for log a new entry.")
        print("\t (v) to view your entries.")
        print("\t (q) to quit")

        selection = input(">>>")

        if selection.lower() == "q":
            break
        elif selection.lower() == "l":
            amount = float(input("How much did you spent?"))
            category = str(input("Which category do you want to log?"))
            message = str(input("Enter a message for your entry."))
            # test query
            log(amount, category, message)
            # log(125.47, "food", "dinner at a restaurant")
        elif selection.lower() == "v":
            results = view()
            for result in results:
                print(result)
            input("Press Enter to get back to the main menu.")


if __name__ == "__main__":
    main()