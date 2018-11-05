#!/usr/bin/env python3

#####################################################################
# This script presents labels buffer that shows only visible game objects
# (enemies, pickups, exploding barrels etc.), each with unique label.
# OpenCV is used here to display images, install it or remove any
# references to cv2
# Configuration is loaded from "../../scenarios/basic.cfg" file.
# <episodes> number of episodes are played.
# Random combination of buttons is chosen for every action.
# Game variables from state and last reward are printed.
#
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from __future__ import print_function

from random import choice
import vizdoom as vzd
import csv
from argparse import ArgumentParser
import numpy as np
import cv2

def logit(data):
    with open('data_gen.csv', 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        w.writerow(data)

DEFAULT_CONFIG = "scenarios/basic.cfg"
if __name__ =="__main__":
    parser = ArgumentParser("ViZDoom example showing how to use labels and labels buffer.")
    parser.add_argument(dest="config",
                        default=DEFAULT_CONFIG,
                        nargs="?",
                        help="Path to the configuration file of the scenario."
                             " Please see "
                             "../../scenarios/*cfg for more scenarios.")

    args = parser.parse_args()

    game = vzd.DoomGame()

    # Use other config file if you wish.
    game.load_config(args.config)
    #game.set_render_hud(False)

    #game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)

    # Set cv2 friendly format.
    game.set_screen_format(vzd.ScreenFormat.BGR24)

    # Enables labeling of the in game objects.
    game.set_labels_buffer_enabled(True)

    game.clear_available_game_variables()
    game.add_available_game_variable(vzd.GameVariable.POSITION_X)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Y)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Z)

    game.init()

    actions = [[True, False, False], [False, True, False], [False, False, True]]

    episodes = 1000

    # Sleep time between actions in ms
    sleep_time = 28

    counter = 0


    with open('inputs.txt', 'w') as f:  # Just use 'w' mode in 3.x
        spamwriter = csv.writer(f, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        

        for i in range(episodes):
            print("Episode #" + str(i + 1))

            # Not needed for the first episode but the loop is nicer.
            game.new_episode()
            while not game.is_episode_finished():

                # Gets the state
                state = game.get_state()

                # Screen buffer, given in selected format. This buffer is always available.
                # Using information from state.labels draw bounding boxes.
                screen = state.screen_buffer   
                ###cv2.imwrite('imgs/' + str(counter) +'.png', screen)

                # Get Info Here
                for obj in state.labels:
                    if obj.object_name == "DoomPlayer":
                        player_x = obj.object_position_x
                        player_y = obj.object_position_y
                        player_z = obj.object_position_z
                        player_wid = obj.width
                        player_height = obj.height
                    elif obj.object_name == "Cacodemon":
                        enemy_x = obj.object_position_x
                        enemy_y = obj.object_position_y
                        enemy_z = obj.object_position_z
                        enemy_wid = obj.width
                        enemy_height = obj.height
                      
                #Shoot?
                if( np.abs(player_y - enemy_y) < enemy_wid):
                    act = [False, False, True]
                elif(player_y < enemy_y):
                    act = [True, False, False]
                elif(player_y > enemy_y):
                    act = [False, True, False]

                game.make_action(act)
                ###spamwriter.writerow((counter, act[0], act[1], act[2]))
                counter = counter + 1
                #print(player_y, enemy_y)

                #end doooooo


                

            print("Episode finished!", game.get_total_reward())
            logit([game.get_total_reward()])
        cv2.destroyAllWindows()
