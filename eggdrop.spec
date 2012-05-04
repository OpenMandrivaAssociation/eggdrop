Name:		eggdrop
Version:	1.6.21
Release:	1
Summary:	IRC bot, written in C
Source0:	ftp://ftp.eggheads.org/pub/eggdrop/source/1.6/%{name}%{version}.tar.bz2
Patch4:		eggdrop1.6.19-fix-str-fmt.patch
Group:		Networking/IRC
URL:		http://www.eggheads.org/
License:	GPLv2+
BuildRequires:	tcl 
BuildRequires:	tcl-devel
BuildRequires:	perl

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

%make LD="gcc %ldflags" \
	SHLIB_LD="gcc -shared -nostartfiles %ldflags" \
	MOD_LD="gcc %ldflags"

%install
mkdir -p %{buildroot}%{_libdir}/eggdrop
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_docdir}/eggdrop-%{version}
mkdir -p %{buildroot}%{_mandir}

%makeinstall prefix=%{buildroot}%{_libdir}/eggdrop
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
