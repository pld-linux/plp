Summary:	PLP Printing Package
Name:		plp
Version:	4.1.2
Release:	1
License:	complicated
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source0:	plp-lpd-%{version}.tar.gz
Source1:	lpd.init
Patch0:		plp-%{version}-rh.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PLP is a updated and improved version of the standard UNIX lpr
printing system. It features enhanced accounting and security, and
backwards compatibility.


%prep
%setup -q
%patch -p1 -b .rh

%build
cd src
./configure --prefix=%{_prefix}
%{__make} SHN_CFLAGS=-DSHORTHOSTNAME 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_prefix}/man/man1 \
	$RPM_BUILD_ROOT%{_prefix}/man/man5 \
	$RPM_BUILD_ROOT%{_prefix}/man/man8 \
	$RPM_BUILD_ROOT%{_prefix}/man/man3

cd src
%{__make} INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_sbindir} \
	INSTALL_MAINT=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_prefix}/man install install.man

cd ..
install -o root plp.conf $RPM_BUILD_ROOT%{_sysconfdir}/plp.conf
install -o root printer_perms $RPM_BUILD_ROOT%{_sysconfdir}/printer_perms

install -m755 $RPM_SOURCE_DIR/lpd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/lpd
( cd $RPM_BUILD_ROOT
  install -d ./etc/rc.d/{rc0.d,rc1.d,rc2.d,rc3.d,rc4.d,rc5.d,rc6.d}
  ln -sf ../init.d/lpd ./etc/rc.d/rc0.d/K60lpd
  ln -sf ../init.d/lpd ./etc/rc.d/rc1.d/K60lpd
  ln -sf ../init.d/lpd ./etc/rc.d/rc2.d/S60lpd
  ln -sf ../init.d/lpd ./etc/rc.d/rc3.d/S60lpd
  ln -sf ../init.d/lpd ./etc/rc.d/rc5.d/S60lpd
  ln -sf ../init.d/lpd ./etc/rc.d/rc6.d/K60lpd
  install -d ./var/spool/lpd
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "`hostname -f`		*	*	*		R	A	0	0" >> /etc/printer_perms
/usr/bin/checkpc -f > /dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc FEATURES HINTS README LICENSE
%doc doc/%-escapes doc/README.lp-pipes doc/plp.xpm
%doc doc/PLP/manual.ps doc/PLP/manual.rtf doc/PLP/manual.txt
%config %{_sysconfdir}/plp.conf
%config %{_sysconfdir}/printer_perms
%config /etc/rc.d/init.d/lpd
/etc/rc.d/rc2.d/S60lpd
/etc/rc.d/rc3.d/S60lpd
/etc/rc.d/rc5.d/S60lpd
/etc/rc.d/rc0.d/K60lpd
/etc/rc.d/rc1.d/K60lpd
/etc/rc.d/rc6.d/K60lpd
%attr(755,root,root) %{_sbindir}/lpd
%attr(755,root,root) %{_bindir}/lpr
%attr(755,root,root) %{_bindir}/lpq
%attr(755,root,root) %{_bindir}/lprm
%attr(755,root,root) %{_bindir}/lpc
%attr(755,root,root) %{_bindir}/pac
%attr(755,root,root) %{_bindir}/checkpc
%attr(755,root,root) %{_bindir}/setstatus
%attr(755,root,root) %{_bindir}/printers
%attr(755,root,root) %{_bindir}/lp
%attr(755,root,root) %{_bindir}/lpstat
%{_prefix}/man/man1/lpc.1
%{_prefix}/man/man1/lpq.1
%{_prefix}/man/man1/lpr.1
%{_prefix}/man/man1/lprm.1
%{_prefix}/man/man5/printcap.5
%{_prefix}/man/man8/checkpc.8
%{_prefix}/man/man8/lpd.8
%{_prefix}/man/man8/pac.8
%{_prefix}/man/man8/setstatus.8
