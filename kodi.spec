#global PRERELEASE rc4
%global DIRVERSION %{version}
#global GITCOMMIT Gotham_r2-ge988513
# use the line below for pre-releases
#global DIRVERSION %{version}%{PRERELEASE}
%global _hardened_build 1
%global _with_dvd 0

Name: kodi
Version: 17.5
Release: 1%{?dist}
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

%if 0%{?_with_dvd}
# kodi uses modified libdvd{css,nav,read} source and downloads at build time
# wget -O kodi-libdvdnav-master.tar.gz https://github.com/xbmc/libdvdnav/archive/master.tar.gz
Source2: kodi-libdvdnav-master.tar.gz
# wget -O kodi-libdvdread-master.tar.gz https://github.com/xbmc/libdvdread/archive/master.tar.gz
Source3: kodi-libdvdread-master.tar.gz
# wget -O kodi-libdvdcss-master.tar.gz https://github.com/xbmc/libdvdcss/archive/master.tar.gz
Source4: kodi-libdvdcss-master.tar.gz
%endif

# Set program version parameters
Patch1: kodi-16.0-versioning.patch

%if 0%{?_with_dvd} == 0
# Drop DVD library support
Patch2: kodi-17a2-libdvd.patch
%endif

# Optional deps (not in EPEL)
%if 0%{?fedora}
# (libbluray in EPEL 6 is too old.)
%global _with_libbluray 1
%global _with_cwiid 1
%global _with_libssh 1
%global _with_libcec 1
%global _with_external_ffmpeg 1
%global _with_wayland 0
%endif

%ifarch x86_64 i686
%global _with_crystalhd 1
%endif

# Upstream does not support ppc64
# ARM support is restricted to one GPU per build
ExclusiveArch: i686 x86_64

BuildRequires: SDL2-devel
BuildRequires: SDL_image-devel
BuildRequires: a52dec-devel
BuildRequires: afpfs-ng-devel
BuildRequires: avahi-devel
BuildRequires: bluez-libs-devel
BuildRequires: boost-devel
BuildRequires: bzip2-devel
BuildRequires: cmake
BuildRequires: crossguid-devel
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
BuildRequires: jasper-devel
BuildRequires: java-devel
BuildRequires: lame-devel
BuildRequires: lcms2-devel
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
%if 0%{?fedora} > 24
BuildRequires: libcec-devel >= 4.0.0
%else
BuildRequires: libcec-devel < 4.0.0
%endif
%endif
%if 0%{?_with_crystalhd}
BuildRequires: libcrystalhd-devel
%endif
BuildRequires: libcurl-devel
BuildRequires: libdca-devel
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
BuildRequires: libnfs-devel
BuildRequires: libogg-devel
# for AirPlay support
BuildRequires: shairplay-devel
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
BuildRequires: libuuid-devel
%ifnarch %{arm}
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
%endif
BuildRequires: libvorbis-devel
%if 0%{?_with_wayland}
BuildRequires: libwayland-client-devel
%endif
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
BuildRequires: pixman-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: python-devel
BuildRequires: python-pillow
BuildRequires: sqlite-devel
BuildRequires: swig
BuildRequires: systemd-devel
BuildRequires: taglib-devel >= 1.10
BuildRequires: tinyxml-devel
BuildRequires: tre-devel
BuildRequires: trousers-devel
BuildRequires: wavpack-devel
%if 0%{?_with_wayland}
BuildRequires: weston-devel
%endif
BuildRequires: yajl-devel
BuildRequires: zlib-devel

Requires: dejavu-sans-fonts
# need explicit requires for these packages
# as they are dynamically loaded via XBMC's arcane
# pseudo-DLL loading scheme (sigh)
%if 0%{?_with_libbluray}
Requires: libbluray%{?_isa}
%endif
%if 0%{?_with_libcec}
%if 0%{?fedora} > 24
Requires: libcec%{?_isa} >= 4.0.0
%else
Requires: libcec%{?_isa} < 4.0.0
%endif
%endif
%if 0%{?_with_crystalhd}
Requires: libcrystalhd%{?_isa}
%endif
Requires: libmad%{?_isa}
Requires: librtmp%{?_isa}
Requires: shairplay-libs%{?_isa}

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
Obsoletes: xbmc-devel < 14.0
Provides: xbmc-devel = %{version}

%description devel
Kodi is a free cross-platform media-player jukebox and entertainment hub.
If you want to develop programs which use Kodi's libraries, you need to
install this package.


%package eventclients
Summary: Media center event client remotes
Obsoletes: xbmc-eventclients < 14.0
Provides: xbmc-eventclients = %{version}

