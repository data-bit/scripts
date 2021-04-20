# ========================================================================================
# AUTHOR:   Mitch Alves (idp7116)
# DATE:     2021-01-21
# DESC:     BOOK API
# ========================================================================================

import os
import json
import datetime
import numpy as np
import requests  
import pyodbc
from odbc import odbc
import pandas as pd
from pathlib import Path
from pandas import json_normalize
from requests.exceptions import HTTPError

# Disable Insecure Request Warning from 'requests'
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ========================================================================================
# GLOBALS
# ========================================================================================

# API Config
TOKEN ='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJjZXJiZXJ1cyIsImV4cCI6MzMxNTA3MjI2NTMsImlhdCI6MTYxNDcyMjY1MywiaXNzIjoiY2VyYmVydXMiLCJqdGkiOiI0ZDA2YjZmNy1jMjI5LTRkOTUtODc2MS0yMGU3NmMyYjk1MWIiLCJuYmYiOjE2MTQ3MjI2NTIsInN1YiI6IntcImRlc2NyaXB0aW9uXCI6XCJkaXYgdXNlciBmb3IgZWFzdCBmbG9yaWRhXCIsXCJmYWNpbGl0aWVzXCI6W1wiQ09DTldcIixcIkNPQ1BUXCIsXCJDT0NVSFwiLFwiQ09DV1NcIixcIkNPQ0FUXCIsXCJDT0NLTlwiLFwiQ09DTUhCXCIsXCIuXCIsXCJDT0NQQVwiLFwiQ09DUEZcIixcIkNPQ0hSQVwiLFwiQ09DVldcIixcIkNPQ1FSXCIsXCJDT0NYR1wiLFwiQ09DSkZLXCJdfSIsInR5cCI6ImFjY2VzcyJ9.4Ykyc69Rh6R_QPnTd0j_l23d5XbnEMksFEhzAKytrVH-UpQyZLQBbjkJNBWnTgbhOKLVKfkyqgRML_9snzQpXg'
API_URL = "https://book-api.com/"
HDR = {'Content-Type': 'application/json','Authorization': '{0}'.format(TOKEN)}

# API Parameters
LIST_ITEMS = ['BOOK1','BOOK2']
PARAM = ['']

# Process Timestamp
T_STAMP = str(datetime.datetime.today()).replace(' ','_').replace('-','').replace(':','')[:-9]

# Data Lake 
DATA_LAKE_PATH = f'C:/DATA_LAKE' 


# ========================================================================================
# FUNCTIONS
# ========================================================================================

def path_verification(full_path):
    print(f'=> [Data Lake] Verifying path...')
    # Year verification
    cur_year = str(datetime.datetime.today().year)
    
    # Month verification
    cur_month = 0
    if(datetime.datetime.today().month > 9): 
        cur_month = str(datetime.datetime.today().month) 
    else: 
        cur_month = '0'+ str(datetime.datetime.today().month)
    
    # Day verification
    cur_day = 0
    if(datetime.datetime.today().day > 9): 
        cur_day = str(datetime.datetime.today().day) 
    else: 
        cur_day = '0'+ str(datetime.datetime.today().day)   

    # Path verification and mapping
    path_year = f'{DATA_LAKE_PATH}/{cur_year}/'
    path_month = f'{DATA_LAKE_PATH}/{cur_year}/{cur_month}/'
    path_day = f'{DATA_LAKE_PATH}/{cur_year}/{cur_month}/{cur_day}/'
    paths = [path_year, path_month, path_day]
    for path in paths:
        if Path(path).exists(): 
            print(f'==> {path} already existent.') 
            pass
        else:
            try:
                os.mkdir(path) 
                print(f'==> {path} created successfully.')  
            except OSError as error:  
                print(error) 
    return path_day


def get_facility_data(data_lake, facility, session):
    url = f'{API_URL}{facility}/?{PARAM[0]}'
    response = None
    try:
        response = session.get(url,headers=HDR,verify=False)
        response.raise_for_status()
        if response.status_code == 200:
            print(f'\n => Downloading data from [ {facility} ]')
            df = json_normalize(response.json())
            data = df.astype(str)
            filepath = f'{data_lake}{facility}_{T_STAMP}.csv'
            csv = data.to_csv(filepath,sep=';',index = None,)
            print(f' => [Data Lake] Storing {filepath}')
            load_facility_data(filepath)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error ocurred: {err}")
        return response
    return response


def load_facility_data(filepath):
    df = pd.read_csv(filepath,sep=';',dtype=str).fillna('NULL') 
    df.replace([np.inf, -np.inf], np.nan, inplace = True)

    data = df.T.reindex(['Field1', 'Field2', 'Field3']).T

    db = odbc(None,None)
    sql = 'EXEC dbo.isp_API_Data ?,?,?'

    try:
        print(' => [Database] Executing dbo.isp_API_Data')
        conn = pyodbc.connect(db.connection())
        cursor = conn.cursor()  
        for i, row in data.iterrows():
            #print(tuple(row))
            cursor.execute(sql, tuple(row))
            conn.commit()
        print(' => Data Loaded Successfully!\n')
    except pyodbc.Error as ex:
        print(ex)


# ========================================================================================
# MAIN
# ========================================================================================

data_lake = path_verification(DATA_LAKE_PATH)

with requests.Session() as session:
    for facility in LIST_ITEMS:
        try:
            response = get_facility_data(data_lake, facility, session)   
        except Exception as err:
            print(f"Exception occured: {err}")
            pass