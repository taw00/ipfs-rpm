# go-ipfs.spec
#
# IPFS implementation in Go.
#
# IPFS is a global, versioned, peer-to-peer filesystem. It combines good ideas
# from Git, BitTorrent, Kademlia, SFS, and the Web. It is like a single
# bittorrent swarm, exchanging git objects. IPFS provides an interface as
# simple as the HTTP web, but with permanence built in. You can also mount the
# world at /ipfs.
#
# For more info see: https://github.com/ipfs/ipfs.

# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]
Name: go-ipfs
%define name2 ipfs
Summary: IPFS reference implementation.

%define targetIsProduction 0
%define includeSnapinfo 1
%define includeMinorbump 1
%define sourceIsPrebuilt 0


# VERSION
# eg. 1.0.1
%define vermajor 0.4
%define verminor 14
Version: %{vermajor}.%{verminor}


# RELEASE
# if production - "targetIsProduction 1"
%define pkgrel_prod 1

# if pre-production - "targetIsProduction 0"
# eg. 0.3.testing
%define pkgrel_preprod 0
%define extraver_preprod 1
%define snapinfo testing
#%%define snapinfo testing.20180424
#%%define snapinfo beta2.41d5c63.gh

# if sourceIsPrebuilt (rp=repackaged)
# eg. 1.rp (prod) or 0.3.testing.rp (pre-prod)
%define snapinfo_rp rp

# if includeMinorbump
%define minorbump taw0

# Building the release string (don't edit this)...

%if %{targetIsProduction}
  %if %{includeSnapinfo}
    %{warn:"Warning: target is production and yet you want snapinfo included. This is not typical."}
  %endif
%else
  %if ! %{includeSnapinfo}
    %{warn:"Warning: target is pre-production and yet you elected not to incude snapinfo (testing, beta, ...). This is not typical."}
  %endif
%endif

# release numbers
%undefine _relbuilder_pt1
%if %{targetIsProduction}
  %define _pkgrel %{pkgrel_prod}
  %define _relbuilder_pt1 %{pkgrel_prod}
%else
  %define _pkgrel %{pkgrel_preprod}
  %define _extraver %{extraver_preprod}
  %define _relbuilder_pt1 %{_pkgrel}.%{_extraver}
%endif

# snapinfo and repackage (pre-built) indicator
%undefine _relbuilder_pt2
%if ! %{includeSnapinfo}
  %undefine snapinfo
%endif
%if ! %{sourceIsPrebuilt}
  %undefine snapinfo_rp
%endif
%if 0%{?snapinfo_rp:1}
  %if 0%{?snapinfo:1}
    %define _relbuilder_pt2 %{snapinfo}.%{snapinfo_rp}
  %else
    %define _relbuilder_pt2 %{snapinfo_rp}
  %endif
%else
  %if 0%{?snapinfo:1}
    %define _relbuilder_pt2 %{snapinfo}
  %endif
%endif

# put it all together
# pt1 will always be defined. pt2 and minorbump may not be
%define _release %{_relbuilder_pt1}
%if ! %{includeMinorbump}
  %undefine minorbump
%endif
%if 0%{?_relbuilder_pt2:1}
  %if 0%{?minorbump:1}
    %define _release %{_relbuilder_pt1}.%{_relbuilder_pt2}%{?dist}.%{minorbump}
  %else
    %define _release %{_relbuilder_pt1}.%{_relbuilder_pt2}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_relbuilder_pt1}%{?dist}.%{minorbump}
  %else
    %define _release %{_relbuilder_pt1}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section

# You should use URLs for sources.
# https://fedoraproject.org/wiki/Packaging:SourceURL
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-%{vermajor}-contrib.tar.gz

# Most of the time, the build system can figure out the requires.
# But if you need something specific...
#Requires:

BuildRequires: tree git

# Go language specific stuff.
# https://fedoraproject.org/wiki/PackagingDrafts/Go
#%%global import_path code.google.com/p/go.net
# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64 ppc64le s390x
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires:  golang(github.com/gorilla/mux) >= 0-0.13
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/dict) = %{version}-%{release}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  golang

# CentOS/RHEL/EPEL can't do "Suggests:"
%if 0%{?fedora:1}
#Suggests:
%endif

