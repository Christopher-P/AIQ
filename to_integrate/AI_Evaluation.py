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


from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory

from random import *


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
		

		
#https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
def flatten(l):
	flat_list = [item for sublist in l for item in sublist]
	return flat_list

def genRPM():
	rpm = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
	
	#We have three variables in each Matrix
	for i in range(0,3):
		#Start var at a random type (not always blue to start)
		tempVar = randint(0,2) / 3
	
		#Not always increment by type (not blue -> red always)
		if randint(0,1) == 1:
			menter = -1/3
		else:
			menter = 1/3
		
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
	for i in range(0, amount):
		rpm = genRPM()
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

Names = ['L_CART_AI.h5', 'L_RPM_AI.h5', 'L_MIXED_AI.h5']	
	
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

		
with open('results.csv', 'a', newline='') as csvfile:
	mywriter = csv.writer(csvfile)
	mywriter.writerow(results)



for retrained in range(0, 10):
	#------------------------ \/ Cart \/ ----------------------#
	if train_cart:
		ep_limit = 5000
		
		
		env = gym.make('CartPole-v0')
		np.random.seed(14372098)
		env.seed(14372098)

		nb_actions = env.action_space.n
		memory = EpisodeParameterMemory(limit=1000, window_length=1)

		model = getLargeModel()
		cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
					   batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
		cem.compile()
		cem.fit(env, nb_steps=10000000000, visualize=False, verbose=2, nb_episodes=ep_limit)

		model.save('L_CART_AI.h5')

	#----------------------- \/ RPM \/ -------------------------#
	if train_rpm:
		#Same loss and optimizer as cartpole
		x,y = genRPMSet(10000)


		for ind, val in enumerate(x):
			dodo = []
			dodo.append(val)
			x[ind] = dodo
			
		for ind, val in enumerate(y):
			dodo = []
			dodo.append(val)
			y[ind] = dodo


		model = getLargeModel()
		model.compile(loss='mse', optimizer=SGD(lr=0.03, momentum=0.0, decay=0.0, nesterov=False))
		model.fit(x, y, epochs = 100, verbose = 1)

		model.save('L_RPM_AI.h5')



	#---------------------  \/  Mixed \/ -----------------------------#
	if train_mixed:
		#Number of times to train on both envs
		iterations = 100

		#Number of RPMs to train on
		RPM_number = 100

		#Number of CartPoles steps to train on (~10 per worst game, 200 per best game)
		Cart_number = 100

		env = gym.make('CartPole-v0')
		np.random.seed(14372098)
		env.seed(14372098)

		nb_actions = env.action_space.n

		# Option 2: deep network
		model = Sequential()
		model.add(Dense(160, input_shape=(1,24)))
		model.add(Dense(160))
		model.add(Activation('relu'))
		model.add(Dense(160))
		model.add(Activation('relu'))
		model.add(Dense(160))
		model.add(Activation('relu'))
		model.add(Dense(3))
		model.add(Activation('softmax'))
		
		
		model = getLargeModel()
		cem = CEMAgent(model=model, nb_actions=nb_actions, memory=EpisodeParameterMemory(limit=100, window_length=1),
				   batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
		cem.compile()

		for k in range(0,iterations):
			#Cart Part
			cem.fit(env, nb_steps=Cart_number*2000, visualize=False, verbose=2, nb_episodes=Cart_number)

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

			model.fit(x, y, epochs = 1, verbose = 1)
			
		model.save('L_MIXED_AI.h5')
		
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

			
	with open('results.csv', 'a', newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		spamwriter.writerow(results)
	
print(results)


