#!/usr/bin/python

import cgi
import cgitb
import pickle
import data
import user
import game

cgitb.enable()

#print "Content-Type: text/html\n\n"

def main():

	try:
		user_data = data.read_users()
		user_info = user.get_session_from_cookie(user_data)
		game_data = data.read_games()

		print "Content-Type: text/html\n\n"
		print "<html><body>"
		print "<h2>Lobby</h2>"

		username = user_info["username"]

		print """
		<p>Welcome back %s</p>
		""" % username

	
		join_games = game.find_games(game_data, username)
		for g in join_games:
			p0 = g["players"][0]
			p1 = g["players"][1]
			print """<p>
			<a href="/cgi-bin/play.py?p0=%s&p1=%s">%s vs %s</a>
			</p>""" % (p0, p1, p0, p1)

		print """
		<p><a href="/cgi-bin/newgame.py">New Game</a></p>
		<p><a href="/cgi-bin/logout.py">Log Out</a></p>
		"""

		print "</body></html>"

	except user.NotLoggedIn:
		print "Content-Type: text/html\n\n"
		print "<html><body>"

		print """<p>Not logged in.
		<a href="/cgi-bin/login.py">Log In</a>
		</p>"""

		print "</body></html>"
		# session not found, redirect back to login
		#print "Location: /cgi-bin/login.py\n\n"

main()
