Summary:	An IRC to other chat networks gateway
Summary(pl):	Bramka pomiêdzy IRC-em i innymi sieciami komunikacyjnymi
Name:		bitlbee
Version:	1.0.1
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://get.bitlbee.org/src/%{name}-%{version}.tar.gz
# Source0-md5:	a4d7daa9b64898dd41a3a6d104692d9a
URL:		http://www.bitlbee.org/
BuildRequires:	gnutls-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An IRC to other chat networks gateway. This program can be used as an
IRC server which forwards everything you say to people on other chat
networks like MSN/ICQ/Jabber.

%description -l pl
Bramka pomiêdzy IRC-em i innymi sieciami komunikacyjnymi. Ten program
mo¿e byæ u¿ywany jako serwer IRC przekazuj±cy wszystko co siê mówi do
ludzi korzystaj±cych z innych sieci komunikacyjnych, takich jak
MSN/ICQ/Jabber.

%prep
%setup -q

%build
./configure \
	--datadir="%{_datadir}/bitlbee" \
	--etcdir=%{_sysconfdir} \
	--prefix=%{_prefix} \
	--ssl=gnutls
%{__make} %{?_smp_mflags}
### FIXME: Documentation needs old sgmltools tool, deprecated.
#%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_datadir}/bitlbee/ \
	$RPM_BUILD_ROOT%{_mandir}/man{5,8}/ \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/bitlbee

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install bitlbee $RPM_BUILD_ROOT%{_sbindir}
install doc/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
install doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,CHANGES,CREDITS,FAQ,README}
%doc %{_mandir}/man?/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/bitlbee
%attr(700,root,root) %{_localstatedir}/lib/bitlbee
