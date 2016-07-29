# Build

## Overview

If you want to dive into TiDB project, change some codes and send us PR, you may follow this guide to build TiDB project.

You can see [user build guide](../op-guide/build.md) to check platforms and prerequisites first. 

## Install RocksDB

RocksDB 4.9+ is required, you can install RocksDB shared library manually according to [INSTALL.md](https://github.com/facebook/rocksdb/blob/master/INSTALL.md). 

The [build RocksDB script](../scripts/build_rocksdb.sh) can help you build and install RocksDB in system path.

## Build TiKV

After you install RocksDB shared library, you can build TiKV directly without `ROCKSDB_SYS_STATIC`.

```bash
# cd TiKV source root.
# build release binary
make release

# run test
make test

# build with clippy
make dev
```