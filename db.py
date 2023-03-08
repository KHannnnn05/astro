import sqlite3

with sqlite3.connect('db.sqlite3', check_same_thread=False) as con:
    cur = con.cursor()

def create_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS search
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        full_name TEXT,
        date TEXT,
        address TEXT,
        time_zone TEXT,
        rezult BLOB DEFAUL NULL
    );""")
    con.commit()

def add_main_data(full_name, date, address, time_zone):
    create_db()
    id = cur.execute("INSERT INTO search (full_name, date, address, time_zone) VALUES (?, ?, ?, ?) RETURNING id;", (full_name, date, address, time_zone, )).fetchone()[0]
    con.commit()
    return id

def add_rezult_data(id, rez):
    cur.execute(f'UPDATE search SET rezult = ? WHERE id == {id};', (str(rez), ))
    con.commit()

def get_rezult(id):
    rez = cur.execute(f"SELECT rezult FROM search WHERE id == {id}").fetchone()[0]
    return rez

def get_parse_data():
    data = cur.execute('SELECT * FROM search WHERE rezult is NULL').fetchall()
    return data