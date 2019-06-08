#!/usr/bin/python

import random

def create_new(game_data, player0_name, player1_name):
	game_key = (player0_name, player1_name)

	game_info = {
		"players": (player0_name, player1_name),
		"turn": 0, # index of whose turn it is
		"board": [
			[None, None, None],
			[None, None, None],
			[None, None, None]
		]
	}
	game_data[game_key] = game_info

def delete(game_data, player0_name, player1_name):
	game_key = (player0_name, player1_name)

	del game_data[game_key]

def find_games(game_data, player_name):
	{game_key: info for game_key, info in game_data.items()
		if player_name in game_key }

class UnknownGame(Exception):
	pass

def get_game_info(game_data, player0_name, player1_name):
	game_key = (player0_name, player1_name)
	
	if game_key in game_data:
		return game_data[game_key]
	else:
		raise UnknownGame(
			"<p>Game with %s vs %s doesn't exist.</p>"
			% (player0_name, player1_name))

def exists(game_data, p0, p1):
	key = (p0, p1)
	return key in game_data
