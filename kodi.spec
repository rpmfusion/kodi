#global PRERELEASE rc3
%global DIRVERSION %{version}
#global GITCOMMIT Gotham_r2-ge988513
# use the line below for pre-releases
#global DIRVERSION %{version}%{PRERELEASE}
%global _hardened_build 1

Name: kodi
Version: 14.0
Release: 2%{?dist}
Summary: Media center

License: GPLv2+ and GPLv3+ and LGPLv2+ and BSD and MIT
# Main binary and all supporting files are GPLv2+/GPLv3+
# Some supporting libraries use the LGPL / BSD / MIT license
Group: Applications/Multimedia
URL: http://www.kodi.tv/
Source0: %{name}-%{DIRVERSION}-patched.tar.xz
# kodi contains code that we cannot ship, as well as redundant private
# copies of upstream libraries that we already distribute.  Therefore
# we use this script to remove the code before shipping it.
# Invoke this script while in the directory where the tarball is located:
# ./kodi-generate-tarball-xz.sh
Source1: kodi-generate-tarball-xz.sh

# filed ticket, but patch still needs work
# http://trac.xbmc.org/ticket/9658
Patch1: xbmc-13.0-dvdread.patch

# need to file trac ticket, this patch just forces external hdhomerun
# functionality, needs to be able fallback internal version
Patch2: kodi-14.0-hdhomerun.patch

# Avoid segfault during goom's configure
# https://bugzilla.redhat.com/1069079
Patch3: xbmc-13.0-libmysqlclient.patch

# Set program version parameters
Patch4: kodi-14.0-versioning.patch

# Remove call to internal ffmpeg function (misued anyway)
Patch5: kodi-14.0-dvddemux-ffmpeg.patch

# Kodi is the renamed XBMC project
Obsoletes: xbmc < 14.0-1
Provides: xbmc = %{version}

# Optional deps (not in EPEL)
%if 0%{?fedora}
# (libbluray in EPEL 6 is too old.)
%global _with_libbluray 1
%global _with_cwiid 1
%global _with_libssh 1
%global _with_libcec 1
%global _with_external_ffmpeg 1
%endif

%ifarch x86_64 i686
%global _with_crystalhd 1
%global _with_hdhomerun 1
%endif

# Upstream does not support ppc64
ExcludeArch: ppc64

BuildRequires: SDL-devel
BuildRequires: SDL_image-devel
BuildRequires: SDL_mixer-devel
BuildRequires: a52dec-devel
BuildRequires: afpfs-ng-devel
BuildRequires: avahi-devel
BuildRequires: bluez-libs-devel
BuildRequires: boost-devel
BuildRequires: bzip2-devel
BuildRequires: cmake
%if 0%{?_with_cwiid}
BuildRequires: cwiid-devel
%endif
BuildRequires: dbus-devel
BuildRequires: desktop-file-utils
BuildRequires: e2fsprogs-devel
BuildRequires: enca-devel
BuildRequires: expat-devel
BuildRequires: faad2-devel
%if 0%{?_with_external_ffmpeg}
BuildRequires: ffmpeg-devel
%endif
BuildRequires: flac-devel
BuildRequires: flex
BuildRequires: fontconfig-devel
BuildRequires: fontpackages-devel
BuildRequires: freetype-devel
BuildRequires: fribidi-devel
%if 0%{?el6}
BuildRequires: gettext-devel
%else
BuildRequires: gettext-autopoint
%endif
BuildRequires: glew-devel
BuildRequires: glib2-devel
BuildRequires: gperf
%if 0%{?_with_hdhomerun}
BuildRequires: hdhomerun-devel
%endif
BuildRequires: jasper-devel
BuildRequires: java-devel
BuildRequires: lame-devel
BuildRequires: libXinerama-devel
BuildRequires: libXmu-devel
BuildRequires: libXtst-devel
BuildRequires: libass-devel >= 0.9.7
%if 0%{?_with_libbluray}
BuildRequires: libbluray-devel
%endif
BuildRequires: libcap-devel
BuildRequires: libcdio-devel
%if 0%{?_with_libcec}
BuildRequires: libcec-devel >= 2.2.0
%endif
%if 0%{?_with_crystalhd}
BuildRequires: libcrystalhd-devel
%endif
BuildRequires: libcurl-devel
BuildRequires: libdca-devel
BuildRequires: libdvdread-devel
%if 0%{?el6}
BuildRequires: libjpeg-devel
%else
BuildRequires: libjpeg-turbo-devel
%endif
BuildRequires: libmad-devel
BuildRequires: libmicrohttpd-devel
BuildRequires: libmms-devel
BuildRequires: libmodplug-devel
BuildRequires: libmpcdec-devel
BuildRequires: libmpeg2-devel
BuildRequires: libogg-devel
# for AirPlay support
BuildRequires: libplist-devel
BuildRequires: libpng-devel
BuildRequires: librtmp-devel
BuildRequires: libsamplerate-devel
BuildRequires: libsmbclient-devel
%if 0%{?_with_libssh}
BuildRequires: libssh-devel
%endif
BuildRequires: libtiff-devel
BuildRequires: libtool
%ifnarch %{arm}
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
%endif
BuildRequires: libvorbis-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: lzo-devel
BuildRequires: mariadb-devel
# ARM uses GLES
%ifarch %{arm}
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
%endif
BuildRequires: nasm
BuildRequires: pcre-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: python-devel
BuildRequires: python-pillow
BuildRequires: sqlite-devel
BuildRequires: swig
BuildRequires: systemd-devel
BuildRequires: taglib-devel >= 1.8
BuildRequires: tinyxml-devel
BuildRequires: tre-devel
BuildRequires: trousers-devel
BuildRequires: wavpack-devel
BuildRequires: yajl-devel
BuildRequires: zlib-devel

