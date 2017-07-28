import shutit

# Tested on OSx only
s1 = shutit.create_session('bash',loglevel='debug')
# TODO: get minishift
s1.send('minishift update',{'want to update':'y'})
while True:
	status = s1.send_and_get_output('minishift status')
	if status == 'Running':
		s1.send('eval $(minishift oc-env)')
		break
	else:
		s1.send('minishift start')
		s1.send('eval $(minishift oc-env)')
		s1.send('minishift start --vm-driver virtualbox')
		s1.send('eval $(minishift oc-env)')
s1.send('oc login -u system:admin')
s1.send('minishift console')
s1.interact()
