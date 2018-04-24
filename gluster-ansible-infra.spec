%global rolesdir %{_sysconfdir}/ansible/roles/gluster.infra
%global docdir %{_datadir}/doc/gluster.infra

Name:      gluster-ansible-infra
Version:   0.1
Release:   1%{?dist}
Summary:   Ansible roles for GlusterFS infrastructure management

URL:       https://github.com/gluster/gluster-ansible-infra
Source0:   %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
License:   GPLv3
BuildArch: noarch

Requires:  ansible >= 2.5

%description
Collection of Ansible roles for the deploying and managing GlusterFS clusters.
The infra role enables user to configure firewall, setup backend disks, reset
backend disks.

%prep
%setup -q -n %{name}-%{version}

%build

%install
mkdir -p %{buildroot}/%{rolesdir}
cp -dpr defaults handlers meta roles tasks tests README.md LICENSE vars \
   %{buildroot}/%{rolesdir}

mkdir -p %{buildroot}/%{docdir}
cp -dpr README.md examples %{buildroot}/%{docdir}

%files
%{rolesdir}
%doc %{docdir}

%license LICENSE

%changelog
* Tue Apr 24 2018 Sachidananda Urs <sac@redhat.com> 0.1
- Initial release.

