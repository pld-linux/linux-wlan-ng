Summary:	PCMCIA wireless microwave network card services - new generation 11Mbit
Summary(pl):	Obs�uga mikrofalowych kart sieciowych PCMCIA - nowa generacja 11Mbit
Name:		linux-wlan-ng
Version:	0.1.12
Release:	0.1
License:	MPL (Mozilla Public License)
Group:		Applications/System
Source0:	ftp://ftp.linux-wlan.com/pub/linux-wlan-ng/%{name}-%{version}.tar.gz
#Patch0:		%{name}.pld.patch
URL:		http://www.linux-wlan.com/
Prereq:		pcmcia-cs
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The pcmcia-cs package adds new generation microwave wirelless PCMCIA
networks cards handling support for your PLD-Linux system.

%description -l pl
Pakiet pcmcia-cs zawiera programy wspieraj�ce obs�ug� mikrofalowych
nowej generacji kart sieciowych PCMCIA w Twoim PLD-Linuksie.

%prep
%setup -q
#%patch0 -p0

%build
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/sbin
install -d $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install wlanctl/wlanctl $RPM_BUILD_ROOT/sbin
install wlandump/wlandump $RPM_BUILD_ROOT/sbin
install scripts/wla* $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia
install man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/wlan.config /$RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/wlan.conf

gzip -9nf SUPPORTED.CARDS CHANGES COPYING README \
	FAQ.isa README.debug README.isa README.linuxppc \
	README.wep TODO THANKS

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
%doc *.gz
%attr(755,root,root) /sbin/*

%attr(755,root,root) %{_sysconfdir}/pcmcia/wlan
%attr(644,root,root) %{_sysconfdir}/pcmcia/wlan.conf
%attr(600,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wlan.opts
%attr(600,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wlan.network.opts
%{_mandir}/man8/*
