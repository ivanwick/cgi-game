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
	return [info for game_key, info in game_data.items()
		if player_name in game_key ]

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

class InvalidMove(Exception):
	pass

class OutOfTurnMove(InvalidMove):
	pass

def validate_move(move):
	print move
	if move[0] == None or move[1] == None:
		raise InvalidMove

	if not ((0 <= move[0] <= 2) and
		(0 <= move[1] <= 2) ):
		print "A"
		raise InvalidMove

def move(game_data, game_info, selfplayer, move):
	validate_move(move)
	selfindex = game_info["players"].index(selfplayer)
	board = game_info["board"]
	if selfindex != game_info["turn"]:
		raise OutOfTurnMove

	if board[ move[0] ][ move[1] ]:
		raise InvalidMove

	board[ move[0] ][ move[1] ] = selfindex

	if (selfindex == 0):
		game_info["turn"] = 1
	else:
		game_info["turn"] = 0

	# update game state

	game_data[ game_info["players"] ] = game_info

	return game_data

def is_game_over(game_info):
	board = game_info["board"]

	for player_index in (0, 1):
		for r in [0, 1, 2]:
			if player_index == \
			board[r][0] == board[r][1] == board[r][2]:
				return (True, player_index)
		for c in [0, 1, 2]:
			if player_index == \
			board[0][c] == board[1][c] == board[2][c]:
				return (True, player_index)

		if player_index == \
		board[0][0] == board[1][1] == board[2][2]:
			return (True, player_index)

		if player_index == \
		board[2][0] == board[1][1] == board[0][2]:
			return (True, player_index)

	found_empty = False
	for r in (0, 1, 2):
		for c in (0, 1, 2):
			if board[r][c] == None:
				found_empty = True

	if not found_empty:
		return (True, None)

	return (False,)
