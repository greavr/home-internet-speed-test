import sqlite3
import datetime 
import backend as app
import logging
import os

localDB = "speed.db"
main_conn = None
#Set OS
os.environ["localDB"] = os.getcwd() + "\\" + localDB

# TABLE STRUCTURE FOR STATS
sql_create_stats_table = """ CREATE TABLE IF NOT EXISTS stats (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        time_stamp TEXT NOT NULL,
                                        upload INTEGER,
                                        download INTEGER,
                                        ping_avg INTEGER
                                    ); """

sql_create_ping_table = """ CREATE TABLE IF NOT EXISTS ping_stats (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        time_stamp TEXT NOT NULL,
                                        ping INTEGER
                                    );   """

sql_create_notification_table = """ CREATE TABLE IF NOT EXISTS notification (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        time_stamp TEXT NOT NULL,
                                        event_Title TEXT,
                                        event_Value TEXT
                                    );   """


# Function create a new table
def create_table(conn, create_table_sql, table_name):
    try:
        logging.debug("Creating table {}".format(table_name))
        cur = conn.cursor()
        cur.execute(create_table_sql)

    except sqlite3.Error as e:
        print(e)

# Function to create connection
def create_connection(db_file = localDB):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to return all rows quickly
def QuickSearch():
        # Create Connection to local DB
    main_conn = create_connection()
    # Check that DB exists and table exists
    if main_conn is not None:
        logging.debug("Connected To DB For Quick Search")
        cur = main_conn.cursor()
        cur.execute("SELECT * FROM ping_stats ORDER BY time_stamp DESC LIMIT 5 ")

        rows = cur.fetchall()

        return rows


# Function to save Values to local DB
def SaveValue(Ping,UploadSpeed="",DownloadSpeed=""):
    # Create Connection to local DB
    try:
        main_conn = create_connection()
        cValues = (str(datetime.datetime.now()), UploadSpeed, DownloadSpeed, Ping)

        # Check that DB exists and table exists
        if main_conn is not None:
            logging.debug("Connected To DB For Save Results")
            # Set Cursor Position
            cur = main_conn.cursor()
            sql = ''' INSERT INTO stats(time_stamp,upload,download,ping_avg) VALUES(?,?,?,?) '''
            cur.execute(sql, cValues)

            #Commit to DB
            main_conn.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (main_conn):
            main_conn.close()
            

# Function to just save ping results
def SavePing(PingResult):
     # Create Connection to local DB
    try:
        main_conn = create_connection()
        cValues = (str(datetime.datetime.now()), PingResult)

        # Check that DB exists and table exists
        if main_conn is not None:
            logging.debug("Connected To DB For Save Ping Results")
            # Set Cursor Position
            cur = main_conn.cursor()
            sql = ''' INSERT INTO ping_stats(time_stamp,ping) VALUES(?,?) '''
            cur.execute(sql, cValues)

            #Commit to DB
            main_conn.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (main_conn):
            main_conn.close()

#Function to toggle full speed test
def SetNotification(setText,setValue):
     # Create Connection to local DB
    try:
        main_conn = create_connection()
        NotificationName = setText
        NotificaionValue = setValue
        cValues = (str(datetime.datetime.now()), NotificationName, NotificaionValue)

        # Check that DB exists and table exists
        if main_conn is not None:
            logging.debug("Deleting Previous Notification(s)")
            # Set Cursor Position
            cur = main_conn.cursor()
            cur.execute(' delete from notification Where event_Title = ?',(NotificationName,))

            logging.debug("Set New Notification")
            cur = main_conn.cursor()
            sql = ''' INSERT INTO notification(time_stamp,event_Title,event_Value) VALUES(?,?,?) '''
            cur.execute(sql, cValues)

            #Commit to DB
            main_conn.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (main_conn):
            main_conn.close()

# Function to 
def CreateConn():
    try:
        # Create Connection to local DB
        main_conn = create_connection()
        # create projects table
        create_table(main_conn, sql_create_stats_table, "Stats")
        create_table(main_conn, sql_create_ping_table, "Ping")
        create_table(main_conn, sql_create_notification_table, "Notifications")
    except sqlite3.Error as error:
        print("Failed to connect", error)