# nfs-utils-lib-devel package currently broken
#BuildRequires: nfs-utils-lib-devel

Requires: google-roboto-fonts
# need explicit requires for these packages
# as they are dynamically loaded via XBMC's arcane
# pseudo-DLL loading scheme (sigh)
%if 0%{?_with_libbluray}
Requires: libbluray%{?_isa}
%endif
%if 0%{?_with_libcec}
Requires: libcec%{?_isa} >= 2.2.0
%endif
%if 0%{?_with_crystalhd}
Requires: libcrystalhd%{?_isa}
%endif
Requires: libmad%{?_isa}
Requires: librtmp%{?_isa}

# needed when doing a minimal install, see
# https://bugzilla.rpmfusion.org/show_bug.cgi?id=1844
Requires: glx-utils
Requires: xorg-x11-utils

# This is just symlinked to, but needed both at build-time
# and for installation
Requires: python-pillow%{?_isa}


%description
Kodi is a free cross-platform media-player jukebox and entertainment hub.
Kodi can play a spectrum of of multimedia formats, and featuring playlist,
audio visualizations, slideshow, and weather forecast functions, together
third-party plugins.


%package devel
Summary: Development files needed to compile C programs against kodi
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Kodi is a free cross-platform media-player jukebox and entertainment hub.
If you want to develop programs which use Kodi's libraries, you need to
install this package.


%package eventclients
Summary: Media center event client remotes

%description eventclients
This package contains support for using Kodi with the PS3 Remote, the Wii
Remote, a J2ME based remote and the command line xbmc-send utility.

%package eventclients-devel
Summary: Media center event client remotes development files
Requires:	%{name}-eventclients%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes: xbmc-eventclients < 14.0-1
Provides:  xbmc-eventclients = %{version}

%description eventclients-devel
This package contains the development header files for the eventclients
library.


%prep
%setup -q -n %{name}-%{DIRVERSION}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0

%if 0%{?_with_hdhomerun}
%else
  # Remove hdhomerun from the build.
  pushd xbmc/filesystem/
    rm HDHomeRunFile.cpp HDHomeRunFile.h
    rm HDHomeRunDirectory.cpp HDHomeRunDirectory.h
    sed -i Makefile.in -e '/HDHomeRunFile\.cpp/d'
    sed -i Makefile.in -e '/HDHomeRunDirectory\.cpp/d'
    sed -i DirectoryFactory.cpp -e '/HomeRun/d'
    sed -i FileFactory.cpp -e '/HomeRun/d'
  popd
%endif


%build
chmod +x bootstrap
./bootstrap
# Can't use export nor %%configure (implies using export), because
# the Makefile pile up *FLAGS in this case.

./configure \
--prefix=%{_prefix} --bindir=%{_bindir} --includedir=%{_includedir} \
--libdir=%{_libdir} --datadir=%{_datadir} \
--with-lirc-device=/var/run/lirc/lircd \
%if 0%{?_with_external_ffmpeg}
--with-ffmpeg=shared \
%endif
--enable-goom \
--enable-pulse \
%if 0%{?_with_libcec}
--enable-libcec \
%else
--disable-libcec \
%endif
%if 0%{?_with_libssh}
--enable-ssh \
%else
--disable-ssh \
%endif
--disable-dvdcss \
--disable-optimizations --disable-debug \
%ifnarch %{arm}
--enable-gl \
--disable-gles \
--enable-vdpau \
%else
--enable-gles \
--disable-vdpau \
--disable-vaapi \
%ifarch armv7hl \
--enable-tegra \
--disable-neon \
%endif
%ifarch armv7hnl
--enable-neon \
%endif
%endif
CFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/afpfs-ng/ -I/usr/include/samba-4.0/ -D__STDC_CONSTANT_MACROS" \
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/afpfs-ng/ -I/usr/include/samba-4.0/ -D__STDC_CONSTANT_MACROS" \
LDFLAGS="-fPIC" \
%if 0%{?_with_hdhomerun}
LIBS=" -lhdhomerun $LIBS" \
%endif
ASFLAGS=-fPIC

