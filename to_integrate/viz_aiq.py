#!/usr/bin/env python3

#####################################################################
# This script presents how to use the most basic features of the environment.
# It configures the engine, and makes the agent perform random actions.
# It also gets current state and reward earned with the action.
# <episodes> number of episodes are played. 
# Random combination of buttons is chosen for every action.
# Game variables from state and last reward are printed.
#
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from __future__ import print_function
import vizdoom as vzd

from viz_env import Env

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv2D, Conv3D, Reshape, MaxPooling1D, AveragePooling2D,MaxPooling2D, Dropout
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.callbacks import TensorBoard
from keras.utils import np_utils
from keras.utils import to_categorical

from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory
import numpy as np
from PIL import Image

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

from random import choice
from time import sleep

import csv

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def logit(data):
    with open('data_v2.csv', 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, data.keys())
        #w.writeheader()
        w.writerow(data)

def logit3(data):
    with open('data_new.csv', 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(data)

def logit4(data):
    with open('data_new_1.csv', 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(data)

def logit2(data, name):
    with open(name, 'a') as f:  # Just use 'w' mode in 3.x
        spamwriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow((data))


def getModel(input_dim, env):
    model = Sequential()
    model.add(Conv2D(8, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(120,160,3)))
    model.add(Conv2D(16, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(Dropout(0.2))
    model.add(Conv2D(16, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(8, (3, 3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(6, activation='softmax'))
    model.add(Reshape((3,2)))
    '''
    # data_v7
    model = Sequential()
    model.add(Conv2D(11, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(120,160,3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(8, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(4, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(6, activation='softmax'))
    model.add(Reshape((3,2)))
    '''
    '''
    # data_v6
    model = Sequential()
    model.add(Conv2D(11, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(120,160,3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.1))
    model.add(Conv2D(8, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.1))
    model.add(Conv2D(4, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.1))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(6, activation='softmax'))
    model.add(Reshape((3,2)))
    '''
    '''
    # data_v5
    model = Sequential()
    model.add(Conv2D(240, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(120,160,3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(16, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(8, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(6, activation='softmax'))
    model.add(Reshape((3,2)))
    '''
    '''
    # data_v4
    model = Sequential()
    model.add(Conv2D(64, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(120,160,3)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(16, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(8, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(6, activation='softmax'))
    model.add(Reshape((3,2)))
    '''
    '''
    model = Sequential()
    model.add(Conv2D(filters=32, kernel_size = (5,5), input_shape=(120,160,3),activation='elu'))
    model.add(Conv2D(filters=16, kernel_size = (3,3),activation='elu'))
    model.add(AveragePooling2D(pool_size=(2,2)))
    model.add(Conv2D(filters=8, kernel_size = (5,5), input_shape=(120,160,3),activation='elu'))
    model.add(Conv2D(filters=4, kernel_size = (3,3),activation='elu'))
    model.add(AveragePooling2D(pool_size=(2,2)))

    model.add(Flatten())
    model.add(Dense(160,activation='elu'))
    model.add(Dense(60,activation='elu'))
    model.add(Dense(6,activation='elu'))
    model.add(Reshape((3,2)))
    '''
    '''
    model = Sequential()
    model.add(Dense(3, input_shape=(120,160,3), activation='relu'))
    
    model.add(Reshape((3,120, 160)))
    model.add(Dense(160, activation='relu'))
    model.add(Reshape((3, 120*160)))
    model.add(Dense(120, activation='relu'))
    model.add(Reshape((1, 3*120)))
    model.add(Dense(3, activation='relu'))
      
    model.add(Flatten())

    #model.add(Dense(3, activation='sigmoid'))
    model.add(Dense(3, activation='relu'))
    '''
    return model



import glob
import pandas as pd

if __name__ == "__main__":
    # Create DoomGame instance. It will run the game and communicate with you.
    game = vzd.DoomGame()

    # Now it's time for configuration!
    # load_config could be used to load configuration instead of doing it here with code.
    # If load_config is used in-code configuration will also work - most recent changes will add to previous ones.
    # game.load_config("../../scenarios/basic.cfg")

    # Sets path to additional resources wad file which is basically your scenario wad.
    # If not specified default maps will be used and it's pretty much useless... unless you want to play good old Doom.
    game.set_doom_scenario_path("scenarios/basic.wad")

    # Sets map to start (scenario .wad files can contain many maps).
    game.set_doom_map("map01")

    # Sets resolution. Default is 320X240
    game.set_screen_resolution(vzd.ScreenResolution.RES_160X120)

    # Sets the screen buffer format. Not used here but now you can change it. Defalut is CRCGCB.
    game.set_screen_format(vzd.ScreenFormat.RGB24)

    # Enables depth buffer.
    game.set_depth_buffer_enabled(True)

    # Enables labeling of in game objects labeling.
    game.set_labels_buffer_enabled(True)

    # Enables buffer with top down map of the current episode/level.
    game.set_automap_buffer_enabled(True)

    # Sets other rendering options (all of these options except crosshair are enabled (set to True) by default)
    game.set_render_hud(False)
    game.set_render_minimal_hud(False)  # If hud is enabled
    game.set_render_crosshair(False)
    game.set_render_weapon(True)
    game.set_render_decals(False)  # Bullet holes and blood on the walls
    game.set_render_particles(False)
    game.set_render_effects_sprites(False)  # Smoke and blood
    game.set_render_messages(False)  # In-game messages
    game.set_render_corpses(False)
    game.set_render_screen_flashes(True)  # Effect upon taking damage or picking up items

    # Adds buttons that will be allowed.
    game.add_available_button(vzd.Button.MOVE_LEFT)
    game.add_available_button(vzd.Button.MOVE_RIGHT)
    game.add_available_button(vzd.Button.ATTACK)

    # Adds game variables that will be included in state.
    game.add_available_game_variable(vzd.GameVariable.AMMO2)

    # Causes episodes to finish after 200 tics (actions)
    game.set_episode_timeout(200)

    # Makes episodes start after 10 tics (~after raising the weapon)
    game.set_episode_start_time(10)

    # Makes the window appear (turned on by default)
    game.set_window_visible(True)

    # Turns on the sound. (turned off by default)
    game.set_sound_enabled(False)

    # Sets the livin reward (for each move) to -1
    game.set_living_reward(-1)

    # Sets ViZDoom mode (PLAYER, ASYNC_PLAYER, SPECTATOR, ASYNC_SPECTATOR, PLAYER mode is default)
    game.set_mode(vzd.Mode.PLAYER)

    # Enables engine output to console.
    #game.set_console_enabled(True)

    # Initialize the game. Further configuration won't take any effect from now on.


    # Define some actions. Each list entry corresponds to declared buttons:
    # MOVE_LEFT, MOVE_RIGHT, ATTACK
    # game.get_available_buttons_size() can be used to check the number of available buttons.
    # 5 more combinations are naturally possible but only 3 are included for transparency when watching.
    actions = [[True, False, False], [False, True, False], [False, False, True]]

    # Run this many episodes
    episodes = 10

    # ****** AI ****** #
    '''
    env = Env(game)
    nb_actions = env.action_space.n
    obs_dim = env.observation_space.shape[0]
    '''
    print("making model")
    model = getModel(-1, -1)
    print(model.summary())
    model.compile(optimizer='adam', loss='categorical_crossentropy',metrics=['mae', 'acc'])



    #Load data
    print("importing data")

    X = []
    count = 0
    for file in glob.glob("/media/chris/NVMe-SSD/Linux/viz_data/imgs/*.png"):
        im = Image.open(file)
        X.append(np.array(im))
        im.close()
        count = count + 1
        if count == 2000:
            break

    X = np.array(X) / 255.0
    X = X.reshape((-1, 120,160,3))


    df = pd.read_csv('/media/chris/NVMe-SSD/Linux/viz_data/inputs.csv',names=['act1','act2', 'act3'])
    Y = df.values
    Y = np.array(Y)
    Y = Y[0:2000]
    Y = Y.astype(float)
    Y = to_categorical(Y)

    tb = TensorBoard(log_dir='./AIQ/logs/run2/', histogram_freq=0, batch_size=32, 
        write_graph=True, write_grads=False, write_images=False)

    game.init()
    for jk in range(1000):
        avg_r = 0
        model.fit(X, Y, batch_size=32, epochs=1, verbose=1, shuffle=True, validation_split=0.1,callbacks=[tb])

        for i in range(30):
            print("Episode #" + str(i + 1))
            game.new_episode()
        
            num = 0

            while not game.is_episode_finished():

                # Gets the state
                state = game.get_state()

                # Which consists of:
                n = state.number
                vars = state.game_variables
                screen_buf = state.screen_buffer
                depth_buf = state.depth_buffer
                labels_buf = state.labels_buffer
                automap_buf = state.automap_buffer
                labels = state.labels


                screen_buf = screen_buf / 255.0
                screen_buf = screen_buf.reshape((-1,120,160,3))
               
                num = model.predict(screen_buf)
                num = num[0]

                acti = []
                for thing in num:
                    if thing[0] < thing[1]:
                        acti.append(True)
                    else:
                        acti.append(False)

                r = game.make_action(acti)


                
            # Check how the episode went.
            print("Episode finished.")
            print("Total reward:", game.get_total_reward())
            print("num:", num)
            logit3([jk, game.get_total_reward()])
            avg_r = avg_r + game.get_total_reward()
        logit4([jk, avg_r/30])

