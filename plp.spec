Summary:	PLP Printing Package
Summary(pl):	Pakiet drukuj±cy PLP
Name:		plp
Version:	4.1.2
Release:	4
License:	Free for non-commercial use
Group:		Applications/System
Source0:	ftp://ftp.informatik.uni-hamburg.de/ftpmnt/inf1/pub/os/unix/utils/plp-unibwhh/%{name}-lpd-%{version}.tar.gz
Source1:	lpd.init
#Patch0:		%{name}-%{version}-rh.patch
BuildRequires:	autoconf
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PLP is a updated and improved version of the standard UNIX lpr
printing system. It features enhanced accounting and security, and
backwards compatibility.

%description -l pl
PLP jest uaktualnion± i rozszerzon± wersj± standardowego uniksowego
systemu drukuj±cego lpr. Jego cechy to rozszerzona kontrola i
bezpieczeñstwo, a tak¿e wsteczna kompatybilno¶æ.

%prep
%setup -q
#%patch -p1

%build
cd src
%{__autoconf}
# struct statcfs doesn't contain f_basetype on Linux - don't use it
ac_cv_func_statvfs=no; export ac_cv_func_statvfs
%configure
%{__make} \
	CCOPTFLAGS="%{rpmcflags}" \
	SHN_CFLAGS=-DSHORTHOSTNAME

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_mandir}/man{1,3,5,8}

%{__make} -C src install install.man \
	INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_sbindir} \
	INSTALL_MAINT=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}

install plp.conf $RPM_BUILD_ROOT%{_sysconfdir}/plp.conf
install printer_perms $RPM_BUILD_ROOT%{_sysconfdir}/printer_perms

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/lpd

install -d $RPM_BUILD_ROOT/var/spool/lpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "`hostname -f`		*	*	*		R	A	0	0" >> /etc/printer_perms
/usr/bin/checkpc -f > /dev/null 2>&1
/sbin/chkconfig --add lpd

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del lpd
fi

%files
%defattr(644,root,root,755)
%doc FEATURES HINTS README LICENSE doc/{%-escapes,README.lp-pipes,plp.xpm} doc/PLP/manual.txt
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/plp.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/printer_perms
%attr(754,root,root) /etc/rc.d/init.d/lpd
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
%{_mandir}/man1/lpc.1*
%{_mandir}/man1/lpq.1*
%{_mandir}/man1/lpr.1*
%{_mandir}/man1/lprm.1*
%{_mandir}/man5/printcap.5*
%{_mandir}/man8/checkpc.8*
%{_mandir}/man8/lpd.8*
%{_mandir}/man8/pac.8*
%{_mandir}/man8/setstatus.8*
