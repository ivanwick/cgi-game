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

print "Content-Type: text/html\n\n"

class MissingPlayers(Exception):
	pass

def get_form_players(form):
	if "p0" not in form or "p1" not in form:
		raise MissingPlayers("<p>missing players</p>")
	else:
		return (form["p0"].value, form["p1"].value)

def print_header():
	print "Content-Type: text/html\n\n"
	print "<html><body>"
	print "<h2>Game</h2>"

def print_footer():
	print "</body></html>"

def print_game(game_info, selfplayer):
	player0 = game_info["players"][0]
	player1 = game_info["players"][1]
	print """
	<h3>%s vs %s</h3>
	""" % (player0, player1)

	playerturn = game_info["players"][ game_info["turn"] ]

	print "<p>%s's turn</p>" % playerturn

	myturn = playerturn == selfplayer
	print_game_board(game_info, myturn)

def print_game_board(game_info, myturn):

	print "<table>"
	for r, row in enumerate(game_info["board"]):
		print "<tr>"
		for c, col in enumerate(row):
			print "<td>"
			if col:
				print col
			else:
				print "[%d, %d]" % (r, c)
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

		#move = get_form_move(form)
		#updated_game_info = game.move(game_data, game_info, selfplayer, move)
		#data.write_games(game_data)

		print_header()

		print "<pre>"
		print game_data
		print "</pre>"

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
