# Kubo - Interplanetary Filesystem (IPFS) - RPMs for Fedora Linux

IPFS is a global, versioned, peer-to-peer filesystem. It combines good ideas
from Git, BitTorrent, Kademlia, SFS, and the Web. It is like a single
bittorrent swarm, exchanging git objects. IPFS provides an interface as
simple as the HTTP web, but with permanence built in. You can also mount the
world at /ipfs.

For more info about IPFS itself, see: <https://github.com/ipfs/ipfs> and <https://github.com/ipfs/kubo>

---


### Installation

**For Fedora and 64bit only.**

(1) First enable the COPR repository

```sh
sudo dnf install -y dnf-plugins-core distribution-gpg-keys
sudo dnf copr enable taw/ipfs
```

<!--
(1) First install Todd's public GPG key and the `toddpkgs-ipfs-repo` package

```sh
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/ipfs-rpm/master/toddpkgs-ipfs-repo.noarch.rpm
```
-->

(2) Then install IPFS (of the [Kubo](https://github.com/ipfs/kubo) variety) …

```sh
sudo dnf install -y kubo --refresh
```

(3) Join the `ipfs` group so you have access to `ipfs`, the application

> *Note, I, personally, create a user `ipfsuser` on my servers and give
> permission only to that user to run IPFS. And I run kubo (ipfs) as a systemd
> service. (In that case, replace `$USER` with `ipfsuser`.) Adapt these generic
> instructions to match your usage model.*


```sh
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

&nbsp;

### Where is everything installed?

```sh
rpm -ql kubo
ls -lh /usr/bin/ipfs
```

### How to use

- Browse to <https://docs.ipfs.tech> and <https://ipfs.io/> and read the docs. 

### See also

- The Fedora RPM build github repo: <https://github.com/taw00/ipfs-rpm>
- The upstream Kubo project: <https://github.com/ipfs/kubo>
- The upstream IPFS project: <https://github.com/ipfs/ipfs>

---

## Enjoy

Comments and feedback: t0dd\@protonmail\.com
