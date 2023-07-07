%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order pylint
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global pypi_name os-ken
%global srcname os_ken
%global binname osken
%global with_doc 1

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Component-based Software-defined Networking Framework

License:        Apache-2.0
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

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{pypi_name}
Os-ken is a fork of Ryu. It provides software components with well
defined API that make it easy for developers to create new network
management and control applications.

%if 0%{?with_doc}
%package doc
Summary: Os-ken documentation
%description doc
Documentation for os-ken
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel
%if 0%{?with_doc}
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

install -d -m 755 %{buildroot}%{_sysconfdir}/%{srcname}
install -p -m 644 etc/%{srcname}/%{srcname}.conf  %{buildroot}%{_sysconfdir}/%{srcname}/%{srcname}.conf

%check
%tox -e %{default_toxenv}

%files -n python3-%{pypi_name}
%license LICENSE
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-*.dist-info
%{_bindir}/%{binname}
%{_bindir}/%{binname}-manager
%dir %{_sysconfdir}/%{srcname}
%config(noreplace) %attr(0644, root, neutron) %{_sysconfdir}/%{srcname}/%{srcname}.conf

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc README.rst
%doc doc/build/html
%endif

%changelog
