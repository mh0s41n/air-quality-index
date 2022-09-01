#!/usr/bin/env python3

import fetcher
import db_helper

import time


def insert_data(i_conn):
    """Insert data to db"""
    d = fetcher.get_data()
    if d is not None:
        date, time = fetcher.get_datetime(d)
        aqi = fetcher.get_aqi(d)
        sql = """INSERT INTO air_quality(date, time, aqi) VALUES(?, ?, ?);"""
        db_helper.insert(i_conn, sql, (date, time, aqi))
        return "Success"
    return "Failure"


def main():
    """main process"""
    retry = 5
    while retry > 0:
        conn = db_helper.connection('/root/AQIndexer/database.db')
        if conn is not None and insert_data(conn) == "Success":
            exit(0)
        time.sleep(1)
        retry -= 1


if __name__ == '__main__':
    main()
