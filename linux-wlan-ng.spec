#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace module
%bcond_with	verbose		# verbose build (V=1)
#
# TODO:
#	- check %%desc, R:, BR:, cflags
#
%define		_rel	0.1
Summary:	Wireless microwave network card services - new generation 11Mbit
Summary(pl.UTF-8):   Obsługa mikrofalowych kart sieciowych - nowa generacja 11Mbit
Name:		linux-wlan-ng
Version:	0.2.7
Release:	%{_rel}
Epoch:		1
License:	MPL
Group:		Applications/System
Source0:	ftp://ftp.linux-wlan.org/pub/linux-wlan-ng/%{name}-%{version}.tar.bz2
# Source0-md5:	b2b0ffd11d27c72a9c01b8a9ef3832b7
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-configure.patch
Patch2:		%{name}-init.patch
URL:		http://www.linux-wlan.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.268
%endif
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The linux-wlan-ng package adds new generation microwave wirelless
networks cards dirvers for your PLD-Linux system.

%description -l pl.UTF-8
Pakiet linux-wlan-ng zawiera programy wspierające obsługę
mikrofalowych kart sieciowych.

%package pcmcia
Summary:	PCMCIA wireless microwave network card services - new generation 11Mbit
Summary(pl.UTF-8):   Obsługa mikrofalowych kart sieciowych PCMCIA - nowa generacja 11Mbit
Release:	%{_rel}
Group:		Applications/System
Requires:	pcmcia-cs

%description pcmcia
The linux-wlan-ng-pcmcia package adds new generation microwave
wirelless PCMCIA networks cards dirvers for your PLD-Linux system.

%description pcmcia -l pl.UTF-8
Pakiet linux-wlan-ng-pcmcia zawiera programy wspierające obsługę
mikrofalowych kart sieciowych PCMCIA.

%package -n kernel-net-wlan-ng
Summary:	Drivers for wireless microwave network cards
Summary(pl.UTF-8):   Sterowniki mikrofalowych kart sieciowych
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/System
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel-net-wlan-ng
Drivers for microwave wirelless network cards.

%description -n kernel-net-wlan-ng -l pl.UTF-8
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych kart
sieciowych.

%package -n kernel-smp-net-wlan-ng
Summary:	Drivers for wireless microwave network cards
Summary(pl.UTF-8):   Sterowniki mikrofalowych kart sieciowych
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/System
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-net-wlan-ng
Drivers for microwave wirelless network cards.

%description -n kernel-smp-net-wlan-ng -l pl.UTF-8
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych kart
sieciowych.

%package -n kernel-net-wlan-ng-pcmcia
Summary:	Drivers for PCMCIA wireless microwave network cards
Summary(pl.UTF-8):   Sterowniki mikrofalowych kart sieciowych PCMCIA
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/System
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel-net-wlan-ng-pcmcia
Drivers for microwave wirelless PCMCIA network cards.

%description -n kernel-net-wlan-ng-pcmcia -l pl.UTF-8
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych kart
sieciowych PCMCIA.

%package -n kernel-smp-net-wlan-ng-pcmcia
Summary:	Drivers for PCMCIA wireless microwave network cards
Summary(pl.UTF-8):   Sterowniki mikrofalowych kart sieciowych PCMCIA
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/System
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-net-wlan-ng-pcmcia
Drivers for microwave wirelless PCMCIA network cards.

%description -n kernel-smp-net-wlan-ng-pcmcia -l pl.UTF-8
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych kart
sieciowych PCMCIA.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
sed -i "s#PCMCIA_SRC=.*#PCMCIA_SRC=%{_kernelsrcdir}#g; s#PRISM2_\([^=]*\)=[yn]#PRISM2_\1=y#; s#TARGET_ROOT_ON_HOST=#TARGET_ROOT_ON_HOST=$RPM_BUILD_ROOT#" config.in
%{__make} auto_config \
	LINUX_SRC=%{_kernelsrcdir}
cd src
ln -sf ../config.mk config.mk
cd prism2
ln -sf ../../config.mk config.mk
cd ../..
%{?with_userspace:%{__make} all}

%if %{with kernel}
cd src
%{__make} -C mkmeta all
rm -rf built*
mkdir -p built-{smp,up,nondist}
w=$PWD
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi

	cd p80211
	ln -sf ../include/wlan wlan
	cd ../prism2
	ln -sf ../include/wlan wlan
	cd driver
	ln -sf ../../include/wlan wlan
	ln -sf ../include/prism2 prism2
	cd ../..

	for d in p80211 prism2/driver; do
		cd $w/$d
		rm -rf o
		install -d o/include/linux
		ln -sf %{_kernelsrcdir}/config-$cfg o/.config
		ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
		ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
		%{__make} -C %{_kernelsrcdir} clean \
			WLAN_SRC="$PWD/" \
			RCS_FIND_IGNORE="-name '*.ko' -o" \
			SYSSRC=%{_kernelsrcdir} \
			SYSOUT=$PWD/o \
			M=$PWD O=$PWD/o \
			%{?with_verbose:V=1}
		%{__make} -C %{_kernelsrcdir} modules \
			CC="%{__cc}" CPP="%{__cpp}" \
			WLAN_SRC="$PWD/" \
			SYSSRC=%{_kernelsrcdir} \
			SYSOUT=$PWD/o \
			M=$PWD O=$PWD/o \
			%{?with_verbose:V=1}

		mv *.ko $w/built-$cfg
		cd ../..
	done
done
cd $w
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install
install -D etc/rc.wlan $RPM_BUILD_ROOT/etc/rc.d/init.d/wlan
%endif

%if %{with kernel}
cd src
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/wireless
install built-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless
%if %{with smp} && %{with dist_kernel}
install built-smp/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add wlan
%service wlan restart

%preun
if [ "$1" = "0" ]; then
	%service wlan stop
	/sbin/chkconfig --del wlan
fi

%post pcmcia
%service pcmcia restart

%postun pcmcia
if [ "$1" = "0" ]; then
	%service pcmcia restart
fi

%post -n kernel-net-wlan-ng
%depmod %{_kernel_ver}

%postun -n kernel-net-wlan-ng
%depmod %{_kernel_ver}

%post -n kernel-smp-net-wlan-ng
%depmod %{_kernel_ver}

%postun -n kernel-smp-net-wlan-ng
%depmod %{_kernel_ver}

%post -n kernel-net-wlan-ng-pcmcia
%depmod %{_kernel_ver}

%postun -n kernel-net-wlan-ng-pcmcia
%depmod %{_kernel_ver}

%post -n kernel-smp-net-wlan-ng-pcmcia
%depmod %{_kernel_ver}

%postun -n kernel-smp-net-wlan-ng-pcmcia
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc CHANGES README FAQ
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%{_mandir}/man1/*
%{_sysconfdir}/wlan/*

%files pcmcia
%defattr(644,root,root,755)
%{_sysconfdir}/pcmcia/*
%endif

%if %{with kernel}
%files -n kernel-net-wlan-ng
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/p80211.ko*
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/prism2_pci.ko*
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/prism2_usb.ko*

%files -n kernel-net-wlan-ng-pcmcia
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/prism2_cs.ko*
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/prism2_plx.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-wlan-ng
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/p80211.ko*
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/prism2_pci.ko*
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/prism2_usb.ko*

%files -n kernel-smp-net-wlan-ng-pcmcia
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/prism2_cs.ko*
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/prism2_plx.ko*
%endif
%endif