License: MIT
URL: https://github.com/taw00/ipfs-rpm
# Group is deprecated. Don't use it. Left this here as a reminder...
# https://fedoraproject.org/wiki/RPMGroups 
#Group: Unspecified

# CHANGE or DELETE this for your package
# System user for the systemd ipfsd.service.
# If you want to retain the systemd service configuration and you therefore
# change this, you will have to dig into the various -contrib configuration
# files to change things there as well. 
%define systemuser ipfs
%define systemgroup ipfsgroup

# If you comment out "debug_package" RPM will create additional RPMs that can
# be used for debugging purposes. I am not an expert at this, BUT ".build_ids"
# are associated to debug packages, and I have lately run into packaging
# conflicts because of them. This is a topic I can't share a whole lot of
# wisdom about, but for now... I turn all that off.
#
# How debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
# https://fedoraproject.org/wiki/Packaging:Guidelines#PIE
%define _hardened_build 1

# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               {name}-1.0
#      \_ srccodetree       \_{name}-1.0.1
#      \_ srccontribtree    \_{name}-1.0-contrib
%define srcroot %{name}-%{vermajor}
%define srccodetree %{name}-%{version}
%define srccontribtree %{name}-%{vermajor}-contrib
# /usr/share/ipfs
%define installtree %{_datadir}/%{name2}

%define _gopath %{_builddir}/%{srcroot}/go
%define _gobin %{_gopath}/bin
%define gopathtosrc %{_gopath}/src/github.com/ipfs/go-ipfs



%description
IPFS implementation in Go.

IPFS is a global, versioned, peer-to-peer filesystem. It combines good ideas
from Git, BitTorrent, Kademlia, SFS, and the Web. It is like a single
bittorrent swarm, exchanging git objects. IPFS provides an interface as
simple as the HTTP web, but with permanence built in. You can also mount the
world at /ipfs.

For more info see: https://github.com/ipfs/ipfs.
 


%prep
# Prep section starts us in directory .../BUILD -or- {_builddir}
#
# I create a root dir and place the source and contribution trees under it.
# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               {name}-<vermajor>
#      \_ srccodetree        \_{name}-<version>
#      \_ go                 \_go/src/github.com/ipfs/go-ipfs -> .../{name}-{version}
#      \_ srccontribtree     \_{name}-<vermajor>-contrib

mkdir %{srcroot}
# sourcecode
%setup -q -T -D -a 0 -n %{srcroot}
# contrib
%setup -q -T -D -a 1 -n %{srcroot}

# go/src/github.com/ipfs/go-ipfs -> /.../BUILD/{name}-{vermajor}/{name}-{version}
mkdir -p %{gopathtosrc} %{_gobin}
rmdir %{gopathtosrc} # pop the last dir
ln -s %{_builddir}/%{srcroot}/%{srccodetree} %{gopathtosrc}
ls -l %{gopathtosrc}
tree -d %{_builddir}/%{srcroot}/%{srccodetree}


# Libraries ldconfig file - we create it, because lib or lib64
echo "%{_libdir}/%{name2}" > %{srccontribtree}/etc-ld.so.conf.d_%{name2}.conf

# For debugging purposes...
cd .. ; /usr/bin/tree -df -L 1 %{srcroot} ; cd -


%build
# This section starts us in directory {_builddir}/{srcroot}

cd %{srccodetree}
export GOPATH=%{_gopath}
export GOBIN=%{_gobin}
make install


%install
# This section starts us in directory {_builddir}/{srcroot}
#
# Cheatsheet for built-in RPM macros:
#   _bindir = /usr/bin
#   _sbindir = /usr/sbin
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix = /usr
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
#   https://fedoraproject.org/wiki/Packaging:RPMMacros
# These two are defined in RPM versions in newer versions of Fedora (not el7)
%define _tmpfilesdir /usr/lib/tmpfiles.d
%define _unitdir /usr/lib/systemd/system

# Create directories
# /usr/bin and /usr/sbin/
install -d -m755 -p %{buildroot}%{_bindir}
#install -d -m755 -p %%{buildroot}%%{_sbindir}

# Do we want to make ipfs a system thing?
# /etc/ipfs/
install -d %{buildroot}%{_sysconfdir}/%{name2}
# /var/lib/ipfs/
install -d %{buildroot}%{_sharedstatedir}/%{name2}
# /var/log/ipfs/
install -d -m750 %{buildroot}%{_localstatedir}/log/%{name2}
# /usr/share/ipfs/
install -d %{buildroot}%{installtree}

