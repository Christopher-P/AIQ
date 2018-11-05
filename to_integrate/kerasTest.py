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


#https://github.com/keras-team/keras/issues/114
class EarlyStopping(Callback):
	global losses
	def on_epoch_end(self, epoch, logs={}):
		if logs.get('loss') <= 0.05:
			losses.append(epoch)
			self.model.stop_training = True


#https://keras.io/callbacks/
class ScoreHistory(Callback):
	def on_train_begin(self, logs={}):
		self.scores = []
		self.epis = []
		self.scores.append(0)
		self.epis.append(logs.get('episode'))

	def on_batch_end(self, batch, logs={}):
        #print(logs)
        #exit(0)
		if self.epis[-1] != logs.get('episode'):
			self.epis.append(logs.get('episode'))
			self.scores.append(0)
		elif len(self.scores) > 0:
			self.scores[-1] += 1
			
		if self.scores[-1] >= 190:
			self.model.stop_training = True

class EpisodeScore(Callback):
	global ScoreList
	def on_episode_end(self, episode, episode_logs={}, logs={}):
		ScoreList.append(logs.get('episode_reward'))
		

class BatchWeights(Callback):
	global weightList
	def on_epoch_end(self, batch, logs={}):
		tpd = []
		tld = self.model.get_weights()
		for i in tld:
			for j in i.flatten():
				tpd.append(j.flatten())

		weightList.append(tpd)
		
		
class BatchWeightsCEM(Callback):
	global weightList
	def on_epoch_end(self, batch, logs={}):
		tpd = []
		tld = self.model.get_weights2()
		for i in tld:
			for j in i.flatten():
				tpd.append(j.flatten())

		weightList.append(tpd)
		
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
			menter = -1/2
		else:
			menter = 1/2
		
		#Change all columns (accros a row it is the same)
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
				if b > 1.0:
					a[ind] = 0.0
				if b < 0:
					a[ind] = 1.0
	
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



SaveFileName = "rpm_handicap_percent.csv"
	
