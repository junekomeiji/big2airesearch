import tensorflow as tf
import numpy as np
import random
from deap import base, creator, tools, algorithms


def model_build():
    model = tf.keras.Sequential()
    model.add(tf.keras.Input(shape=(140,)))
    model.add(tf.keras.layers.Dense(104, activation="relu"))
    model.add(tf.keras.layers.Dense(104, activation="relu"))
    model.add(tf.keras.layers.Dense(13, activation="softmax"))
    
    # these are not used for this model, but are needed for compilation
    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    return model

def evaluate_game(ind1, ind2, ind3, ind4):
    
    pass


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    