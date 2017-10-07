# Install Rust

## Background

Now tikv must be compiled by rust nightly-build version, details in [issue1671](https://github.com/pingcap/tikv/issues/1671).
For those who are new to rust, here is the step how you can install rust nightly-build version.


## For rust newly installation

1. run install script as mentioned in [official site](https://www.rust-lang.org/zh-CN/install.html)
```
curl https://sh.rustup.rs -sSf | sh
```

2. in the first selection window we type 2 and enter
```

Current installation options:

default host triple: x86_64-apple-darwin
default toolchain: stable
modify PATH variable: yes

1) Proceed with installation (default)
2) Customize installation
3) Cancel installation
```


3.  in the second selection, we type enter directly
```
I'm going to ask you the value of each these installation options.
You may simply press the Enter key to leave unchanged.

Default host triple?
```

4. in the third selection, we type nightly and enter
```
Default toolchain? (stable/beta/nightly)
```

5. then we type enter all the way, rust nightly-build will be installed in your machine.



## For those who has already installed rust but not nightly-build

1. check  rust version
```
rustc -V
```
check whether what displays in your terminal after this command  contains **nightly** 

like 
```
rustc 1.15.1 (021bd294c 2017-02-08)
```
is not a nightly version

2 install nightly-build version
```
rustup install nightly
```
