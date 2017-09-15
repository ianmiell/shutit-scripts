import shutit

# IF YOU SEE GENERAL FAILURES, TRY:
#sudo rm -rf ~/.minishift/

def startup():
	s1 = shutit.create_session('bash',loglevel='debug',echo=True)
	# TODO: get minishift itself?
	s1.send('minishift update',{'want to update':'y'})
	while True:
		status = s1.send_and_get_output('minishift status')
		if status == 'Running':

			s1.send('eval $(minishift oc-env)')
			break
		else:
			if s1.send_and_get_output('uname') == 'Darwin':
				# Problems?
 				# sudo minishift delete --cache
 				# sudo rm -rf ~/.minishift/
				s1.send('minishift addons install --defaults')
				s1.send('minishift addons enable cluster-admin')
				s1.send('minishift start')
			else:
				s1.send('minishift addons install --defaults')
				s1.send('minishift addons enable cluster-admin')
				s1.send('minishift start --vm-driver virtualbox')
			s1.send('eval $(minishift oc-env)')
	s1.send('oc adm policy add-cluster-role-to-user cluster-admin admin --as=system:admin')
	return s1

if __name__ == "__main__":
	s1 = startup()
	s1.send('oc login -u system:admin')
	s1.send('minishift console')
	s1.interact()
