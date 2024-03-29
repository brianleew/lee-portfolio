""" Script To Import Historial Data, Provider Data, And Fake Data """
from typing import List, Dict, Any
from os import getenv, path, getcwd
from argparse import ArgumentParser
from json import load
import pandas as pd
import mysql.connector as msql
from bcrypt import hashpw, gensalt
from dotenv import load_dotenv

PARSER = ArgumentParser(
    prog='import.py',
    description='Imports historical and test data to database'
)
PARSER.add_argument(
    '-c', '--container',
    action='store_true',
    help='Toggle for running in container'
)
ARGS = PARSER.parse_args()
HOST = 'db'

if not ARGS.container:
    HOST = '127.0.0.1'
    load_dotenv(path.join(path.dirname(__file__), '../.env'))

DB_CONFIG = {
    'host': HOST,
    'user': getenv('DB_USER'),
    'password': getenv('DB_PASSWORD'),
    'database': getenv('DB_DATABASE')
}


def get_meters(file:str) -> List[int]:
    """ Get Meter IDs From File """
    col_names = pd.read_csv(file).columns.values.tolist()
    meter_ids = []
    for col in col_names:
        if col.isdigit():
            meter_ids.append(col)
    return meter_ids


def insert_meters(conn:msql.MySQLConnection, file:str) -> None:
    """ Insert Meters Into Table """
    meters = get_meters(file)
    with conn.cursor() as cursor:
        for m_id in meters:
            insert_query = 'INSERT INTO meters (meter_id) VALUES(%s)'
            try:
                cursor.execute(insert_query, (m_id,))
                conn.commit()
                print(f'Successfully Inserted: ({m_id})')
            except msql.Error as e:
                print(f'Failed to insert: ({m_id}) \n {e}')
                if 'Duplicate' in str(e):
                    continue
                exit(1)


def insert_real_data(conn:msql.MySQLConnection, file:str) -> None:
    """ Insert Real Meter Data Into Database """
    meters = get_meters(file)
    ## FORMAT METER DATAFRAMES ##
    meter_dfs = []
    for meter_id in meters:
        use_cols = ['AMI Meter ID', 'date', f'{meter_id}']
        meter_data = pd.read_csv(file, usecols=use_cols)
        meter_data = meter_data.rename(columns={
            'AMI Meter ID': 'start_time',
            'date': 'end_time',
            f'{meter_id}': 'value'
            })
        meter_dfs.append(meter_data.to_dict('records'))

    ## INSERT METER DATA ##
    insert_query = """
        INSERT INTO meter_data (meter_value, meter_id, start_time, end_time)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE meter_value = %s
        """
    # Get nth row from each df and append on meter_id then append to query queue
    for i in range(0, len(meter_dfs[0])):
        query_queue = []
        for j, _ in enumerate(meter_dfs):
            # Get nth row
            start_time = meter_dfs[j][i]['start_time']
            end_time = meter_dfs[j][i]['end_time']
            value = meter_dfs[j][i]['value']
            query_queue.append((value, meters[j], start_time, end_time, value))
        # execute query queue
        with conn.cursor() as cursor:
            for query_values in query_queue:
                try:
                    cursor.execute(insert_query, query_values)
                    conn.commit()
                    print(f'Successfully Inserted: ({query_values})')
                except msql.Error as e:
                    print(f'Failed to insert: ({query_values}) \n {e}')
                    if 'Duplicate' in str(e):
                        continue
                    exit(1)


def insert_pred_data(conn:msql.MySQLConnection, file:str) -> None:
    """ Insert Prediciton Data Into Database """
    ## FORMAT DATAFRAME ##
    use_cols = ['meter_id', 'start_time', 'end_time', 'prediction']
    pred_data = pd.read_csv(file, usecols=use_cols)
    pred_data = pred_data.rename(columns={'prediction': 'value'})
    pred_data = pred_data.to_dict('records')

    ## INSERT PREDICTION DATA ##
    insert_query = """
        INSERT INTO meter_data (meter_id, start_time, end_time, prediction_value)
        VALUES (%s, %s, %s, %s)
        """
    with conn.cursor() as cursor:
        for row in pred_data:
            if row['meter_id'].isdigit() is False:
                continue
            query_values = (row['meter_id'], row['start_time'], row['end_time'], row['value'])
            try:
                cursor.execute(insert_query, query_values)
                conn.commit()
            except msql.Error as e:
                print(f'Failed to insert: ({query_values}) \n {e}')
                if 'Duplicate' in str(e):
                    continue
                else:
                    exit(1)


def load_config(file:str) -> Dict[str, Any]:
    """ Load Provider Config """
    config_path = path.join(path.abspath(getcwd()), file)
    with open(config_path, 'r', encoding='UTF-8') as config_file:
        config = load(config_file)
    return config


def insert_default_org(conn:msql.MySQLConnection, file:str) -> None:
    """ Insert Provider Organization """
    config = load_config(file)
    ## CHECK QUERIES ##
    check_org = 'SELECT * FROM organizations WHERE org_name = %s'
    check_user = 'SELECT * FROM users WHERE email = %s'
    ## INSERT QUERIES ##
    insert_org = 'INSERT INTO organizations (org_name) VALUES (%s)'
    insert_user = """
        INSERT INTO users (email, first_name, last_name, org_id, approval_status)
        VALUES (%s, %s, %s, %s, %s)
        """
    insert_logins = 'INSERT INTO logins (account_id, password_hash) VALUES (%s, %s)'
    ## GET QUERIES ##
    get_org = 'SELECT org_id FROM organizations WHERE org_name = %s'
    get_account = 'SELECT account_id FROM users WHERE email = %s'
    with conn.cursor(dictionary=True) as cursor:
        cursor.execute(check_org, (config['provider_org_name'],))
        result = cursor.fetchone()
        if result is None:
            cursor.execute(insert_org, (config['provider_org_name'],))
            conn.commit()
        cursor.execute(check_user, (config['default_admin_email'],))
        result = cursor.fetchone()
        if result is None:
            cursor.execute(get_org, (config['provider_org_name'],))
            result = cursor.fetchone()
            cursor.execute(insert_user,
                           (config['default_admin_email'],
                            config['default_admin_fname'],
                            config['default_admin_lname'],
                            result['org_id'], 'Admin'
                            ))
            conn.commit()
            cursor.execute(get_account, (config['default_admin_email'],))
            result = cursor.fetchone()
            cursor.execute(insert_logins,
                           (result['account_id'],
                            hashpw(config['default_admin_password'].encode('utf-8'), gensalt())
                            ))
            conn.commit()


def insert_fake_data (conn:msql.MySQLConnection, file:str) -> None:
    """ Insert Fake Data Into Database For Testing """
    with open(file, 'r', encoding='UTF-8') as sql_file:
        sql_data = sql_file.read()
    sql_commands = sql_data.split(';')
    with conn.cursor() as cursor:
        for command in sql_commands:
            try:
                if command.strip() != '':
                    cursor.execute(command)
            except msql.Error as err:
                print(f'Error: {err}')
        conn.commit()


def main() -> None:
    """ Entry Point For Import Script """
    try:
        conn = msql.connect(**DB_CONFIG)
    except msql.Error as err:
        print(f'Error connecting to database: {err}')
        exit(1)
    insert_default_org(conn, 'provider-config.json')
    insert_meters(conn, 'meter-data.csv')
    insert_fake_data(conn, 'fake-data.sql')
    insert_pred_data(conn, 'model_predictions.csv')
    insert_real_data(conn, 'meter-data.csv')


if __name__ == '__main__':
    main()
