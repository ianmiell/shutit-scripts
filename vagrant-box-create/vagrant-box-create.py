import shutit

# This creates a box

s = shutit.create_session('bash',loglevel='debug',echo=True)
s.send('rm -rf tmpvagrantboxcreate && mkdir tmpvagrantboxcreate && cd tmpvagrantboxcreate')
s.send('vagrant init centos/7')
s.send('vagrant box update')
s.send('vagrant up')
s.login('vagrant ssh')
s.login('sudo su -')
s.send('yum install -y wget vim-enhanced docker git sysstat dnsmasq python epel-release git libselinux-python net-tools bind-utils bash-completion')
s.send(r'''sed -i 's/^\(127.0.0.1[ \t]*[^ \t]*\).*/\1/' /etc/hosts''',note='Make sure chef sees a fqdn.')
s.send('echo root:origin | /usr/sbin/chpasswd',note='set root password')
s.send('wget -qO- https://raw.githubusercontent.com/ianmiell/vagrant-swapfile/master/vagrant-swapfile.sh | sh')


# Workaround for docker networking issues + landrush.
s.insert_text('Environment=GODEBUG=netdns=cgo','/lib/systemd/system/docker.service',pattern='.Service.')
s.send('mkdir -p /etc/docker',note='Create the docker config folder')
# The containers running in the pods take their dns setting from the docker daemon. Add the default kubernetes service ip to the list so that items can be updated.
# Ref: IWT-3895
s.send_file('/etc/docker/daemon.json',"""{
  "dns": ["8.8.8.8"]
}""",note='Use the google dns server rather than the vagrant one. Change to the value you want if this does not work, eg if google dns is blocked.')

s.send(r'''sed -i 's/^\(127.0.0.1[ \t]*[^ \t]*\).*/\1/' /etc/hosts''')                                                                                           
s.send('''sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config''')                                                              
s.send('''sed -i 's/.*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config''')                                                                           
s.send('service sshd restart')                                                                                                                                   
s.multisend('ssh-keygen',{'Enter file':'','Enter passphrase':'','Enter same pass':''})  

s.logout()
s.logout()

s.send('vagrant package')

s.pause_point('Now take the file and upload it to atlas.hashcorp.com')
