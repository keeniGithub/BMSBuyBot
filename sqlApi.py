import sqlite3

sql = sqlite3.connect('data.db',  check_same_thread=False)
db = sql.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS usersnick
             (id INTEGER PRIMARY KEY, nickname TEXT)''')

sql.commit()

def select_nick_from_db(id):
    db.execute("SELECT nickname FROM usersnick WHERE id=?", (id,))
    nick = db.fetchone()[0]

    if not nick:
        return None
    else:
        return nick
    
def add_to_db(id, nickname):
    db.execute("INSERT OR REPLACE INTO usersnick (id, nickname) VALUES (?, ?)", (id, nickname,))
    sql.commit()
    return True
