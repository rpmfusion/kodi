#global PRERELEASE rc5
#global DIRVERSION %{version}
%global GITCOMMIT b6daed5
# use the line below for pre-releases
%global DIRVERSION %{version}-%{GITCOMMIT}
#global DIRVERSION %{version}%{PRERELEASE}
%global _hardened_build 1
%ifarch %{arm}
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

# We support hte following options:
# --with,
# * dvdcss - Include DVD decryption support
#
# Default: Do not ship DVD decryption for legal reasons
%bcond_with dvdcss

# Optional deps (not in EPEL)
%if 0%{?fedora}
# (libbluray in EPEL 6 is too old.)
%global _with_libbluray 1
%if 0%{?fedora} < 31
%global _with_cwiid 1
%else
%global _with_cwiid 0
%endif
%global _with_libssh 1
%global _with_libcec 1
%global _with_external_ffmpeg 1
%global _with_wayland 1
%endif
%if 0%{?_with_wayland}
%global kodi_backends x11 wayland gbm
%else
%global kodi_backends x11 gbm
%endif

Name: kodi
Version: 19.0
Release: 0.20200706gitb6daed5%{?dist}
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

# kodi uses modified libdvd{css,nav,read} source and downloads at build time
# wget -O kodi-libdvdnav-6.0.0-Leia-Alpha-3.tar.gz https://github.com/xbmc/libdvdnav/archive/6.0.0-Leia-Alpha-3.tar.gz
Source2: kodi-libdvdnav-6.0.0-Leia-Alpha-3.tar.gz
# wget -O kodi-libdvdread-6.0.0-Leia-Alpha-3.tar.gz https://github.com/xbmc/libdvdread/archive/6.0.0-Leia-Alpha-3.tar.gz
Source3: kodi-libdvdread-6.0.0-Leia-Alpha-3.tar.gz
%if %{with dvdcss}
# wget -O kodi-libdvdcss-1.4.2-Leia-Beta-5.tar.gz https://github.com/xbmc/libdvdcss/archive/1.4.2-Leia-Beta-5.tar.gz
Source4: kodi-libdvdcss-1.4.2-Leia-Beta-5.tar.gz
%endif

%if ! 0%{?_with_external_ffmpeg}
# wget -O ffmpeg-4.3-Matrix-Alpha1.tar.gz https://github.com/xbmc/FFmpeg/archive/4.3-Matrix-Alpha1.tar.gz
Source5: ffmpeg-4.3-Matrix-Alpha1.tar.gz
%endif

# Set program version parameters
Patch1: kodi-19-versioning.patch

# Prevent trousers from being linked, which breaks Samba
Patch2: kodi-18-trousers.patch

# Fix an annobin issue
Patch3: kodi-18-annobin-workaround.patch

# Workaround for brp-mangle-shebangs behavior (RHBZ#1787088)
Patch4: kodi-18-brp-mangle-shebangs.patch

# GCC/libmicrohttpd casting fix
Patch5: kodi-19-webserver.patch
Patch6: kodi-19-httprequesthandler.patch

# Python 3.9 fix
Patch7: kodi-19-python.patch

%ifarch x86_64 i686
%global _with_crystalhd 1
%endif

# Upstream does not support ppc64
ExcludeArch: %{power64}

BuildRequires: a52dec-devel
BuildRequires: afpfs-ng-devel
BuildRequires: alsa-lib-devel
BuildRequires: avahi-devel
BuildRequires: bluez-libs-devel
BuildRequires: boost-devel
BuildRequires: bzip2-devel
BuildRequires: cmake3
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
BuildRequires: firewalld-filesystem
%if 0%{?_with_external_ffmpeg}
BuildRequires: ffmpeg-devel
%else
BuildRequires: trousers-devel
%endif
BuildRequires: flac-devel
BuildRequires: flatbuffers-devel
BuildRequires: flex
BuildRequires: fmt-devel
BuildRequires: fontconfig-devel
BuildRequires: fontpackages-devel
BuildRequires: freetype-devel
BuildRequires: fribidi-devel
BuildRequires: fstrcmp-devel
%if 0%{?el6}
BuildRequires: gettext-devel
%else
BuildRequires: gettext-autopoint
%endif
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: giflib-devel
BuildRequires: glew-devel
BuildRequires: glib2-devel
BuildRequires: gperf
BuildRequires: gtest-devel
BuildRequires: jasper-devel
BuildRequires: java-devel
BuildRequires: lame-devel
BuildRequires: lcms2-devel
BuildRequires: libXinerama-devel
BuildRequires: libXmu-devel
BuildRequires: libXrandr-devel
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
BuildRequires: libdrm-devel
BuildRequires: libidn2-devel
BuildRequires: libinput-devel
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
BuildRequires: libunistring-devel
BuildRequires: libuuid-devel
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
BuildRequires: libvorbis-devel
%if 0%{?_with_wayland}
BuildRequires: libxkbcommon-devel
%endif
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: lirc-devel
BuildRequires: lzo-devel
BuildRequires: mariadb-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: nasm
BuildRequires: ninja-build
BuildRequires: pcre-devel
BuildRequires: pixman-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: python3-devel
BuildRequires: python3-pillow
BuildRequires: /usr/bin/pathfix.py
BuildRequires: rapidjson-devel
BuildRequires: spdlog-devel
BuildRequires: sqlite-devel
BuildRequires: swig
BuildRequires: systemd-devel
BuildRequires: taglib-devel >= 1.10
BuildRequires: tinyxml-devel
BuildRequires: tre-devel
BuildRequires: wavpack-devel
%if 0%{?_with_wayland}
BuildRequires: wayland-protocols-devel
BuildRequires: waylandpp-devel
%endif
BuildRequires: yajl-devel
BuildRequires: zlib-devel

