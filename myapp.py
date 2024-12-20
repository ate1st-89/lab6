import sqlite3
import pandas as pd
from flask import Flask, render_template


app = Flask(__name__)


connection  = sqlite3.connect('gifts.db')
table = pd.DataFrame({'ФИО': ["Иванов И.И.", "Петрова А.Ю.", "Иванова Г.Б.", "Федоров В.С.", "Петров С.С.", "Сидоров В.В", "Жеглов П.П.", "Степанов А.М.", "Ушаков С.М.", "Ушакова М.С."],
                      'Подарок': ["Велосипед", "Коньки", "Мяч", "Кросовки", "Робот", "Шахматы", "Биноколь", "Очки", "Телескоп", "Машинка"],
                      'Стоимость': [ 100, 15, 30, 22, 25, 36, 64, 66, 73, 23],
                      "Статус" : ["Куплен", "Куплен","Куплен","Куплен","Не куплен","Куплен","Куплен","Не куплен","Куплен","Не куплен"]})
table
table.to_sql('gifts', connection, index = False, if_exists='replace')

sql = ''' select *
            from gifts
'''
pd.read_sql(sql, connection)


def get_db_connection():
    conn = sqlite3.connect('gifts.db')
    conn.row_factory = sqlite3.Row
    return conn



def check_create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name='gifts'
        """
    )
    exists = cursor.fetchone()
    
    if not exists:
        table.to_sql('gifts', connection, index = False, if_exists='replace')
        conn.commit()
        
        print("Table 'gifts' created.")
    else:
        print("Table 'gifts' already exists.")


# Заполняет базу данных данными, если таблица пустая
def fill_database_if_empty(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM gifts')
    count = cursor.fetchone()[0]
    



# Главная страница
@app.route('/')
def index():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM gifts')
            rows = cursor.fetchall()
            return render_template('index.html', rows=rows)
            
    except sqlite3.Error as e:
        return f"Error fetching data from database: {e}"


if __name__ == '__main__':
    with get_db_connection() as conn:
        check_create_table(conn)
        fill_database_if_empty(conn)
        
    app.run(debug=True)
