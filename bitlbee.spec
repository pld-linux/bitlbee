# TODO
# - sync pl
# - bilbee user
#
# Conditional build:
%bcond_without	otr		# build without OTR

Summary:	An IRC to other chat networks gateway
Summary(pl.UTF-8):	Bramka pomiędzy IRC-em i innymi sieciami komunikacyjnymi
Name:		bitlbee
Version:	3.0.5
Release:	0.1
License:	GPL v2+ and MIT
Group:		Daemons
Source0:	http://get.bitlbee.org/src/%{name}-%{version}.tar.gz
# Source0-md5:	9ff97260a2a7f3a7d102db158a8d9887
URL:		http://www.bitlbee.org/
BuildRequires:	gnutls-devel
%{?with_otr:BuildRequires:	libotr-devel >= 3.2.0}
BuildRequires:	systemd-units
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

%prep
%setup -q

# fix wrong assumption with $DESTDIR
%{__sed} -i -e 's,$(shell id -u),0,' Makefile

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
%if %{with otr}
	--otr=plugin \
%endif

%{__make}

### FIXME: Documentation needs old sgmltools tool, deprecated.
#%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}

%{__make} install install-dev install-etc install-systemd \
	DESTDIR=$RPM_BUILD_ROOT

# Install some files manually to their correct destination
#install -d $RPM_BUILD_ROOT{%{_localstatedir}/lib,%{_libdir}}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,CHANGES,CREDITS,FAQ,README}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/bitlbee.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/motd.txt
%attr(755,root,root) %{_sbindir}/bitlbee
%{_mandir}/man5/bitlbee.conf.5*
%{_mandir}/man8/bitlbee.8*
%{_datadir}/bitlbee
%attr(700,root,root) %{_localstatedir}/lib/bitlbee
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
