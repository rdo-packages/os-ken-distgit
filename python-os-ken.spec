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
%{pyver_bin} setup.py build_sphinx


%install
%{pyver_install}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{pypi_name}
mv %{buildroot}%{_prefix}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf %{buildroot}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf

%if %{with check}
%check
# Tests without virtualenv (N) and without PEP8 tests (P)
PYTHON=python%{pyver} ./run_tests.sh -N -P
%endif

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%doc %{docpath}
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}-*.egg-info

%{_bindir}/%{pypi_name}
%{_bindir}/%{pypi_name}-manager
%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf


%changelog
