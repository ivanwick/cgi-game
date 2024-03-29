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

#print "Content-Type: text/html\n\n"

def get_form_otherplayer(form):
	if "otherplayer" not in form:
		raise Exception("<p>other player missing</p>")
	else:
		return form["otherplayer"].value

def print_header():
	print "Content-Type: text/html\n\n"
	print "<html><body>"
	print "<h2>New Game</h2>"

def print_footer():
	print "</body></html>"


def print_form(values):
	print """
	<form method="POST" action="/cgi-bin/newgame.py">
	<p>other player: <input type="text" name="otherplayer" value="%s"/></p>
	<input type="submit" value="Create"/>
	</form>
	""" % cgi.escape(values.get("otherplayer", ""), quote=True)

class GameAlreadyExists(Exception):
	pass

class GameVsSelf(Exception):
	pass

def main():
	form = cgi.FieldStorage()

	otherplayer = ""
	try:
		user_data = data.read_users()
		user_info = user.get_session_from_cookie(user_data)
		game_data = data.read_games()
		selfplayer = user_info["username"]
		otherplayer = get_form_otherplayer(form)
		# lookup will verify that otherplayer exists
		otherplayer_info = user.find_info(user_data, otherplayer)

		if (selfplayer == otherplayer):
			raise GameVsSelf("""<p>
			Choose a different player</p>""")

		if game.exists(game_data, selfplayer, otherplayer):
			raise GameAlreadyExists(
			"""<p><a href="/cgi-bin/play.py?p0=%s&p1=%s">
			%s vs %s already exists</a></p>""" % (
			cgi.escape(selfplayer, quote=True),
			cgi.escape(otherplayer, quote=True),
			cgi.escape(selfplayer, quote=True),
			cgi.escape(otherplayer, quote=True)
			))

		game.create_new(game_data, selfplayer, otherplayer)

		data.write_games(game_data)

		#print "<pre>"
		#print game_data
		#print "</pre>"
		print "Status: 302 Found"
		print "Location: /cgi-bin/play.py?p0=%s&p1=%s\n\n" % (
			cgi.escape(selfplayer, quote=True),
			cgi.escape(otherplayer, quote=True)
			)
	
	except user.NotLoggedIn:
		print "Content-Type: text/html\n\n"
		print "<html><body>"

		print """<p>Not logged in.
		<a href="/cgi-bin/login.py">Log In</a>
		</p>"""

		print "</body></html>"
		# session not found, redirect back to login
		#print "Location: /cgi-bin/login.py\n\n"

	except user.UnknownUser:
		print_header()
		print "<p>Unknown player</p>"
		print_form({"otherplayer":otherplayer})
		print_footer()

	except Exception as ex:
		print_header()
		print ex
		print_form({"otherplayer":otherplayer})
		print_footer()

main()
