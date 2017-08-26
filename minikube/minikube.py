import shutit

def startup():
	s1 = shutit.create_session('bash',loglevel='debug',echo=True)
	# TODO: get minikube itself?
	# curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
	# curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.7.0/bin/linux/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/
	while True:
		status = s1.send_and_get_output('minikube status')
		status_list = status.split('\n')
		print status_list
		print status_list[2][:28]
		if status_list[0] == 'minikube: Running' and status_list[1] == 'localkube: Running' and status_list[2][:29] == 'kubectl: Correctly Configured':
			break
	return s1

if __name__ == "__main__":
	s1 = startup()
	s1.send('minikube dashboard')
	s1.interact()
