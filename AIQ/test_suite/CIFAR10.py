from .common import header, desc
from keras.utils import np_utils
import numpy as np

class CIFAR10(desc):

    def __init__(self, params):

        super().__init__()
        try:
            # Data is currently gotten from keras datasets
            from keras.datasets import cifar10
            from argparse import ArgumentParser
        except:
            print("Failed to import CIFAR10, make sure you have Keras,cifar10 installed!")

        # Prep data
        (x_train, y_train), (x_test, y_test) = cifar10.load_data()

        # Normalize xs
        self.x_train = x_train / 255
        self.x_test = x_test / 255

        # Convert to greyscale
        rgb_convert = [0.2989,0.5870,0.1140]
        self.x_train = np.dot(self.x_train, rgb_convert)
        self.x_test  = np.dot(self.x_test , rgb_convert)

        # Flatten x data
        self.x_train = np.reshape(self.x_train, (-1, 1024))
        self.x_test  = np.reshape(self.x_test , (-1, 1024))

        # Convert y to one-hot
        self.y_train = np_utils.to_categorical(y_train)
        self.y_test =  np_utils.to_categorical(y_test)
        
        self.input_dim = len(self.y_train[0]) 
        self.output_dim = len(self.x_train[0])
        self.num_classes = self.y_test.shape[1]
        
        # Global variable initialization
        self.current_image_ind = None
        self.instance_counter  = None 
        self.max_instances = 1000
        
        # Define header
        self.header = header(env_name="CIFAR10", 
                             input_dim=[self.input_dim], 
                             output_dim=[self.output_dim],
                             info="Cifar10 Data set",
                             env_min_score = 0.0,
                             env_max_score = 1000.0,
                             rl=True)
    # Return header object
    def get_header(self):
        return self.header
        
    def random_action(self):
        return np.random.rand(10)

    # Used for CEM Agent
    def step(self, action):
        return self.act(action)

    # Make prediction
    def act(self, action):
        
        # Get correct solution
        solution = self.y_train[self.current_image_ind]

        # Check if correct solution
        #print(action, solution)
        if action == np.argmax(solution):
            self.reward_step = 1.0
        else:
            self.reward_step = 0.0

        # Add step to total reward
        self.reward_total = self.reward_total + self.reward_step

        # Add to counter
        self.instance_counter = self.instance_counter + 1

        # Check if max count has been reached
        if self.instance_counter >= self.max_instances:
            self.done = True
        else:
            self.done = False

        
        # Set new index and get new image
        self.current_image_ind = np.random.randint(len(self.x_train) + 1)
        self.observation = self.x_train[self.current_image_ind]
        
        return self.observation, self.reward_step, self.done, {}
    
    def reset(self):
        self.current_image_ind = None
        self.instance_counter = 0
        self.observation = None
        self.reward_step = 0
        self.reward_total = 0
        self.done = False


        self.current_image_ind = np.random.randint(len(self.x_train) + 1)

        return self.x_train[self.current_image_ind]
