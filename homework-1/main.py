"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv


def csv_rider(file: str) -> list:
    """
    Записываем данные в список кортежей
    для дальнейшей записи в базу данных
    """
    list_data = []
    with open(file, 'r', newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')

        for row in filereader:

            tuple_row = ()
            for data in row:
                tuple_row += (data,)

            list_data.append(tuple_row)
        list_data.pop(0)  # удалить заголовки таблиц
        return list_data


def len_row(rows: list) -> str:
    """
    получаем колличество элементов
    для добавления в SQL таблицу
    """
    words_in_row = ('%s, ' * len(rows[0]))
    return words_in_row[0:-2]


def sql_writer(sql_tab_name: str, row_data: list) -> None:
    """
    Записываем данные в SQL таблицу
    """
    with psycopg2.connect(
            host='localhost',
            database='north',
            user='postgres',
            password='5482'
    ) as conn:
        with conn.cursor() as cur:
            cur.executemany(f'INSERT INTO {sql_tab_name} VALUES ({len_row(row_data)})', row_data)

    conn.close()


employees = csv_rider('north_data/employees_data.csv')
customers = csv_rider('north_data/customers_data.csv')
orders = csv_rider('north_data/orders_data.csv')

sql_writer('employees', employees)
sql_writer('customers', customers)
sql_writer('orders', orders)