for again in range(0,20):
	''''
	with open(SaveFileName, 'a', newline='') as csvfile:
		mywriter = csv.writer(csvfile)
		mywriter.writerow(["Get Weights"])
	'''
	weightList = []
	
	Names = ['RPM_AI.h5']	
		
	train_cart = True
	train_rpm = True
	train_mixed = True


	eval_cart = True
	eval_rpm = True
	eval_mixed = True

	results = []

	#Write a header to the csv
	if eval_cart:
		for i in Names:
			results.append("CART" + "->" + i)

	if eval_rpm:
		for i in Names:
			results.append("RPM" + "->" + i)
		
	if eval_mixed:
		for i in Names:
			results.append("MIXED_RPM" + "->" + i)
			results.append("MIXED_CART" + "->" + i)

			
	with open(SaveFileName, 'a', newline='') as csvfile:
		mywriter = csv.writer(csvfile)
		mywriter.writerow(results)

	Waits = BatchWeights()
	WaitsCEM = BatchWeightsCEM()
	for retrained in range(15, 16):

		#------------------------ \/ Cart \/ ----------------------#
		if train_cart:
			ep_limit = 2000
			
			
			env = gym.make('CartPole-v0')

			nb_actions = env.action_space.n
			memory = EpisodeParameterMemory(limit=1000, window_length=1)

			model = Sequential()
			model.add(Dense(16 - retrained, input_shape=(1,24)))
			model.add(Dense(16 - retrained))
			model.add(Activation('relu'))
			model.add(Dense(16 - retrained))
			model.add(Activation('relu'))
			model.add(Dense(16 - retrained))
			model.add(Activation('relu'))
			model.add(Dense(3))
			model.add(Activation('relu'))
			
			cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
						   batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
			cem.compile()
			cem.fit(env, nb_steps=200*ep_limit, nb_episodes =ep_limit, visualize=False, verbose=1)

			model.save('CART_AI.h5')
			
		#----------------------- \/  \/ -------------------------#
		if train_rpm:
			#Same loss and optimizer as cartpole
			x,y = genRPMSet(500)


			for ind, val in enumerate(x):
				dodo = []
				dodo.append(val)
				x[ind] = dodo
				
			for ind, val in enumerate(y):
				dodo = []
				dodo.append(val)
				y[ind] = dodo

				
			model = Sequential()
			model.add(Dense(16 - retrained, input_shape=(1,24)))
			model.add(Dense(16 - retrained))
			model.add(Activation('relu'))
			model.add(Dense(16 - retrained))
			model.add(Activation('relu'))
			model.add(Dense(16 - retrained))
			model.add(Activation('relu'))
			model.add(Dense(3))
			model.add(Activation('relu'))
			
			model.compile(loss='mse', optimizer='sgd')
			model.fit(x, y, epochs = 1000, batch_size=32, verbose = 1, callbacks=[Waits])

			model.save('RPM_AI.h5')
			'''
			tAr = []
			
			for ind,val in enumerate(weightList):
				if ind < len(weightList) - 1:
					subbed = np.subtract(val, weightList[ind + 1])
					summed = np.sum(subbed)
					tAr.append(np.absolute(summed))
				
			with open('waits.csv', 'a', newline='') as csvfile:
				mywriter = csv.writer(csvfile)
				mywriter.writerow(tAr)

				
			'''
		#---------------------  \/  Mixed \/ -----------------------------#
		if train_mixed:
			#Number of times to train on both envs
			iterations = 100

			#Number of RPMs to train on
			RPM_number = 10000

			#Number of CartPoles steps to train on (~10 per worst game, 200 per best game)
			Cart_number = 100

			env = gym.make('CartPole-v0')
			np.random.seed(14372098)
			env.seed(14372098)

			nb_actions = env.action_space.n
			
			
			model = getSmallModel()
			cem = CEMAgent(model=model, nb_actions=nb_actions, memory=EpisodeParameterMemory(limit=100, window_length=1),
					   batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
			cem.compile()

			for k in range(0,iterations):
				#Cart Part
				cem.fit(env, nb_steps=Cart_number*10, visualize=False, verbose=1, callbacks=[WaitsCEM])

				#RPM Part
				x,y = genRPMSet(RPM_number)


				for ind, val in enumerate(x):
					dodo = []
					dodo.append(val)
					x[ind] = dodo
					
				for ind, val in enumerate(y):
					dodo = []
					dodo.append(val)
					y[ind] = dodo

				model.fit(x, y, epochs = 1, verbose = 1, callbacks=[Waits])
				
			model.save('MIXED_AI.h5')
			

			
		#==========================================Evaluation================================
			
		results = []

		#---------------------------Evaluation CART
		if eval_cart:
			ENV_NAME = 'CartPole-v0'

			ScoreList = []


			# Get the environment and extract the number of actions.
			env = gym.make(ENV_NAME)
			np.random.seed(14372098)
			env.seed(14372098)

			nb_actions = env.action_space.n
			obs_dim = env.observation_space.shape[0]

			for i in Names:
				model = load_model(i)
				memory = EpisodeParameterMemory(limit=1000, window_length=1)
				cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
							   batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
				cem.compile()

				epHistory = EpisodeScore()
				cem.test(env, nb_episodes=100, visualize=False, callbacks=[epHistory]) 
				#results = results + i + "," + ENV_NAME + "," + str(sum(ScoreList)/ len(ScoreList))
				results.append(sum(ScoreList)/ len(ScoreList))
				



		#------------------------------------Evaluation RPM
		if eval_rpm:
			
			x,y = genRPMSet(1000)

			for ind, val in enumerate(x):
				dodo = []
				dodo.append(val)
				x[ind] = dodo
				
			for ind, val in enumerate(y):
				dodo = []
				dodo.append(val)
				y[ind] = dodo

			
			for i in Names:
				model = load_model(i)
				preds = model.predict(x, verbose=0)
				score = scoreRPM(preds,y)
				results.append(score)

		#-----------------------------------Evaluation Mixed
		if eval_mixed:
			env = gym.make('CartPole-v0')
			np.random.seed(14372098)
			env.seed(14372098)
			ScoreList = []
				
			x,y = genRPMSet(100)

			for ind, val in enumerate(x):
				dodo = []
				dodo.append(val)
				x[ind] = dodo
				
			for ind, val in enumerate(y):
				dodo = []
				dodo.append(val)
				y[ind] = dodo

			for i in Names:
				model = load_model(i)
				memory = EpisodeParameterMemory(limit=1000, window_length=1)
				cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
							   batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
				cem.compile()

				epHistory = EpisodeScore()
				cem.test(env, nb_episodes=100, visualize=False, callbacks=[epHistory]) 
				
				
				preds = model.predict(x, verbose=0)
				score = scoreRPM(preds,y)

				#results = results + i + ",Cartpole," + str(sum(ScoreList)/ len(ScoreList)) + ",RPM," + str(score)
				results.append(score)
				results.append(sum(ScoreList)/ len(ScoreList))

				
		with open(SaveFileName, 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile)
			spamwriter.writerow(results)
		
	print(results)


