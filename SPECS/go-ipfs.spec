# go-ipfs.spec
# vim:tw=0:ts=2:sw=2:et:
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
%define sourceIsBinary 1

# ie. if the dev team includes things like rc1 or a date in the source filename
%define buildQualifier rc1
%undefine buildQualifier

# VERSION
%define vermajor 0.5
%define verminor 1
Version: %{vermajor}.%{verminor}


# RELEASE
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 0.1
%endif

# MINORBUMP
%define minorbump taw
#%%define minorbump taw

#
# Build the release string - don't edit this
#

# -- snapinfo
%define _snapinfo testing
%define _repackaged rp
%undefine snapinfo

%if %{targetIsProduction}
  %if %{sourceIsBinary}
    %define snapinfo %{_repackaged}
  %else
    %undefine snapinfo
  %endif
%else
  %if %{sourceIsBinary}
    %define snapinfo %{_snapinfo}.%{_repackaged}
  %else
    %define snapinfo %{_snapinfo}
  %endif
%endif

# -- _release
# pkgrel will always be defined, snapinfo and minorbump may not be
%define _release %{_pkgrel}
%if 0%{?snapinfo:1}
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section


# Project tree structure in .../BUILD directory:
#   projectroot               go-ipfs-0.4
#      \_sourcetree             \_go-ipfs-0.4.19
#      \_sourcetree_contrib     \_go-ipfs-0.4-contrib
#      \_ _gopath               \_go

%define projectroot %{name}-%{vermajor}
%define sourcetree_contrib %{name}-%{vermajor}-contrib

%if 0%{?buildQualifier:1}
  %define sourcearchivename %{name}-%{version}-%{buildQualifier}
  %define sourcetree %{sourcearchivename}-%{buildQualifier}
%else
  %define sourcearchivename %{name}-%{version}
  %define sourcetree %{sourcearchivename}
%endif

%define binaryarchivename %{name}_v%{version}_linux-amd64
%define binarytree %{name}

%define _gopath %{_builddir}/%{projectroot}/go
%define _gobin %{_gopath}/bin
%define gopathtosrc %{_gopath}/src/github.com/ipfs/go-ipfs

# /usr/share/ipfs
%define installtree %{_datadir}/%{name2}


%if ! %{sourceIsBinary}
%if 0%{?buildQualifier:1}
Source0: https://github.com/dashpay/dash/archive/v%{version}-%{buildQualifier}/%{sourcearchivename}.tar.gz
%else
Source0: https://github.com/dashpay/dash/archive/v%{version}/%{sourcearchivename}.tar.gz
%endif
%endif

Source1: https://raw.githubusercontent.com/taw00/ipfs-rpm/master/SOURCES/%{name}-%{vermajor}-contrib.tar.gz

%if %{sourceIsBinary}
Source2: https://raw.githubusercontent.com/taw00/ipfs-rpm/master/SOURCES/%{binaryarchivename}.tar.gz
%endif



# Most of the time, the build system can figure out the requires.
# But if you need something specific...
#Requires:

%if ! %{targetIsProduction}
BuildRequires: tree vim-enhanced less findutils
%endif

%if ! %{sourceIsBinary}
BuildRequires: git
%endif

# Go language specific stuff.
# https://fedoraproject.org/wiki/PackagingDrafts/Go
#%%global import_path code.google.com/p/go.net
# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
#ExclusiveArch:  %%{ix86} x86_64 %%{arm} aarch64 ppc64le s390x
ExclusiveArch: x86_64
%if ! %{sourceIsBinary}
#BuildRequires:  %%{?go_compiler:compiler(go-compiler)}%%{!?go_compiler:golang}
#BuildRequires:  golang(github.com/gorilla/mux) >= 0-0.13
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/dict) = %{version}-%{release}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  golang >= 1.11
%endif

License: MIT
URL: https://github.com/taw00/ipfs-rpm
# Group is deprecated. Don't use it. Left this here as a reminder...
# https://fedoraproject.org/wiki/RPMGroups 
#Group: Unspecified

# CHANGE or DELETE this for your package
# System user for the systemd ipfsd.service.
# If you want to retain the systemd service configuration and you therefore
# change this, you will have to dig into the various -contrib configuration
# files to change things there as well.
%define systemuser ipfs
%define systemgroup ipfs

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

