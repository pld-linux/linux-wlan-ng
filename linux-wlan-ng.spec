#
# TO DO:
#  fix to build without pcmcia-cs sources in /usr/src
#  add to config pci & usb device support 

%define         _pre    pre4
Summary:	PCMCIA wireless microwave network card services - new generation 11Mbit
Summary(pl):	Obs³uga mikrofalowych kart sieciowych PCMCIA - nowa generacja 11Mbit
Name:		linux-wlan-ng
Version:	0.2.1
Release:	%{_pre}.0.2
License:	MPL
Group:		Applications/System
Source0:	ftp://ftp.linux-wlan.org/pub/linux-wlan-ng/%{name}-%{version}-%{_pre}.tar.gz
URL:		http://www.linux-wlan.com/
Prereq:		pcmcia-cs
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The pcmcia-cs package adds new generation microwave wirelless PCMCIA
networks cards handling support for your PLD-Linux system.

%description -l pl
Pakiet pcmcia-cs zawiera programy wspieraj±ce obs³ugê mikrofalowych
nowej generacji kart sieciowych PCMCIA w Twoim PLD-Linuksie.

%prep
%setup -q -n %{name}-%{version}-%{_pre}

%build
make auto_config
#./Configure
make all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
install -d $RPM_BUILD_ROOT%{_sysconfdir}/interfaces
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install src/wlanctl/wlanctl $RPM_BUILD_ROOT%{_sbindir}
install src/wlancfg/wlancfg $RPM_BUILD_ROOT%{_sbindir}
install src/wland/wland $RPM_BUILD_ROOT%{_sbindir}
install etc/wlan/wla* $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
install man/*.man $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/pcmcia ]; then
	/etc/rc.d/init.d/pcmcia restart 2> /dev/null
else
	echo "Run \"/rc.d/init.d/pcmcia start\" to start pcmcia cardbus daemon."
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/state/run/pcmcia ]; then
		/etc/rc.d/init.d/pcmcia restart 2> /dev/null
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING README
%doc FAQ TODO THANKS

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_sysconfdir}/pcmcia
%attr(644,root,root) %{_sysconfdir}/pcmcia/wlan.conf
#%attr(600,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wlan.opts
#%attr(600,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wlan.network.opts
%{_mandir}/man8/*
