#!/usr/bin/python

import cgi
import cgitb
import os
import datetime
import Cookie
import data
import user
import game

cgitb.enable()

# print "Content-Type: text/html\n\n"

class MissingPlayers(Exception):
	pass

def get_form_players(form):
	if "p0" not in form or "p1" not in form:
		raise MissingPlayers("<p>missing players</p>")
	else:
		return (form["p0"].value, form["p1"].value)

def get_form_move(form):
	if "move" not in form:
		return None

	if "r" not in form or "c" not in form:
		raise game.InvalidMove

	return (int(form["r"].value), int(form["c"].value))

def print_header():
	print "Content-Type: text/html\n\n"
	print "<html><body>"
	print "<h2>Game</h2>"

def print_footer():
	print "</body></html>"

def print_game_header(game_info):
	player0 = game_info["players"][0]
	player1 = game_info["players"][1]
	print """
	<h3>%s vs %s</h3>
	""" % (player0, player1)


def print_game_over(game_info, game_result):
	print_game_header(game_info)
	print "<p>Game Over<p>"

	print "<p>"
	if game_result == None:
		print "Tie"
	else:
		print "Winner: "
		print game_info["players"][game_result]
	print "</p>"

	print_game_board(game_info, False)


def print_game(game_info, selfplayer):
	print_game_header(game_info)
	playerturn = game_info["players"][ game_info["turn"] ]

	print "<p>%s's turn" % playerturn
	if selfplayer != playerturn:
		print """
		<a href="/cgi-bin/play.py?p0=%s&p1=%s">Check for move</a>
		"""  % game_info["players"]
	print "</p>"

	myturn = playerturn == selfplayer
	print_game_board(game_info, myturn)

def print_cell(game_info, myturn, r, c):
	cell = game_info["board"][r][c]
	if cell != None:
		print cell
	else:
		if myturn:
			print_cell_form(game_info, r, c)
		else:
			print "&nbsp;&nbsp;"

def print_cell_form(game_info, r, c):
	(p0, p1) = game_info["players"]
	print """
	<form method="POST" action="/cgi-bin/play.py">
	<input type="hidden" name="p0" value="%s"/>
	<input type="hidden" name="p1" value="%s"/>
	<input type="hidden" name="r" value="%d"/>
	<input type="hidden" name="c" value="%d"/>
	<input type="submit" name="move" value="  "/>
	</form>
	""" % (p0, p1, r, c)
	

def print_game_board(game_info, myturn):
	print """<table>"""
	for r, row in enumerate(game_info["board"]):
		print "<tr>"
		for c, col in enumerate(row):
			print """<td style="border: 1px solid black; padding: 0.5em">"""
			if col:
				print col
			else:
				print_cell(game_info, myturn, r, c)
			print "</td>"
		print "</tr>"
	print "</table>"


def main():
	form = cgi.FieldStorage()

	try:
		user_data = data.read_users()
		user_info = user.get_session_from_cookie(user_data)
		selfplayer = user_info["username"]
		game_data = data.read_games()
		(p0, p1) = get_form_players(form)
		game_info = game.get_game_info(game_data, p0, p1)

		print_header()

		move = get_form_move(form)
		if move:
			try:
				game_data = game.move(game_data, game_info, selfplayer, move)
				data.write_games(game_data)
			except game.InvalidMove:
				print "<p>Invalid Move</p>"

		#print "<pre>"
		#print game_data
		#print "</pre>"

		game_over = game.is_game_over(game_info)

		if game_over[0]:
			print_game_over(game_info, game_over[1])
		else:
			print_game(game_info, selfplayer)

		print_footer()


	except user.NotLoggedIn:
		print "Content-Type: text/html\n\n"
		print "<html><body>"

		print """<p>Not logged in.
		<a href="/cgi-bin/login.py">Log In</a>
		</p>"""

		print "</body></html>"
		# session not found, redirect back to login
		#print "Location: /cgi-bin/login.py\n\n"

	except (game.UnknownGame, MissingPlayers) as ex:
		print_header()
		print ex
		print """<a href="/cgi-bin/newgame.py">New Game</a></p>"""
		print_footer()

main()
