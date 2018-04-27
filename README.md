# ipfs-rpm - Interplanetary Filesystem RPMs for Fedora Linux

This is still in testing. Quick start...

## Install repository configuration RPM
```sh
sudo dnf install -y https://raw.githubusercontent.com/taw00/ipfs-rpm/master/toddpkgs-ipfs-repo-1.0-1.fc27.taw0.noarch.rpm
```

## Turn on test repo

Right now we only have test RPMs. So, if you are brave...
```sh
sudo dnf config-manager --set-disabled ipfs-stable
sudo dnf config-manager --set-enabled ipfs-testing
sudo dnf list --refresh|grep ipfs
```

## Install go-ipfs, the reference implementation...

```sh
sudo dnf install -y go-ipfs
```

## Where install?
```sh
rpm -ql go-ipfs
```

## How to use it?

Browse to <https://ipfs.io> and read the docs.

## Enjoy

Comments and feedback: t0dd\@protonmail\.com
