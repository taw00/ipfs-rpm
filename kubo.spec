# kubo.spec
# vim:tw=0:ts=2:sw=2:et:
#
# Kubo: IPFS implementation in Go.
#
# IPFS is a global, versioned, peer-to-peer filesystem. It combines good ideas
# from Git, BitTorrent, Kademlia, SFS, and the Web. It is like a single
# bittorrent swarm, exchanging git objects. IPFS provides an interface as
# simple as the HTTP web, but with permanence built in. You can also mount the
# world at /ipfs.
#
# For more info see: https://github.com/ipfs/ipfs.

# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]
Name: kubo
%define name2 ipfs
Summary: IPFS reference implementation.

# Not currently used
%define appid tech.ipfs.%{name}

%define isTestBuild 1
%define sourceIsBinary 1


# VERSION
%define vermajor 0.31
%define verminor 0
Version: %{vermajor}.%{verminor}


# RELEASE
%define _pkgrel 1
%if %{isTestBuild}
  %define _pkgrel 0.2
%endif

# MINORBUMP
%define minorbump taw

#
# Build the release string - don't edit this
#

# -- snapinfo
%define _snapinfo testing
%define _repackaged rp
%undefine snapinfo

%if %{isTestBuild}
  %define snapinfo %{_snapinfo}.%{_repackaged}
%else
  %define snapinfo %{_repackaged}
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
#   projectroot               kubo-0.31
#      \_sourcetree             \_kubo-0.31.0
#      \_sourcetree_contrib     \_kubop-contrib
#      \_ _gopath               \_go

%define projectroot %{name}-%{vermajor}
%define sourcetree_contrib %{name}-contrib

%define binaryarchivename %{name}_v%{version}_linux-amd64
%define binarytree %{name}

%define _gopath %{_builddir}/%{projectroot}/go
%define _gobin %{_gopath}/bin
%define gopathtosrc %{_gopath}/src/github.com/ipfs/go-ipfs

Source1: https://raw.githubusercontent.com/taw00/ipfs-rpm/master/SOURCES/%{name}-contrib.tar.gz
Source2: https://github.com/ipfs/kubo/releases/download/v%{version}/%{binaryarchivename}.tar.gz

# Most of the time, the build system can figure out the requires.
# But if you need something specific...
Requires: fuse

%if %{isTestBuild}
BuildRequires: tree vim-enhanced less findutils
%endif

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
#ExclusiveArch:  %%{ix86} x86_64 %%{arm} aarch64 ppc64le s390x
ExclusiveArch: x86_64

# Name of package changed from go-ipfs to kubo
Provides: go-ipfs = 0.16.0
Obsoletes: go-ipfs < 0.16.0

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

For more info see:
https://github.com/ipfs/ipfs https://ipfs.io and https://docs.ipfs.tech/



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
%if 0%{?fedora} && 0%{?fedora} < 35
  %{error: "Build requires Fedora 35 or better."}
  exit 1
%endif


mkdir -p %{projectroot}
# binary
%setup -q -T -D -a 2 -n %{projectroot}
# contrib
%setup -q -T -D -a 1 -n %{projectroot}

%if %{isTestBuild}
tree -d %{_builddir}/%{projectroot}/%{binarytree}
%endif

# Libraries ldconfig file - we create it, because lib or lib64
echo "%{_libdir}/%{name2}" > %{sourcetree_contrib}/etc-ld.so.conf.d_%{name2}.conf

# For debugging purposes...
%if %{isTestBuild}
cd .. ; /usr/bin/tree -df -L 1 %{projectroot} ; cd -
%endif


%build
# This section starts us in directory {_builddir}/{projectroot}


%install
# This section starts us in directory {_builddir}/{projectroot}
#
# Cheatsheet for built-in RPM macros:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/
#   _builddir = {_topdir}/BUILD
#   _buildrootdir = {_topdir}/BUILDROOT
#   buildroot = {_buildrootdir}/{name}-{version}-{release}.{_arch}
#   _bindir = /usr/bin
#   _sbindir = /usr/sbin
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix = /usr
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
# The _rawlib define is used to quiet rpmlint who can't seem to understand
# that /usr/lib is still used for certain things.
%define _rawlib lib
%define _usr_lib /usr/%{_rawlib}
# These three are defined in some versions of RPM and not in others.
%if ! 0%{?_unitdir:1}
  %define _unitdir %{_usr_lib}/systemd/system
