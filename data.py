#!/usr/bin/python

import os
import pickle
import random

USER_DATA_FILENAME = "/tmp/users.pickle"
GAME_DATA_FILENAME = "/tmp/games.pickle"

def read_users():
	if (not os.path.exists(USER_DATA_FILENAME)):
		write_users({})
		return {}
	else:
		with open(USER_DATA_FILENAME, "r") as f:
			return pickle.load(f)

def write_users(user_data):
	with open(USER_DATA_FILENAME, "w") as f:
		pickle.dump(user_data, f)

def read_games():
	if (not os.path.exists(GAME_DATA_FILENAME)):
		write_games({})
		return {}
	else:
		with open(GAME_DATA_FILENAME, "r") as f:
			return pickle.load(f)

def write_games(game_data):
	with open(GAME_DATA_FILENAME, "w") as f:
		pickle.dump(game_data, f)


