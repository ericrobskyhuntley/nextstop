import psycopg2
import os
import json
from . import PSQL_PASSWORD

def push_json(filename):
    # sql = "COPY pushjson (%s) FROM STDIN;"
    #         data = json.load(f)
    try:
        conn = psycopg2.connect(host="ehuntley.media.mit.edu", database="nextstop", user="ehuntley", password=PSQL_PASSWORD)
        cur = conn.cursor()
        # cur.execute(sql, (json.dumps(data),))
        if filename:
            with open(filename, 'r') as f:
                cur.copy_from(f, 'pushjson', columns=('data'))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()


def insert_response(q_id):
    sql = "INSERT INTO survey_response(q_id) VALUES(%s) RETURNING id;"
    try:
        conn = psycopg2.connect(host="ehuntley.media.mit.edu", database="nextstop", user="ehuntley", password=PSQL_PASSWORD)
        cur = conn.cursor()
        cur.execute(sql, (q_id))
    except:
        conn.close()
