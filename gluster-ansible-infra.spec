%global rolesdir %{_sysconfdir}/ansible/roles/gluster.infra
%global buildnum 20

Name:      gluster-ansible-infra
Version:   1.0.4
Release:   %{buildnum}%{?dist}
Summary:   Ansible roles for GlusterFS infrastructure management

URL:       https://github.com/gluster/gluster-ansible-infra
Source0:   %{url}/archive/v%{version}-%{buildnum}.tar.gz#/%{name}-%{version}-%{buildnum}.tar.gz
License:   GPLv3
BuildArch: noarch

Requires:  ansible-core >= 2.12

%description
Collection of Ansible roles for the deploying and managing GlusterFS clusters.
The infra role enables user to configure firewall, setup backend disks, reset
backend disks.

%prep
%autosetup -p1 -n %{name}-%{version}-%{buildnum}

%build

%install
mkdir -p %{buildroot}/%{rolesdir}
cp -dpr defaults handlers meta roles tasks tests README.md LICENSE vars playbooks README.md\
   %{buildroot}/%{rolesdir}

%files
%{rolesdir}

%license LICENSE

%changelog
* Fri Apr 01 2022 Sandro Bonazzola <sbonazzo@redhat.com> - 1.0.4-20
- Rebase on v1.0.4-20

* Wed Feb 20 2019 Sachidananda Urs <sac@redhat.com> 1.0.0-1
- Bump the version numer to 1

* Thu Jan 03 2019 Sachidananda Urs <sac@redhat.com> 0.6
- Add example and molecule tests

* Mon Oct 15 2018 Sachidananda Urs <sac@redhat.com> 0.5
- Add Gluster specific SeLinux label on brick mounts

* Fri Oct 12 2018 Sachidananda Urs <sac@redhat.com> 0.4
- Added tests, and enhanced documentation, fixed fscreate bug
- Remove xfs runtime specific configuration

* Tue Sep 25 2018 Sachidananda Urs <sac@redhat.com> 0.3
- Remove the examples directory and add backend_reset role

* Fri Aug 31 2018 Sachidananda Urs <sac@redhat.com> 0.2
- Backend setup enhancements

* Tue Apr 24 2018 Sachidananda Urs <sac@redhat.com> 0.1
- Initial release.
