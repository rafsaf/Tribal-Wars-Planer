from plemiona_pliki.db_pool import db_pool


def get_tribe(number):
    conn = db_pool.getconn()
    cur = conn.cursor()
    cur.execute('select tag from data_tribe where world=%s;', [number])
    tribes = [(i[0], i[0]) for i in cur.fetchall()]
    conn.commit()
    cur.close()
    db_pool.putconn(conn)
    return tribes


if __name__ == "__main__":
    print(get_tribe(150))

