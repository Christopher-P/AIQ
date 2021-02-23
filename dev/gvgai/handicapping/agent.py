from __future__ import division
import argparse

from PIL import Image
import numpy as np
import gym
import gym_gvgai

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Convolution2D, Permute
from keras.optimizers import Adam
import keras.backend as K

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from rl.callbacks import FileLogger, ModelIntervalCheckpoint

INPUT_SHAPE = (84, 84)
WINDOW_LENGTH = 4


class AtariProcessor(Processor):
    def process_observation(self, observation):
        assert observation.ndim == 3  # (height, width, channel)
        img = Image.fromarray(observation)
        img = img.resize(INPUT_SHAPE).convert('L')  # resize and convert to grayscale
        processed_observation = np.array(img)
        assert processed_observation.shape == INPUT_SHAPE
        return processed_observation.astype('uint8')  # saves storage in experience memory

    def process_state_batch(self, batch):
        # We could perform this processing step in `process_observation`. In this case, however,
        # we would need to store a `float32` array instead, which is 4x more memory intensive than
        # an `uint8` array. This matters if we store 1M observations.
        processed_batch = batch.astype('float32') / 255.
        return processed_batch

    def process_reward(self, reward):
        return np.clip(reward, -1., 1.)


class NeuralNetwork:

    def __init__(self, env, nodes, layers, seed=123):
        # Get the environment and extract the number of actions.
        self.env = env
        self.nodes = nodes
        self.layers = layers

        np.random.seed(seed)

        # Later vars
        self.dqn = None

        return None

    def gen_model(self):
        nb_actions = len(self.env.actions)

        # Next, we build our model. We use the same model that was described by Mnih et al. (2015).
        input_shape = (WINDOW_LENGTH,) + INPUT_SHAPE
        model = Sequential()
        if K.image_dim_ordering() == 'tf':
            # (width, height, channels)
            model.add(Permute((2, 3, 1), input_shape=input_shape))
        elif K.image_dim_ordering() == 'th':
            # (channels, width, height)
            model.add(Permute((1, 2, 3), input_shape=input_shape))
        else:
            raise RuntimeError('Unknown image_dim_ordering.')

        for i in range(self.layers):
            model.add(Convolution2D(self.nodes, (2, 2), strides=(4, 4), padding='same'))
            model.add(Activation('relu'))

        model.add(Flatten())
        model.add(Dense(256))
        model.add(Activation('relu'))
        model.add(Dense(nb_actions))
        model.add(Activation('linear'))
        print(model.summary())

        # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
        # even the metrics!
        memory = SequentialMemory(limit=1000000, window_length=WINDOW_LENGTH)
        processor = AtariProcessor()

        # Select a policy. We use eps-greedy action selection, which means that a random action is selected
        # with probability eps. We anneal eps from 1.0 to 0.1 over the course of 1M steps. This is done so that
        # the agent initially explores the environment (high eps) and then gradually sticks to what it knows
        # (low eps). We also set a dedicated eps value that is used during testing. Note that we set it to 0.05
        # so that the agent still performs some random actions. This ensures that the agent cannot get stuck.
        policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05,
                                      nb_steps=1000000)

        # The trade-off between exploration and exploitation is difficult and an on-going research topic.
        # If you want, you can experiment with the parameters or use a different policy. Another popular one
        # is Boltzmann-style exploration:
        # policy = BoltzmannQPolicy(tau=1.)
        # Feel free to give it a try!

        dqn = DQNAgent(model=model, nb_actions=nb_actions, policy=policy, memory=memory,
                       processor=processor, nb_steps_warmup=50000, gamma=.99, target_model_update=1000,
                       train_interval=4, delta_clip=1.)
        dqn.compile(Adam(lr=.00025), metrics=['mae'])

        self.trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))

        self.non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))

        self.dqn = dqn

        return None

    def train(self):
        # Make model
        self.gen_model()

        # Okay, now it's time to learn something! We capture the interrupt exception so that training
        # can be prematurely aborted. Notice that now you can use the built-in Keras callbacks!
        self.dqn.fit(self.env, nb_steps=150000, visualize=False)

        # Finally, evaluate our algorithm for 10 episodes.
        a = self.dqn.test(self.env, nb_episodes=10, visualize=False)
        return a, self.trainable_count, self.non_trainable_count

    def test(self):
        weights_filename = 'dqn_{}_weights.h5f'.format(args.env_name)
        if args.weights:
            weights_filename = args.weights
        dqn.load_weights(weights_filename)
        a = dqn.test(env, nb_episodes=10, visualize=True)
        return a
