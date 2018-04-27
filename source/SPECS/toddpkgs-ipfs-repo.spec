Name:		toddpkgs-ipfs-repo
Version:	1.0
Release:	1%{?dist}.taw0
Summary:	Repository configuration to enable management of IPFS packages

License:	MIT
URL:		https://github.com/taw00/ipfs-rpm
Source0:	https://raw.githubusercontent.com/taw00/ipfs-rpm/master/source/SOURCES/toddpkgs-ipfs-repo-1.0.tar.gz
BuildArch:	noarch

# CentOS/RHEL/EPEL can't do "Suggests:"
%if 0%{?fedora:1}
Suggests:	distribution-gpg-keys-copr
%endif


# pulled out of the description below...
#* For CentOS or RHEL:
#  sudo yum clean expire-cache
#  sudo yum install go-ipfs -y

%description
Todd (aka, taw, taw00, t0dd in various communities) packages applications for
Fedora Linux and RHEL/CentOS/EPEL. This package deploys the repository
configuration file necessary to enable on-going management of the go-ipfs
reference RPM package for Fedora Linux (and perhaps, someday, CentOS and
RHEL).

---

IPFS is a global, versioned, peer-to-peer filesystem. It combines good ideas
from Git, BitTorrent, Kademlia, SFS, and the Web. It is like a single
bittorrent swarm, exchanging git objects. IPFS provides an interface as
simple as the HTTP web, but with permanence built in. You can also mount the
world at /ipfs.

For more info see: https://github.com/ipfs/ipfs

---

Install this (toddpkgs-ipfs-repo), then...

* For fedora:
  sudo dnf install go-ipfs -y --refresh

You can edit /etc/yum.repos.d/ipfs.repo (as root) and 'enable=1' or '0'
whether you want the stable or the testing repositories.

Notes about GPG keys:
* An RPM signing key is included. It is used to sign RPMs that I build by
  hand. Namely any *.src.rpm found in github.com/taw00/ipfs-rpm
* RPMs from the copr repositories are signed by fedoraproject build system
  keys.


%prep
%setup -q
# For debugging purposes...
#cd .. ; tree -df -L 1  ; cd -


%build
# no-op


%install
# Builds generically. Will need a disto specific RPM though.
install -d %{buildroot}%{_sysconfdir}/yum.repos.d
install -d %{buildroot}%{_sysconfdir}/pki/rpm-gpg

install -D -m644 todd-694673ED-public-2030-01-04.2016-11-07.asc %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-todd-694673ED-public

%if 0%{?fedora:1}
  install -D -m644 ipfs-fedora.repo %{buildroot}%{_sysconfdir}/yum.repos.d/ipfs.repo
%else
  %if 0%{?rhel:1}
  # no-op for now
  #install -D -m644 ipfs-epel.repo %%{buildroot}%%{_sysconfdir}/yum.repos.d/ipfs.repo
  %endif
%endif


%files
#%%config(noreplace) %%attr(644, root,root) %%{_sysconfdir}/yum.repos.d/ipfs.repo
%config %attr(644, root,root) %{_sysconfdir}/yum.repos.d/ipfs.repo
%attr(644, root,root) %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-todd-694673ED-public


%changelog
* Thu Apr 26 2018 Todd Warner <t0dd at protonmail.com> 1.0-1.taw
- Initial build