make %{?_smp_mflags} VERBOSE=1


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
make -C tools/EventClients DESTDIR=$RPM_BUILD_ROOT install
# remove the doc files from unversioned /usr/share/doc/xbmc, they should be in versioned docdir
rm -r $RPM_BUILD_ROOT/%{_datadir}/doc/

desktop-file-install \
 --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
 $RPM_BUILD_ROOT%{_datadir}/applications/kodi.desktop

# Normally we are expected to build these manually. But since we are using
# the system Python interpreter, we also want to use the system libraries
install -d $RPM_BUILD_ROOT%{_libdir}/kodi/addons/script.module.pil/lib
ln -s %{python_sitearch}/PIL $RPM_BUILD_ROOT%{_libdir}/kodi/addons/script.module.pil/lib/PIL
#install -d $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib
#ln -s %{python_sitearch}/pysqlite2 $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib/pysqlite2

# Use external Roboto font files instead of bundled ones
ln -sf %{_fontbasedir}/google-roboto/Roboto-Regular.ttf ${RPM_BUILD_ROOT}%{_datadir}/kodi/addons/skin.confluence/fonts/
ln -sf %{_fontbasedir}/google-roboto/Roboto-Bold.ttf ${RPM_BUILD_ROOT}%{_datadir}/kodi/addons/skin.confluence/fonts/

# Move man-pages into system dir
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/
mv docs/manpages ${RPM_BUILD_ROOT}%{_mandir}/man1/


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
rmdir %{_libdir}/xbmc %{_datadir}/xbmc
ln -s kodi ${RPM_BUILD_ROOT}%{_libdir}/xbmc
ln -s kodi ${RPM_BUILD_ROOT}%{_datadir}/xbmc


%posttrans devel
rmdir %{_includedir}/xbmc
ln -s kodi ${RPM_BUILD_ROOT}%{_includedir}/xbmc


%files
%license copying.txt LICENSE.GPL
%doc CONTRIBUTORS README.md docs
%{_bindir}/kodi
%{_bindir}/kodi-standalone
%{_bindir}/xbmc
%{_bindir}/xbmc-standalone
%{_libdir}/kodi
%ghost %{_libdir}/xbmc
%{_datadir}/kodi
%ghost %{_datadir}/xbmc
%{_datadir}/xsessions/kodi.desktop
%{_datadir}/xsessions/xbmc.desktop
%{_datadir}/applications/kodi.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_mandir}/man1/kodi.1.gz
%{_mandir}/man1/kodi.bin.1.gz
%{_mandir}/man1/kodi-standalone.1.gz


%files devel
%{_includedir}/kodi
%ghost %{_includedir}/xbmc


%files eventclients
%license copying.txt LICENSE.GPL
%python_sitelib/kodi
%dir %{_datadir}/pixmaps/kodi
%{_datadir}/pixmaps/kodi/*.png
%{_bindir}/kodi-j2meremote
%{_bindir}/kodi-ps3d
%{_bindir}/kodi-ps3remote
%{_bindir}/kodi-send
%{_bindir}/kodi-wiiremote
%{_mandir}/man1/kodi-j2meremote.1.gz
%{_mandir}/man1/kodi-ps3remote.1.gz
%{_mandir}/man1/kodi-send.1.gz
%{_mandir}/man1/kodi-standalone.1.gz
%{_mandir}/man1/kodi-wiiremote.1.gz


%files eventclients-devel
%{_includedir}/kodi/xbmcclient.h


%changelog
* Mon Jan 05 2015 Michael Cronenworth <mike@cchtml.com> - 14.0-2
- Fix xbmc upgrade path

* Sun Dec 28 2014 Michael Cronenworth <mike@cchtml.com> - 14.0-1
- Update to 14.0 final

* Tue Dec 09 2014 Michael Cronenworth <mike@cchtml.com> - 14.0-0.4.rc3
- Update to 14.0 RC3

* Sun Nov 09 2014 Michael Cronenworth <mike@cchtml.com> - 14.0-0.3.beta2
- Update to 14.0 beta 2

* Tue Sep 02 2014 Michael Cronenworth <mike@cchtml.com> - 14.0-0.2.alpha3
- Update to 14.0 alpha 3

* Sun Aug 24 2014 Michael Cronenworth <mike@cchtml.com> - 14.0-0.1.alpha2
- Update to 14.0 alpha 2
- Renamed XBMC to Kodi
