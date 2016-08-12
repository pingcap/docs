#!/bin/bash

set -e 

# Use current path for building and installing TiDB. 
TIDB_PATH=`pwd`
echo "updating and building TiDB components in $TIDB_PATH"

# All the binaries are installed in the `bin` directory. 
mkdir -p $TIDB_PATH/bin

# Assume we install go in /usr/local/go
export PATH=$PATH:/usr/local/go/bin

echo "checking go is installed"
# go is required
go version 
# go version go1.6 darwin/amd64

echo "checking rust is installed"
# rust nightly is required
rustc -V
# rustc 1.12.0-nightly (7ad125c4e 2016-07-11)

# GOPATH should be set correctly.
export GOPATH=$TIDB_PATH/deps/go

# build TiDB
echo "updating and building TiDB..."
cd $GOPATH/src/github.com/pingcap/tidb
git pull

make
cp -f ./bin/tidb-server $TIDB_PATH/bin
cd $TIDB_PATH
echo "build TiDB OK"

# build PD
echo "updating and building PD..."
cd $GOPATH/src/github.com/pingcap/pd

make
cp -f ./bin/pd-server $TIDB_PATH/bin
cp -rf ./templates $TIDB_PATH/bin/templates
cd $TIDB_PATH
echo "build PD OK"

# build TiKV
echo "updating and building TiKV..."
cd $TIDB_PATH/deps/tikv
git pull 

ROCKSDB_SYS_STATIC=1 ROCSDB_SYS_PORTABLE=1 make

cp -f ./bin/tikv-server $TIDB_PATH/bin
cd $TIDB_PATH
echo "build TiKV OK"
