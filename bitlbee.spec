# TODO
# - sync pl
#
# Conditional build:
%bcond_with		otr		# build without OTR
%bcond_with		purple	# build with libpurple (not recommended for public servers). http://wiki.bitlbee.org/HowtoPurple

Summary:	An IRC to other chat networks gateway
Summary(pl.UTF-8):	Bramka pomiędzy IRC-em i innymi sieciami komunikacyjnymi
Name:		bitlbee
Version:	3.2
Release:	3
License:	GPL v2+ and MIT
Group:		Daemons
Source0:	http://get.bitlbee.org/src/%{name}-%{version}.tar.gz
# Source0-md5:	6a8fe98e96a47c636004a245075d5d7c
URL:		http://www.bitlbee.org/
Patch0:		config.patch
Patch1:		systemd.patch
Patch3:		skype-no-groups.patch
Patch4:		skyped-transport.patch
BuildRequires:	asciidoc
BuildRequires:	glib2-devel >= 1:2.14
BuildRequires:	gnutls-devel
%{?with_otr:BuildRequires:	libotr-devel >= 3.2.0}
%{?with_purple:BuildRequires:	libpurple-devel}
BuildRequires:	rpmbuild(macros) >= 1.461
BuildRequires:	systemd-units
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 38
Provides:	group(bitlbee)
Provides:	user(bitlbee)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bitlbee is an IRC to other chat networks gateway. Bitlbee can be used
as an IRC server which forwards everything you say to people on other
chat networks like ICQ/AIM, MSN, XMPP/Jabber (including Google Talk),
Yahoo or Twitter!

%description -l pl.UTF-8
Bramka pomiędzy IRC-em i innymi sieciami komunikacyjnymi. Ten program
może być używany jako serwer IRC przekazujący wszystko co się mówi do
ludzi korzystających z innych sieci komunikacyjnych, takich jak
MSN/ICQ/Jabber.

%package devel
Summary:	Development files for bitlbee
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The bitlbee-devel package includes header files necessary for building
and developing programs and plugins which use bitlbee.

%package otr
Summary:	OTR plugin for bitlbee
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description otr
The bitlbee-otr package includes OTR plugin for bitlbee. Not
completely stable and not 100% foolproof so use at your own risk.

%package protocol-skype
Summary:	Skype protocol support for bitlbee
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
Suggests:	skyped

%description protocol-skype
Skype protocol support for bitlbee.

%package -n skyped
Summary:	Remote control of the Skype GUI client
Group:		Daemons
Requires:	python-skype

%description -n skyped
Skype supports remote control of the GUI client only via X11 or DBus
messages. This is hard in care you want remote control. This daemon
listens on a TCP port and runs on the same machine where the GUI
client runs. It passes all the input it gets to Skype directly, except
for a few commands which is related to authentication. The whole
communication is done via SSL.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1

# fix wrong assumption with $DESTDIR
%{__sed} -i -e 's,$(shell id -u),0,' Makefile

# fix #!%{_bindir}/env python -> #!%{__python}:
%{__sed} -i -e '1s,^#!.*python.*,#!%{__python},' protocols/skype/*.py

# fix config path
%{__sed} -i -e 's,/usr/local/etc/skyped,%{_sysconfdir}/skyped,' protocols/skype/*.py

%build
CFLAGS="%{rpmcflags}" \
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_sbindir} \
	--etcdir=%{_sysconfdir}/%{name} \
	--mandir=%{_mandir} \
	--datadir=%{_datadir}/%{name} \
	--config=%{_localstatedir}/lib/%{name} \
	--pcdir=%{_pkgconfigdir} \
	--plugindir=%{_libdir}/%{name} \
	--strip=0 \
	--plugins=1 \
	--ssl=gnutls \
	--pie=1 \
%if %{with purple}
	--purple=1 \
%endif
%if %{with otr}
	--otr=plugin \
%endif
	--skype=plugin \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}
%{__make} install install-dev install-etc install-systemd \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 280 bitlbee
%useradd -u 280 -d /var/lib/bitlbee -g bitlbee -c "Bitlbee User" bitlbee
%systemd_post bitlbee.service

%preun
%systemd_preun bitlbee.service

%postun
if [ "$1" = "0" ]; then
	%userremove bitlbee
	%groupremove bitlbee
fi
%systemd_reload

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,CHANGES,CREDITS,FAQ,README} utils
%dir %attr(750,root,bitlbee) %{_sysconfdir}/%{name}
%attr(640,root,bitlbee) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/bitlbee.conf
%attr(640,root,bitlbee) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/motd.txt
%attr(755,root,root) %{_sbindir}/bitlbee
%{_mandir}/man5/bitlbee.conf.5*
%{_mandir}/man8/bitlbee.8*
%{_datadir}/bitlbee
%dir %{_libdir}/%{name}
%attr(770,root,bitlbee) %{_localstatedir}/lib/bitlbee
%{systemdunitdir}/bitlbee.service
%{systemdunitdir}/bitlbee.socket
%{systemdunitdir}/bitlbee@.service

%files devel
%defattr(644,root,root,755)
%doc doc/example_plugin.c
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc

%if %{with otr}
%files otr
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/otr.so
%endif

%files protocol-skype
%defattr(644,root,root,755)
%doc protocols/skype/{HACKING,NEWS,README}
%attr(755,root,root) %{_libdir}/%{name}/skype.so

%files -n skyped
%defattr(644,root,root,755)
%doc protocols/skype/{skyped.txt,client.sh}
%dir %{_sysconfdir}/skyped
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/skyped/skyped.cnf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/skyped/skyped.conf
%attr(755,root,root) %{_sbindir}/skyped
%{_mandir}/man1/skyped.1*
