"""This class holds every relevant data from the database and can preform some basic analysis"""

import sqlite3 as db
import pandas as pd

class Analyzer():
    def __init__(self, database_path, cf_type):
        self.df = self.get_data(database_path=database_path, cf_type=cf_type)
        self.df.set_index('date', inplace=True)

    def get_data(self, database_path, cf_type):
        """"""
        conn = db.connect(database_path)
        sql = f"""
                select * from {cf_type}
                """
        df = pd.read_sql_query(sql, conn)
        df['date'] = pd.to_datetime(df['date'])
        conn.close()
        return df

    def sum_values_for_time_period(self, start_data, end_date='current_date'):
        """
        sums all values for a given time period
        if no end_date is given the default value is today
        """
        pass

if __name__ == "__main__":
    analyzer = Analyzer(database_path="db.db", cf_type='expenses')
    print(analyzer.df)
    print(analyzer.df.groupby(pd.Grouper(freq="M")).sum())