%if 0%{?rhel} && 0%{?rhel} < 8
  %{error: "EL7 builds no longer supported due to outdated build tools (golang version in particular)"}
  exit 1
%endif

%if 0%{?fedora} && 0%{?fedora} < 29
  %{error: "Build requires Fedora 29 or better due to outdated build tools (golang version in particular)"}
  exit 1
%endif

mkdir -p %{projectroot}
%if %{sourceIsBinary}
# binary
%setup -q -T -D -a 2 -n %{projectroot}
%else
# sourcecode
%setup -q -T -D -a 0 -n %{projectroot}
%endif
# contrib
%setup -q -T -D -a 1 -n %{projectroot}

%if ! %{sourceIsBinary}
# TODO: This is confusing. Simplify/clarify it.
# {projectroot}/go/src/github.com/ipfs/go-ipfs -> /.../BUILD/{name}-{vermajor}/{name}-{version}
mkdir -p %{gopathtosrc} %{_gobin}
rmdir %{gopathtosrc} # pop the last dir
ln -s %{_builddir}/%{projectroot}/%{sourcetree} %{gopathtosrc}
ls -l %{gopathtosrc}
%endif

%if ! %{targetIsProduction}
%if %{sourceIsBinary}
tree -d %{_builddir}/%{projectroot}/%{binarytree}
%else
tree -d %{_builddir}/%{projectroot}/%{sourcetree}
%endif
%endif

# Libraries ldconfig file - we create it, because lib or lib64
echo "%{_libdir}/%{name2}" > %{sourcetree_contrib}/etc-ld.so.conf.d_%{name2}.conf

# For debugging purposes...
%if ! %{targetIsProduction}
cd .. ; /usr/bin/tree -df -L 1 %{projectroot} ; cd -
%endif


%build
# This section starts us in directory {_builddir}/{projectroot}

%if ! %{sourceIsBinary}
cd %{sourcetree}
export GOPATH=%{_gopath}
export GOBIN=%{_gobin}
# temporary - for testing RPM basic build structure
# (uncomment this touch and comment out make install)
#touch %{_gobin}/ipfs
make build GOFLAGS=-tags=openssl
make install
%endif


%install
# This section starts us in directory {_builddir}/{projectroot}
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
# These two are defined in RPM versions in newer versions of Fedora (not el7)
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
install -d %{buildroot}%{_sharedstatedir}/%{name2}/repo
# /var/log/ipfs/
install -d -m750 %{buildroot}%{_localstatedir}/log/%{name2}
# /usr/share/ipfs/
install -d %{buildroot}%{installtree}

# /ipfs/ -- directory for mountpoints ipfs and ipfn
# Might end up building script for folks to do by username: /ipfs/todd/
# The systemd service allocates /ipfs/ipfsd.service/[ipfs,ipfn]
install -d %{buildroot}/%{name2}
install -d %{buildroot}/%{name2}/%{name2}d
install -d %{buildroot}/%{name2}/%{name2}d.service/ipfs
install -d %{buildroot}/%{name2}/%{name2}d.service/ipfn
#install -d %%{buildroot}%%{name2}/%%{ipfs}
#install -d %%{buildroot}%%{name2}/%%{ipfn}

# Systemd...
# /usr/lib/systemd/system/ -- 
install -d %{buildroot}%{_unitdir}
# /etc/sysconfig/ipfsd-scripts/
install -d %{buildroot}%{_sysconfdir}/sysconfig/%{name2}d-scripts
# /usr/lib/tmpfiles.d/
install -d %{buildroot}%{_tmpfilesdir}

# For now, we just install the binary in /usr/bin
# Only members of the ipfs can do stuff with ipfs
%if %{sourceIsBinary}
install -D -m750 %{binarytree}/ipfs %{buildroot}%{_bindir}/
%else

install -D -m750 %{_gobin}/ipfs %{buildroot}%{_bindir}/

# Bash completion
# /usr/share/bash-completion/completions/...
install -D -m644 %{sourcetree}/misc/completion/ipfs-completion.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name2}
%endif

