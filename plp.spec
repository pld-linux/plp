Summary: PLP Printing Package
Name: plp
Version: 4.1.2
Release: 1
Copyright: complicated
Group: Utilities/System
Source: plp-lpd-%{version}.tar.gz
Source1: lpd.init
Patch: plp-%{version}-rh.patch
BuildRoot: /tmp/plp-root
%description
PLP is a updated and improved version of the standard UNIX lpr printing
system. It features enhanced accounting and security, and backwards
compatibility.

%Changelog
* Sun Jun 06 1999 Vu Hung Quan <binaire@binaire.cx>
- Update to 4.1.2 ; adapted from Suse source

%prep
%setup
%patch -p1 -b .rh

%build
cd src
./configure --prefix=/usr
make SHN_CFLAGS=-DSHORTHOSTNAME 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/sbin \
 $RPM_BUILD_ROOT/etc/rc.d/init.d \
 $RPM_BUILD_ROOT/usr/bin \
 $RPM_BUILD_ROOT/usr/man/man1 \
 $RPM_BUILD_ROOT/usr/man/man5 \
 $RPM_BUILD_ROOT/usr/man/man8 \
 $RPM_BUILD_ROOT/usr/man/man3

cd src
make INSTALL_BIN=$RPM_BUILD_ROOT/usr/bin \
INSTALL_LIB=$RPM_BUILD_ROOT/usr/sbin \
INSTALL_MAINT=$RPM_BUILD_ROOT/usr/bin \
INSTALL_MAN=$RPM_BUILD_ROOT/usr/man install install.man

strip $RPM_BUILD_ROOT/usr/bin/* $RPM_BUILD_ROOT/usr/sbin/* ||:
cd ..
install -m 644 -o root -g root plp.conf $RPM_BUILD_ROOT/etc/plp.conf
install -m 644 -o root -g root printer_perms $RPM_BUILD_ROOT/etc/printer_perms

install -m755 $RPM_SOURCE_DIR/lpd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/lpd
( cd $RPM_BUILD_ROOT
mkdir -p ./etc/rc.d/{rc0.d,rc1.d,rc2.d,rc3.d,rc4.d,rc5.d,rc6.d}
  ln -sf ../init.d/lpd ./etc/rc.d/rc0.d/K60lpd
  ln -sf ../init.d/lpd ./etc/rc.d/rc1.d/K60lpd
  ln -sf ../init.d/lpd ./etc/rc.d/rc2.d/S60lpd
  ln -sf ../init.d/lpd ./etc/rc.d/rc3.d/S60lpd
  ln -sf ../init.d/lpd ./etc/rc.d/rc5.d/S60lpd
  ln -sf ../init.d/lpd ./etc/rc.d/rc6.d/K60lpd
  mkdir -p ./var/spool/lpd
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "`hostname -f`		*	*	*		R	A	0	0" >> /etc/printer_perms
/usr/bin/checkpc -f > /dev/null 2>&1


%files
%doc FEATURES HINTS README LICENSE
%doc doc/%-escapes doc/README.lp-pipes doc/plp.xpm
%doc doc/PLP/manual.ps doc/PLP/manual.rtf doc/PLP/manual.txt
%config /etc/plp.conf
%config /etc/printer_perms
%config /etc/rc.d/init.d/lpd
/etc/rc.d/rc2.d/S60lpd
/etc/rc.d/rc3.d/S60lpd
/etc/rc.d/rc5.d/S60lpd
/etc/rc.d/rc0.d/K60lpd
/etc/rc.d/rc1.d/K60lpd
/etc/rc.d/rc6.d/K60lpd
/usr/sbin/lpd
/usr/bin/lpr
/usr/bin/lpq
/usr/bin/lprm
/usr/bin/lpc
/usr/bin/pac
/usr/bin/checkpc
/usr/bin/setstatus
/usr/bin/printers
/usr/bin/lp
/usr/bin/lpstat
/usr/man/man1/lpc.1
/usr/man/man1/lpq.1
/usr/man/man1/lpr.1
/usr/man/man1/lprm.1
/usr/man/man5/printcap.5
/usr/man/man8/checkpc.8
/usr/man/man8/lpd.8
/usr/man/man8/pac.8
/usr/man/man8/setstatus.8