# Install major backends, users can remove them individually
Requires: %{name}-common = %{version}-%{release}
Requires: (%{name}-wayland = %{version}-%{release} if libwayland-server)
Requires: (%{name}-x11 = %{version}-%{release} if xorg-x11-server-Xorg)
Requires: (%{name}-firewalld = %{version}-%{release} if firewalld)


%description
Kodi is a free cross-platform media-player jukebox and entertainment hub.
Kodi can play a spectrum of of multimedia formats, and featuring playlist,
audio visualizations, slideshow, and weather forecast functions, together
third-party plugins.

This is a meta package.


%package common
Summary: Common Kodi files and binaries
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
Requires: python3-pillow%{?_isa}

%description common
Common Kodi files and binaries


%package devel
Summary: Development files needed to compile C programs against kodi
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


%package firewalld
Summary: FirewallD metadata files for Kodi
Requires: firewalld-filesystem
Requires(post): firewalld-filesystem

%description firewalld
This package contains FirewallD files for Kodi.


%package gbm
Summary: Kodi binary for Generic Buffer Management
Requires: %{name}-common = %{version}-%{release}


%description gbm
This package contains the Kodi binary for Generic Buffer Management.


%package wayland
Summary: Kodi binary for Wayland compositors
Requires: %{name}-common = %{version}-%{release}


%description wayland
This package contains the Kodi binary for Wayland compositors.


%package x11
Summary: Kodi binary for X11 servers
Requires: %{name}-common = %{version}-%{release}


%description x11
This package contains the Kodi binary for X11 servers.


%prep
%setup -q -n %{name}-%{DIRVERSION}
%patch1 -p1 -b.versioning
%patch2 -p1 -b.trousers
%patch3 -p1 -b.innobinfix
%patch4 -p1 -b.brp-mangle-shebangs
%patch5 -p1 -b.webserver
%patch6 -p1 -b.httprequesthandler
%patch7 -p1 -b.python

# Fix up Python shebangs
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" \
  tools/EventClients/lib/python/zeroconf.py \
  tools/EventClients/Clients/PS3BDRemote/ps3_remote.py \
  tools/EventClients/lib/python/ps3/sixaxis.py \
  tools/EventClients/lib/python/ps3/sixpair.py \
  tools/EventClients/lib/python/ps3/sixwatch.py \
  tools/EventClients/Clients/KodiSend/kodi-send.py \
  tools/EventClients/lib/python/xbmcclient.py

%if 0%{?fedora} < 32
# Fix python binary search
sed -i 's/  pkg_check_modules(PC_PYTHON python>=2.7 QUIET)/  pkg_check_modules(PC_PYTHON python=2.7 QUIET)/' cmake/modules/FindPython.cmake
%endif


%build
mkdir {fedora-gbm,fedora-wayland,fedora-x11}

for BACKEND in %{kodi_backends}
do
    pushd fedora-$BACKEND
%cmake3 \
%if %{with dvdcss}
  -DLIBDVDCSS_URL=%{SOURCE4} \
%else
  -DENABLE_DVDCSS=OFF \
%endif
%if ! 0%{?_with_external_ffmpeg}
  -DFFMPEG_URL=%{SOURCE5} \
