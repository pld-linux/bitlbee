Summary:	An IRC to other chat networks gateway
Summary(pl.UTF-8):	Bramka pomiędzy IRC-em i innymi sieciami komunikacyjnymi
Name:		bitlbee
Version:	1.2.3
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://get.bitlbee.org/src/%{name}-%{version}.tar.gz
# Source0-md5:	2b1674d98804970809de3da3edf0bed2
URL:		http://www.bitlbee.org/
BuildRequires:	gnutls-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An IRC to other chat networks gateway. This program can be used as an
IRC server which forwards everything you say to people on other chat
networks like MSN/ICQ/Jabber.

%description -l pl.UTF-8
Bramka pomiędzy IRC-em i innymi sieciami komunikacyjnymi. Ten program
może być używany jako serwer IRC przekazujący wszystko co się mówi do
ludzi korzystających z innych sieci komunikacyjnych, takich jak
MSN/ICQ/Jabber.

%prep
%setup -q

%build
./configure \
	--datadir="%{_datadir}/bitlbee" \
	--etcdir=%{_sysconfdir} \
	--prefix=%{_prefix} \
	--ssl=gnutls

%{__make}
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
%{_mandir}/man?/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/bitlbee
%attr(700,root,root) %{_localstatedir}/lib/bitlbee
