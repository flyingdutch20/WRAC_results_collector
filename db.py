import os
import sqlite3
from sqlite3 import Error

def create_connection(dbname):
    dbdir = "./db"
    if not os.path.isdir(dbdir):
        os.mkdir(dbdir)
    path = '/'.join([dbdir, dbname])
    connection = None
    try:
        connection = sqlite3.connect('file:aaa.db?mode=rw', uri=True)
        print(f"Connection to SQLite DB {path} successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connection("placepot.sqlite")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

#Don't use AUTOINCREMENT on primary key - it will automatically become the rowid

create_meeting_table = """
CREATE TABLE IF NOT EXISTS meeting (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    race_date TEXT NOT NULL,
    start TEXT,
    type TEXT,
    going TEXT,
    stalls TEXT,
    pp_pool REAL,
    pp_div REAL);
    """

execute_query(connection, create_meeting_table)

create_meeting_index = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_meeting_name_date
ON meeting (name, race_date);
"""

execute_query(connection, create_meeting_index)

create_race_table = """
CREATE TABLE IF NOT EXISTS race (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    race_time TEXT,
    race_class TEXT,
    distance TEXT,
    field TEXT,
    verdict TEXT,
    pp_fav REAL,
    pp_fav_perc TEXT,
    pp_nr REAL,
    pp_pool REAL,
    leg INTEGER,
    FOREIGN KEY (meeting_id) REFERENCES meeting (id));
    """

execute_query(connection, create_race_table)

create_race_index = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_race_leg_mtg
ON race (leg, meeting_id);
"""

execute_query(connection, create_race_index)

create_nag_table = """
CREATE TABLE IF NOT EXISTS nag (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    no TEXT,
    draw TEXT,
    lastrun TEXT,
    form TEXT,
    age TEXT,
    jockey TEXT,
    trainer TEXT,
    ts TEXT,
    rpr TEXT,
    rp_comment TEXT,
    rp_forecast TEXT,
    result TEXT,
    sp TEXT,
    fav TEXT,
    race_comment TEXT,
    pp_pool REAL,
    pp_pool_perc TEXT,
    pp_placed INTEGER,
    placed INTEGER,
    rp_forecast_win_chance REAL,
    rp_forecast_place_chance REAL,
    sp_win_chance REAL,
    sp_place_chance REAL,
    FOREIGN KEY (race_id) REFERENCES race (id));
    """

execute_query(connection, create_nag_table)

create_nag_index = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_nag_name_race
ON nag (name, race_id);
"""

execute_query(connection, create_race_index)


create_users = """
INSERT INTO
  users (name, age, gender, nationality)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');
"""
execute_query(connection, create_users)

create_posts = """
INSERT INTO
  posts (title, description, user_id)
VALUES
  ("Happy", "I am feeling very happy today", 1),
  ("Hot Weather", "The weather is very hot today", 2),
  ("Help", "I need some help with my work", 2),
  ("Great News", "I am getting married", 1),
  ("Interesting Game", "It was a fantastic game of tennis", 5),
  ("Party", "Anyone up for a late-night party today?", 3);
"""

execute_query(connection, create_posts)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

select_users = "SELECT * from users"
users = execute_read_query(connection, select_users)

for user in users:
    print(user)

select_users_posts = """
SELECT
    users.id,
    users.name,
    posts.description
FROM
    posts
    INNER JOIN users ON users.id = posts.user_id"""

users_posts = execute_read_query(connection, select_users_posts)

for users_post in users_posts:
    print(users_post)


sqlite_insert_with_param = """INSERT INTO SqliteDb_developers
                          (id, name, email, joining_date, salary)
                          VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (id, name, email, joinDate, salary)
        cursor.execute(sqlite_insert_with_param, data_tuple)




import sqlite3

def insertMultipleRecords(recordList):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_query = """INSERT INTO SqliteDb_developers
                          (id, name, email, joining_date, salary)
                          VALUES (?, ?, ?, ?, ?);"""

        cursor.executemany(sqlite_insert_query, recordList)
        sqliteConnection.commit()
        print("Total", cursor.rowcount, "Records inserted successfully into SqliteDb_developers table")
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert multiple records into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

recordsToInsert = [(4, 'Jos', 'jos@gmail.com', '2019-01-14', 9500),
                  (5, 'Chris', 'chris@gmail.com', '2019-05-15',7600),
                  (6, 'Jonny', 'jonny@gmail.com', '2019-03-27', 8400)]

insertMultipleRecords(recordsToInsert)


