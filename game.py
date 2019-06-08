#!/usr/bin/python

import random

def create_new(game_data, player1_info, player2_info):
	player1_name = player1_info["username"]
	player2_name = player2_info["username"]
	game_key = (player1_name, player2_name)

	game_info = {
		"players": (player1_name, player2_name),
		"turn": 0, # index of whose turn it is
		"board": [
			[None, None, None],
			[None, None, None],
			[None, None, None]
		]
	}
	game_data[game_key] = game_info

def delete(game_data, player1_info, player2_info):
	player1_name = player1_info["username"]
	player2_name = player2_info["username"]
	game_key = (player1_name, player2_name)

	del game_data[game_key]

def find_games(game_data, player_info):
	player_name = player_info["username"]

	{game_key: info for game_key, info in game_data.items()
		if player_name in game_key }

def find_game_with(game_data, player1_info, player2_info):
	player1_name = player1_info["username"]
	player2_name = player2_info["username"]
	game_key = (player1_name, player2_name)
	
	if game_key in game_data:
		return game_data[game_key]
	else:
		return None
