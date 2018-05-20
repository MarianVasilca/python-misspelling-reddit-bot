#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 The Android Open Source Project
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import codecs
import praw
import config
import time
import re

DEBUG = True # do not comment when debug is activated
sleep_time = 3600 # in seconds
comment_limit = 100 # number of comments obtained; cannot be bigger than 1000
subreddit = "test".lower() # the name of the subreddit
comments_repplied_to_file = subreddit + "/comments_repplied_to.txt"
misspell_db_file = subreddit + "/misspell_db_file.txt"
misspell_db_file_char_sep = ':'
misspell_db_file_comment_line = '#'

comment_delimiters = ['\n', ' ', ',', '.', '?', '!', ':', ';', '(', ')']
comment_regex_pattern = '|'.join(map(re.escape, comment_delimiters))

comments_repplied_to = []

def bot_login():
	print ("Logging in...")
	return praw.Reddit(
		username = config.username,
		password = config.password,
		client_id = config.client_id,
		client_secret = config.client_secret,
		user_agent = config.user_agent
	)

def get_words_in_comment(comment):
	# no uppercase words for now
	comment = comment.body.lower()
	# Ignore empy lines and strip lines
	words = re.split(comment_regex_pattern, comment)
	words = filter(None, map(unicode.strip, words))
	return words

def get_reply_comment(mispelled, correct, author):
	r = u"Salut, {0}!\n\nForma corectă a cuvântului {1} este {2}.\n\nO zi faină!"
	return r.format(author, mispelled, correct)

def run_bot(r):
	print ("Obtaining %d comments..." % (comment_limit))
	for comment in r.subreddit(subreddit).comments(limit = comment_limit):
		if (comment.id not in comments_repplied_to 
			and comment.author != r.user.me()):

			# get words in comment
			words_in_comment = get_words_in_comment(comment)
			# iteritems() for Python 2.7. items() for Python 3.0 or higher
			for mispelled, correct in misspelled_words_dict.items():
				if mispelled in words_in_comment:
					print (mispelled + " is actually spelled " + correct + 
						". Found in comment: " + comment.id + " user: " + comment.author.name)
					response = get_reply_comment(mispelled, correct, comment.author.name)
					if not DEBUG:
						comment.reply(response)
					comments_repplied_to.append(comment.id)
					# append to the file
					with open(comments_repplied_to_file, "a") as f:
						f.write(comment.id + "\n")

def create_folder(path):
	try:
		# create folder for this subreddit
		os.makedirs(path)
	except OSError:
		if not os.path.isdir(path):
			raise

def get_save_comments():
	# create a folder for each subreddit if it does not exists
	create_folder(subreddit)

	if not os.path.isfile(comments_repplied_to_file):
		comments_repplied_to = []
	else:
		with open(comments_repplied_to_file, "r") as f:
			comments_repplied_to = f.read()
			comments_repplied_to = comments_repplied_to.split("\n")
			# remove empty string
			comments_repplied_to = filter(None, comments_repplied_to)
	return comments_repplied_to

def get_misspell_dict():
	misspelled_words_dict = {}
	if os.path.isfile(misspell_db_file):
		with codecs.open(misspell_db_file, "r", 'utf-8') as f:
			file = f.read()
			lines = file.split("\n")
			# Ignore empy lines and strip lines
			lines = filter(None, map(unicode.strip, lines))
			# Ignore comment lines
			lines = filter(lambda x: not x.startswith(misspell_db_file_comment_line), 
				lines)
			for line in lines:
				split = line.split(misspell_db_file_char_sep)
				if len(split) == 2:
					# no uppercase words for now
					misspelled_word = split[0].lower()
					correct_word = split[1].lower()
					misspelled_words_dict[misspelled_word] = correct_word
				else:
					print ("Error parsing line: " + line)
					print ("Correct format is misspelled_word" + 
						misspell_db_file_char_sep + "correct_word")

	return misspelled_words_dict

r = bot_login()
comments_repplied_to = get_save_comments()
# print (comments_repplied_to)

misspelled_words_dict = get_misspell_dict()
# print (misspelled_words_dict)

print ("DEBUG active: " + str(DEBUG))

while True:
	run_bot(r)
	# Sleep
	time.sleep(sleep_time)