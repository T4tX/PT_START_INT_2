import psycopg2
from psycopg2 import Error


def connect_to_postgres():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password='postgres',
            host="127.0.0.1",
            port="5432",
            database="postgres"
        )
        return connection
    except psycopg2.Error as e:
        print(f"Ошибка при подключении к PostgreSQL: {e}")
        return None

# Функция для создания базы данных
def create_database(connection, database_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"База данных {database_name} успешно создана или уже существует.")
        connection.close()
    except Error as e:
        print(f"Ошибка при создании базы данных: {e}")

def drop_table(connection): 
    try: 
        cursor = connection.cursor() 
        create_table_query = """ DROP TABLE int_2; """ 
        cursor.execute(create_table_query) 
        connection.commit() 
        print("Таблица успешно удалена.") 
    except Error as e: 
        print(f"Ошибка при удалении таблицы: {e}") 

def create_table(connection): 
    try: 
        cursor = connection.cursor() 
        create_table_query = """ CREATE TABLE IF NOT EXISTS int_2 ( id SERIAL PRIMARY KEY, 
        Command_hist text, 
        os_info text, 
        Arch text, 
        PreеtName text,
        Version text,
        VersionID text,
        VersionCodename text,
        IDLike text,
        HomeURL text,
        SupportURL text,
        BugReportURL text); """ 
        cursor.execute(create_table_query) 
        connection.commit() 
        print("Таблица успешно создана.") 
    except Error as e: 
        print(f"Ошибка при создании таблицы: {e}")




def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        insert_query = """INSERT INTO int_2 (id, 
        Command_hist, 
        os_info, 
        Arch, 
        PreеtName,
        Version,
        VersionID,
        VersionCodename,
        IDLike,
        HomeURL,
        SupportURL,
        BugReportURL) VALUES (default, '{0}', '{1}','{2}', '{3}','{4}', '{5}','{6}', '{7}','{8}', '{9}','{10}');"""
        cursor.execute(insert_query, data)
        print(20)
        connection.commit()
        print("Данные успешно вставлены.")
    except Error as e:
        print(f"Ошибка при вставке данных: {e}")


def read_data(connection):
    try:
        cursor = connection.cursor()
        select_query = "SELECT * FROM int_2;"
        cursor.execute(select_query)
        records = cursor.fetchall()
        print(2)
        for record in records:
            
            print(record)
    except Error as e:
        print(f"Ошибка при чтении данных: {e}")

if __name__ == "__main__":
    print('debug')