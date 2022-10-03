
from os import curdir
import sqlite3


class DataBase:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_company_profile(self, connection: sqlite3.Connection, company):
        try:
            try:
                sql_query = """ INSERT INTO companies(id, name, description, site_url, email) VALUES (?,?,?,?,?); """

                self.cur.execute(sql_query, company)
                connection.commit()
            except sqlite3.OperationalError as OE:
                sql_create_table_query = """CREATE TABLE companies(id INTEGER PRIMARY KEY, name TEXT, description TEXT, site_url TEXT, email TEXT);"""
                self.cur.execute(sql_create_table_query)
                self.create_company_profile(self.conn, company)
            return self.cur.lastrowid
        except Exception as e:
            print(e)

    def create_worker_profile(self, connection: sqlite3.Connection, person: tuple):
        try:
            try:
                sql_query = """INSERT INTO workers(id, name, lastname, age, position, email, tg_url) VALUES (?,?,?,?,?,?,?);"""
                self.cur.execute(sql_query, person)
                connection.commit()
            except sqlite3.OperationalError as OE:
                sql_create_table_query = """CREATE TABLE workers(
                    id INTEGER PRIMARY KEY, name TEXT, lastname TEXT,
                    age INTEGER, position TEXT, email TEXT, tg_url TEXT)"""
                self.cur.execute(sql_create_table_query)
                self.create_worker_profile(self.conn, person)
            return self.cur.lastrowid
        except sqlite3.IntegrityError as IE:
            pass

    # def get_company_last_id(self):
    #     try:
    #         sql_query = """SELECT id FROM companies ORDER BY id DESC LIMIT 1;"""
    #         self.cur.execute(sql_query)
    #         rows = self.cur.fetchall()
    #         for i in rows:
    #             return i
    #     except Exception as e:
    #         print(e)


# def main():
#     db = DataBase()
#     conn = db.conn
#     # db.create_worker_profile(conn, (1, "alexy", "sys", "19", "BACKEND-developer",
#     #                          "qertynon@gmail.com", "https://t.me/vbutkev1ch"))
#     # db.create_company_profile(
#     #     conn, (1, "WyzleDev", "best team", "https://google.com", "qertynon@gmail.com"))
#     for value in db.get_company_last_id():
#         print(int(value))


# if __name__ == "__main__":
#     main()
