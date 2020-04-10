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
# Created by pyp2rpm-1.0.1
%global pypi_name tooz
%global with_doc 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
The Tooz project aims at centralizing the most common distributed primitives \
like group membership protocol, lock service and leader election by providing \
a coordination API helping developers to build distributed applications.

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Coordination library for distributed systems

License:        ASL 2.0
URL:            https://tooz.readthedocs.org
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git

%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        Coordination library for distributed systems
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-fasteners
Requires:       python%{pyver}-futurist
Requires:       python%{pyver}-oslo-serialization >= 1.10.0
Requires:       python%{pyver}-oslo-utils >= 3.15.0
Requires:       python%{pyver}-pbr >= 1.6
Requires:       python%{pyver}-six >= 1.9.0
Requires:       python%{pyver}-stevedore >= 1.16.0
Requires:       python%{pyver}-tenacity >= 3.2.1
Requires:       python%{pyver}-voluptuous >= 0.8.9
Requires:       python%{pyver}-zake
Requires:       python%{pyver}-msgpack >= 0.4.0

# Handle python2 exception
%if %{pyver} == 2
Requires:       python%{pyver}-futures
%endif

# Handle python2 exception
%if %{pyver} == 2
Requires:       python-enum34
Requires:       python-redis
%else
Requires:       python%{pyver}-redis
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if %{?with_doc}
%package doc
Summary:    Documentation for %{name}
Group:      Documentation
License:    ASL 2.0

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-fasteners
BuildRequires:  python%{pyver}-futurist
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-stevedore >= 1.5.0
BuildRequires:  python%{pyver}-sysv_ipc
BuildRequires:  python%{pyver}-tenacity
BuildRequires:  python%{pyver}-voluptuous
BuildRequires:  python%{pyver}-pymemcache
BuildRequires:  python%{pyver}-PyMySQL
BuildRequires:  python%{pyver}-zake
BuildRequires:  python%{pyver}-msgpack >= 0.4.0

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python%{pyver}-futures
%endif

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-enum34
BuildRequires:  python-psycopg2
BuildRequires:  python-redis
%else
BuildRequires:  python%{pyver}-psycopg2
BuildRequires:  python%{pyver}-redis
%endif

%description doc
%{common_desc}

This package contains documentation in HTML format.
%endif


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the requirements
rm -f {test-,}requirements.txt

find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{pyver_bin}|'


%build
%{pyver_build}

%if %{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
%{pyver_install}
rm -fr %{buildroot}%{pyver_sitelib}/%{pypi_name}/tests/

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}-*.egg-info

%if %{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
