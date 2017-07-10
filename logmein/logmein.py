import json
import shutit

password_dict = None
# password json file - must be 0400 - shutit issecure function
stat file
if file exists and has bad perms,
	exit
if file exists read in file


server_dict = json.loads(open('servers.json').read())

server_list = servers.keys()
print server_list
for item in server_dict:
	print item
	print servers[item]
