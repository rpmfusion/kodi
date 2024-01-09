#global PRERELEASE rc2
%global DIRVERSION %{version}
#global GITCOMMIT db40b2a
# use the line below for pre-releases
#global DIRVERSION %{version}-%{GITCOMMIT}
#global DIRVERSION %{version}%{PRERELEASE}
%global _hardened_build 1
%ifarch %{arm} %{arm64}
# Disable LTO for arm, see http://koji.rpmfusion.org/koji/taskinfo?taskID=424139
%global _lto_cflags %{nil}
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

# Needed for F36 build issue
%undefine _package_note_file

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
%global _with_cwiid 0
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
Version: 20.2
Release: 7%{?dist}
Summary: Media center

License: GPLv2+ and GPLv3+ and LGPLv2+ and BSD and MIT
# Main binary and all supporting files are GPLv2+/GPLv3+
# Some supporting libraries use the LGPL / BSD / MIT license
Group: Applications/Multimedia
URL: https://www.kodi.tv/
Source0: %{name}-%{DIRVERSION}-patched.tar.xz
# kodi contains code that we cannot ship, as well as redundant private
# copies of upstream libraries that we already distribute.  Therefore
# we use this script to remove the code before shipping it.
# Invoke this script while in the directory where the tarball is located:
# ./kodi-generate-tarball-xz.sh
Source1: kodi-generate-tarball-xz.sh

# kodi uses modified libdvd{css,nav,read} source and downloads at build time
# wget -O kodi-libdvdnav-6.1.1-Next-Nexus-Alpha2-2.tar.gz https://github.com/xbmc/libdvdnav/archive/6.1.1-Next-Nexus-Alpha2-2.tar.gz
Source2: kodi-libdvdnav-6.1.1-Next-Nexus-Alpha2-2.tar.gz
# wget -O kodi-libdvdread-6.1.3-Next-Nexus-Alpha2-2.tar.gz https://github.com/xbmc/libdvdread/archive/6.1.3-Next-Nexus-Alpha2-2.tar.gz
Source3: kodi-libdvdread-6.1.3-Next-Nexus-Alpha2-2.tar.gz
%if %{with dvdcss}
# wget -O kodi-libdvdcss-1.4.3-Next-Nexus-Alpha2-2.tar.gz https://github.com/xbmc/libdvdcss/archive/1.4.3-Next-Nexus-Alpha2-2.tar.gz
Source4: kodi-libdvdcss-1.4.3-Next-Nexus-Alpha2-2.tar.gz
%endif

%if ! 0%{?_with_external_ffmpeg}
# wget -O ffmpeg-5.1.2-Nexus-Alpha3.tar.gz https://github.com/xbmc/FFmpeg/archive/5.1.2-Nexus-Alpha3.tar.gz
Source5: ffmpeg-5.1.2-Nexus-Alpha3.tar.gz
%endif

# Set program version parameters
Patch1: kodi-20-versioning.patch

# Fix an annobin issue, required for ARM arch
Patch2: kodi-20-annobin-workaround.patch

Patch3: https://github.com/xbmc/xbmc/pull/23453.patch#/fmt10_buildfix.patch

# Add initializer for tp_watched
Patch4: https://github.com/xbmc/xbmc/commit/2c84ee54a75770e291f38d4ebb2c31c8f2c3b8c5.patch#/tp_watched_initializer.patch
# Python 3.12 support
Patch5: https://github.com/xbmc/xbmc/commit/4bf9de87e700f0de56ef698a8d8d6eb7d4ff9050.patch#/kodi-20-python-312.patch

%ifarch x86_64
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
BuildRequires: firewalld-filesystem
%if 0%{?_with_external_ffmpeg}
BuildRequires: compat-ffmpeg4-devel
%else
BuildRequires: trousers-devel
%endif
BuildRequires: flac-devel
BuildRequires: flatbuffers-compiler
BuildRequires: flatbuffers-devel
BuildRequires: flex
BuildRequires: fmt-devel
BuildRequires: fontconfig-devel
BuildRequires: fontpackages-devel
BuildRequires: freetype-devel
BuildRequires: fribidi-devel
BuildRequires: fstrcmp-devel
BuildRequires: gettext-autopoint
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
BuildRequires: libcec-devel >= 4.0.0
%endif
%if 0%{?_with_crystalhd}
BuildRequires: libcrystalhd-devel
%endif
BuildRequires: libcurl-devel
BuildRequires: libdav1d-devel
BuildRequires: libdca-devel
BuildRequires: libdrm-devel
BuildRequires: libidn2-devel
BuildRequires: libinput-devel
BuildRequires: libjpeg-turbo-devel
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
BuildRequires: mariadb-connector-c-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: nasm
BuildRequires: ninja-build
BuildRequires: pcre-devel
BuildRequires: pixman-devel
BuildRequires: pipewire-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: python3-devel
BuildRequires: python3-pillow
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

