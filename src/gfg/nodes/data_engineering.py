import zipfile
import hashlib
import json
import pandas as pd
import numpy as np
from kedro.config import ConfigLoader

def __get_creds():
	conf_paths = ["conf/base", "conf/local"]
	conf_loader = ConfigLoader(conf_paths)
	credentials = conf_loader.get("credentials*", "credentials*/**")
	return credentials

def __decrypt(credentials):
	PASS = credentials['zip']['password']
	hash_object = hashlib.sha256(PASS.encode())
	hex_dig = hash_object.hexdigest()
	return hex_dig

def unzip(PATH = './data/01_raw/test_data.zip'):
	credentials = __get_creds()
	hex_dig = __decrypt(credentials)
	z = zipfile.ZipFile(PATH)
	z.extract('data.json', pwd = hex_dig.encode(), path = './data/01_raw/')
	with open('./data/01_raw/data.json', 'r') as f:
		data = json.load(f)
	return data

def __make_dataframe(json_data):
	df = pd.read_json(json_data[0], orient = 'records')
	return df 

def make_clean(json_data):
	raw_data = __make_dataframe(json_data)
	raw_data['customer_id'] = raw_data['customer_id'].astype(str)
	clean_data = raw_data[(raw_data['coupon_discount_applied'] < 1) &
			 			  (raw_data['coupon_discount_applied'] >= 0)]
	return clean_data

def feature_engineering(clean_data):
	clean_data['X_days_active'] = clean_data['days_since_first_order'] - clean_data['days_since_last_order']

	clean_data['X_order_per_day'] = clean_data['orders'] / clean_data['X_days_active']
	clean_data['X_order_per_day'] = clean_data['X_order_per_day'].replace([np.inf, -np.inf], 0)

	clean_data['X_items_per_order'] = clean_data['items'] / clean_data['orders']
	clean_data['X_avg_rev_per_items_per_order'] = clean_data['revenue'] / clean_data['X_items_per_order']
	clean_data['X_returns_per_order'] = clean_data['returns'] / clean_data['orders']
	clean_data['X_vouchers_per_order'] = clean_data['vouchers'] / clean_data['orders']
	clean_data['X_female_items_per_item'] = clean_data['female_items'] / clean_data['items']

	clean_data['X_waap_per_app'] = clean_data['wapp_items'] / (clean_data['wapp_items'] + clean_data['mapp_items'])
	clean_data['X_wacc_per_acc'] = clean_data['wacc_items'] / (clean_data['wacc_items'] + clean_data['macc_items'])
	clean_data['X_wftw_per_ftw'] = clean_data['wftw_items'] / (clean_data['wftw_items'] + clean_data['mftw_items'])
	clean_data = clean_data.fillna(0) #dangerous, but will run with it for now..
	return clean_data

