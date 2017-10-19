import shutit

def startup():
	s1 = shutit.create_session('bash',loglevel='info',echo=True)

	if not s1.command_available('minikube'):
		if s1.send_and_get_output('uname') == 'Darwin':
			s1.send('curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.22.3/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/')
		else:
			s1.send('curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.22.3/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/')

	while True:
		status = s1.send_and_get_output('minikube status')
		status_list = status.split('\n')
		if status_list[0] == 'minikube: Running' and status_list[1] == 'cluster: Running' and status_list[2][:29] == 'kubectl: Correctly Configured':
			break
		s1.send('minikube start')

	return s1

if __name__ == "__main__":
	s1 = startup()
	s1.send('minikube dashboard')
	s1.interact()
