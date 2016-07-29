# Build

## Overview

If you want to dive into TiDB project, change some codes and send us PR, you can follow this guide to build TiDB project.

See [user build guide](../op-guide/build.md) to check platforms and prerequisites first. 

## Install RocksDB

RocksDB 4.9+ is required, You can install the RocksDB shared library manually according to INSTALL.md or use the [build RocksDB script](../scripts/build_rocksdb.sh) to build and install RocksDB in the system path.

## Build TiKV

After you install the RocksDB shared library, you can build TiKV directly without `ROCKSDB_SYS_STATIC`.

```bash
# cd TiKV source directory
# build and install the binary in the `bin` directory
make 

# run test
make test
```