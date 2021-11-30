#!/usr/bin/python3
# This is very experimental so use at your own risk
# make a backup of whitelist.json as it MAY ACIDENTALLY ERASE FILES
# more testing is needed. 

import json
from requests_cache import CachedSession
import sys
import argparse
import time

parser = argparse.ArgumentParser()
#parser.add_argument('-u','--username')
parser.add_argument('command',choices=['add','delete'])
parser.add_argument('username')
parser.add_argument('-f','--file',default='whitelist.json')
args = parser.parse_args()
username = args.username

# cached session to prevent spamming requests.
session = CachedSession('/tmp/minecraft_whitelist_edit', backend='filesystem')
response = session.request("GET","https://api.mojang.com/users/profiles/minecraft/"+username)

if response.status_code != 200:
	if response.status_code == 204:
		sys.exit("User does not exist")
	sys.exit("Mojang API responded with code other than 200 or 204: {}".format(response.status_code))

# formats the data into the way it looks like in the file normally
user_data = json.loads(response.text)
user_id = user_data.pop("id")

user_id = user_id[:8] + '-' + user_id[8:]
user_id = user_id[:13] + '-' + user_id[13:]
user_id = user_id[:18] + '-' + user_id[18:]
user_id = user_id[:23] + '-' + user_id[23:]

user_data["uuid"] = user_id

try:
	whitelist_file = open(args.file)
except OSError:
	sys.exit("Could not open whitelist file")

try:
	whitelist_data = json.load(whitelist_file)
except json.JSONDecodeError:
	sys.exit("Malformed JSON file.")

whitelist_file.close()

if args.command == 'add':
	for item in whitelist_data:
		if item["uuid"].replace("-","") == user_id.replace("-",""):
			sys.exit("User already whitelisted")
	whitelist_data.append(user_data)	
elif args.command == 'delete':
	user_removed = False
	for item in whitelist_data:
		if item["uuid"].replace("-","") == user_id.replace("-",""):
			whitelist_data.remove(item)
			user_removed = True
			break
	if not user_removed:
		sys.exit("No User removed.")

output_file = open(args.file,"w")
json.dump(whitelist_data,output_file,indent="  ")
