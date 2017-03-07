# Build For Development

## Overview

If you want to develop the TiDB project, you can follow this guide.

Before you begin, check the [supported platforms](./requirements.md#supported-platforms) and [prerequisites](./requirements.md#prerequisites) first.

## Install RocksDB

RocksDB 5.1 is required, You can install the RocksDB shared library manually according to [INSTALL.md](https://github.com/facebook/rocksdb/blob/master/INSTALL.md) or use the [build RocksDB script](../scripts/build_rocksdb.sh) to build and install RocksDB in the system path.

## Build TiKV

After you install the RocksDB shared library, you can build TiKV directly without `ROCKSDB_SYS_STATIC`.

+ Get the TiKV source code.

    ```bash
    git clone https://github.com/pingcap/tikv.git 
    ```
+ Enter the source directory to build and install the binary in the `bin` directory.

    ```bash
    make
    ```
    
+ Run unit test.
    
    ```bash
    make test
    ```

## Build TiDB

+ Make sure the GOPATH environment is set correctly.

+ Get the TiDB source code.

    ```bash
    git clone https://github.com/pingcap/tidb.git $GOPATH/src/github.com/pingcap/tidb
    ```
    
+ Enter `$GOPATH/src/github.com/pingcap/tidb` to build and install the binary in the `bin` directory.

    ```bash
    make
    ```
+ Run unit test.
    
    ```bash
    make test
    ```

## Build PD

+ Get the PD source code.

    ```bash
    git clone https://github.com/pingcap/pd.git $GOPATH/src/github.com/pingcap/pd
    ```
    
+ Enter `$GOPATH/src/github.com/pingcap/pd` to build and install the binary in the `bin` directory.

    ```bash
    make
    ```
+ Run unit test.
    
    ```bash
    make test
    ```
