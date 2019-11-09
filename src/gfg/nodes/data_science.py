import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical 

pd.set_option('display.max_rows', 999)
pd.set_option('display.max_columns', 999)
pd.set_option('float_format', '{:f}'.format)
pd.options.mode.chained_assignment = None 

def __get_scaled_features(clean_data_with_fe):
	asis_features = [x for x in clean_data_with_fe.columns if x not in ['customer_id', 'is_newsletter_subscriber']]
	eng_features = [x for x in list(clean_data_with_fe.columns) if x.startswith('X_')]
	features = asis_features + eng_features
	X = clean_data_with_fe[features]

	scaler = MinMaxScaler()
	X_scaled = scaler.fit_transform(X)
	return X_scaled

def cluster(parameters, clean_data_with_fe):
	X_scaled = __get_scaled_features(clean_data_with_fe)

	kmeans = KMeans(n_clusters = parameters['cluster']['n_clusters'], 
                	max_iter = parameters['cluster']['max_iter'], 
                	algorithm = parameters['cluster']['algorithm'], 
                	random_state = parameters['cluster']['random_state'])
	kmeans.fit(X_scaled)

	labels = kmeans.predict(X_scaled)
	clean_data_with_fe['labels'] = labels
	clean_data_with_fe['labels'] = clean_data_with_fe['labels'].map({0: 1, 1: 0})

	return kmeans, clean_data_with_fe

def preprocess_for_classification(clean_data_with_fe_labels):
	clean_data_with_fe_classification = (clean_data_with_fe_labels.join(pd.get_dummies(clean_data_with_fe_labels['is_newsletter_subscriber'], 
                               									 					   prefix = 'newsletter'))
       															  .drop(columns = 'is_newsletter_subscriber'))
	return clean_data_with_fe_classification

def split_train_test(parameters, clean_data_with_fe_classification):
	df = clean_data_with_fe_classification.set_index('customer_id')
	X = df.loc[:,df.columns != 'labels']
	y = df['labels']
	X_train, X_test, y_train, y_test = train_test_split(X, 
														y, 
														test_size = parameters['train_test_split']['test_size'], 
														random_state = parameters['train_test_split']['random_state'])
	scaler = MinMaxScaler()
	scaler.fit(X_train)

	X_train_norm = scaler.transform(X_train)
	X_test_norm = scaler.transform(X_test)
	return scaler, X_train_norm, X_test_norm, y_train, y_test

def train_model(parameters, X_train_norm, X_test_norm, y_train, y_test):
	model = Sequential()
	model.add(Dense(parameters['classifier']['layers']['first']['neurons'], 
					activation= parameters['classifier']['layers']['first']['activation'], 
					input_dim = X_train_norm.shape[1]))
	model.add(Dense(parameters['classifier']['layers']['second']['neurons'], 
					activation= parameters['classifier']['layers']['second']['activation']))
	model.add(Dense(parameters['classifier']['layers']['output']['neurons'], 
					activation= parameters['classifier']['layers']['output']['activation']))

	#sgd = keras.optimizers.SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)

	model.compile(loss = parameters['classifier']['loss'], 
              	  optimizer = parameters['classifier']['optimizer'], 
              	  metrics= [parameters['classifier']['metrics']])

	model.fit(X_train_norm, 
          	  y_train, 
          	  epochs = parameters['classifier']['epochs'], 
          	  batch_size = parameters['classifier']['batch_size'],
          	  validation_split = parameters['classifier']['validation_split'],
          	  verbose = parameters['classifier']['verbose'])

	predicted = model.predict_classes(X_test_norm)
	print('Test Accuracy: ',accuracy_score(y_test, predicted))
	
	return model

def make_predictions(scaler, model, clean_data_with_fe_classification):
	
	X = clean_data_with_fe_classification.loc[:, ~clean_data_with_fe_classification.columns.isin(['customer_id', 'labels'])]
	y = clean_data_with_fe_classification['labels']

	y_pred = model.predict_classes(X)

	submission = pd.DataFrame({'customer_id' : clean_data_with_fe_classification['customer_id'],
                           	   'predictions' : y_pred.reshape((y_pred.shape[0],))})
	return submission
