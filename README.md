Misspelling Reddit Bot 
===================================

This repository contains an example of building a Reddit bot that scans a given subreddit's comments, checks if there are any misspelled words in each comment and replies to the author with the correct form of that word.

Pre-requisites
--------------

* Python 2.7 - conversion to Python3 is very easy
* A Reddit username and its password
* A Reddit client id and a client secret for a script
* A list of misspelled words and their correct form

Getting Started
---------------

1) Install Python
2) Install [pip](https://pip.pypa.io/en/stable/installing/)
3) Install [praw](https://praw.readthedocs.io/en/latest/): pip install praw
4) Create a Reddit user if you don't have one
5) Go to this [link](https://www.reddit.com/prefs/apps)
6) In the 'create application' section select 'script' option, give your application a name, and for 'redirect url' put a default value like http://localhost:8080/. Click 'Create app' button.
7) Under 'personal use script' you can find your client_id and down to 'secret' section you can find your client_secret. Copy those values into the config.py file. Add your username and your password in the same file.
8) Run bot from terminal: python misspell-checker.py

What I learned?
---------------

I learned:

1) How to use praw library
2) How to create a Reddit bot
3) How to login to Reddit, get comments from a subreddit, reply to a comment
4) How to work with Unicode strings

License
-------

Copyright 2018 Marian Vasilca.

Licensed to the Apache Software Foundation (ASF) under one or more contributor
license agreements.  See the LICENSE file distributed with this work for
additional information regarding copyright ownership.  The ASF licenses this
file to you under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License.  You may obtain a copy of
the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
License for the specific language governing permissions and limitations under
the License.