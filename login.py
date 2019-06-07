#!/usr/bin/python

import cgi
import cgitb
import os
import datetime
import Cookie
import data
import user

cgitb.enable()

#print "Content-Type: text/html\n\n"

def get_form_username(form):
	if "username" not in form:
		raise Exception("<p>username missing</p>")
	else:
		return form["username"].value

def get_form_password(form):
	if "password" not in form:
		raise Exception("<p>password missing</p>")
	else:
		return form["password"].value

def main():
	form = cgi.FieldStorage()

	username = ""
	try:
		user_data = data.read_users()

		username = get_form_username(form)
		password = get_form_password(form)
		user_info = user.find_info_check_password(user_data, username, password)

		session_id = user.register_user_session(user_data, username)
		expiration = datetime.datetime.now() + datetime.timedelta(days=1)
		cookie = Cookie.SimpleCookie()
		cookie["session"] = session_id

		data.write_users(user_data)

		print cookie.output()
		print "Status: 302 Found"
		print "Location: /cgi-bin/lobby.py\n\n"

	except (Exception, user.UnknownUser) as ex:
		print "Content-Type: text/html\n\n"
		print "<html><body>"
		print "<h2>Log In</h2>"

		print "<pre>\n"
		print user_data
		print "</pre>"

		if isinstance(ex, user.UnknownUser):
			print "<p>Unknown username</p>"
		else:
			print ex

		print """
		<form method="POST" action="/cgi-bin/login.py">
		"""

		print """
		<p>username: <input type="text" name="username" value="%s"/></p>
		""" % cgi.escape(username, quote=True)

		print """
		<p>password: <input type="password" name="password"/></p>
		<input type="submit" value="Log In"/>
		</form>
		"""

		print """
		<p><a href="/cgi-bin/signup.py">Sign Up</a></p>
		"""

		print "</body></html>"

main()
