---
title: TRAFFIC REPLAY
summary: An overview of the usage of TRAFFIC REPLAY for the TiDB database.
---

# TRAFFIC REPLAY

TiDB v9.0.0 introduces the `TRAFFIC REPLAY` syntax, which is used to send requests to all [TiProxy](/tiproxy/tiproxy-overview.md) instances in the cluster, allowing TiProxy to replay traffic from the traffic file to TiDB.

To replay traffic, the current user must have the `SUPER` or [`TRAFFIC_REPLAY_ADMIN`](/privilege-management.md#dynamic-privileges) privilege.

`TRAFFIC REPLAY` supports the following options:

- `USER`: (required) specifies the database username for replay.
- `PASSWORD`: (optional) specifies the password for the username. The default value is an empty string `""`.
- `SPEED`: (optional) specifies the replay speed multiplier. The range is `[0.1, 10]`. The default value is `1`, indicating replay at the original speed.
- `READ_ONLY`: (optional) specifies whether to replay only read-only SQL statements. `true` means to replay only read-only SQL statements, `false` means to replay all SQL statements. The default value is `false`.

## Synopsis

```ebnf+diagram
TrafficStmt ::=
    "TRAFFIC" "REPLAY" "FROM" stringLit TrafficReplayOptList

TrafficReplayOptList ::=
    TrafficReplayOpt
|   TrafficReplayOptList TrafficReplayOpt

TrafficReplayOpt ::=
    "USER" EqOpt stringLit
|   "PASSWORD" EqOpt stringLit
|   "SPEED" EqOpt NumLiteral
|   "READ_ONLY" EqOpt Boolean
```

## Examples

Replay traffic from the local `/tmp/traffic` directory of the TiProxy instance, using the TiDB user `u1`, whose password is `"123456"`:

```sql
TRAFFIC REPLAY FROM "/tmp/traffic" USER="u1" PASSWORD="123456";
```

Replay traffic from the traffic files stored in the S3 storage:

```sql
TRAFFIC REPLAY FROM "s3://external/traffic?access-key=${access-key}&secret-access-key=${secret-access-key}" USER="u1" PASSWORD="123456";
```

Replay traffic at double speed:

```sql
TRAFFIC REPLAY FROM "/tmp/traffic" USER="u1" PASSWORD="123456" SPEED=2;
```

Replay only read-only statements, not write statements:

```sql
TRAFFIC REPLAY FROM "/tmp/traffic" USER="u1" PASSWORD="123456" READ_ONLY=true;
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [TiProxy traffic replay](/tiproxy/tiproxy-traffic-replay.md)
* [`TRAFFIC CAPTURE`](/sql-statements/sql-statement-traffic-capture.md)
* [`SHOW TRAFFIC JOBS`](/sql-statements/sql-statement-show-traffic-jobs.md)
* [`CANCEL TRAFFIC JOBS`](/sql-statements/sql-statement-cancel-traffic-jobs.md)
