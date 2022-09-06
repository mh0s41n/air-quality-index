#!/usr/bin/env python3

import db_helper

from pathlib import Path


def retrieve_data(r_conn, additional):
    """
    Retrieve data from database
    :param r_conn:
    :param additional:
    :return:
    """
    params = []
    sql = """SELECT * FROM air_quality;"""
    if additional is not None:
        sql = """SELECT * FROM air_quality where date=? and time=?;"""
        params += additional

    return db_helper.retrieve(r_conn, sql, params)


if __name__ == '__main__':
    print("Air Quality Index of Dhaka. See")
    ch = int(input("1. Full database\n2. Select time\nEnter choice: "))

    conn = None
    is_file = Path('database.db').is_file()
    if is_file:
        conn = db_helper.connection('database.db')
    else:
        print('Database Not found')
        exit(0)

    aqi = None
    if ch == 1:
        aqi = retrieve_data(conn, None)
    elif ch == 2:
        date = input("Enter date (yyyy/mm/dd): ")
        time = input("Enter time (hh:mm): ")
        aqi = retrieve_data(conn, (date, time))

    if not aqi:
        print("No data found.")
        exit(0)
    for dt in aqi:
        print(f"{dt[0]}. {dt[1]} {dt[2]}  {dt[3]}")
