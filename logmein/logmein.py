import json
import shutit
import os
import texttable
import stat
import sys

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


def choose(server_dict):
	server_list = server_dict.keys()
	table = texttable.Texttable()
	rows = []
	if len(server_list):
		for item in server_list:
			rows += [['server']+list(server_dict[item])]
			break
		for item in server_list:
			rows += [[item]+list(server_dict[item].values())]
		table.add_rows(rows)
		print table.draw()
		res = raw_input('Choose a server: ')
		if res in server_dict:
			return res
		else:
			print 'Not in list, try again'
			choose(server_dict)
	else:
		sys.exit()
	

def go(shutit_session, destination, server_dict, password_dict):
	servers = server_dict.keys()
	server_info = server_dict[destination]
	# get the item
	if 'via' in server_info:
		via = server_info['via']
	else:
		via = None
	# if there is a via, recurse
	if via is not None:
		go(shutit_session, via, server_dict, password_dict)
	# then go to server
	command = server_info['command']
	username = server_info['username']
	server = server_info['server']
	password = password_dict[destination][username]['password']
	if command is None:
		command = 'ssh '
		if username is not None:
			command += username + '@'
		command += server
	shutit_session.login(command=command,password=password,user=username)
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
		for name in ('via','command','username','server'):
			if name not in server_dict[item]:
				server_dict[item][name] = None
		if server_dict[item]['command'] is None and server_dict[item]['server'] is None:
			print 'Either "command" or "server" must be set in: ' + item
			sys.exit(1)
	return server_dict


password_dict = get_passwords()
server_dict   = get_servers()
server_dict   = tidy_server_dict(server_dict)
destination   = choose(server_dict)
print 'Please wait'
shutit_session = shutit.create_session('bash')

go(shutit_session, destination, server_dict,password_dict)
shutit_session.interact()



#    "pb": {
#        "description": "Powerbroker server",
#        "via":      null,
#        "command":  "ssh server1",
#        "username": "miellian",
#        "password": null


#if chosen_env in ('aws_terraform_prod','aws_terraform_etf','npclientsl','npclientgl','pclientsl','pclientgl'):
#             shutit.login('pbrun -h slgdsr000002614.intranet.barcapint.com bash',user='root',password=password)
#     if chosen_env in ('aws_terraform_etf','npclientsl','npclientgl','pclientsl','pclientgl'):
#             shutit.login('sudo su - miellian',user='miellian')
#     if chosen_env in ('aws_terraform_prod',):
#             shutit.login('sudo su - miellian',user='miellian_adm')
#     if chosen_env == 'chef_prod':
#             shutit.login('pbrun -h duwdsr002001276.intranet.barcapint.com bash',user=user,password=password)
#     if chosen_env == 'clustertest':
#             shutit.login('pbrun -h gbrpsr000004601 bash',user=user,password=password)
#     if chosen_env == 'chef_etf':
#             shutit.login('ssh ' + user + '@ldtdsr000001743.etf.barcapetf.com',password=password,user=user)
#     if chosen_env == 'aws_pilot_d':
#             shutit.login('pbrun -h duwdsr002001276 bash',user='root',password=password)
#             shutit.login('sudo su - miellian',user='miellian_adm')
#     if chosen_env == 'nposea':
#             shutit.login('pbrun -h gbrpsr000002521 bash',user='root',password=password)
#     if chosen_env == 'osepilota1':
#             shutit.login('pbrun -h slgdsr000002618 bash',user='root',password=password)
#     if chosen_env == 'osepilotd1':
#             shutit.login('pbrun -h duwdsr002000264.intranet.barcapint.com bash',user='root',password=password)
#     if chosen_env in ('etf','34upgrade'):
#             shutit.login('ssh ' + user + '@10.123.53.149',password=password,user=user)
#     if chosen_env == 'npclientsl':
#             shutit.send('oc login https://console-sl.appcloud-np.barcapint.com',expect='Username')
#             shutit.send('miellian_adm',expect='assword')
#             shutit.send(password)
#     if chosen_env == 'npclientgl':
#             shutit.send('oc login https://console-gl.appcloud-np.barcapint.com',expect='Username')
#             shutit.send('miellian_adm',expect='assword')
#             shutit.send(password)