%endif
%if ! 0%{?_tmpfilesdir:1}
  %define _tmpfilesdir %{_usr_lib}/tmpfiles.d
%endif
%if ! 0%{?_metainfodir:1}
  %define _metainfodir %{_datadir}/metainfo
%endif

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

# /ipfs/ -- directory for mountpoints ipfs and ipns
# Might end up building script for folks to do by username: /ipfs/todd/
# The systemd service allocates /ipfs/ipfsd.service/[ipfs,ipns]
install -d %{buildroot}/%{name2}
install -d %{buildroot}/%{name2}/%{name2}d
install -d %{buildroot}/%{name2}/%{name2}d.service/ipfs
install -d %{buildroot}/%{name2}/%{name2}d.service/ipns
#install -d %%{buildroot}%%{name2}/%%{ipfs}
#install -d %%{buildroot}%%{name2}/%%{ipns}

# Systemd...
# /usr/lib/systemd/system/ -- 
install -d %{buildroot}%{_unitdir}
# /etc/sysconfig/ipfsd-scripts/
install -d %{buildroot}%{_sysconfdir}/sysconfig/%{name2}d-scripts
# /usr/lib/tmpfiles.d/
install -d %{buildroot}%{_tmpfilesdir}

# For now, we just install the binary in /usr/bin
# Only members of the ipfs can do stuff with ipfs
install -D -m750 %{binarytree}/ipfs %{buildroot}%{_bindir}/

# Systemd services
install -D -m600 -p %{sourcetree_contrib}/systemd/etc-sysconfig_ipfsd %{buildroot}%{_sysconfdir}/sysconfig/%{name2}d
install -D -m755 -p %{sourcetree_contrib}/systemd/etc-sysconfig-ipfsd-scripts_ipfsd-init.sh %{buildroot}%{_sysconfdir}/sysconfig/%{name2}d-scripts/%{name2}d-init.sh
install -D -m644 -p %{sourcetree_contrib}/systemd/usr-lib-systemd-system_ipfsd.service %{buildroot}%{_unitdir}/%{name2}d.service
install -D -m644 -p %{sourcetree_contrib}/systemd/usr-lib-tmpfiles.d_ipfsd.conf %{buildroot}%{_tmpfilesdir}/%{name2}d.conf

# Service definition files for firewalld
install -D -m644 -p %{sourcetree_contrib}/firewalld/usr-lib-firewalld-services_ipfs-api.xml %{buildroot}%{_usr_lib}/firewalld/services/%{name2}-api.xml
install -D -m644 -p %{sourcetree_contrib}/firewalld/usr-lib-firewalld-services_ipfs-gateway.xml %{buildroot}%{_usr_lib}/firewalld/services/%{name2}-gateway.xml


%files
# CREATING RPM:
# - files step (final step)
# - This step makes a declaration of ownership of any listed directories
#   or files
# - The install step should have set permissions and ownership correctly,
#   but of final tweaking is often done in this section
#
%defattr(-,root,root,-)
%license %{binarytree}/LICENSE
%doc %{binarytree}/README.md

# The directories...
# /var/lib/ipfs/ -- also ipfs user's $HOME dir
%dir %attr(750,%{systemuser},%{systemgroup}) %{_sharedstatedir}/%{name2}
# repo needs to be more secure since there is a private key involved...
%dir %attr(700,%{systemuser},%{systemgroup}) %{_sharedstatedir}/%{name2}/repo

# firewalld service definition
%{_usr_lib}/firewalld/services/%{name2}-api.xml
%{_usr_lib}/firewalld/services/%{name2}-gateway.xml

# systemd service definitions, scripts, configuration
%{_unitdir}/%{name2}d.service
%{_tmpfilesdir}/%{name2}d.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/%{name2}d
%attr(755,root,root) %{_sysconfdir}/sysconfig/%{name2}d-scripts/%{name2}d-init.sh


# Mountpoints
%dir %attr(770,%{systemuser},%{systemgroup}) /%{name2}
%dir %attr(750,%{systemuser},%{systemgroup}) /%{name2}/ipfsd.service
%dir %attr(750,%{systemuser},%{systemgroup}) /%{name2}/ipfsd.service/ipfs
%dir %attr(750,%{systemuser},%{systemgroup}) /%{name2}/ipfsd.service/ipns

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


