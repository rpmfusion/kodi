#!/bin/sh

MAJORVERSION=17
MINORVERSION=0b2
#GITCOMMIT=e988513175fccca83f8b688bb77b932f6a403b96
#GITSHORT=ge988513
CODENAME=Krypton

VERSION=${MAJORVERSION}.${MINORVERSION}${GITSHORT:+-${GITSHORT}}

GITHUBURL=https://github.com/xbmc/xbmc/zipball/$VERSION-$CODENAME
#GITHUBURL=https://github.com/xbmc/xbmc/zipball/$GITCOMMIT

# download zipball
if [[ ! -f xbmc-$VERSION.zip ]]; then
    curl -o xbmc-$VERSION.zip -L $GITHUBURL
fi

# extract zipball
rm -rf xbmc-xbmc-*
unzip xbmc-$VERSION.zip

# Repair GitHub's odd auto-generated top-level directory...
mv xbmc-xbmc-* kodi-$VERSION

pushd kodi-$VERSION

# remove bundled libraries, saves space and forces using external versions
# grrr, *still* have to keep in ffmpeg for now (2011-12-28) since upstream
# seems to require files within that subdirectory <sigh>, filed
# http://trac.xbmc.org/ticket/12370
for i in  cximage-6.0/zlib libhdhomerun libmpeg2 ffmpeg
do
    rm -r lib/$i
done

# remove more bundled codecs
for i in libmpeg2
do
    rm -r kodi/cores/dvdplayer/DVDCodecs/Video/$i
done


# remove DVD stuff we can't ship, or is already in external libraries
for i in libdvdcss libdvdread includes
do
    rm -r lib/libdvd/$i
done

# remove all prebuilt binaries (e.g., Win32 DLLs)
find \( -type f -name '*.DLL' -o -name '*.dll' -o -name '*.lib' -o -name '*.obj' -o -name '*.exe' \) -print0 | xargs -0 rm -f

# remove all other packages that should be system-wide
# except for libass, cpluff (need to figure out how to
# remove these too)
# xbmc-dll-symbols seems to be XBMC-specific
for i in enca freetype libbluray libmicrohttpd libmodplug librtmp win32
do
    rm -r lib/$i
done

# TODO/FIXME: remove other unnecessary things under tools/
# also remove anything to do with win32
for i in win32buildtools
do
    rm -r tools/$i
done

popd

# repack
tar -cJvf kodi-$VERSION-patched.tar.xz kodi-$VERSION
