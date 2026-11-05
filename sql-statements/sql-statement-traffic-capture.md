---
title: TRAFFIC CAPTURE
summary: An overview of the usage of TRAFFIC CAPTURE for the TiDB database.
---

# TRAFFIC CAPTURE

TiDB v9.0.0 introduces the `TRAFFIC CAPTURE` syntax, which is used to send requests to all [TiProxy](/tiproxy/tiproxy-overview.md) instances in the cluster, allowing TiProxy to capture client traffic and save it to traffic files.

TiProxy supports capturing traffic to local and external storage. When using local storage, you need to manually copy the traffic files to the TiProxy cluster for replay. When using external storage, no manual copying is needed.

TiProxy supports external storage including Amazon S3, Google Cloud Storage (GCS), Azure Blob Storage, and other S3-compatible file storage services. For more information about external storage, see [URI formats of external storage services](/external-storage-uri.md).

`TRAFFIC CAPTURE` supports the following options:

- `DURATION`: (required) specifies the duration of capture. The unit is one of `m` (minutes), `h` (hours), or `d` (days). For example, `DURATION="1h"` captures traffic for one hour.
- `COMPRESS`: (optional) specifies whether to compress traffic files. `true` means compression, and the compression format is gzip. `false` means no compression. The default value is `true`.
- `ENCRYPTION_METHOD`: (optional) specifies the algorithm for encrypting traffic files. Only `""`, `plaintext`, and `aes256-ctr` are supported. `""` and `plaintext` indicate no encryption, and `aes256-ctr` indicates encryption using the `AES256-CTR` algorithm. When specifying encryption, you also need to configure [`encryption-key-path`](/tiproxy/tiproxy-configuration.md#encryption-key-path). The default value is `""`.

To capture traffic, the current user must have the `SUPER` or [`TRAFFIC_CAPTURE_ADMIN`](/privilege-management.md#dynamic-privileges) privilege.

## Synopsis

```ebnf+diagram
TrafficStmt ::=
    "TRAFFIC" "CAPTURE" "TO" stringLit TrafficCaptureOptList

TrafficCaptureOptList ::=
    TrafficCaptureOpt
|   TrafficCaptureOptList TrafficCaptureOpt

TrafficCaptureOpt ::=
    "DURATION" EqOpt stringLit
|   "ENCRYPTION_METHOD" EqOpt stringLit
|   "COMPRESS" EqOpt Boolean
```

## Examples

Capture traffic for one day and save it to the local `/tmp/traffic` directory on the TiProxy instance:

```sql
TRAFFIC CAPTURE TO "/tmp/traffic" DURATION="1d";
```

Capture traffic for 10 minutes and save it to S3:

```sql
TRAFFIC CAPTURE TO "s3://external/traffic?access-key=${access-key}&secret-access-key=${secret-access-key}" DURATION="10m";
```

Capture traffic with automatic encryption but without compression:

```sql
TRAFFIC CAPTURE TO "/tmp/traffic" DURATION="1h" COMPRESS=false ENCRYPTION_METHOD="aes256-ctr";
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [TiProxy traffic replay](/tiproxy/tiproxy-traffic-replay.md)
* [`TRAFFIC REPLAY`](/sql-statements/sql-statement-traffic-replay.md)
* [`CANCEL TRAFFIC JOBS`](/sql-statements/sql-statement-cancel-traffic-jobs.md)
* [`SHOW TRAFFIC JOBS`](/sql-statements/sql-statement-show-traffic-jobs.md)
