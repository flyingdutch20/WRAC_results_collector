import os
import sqlite3
import logging


logger = logging.getLogger("Placepot.db")

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect('file:path?mode=rw', uri=True)
        logger.info(f"Connection to SQLite DB {path} successful")
    except sqlite3.DatabaseError as e:
        logger.error(f"The error '{e}' occurred, I am going to create the database")
        connection = create_database(path)
    except sqlite3.Error as e:
        logger.error(f"The error '{e}' occurred, I am stopping")
    return connection

def create_database(path):
    connection = None
    dirs = os.path.split(path)[0]
    if dirs and not os.path.exists(dirs):
        os.makedirs(dirs)
    try:
        connection = sqlite3.connect(path)
        logger.info(f"Database {path} created")
    except sqlite3.Error as e:
        logger.error(f"The error '{e}' occurred, I am stopping")
    else:
        execute_query(connection, create_meeting_table)
        execute_query(connection, create_meeting_index)
        execute_query(connection, create_race_table)
        execute_query(connection, create_race_index)
        execute_query(connection, create_nag_table)
        execute_query(connection, create_nag_index)
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logger.debug("Query executed successfully")
    except sqlite3.Error as e:
        logger.error(f"The error '{e}' occurred")

def execute_read_query(connection, query, all=True):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall() if all else cursor.fetchone()
        return result
    except sqlite3.Error as e:
        logger.error(f"The error '{e}' occurred")

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

create_meeting_index = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_meeting_name_date
ON meeting (name, race_date);
"""

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
    meeting_id INTEGER NOT NULL,
    FOREIGN KEY (meeting_id) REFERENCES meeting (id));
    """

create_race_index = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_race_leg_mtg
ON race (leg, meeting_id);
"""

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
    race_id INTEGER NOT NULL,
    FOREIGN KEY (race_id) REFERENCES race (id));
    """

create_nag_index = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_nag_name_race
ON nag (name, race_id);
"""

