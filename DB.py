import sqlite3 as sql_l


class DB:
    def __init__(self, how_db: str):
        try:
            self.sql = sql_l.connect(how_db)
            self.cur = self.sql.cursor()
        except:
            print("Ошибка подсоединения к базе данных")

    def INSERT(self, TABLE, DATA_VALUES, DATA_FOR_INSERT):
        sql = F"INSERT INTO {TABLE} VALUES{DATA_VALUES}"
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
    if data:
        return 1
    else:
        return 0


def add_user(id_user, true_name, sex, nic, photo, description, sex_poisc):
    db = DB("Clop.db")
    db.INSERT("user", "(?, ?, ?, ?, ?, ?, ?)", [(id_user, true_name, sex, nic, photo, description, sex_poisc)])
