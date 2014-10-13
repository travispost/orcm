#!/bin/bash
set -ex

dpkg-query -L libhyperic-sigar-java
./autogen.pl
mkdir build
pushd build
../configure --with-platform=../contrib/platform/intel/hillsboro/orcm-nightly-build
make
make install
#popd
#mkdir static
#pushd static
#../configure --with-platform=../contrib/platform/intel/hillsboro/orcm-nightly-build-static
#make
#popd

