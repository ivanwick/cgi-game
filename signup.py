#!/usr/bin/python

import cgi
import cgitb
import data
import user

cgitb.enable()

# print "Content-Type: text/html\n\n"

def check_username(form, user_data):
	if "username" not in form:
		raise Exception("<p>username missing</p>")

	username = form["username"].value

	if username in user_data:
		raise Exception("<p>username %s is already registered</p>" % username)
	else:
		return username

def check_password(form):
	if "password1" not in form or "password2" not in form:
		raise Exception("<p>choose a password</p>")

	pass1 = form["password1"].value
	pass2 = form["password2"].value

	if pass1 != pass2:
		raise Exception("<p>new password doesn't match</p>")

	return pass1 # either one

def main():
	form = cgi.FieldStorage()

	username = ""

	try:
		user_data = data.read_users()

		username = check_username(form, user_data)
		newpass = check_password(form)

		user.register_new_user(user_data, username, newpass)

		data.write_users(user_data)

		print "Status: 302 Found"
		print "Location: /cgi-bin/login.py\n\n"

	except Exception as e:
		print "Content-Type: text/html\n\n"
		print "<html><body>"
		print "<h2>Sign Up</h2>"

		#print "<pre>\n"
		#print user_data
		#print "</pre>"

		print e

		print """
		<form method="POST" action="/cgi-bin/signup.py">
		"""

		print """
		<p>username: <input type="text" name="username" value="%s"/></p>
		""" % cgi.escape(username, quote=True)

		print """
		<p>password: <input type="password" name="password1"/></p>
		<p>password again: <input type="password" name="password2"/></p>
		<input type="submit"/>
		</form>
		"""

		print "</body></html>"

main()
