---
title: TiDB 1.1 Alpha Release Notes
aliases: ['/docs/dev/releases/release-1.1-alpha/','/docs/dev/releases/11alpha/']
summary: TiDB 1.1 Alpha, released on January 19, 2018, brings significant improvements in MySQL compatibility, SQL optimization, stability, and performance. Key updates include enhanced SQL parser, query optimizer, and executor, as well as server support for the PROXY protocol. PD now offers more APIs, TLS support, and improved scheduling, while TiKV introduces Raft learner support, TLS, and performance optimizations. Additionally, it enhances data recovery tools and improves flow control mechanisms.
---

# TiDB 1.1 Alpha Release Notes

On January 19, 2018, TiDB 1.1 Alpha is released. This release has great improvement in MySQL compatibility, SQL optimization, stability, and performance.

## TiDB

- SQL parser
    - Support more syntax
- SQL query optimizer
    - Use more compact structure to reduce statistics info memory usage
    - Speed up loading statistics info when starting tidb-server
    - Provide more accurate query cost evaluation
    - Use `Count-Min Sketch` to estimate the cost of queries using unique index more accurately
    - Support more complex conditions to make full use of index
- SQL executor
    - Refactor all executor operators using Chunk architecture, improve the execution performance of analytical statements and reduce memory usage
    - Optimize performance of the `INSERT IGNORE` statement
    - Push down more types and functions to TiKV
    - Support more `SQL_MODE`
    - Optimize the `Load Data` performance to increase the speed by 10 times
    - Optimize the `Use Database` performance
    - Support statistics on the memory usage of physical operators
- Server
    - Support the PROXY protocol

## PD

- Add more APIs
- Support TLS
- Add more cases for scheduling Simulator
- Schedule to adapt to different Region sizes
- Fix some bugs about scheduling

## TiKV

- Support Raft learner
- Optimize Raft Snapshot and reduce the I/O overhead
- Support TLS
- Optimize the RocksDB configuration to improve performance
- Optimize `count (*)` and query performance of unique index in Coprocessor
- Add more failpoints and stability test cases
- Solve the reconnection issue between PD and TiKV
- Enhance the features of the data recovery tool `tikv-ctl`
- Support splitting according to table in Region
- Support the `Delete Range` feature
- Support setting the I/O limit caused by snapshot
- Improve the flow control mechanism
