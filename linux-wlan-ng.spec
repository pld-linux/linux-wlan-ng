#
# TO DO:
#  fix to build without pcmcia-cs sources in /usr/src
#  add to config pci & usb device support

%define		_pre	pre13
%define		_rel	0.%{_pre}.0.1
Summary:	Wireless microwave network card services - new generation 11Mbit
Summary(pl):	Obs³uga mikrofalowych kart sieciowych - nowa generacja 11Mbit
Name:		linux-wlan-ng
Version:	0.2.1
Release:	%{_rel}
Epoch:		1
License:	MPL
Group:		Applications/System
Source0:	ftp://ftp.linux-wlan.org/pub/linux-wlan-ng/%{name}-%{version}-%{_pre}.tar.gz
# Source0-md5:	7d166956c94bdcbc9f8881b2bad4391c
Patch0:		%{name}-pcmcia.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-init.patch
Patch3:		%{name}-wland.patch
Patch4:		%{name}-gcc2.patch
BuildRequires:	kernel-headers
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
Group:		Applications/System
Release:	%{_rel}
Prereq:		pcmcia-cs
Requires:	%{name}

%description pcmcia
The linux-wlan-ng-pcmcia package adds new generation microwave
wirelless PCMCIA networks cards dirvers for your PLD-Linux system.

%description -l pl pcmcia
Pakiet linux-wlan-ng-pcmcia zawiera programy wspieraj±ce obs³ugê
mikrofalowych kart sieciowych PCMCIA.


%package -n kernel-net-wlan-ng
Summary:	Drivers for wireless microwave network cards
Summary(pl):	Sterowniki mikrofalowych kart sieciowych
Group:		Applications/System
Release:	%{_rel}@%{_kernel_ver_str}

%description -n kernel-net-wlan-ng
Drivers for microwave wirelless network cards.

%description -n kernel-net-wlan-ng -l pl
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych kart
sieciowych.

%package -n kernel-net-wlan-ng-pcmcia
Summary:	Drivers for PCMCIA wireless microwave network cards
Summary(pl):	Sterowniki mikrofalowych kart sieciowych PCMCIA
Group:		Applications/System
Release:	%{_rel}@%{_kernel_ver_str}

%description -n kernel-net-wlan-ng-pcmcia
Drivers for microwave wirelless PCMCIA network cards.

%description -n kernel-net-wlan-ng-pcmcia -l pl
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych kart
sieciowych PCMCIA.

%prep
%setup -q -n %{name}-%{version}-%{_pre}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
#%%patch4

%build
ln -s pcmcia-cs-* pcmcia-cs
cp -f config.in config.in.org
sed -e "s#PCMCIA_SRC=.*#PCMCIA_SRC=/usr/src/linux#g; s#PRISM2_\([^=]*\)=[yn]#PRISM2_\1=y#; s#TARGET_ROOT_ON_HOST=#TARGET_ROOT_ON_HOST=$RPM_BUILD_ROOT#" config.in.org > config.in
make auto_config
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
make install
mv $RPM_BUILD_ROOT/lib/modules/%{__kernel_ver} $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d/
install etc/rc.wlan $RPM_BUILD_ROOT/etc/rc.d/init.d/wlan

%clean
#rm -rf $RPM_BUILD_ROOT

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

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING README FAQ TODO THANKS
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%{_mandir}/man1/*
%attr(644,root,root) %{_sysconfdir}/wlan/*

%files pcmcia
%defattr(644,root,root,755)
%attr(644,root,root) %{_sysconfdir}/pcmcia/*

%files -n kernel-net-wlan-ng
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/*
/lib/modules/%{_kernel_ver}/kernel/drivers/usb/*

%files -n kernel-net-wlan-ng-pcmcia
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/pcmcia/*
