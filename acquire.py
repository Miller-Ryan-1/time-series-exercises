import pandas as pd
import requests
import os

def acquire_store_data():
    domain = 'https://python.zgulde.net'

    # Sales
    if os.path.isfile('acquired_sales_data.csv'):
        sales = pd.read_csv('acquired_sales_data.csv', index_col=0)
    else:
        endpoint = '/api/v1/sales'
        page = requests.get(domain + endpoint).json()['payload']['max_page']
        sectionlist=[]

        for i in range(page):
            url = domain + endpoint
            response = requests.get(url)
            sectionlist.extend(response.json()['payload']['sales'])
            endpoint = response.json()['payload']['next_page']
        sales = pd.DataFrame(sectionlist)
        sales.to_csv('acquired_sales_data.csv')

    # Items
    if os.path.isfile('acquired_items_data.csv'):
        items = pd.read_csv('acquired_items_data.csv', index_col=0)
    else:
        endpoint = '/api/v1/items'
        page = requests.get(domain + endpoint).json()['payload']['max_page']
        sectionlist=[]

        for i in range(page):
            url = domain + endpoint
            response = requests.get(url)
            sectionlist.extend(response.json()['payload']['items'])
            endpoint = response.json()['payload']['next_page']
        items = pd.DataFrame(sectionlist)
        items.to_csv('acquired_items_data.csv')

    # Stores
    if os.path.isfile('acquired_stores_data.csv'):
        stores = pd.read_csv('acquired_stores_data.csv', index_col=0)
    else:
        endpoint = '/api/v1/stores'
        page = requests.get(domain + endpoint).json()['payload']['max_page']
        sectionlist=[]

        for i in range(page):
            url = domain + endpoint
            response = requests.get(url)
            sectionlist.extend(response.json()['payload']['stores'])
            endpoint = response.json()['payload']['next_page']
        stores = pd.DataFrame(sectionlist)
        stores.to_csv('acquired_stores_data.csv')

    df = sales.merge(items, how = 'inner', left_on = 'item', right_on = 'item_id').merge(stores, how = 'inner', left_on = 'store', right_on = 'store_id')
    df = df.drop(columns = ['item','store'])
    return df

def OPS_acquire():
    if os.path.isfile('acquired_OPS_Germany.csv'):
        return pd.read_csv('acquired_OPS_Germany.csv', index_col=0)
    else:
        df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
        df.to_csv('acquired_OPS_Germany.csv')
        return df