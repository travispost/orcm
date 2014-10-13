#!/bin/bash
set -ex

AUTOCONF="autoconf-2.69"
AUTOCONF_TARBALL="${AUTOCONF}.tar.gz"
AUTOMAKE="automake-1.12.2"
AUTOMAKE_TARBALL="${AUTOMAKE}.tar.gz"
LIBTOOL="libtool-2.4.2"
LIBTOOL_TARBALL="${LIBTOOL}.tar.gz"

PREFIX="/opt/autotools"

wget http://ftp.gnu.org/gnu/autoconf/${AUTOCONF_TARBALL}
tar zxvf ${AUTOCONF_TARBALL}
pushd ${AUTOCONF}
./configure --prefix=${PREFIX}
make
sudo make install
popd

export set PATH="${PREFIX}/bin:${PREFIX}/include:${PREFIX}/lib:${PREFIX}/share:${PATH}"

wget http://ftp.gnu.org/gnu/automake/${AUTOMAKE_TARBALL}
tar zxvf  ${AUTOMAKE_TARBALL}
pushd ${AUTOMAKE}
./configure --prefix=${PREFIX}
make
sudo make install
popd

wget http://ftp.gnu.org/gnu/libtool/${LIBTOOL_TARBALL}
tar zxvf ${LIBTOOL_TARBALL}
pushd ${LIBTOOL}
./configure --prefix=${PREFIX}
make
sudo make install
popd

sudo apt-get install libssl-dev unixodbc-dev unixodbc-bin unixodbc lm-sensors

wget http://downloads.sourceforge.net/project/sigar/sigar/1.6/hyperic-sigar-1.6.4.zip
unzip hyperic-sigar-1.6.4.zip
sudo install hyperic-sigar-1.6.4/sigar-bin/lib/libsigar-amd64-linux.so /lib/x86_64-linux-gnu/libsigar.so
sudo install hyperic-sigar-1.6.4/sigar-bin/include/*.h /usr/include/
sudo /sbin/ldconfig -v /lib/x86_64-linux-gnu
git clone https://github.com/vpedabal/ipmiutil_orcm.git
pushd ipmiutil_orcm
git checkout 6e028f17915bfbe841bd241d5832028a94c8ce78
./beforeconf.sh
./configure --libdir=/usr/lib/x86_64-linux-gnu
make
sudo make install
popd