%endif
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_C_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG" \
  -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG" \
  -DCMAKE_ASM_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG" \
  -DENABLE_DEBUGFISSION=OFF \
  -GNinja \
  -DENABLE_EVENTCLIENTS=ON \
  -DENABLE_INTERNAL_CROSSGUID=OFF \
  -DLIRC_DEVICE=/var/run/lirc/lircd \
  -DLIBDVDNAV_URL=%{SOURCE2} \
  -DLIBDVDREAD_URL=%{SOURCE3} \
  -DPYTHON_EXECUTABLE=%{__python3} \
  -DCORE_PLATFORM_NAME=$BACKEND \
%ifarch x86_64 i686
  -DX11_RENDER_SYSTEM=gl \
  -DWAYLAND_RENDER_SYSTEM=gl \
  -DGBM_RENDER_SYSTEM=gl \
%else
  -DX11_RENDER_SYSTEM=gles \
  -DWAYLAND_RENDER_SYSTEM=gles \
  -DGBM_RENDER_SYSTEM=gles \
%endif
  ../
    %ninja_build
    popd
done


%install
for BACKEND in %{kodi_backends}
do
    pushd fedora-$BACKEND
    %ninja_install
    popd
done

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
ln -s %{python3_sitearch}/PIL $RPM_BUILD_ROOT%{_libdir}/kodi/addons/script.module.pil/lib/PIL
#install -d $RPM_BUILD_ROOT%{_libdir}/xbmc/addons/script.module.pysqlite/lib

# Use external font files instead of bundled ones
ln -sf %{_fontbasedir}/dejavu/DejaVuSans-Bold.ttf ${RPM_BUILD_ROOT}%{_datadir}/kodi/addons/skin.estouchy/fonts/

# Move man-pages into system dir
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/
mv docs/manpages ${RPM_BUILD_ROOT}%{_mandir}/man1/

# Remove wiiremote man page if support was disabled
%if ! 0%{?_with_cwiid}
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/kodi-wiiremote.1
%endif


%post firewalld
%firewalld_reload


%files


%files common
%license LICENSE.md LICENSES/
%doc README.md docs
%{_bindir}/kodi
%{_bindir}/kodi-standalone
%{_bindir}/JsonSchemaBuilder
%{_bindir}/TexturePacker
%dir %{_libdir}/kodi/
%{_libdir}/kodi/addons/
%{_libdir}/kodi/system/
%{_datadir}/kodi/
%{_datadir}/xsessions/kodi.desktop
%{_datadir}/applications/kodi.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_mandir}/man1/kodi.1.gz
%{_mandir}/man1/kodi.bin.1.gz
%{_mandir}/man1/kodi-standalone.1.gz


%files devel
%{_includedir}/kodi


