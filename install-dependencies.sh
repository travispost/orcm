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

if [[  `apt-get --version` ]] ; then
    sudo apt-get install libssl-dev unixodbc-dev unixodbc-bin unixodbc \
    lm-sensors
elif [[ `zypper --version` ]] ; then
    sudo zypper in libopenssl-devel sensors unixODBC unixODBC-devel
else
    sudo yum install openssl-devel lm_sensors sigar sigar-devel unixODBC \
    unixODBC-devel
fi

if [[ ! `yum --version` ]] ; then
    git clone https://github.com/hyperic/sigar.git
    pushd sigar
    git checkout b89060c48120d14feb2b5d8acd5612cb36db40a2
    ./autogen.sh
    ./configure
    make
    sudo make install
    popd
fi

git clone https://github.com/vpedabal/ipmiutil_orcm.git
pushd ipmiutil_orcm
git checkout 6e028f17915bfbe841bd241d5832028a94c8ce78
./beforeconf.sh
if [[ ! `yum --version ` ]] ; then
    ./configure --libdir=/usr/lib/x86_64-linux-gnu
else
    ./configure
fi
make
sudo make install
popd

