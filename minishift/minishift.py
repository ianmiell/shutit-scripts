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
 				# 2821  17/08/17 20:12:20 minishift delete
 				# 2822  17/08/17 20:12:38 sudo rm -rf ~/.minishift/
				s1.send('minishift start')
			else:
				s1.send('minishift start --vm-driver virtualbox')
			s1.send('eval $(minishift oc-env)')
	return s1

if __name__ == "__main__":
	s1 = startup()
	s1.send('minishift console')
	s1.interact()
