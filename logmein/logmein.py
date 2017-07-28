import json
import shutit
import os
import texttable
import stat
import sys


# TODO: cl args
debug=False
loglevel='WARNING'


def is_file_secure(file_name):
    """Returns false if file is considered insecure, true if secure.
    If file doesn't exist, it's considered secure!
    """
    if not os.path.isfile(file_name):
        return True
    file_mode = os.stat(file_name).st_mode
    if file_mode & (stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH):
        return False
    return True


def choose(server_dict,longtable):
	server_list = server_dict.keys()
	table = texttable.Texttable(max_width=200)
	rows = []
	if len(server_list):
		if longtable:
			for item in server_list:
				headers = list(server_dict[item])
				rows += [['server']+headers]
				break
		else:
			headers = ['description']
			rows += [['server','description']]
		for item in server_list:
			value_list = []
			for name in headers:
				value = server_dict[item][name]
				value_list += [server_dict[item][name]]
			rows += [[item]+value_list]
		for name in headers:
			#set collength
			pass
		table.add_rows(rows)
		print table.draw()
		res = raw_input('Choose a server: ')
		if res in server_dict:
			return res
		else:
			print 'Not in list, try again'
			choose(server_dict,longtable)
	else:
		sys.exit()
	

def go(shutit_session, destination, server_dict, password_dict):
	log('Server info: ' + str(server_dict))
	servers = server_dict.keys()
	server_info = server_dict[destination]
	# get the item
	log('Destination: ' + destination)
	if 'via' in server_info:
		via = server_info['via']
	else:
		via = None
	# if there is a via, recurse
	if via is not None:
		go(shutit_session, via, server_dict, password_dict)
		log('Logged into: ' + via)
	log('Now logging into: ' + destination)
	# then go to server
	login_command = server_info['login_command']
	username      = server_info['username']
	server        = server_info['server']
	commands      = server_info['commands']
	password      = None
	log('\nLogin command: ' + str(login_command) + ' \nUsername: ' + str(username) + ' \nServer: ' + str(server) + ' \nCommands' + str(commands))
	if username is None:
		# TODO: extract username from login_command if it's not specified and in there
		pass
	if destination in password_dict:
		password = password_dict[destination]
	log(password_dict)
	log("Password: " + str(password))
	if login_command is None and server is not None:
		login_command = 'ssh '
		if username is not None:
			login_command += username + '@'
			login_command += server
	if login_command is not None or server is not None:
		shutit_session.login(command=login_command,password=password,user=username)
	if commands is not None:
		for command in commands:
			shutit_session.send(command)
	return


# password json file - must be 0400 - shutit issecure function
def get_passwords():
	password_dict = None
	file_name = 'passwords.json'
	if os.path.exists(file_name):
		if not is_file_secure(file_name):
			print 'Password file: ' + file_name + ' is not secure'
			sys.exit(1)
		password_dict = json.loads(open(file_name).read())
	return password_dict


def get_servers():
	servers_file_name = 'servers.json'
	server_dict = json.loads(open(servers_file_name).read())
	return server_dict


def tidy_server_dict(server_dict):
	for item in server_dict:
		for name in ('via','login_command','username','server','commands'):
			if name not in server_dict[item]:
				server_dict[item][name] = None
		if server_dict[item]['login_command'] is None and server_dict[item]['server'] is None and server_dict[item]['commands'] is None:
			print 'Either "login_command" or "server" must be set in: ' + item
			sys.exit(1)
	return server_dict


def log(msg):
	if debug:
		print msg


password_dict = get_passwords()
server_dict   = get_servers()
server_dict   = tidy_server_dict(server_dict)
destination   = choose(server_dict,longtable=False)


# Create the bash session
print 'Please wait...'
shutit_session = shutit.create_session('bash',loglevel=loglevel)


# Off we go.
go(shutit_session, destination, server_dict,password_dict)
shutit_session.pause_point()