%description eventclients
This package contains support for using Kodi with the PS3 Remote, the Wii
Remote, a J2ME based remote and the command line xbmc-send utility.

%package eventclients-devel
Summary: Media center event client remotes development files
Requires:	%{name}-eventclients%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes: xbmc-eventclients-devel < 14.0
Provides:  xbmc-eventclients-devel = %{version}

%description eventclients-devel
This package contains the development header files for the eventclients
library.


%prep
%setup -q -n %{name}-%{DIRVERSION}
%patch1 -p1 -b.versioning
%if 0%{?_with_dvd}
cp -p %{SOURCE2} tools/depends/target/libdvdnav/libdvdnav-master.tar.gz
cp -p %{SOURCE3} tools/depends/target/libdvdread/libdvdread-master.tar.gz
cp -p %{SOURCE4} tools/depends/target/libdvdcss/libdvdcss-master.tar.gz
%else
%patch2 -p1 -b.libdvd
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
%if 0%{?_with_wayland}
--enable-wayland \
%endif
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
%if 0%{?_with_dvd} == 0
--disable-optical-drive \
%endif
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
%endif
%endif
CFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/afpfs-ng/ -I/usr/include/samba-4.0/ -D__STDC_CONSTANT_MACROS" \
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/afpfs-ng/ -I/usr/include/samba-4.0/ -D__STDC_CONSTANT_MACROS" \
LDFLAGS="$RPM_LD_FLAGS -fPIC" \
ASFLAGS=-fPIC

make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
make -C tools/EventClients DESTDIR=$RPM_BUILD_ROOT install
# remove the doc files from unversioned /usr/share/doc/xbmc, they should be in versioned docdir
rm -r $RPM_BUILD_ROOT/%{_datadir}/doc/

desktop-file-install \
 --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
 $RPM_BUILD_ROOT%{_datadir}/applications/kodi.desktop

# Stop shipping the duplicate xsession file
rm -f $RPM_BUILD_ROOT/%{_datadir}/xsessions/xbmc.desktop

# Normally we are expected to build these manually. But since we are using
# the system Python interpreter, we also want to use the system libraries
install -d $RPM_BUILD_ROOT%{_libdir}/kodi/addons/script.module.pil/lib
ln -s %{python_sitearch}/PIL $RPM_BUILD_ROOT%{_libdir}/kodi/addons/script.module.pil/lib/PIL
#install -d $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib
#ln -s %{python_sitearch}/pysqlite2 $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib/pysqlite2

# Use external font files instead of bundled ones
ln -sf %{_fontbasedir}/dejavu/DejaVuSans-Bold.ttf ${RPM_BUILD_ROOT}%{_datadir}/kodi/addons/skin.estouchy/fonts/

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
if [ ! -L %{_libdir}/xbmc ] ; then
    if [ -d %{_libdir}/xbmc ] ; then
        rmdir %{_libdir}/xbmc %{_datadir}/xbmc
    fi
    ln -s kodi ${RPM_BUILD_ROOT}%{_libdir}/xbmc
    ln -s kodi ${RPM_BUILD_ROOT}%{_datadir}/xbmc
fi


%posttrans devel
if [ ! -L %{_includedir}/xbmc ] ; then
    if [ -d %{_includedir}/xbmc ] ; then
        rmdir %{_includedir}/xbmc
    fi
    ln -s kodi ${RPM_BUILD_ROOT}%{_includedir}/xbmc
fi


%files
%license copying.txt LICENSE.GPL
%doc CONTRIBUTING.md README.md docs
%{_bindir}/kodi
%{_bindir}/kodi-standalone
%{_bindir}/xbmc
%{_bindir}/xbmc-standalone
%{_libdir}/kodi
%ghost %{_libdir}/xbmc
%{_datadir}/kodi
%ghost %{_datadir}/xbmc
%{_datadir}/xsessions/kodi.desktop
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
%{_bindir}/kodi-ps3d
%{_bindir}/kodi-ps3remote
%{_bindir}/kodi-send
%{_bindir}/kodi-wiiremote
%{_mandir}/man1/kodi-ps3remote.1.gz
%{_mandir}/man1/kodi-send.1.gz
%{_mandir}/man1/kodi-standalone.1.gz
%{_mandir}/man1/kodi-wiiremote.1.gz


%files eventclients-devel
%{_includedir}/kodi/xbmcclient.h


%changelog
* Wed Oct 25 2017 Michael Cronenworth <mike@cchtml.com> - 17.5-1
- Kodi 17.5 final

* Wed Aug 23 2017 Michael Cronenworth <mike@cchtml.com> - 17.4-1
- Kodi 17.4 final

* Wed May 31 2017 Michael Cronenworth <mike@cchtml.com> - 17.3-1
- Kodi 17.3 final

