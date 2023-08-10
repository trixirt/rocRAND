%global commit0 39d1b4d3a7d0bbe26c50f6732abce727e0377a91
%global _lto_cflags %{nil}
%global build_cxxflags %{nil}
%global build_ldflags %{nil}
%global gpus gfx1102
%global _name amd-rocm-rocrand
%global rocm_path /opt/rocm
%global hipcc %{rocm_path}/bin/hipcc
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global toolchain clang
%global up_name rocRAND

%define patch_level 2

%bcond_with debug
%bcond_with extra
%bcond_with gpu
%bcond_with static

%if %{without debug}
  %if %{without static}
    %global suf %{nil}
  %else
    %global suf -static
  %endif
%else
  %if %{without static}
    %global suf -debug
  %else
    %global suf -static-debug
  %endif
%endif

Name: %{_name}%{suf}

Version:        5.6
Release:        %{patch_level}.git%{?shortcommit0}%{?dist}
Summary:        TBD
License:        TBD

URL:            https://github.com/trixirt/%{up_name}
Source0:        %{url}/archive/%{commit0}/%{up_name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake

%if %{with extra}
BuildRequires:  google-benchmark-devel
BuildRequires:  gtest-devel
%endif

# %if %{without debug}
# librocrand-d.so.1.1: Unknown DWARF DW_FORM_0x25
%global debug_package %{nil}
# %endif

%description
TBD

%package devel
Summary:        TBD

%description devel
%{summary}

%prep
%autosetup -p1 -n %{up_name}-%{commit0}

%build
%cmake -G Ninja \
%if %{with gpu}
       -DAMDGPU_TARGETS=%{gpus} \
%endif
%if %{with extra}
       -DBUILD_CLIENTS=ON \
       -DBUILD_CLIENTS_TESTS_OPENMP=OFF \
%endif
%if %{with static}
       -DBUILD_SHARED_LIBS=OFF \
%endif
%if %{without debug}
       -DCMAKE_BUILD_TYPE=RELEASE \
%else
       -DCMAKE_BUILD_TYPE=DEBUG \
%endif
       -DCMAKE_C_COMPILER=%{hipcc} \
       -DCMAKE_CXX_COMPILER=%{hipcc} \
       -DCMAKE_EXE_LINKER_FLAGS=-L%{rocm_path}/lib64 \
       -DCMAKE_INSTALL_PREFIX=%{rocm_path} \
       -DCMAKE_SHARED_LINKER_FLAGS=-L%{rocm_path}/lib64 \
       -DBUILD_HIPRAND=OFF

#  /opt/rocm/bin/rocminfo: error while loading shared libraries: libhsa-runtime64.so.1:
export LD_LIBRARY_PATH=%{rocm_path}/lib64

%cmake_build

%install
%cmake_install

%files devel
%{rocm_path}

%changelog
* Mon Aug 07 2023 Tom Rix <trix@redhat.com>
- Stub something together
