# Interplanetary Filesystem (IPFS) RPMs for Fedora Linux

This is all still in testing. Quick start...

## Install repository configuration RPM
```sh
# Install Todd's public GPG key and the toddpkgs-ipfs-repo package
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/ipfs-rpm/master/toddpkgs-ipfs-repo.noarch.rpm
```

## Turn on test repo

Right now we only have test RPMs. So, if you are brave...
```sh
# Flip the enabled repository from stable to testing
sudo dnf config-manager --set-disabled ipfs-stable
sudo dnf config-manager --set-enabled ipfs-testing
sudo dnf list | grep ipfs
```

## Install `go-ipfs` and add yourself to the `ipfs` group...

```sh
# Install IPFS
sudo dnf install -y go-ipfs
```
```sh
# Join the ipfs so you have access to ipfs, the application
sudo usermod -a -G ipfs $USER
newgrp -
getent group ipfs
groups

# if you do not see ipfs as one of your groups, force the relogin.
# if, for whatever reason, 'newgrp -' doesn't do what it is suppose to do
sudo su -l $USER
getent group ipfs
groups
```

## Where is everything installed?
```sh
rpm -ql go-ipfs
ls -lh /usr/bin/ipfs
```

## How to use it?

Browse to <https://ipfs.io> and read the docs.

## Enjoy

Comments and feedback: t0dd\@protonmail\.com
