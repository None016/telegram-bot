import sqlite3 as sql_l


class DB:
    def __init__(self, how_db: str):
        try:
            self.sql = sql_l.connect(how_db)
            self.cur = self.sql.cursor()
        except:
            print("Ошибка подсоединения к базе данных")

    def INSERT(self, TABLE, DATA_VALUES, DATA_FOR_INSERT):
        sql = F"INSERT INTO {TABLE} VALUES({DATA_VALUES})"
        try:
            self.cur.executemany(sql, DATA_FOR_INSERT)
            self.sql.commit()
        except:
            print("Ошибка добавления данных")

    def SELECT(self, TABLE, IF):
        sql = f"SELECT * FROM {TABLE} WHERE {IF}"
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except:
            print("Ошибка выборки")
            return -1


def check_for_availability_user(id_user):
    db = DB("Clop.db")
    data = db.SELECT("user", f"id == '{id_user}'")
    print(data)
    if data:
        print(1)
        return 1
    else:
        print(0)
        return 0
