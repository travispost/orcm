#!/bin/bash
set -ex

./autogen.pl
mkdir build
pushd build
export LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
../configure --with-platform=../contrib/platform/intel/hillsboro/orcm-nightly-build --SIGAR=/usr/local/lib
make
make install
#popd
#mkdir static
#pushd static
#../configure --with-platform=../contrib/platform/intel/hillsboro/orcm-nightly-build-static
#make
#popd

