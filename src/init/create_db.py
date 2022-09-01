#!/usr/bin/env python3

import sqlite3


def create_db():
    """Creates the database"""
    db = 'database.db'
    table = """CREATE TABLE IF NOT EXISTS "air_quality" (
        "sl" INTEGER PRIMARY KEY AUTOINCREMENT,
        "date" TEXT NOT NULL,
        "time" TEXT NOT NULL,
        "aqi" INTEGER NOT NULL
    );"""
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(table)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    create_db()
