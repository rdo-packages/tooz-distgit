# Created by pyp2rpm-1.0.1
%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name tooz
%global with_doc 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order pifpaf
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
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
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        Coordination library for distributed systems

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

Requires:  python3-%{pypi_name}+zake = %{version}-%{release}
Requires:  python3-%{pypi_name}+redis = %{version}-%{release}

%description -n python3-%{pypi_name}
%{common_desc}

%if %{?with_doc}
%package doc
Summary:    Documentation for %{name}
Group:      Documentation
License:    ASL 2.0


%description doc
%{common_desc}

This package contains documentation in HTML format.
%endif


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/:[[:space:]]\.\[.*\]/d' tox.ini
sed -i 's/deps = .\[zake.*/deps =/' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
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

%if %{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
%pyproject_install
rm -fr %{buildroot}%{python3_sitelib}/%{pypi_name}/tests/

%pyproject_extras_subpkg -n python3-%{pypi_name} zake redis etcd3gw

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.dist-info

%if %{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