# Systemd... - Do we want to make ipfs a service?
# /usr/lib/systemd/system/ -- 
install -d %{buildroot}%{_unitdir}
# /etc/sysconfig/ipfsd-scripts/
install -d %{buildroot}%{_sysconfdir}/sysconfig/%{name2}d-scripts
# /usr/lib/tmpfiles.d/
install -d %{buildroot}%{_tmpfilesdir}

# For now, we just install the binary in /usr/bin
# Only members of the ipfsgroup can do stuff with ipfs
install -D -m750 %{_gobin}/%{name2} %{buildroot}%{_bindir}/

# Bash completion
# /usr/share/bash-completion/completions/...
install -D -m644 %{srccodetree}/misc/completion/%{name2}-completion.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name2}


%files
# CREATING RPM:
# - files step (final step)
# - This step makes a declaration of ownership of any listed directories
#   or files
# - The install step should have set permissions and ownership correctly,
#   but of final tweaking is often done in this section
#
%defattr(-,root,root,-)
%license %{srccodetree}/LICENSE
%doc %{srccodetree}/docs/plugins.md %{srccodetree}/docs/transports.md
%doc %{srccodetree}/docs/implement-api-bindings.md %{srccodetree}/docs/github-issue-guide.md
%doc %{srccodetree}/docs/fuse.md %{srccodetree}/docs/file-transfer.md
%doc %{srccodetree}/docs/debug-guide.md %{srccodetree}/docs/config.md
%doc %{srccodetree}/docs/datastores.md %{srccodetree}/docs/experimental-features.md
%doc %{srccodetree}/docs/releases.md

# The directories...
# /etc/ipfs/
#%%dir %%attr(750,%%{systemuser},%%{systemgroup}) %%{_sysconfdir}/%%{name2}
# /var/lib/ipfs/ -- also ipfs user's $HOME dir
%dir %attr(750,%{systemuser},%{systemgroup}) %{_sharedstatedir}/%{name2}
# /var/log/ipfs/
#%%dir %%attr(750,%%{systemuser},%%{systemgroup}) %%{_localstatedir}/log/%%{name2}
# /etc/sysconfig/ipfsd-scripts/
#%%dir %%attr(755,%%{systemuser},%%{systemgroup}) %%{_sysconfdir}/sysconfig/%%{name2}d-scripts
# /usr/share/ipfs/
#%%dir %%attr(755,%%{systemuser},%%{systemgroup}) %%{_datadir}/%%{name2}
# /usr/[lib,lib64]/ipfs/
#%%dir %%attr(755,root,root) %%{_libdir}/%%{name2}

# Bash completion
# /usr/share/bash-completion/completions/...
%{_datadir}/bash-completion/completions/%{name2}

# Binaries
%{_bindir}/ipfs


%pre
# INSTALLING THE RPM:
# - pre section (runs before the install process)
# - system users are added if needed. Any other roadbuilding.
#
# You have to be a member of ipfsgroup in order to use ipfs
# /var/lib/ipfs/ is the homedir of ipfs
getent group %{systemgroup} >/dev/null || groupadd -r %{systemgroup}
getent passwd %{systemuser} >/dev/null || useradd -r -g %{systemgroup} -d %{_sharedstatedir}/%{name2} -s /sbin/nologin -c "System user '%{systemuser}' to isolate execution" %{systemuser}


%post
# INSTALLING THE RPM:
# - post section (runs after the install process is complete)
#
umask 007
# refresh library context
/sbin/ldconfig > /dev/null 2>&1
# refresh systemd context
test -e %{_sysconfdir}/%{name2}/%{name2}.conf && %systemd_post %{name2}d.service
# refresh firewalld context
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


%postun
# UNINSTALLING THE RPM:
# - postun section (runs after an RPM has been removed)
#
umask 007
# refresh library context
/sbin/ldconfig > /dev/null 2>&1
# refresh firewalld context
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


#%clean
## Once needed if you are building on old RHEL/CentOS.
## No longer used.
#rm -rf %{buildroot}


%changelog
* Thu Apr 26 2018 Todd Warner <t0dd@protonmail.com> 0.4.14-0.1.testing.taw0
- Initial test build.