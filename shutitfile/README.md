# ShutItFile Examples 

0) Set up

1) Create file locally if it doesn't exist

2) Create Docker image, commit and push

3) Set up my home server

## 0) Set up

Check out this repo and the example ShutItFiles:

```
sudo pip install --upgrade --force shutit
git clone https://github.com/ianmiell/shutitfile && cd shutitfile
```
                                                                                                                                             

## 1) Create file locally if it doesn't exist

This ShutItFile which creates the file /tmp/shutit_marker on the running host if
it doesn't exist:

```
IF_NOT FILE_EXISTS /tmp/shutit_marker
RUN touch /tmp/shutit_marker
ENDIF
```

Create the above file 'Shutitfile' in a folder.

To run it, install ShutIt and run:

```
shutit skeleton --shutitfile examples/simple_bash.sf --accept
```

follow the instructions.

TODO: video running this twice

This all happened on the local host, and is the default 'bash' mode.

The next example does the same, but creates a simple Docker image.

## 2) Create Docker image, commit and push

```
DELIVERY docker
FROM debian
INSTALL nginx
COMMIT myusername/example_shutitfile:latest
PUSH myusername/example_shutitfile:latest
```

Your Docker credentials need to be in your ~/.shutit/config file, eg:
NB this file is created by ShutIt and stored with 0600 permissions (ie only you
can view it)

```
[repository]
user:myusername
password:mypassword
email:you@example.com
```

## 3) Set up my home server

This more practical example sets up my home server. It also serves as
documentation for what my home servers and other machines typically need.

```
# We assert here that we are running as root
SEND whoami
ASSERT_OUTPUT root

# We assert here the user imiell was set up by the OS installation process
SEND cut -d: -f1 /etc/passwd | grep imiell | wc -l
ASSERT_OUTPUT 1

# Install required packages
INSTALL docker.io
INSTALL openssh-server
INSTALL run-one
INSTALL apache2
INSTALL vim
INSTALL python-pip
INSTALL meld
INSTALL tmux
INSTALL docker-compose
INSTALL openjdk-8-jre
INSTALL alien
INSTALL brasero
INSTALL virtualbox
INSTALL vagrant

# Install ShutIt, naturally
RUN pip install shutit
# Add imiell to the docker user group
RUN usermod -G docker -a imiell 

# Pull my dev tools image from Dockerhub
# Takes a while, so leave out for demo
#RUN docker pull imiell/docker-dev-tools-image

# Set up local storage
RUN mkdir -p /media/storage_{1,2}

# Create space folder and chown it to imiell
RUN mkdir -p /space && chown imiell: /space

# Generate an ssh key
RUN ssh-keygen
# Note that the response to 'already exists' below prevents overwrite here.                                                                                                       
EXPECT_MULTI ['file in which=','empty for no passphrase=','Enter same passphrase again=','already exists=n'] 

# Log me in as imiell
USER imiell
# If it's not been done before, check out my dotfiles and set it up
IF_NOT FILE_EXISTS /home/imiell/.dotfiles
	RUN cd /home/imiell
	RUN git clone --depth=1 https://github.com/ianmiell/dotfiles ~imiell/.dotfiles
	RUN cd .dotfiles
	RUN ./script/bootstrap
	EXPECT_MULTI ['What is your github author name=Ian Miell','What is your github author email=ian.miell@gmail.com','verwrite=O']
ENDIF
LOGOUT
```

[![asciicast](https://asciinema.org/a/48685.png)](https://asciinema.org/a/48685)

Latest version [here](https://github.com/ianmiell/shutit-home-server/blob/master/Shutitfile)

