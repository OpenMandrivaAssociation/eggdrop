Name:		eggdrop
Version:	1.6.20
Release:	%mkrel 1
Summary:	IRC bot, written in C
Source0:	ftp://ftp.eggheads.org/pub/eggdrop/source/1.6/%{name}%{version}.tar.bz2
Patch4:		eggdrop1.6.19-fix-str-fmt.patch
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
%patch4 -p0 -b .str

%build
export CPPFLAGS="%{optflags} -DHAVE_TCL_THREADS"
#any optimizations on PPC break bots
%ifnarch ppc
export CFLAGS="%optflags"
%endif
%configure2_5x --prefix=%{_prefix} --libdir=%{_libdir}

make config

#sed -i -e "s#LD = gcc#LD = gcc %ldflags#g" Makefile

%make LD="gcc %ldflags" \
	SHLIB_LD="gcc -shared -nostartfiles %ldflags" \
	MOD_LD="gcc %ldflags"

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
perl -pi -e s":/path/to/executable/eggdrop:%{_libdir}/eggdrop/eggdrop:" %{_builddir}/eggdrop%{version}/eggdrop.conf
cp -fR %{_builddir}/eggdrop%{version}/eggdrop.conf $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
#cp -Rf %{_builddir}/eggdrop%{version}/eggdrop.simple.conf $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
cp -Rf %{_builddir}/eggdrop%{version}/scripts/botchk $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
#cp -fR %{_builddir}/eggdrop%{version}/eggdrop.advanced.conf $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
#cp -fR %{_builddir}/eggdrop%{version}/eggdrop.complete.conf $RPM_BUILD_ROOT%{_docdir}/eggdrop-%{version}/
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
