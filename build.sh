#!/bin/bash
set -ex

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