#%%clean
# # Once needed if you are building on old RHEL/CentOS.
# # No longer used.
# rm -rf %%{buildroot}


%changelog
* Tue Nov 12 2024 Todd Warner <t0dd_at_protonmail.com> 0.31.0-0.2.testing.rp.taw
  - stripped out the build instructions
  - flipped the "is this a test build" logic bit

* Tue Nov 12 2024 Todd Warner <t0dd_at_protonmail.com> 0.31.0-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/kudo/releases/tag/v0.31.0

* Fri Aug 30 2024 Todd Warner <t0dd_at_protonmail.com> 0.29.0-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/kudo/releases/tag/v0.29.0

* Fri May 10 2024 Todd Warner <t0dd_at_protonmail.com> 0.28.0-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/kudo/releases/tag/v0.28.0

* Tue Mar 5 2024 Todd Warner <t0dd_at_protonmail.com> 0.27.0-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/kudo/releases/tag/v0.27.0

* Thu Jan 27 2024 Todd Warner <t0dd_at_protonmail.com> 0.26.0-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/kudo/releases/tag/v0.26.0

* Thu May 11 2023 Todd Warner <t0dd_at_protonmail.com> 0.20.0-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/kudo/releases/tag/v0.20.0

* Wed May 10 2023 Todd Warner <t0dd_at_protonmail.com> 0.18.1-0.5.testing.rp.taw
* Wed May 10 2023 Todd Warner <t0dd_at_protonmail.com> 0.18.1-0.4.testing.rp.taw
* Wed May 10 2023 Todd Warner <t0dd_at_protonmail.com> 0.18.1-0.3.testing.rp.taw
* Wed May 10 2023 Todd Warner <t0dd_at_protonmail.com> 0.18.1-0.2.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/kudo/releases/tag/v0.18.1
  - Simplifying the systemd stuff and nuking the emaily stuff (thank you github user jbash)
  - s/ipfn/ipns because .. GAH! How did this ever work?
  - added fuse dependency

* Sat Feb 04 2023 Todd Warner <t0dd_at_protonmail.com> 0.18.1-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/kudo/releases/tag/v0.18.1

* Wed Nov 23 2022 Todd Warner <t0dd_at_protonmail.com> 0.17.0-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/kudo/releases/tag/v0.17.0

* Thu Oct 6 2022 Todd Warner <t0dd_at_protonmail.com> 0.16.0-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/kudo/releases/tag/v0.16.0

* Thu May 12 2022 Todd Warner <t0dd_at_protonmail.com> 0.12.2-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/go-ipfs/releases/tag/v0.12.2

* Tue Dec 14 2021 Todd Warner <t0dd_at_protonmail.com> 0.11.0-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/go-ipfs/releases/tag/v0.11.0

* Fri Jul 23 2021 Todd Warner <t0dd_at_protonmail.com> 0.9.1-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/go-ipfs/releases/tag/v0.9.1
  - fixed cut-n-paste errors in the specfile.
  - fixed loads of specfile errors discovered by rpmlint
  - genericized the rpm-version-specific macros

* Fri Feb 26 2021 Todd Warner <t0dd_at_protonmail.com> 0.8.0-0.1.testing.rp.taw
  - repackaged binary build - https://github.com/ipfs/go-ipfs/releases/tag/v0.8.0

* Thu Sep 24 2020 Todd Warner <t0dd_at_protonmail.com> 0.7.0-0.1.testing.rp.taw
  - 0.7.0 repackaged binary build

* Thu Aug 06 2020 Todd Warner <t0dd_at_protonmail.com> 0.6.0-0.1.testing.rp.taw
  - 0.6.0 repackaged binary build

* Thu May 14 2020 Todd Warner <t0dd_at_protonmail.com> 0.5.1-0.1.testing.rp.taw
  - 0.5.1 repackaged binary build

* Mon Feb 17 2020 Todd Warner <t0dd_at_protonmail.com> 0.4.23-0.1.testing.rp.taw
  - 0.4.23 repackaged binary build

* Wed Aug 14 2019 Todd Warner <t0dd_at_protonmail.com> 0.4.22-0.1.testing.rp.taw
  - 0.4.22 repackaged binary build

* Mon Jun 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.4.21-0.3.testing.rp.taw
  - 0.4.21 repackaged binary build

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
