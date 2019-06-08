#!/usr/bin/python

import cgi
import cgitb
import pickle
import data
import user

cgitb.enable()

print "Content-Type: text/html\n\n"

def main():

	try:
		user_data = data.read_users()
		user_info = user.get_session_from_cookie(user_data)

		print "Content-Type: text/html\n\n"
		print "<html><body>"
		print "<h2>Lobby</h2>"

		print """
		<p>Welcome back %s</p>
		""" % user_info["username"]

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
