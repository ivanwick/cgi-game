#!/usr/bin/python

import random
import Cookie
import os

def register_user_session(user_data, username):
	user_info = user_data[username]
	session_id = str(random.getrandbits(64))
	user_info["session"] = session_id
	return session_id

def delete_user_session(user_data, username):
	if username not in user_data:
		raise Exception("<p>Not logged in</p>")

	user_info = user_data[username]
	user_info["session"] = None

def register_new_user(user_data, username, password):
	user_data[username] = {
		"username": username,
		"password": password,
		"session": None
	}


class NotLoggedIn(Exception):
	pass

def get_session_from_cookie(user_data):
	try:
		cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
		cookie_session = cookie["session"].value
		for (username, user_info) in user_data.items():
			if user_info["session"] == cookie_session:
				return user_info
		raise
	except:
		raise NotLoggedIn()

class UnknownUser(Exception):
	pass

def find_info(user_data, username):
	if username not in user_data:
		raise UnknownUser

	return user_data[username]

def find_info_check_password(user_data, username, login_password):
	user_info = find_info(user_data, username)
	data_password = user_info["password"]
	if login_password != data_password:
		raise Exception("<p>wrong password</p>")

	return user_data[username]
