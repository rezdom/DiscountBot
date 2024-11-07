import sqlite3 as sq

'''
конфиг, который содержит важные ссылки к файлам,
функции и тд
'''

ads = """ЗДЕСЬ МОГЛА БЫТЬ ВАША РЕКЛАМА"""

file_path = [r"source\users_info.db"]

def add_user_id(ID,cur,db): #функция, которая вбивает в бд нового пользователя
    cur.execute(f"SELECT userID FROM users_info")
    if (ID,) in cur.fetchall():
        return "user уже вбит в базу"
    else:
        cur.execute(f"INSERT INTO users_info(code, userID) VALUES (?, ?)",(0, ID))
        db.commit()

def is_admin(ID): #функция, которая проверяет есть ли бан или является админом юзер
    db_user_info = sq.connect(file_path[0])
    cur = db_user_info.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users_info(code INTEGER, userID INTEGER)")
    add_user_id(ID,cur,db_user_info)
    cur.execute(f"SELECT code FROM users_info WHERE userID == {ID}")
    if cur.fetchone()[0] == 1:
        db_user_info.close()
        return True
    elif cur.fetchone()[0] == 2:
        db_user_info.close()
        return 'ban'
    db_user_info.close()
    return False
