# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: jsoncpp
Epoch: 100
Version: 1.9.4
Release: 1%{?dist}
Summary: JSON library implemented in C++
License: MIT
URL: https://github.com/open-source-parsers/jsoncpp/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: meson
BuildRequires: ninja-build
BuildRequires: pkgconfig

%description
jsoncpp is an implementation of a JSON (<http://json.org>) reader and
writer in C++. JSON (JavaScript Object Notation) is a lightweight
data-interchange format. It is easy for humans to read and write. It is
easy for machines to parse and generate.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%meson
(
    cd %{_vpath_builddir}
    meson configure -D b_lto=false
    meson configure -D b_lundef=false
    meson configure -D tests=false
    meson configure -D includedir=%{_includedir}/jsoncpp
    ninja reconfigure
)
%meson_build

%install
%meson_install

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n libjsoncpp24
Summary: Shared library for jsoncpp

%description -n libjsoncpp24
jsoncpp is an implementation of a JSON (<http://json.org>) reader and
writer in C++. JSON (JavaScript Object Notation) is a lightweight
data-interchange format. It is easy for humans to read and write. It is
easy for machines to parse and generate.

%package -n jsoncpp-devel
Summary: Development headers and library for jsoncpp
Requires: libjsoncpp24 = %{epoch}:%{version}-%{release}

%description -n jsoncpp-devel
This package contains the development headers and library for jsoncpp.

%post -n libjsoncpp24 -p /sbin/ldconfig
%postun -n libjsoncpp24 -p /sbin/ldconfig

%files -n libjsoncpp24
%license LICENSE
%{_libdir}/*.so.*

%files -n jsoncpp-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/jsoncpp.pc
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n jsoncpp-devel
Summary: Development headers and library for jsoncpp
Requires: jsoncpp = %{epoch}:%{version}-%{release}

%description -n jsoncpp-devel
This package contains the development headers and library for jsoncpp.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/*.so.*

%files -n jsoncpp-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/jsoncpp.pc
%endif

%changelog
