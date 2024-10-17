Name:		eggdrop
Version:	1.9.0
Release:	1
Summary:	IRC bot, written in C
Source0:	http://ftp.eggheads.org/pub/%{name}/source/1.9/%{name}-%{version}.tar.gz
Group:		Networking/IRC
URL:		https://www.eggheads.org/
License:	GPLv2+
BuildRequires:	perl
BuildRequires:	tcl 
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(openssl)

%description
Eggdrop is an IRC bot, written in C.  If you don't know what IRC is,
this is probably not whatever you're looking for!  Eggdrop, being a
 bot, sits on a channel and takes protective measures: to keep the
channel from being taken over (in the few ways that anything CAN),

to recognize banished users or sites and reject them, to recognize
privileged users and let them gain ops, etc.

%prep
%autosetup -p1

%build
export CPPFLAGS="%{optflags} -DHAVE_TCL_THREADS"
#any optimizations on PPC break bots
%ifnarch ppc
export CFLAGS="%optflags"
%endif
%configure2_5x --prefix=%{_prefix} --libdir=%{_libdir}

make config

%make_build LD="gcc %ldflags" \
	SHLIB_LD="gcc -shared -nostartfiles %ldflags" \
	MOD_LD="gcc %ldflags"

%install
mkdir -p %{buildroot}%{_libdir}/eggdrop
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_docdir}/eggdrop-%{version}
mkdir -p %{buildroot}%{_mandir}

%make_install prefix=%{buildroot}%{_libdir}/eggdrop
cd %{buildroot}
mv %{buildroot}%{_libdir}/eggdrop/doc/man1/ %{buildroot}%{_mandir}

