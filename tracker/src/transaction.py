"""Transaction file"""

import sqlite3
import os

ITEM_NAME = 'item #'


def to_dict(value):
    ''' t is a tuple (id,[item #],amount,category,date, description)'''
    transactions = {}
    if len(value) == 6:
        transactions = {'id': value[0], ITEM_NAME: value[1], 'amount': value[2],
                        'category': value[3], 'date': value[4], 'description': value[5]}
    else:
        transactions = {ITEM_NAME: value[0], 'time': value[1], 'total': value[2]}
    return transactions


class Transaction():
    """Transaction class"""

    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()
        self.filename = filename

        self.cur.execute('''CREATE TABLE IF NOT EXISTS transactions
            (id INTEGER PRIMARY KEY,
            [item #] VARCHAR,
            amount INTEGER,
            category TEXT,
            date DATE,
            description TEXT)''')
        self.conn.commit()
        self.conn.close()

    def select_all(self):
        ''' return all of the transaction as a list of dicts.'''
        return self.run_query("SELECT * from transactions")

    def select_where(self, where=None):
        ''' return all of the transaction where ...'''
        query = "SELECT * FROM transactions"
        if where is not None:
            query += f" WHERE {where}"
        return self.run_query(query)

    def add(self, dict_data):
        """Add new transaction to transaction database"""
        query = """INSERT INTO transactions(id, [item #], amount, category, date, description)
                VALUES (?, ?, ?, ?, ?, ?)"""
        params = (dict_data['id'],
                  dict_data[ITEM_NAME],
                  dict_data['amount'],
                  dict_data['category'],
                  dict_data['date'],
                  dict_data['description'])
        self.run_query(query, params)

    def delete(self, identity):
        ''' delete a transaction '''
        return self.run_query("DELETE FROM transactions WHERE id=(?)", (identity,))

    def update(self, dict_data):
        """update a transaction where id=?"""
        query = """UPDATE transactions SET [item #] = ?,
                amount=?, category=?, date=?, description=? WHERE id=?"""
        params = (dict_data[ITEM_NAME],
                  dict_data['amount'],
                  dict_data['category'],
                  dict_data['date'],
                  dict_data['description'],
                  dict_data['id'])
        return self.run_query(query, params)

    def summarize(self, by_time):
        """summarize transactions by date, month, year or category"""
        if by_time == "date":
            query = """SELECT [item #], strftime('%d', date) AS day,
                SUM(amount) as total FROM transactions GROUP BY date"""
        elif by_time == "month":
            query = """SELECT [item #], strftime('%m', date) AS month, SUM(amount) as total
                    FROM transactions GROUP BY month"""
        elif by_time == "year":
            query = """SELECT [item #], strftime('%Y', date) AS year, SUM(amount) as total
                    FROM transactions GROUP BY year"""
        elif by_time == "category":
            query = """SELECT category, [item #], SUM(amount)
                as total FROM transactions GROUP BY category"""
        else:
            raise ValueError(f"Invalid 'by' parameter: {by_time}.")
        return self.run_query(query)

    def run_query(self, query, tuple_data=()):
        """run SQL query"""
        con = sqlite3.connect(os.curdir + '/' + self.filename)
        cur = con.cursor()
        cur.execute(query, tuple_data)
        tuples = cur.fetchall()
        con.commit()
        con.close()
        return [to_dict(t) for t in tuples]
