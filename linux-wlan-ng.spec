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
Summary:	Wireless microwave network card services - new generation 11Mbit
Summary(pl):	Obs³uga mikrofalowych kart sieciowych - nowa generacja 11Mbit
Name:		linux-wlan-ng
Epoch:		1
Version:	0.2.1
%define		_pre	pre21
%define		_rel	0.%{_pre}.1
Release:	%{_rel}
License:	MPL
Group:		Applications/System
Source0:	ftp://ftp.linux-wlan.org/pub/linux-wlan-ng/%{name}-%{version}%{_pre}.tar.bz2
# Source0-md5:	91eaa768b77cccd0f18230bc8d82eeea
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-pcmcia.patch
Patch2:		%{name}-init.patch
Patch3:		%{name}-wland.patch
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
Requires(post,preun):	/sbin/chkconfig
URL:		http://www.linux-wlan.com/
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The linux-wlan-ng package adds new generation microwave wirelless
networks cards dirvers for your PLD-Linux system.

%description -l pl
Pakiet linux-wlan-ng zawiera programy wspieraj±ce obs³ugê
mikrofalowych kart sieciowych.

%package pcmcia
Summary:	PCMCIA wireless microwave network card services - new generation 11Mbit
Summary(pl):	Obs³uga mikrofalowych kart sieciowych PCMCIA - nowa generacja 11Mbit
Release:	%{_rel}
Group:		Applications/System
Prereq:		pcmcia-cs

%description pcmcia
The linux-wlan-ng-pcmcia package adds new generation microwave
wirelless PCMCIA networks cards dirvers for your PLD-Linux system.

%description pcmcia -l pl
Pakiet linux-wlan-ng-pcmcia zawiera programy wspieraj±ce obs³ugê
mikrofalowych kart sieciowych PCMCIA.

%package -n kernel-net-wlan-ng
Summary:	Drivers for wireless microwave network cards
Summary(pl):	Sterowniki mikrofalowych kart sieciowych
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/System
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-net-wlan-ng
Drivers for microwave wirelless network cards.

%description -n kernel-net-wlan-ng -l pl
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych kart
sieciowych.

%package -n kernel-smp-net-wlan-ng
Summary:	Drivers for wireless microwave network cards
Summary(pl):	Sterowniki mikrofalowych kart sieciowych
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/System
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Provides:	kernel-net-wlan-ng
Obsoletes:	kernel-net-wlan-ng

%description -n kernel-smp-net-wlan-ng
Drivers for microwave wirelless network cards.

%description -n kernel-smp-net-wlan-ng -l pl
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych kart
sieciowych.

%package -n kernel-net-wlan-ng-pcmcia
Summary:	Drivers for PCMCIA wireless microwave network cards
Summary(pl):	Sterowniki mikrofalowych kart sieciowych PCMCIA
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/System
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-net-wlan-ng-pcmcia
Drivers for microwave wirelless PCMCIA network cards.

%description -n kernel-net-wlan-ng-pcmcia -l pl
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych kart
sieciowych PCMCIA.

%package -n kernel-smp-net-wlan-ng-pcmcia
Summary:	Drivers for PCMCIA wireless microwave network cards
Summary(pl):	Sterowniki mikrofalowych kart sieciowych PCMCIA
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Applications/System
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Provides:	kernel-net-wlan-ng-pcmcia
Obsoletes:	kernel-net-wlan-ng-pcmcia

%description -n kernel-smp-net-wlan-ng-pcmcia
Drivers for microwave wirelless PCMCIA network cards.

%description -n kernel-smp-net-wlan-ng-pcmcia -l pl
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych kart
sieciowych PCMCIA.

%prep
%setup -q -n %{name}-%{version}%{_pre}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
sed -i "s#PCMCIA_SRC=.*#PCMCIA_SRC=%{_kernelsrcdir}#g; s#PRISM2_\([^=]*\)=[yn]#PRISM2_\1=y#; s#TARGET_ROOT_ON_HOST=#TARGET_ROOT_ON_HOST=$RPM_BUILD_ROOT#" config.in
make auto_config

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
    for d in p80211 prism2/driver; do
	cd $w/$d
	rm -rf include
	install -d include/{config,linux}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean modules \
	    WLAN_SRC="$PWD/" \
	    RCS_FIND_IGNORE="-name '*.ko' -o" \
	    M=$PWD O=$PWD \
	    %{?with_verbose:V=1}
	mv *.ko $w/built-$cfg
    done
done
cd $w
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{?with_userspace:%{__make} install}

%if %{with kernel}
cd src
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/wireless
install built-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless
%if %{with smp} && %{with dist_kernel}
install built-smp/*.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless
%endif
cd -
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/wlan ]; then
	/etc/rc.d/init.d/wlan restart 2> /dev/null
else
	echo "Tape \"/etc/rc.d/init.d/wlan start to start wland daemon."
fi
/sbin/chkconfig --add wlan

%preun
if [ -f /var/lock/subsys/wlan ]; then
	/etc/rc.d/init.d/wlan stop 2> /dev/null
fi
/sbin/chkconfig --del wlan

%post pcmcia
if [ -f /var/lock/subsys/pcmcia ]; then
	/etc/rc.d/init.d/pcmcia restart 2> /dev/null
else
	echo "Run \"/rc.d/init.d/pcmcia start\" to start pcmcia cardbus daemon."
fi

%postun pcmcia
if [ "$1" = "0" ]; then
	if [ -f /var/state/run/pcmcia ]; then
		/etc/rc.d/init.d/pcmcia restart 2> /dev/null
	fi
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
%attr(644,root,root) %{_sysconfdir}/wlan/*

%files pcmcia
%defattr(644,root,root,755)
%attr(644,root,root) %{_sysconfdir}/pcmcia/*
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
