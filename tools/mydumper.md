---
title: mydumper Instructions 
summary: Use mydumper to export data from TiDB.
category: tools
---

# mydumper Instructions

## What is mydumper?

Mydumper is a fork of the [mydumper](https://github.com/maxbube/mydumper) project with additional functionality specific to TiDB.  It is the recommended method to use for logical backups of TiDB.

[Download the Binary](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz).

## What enhancements does this contain over regular mydumper?

+ Use `tidb_snapshot` to provide backup consistency instead of `FLUSH TABLES WITH READ LOCK`

+ Include the hidden `_tidb_rowid` column in exports when present

+ Allow for `tidb_snapshot` to be configurable (i.e. backup data as it appeared at an earlier point in time)


### New parameter description

```
  -z, --tidb-snapshot: Set the tidb_snapshot to be used for the backup.
                       Default: NOW()-INTERVAL 1 SECOND.
```

### Usage example

Command line parameter:

```
./bin/mydumper -h 127.0.0.1 -u root -P 4000
```
## FAQ

### Is this source code for these changes available?

Source code for PingCAP's mydumper is [available on GitHub](https://github.com/pingcap/mydumper).

### Do you plan to make these changes available to upstream mydumper?

Yes, we intend to make our changes available to upstream mydumper.  See [PR #155](https://github.com/maxbube/mydumper/pull/155).
