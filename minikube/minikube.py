import shutit

def startup(delete=False):
	s1 = shutit.create_session('bash',loglevel='info',echo=True)
	if not s1.command_available('minikube') or s1.send_and_get_output("""minikube version | awk '{print $NF}'""") != 'v0.23.0':
		try:
			pw = file('secret').read().strip()
		except IOError:
			 pw = ''
		if pw == '':
			s1.log('''WARNING! IF THIS DOES NOT WORK YOU MAY NEED TO SET UP A 'secret' FILE IN THIS FOLDER!''')
			import time
			time.sleep(10)
		if s1.send_and_get_output('uname') == 'Darwin':
			s1.multisend('curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.25.2/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/',{'assword':pw})
		else:
			s1.multisend('curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.8.0/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/',{'password':pw})
			s1.multisend('curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.25.2/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/',{'assword':pw})
	if delete:
		s1.send('minikube delete || true')
	while True:
		status = s1.send_and_get_output('minikube status')
		status_list = status.split('\n')
		if status_list[0] == 'minikube: Running' and status_list[1] == 'cluster: Running' and status_list[2][:29] == 'kubectl: Correctly Configured':
			break
		s1.send('minikube start --memory 4096')

	return s1

if __name__ == "__main__":
	s1 = startup()
	s1.send('#minikube dashboard')
	s1.interact()
