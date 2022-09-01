#!/usr/bin/env python3

import sqlite3
import datetime


def connection(db):
    """Open database file
    """
    conn = None
    try:
        conn = sqlite3.connect(db)
    except sqlite3.Error as e:
        log = open("/root/AQIndexer/dbErrors.log", "a")
        log.writelines("{0}\n{1}\n\n".format(datetime.datetime.now(), e))
        log.close()
    return conn


def insert(conn, sql, data):
    """Insert fetched AQI data into database
    """
    with conn:
        cur = conn.cursor()
        cur.execute(sql, data)


def retrieve(conn, sql, data):
    """Retrieve specific data from database
    """
    with conn:
        cur = conn.cursor()
        cur.execute(sql, data)
        return cur.fetchall()