Requires: (%{name}-firewalld = %{version}-%{release} if firewalld)
Requires: dejavu-sans-fonts
# need explicit requires for these packages
# as they are dynamically loaded via XBMC's arcane
# pseudo-DLL loading scheme (sigh)
%if 0%{?_with_libbluray}
Requires: libbluray%{?_isa}
%endif
%if 0%{?_with_libcec}
Requires: libcec%{?_isa} >= 4.0.0
%endif
%if 0%{?_with_crystalhd}
Requires: libcrystalhd%{?_isa}
%endif
Requires: libmad%{?_isa}
Requires: librtmp%{?_isa}
Requires: shairplay-libs%{?_isa}

# This is just symlinked to, but needed both at build-time
# and for installation
Requires: python3-pillow%{?_isa}

# https://github.com/xbmc/xbmc/pull/18534
Provides: kodi-common = %{version}-%{release}
Obsoletes: kodi-common < %{version}-%{release}
Provides: kodi-gbm = %{version}-%{release}
Obsoletes: kodi-gbm < %{version}-%{release}
Provides: kodi-wayland = %{version}-%{release}
Obsoletes: kodi-wayland < %{version}-%{release}
Provides: kodi-x11 = %{version}-%{release}
Obsoletes: kodi-x11 < %{version}-%{release}


%description
Kodi is a free cross-platform media-player jukebox and entertainment hub.
Kodi can play a spectrum of of multimedia formats, and featuring playlist,
audio visualizations, slideshow, and weather forecast functions, together
third-party plugins.


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


%prep
%setup -q -n %{name}-%{DIRVERSION}
%patch -P 1 -p1 -b.versioning
%patch -P 2 -p1 -b.innobinfix
%if 0%{?fedora} && 0%{?fedora} > 38
%patch -P 3 -p1 -b.fmt
%patch -P 4 -p1 -b.initializer
%patch -P 5 -p1 -b.python-312
%endif

# Fix up Python shebangs
%py3_shebang_fix \
  tools/EventClients/lib/python/zeroconf.py \
  tools/EventClients/Clients/PS3BDRemote/ps3_remote.py \
  tools/EventClients/lib/python/ps3/sixaxis.py \
  tools/EventClients/lib/python/ps3/sixpair.py \
  tools/EventClients/lib/python/ps3/sixwatch.py \
  tools/EventClients/Clients/KodiSend/kodi-send.py \
  tools/EventClients/lib/python/xbmcclient.py

%build
export PKG_CONFIG_PATH="%{_libdir}/compat-ffmpeg4/pkgconfig"
%cmake \
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
  -DCORE_PLATFORM_NAME="%{kodi_backends}" \
  -DAPP_RENDER_SYSTEM=gl \
  -DENABLE_INTERNAL_RapidJSON=OFF

%cmake_build


%install
%cmake_install

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
%license LICENSE.md LICENSES/
%doc README.md docs
%{_bindir}/kodi
%{_bindir}/kodi-standalone
%{_bindir}/JsonSchemaBuilder
%{_bindir}/kodi-TexturePacker
%{_libdir}/kodi/
%{_datadir}/kodi/
%{_datadir}/xsessions/kodi.desktop
%{_datadir}/applications/kodi.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/metainfo/org.xbmc.kodi.metainfo.xml
%{_mandir}/man1/kodi.1.gz
%{_mandir}/man1/kodi.bin.1.gz
%{_mandir}/man1/kodi-standalone.1.gz
%{_mandir}/man1/kodi-TexturePacker.1.gz


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


