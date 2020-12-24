###########################################################################
# This the database file for connecting to                                #
# database. PostgresSQL is being used along with                          #
#                                                                         #
# psycopg2: python module for interacting with                            #
#           PostgresSQL                                                   #
#                                                                         #
# Database Schema:                                                        #
# Databse Name: search_history                                            #
#  ---------------------------------------------------------------------- #
# |(user_id varchar(256) | keyword varchar(256) | search_time timestamp)| #
# ----------------------------------------------------------------------  #
###########################################################################

import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # loads values from env file

DATABASE_URL = os.environ['DATABASE_URL']

def create_db_connection():
    conn = psycopg2.connect(host='ec2-34-204-121-199.compute-1.amazonaws.com',
                            port=5432,
                            user=os.getenv('DB_USER'),
                            password=os.getenv('DB_PASS'),
                            database='dfgi7dou33g0p5',
                            sslmode='allow'
                            )
    return conn


def post_search_data(user_id, keyword):
    connection = create_db_connection()
    sql_cursor = connection.cursor()

    # adding timestamp so that I can get same query saved to the database
    sql_cursor.execute("INSERT INTO public.search_history VALUES('{}', '{}', '{}')".format(
        user_id, keyword, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    connection.commit()
    connection.close()


def get_search_data(user_id, keyword):
    connection = create_db_connection()
    sql_cursor = connection.cursor()

    # getting search history for the keyword
    sql_cursor.execute(
        "SELECT * FROM public.search_history WHERE user_id = '{}' AND keyword LIKE '%".format(user_id) + keyword + "%'")

    results = sql_cursor.fetchall()
    connection.close()

    return results
