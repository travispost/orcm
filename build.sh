#!/bin/bash
set -ex

./autogen.pl
mkdir build
pushd build
export LD_LIBRARY_PATH=/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}
../configure --with-platform=../contrib/platform/intel/hillsboro/orcm-nightly-build
make
make install
#popd
#mkdir static
#pushd static
#../configure --with-platform=../contrib/platform/intel/hillsboro/orcm-nightly-build-static
#make
#popd

