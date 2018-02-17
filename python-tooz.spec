# Created by pyp2rpm-1.0.1
%global pypi_name tooz
%global with_doc 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global common_desc \
The Tooz project aims at centralizing the most common distributed primitives \
like group membership protocol, lock service and leader election by providing \
a coordination API helping developers to build distributed applications.

Name:           python-%{pypi_name}
Version:        1.60.0
Release:        1%{?dist}
Summary:        Coordination library for distributed systems

License:        ASL 2.0
URL:            https://tooz.readthedocs.org
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git

%description
%{common_desc}

%package -n     python2-%{pypi_name}
Summary:        Coordination library for distributed systems
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr >= 2.0.0
Requires:       python2-babel
Requires:       python2-fasteners
Requires:       python2-futurist
Requires:       python2-iso8601 >= 0.1.9
Requires:       python2-oslo-serialization >= 1.10.0
Requires:       python2-oslo-utils >= 3.15.0
Requires:       python2-pbr >= 2.0.0
Requires:       python2-six >= 1.9.0
Requires:       python2-stevedore >= 1.16.0
Requires:       python2-tenacity >= 3.2.1
Requires:       python2-voluptuous >= 0.8.9
Requires:       python2-zake
%if 0%{?fedora} > 0
Requires:       python2-enum34
Requires:       python2-futures
Requires:       python2-msgpack
Requires:       python2-redis
Requires:       python2-retrying
%else
Requires:       python-enum34
Requires:       python-futures
Requires:       python-msgpack
Requires:       python-redis
Requires:       python-retrying
%endif

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Coordination library for distributed systems
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 2.0.0
Requires:       python3-babel
Requires:       python3-fasteners
Requires:       python3-futurist
Requires:       python3-iso8601 >= 0.1.9
Requires:       python3-msgpack
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.15.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-redis
Requires:       python3-retrying
Requires:       python3-six >= 1.9.0
Requires:       python3-stevedore >= 1.16.0
Requires:       python3-tenacity >= 3.2.1
Requires:       python3-voluptuous >= 0.8.9
Requires:       python3-zake

%description -n python3-%{pypi_name}
%{common_desc}
%endif

%if %{?with_doc}
%package doc
Summary:    Documentation for %{name}
Group:      Documentation
License:    ASL 2.0

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-fasteners
BuildRequires:  python2-futurist
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-stevedore >= 1.5.0
BuildRequires:  python2-sysv_ipc
BuildRequires:  python2-tenacity
BuildRequires:  python2-voluptuous
BuildRequires:  python2-pymemcache
BuildRequires:  python2-PyMySQL
BuildRequires:  python2-zake
%if 0%{?fedora} > 0
BuildRequires:  python2-msgpack
BuildRequires:  python2-enum34
BuildRequires:  python2-futures
BuildRequires:  python2-psycopg2
BuildRequires:  python2-redis
%else
BuildRequires:  python-msgpack
BuildRequires:  python-enum34
BuildRequires:  python-futures
BuildRequires:  python-psycopg2
BuildRequires:  python-redis
%endif

%description doc
%{common_desc}

This package contains documentation in HTML format.
%endif


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%if %{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
%{__python2} setup.py install --skip-build --root %{buildroot}
rm -fr %{buildroot}%{python2_sitelib}/%{pypi_name}/tests/

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
rm -fr %{buildroot}%{python3_sitelib}/%{pypi_name}/tests/
%endif



%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%if %{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Sat Feb 17 2018 RDO <dev@lists.rdoproject.org> 1.60.0-1
- Update to 1.60.0

* Mon Feb 12 2018 Alfredo Moralejo <amoralej@redhat.com> 1.59.0-2
- Renamed python-tooz to python2-tooz

* Sat Feb 10 2018 RDO <dev@lists.rdoproject.org> 1.59.0-1
- Update to 1.59.0