%changelog
* Fri Nov 10 2023 Michael Cronenworth <mike@cchtml.com> - 20.2-7
- Another upstream python-3.12 fix (RFBZ#6783)

* Tue Oct 31 2023 Leigh Scott <leigh123linux@gmail.com> - 20.2-6
- Use upstream python-3.12 fix

* Thu Sep 28 2023 Michael Cronenworth <mike@cchtml.com> - 20.2-5
- Update mariadb BR (RFBZ#6771)

* Fri Aug 11 2023 Leigh Scott <leigh123linux@gmail.com> - 20.2-4
- Rebuild for new libplist

* Wed Aug 02 2023 Sérgio Basto <sergio@serjux.com> - 20.2-3
- Rebuild for spdlog soname bump

* Sat Jul 08 2023 Leigh Scott <leigh123linux@gmail.com> - 20.2-2
- Rebuilt for Python 3.12

* Thu Jun 29 2023 Michael Cronenworth <mike@cchtml.com> - 20.2-1
- Kodi 20.2 Final

* Wed Mar 15 2023 Michael Cronenworth <mike@cchtml.com> - 20.1-1
- Kodi 20.1 Final

* Mon Jan 16 2023 Michael Cronenworth <mike@cchtml.com> - 20.0-1
- Kodi 20.0 Final

* Fri Jan 13 2023 Michael Cronenworth <mike@cchtml.com> - 20.0-0.rc2.0
- Kodi 20.0 RC2

* Sat Dec 24 2022 Leigh Scott <leigh123linux@gmail.com> - 19.5-1
- Kodi 19.5 Final

* Sun Aug 07 2022 Leigh Scott <leigh123linux@gmail.com> - 19.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Sat Jun 25 2022 Robert-André Mauchin <zebob.m@gmail.com> - 19.4-3
- Rebuilt for Python 3.11

* Thu Jun 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 19.4-2
- Rebuilt for new dav1d

* Tue Mar 08 2022 Michael Cronenworth <mike@cchtml.com> - 19.4-1
- Kodi 19.4 Final

* Sun Feb 20 2022 Michael Cronenworth <mike@cchtml.com> - 19.3-3
- Patch for AC3 transcoding (RHBZ#6000)

* Sat Feb 19 2022 Leigh Scott <leigh123linux@gmail.com> - 19.3-2
- Switch to compat-ffmpeg4
- Disable package note

* Wed Oct 27 2021 Michael Cronenworth <mike@cchtml.com> - 19.3-1
- Kodi 19.3 Final

* Sat Oct 09 2021 Michael Cronenworth <mike@cchtml.com> - 19.2-1
- Kodi 19.2 Final

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 19.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 11 2021 Leigh Scott <leigh123linux@gmail.com> - 19.1-4
- Rebuild for new fmt version

* Tue Jun 15 2021 Leigh Scott <leigh123linux@gmail.com> - 19.1-3
- Rebuild for python-3.10

* Thu Jun 03 2021 Michael Cronenworth <mike@cchtml.com> - 19.1-2
- FFmpeg 4.4 support

* Mon May 10 2021 Michael Cronenworth <mike@cchtml.com> - 19.1-1
- Kodi 19.1 Final

* Fri Apr 23 2021 Michael Cronenworth <mike@cchtml.com> - 19.0-3
- Drop old dependencies

* Thu Apr 22 2021 Michael Cronenworth <mike@cchtml.com> - 19.0-2
- Update dependency on xdpyinfo (rfbz#5979)

* Sat Feb 20 2021 Michael Cronenworth <mike@cchtml.com> - 19.0-1
- Kodi 19.0 Final

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 19.0-0.10.20210115git90a1e12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Michael Cronenworth <mike@cchtml.com> - 19.0-0.9.20210115git90a1e12
- Kodi 19.0 RC1

* Mon Dec 07 2020 Michael Cronenworth <mike@cchtml.com> - 19.0-0.8.20201207git8cc9e80
- Kodi 19.0 beta 2

* Fri Nov 20 2020 Michael Cronenworth <mike@cchtml.com> - 19.0-0.7.20201119gitc08d72a
- Kodi 19.0 beta 1

* Mon Nov 02 2020 Michael Cronenworth <mike@cchtml.com> - 19.0-0.6.20201031gitbb0699d
- Kodi 19.0 alpha 3

* Thu Oct 29 2020 Michael Cronenworth <mike@cchtml.com> - 19.0-0.5.20201005git54be31b
- Python 3.9 support

* Tue Oct 27 2020 Michael Cronenworth <mike@cchtml.com> - 19.0-0.4.20201005git54be31b
- Kodi 19.0 alpha 2

* Sun Sep 13 2020 Nicolas Chauvet <kwizart@gmail.com> - 19.0-0.3.20200727gitdb40b2a
- rebuilt

* Tue Aug 25 2020 Nicolas Chauvet <kwizart@gmail.com> - 19.0-0.2.20200727gitdb40b2a
- Update release tag
- Revert java change to workaround glibc issue
- Use gl by default on all arches

* Sat Aug 08 2020 Michael Cronenworth <mike@cchtml.com> - 19.0-0.20200727gitdb40b2a
- Kodi 19.0 alpha 1

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
