# generating signup keys
import pickle
import asyncio
from pprint import pprint
from functools import lru_cache
from typing import Optional, List
from typing import List, Optional
from datetime import datetime
from datetime import datetime, timedelta, timezone

import hashlib
import sqlite3
import typer
import emoji
from rich.console import Console
from pydantic import BaseModel
from pydantic import Field, EmailStr, validator


# hash user password
class PasswordEncription:

    def __init__(self, password):
        passowrd: str
        salt = "5gz"
        self.hased = hashlib.sha1(password.encode())

    def __str__(self):
        __password = self.hased.hexdigest()
        return __password


# user database actions
class User:

    """ CREATE TABLE Users(username VARCAHR(100), email TEXT, phone INTEGER, age INTERGER, password VARCAHR(50)); """

    def __init__(self):
        self.console = Console()
        self.conn = sqlite3.connect("Indicators.sql")
        self.cursor = self.conn.cursor()

    # re create table on operational error
    def re_create(self, table_name: str):

        self.cursor.execute(f""" CREATE TABLE {table_name}(
			id INTEGER PRIMARY KEY,
			username TEXT NOT NULL UNIQUE,
			email TEXT,
			phone INTEGER,
			age INTEGER,
			password TEXT NOT NULL)
			""")
        self.console.print(emoji.emojize(
            "[green bold]:muscle: Table created -- :tada:[/green bold]"))

    # register user
    def signup(self, user: dict):

        username = user["username"]
        email = user["email"]
        phone = user["phone"]
        age = user["age"]
        password = str(PasswordEncription(user["password"]))

        try:
            self.cursor.execute("""
					INSERT INTO Users(username, email, phone, age, password)
					VALUES(?, ?, ?, ?, ?)
					""", (username, email, phone, age, password))
            self.conn.commit()
            self.console.print(emoji.emojize(
                "[green bold]:zap: Success -- :tada:[/green bold]"))
            return True
        except sqlite3.OperationalError as e:
            self.console.print(emoji.emojize(f"[green bold]:no_entry_sign: {e} [/green bold]"))
            return False
        except sqlite3.IntegrityError:
            self.console.print(emoji.emojize(
                "[green bold]:no_entry: User exists :X:[/green bold]"))
            return False

    # login user
    def login(self, details: dict):

        # cheack for the user

        username = details["username"]
        password = str(PasswordEncription(details["password"]))

        self.cursor.execute("""
			SELECT * FROM Users
			WHERE username=? AND password=?
			""", (username, password))
        val = self.cursor.fetchall()

        if len(val) > 0:
            return True
        elif len(val) == 0:
            return False


# # testing methods
# if __name__ == '__main__':
	# new = {
	# "username" : "Shadrack",
	# "email" : "shadrackmeoli@gmail.com",
	# "age" : 25,
	# "phone": 254742909056,
	# "password" : "sdfdsyhY*%67"
	# }
# 	client = {
# 	"username" : "Shadrack",
# 	"password" : "sdfdsyhY*%67"
# 	}
	# new_user = User()
	# new_user.re_create("Users")
	# new_user.signup(new)
# 	new_user.login(client)
# 	pswd = str(PasswordEncription("Shadrack"))
# 	print(len(pswd))
