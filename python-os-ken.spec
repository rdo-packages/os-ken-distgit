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
%global with_doc 1

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Component-based Software-defined Networking Framework

License:        Apache-2.0
Url:            http://github.com/openstack/os-ken
Source:         http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

Patch0001:      0001-Remove-requirements-unit-tests-module.patch

BuildArch:      noarch

%description
Os-ken is a fork of Ryu. It provides software components with well
defined API that make it easy for developers to create new network
management and control applications.

%package -n python%{pyver}-%{pypi_name}
Summary: Component-based Software-defined Networking Framework
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

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
BuildRequires:  python%{pyver}-tinyrpc
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-webob
BuildRequires:  python%{pyver}-dns

BuildRequires:  python%{pyver}-coverage
BuildRequires:  python%{pyver}-nose
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-monotonic

BuildRequires:  python%{pyver}-tinyrpc

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-lxml
BuildRequires:  python-repoze-lru
BuildRequires:  python-pep8
%else
BuildRequires:  python%{pyver}-lxml
BuildRequires:  python%{pyver}-repoze-lru
BuildRequires:  python%{pyver}-pep8
%endif

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

%description -n python%{pyver}-%{pypi_name}
Os-ken is a fork of Ryu. It provides software components with well
defined API that make it easy for developers to create new network
management and control applications.

%if 0%{?with_doc}
%package doc
Summary: Os-ken documentation

BuildRequires:  python%{pyver}-sphinx

%description doc
Documentation for os-ken
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%build
%{pyver_build}
%if 0%{?with_doc}
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
export PBR_VERSION=%{version}
%{pyver_install}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{srcname}
install -p -m 640 etc/%{srcname}/%{srcname}.conf  %{buildroot}%{_sysconfdir}/%{srcname}/%{srcname}.conf

%check
# Tests without virtualenv (N) and without PEP8 tests (P)
PYTHON=python%{pyver} ./run_tests.sh -N -P

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%{pyver_sitelib}/%{srcname}
%{pyver_sitelib}/%{srcname}-%{version}-*.egg-info
%{_bindir}/%{binname}
%{_bindir}/%{binname}-manager
%{_sysconfdir}/%{srcname}/%{srcname}.conf

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc README.rst
%doc %{docpath}
%endif

%changelog
