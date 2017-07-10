# Created by pyp2rpm-1.0.1
%global pypi_name tooz
%global with_doc 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Coordination library for distributed systems

License:        ASL 2.0
URL:            https://tooz.readthedocs.org
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr >= 1.8
BuildRequires:  git
Requires:       python-babel
Requires:       python-enum34
Requires:       python-fasteners
Requires:       python-futures
Requires:       python-futurist
Requires:       python-iso8601 >= 0.1.9
Requires:       python-msgpack
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-utils >= 3.15.0
Requires:       python-pbr >= 1.6
Requires:       python-redis
Requires:       python-retrying
Requires:       python-six >= 1.9.0
Requires:       python-stevedore >= 1.16.0
Requires:       python-tenacity >= 3.2.1
Requires:       python-voluptuous >= 0.8.9
Requires:       python-zake

%description
The Tooz project aims at centralizing the most common distributed primitives
like group membership protocol, lock service and leader election by providing
a coordination API helping developers to build distributed applications.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Coordination library for distributed systems
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 1.8
Requires:       python3-babel
Requires:       python3-fasteners
Requires:       python3-futures
Requires:       python3-futurist
Requires:       python3-iso8601 >= 0.1.9
Requires:       python3-msgpack
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.15.0
Requires:       python3-pbr >= 1.6
Requires:       python3-redis
Requires:       python3-retrying
Requires:       python3-six >= 1.9.0
Requires:       python3-stevedore >= 1.16.0
Requires:       python3-tenacity >= 3.2.1
Requires:       python3-voluptuous >= 0.8.9
Requires:       python3-zake

%description -n python3-%{pypi_name}
The Tooz project aims at centralizing the most common distributed primitives
like group membership protocol, lock service and leader election by providing
a coordination API helping developers to build distributed applications.
%endif

%if %{?with_doc}
%package doc
Summary:    Documentation for %{name}
Group:      Documentation
License:    ASL 2.0

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-msgpack
BuildRequires:  python-enum
BuildRequires:  python-futures
BuildRequires:  python-futurist
BuildRequires:  python-msgpack
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-utils
BuildRequires:  python-stevedore >= 1.5.0
BuildRequires:  python-tenacity

%description doc
The Tooz project aims at centralizing the most common distributed primitives
like group membership protocol, lock service and leader election by providing
a coordination API helping developers to build distributed applications.

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



%files
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
