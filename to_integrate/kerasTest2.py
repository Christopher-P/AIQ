import numpy as np
import gym
import csv
import io

from statistics import * 

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, Adagrad, Adadelta, SGD
from keras.callbacks import Callback
from keras.models import load_model

import keras.backend as K
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory

from random import *

import threading


		
#https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
def flatten(l):
	flat_list = [item for sublist in l for item in sublist]
	return flat_list

def genRPM():
	rpm = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
	
	#We have three variables in each Matrix
	for i in range(0,3):
		#Start var at a random type (not always blue to start)
		tempVar = randint(0,2) / 2

		#Not always increment by type (not blue -> red always)
		if randint(0,1) == 1:
			menter = -0.5
		else:
			menter = 0.5
		
		#Change all columns (across a row it is the same)
		if randint(0,1) == 1:
			for j in range(0,3):
				#1.1 used to set 1.5 -> 0 so possible choice becomes 0, 0.5, 1.0
				rpm[0 + 3*j][i] = (tempVar + (j * menter))
				rpm[1 + 3*j][i] = (tempVar + (j * menter))
				rpm[2 + 3*j][i] = (tempVar + (j * menter))


		#Change all rows
		else:
			for j in range(0,3):
				rpm[0 + j][i] = (tempVar + (j * menter))
				rpm[3 + j][i] = (tempVar + (j * menter))
				rpm[6 + j][i] = (tempVar + (j * menter))
				
		for a in rpm:
			for ind, b in enumerate(a):
				if b == 2.0:
					a[ind] = 0.5
				if b == 1.5:
					a[ind] = 0.0
				if b == -0.5:
					a[ind] = 1.0
				if b == -1.0:
					a[ind] = 0.5
				if b == -1.5:
					a[ind] = 0.0
				
	return rpm
	
def genRPMSet(amount):
	info = []
	solution = []
	rpms = []
	for i in range(0, amount):
		rpm = genRPM()
		if rpm not in rpms:
			rpms.append(rpm)
			#[0:8] because 8 is not included
			info.append(flatten(rpm[0:8]))
			solution.append(rpm[8])
	return (info, solution)

def scoreRPM(x, y):
	runningScore = 0
	maxScore = len(x) * 3
	
	for set, i in enumerate(x):
		i = i[0]

		#Copy prediction data
		tmpVal = i
		
		#Classify data based on closest prediction
		for ind,val in enumerate(tmpVal):
			
			if val < (1/3):
				tmpVal[ind] = 0.0
			elif val < (2/3) and val >= (1/3):
				tmpVal[ind] = 0.5
			else:
				tmpVal[ind] = 1.0
				
		for ind, j in enumerate(i):
			if j == y[set][0][ind]:
				runningScore += 1
				
	return runningScore / maxScore
	
def getSmallModel():
	model = Sequential()
	model.add(Dense(16, input_shape=(1,24)))
	model.add(Dense(16))
	model.add(Activation('relu'))
	model.add(Dense(16))
	model.add(Activation('relu'))
	model.add(Dense(16))
	model.add(Activation('relu'))
	model.add(Dense(3))
	model.add(Activation('relu'))
	return model
	
def getLargeModel():
	model = Sequential()
	model.add(Dense(1600, input_shape=(1,24)))
	model.add(Dense(800))
	model.add(Activation('relu'))
	model.add(Dense(400))
	model.add(Activation('relu'))
	model.add(Dense(100))
	model.add(Activation('relu'))
	model.add(Dense(3))
	model.add(Activation('relu'))
	return model



SaveFileName = "2_rpm_train_amount.csv"

x,y = genRPMSet(10000)
for ind, val in enumerate(x):
	dodo = []
	dodo.append(val)
	x[ind] = dodo
	
for ind, val in enumerate(y):
	dodo = []
	dodo.append(val)
	y[ind] = dodo

trainValue =int(0.9 * len(x))
testValue = int(0.1 * len(x))
	
x_train, x_test = x[:trainValue], x[testValue:]
y_train, y_test = y[:trainValue], y[testValue:]



for prop in range(0,31):
	results = []
	results.append(prop*10)
	
	#propVal = int(prop / 100 * len(x_train))
	for retrained in range(0,5):

		#----------------------- \/ RPM \/ -------------------------#
		
		#Same loss and optimizer as cartpole

		model = Sequential()
		model.add(Dense(16, input_shape=(1,24)))
		model.add(Dense(16))
		model.add(Activation('relu'))
		model.add(Dense(16))
		model.add(Activation('relu'))
		model.add(Dense(16))
		model.add(Activation('relu'))
		model.add(Dense(3))
		model.add(Activation('relu'))
		
		model.compile(loss='mse', optimizer='sgd')
		#model.fit(x[:propVal], y[:propVal], epochs = 10*prop, batch_size=32, verbose = 1)
		model.fit(x_train, y_train, epochs = 10*prop, batch_size=32, verbose = 1)

		#------------------------------------Evaluation RPM
		preds = model.predict(x_test, verbose=0)
		score = scoreRPM(preds, y_test)
		results.append(score)
		
		

				
	with open(SaveFileName, 'a', newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		spamwriter.writerow(results)



