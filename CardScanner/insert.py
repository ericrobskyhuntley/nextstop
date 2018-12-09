import psycopg2
import os
import json
from CardScanner import PSQL_PASSWORD

def insert_response():
    sql = """
    INSERT INTO survey_response (id, q_id, survey_id, age, gender, home, zip_code, front, back, timestamp, free_q_id, free_resp)
    SELECT cast(data->>'id' as UUID) AS id,
    cast(data->>'q' as int)  AS q_id,
    cast(data->>'survey_id' as INT) AS survey_id,
    data->>'age' as age,
    data->>'gender' as gender,
    data->>'home' as home,
    data->>'zip_code' as zip_code,
    data->>'front' as front,
    data->>'back' as back,
    cast(data->>'timestamp' as timestamp) as timestamp,
    cast(data->>'free_q_id' as int) as free_q_id,
    data->>'free_resp' as free_resp
    FROM pushjson
    WHERE ingested_at > now() - interval '1 day';

    INSERT INTO survey_response_a (response_id, answer_id)
    SELECT cast(data->>'id' as UUID) AS response_id, cast(jsonb_array_elements_text(data->'a_id') as int) AS answer_id
    FROM pushjson
    WHERE ingested_at > now() - interval '1 day';
    """
    try:
        conn = psycopg2.connect(host="ehuntley.media.mit.edu", database="nextstop", user="ehuntley", password=PSQL_PASSWORD)
        cur = conn.cursor()
        cur.execute(sql, )
        print('hi')
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if(conn):
            cur.close()
            conn.close()
            print("Closed")
