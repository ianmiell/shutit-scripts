import json
import shutit
import os

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
	for item in server_list:
		description = server_dict[item]['description']
		print 'Server name: ' + item + ' - ' + description
		res = input()
	return res
	

def go(shutit_session, destination, server_dict, password_dict):
	servers = server_dict.keys()
	# get the item
	# if there is a via, recurse
	# then go to server
	return

# password json file - must be 0400 - shutit issecure function
def get_passwords():
	password_dict = None
	file_name = 'password.json'
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


password_dict = get_passwords()
server_dict   = get_servers()
destination   = choose()
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


