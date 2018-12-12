# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name os-ken
%global srcname os_ken
%global binname osken
%global docpath doc/build/html

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Component-based Software-defined Networking Framework

License:        Apache-2.0
Url:            http://github.com/openstack/os-ken
Source:         http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
Os-ken is a fork of Ryu. It provides software components with well
defined API that make it easy for developers to create new network
management and control applications.

%package -n python%{pyver}-%{pypi_name}
Summary: Component-based Software-defined Networking Framework
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

Requires:  python%{pyver}-eventlet
Requires:  python%{pyver}-debtcollector
Requires:  python%{pyver}-msgpack
Requires:  python%{pyver}-netaddr
Requires:  python%{pyver}-openvswitch
Requires:  python%{pyver}-oslo-config
Requires:  python%{pyver}-paramiko
Requires:  python%{pyver}-routes
Requires:  python%{pyver}-six
Requires:  python%{pyver}-tinyrpc
Requires:  python%{pyver}-webob

# Handle python2 exception
%if %{pyver} == 2
Requires:  python-lxml
%else
Requires:  python%{pyver}-lxml
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-debtcollector
BuildRequires:  python%{pyver}-eventlet
BuildRequires:  python%{pyver}-greenlet
BuildRequires:  python%{pyver}-msgpack
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-openvswitch
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-paramiko
BuildRequires:  python%{pyver}-routes
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-tinyrpc
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-webob

%if %{with check}
BuildRequires:  python%{pyver}-dns
BuildRequires:  python%{pyver}-pylint
BuildRequires:  python%{pyver}-coverage
BuildRequires:  python%{pyver}-formencode
BuildRequires:  python%{pyver}-nose
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-monotonic
BuildRequires:  python%{pyver}-pep8
BuildRequires:  python%{pyver}-tinyrpc
%endif

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-lxml
BuildRequires:  python-repoze-lru
%else
BuildRequires:  python%{pyver}-lxml
BuildRequires:  python%{pyver}-repoze-lru
%endif

%description -n python%{pyver}-%{pypi_name}
Os-ken is a fork of Ryu. It provides software components with well
defined API that make it easy for developers to create new network
management and control applications.

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%build
%{pyver_build}
sphinx-build-%{pyver} -W -b html doc/source doc/build/html


%install
export PBR_VERSION=%{version}
%{pyver_install}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{srcname}
install -d -m 755 %{buildroot}%{_bindir}/%{binname}
install -p -D -m 640 etc/%{srcname}/%{srcname}.conf  %{buildroot}%{_sysconfdir}/%{srcname}/%{srcname}.conf
install -p -D -m 640 bin/%{binname}  %{buildroot}%{_bindir}/%{binname}
install -p -D -m 640 bin/%{binname}-manager  %{buildroot}%{_bindir}/%{binname}-manager

%if %{with check}
%check
# Tests without virtualenv (N) and without PEP8 tests (P)
PYTHON=python%{pyver} ./run_tests.sh -N -P
%endif

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%doc %{docpath}
%{pyver_sitelib}/%{srcname}
%{pyver_sitelib}/%{srcname}-%{version}-*.egg-info

%{_bindir}/%{binname}
%{_bindir}/%{binname}-manager
%{_sysconfdir}/%{srcname}/%{pypi_name}.conf

%changelog