%files eventclients
%license LICENSE.md LICENSES/
%{python3_sitelib}/kodi
%dir %{_datadir}/pixmaps/kodi
%{_datadir}/pixmaps/kodi/*.png
%{_bindir}/kodi-ps3remote
%{_bindir}/kodi-send
%if 0%{?_with_cwiid}
%{_bindir}/kodi-wiiremote
%endif
%{_mandir}/man1/kodi-ps3remote.1.gz
%{_mandir}/man1/kodi-send.1.gz
%if 0%{?_with_cwiid}
%{_mandir}/man1/kodi-wiiremote.1.gz
%endif


%files eventclients-devel
%{_includedir}/kodi/xbmcclient.h


%files firewalld
%license LICENSE.md LICENSES/
%{_prefix}/lib/firewalld/services/kodi-eventserver.xml
%{_prefix}/lib/firewalld/services/kodi-http.xml
%{_prefix}/lib/firewalld/services/kodi-jsonrpc.xml


%files gbm
%{_libdir}/kodi/kodi-gbm


%files wayland
%{_libdir}/kodi/kodi-wayland


%files x11
%{_libdir}/kodi/kodi-x11
%{_libdir}/kodi/kodi-xrandr


%changelog
* Sun Aug 02 2020 Leigh Scott <leigh123linux@gmail.com> - 19.0-0.20200706gitb6daed5
- Rebuild for libfmt

* Mon Jul 06 2020 Michael Cronenworth <mike@cchtml.com> - 19.0-0.20200705gitb6daed5
- Initial version 19 snapshot

* Sun Apr 26 2020 Michael Cronenworth <mike@cchtml.com> - 18.6-3
- Python 3 and libfmt fixes

* Fri Apr 10 2020 Leigh Scott <leigh123linux@gmail.com> - 18.6-2
- Rebuild for new libcdio version

* Wed Mar 04 2020 Michael Cronenworth <mike@cchtml.com> - 18.6-1
- Kodi 18.6 final

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 18.5-3
- Rebuild for ffmpeg-4.3 git

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 18.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 22 2019 Michael Cronenworth <mike@cchtml.com> - 18.5-1
- Kodi 18.5 final

* Wed Sep 11 2019 Leigh Scott <leigh123linux@googlemail.com> - 18.4-2
- Rebuild for new libnfs version

* Mon Sep 02 2019 Michael Cronenworth <mike@cchtml.com> - 18.4-1
- Kodi 18.4 final

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 18.3-2
- Rebuild for new ffmpeg version

* Sat Jun 29 2019 Michael Cronenworth <mike@cchtml.com> - 18.3-1
- Kodi 18.3 final

* Wed May 08 2019 Leigh Scott <leigh123linux@gmail.com> - 18.2-4
- Bump release for koji failed task

* Mon May 06 2019 Michael Cronenworth <mike@cchtml.com> - 18.2-3
- Release build with debugging symbols

* Sun May 05 2019 Michael Cronenworth <mike@cchtml.com> - 18.2-2
- Build with debugging symbols (rfbz#5248)

* Tue Apr 23 2019 Michael Cronenworth <mike@cchtml.com> - 18.2-1
- Kodi 18.2 final

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Feb 26 2019 Nicolas Chauvet <kwizart@gmail.com> - 18.1-2
- Apply patch by Gaël Stephan to fix kodi on aarch64 - rfbz#5171

* Tue Feb 19 2019 Michael Cronenworth <mike@cchtml.com> - 18.1-1
- Kodi 18.1 final

* Tue Jan 29 2019 Leigh Scott <leigh123linux@googlemail.com> - 18.0-1
- Kodi 18.0 final

* Sat Jan 12 2019 Leigh Scott <leigh123linux@googlemail.com> - 18.0-0.24.rc5
- Kodi 18.0 RC5

* Sun Dec 30 2018 Leigh Scott <leigh123linux@googlemail.com> - 18.0-0.23.rc4
- Kodi 18.0 RC4

* Tue Dec 25 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.22.rc3
- Add upstream patches to fix a few crashers

* Sun Dec 16 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.21.rc3
- Kodi 18.0 RC3

* Thu Dec 06 2018 Nicolas Chauvet <kwizart@gmail.com> - 18.0-0.20.rc2
- Rebuilt for fmt

* Mon Dec 03 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.19.rc2
- Kodi 18.0 RC2

* Fri Nov 23 2018 Leigh Scott <leigh123linux@googlemail.com> - 18.0-0.18.rc1
- Kodi 18.0 RC1

* Mon Nov 19 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.17.b5
- Add patch to fix video calibration

* Sun Nov 04 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.16.b5
- Kodi 18.0 beta 5

* Sat Nov 03 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.15.b4
- Add patch to fix SMB browsing (RFBZ#5001)

* Fri Oct 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 18.0-0.14.b4
- Switch to ninja-build

* Fri Oct 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 18.0-0.13.b4
- Rebuild for fmt-5.2.1

* Wed Oct 24 2018 Nicolas Chauvet <kwizart@gmail.com> - 18.0-0.12.b4
- Update to beta4
- Fixup versioning

* Sat Oct 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 18.0-0.11.b3
- Add BuildRequires lirc-devel (rfbz#5037)

* Thu Oct 11 2018 Nicolas Chauvet <kwizart@gmail.com> - 18.0-0.10.b3
- Update to beta3
- Enable arm build
- Build EGL/GLES everywhere
- Add firewalld sub-package when relevant

* Thu Sep 27 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.9.b2
- Kodi 18.0 beta 2

* Fri Aug 31 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.8.b1
- Fix Requires and versioning in new split packages

* Thu Aug 30 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.7.b1
- Update Requires for new split packages

* Tue Aug 28 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.6.b1
- Build wayland and GBM binaries

* Tue Aug 28 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.5.b1
- Kodi 18.0 beta 1 v2

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 18.0-0.4.a2
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 18.0-0.3.a2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 24 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.2.a2
- Kodi 18.0 alpha 2

* Thu May 03 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.1.a1
- Add patch to fix assert on start.

* Fri Mar 16 2018 Michael Cronenworth <mike@cchtml.com> - 18.0-0.0.a1
- Kodi 18.0 alpha 1

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 17.6-7
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 17.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Feb 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 17.6-5
- Rebuild for boost-1.66

* Wed Jan 24 2018 Michael Cronenworth <mike@cchtml.com> - 17.6-4
- ffmpeg-3.5 support
- Make dvd support an rpm build conditional

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 17.6-3
- Rebuilt for ffmpeg-3.5 git

* Mon Jan 15 2018 Nicolas Chauvet <kwizart@gmail.com> - 17.6-2
- Rebuilt for VA-API 1.0.0

* Fri Nov 17 2017 Michael Cronenworth <mike@cchtml.com> - 17.6-1
- Kodi 17.6 final

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
