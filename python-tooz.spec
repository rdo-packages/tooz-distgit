# Created by pyp2rpm-1.0.1
%global pypi_name tooz

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        1.24.0
Release:        2%{?dist}
Summary:        Coordination library for distributed systems

License:        ASL 2.0
URL:            https://tooz.readthedocs.org
Source0:        https://pypi.python.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
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
%setup -q -n %{pypi_name}-%{version}

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
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files doc
%license LICENSE
%doc html

%changelog
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 07 2015 Alan Pevec <alan.pevec@redhat.com> 1.24.0-1
- Update to upstream 1.24.0

* Wed Sep 09 2015 Alan Pevec <alan.pevec@redhat.com> 1.23.0-1
- Update to upstream 1.23.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Alan Pevec <alan.pevec@redhat.com> 0.13.2-1
- Update to upstream 0.13.2

* Fri Nov 21 2014 Eoghan Glynn <eglynn@redhat.com> - 0.9-1
- Rebased on 0.9 upstream.
- Removed python-posix_ipc dependency.

* Thu Oct 23 2014 Eoghan Glynn <eglynn@redhat.com> - 0.8-1
- Rebased on 0.8 upstream.

* Tue Sep 09 2014 Nejc Saje <nsaje@redhat.com> - 0.3-1
- Initial package.

