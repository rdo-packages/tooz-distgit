# Created by pyp2rpm-1.0.1
%global pypi_name tooz

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Coordination library for distributed systems

License:        ASL 2.0
URL:            https://tooz.readthedocs.org
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-master.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
Requires:       python-babel
Requires:       python-stevedore >= 1.5.0
Requires:       python-six >= 1.9.0
Requires:       python-iso8601 >= 0.1.9
Requires:       python-oslo-utils >= 2.0.0
Requires:       python-msgpack
Requires:       python-retrying
Requires:       python-futures
Requires:       python-fasteners
Requires:       python-futurist
Requires:       python-oslo-serialization


%description
The Tooz project aims at centralizing the most common distributed primitives
like group membership protocol, lock service and leader election by providing
a coordination API helping developers to build distributed applications.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Coordination library for distributed systems
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
Requires:       python3-babel
Requires:       python3-stevedore
Requires:       python3-six
Requires:       python3-iso8601
Requires:       python3-oslo-utils
Requires:       python3-msgpack
Requires:       python3-retrying
Requires:       python3-fasteners
Requires:       python3-futurist
Requires:       python3-oslo-serialization

%description -n python3-%{pypi_name}
The Tooz project aims at centralizing the most common distributed primitives
like group membership protocol, lock service and leader election by providing
a coordination API helping developers to build distributed applications.
%endif

%package doc
Summary:    Documentation for %{name}
Group:      Documentation
License:    ASL 2.0

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-stevedore >= 1.5.0

%description doc
The Tooz project aims at centralizing the most common distributed primitives
like group membership protocol, lock service and leader election by providing
a coordination API helping developers to build distributed applications.

This package contains documentation in HTML format.


%prep
%setup -q -n %{pypi_name}-%{upstream_version}

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

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


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

%files doc
%license LICENSE
%doc html

%changelog
