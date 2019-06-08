#!/usr/bin/python

import cgi
import cgitb
import data
import user

cgitb.enable()

# print "Content-Type: text/html\n\n"

def main():
	user_data = data.read_users()

	user_info = user.get_session_from_cookie(user_data)

	if user_info:
		user.delete_user_session(user_data, user_info["username"])
		data.write_users(user_data)

	print "Status: 302 Found"
	print "Location: /cgi-bin/login.py\n\n"

main()
