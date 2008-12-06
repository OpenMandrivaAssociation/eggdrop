Name:		eggdrop
Version:	1.6.19
Release:	%mkrel 3
Summary:	IRC bot, written in C
Source0:	ftp://ftp.eggheads.org/pub/eggdrop/source/1.6/%{name}%{version}.tar.bz2
Patch0:		eggdrop1.6.17-64bit-fixes.patch
Patch1:		01_CVE-2007-2807_servmsg.patch
# Kludge build for Tcl 8.6 (interp->result, TIP #330) - AdamW 2008/12
Patch2:		eggdrop1.6.19-tcl86.patch
Group:		Networking/IRC
BuildRequires:	tcl tcl-devel perl
URL:		http://www.eggheads.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPLv2+

%description
Eggdrop is an IRC bot, written in C.  If you don't know what IRC is,
this is probably not whatever you're looking for!  Eggdrop, being a
 bot, sits on a channel and takes protective measures: to keep the
channel from being taken over (in the few ways that anything CAN),

to recognize banished users or sites and reject them, to recognize
privileged users and let them gain ops, etc.

%prep
%setup -q -n eggdrop%{version}
%patch0 -p1 -b .64bit-fixes
#%patch1 -p0 -b .overflow
%patch2 -p1 -b .tcl86
autoconf
  
%build
export CPPFLAGS="-DHAVE_TCL_THREADS"
#any optimizations on PPC break bots
%ifnarch ppc
export CFLAGS="$RPM_OPT_FLAGS"
%endif
./configure --prefix=%{_prefix} --libdir=%{_libdir}

make config

%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/eggdrop
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}
mkdir -p $RPM_BUILD_ROOT%{_mandir}

make install prefix=$RPM_BUILD_ROOT%{_libdir}/eggdrop
cd $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_libdir}/eggdrop/doc/man1/ $RPM_BUILD_ROOT%{_mandir}

#rpm installation complains otherwise due to rpm looking up the executables..
perl -pi -e s":/path/to/executable/eggdrop:%{_libdir}/eggdrop/eggdrop:" $RPM_BUILD_DIR/eggdrop%{version}/eggdrop.conf
cp -fR $RPM_BUILD_DIR/eggdrop%{version}/eggdrop.conf $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
#cp -Rf $RPM_BUILD_DIR/eggdrop%{version}/eggdrop.simple.conf $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
cp -Rf $RPM_BUILD_DIR/eggdrop%{version}/scripts/botchk $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
#cp -fR $RPM_BUILD_DIR/eggdrop%{version}/eggdrop.advanced.conf $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
#cp -fR $RPM_BUILD_DIR/eggdrop%{version}/eggdrop.complete.conf $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
#grumble rpm grumble wanted to require /path/to/eggdrop
#bzip2 -9f $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/eggdrop.conf.dist

rm -rf $RPM_BUILD_ROOT%{_libdir}/eggdrop/filesys
cp -Rf $RPM_BUILD_ROOT%{_libdir}/eggdrop/doc/* $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
rm -rf $RPM_BUILD_ROOT%{_libdir}/eggdrop/doc/
cp $RPM_BUILD_ROOT%{_libdir}/eggdrop/README $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/

# removing uneeded stuff
rm -rf %{buildroot}%{_libdir}/eggdrop/README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
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