* Wed May 24 2017 Michael Cronenworth <mike@cchtml.com> - 17.2-1
- Kodi 17.2 final

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 17.1-2
- Rebuild for ffmpeg update

* Tue Mar 28 2017 Michael Cronenworth <mike@cchtml.com> - 17.1-1
- Kodi 17.1 final

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Michael Cronenworth <mike@cchtml.com> - 17.0-1
- Kodi 17.0 final

* Fri Jan 27 2017 Michael Cronenworth <mike@cchtml.com> - 17.0-0.12.rc4
- Kodi 17 RC4

* Mon Jan 16 2017 Michael Cronenworth <mike@cchtml.com> - 17.0-0.12.rc3
- Kodi 17 RC3
- Check for new installs (RFBZ#4409)
- Drop the XBMC xsession file (RFBZ#4422)

* Wed Jan 04 2017 Michael Cronenworth <mike@cchtml.com> - 17.0-0.11.rc2
- Kodi 17 RC2

* Thu Dec 29 2016 Michael Cronenworth <mike@cchtml.com> - 17.0-0.11.rc1
- Kodi 17 RC1

* Mon Dec 19 2016 Michael Cronenworth <mike@cchtml.com> - 17.0-0.10
- Kodi 17 beta 7

* Sun Dec 11 2016 Michael Cronenworth <mike@cchtml.com> - 17.0-0.9
- Kodi 17 beta 6
- Drop libcec patch, now upstream

* Mon Oct 31 2016 Michael Cronenworth <mike@cchtml.com> - 17.0-0.8
- Kodi 17 beta 5
- Include patch for libcec 4.0 support
- Drop ARM support

* Mon Oct 10 2016 Michael Cronenworth <mike@cchtml.com> - 17.0-0.7
- Kodi 17 beta 3

* Mon Sep 19 2016 Michael Cronenworth <mike@cchtml.com> - 17.0-0.6
- Kodi 17 beta 2

* Fri Aug 26 2016 Michael Cronenworth <mike@cchtml.com> - 17.0-0.5
- Kodi 17 beta 1

* Fri Aug 05 2016 Michael Cronenworth <mike@cchtml.com> - 17.0-0.4
- Kodi 17 alpha 3

* Sun Jul 31 2016 Julian Sikorski <belegdol@fedoraproject.org> - 17.0-0.3
- Rebuilt for ffmpeg-3.1.1
- Fixed the verbose build
- Ensured $RPM_LD_FLAGS are used

* Tue Jul 05 2016 Michael Cronenworth <mike@cchtml.com> - 17.0-0.2
- Kodi 17.0 alpha 2

* Wed Jun 22 2016 Michael Cronenworth <mike@cchtml.com> - 17.0-0.1
- Kodi 17.0 alpha 1

* Mon Apr 25 2016 Michael Cronenworth <mike@cchtml.com> - 16.1-1
- Kodi 16.1 final

* Sat Feb 20 2016 Michael Cronenworth <mike@cchtml.com> - 16.0-1
- Kodi 16.0 final

* Fri Jan 22 2016 Michael Cronenworth <mike@cchtml.com> - 16.0-0.2
- Kodi 16.0 RC1

* Sun Dec 06 2015 Michael Cronenworth <mike@cchtml.com> - 16.0-0.1
- Kodi 16.0 beta 3
- Drop libhdhomerun support (dropped by Kodi)

* Wed Nov 25 2015 Michael Cronenworth <mike@cchtml.com> - 15.2-3
- Enable AirPlay support (shairplay library)

* Sat Oct 24 2015 Michael Cronenworth <mike@cchtml.com> - 15.2-2
- Enable NFS client support

* Thu Oct 22 2015 Michael Cronenworth <mike@cchtml.com> - 15.2-1
- Kodi 15.2 final

* Sun Aug 16 2015 Michael Cronenworth <mike@cchtml.com> - 15.1-1
- Kodi 15.1 final

* Wed Jul 22 2015 Michael Cronenworth <mike@cchtml.com> - 15.0-1
- Kodi 15.0 final

* Tue Jun 16 2015 Michael Cronenworth <mike@cchtml.com> - 15.0-0.1
- Kodi 15.0 beta 2

* Fri May 22 2015 Michael Cronenworth <mike@cchtml.com> - 14.2-2
- GCC5 fixes

* Sun Mar 29 2015 Michael Cronenworth <mike@cchtml.com> - 14.2-1
- Update to 14.2 final
- Build with SDL2 to enable joystick support

* Fri Jan 30 2015 Michael Cronenworth <mike@cchtml.com> - 14.1-1
- Update to 14.1 final
- Fix Obsoletes for -devel

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
