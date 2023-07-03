%define vendor_name Qlogic
%define vendor_label qlogic
%define driver_name fastlinq

# XCP-ng: install to the override directory
%define module_dir override

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 8.70.12.0
Release: 1%{?dist}
License: GPL

# Extracted from latest XS driver disk
Source0: qlogic-fastlinq-8.70.12.0.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{vendor_label}-%{driver_name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qed-%{version}/src  modules
%{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qede-%{version}/src modules
%{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedr-%{version}/src modules
%{make_build} -C $(pwd)/qedf-%{version} KVER=%{kernel_version} build_pre
%{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedf-%{version} modules
%{make_build} -C $(pwd)/qedi-%{version} KVER=%{kernel_version} build_pre
%{make_build} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedi-%{version} modules

%install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qed-%{version}/src  INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qede-%{version}/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedr-%{version}/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedf-%{version} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build KVER=%{kernel_version} M=$(pwd)/qedi-%{version} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install
# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x
mkdir -p %{buildroot}/lib/firmware/qed
install -m 755 $(pwd)/qed-%{version}/src/qed_init_values_zipped-*.bin %{buildroot}/lib/firmware/qed

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/firmware
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Mon Jul 03 2023 Gael Duperrey <gduperrey@vates.fr> - 8.70.12.0-1
- initial package, version 8.70.12.0