# Systemd services
install -D -m600 -p %{sourcetree_contrib}/systemd/etc-sysconfig_ipfsd %{buildroot}%{_sysconfdir}/sysconfig/%{name2}d
install -D -m755 -p %{sourcetree_contrib}/systemd/etc-sysconfig-ipfsd-scripts_send-email.sh %{buildroot}%{_sysconfdir}/sysconfig/%{name2}d-scripts/send-email.sh
install -D -m755 -p %{sourcetree_contrib}/systemd/etc-sysconfig-ipfsd-scripts_ipfsd-init.sh %{buildroot}%{_sysconfdir}/sysconfig/%{name2}d-scripts/%{name2}d-init.sh
install -D -m755 -p %{sourcetree_contrib}/systemd/etc-sysconfig-ipfsd-scripts_write-to-journal.sh %{buildroot}%{_sysconfdir}/sysconfig/%{name2}d-scripts/write-to-journal.sh
install -D -m644 -p %{sourcetree_contrib}/systemd/usr-lib-systemd-system_ipfsd.service %{buildroot}%{_unitdir}/%{name2}d.service
install -D -m644 -p %{sourcetree_contrib}/systemd/usr-lib-tmpfiles.d_ipfsd.conf %{buildroot}%{_tmpfilesdir}/%{name2}d.conf

# Service definition files for firewalld
install -D -m644 -p %{sourcetree_contrib}/firewalld/usr-lib-firewalld-services_ipfs-api.xml %{buildroot}%{_prefix}/lib/firewalld/services/%{name2}-api.xml
install -D -m644 -p %{sourcetree_contrib}/firewalld/usr-lib-firewalld-services_ipfs-gateway.xml %{buildroot}%{_prefix}/lib/firewalld/services/%{name2}-gateway.xml


