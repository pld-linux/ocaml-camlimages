Summary:	Image processing library for OCaml
Summary(pl.UTF-8):	Biblioteka przetwarzania obrazów dla OCamla
Name:		ocaml-camlimages
Version:	2.12
Release:	1
License:	LGPL with additional linking exception
Group:		Libraries
Source0:	ftp://ftp.inria.fr/INRIA/Projects/cristal/caml-light/bazar-ocaml/camlimages-%{version}.tgz
# Source0-md5:	6662c0a3e7653a731410cd9783a55bfb
Patch0:		%{name}-ac.patch
Patch1:		%{name}-kill-gtk.patch
URL:		http://pauillac.inria.fr/camlimages/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	ghostscript
BuildRequires:	giflib-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	ocaml >= 3.04-7
# our lablgtk is too recent
#BuildRequires:	ocaml-lablgtk-devel
BuildRequires:	ocaml-x11graphics-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is an image processing library, which provides some basic
functions of image processing and loading/saving various image file
formats.

This package contains files needed to run bytecode executables using
this library.

%description -l pl.UTF-8
Jest to biblioteka przetwarzania obrazów, dostarczająca pewnych
podstawowych funkcji przetwarzania oraz wczytywania/nagrywania różnych
formatów plików graficznych.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	Image processing library for OCaml - development part
Summary(pl.UTF-8):	Biblioteka przetwarzania obrazów dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This is an image processing library, which provides some basic
functions of image processing and loading/saving various image file
formats.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Jest to biblioteka przetwarzania obrazów, dostarczająca pewnych
podstawowych funkcji przetwarzania oraz wczytywania/nagrywania różnych
formatów plików graficznych.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n camlimages-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure
%{__make} all opt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/camlimages

%{__make} install \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/camlimages

(cd $RPM_BUILD_ROOT%{_libdir}/ocaml && ln -s camlimages/dll*.so .)

gzip -9nf $RPM_BUILD_ROOT%{_libdir}/ocaml/camlimages/*.mli
mv -f $RPM_BUILD_ROOT%{_libdir}/ocaml/camlimages/*.mli.gz .

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# remove empty directories
rm -r $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/{slideanim,animator}

# TODO: this is fucked up and should be split into subpackages
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ci_core
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ci_core/META <<EOF
requires = ""
version = "%{version}"
directory = "+camlimages"
archive(byte) = "ci_core.cma"
archive(native) = "ci_core.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE CHANGES README
%dir %{_libdir}/ocaml/camlimages
%attr(755,root,root) %{_libdir}/ocaml/camlimages/*.so
%attr(755,root,root) %{_libdir}/ocaml/*.so

%files devel
%defattr(644,root,root,755)
%doc doc/*
%{_libdir}/ocaml/camlimages/*.cm[ixa]*
%{_libdir}/ocaml/camlimages/*.a
%{_libdir}/ocaml/camlimages/Makefile.config
%{_libdir}/ocaml/camlimages/*.h
%{_libdir}/ocaml/site-lib/ci_core
%{_examplesdir}/%{name}-%{version}