#rpm installation complains otherwise due to rpm looking up the executables..
perl -pi -e s":/path/to/executable/eggdrop:%{_libdir}/eggdrop/eggdrop:" %{_builddir}/eggdrop%{version}/eggdrop.conf
cp -fR %{_builddir}/eggdrop%{version}/eggdrop.conf %{buildroot}%{_docdir}/eggdrop-%{version}/
cp -Rf %{_builddir}/eggdrop%{version}/scripts/botchk %{buildroot}%{_docdir}/eggdrop-%{version}/
rm -rf %{buildroot}%{_libdir}/eggdrop/filesys
cp -Rf %{buildroot}%{_libdir}/eggdrop/doc/* %{buildroot}%{_docdir}/eggdrop-%{version}/
rm -rf %{buildroot}%{_libdir}/eggdrop/doc/
mv %{buildroot}%{_libdir}/eggdrop/README %{buildroot}%{_docdir}/eggdrop-%{version}/

%files
%dir %{_libdir}/eggdrop
%dir %{_libdir}/eggdrop/language
%dir %{_libdir}/eggdrop/modules-%{version}
%dir %{_libdir}/eggdrop/help
%dir %{_libdir}/eggdrop/help/msg
%dir %{_libdir}/eggdrop/help/set
%dir %{_libdir}/eggdrop/scripts
%dir %{_libdir}/eggdrop/logs
%dir %{_libdir}/eggdrop/text
%{_libdir}/eggdrop/language/*.lang
%{_libdir}/eggdrop/text/*
%{_libdir}/eggdrop/logs/*
%{_libdir}/eggdrop/modules-%{version}/*.so
%{_libdir}/eggdrop/eggdrop-%{version}
%{_libdir}/eggdrop/eggdrop
%{_libdir}/eggdrop/help/*.help
%{_libdir}/eggdrop/help/msg/*.help
%{_libdir}/eggdrop/help/set/*.help
%{_libdir}/eggdrop/scripts/CONTENTS
%{_libdir}/eggdrop/scripts/*.tcl
%{_libdir}/eggdrop/scripts/botchk
%{_libdir}/eggdrop/scripts/autobotchk
%{_libdir}/eggdrop/scripts/weed
%{_libdir}/eggdrop/eggdrop.conf
%{_mandir}/man1/*

%doc %{_docdir}/*
%doc %{_libdir}/eggdrop/modules


%changelog
* Fri May 04 2012 Johnny A. Solbu <solbu@mandriva.org> 1.6.21-1
+ Revision: 795918
- New version
- Spec cleanup

* Tue Oct 05 2010 Funda Wang <fwang@mandriva.org> 1.6.20-1mdv2011.0
+ Revision: 583056
- New version 1.6.20

  + Oden Eriksson <oeriksson@mandriva.com>
    - revert as CVE-2009-1789 was fixed in the eggdrop1.6.19+ctcpfix.patch patch
    - P1: security fix for CVE-2009-1789

* Wed May 20 2009 Funda Wang <fwang@mandriva.org> 1.6.19-4mdv2010.0
+ Revision: 377930
- add patches

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 1.6.19-3mdv2009.1
+ Revision: 311127
- rebuild for new tcl
- add tcl86.patch (kludge build for Tcl 8.6)

* Mon Jun 16 2008 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 1.6.19-2mdv2009.0
+ Revision: 220395
- be sure to activate threaded tcl support, otherwise eggdrop will fail to fork
  in background (workaround for actual problem in tcl that prevents test from
  succeed, should rather be fixed properly in tcl, but no time for me today at
  least..)

* Fri May 02 2008 Funda Wang <fwang@mandriva.org> 1.6.19-1mdv2009.0
+ Revision: 200042
- New version 1.6.19

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.6.18-5mdv2008.1
+ Revision: 170809
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 1.6.18-4mdv2008.1
+ Revision: 149691
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 1.6.18-3mdv2008.0
+ Revision: 82011
- rebuild for new soname of tcl

* Thu Sep 06 2007 Adam Williamson <awilliamson@mandriva.org> 1.6.18-2mdv2008.0
+ Revision: 81293
- use Fedora license policy
- add patch1 (SECURITY FIX for overflow issue: CVE-2007-2807)

* Sat Apr 28 2007 Adam Williamson <awilliamson@mandriva.org> 1.6.18-1mdv2008.0
+ Revision: 18871
- 1.6.18 (rebuild for new era)
- drop patch0 (no longer needed), rename patch1 as patch0


* Sun Jan 01 2006 Oden Eriksson <oeriksson@mandriva.com> 1.6.17-3mdk
- rebuilt against soname aware deps (tcl/tk)
- fix deps

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.6.17-2mdk
- Rebuild

* Thu Nov 11 2004 Per Ã˜yvind Karlsen <peroyvind@linux-mandrake.com> 1.6.17-1mdk
- 1.6.17
- regenerate P0 & P1

* Sun Jul 25 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.6.16-1mdk
- 1.6.16
- regenerate P0
- drop useless prefix
- cosmetics

* Wed Oct 08 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.6.15-3mdk
- lib64 & some 64-bit fixes

* Mon Aug 11 2003 Per Ã˜yvind Karlsen <peroyvind@linux-mandrake.com> 1.6.15-2mdk
- from Pekka Savola <pekkas@netcore.fi>:
	o fix eggdrop.conf run-path so installing the RPM works
	o also install the eggdrop symlink, not just the version-specific binary
	o use make not %%make to enable build on Red Hat Linux. (peroyvind: it doesn't
	  support parallell make anyways)

* Fri May 09 2003 Per Ã˜yvind Karlsen <peroyvind@sintrax.net> 1.6.15-1mdk
- version 1.6.15
- rm -rf $RPM_BUILD_ROOT in correct stage
- actually use optimize flags
- configure with libdir
- minor cleanups

* Mon Feb 03 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 1.6.13-2mdk
- change url

* Mon Jan 13 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 1.6.13-1mdk
- version 1.6.13

* Wed Jul 24 2002 damien <dchaumette@mandrakesoft.com> 1.6.10-1mdk
- version 1.6.10
- remove tcl/tk version checking

* Thu Feb 28 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.6.6-5mdk
- Don't make eggdrop require on a versionless tcl.
- Don't run aclocal and autoconf (normally required for a patch to
  configure), because it seems broke. The patch itself contains both
  patches to aclocal.m4 and configure.

* Wed Oct 31 2001 Stew Benedict <sbenediict@mandrakesoft.com> 1.6.6-4mdk
- no optimizations for PPC build, else broken bots

* Tue Oct 30 2001 Ludovic Francois <lfrancois@mandrakesoft.com> 1.6.6-3mdk
- clean spec file removed useless ./configure

* Thu Oct 25 2001 Ludovic Francois <lfrancois@mandrakesoft.com> 1.6.6-2mdk
- Rebuild for rpmlint.

* Thu Aug 30 2001 Etienne Faure  <etienne@mandrakesoft.com> 1.6.6-1mdk
- 1.6.6

* Fri Apr 27 2001 Etienne Faure  <etienne@mandrakesoft.com> 1.6.4-1mdk
- 1.6.4
- removed now useless patch

* Sat Jan 20 2001 Etienne Faure  <etienne@mandrakesoft.com> 1.6.2-3mdk
- updated to new version + patch

* Sat Jan 20 2001 Etienne Faure  <etienne@mandrakesoft.com> 1.6.1-2mdk
- bz2'ed man page

* Fri Nov 24 2000 Geoffrey Lee <sniltalk@mandrakesoft.com> 1.6.1-1mdk
- new and shiny source.
- fix the build for the new version.
- short_circuit_me_babe.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.4.4-2mdk
- automatically added BuildRequires

* Wed Jul 26 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 1.4.4-1mdk
- Release 1.4.4
- clean spec

* Wed Jul 26 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 1.4.3-2mdk
- BM + macroszification

* Wed Apr 19 2000 Daouda Lo <daouda@mandrakesoft.com> 1.4.3-1mdk
- big release 1.3.23 -> 1.4.3
- many bug fixes 
- cleanup spec

* Tue Apr 18 2000 Daouda Lo <daouda@mandrakesoft.com> 1.3.23-5mdk
- fix group.
- spec cleanup.
- SMP build/check

* Thu Nov 04 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Forgot defattr

* Tue Nov 02 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Update bzip and SMP build macros
- Add botchk to docs

* Sat Jul 10 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- add default langfile patch 
- Added a few posible optimizations i missed

* Fri Jul 09 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Initial rpm

