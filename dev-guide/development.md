# Build For Development

## Overview

If you want to develop the TiDB project, you can follow this guide.

Before you begin, check the [supported platforms](./requirements.md#supported-platforms) and [prerequisites](./requirements.md#prerequisites) first.

## Build TiKV

### Rust toolchain

Rust Nightly is required. The version that we currently use can be found in the file named `RUST_VERSION` in TiKV git repository. 

```
# Get rustup from rustup.rs, then in your `tikv` folder:
$ rustup override set nightly-2018-01-12
$ cargo +nightly-2018-01-12 install rustfmt-nightly --version 0.3.4
```

### Golang

Golang 1.9 or higher version is required. Please refer to [](https://golang.org/doc/install) to find how to install.

### GCC

GCC 4.8 or higher version is needed. If your GCC's version is too low, please upgrade first.

### CMake

Some dependencies of TiKV need CMake to be built. Please install CMake 3.1 or higher version.

### TiKV

Get TiKV source code from GitHub

```
$ git clone https://github.com/pingcap/tikv.git 
```

Run all unit tests:

```
$ make test
```

Build in release mode:

```
$ make release
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
