import minikube

s1 = minikube.startup()

if not s1.command_available('kubeless'):
	s1.send('rm -rf tmpkubeless && mkdir tmpkubeless')
	s1.send('cd tmpkubeless')
	s1.send('wget https://github.com/kubeless/kubeless/releases/download/v0.2.3/kubeless_darwin-amd64.zip')
	s1.send('unzip kubeless_darwin-amd64.zip')
	s1.send('chmod +x bundles/kubeless_darwin-amd64/kubeless')
	s1.send('mv bundles/kubeless_darwin-amd64/kubeless /usr/local/bin')
	s1.send('cd ..')
	s1.send('rm -rf tmpkubeless')

if s1.send_and_get_output('kubectl get ns | grep -w kubeless | wc -l') == '0':
	s1.send('kubectl create ns kubeless')
	# No RBAC
	s1.send('curl -sL https://github.com/kubeless/kubeless/releases/download/v0.2.3/kubeless-v0.2.3.yaml | kubectl create -f -')


s1.send('rm -rf tmpkubeless && mkdir tmpkubeless')
s1.send('cd tmpkubeless')
s1.send('git clone https://github.com/kubeless/kubeless.git')
s1.send('cd kubeless/examples')
if s1.send_and_get_output('kubeless function list | grep -w get-python | wc -l') != '0':
	s1.send('kubeless function delete get-python')
s1.send('make get-python')
s1.send('kubeless function call get-python')
s1.pause_point('')
s1.send('cd ../..')
s1.send('rm -rf tmpkubeless')



s1.pause_point('kubectl')