%files
# CREATING RPM:
# - files step (final step)
# - This step makes a declaration of ownership of any listed directories
#   or files
# - The install step should have set permissions and ownership correctly,
#   but of final tweaking is often done in this section
#
%defattr(-,root,root,-)
%if %{sourceIsBinary}
%license %{binarytree}/LICENSE
%doc %{binarytree}/README.md
%else
%license %{sourcetree}/LICENSE
%doc %{sourcetree}/CHANGELOG.md
%doc %{sourcetree}/CONTRIBUTING.md
%doc %{sourcetree}/CODEOWNERS
%doc %{sourcetree}/ISSUE_TEMPLATE.md
%doc %{sourcetree}/docs/*.md
%doc %{sourcetree}/docs/developer-certificate-of-origin
%doc %{sourcetree}/docs/*.png
%doc %{sourcetree}/docs/AUTHORS
%endif

# The directories...
# /etc/ipfs/
#%%dir %%attr(750,%%{systemuser},%%{systemgroup}) %%{_sysconfdir}/%%{name2}
# /var/log/ipfs/
#%%dir %%attr(750,%%{systemuser},%%{systemgroup}) %%{_localstatedir}/log/%%{name2}
# /etc/sysconfig/ipfsd-scripts/
#%%dir %%attr(755,%%{systemuser},%%{systemgroup}) %%{_sysconfdir}/sysconfig/%%{name2}d-scripts
# /usr/share/ipfs/
#%%dir %%attr(755,%%{systemuser},%%{systemgroup}) %%{_datadir}/%%{name2}
# /usr/[lib,lib64]/ipfs/
#%%dir %%attr(755,root,root) %%{_libdir}/%%{name2}

# /var/lib/ipfs/ -- also ipfs user's $HOME dir
%dir %attr(750,%{systemuser},%{systemgroup}) %{_sharedstatedir}/%{name2}
# repo needs to be more secure since there is a private key involved...
%dir %attr(700,%{systemuser},%{systemgroup}) %{_sharedstatedir}/%{name2}/repo

# firewalld service definition
%{_prefix}/lib/firewalld/services/%{name2}-api.xml
%{_prefix}/lib/firewalld/services/%{name2}-gateway.xml

# systemd service definitions, scripts, configuration
%{_unitdir}/%{name2}d.service
%{_tmpfilesdir}/%{name2}d.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/%{name2}d
%attr(755,root,root) %{_sysconfdir}/sysconfig/%{name2}d-scripts/send-email.sh
%attr(755,root,root) %{_sysconfdir}/sysconfig/%{name2}d-scripts/%{name2}d-init.sh
%attr(755,root,root) %{_sysconfdir}/sysconfig/%{name2}d-scripts/write-to-journal.sh

# application configuration when run as systemd service
#%%config(noreplace) %%attr(640,%%{systemuser},%%{systemgroup}) %%{_sysconfdir}/ipfs/ipfs.conf


# Mountpoints
%dir %attr(770,%{systemuser},%{systemgroup}) /%{name2}
%dir %attr(750,%{systemuser},%{systemgroup}) /%{name2}/ipfsd.service
%dir %attr(750,%{systemuser},%{systemgroup}) /%{name2}/ipfsd.service/ipfs
%dir %attr(750,%{systemuser},%{systemgroup}) /%{name2}/ipfsd.service/ipfn

# Bash completion
%if ! %{sourceIsBinary}
# /usr/share/bash-completion/completions/...
%{_datadir}/bash-completion/completions/%{name2}
%endif

# Binaries
%attr(750,%{systemuser},%{systemgroup}) %{_bindir}/ipfs


%pre
# INSTALLING THE RPM:
# - pre section (runs before the install process)
# - system users are added if needed. Any other roadbuilding.
#
# You have to be a member of ipfs in order to use ipfs
# /var/lib/ipfs/ is the homedir of ipfs
getent group %{systemgroup} >/dev/null || groupadd -r %{systemgroup}
getent passwd %{systemuser} >/dev/null || useradd -r -g %{systemgroup} -d %{_sharedstatedir}/%{name2} -s /sbin/nologin -c "System user '%{systemuser}' to isolate execution" %{systemuser}


%post
# INSTALLING THE RPM:
# - post section (runs after the install process is complete)
#
umask 007
# refresh library context
/sbin/ldconfig > /dev/null 2>&1
# refresh systemd context
test -e %{_sysconfdir}/%{name2}/%{name2}.conf && %systemd_post %{name2}d.service
# refresh firewalld context
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


%postun
# UNINSTALLING THE RPM:
# - postun section (runs after an RPM has been removed)
#
umask 007
# refresh library context
/sbin/ldconfig > /dev/null 2>&1
# refresh firewalld context
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


#%clean
## Once needed if you are building on old RHEL/CentOS.
## No longer used.
#rm -rf %{buildroot}


%changelog
* Thu May 14 2020 Todd Warner <t0dd_at_protonmail.com> 0.5.1-0.1.testing.rp.taw
  - 0.5.1 repackage - binary build

* Mon Feb 17 2020 Todd Warner <t0dd_at_protonmail.com> 0.4.23-0.1.testing.rp.taw
  - 0.4.23 repackage - binary build

* Wed Aug 14 2019 Todd Warner <t0dd_at_protonmail.com> 0.4.22-0.1.testing.rp.taw
  - 0.4.22 repackage - binary build

* Mon Jun 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.4.21-0.3.testing.rp.taw
  - 0.4.21 repackage - binary build

* Mon Jun 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.4.21-0.2.testing.taw
* Sun Jun 23 2019 Todd Warner <t0dd_at_protonmail.com> 0.4.21-0.1.testing.taw
  - 0.4.21 FAILED
  - prestine source will not build (Fedora 29 and 30 don't ship go-1.12)
  - modified go.mod and mk/golang.mk to allow 1.11  
    still fails, but for other reasons
  - not successfully building yet

* Fri Apr 19 2019 Todd Warner <t0dd_at_protonmail.com> 0.4.20-0.1.testing.taw
  - 0.4.20 FAILED
  - not successfully building yet

* Sat Apr 06 2019 Todd Warner <t0dd_at_protonmail.com> 0.4.19-0.2.testing.taw
  - minor overhaul of the specfile
  - systemgroup is now ipfs instead of ipfsgroup -- please manually  
    `groupdel ipfsgroup` after upgrading to this version

* Wed Mar 06 2019 Todd Warner <t0dd_at_protonmail.com> 0.4.19-0.1.testing.taw
  - 0.4.19
  - the manifest of docs changed a bit... updated in specfile

* Tue Dec 25 2018 Todd Warner <t0dd_at_protonmail.com> 0.4.18-0.1.testing.taw
  - 0.4.18
  - spec file updates

* Thu May 10 2018 Todd Warner <t0dd_at_protonmail.com> 0.4.14-0.2.testing.taw1
  - spec file: mkdir -p and not just mkdir

* Tue May 1 2018 Todd Warner <t0dd_at_protonmail.com> 0.4.14-0.2.testing.taw0
  - Default mountpoints added. Not sure if this correct best practice.
  - Systemd service and associated configuration and scripts were added.
  - firewalld service description files added.

* Thu Apr 26 2018 Todd Warner <t0dd_at_protonmail.com> 0.4.14-0.1.testing.taw[n]
  - Initial test build.
