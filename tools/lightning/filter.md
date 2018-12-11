---
title: TiDB-Lightning Table Filter
summary: Use black and white lists to filter out tables, ignoring them during import.
category: tools
---

# TiDB-Lightning Table Filter

TiDB-Lightning supports setting up black and white lists to ignore certain databases and tables. This can be used to skip cache tables, or manually partition the data source on a shared storage to allow multiple Lightning instances work together without interfering each other.

The filtering rule is similar to MySQL `replication-rules-db`/`replication-rules-table`.

## Filtering databases

```toml
[black-white-list]
do-dbs = ["pattern1", "pattern2", "pattern3"]
ignore-dbs = ["pattern4", "pattern5"]
```

If the name of a database matched *any* pattern in the `do-dbs` array in the `[black-white-list]` section, the database will be included.

Otherwise, if the name matched *any* pattern in the `ignore-dbs` array, the database will be skipped.

If a database’s name matched *both* the `do-dbs` and `ignore-dbs` arrays, the database will be included.

The pattern can either be a simple name, or a regular expression in [Go dialect](https://golang.org/pkg/regexp/syntax/#hdr-Syntax) if it starts with a `~` character.

## Filtering tables

```toml
[[black-white-list.do-tables]]
db-name = "db-pattern-1"
table-name = "table-pattern-1"

[[black-white-list.do-tables]]
db-name = "db-pattern-2"
table-name = "table-pattern-2"

[[black-white-list.do-tables]]
db-name = "db-pattern-3"
table-name = "table-pattern-3"

[[black-white-list.ignore-tables]]
db-name = "db-pattern-4"
table-name = "table-pattern-4"

[[black-white-list.ignore-tables]]
db-name = "db-pattern-5"
table-name = "table-pattern-5"
```

If the qualified name of a table matched *any* pair of patterns in the `do-tables` array, the table will be included.

Otherwise, if the qualified name matched *any* pair of patterns in the `ignore-tables` array, the table will be skipped.

If a table’s qualified name matched *both* the `do-tables` and `ignore-tables` arrays, the table will be included.

Note that the database filtering rules are applied before considering the table filtering rules. This means if a database is ignored by `ignore-dbs`, all tables inside this database will not be considered even if they matched any `do-tables` array.

## Example

To illustrate how these rules work, suppose the data source contains the following tables:

```
`logs`.`messages_2016`
`logs`.`messages_2017`
`logs`.`messages_2018`
`forum`.`users`
`forum`.`messages`
`forum_backup_2016`.`messages`
`forum_backup_2017`.`messages`
`forum_backup_2018`.`messages`
```

Using this configuration:

```toml
[black-white-list]
do-dbs = [
    "forum_backup_2018",            # rule A
    "forum",                        # rule B
]
ignore-dbs = [
    "~^forum_backup_",              # rule C
]

[[black-white-list.do-tables]]      # rule D
db-name = "logs"
table-name = "~_2018$"

[[black-white-list.ignore-tables]]  # rule E
db-name = "~.*"
table-name = "~^messages.*"

[[black-white-list.do-tables]]      # rule F
db-name = "~^forum.*"
table-name = "messages"
```

First apply the database rules:

| Database                  | Outcome                                    |
|---------------------------|--------------------------------------------|
| `` `logs` ``              | Included by default                        |
| `` `forum` ``             | Included by rule B                         |
| `` `forum_backup_2016` `` | Skipped by rule C                          |
| `` `forum_backup_2017` `` | Skipped by rule C                          |
| `` `forum_backup_2018` `` | Included by rule A (rule C will not apply) |

Then apply the table rules:

| Table                                | Outcome                                    |
|--------------------------------------|--------------------------------------------|
| `` `logs`.`messages_2016` ``         | Skipped by rule E                          |
| `` `logs`.`messages_2017` ``         | Skipped by rule E                          |
| `` `logs`.`messages_2018` ``         | Included by rule D (rule E will not apply) |
| `` `forum`.`users` ``                | Included by default                        |
| `` `forum`.`messages` ``             | Included by rule F (rule E will not apply) |
| `` `forum_backup_2016`.`messages` `` | Skipped, since is database already skipped |
| `` `forum_backup_2017`.`messages` `` | Skipped, since is database already skipped |
| `` `forum_backup_2018`.`messages` `` | Included by rule F (rule E will not apply) |
