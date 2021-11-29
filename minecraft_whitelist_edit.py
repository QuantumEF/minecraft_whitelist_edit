#!/usr/bin/python3
# This is very experimental so use at your own risk
# make a backup of whitelist.json as it MAY ACIDENTALLY ERASE FILES
# more testing is needed. 
# right now it can only add names to whitelist
# usage minecraft_whitelist_edit.py -u Username_To_Add

import json
import requests
import sys
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username')
args = parser.parse_args()
username = args.username

#to prevent spamming requests. 
time.sleep(1)
response = requests.get("https://api.mojang.com/users/profiles/minecraft/"+username)
if response.status_code == 200:
	user_data = json.loads(response.text)
	user_id = user_data.pop("id")

	user_id = user_id[:8] + '-' + user_id[8:]
	user_id = user_id[:13] + '-' + user_id[13:]
	user_id = user_id[:18] + '-' + user_id[18:]
	user_id = user_id[:23] + '-' + user_id[23:]

	user_data["uuid"] = user_id

	try:
		whitelist_file = open('whitelist.json')
	except OSError:
		print("Could not open whitelist file:")
		sys.exit(1)

	whitelist_data = json.load(whitelist_file)
	whitelist_file.close()

	whitelist_data.append(user_data)

	output_file = open("whitelist.json","w")
	json.dump(whitelist_data,output_file,indent="  ")
	print("Sucess")
else:
	print("Error")
	sys.exit(1)
