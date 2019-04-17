import os
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from airflow.hooks.base_hook import BaseHook

LOCAL_DIR = '/tmp/'


class BigQueryHook(BaseHook):

    # Hook to connect with BigQueryHook
    def __init__(self, big_query_conn_id='big_query_default', type='client'):

        self.big_query_conn_id = big_query_conn_id
        self.type = type

        # Link to the connection setting
        conn = self.get_connection(big_query_conn_id)

        # Getting Acces ID from connection
        json_credentials = conn.extra_dejson

        self.project_id = conn.extra_dejson['project_id']

        with open(LOCAL_DIR + 'big_query.json', 'w') as fp:
            json.dump(json_credentials, fp)

        if self.type == 'client':
            self.client = bigquery.Client.from_service_account_json(
                LOCAL_DIR + 'big_query.json')

        if self.type == 'credentials':
            self.credentials = service_account.Credentials.from_service_account_file(
                LOCAL_DIR + 'big_query.json',)

        os.remove(LOCAL_DIR + 'big_query.json')
