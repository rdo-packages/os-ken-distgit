%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name os-ken
%global srcname os_ken
%global binname osken
%global docpath doc/build/html
%global with_doc 1

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Component-based Software-defined Networking Framework

License:        ASL 2.0
Url:            http://github.com/openstack/os-ken
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  git-core

%description
Os-ken is a fork of Ryu. It provides software components with well
defined API that make it easy for developers to create new network
management and control applications.

%package -n python3-%{pypi_name}
Summary: Component-based Software-defined Networking Framework
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-eventlet
BuildRequires:  python3-greenlet
BuildRequires:  python3-msgpack
BuildRequires:  python3-openvswitch
BuildRequires:  python3-oslo-config
BuildRequires:  python3-paramiko
BuildRequires:  python3-routes
BuildRequires:  python3-setuptools
BuildRequires:  python3-webob
BuildRequires:  python3-dns
BuildRequires:  python3-mock
BuildRequires:  python3-monotonic
BuildRequires:  python3-lxml
BuildRequires:  python3-repoze-lru
BuildRequires:  python3-stestr
BuildRequires:  python3-testscenarios
BuildRequires:  python3-ncclient

Requires:  python3-eventlet
Requires:  python3-pbr >= 2.0.0
Requires:  python3-msgpack
Requires:  python3-netaddr
Requires:  python3-openvswitch
Requires:  python3-oslo-config
Requires:  python3-paramiko
Requires:  python3-routes
Requires:  python3-webob
Requires:  python3-lxml
Requires:  python3-ncclient >= 0.6.13

%description -n python3-%{pypi_name}
Os-ken is a fork of Ryu. It provides software components with well
defined API that make it easy for developers to create new network
management and control applications.

%if 0%{?with_doc}
%package doc
Summary: Os-ken documentation
BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

%description doc
Documentation for os-ken
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# (TODO) remove this line once https://review.openstack.org/#/c/625704/ is tagged and
# in u-c and source-branch in stein-uc and stein-py3-uc.
rm -f os_ken/tests/unit/test_requirements.py

%build
%{py3_build}
%if 0%{?with_doc}
sphinx-build-3 -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
export PBR_VERSION=%{version}
%{py3_install}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{srcname}
install -p -m 644 etc/%{srcname}/%{srcname}.conf  %{buildroot}%{_sysconfdir}/%{srcname}/%{srcname}.conf

%check
stestr run

%files -n python3-%{pypi_name}
%license LICENSE
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-*.egg-info
%{_bindir}/%{binname}
%{_bindir}/%{binname}-manager
%dir %{_sysconfdir}/%{srcname}
%config(noreplace) %attr(0644, root, neutron) %{_sysconfdir}/%{srcname}/%{srcname}.conf

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc README.rst
%doc %{docpath}
%endif

%changelog
