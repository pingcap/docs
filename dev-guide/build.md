# Build

## Overview

You can follow this guide to build the TiDB project.

Before your begin, check the [supported platforms](../op-guide/build.md#supported-platforms) and [prerequisites](../op-guide/build.md#prerequisites) first.

## Install RocksDB

RocksDB 4.9+ is required, You can install the RocksDB shared library manually according to [INSTALL.md](https://github.com/facebook/rocksdb/blob/master/INSTALL.md) or use the [build RocksDB script](../scripts/build_rocksdb.sh) to build and install RocksDB in the system path.

## Build TiKV

After you install the RocksDB shared library, you can build TiKV directly without `ROCKSDB_SYS_STATIC`.

```bash
# cd TiKV source directory
# build and install the binary in the `bin` directory
make 

# run test
make test
```