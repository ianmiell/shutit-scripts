import shutit

# This creates a box

s = shutit.create_session('bash',loglevel='debug',echo=True)
s.send('rm -rf tmpvagrantboxcreate && mkdir tmpvagrantboxcreate && cd tmpvagrantboxcreate')
s.send('vagrant init centos/7')
s.send('vagrant box update')
s.send('vagrant up')
s.login('vagrant ssh')
s.login('sudo su -')
s.multisend('yum install -y wget vim-enhanced docker git sysstat dnsmasq python epel-release git libselinux-python net-tools bind-utils bash-completion dkms kernel-devel',{'s this ok':'y'})
s.multisend('yum groupinstall "Development Tools"',{'s this ok':'y'})
s.send(r'''sed -i 's/^\(127.0.0.1[ \t]*[^ \t]*\).*/\1/' /etc/hosts''',note='Make sure chef sees a fqdn.')
s.send('echo root:origin | /usr/sbin/chpasswd',note='set root password')
s.send('wget -qO- https://raw.githubusercontent.com/ianmiell/vagrant-swapfile/master/vagrant-swapfile.sh | sh')

# Downloads
s.send('wget -nc -q https://packages.chef.io/files/stable/chef/13.5.3/el/7/chef-13.5.3-1.el7.x86_64.rpm')
s.send('wget -nc -q https://packages.chef.io/files/stable/chefdk/2.3.4/el/7/chefdk-2.3.4-1.el7.x86_64.rpm')
s.send('https://github.com/ianmiell/shutit-chef-env/raw/master/chef-server-core-12.17.3-1.el7.x86_64.rpm.xaa')
s.send('https://github.com/ianmiell/shutit-chef-env/raw/master/chef-server-core-12.17.3-1.el7.x86_64.rpm.xab')
s.send('https://github.com/ianmiell/shutit-chef-env/raw/master/chef-server-core-12.17.3-1.el7.x86_64.rpm.xac')
s.send('cat chef-server-core-12.17.3-1.el7.x86_64.rpm.xaa chef-server-core-12.17.3-1.el7.x86_64.rpm.xab chef-server-core-12.17.3-1.el7.x86_64.rpm.xac > chef-server-core-12.17.3-1.el7.x86_64.rpm')
s.send('rm -f *xaa *xab *xac')

# Guest additions
s.send('wget http://download.virtualbox.org/virtualbox/5.2.2/VBoxGuestAdditions_5.2.2.iso')
s.send('mount -t iso9660 -o loop ./VBoxGuestAdditions_*.iso /mnt')
s.send('cd /mnt')
s.send('./VBoxLinuxAdditions.run')
s.send('cd -')


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
