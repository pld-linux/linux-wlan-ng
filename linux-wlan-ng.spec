#
# TO DO:
#  fix to build without pcmcia-cs sources in /usr/src
#  add to config pci & usb device support

%define         _pre    pre12
%define		_rel	0.%{_pre}.1
Summary:	wireless microwave network card services - new generation 11Mbit
Summary(pl):	Obs³uga mikrofalowych kart sieciowych - nowa generacja 11Mbit
Name:		linux-wlan-ng
Version:	0.2.1
Release:	%{_rel}
Epoch:		1
License:	MPL
Group:		Applications/System
Source0:	ftp://ftp.linux-wlan.org/pub/linux-wlan-ng/%{name}-%{version}-%{_pre}.tar.gz
Patch0:		%{name}-pcmcia.patch
Patch1:         %{name}-install.patch
Patch2:		%{name}-init.patch
URL:		http://www.linux-wlan.com/
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The pcmcia-cs package adds new generation microwave wirelless
networks cards dirvers for your PLD-Linux system.

%description -l pl
Pakiet zawiera programy wspieraj±ce obs³ugê mikrofalowych kart sieciowych.

%package pcmcia
Summary:	PCMCIA wireless microwave network card services - new generation 11Mbit
Summary(pl):	Obs³uga mikrofalowych kart sieciowych PCMCIA - nowa generacja 11Mbit
Group:		Applications/System
Release:        %{_rel}
Prereq:		pcmcia-cs
Requires:	%{name}
%description pcmcia
The pcmcia-cs package adds new generation microwave wirelless PCMCIA
networks cards dirvers for your PLD-Linux system.

%description -l pl pcmcia
Pakiet zawiera programy wspieraj±ce obs³ugê mikrofalowych kart sieciowych 
PCMCIA.


%package -n kernel-net-wlan-ng
Summary:	dirvers for wireless microwave network cards
Summary(pl):	Sterowniki mikrofalowych kart sieciowych
Group:		Applications/System
Release:        %{_rel}@%{_kernel_ver_str}

%description -n kernel-net-wlan-ng
Drivers for microwave wirelless network cards.

%description -n kernel-net-wlan-ng -l pl
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych 
kart sieciowych.

%package -n kernel-net-wlan-ng-pcmcia
Summary:	dirvers for PCMCIA wireless microwave network cards
Summary(pl):	Sterowniki mikrofalowych kart sieciowych PCMCIA
Group:		Applications/System
Release:        %{_rel}@%{_kernel_ver_str}

%description -n kernel-net-wlan-ng-pcmcia
Drivers for microwave wirelless PCMCIA network cards.

%description -n kernel-net-wlan-ng-pcmcia -l pl
Pakiet zawiera sterowniki nowej generacji dla mikrofalowych 
kart sieciowych PCMCIA


%prep
%setup -q -n %{name}-%{version}-%{_pre} 
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
