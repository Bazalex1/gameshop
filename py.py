import sqlite3

# Укажите путь к вашей базе данных
db_path = "db.sqlite3"

# Подключение к базе данных
conn = sqlite3.connect(db_path)

# Создание курсора
cursor = conn.cursor()

# Выполнение SQL-запроса (замените "table_name" на имя вашей таблицы)
cursor.execute("SELECT * FROM shop_game")

# Получение данных
rows = cursor.fetchall()

# Вывод данных
for row in rows:
    print(row)

# Закрытие соединения
conn.close()
