import shutit

s1 = shutit.create_session(echo=True,loglevel='info')
s2 = shutit.create_session(echo=True,loglevel='info')

s1.send('vagrant up')
s1.login('vagrant ssh master1')

s2.login('vagrant ssh master2')

s1.login('sudo su -')
s2.login('sudo su -')
s1.send('sleep 10 && reboot &')
s2.send('sleep 10 && reboot &')
s1.logout()
s1.logout()
s2.logout()
s2.logout()

s1.send('sleep 30')
s1.login('vagrant ssh master1')
s1.logout()

print 'OK'
