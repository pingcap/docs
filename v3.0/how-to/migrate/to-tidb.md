---
title: Migrate Data from TiDB to TiDB/MySQL
summary: migrate data from master TiDB clister to slave TiDB cluster or MySQL.
category: how-to
aliases: ['/docs/op-guide/migration/']
---

# Migrate Data from TiDB to TiDB/MySQL

## Pre-requirements

* you must already [deploy pump cluster](https://pingcap.com/docs/v3.0/reference/tools/tidb-binlog/deploy/), don't need to deploy drainer.

## Temporal logic of migration opeations

1.  Obtain `initial_commit_ts`. 

2. Use `mydumper` to export data from master TiDB cluster

3. Use `loader` to import the data into slave TiDB cluster or MySQL.

4. Use `initial_commit_ts` obtained in step 1 to start drainer

## Migrate Data Process

`Mydumper` and `loader` can be [downloaded as part of Enterprise Tools](/reference/tools/download.md).

### Obtain `initial_commit_ts`

Run the following command to use `binlogctl` to generate the `tso` information which is needed for the initial start of Drainer:

```bash
$ cd /home/tidb/tidb-ansible
$ resources/bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd generate_meta
INFO[0000] [pd] create pd client with endpoints [http://192.168.199.118:32379]
INFO[0000] [pd] leader switches to: http://192.168.199.118:32379, previous:
INFO[0000] [pd] init cluster id 6569368151110378289
2018/06/21 11:24:47 meta.go:117: [info] meta: &{CommitTS:400962745252184065}
```

This command outputs `meta: &{CommitTS:400962745252184065}`, and the value of `CommitTS` is used as the value of the `initial_commit_ts` parameter needed for the initial start of Drainer. 


### Export data from master TiDB cluster

Use the `mydumper` tool to export data from master TiDB cluster by using the following command:

```bash
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 64 -B test -T t1,t2 --skip-tz-utc -o ./var/test
```
In this command,

- `-B test`: means the data is exported from the `test` database.
- `-T t1,t2`: means only the `t1` and `t2` tables are exported.
- `-t 16`: means 16 threads are used to export the data.
- `-F 64`: means a table is partitioned into chunks and one chunk is 64MB.
- `--skip-tz-utc`: the purpose of adding this parameter is to ignore the inconsistency of time zone setting between MySQL and the data exporting machine and to disable automatic conversion.

### Import data to slave TiDB cluster/MySQL

Use `loader` to import the data to slave TiDB cluster/MySQL. See [Loader instructions](/reference/tools/loader.md) for more information.

```bash
./bin/loader -h 127.0.0.1 -u root -P 4000 -t 32 -d ./var/test
```

After the data is imported, you can view the data in TiDB using the MySQL client:

```sql
mysql -h127.0.0.1 -P4000 -uroot

mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| t2             |
+----------------+

mysql> select * from t1;
+----+------+
| id | age  |
+----+------+
|  1 |    1 |
|  2 |    2 |
|  3 |    3 |
+----+------+

mysql> select * from t2;
+----+------+
| id | name |
+----+------+
|  1 | a    |
|  2 | b    |
|  3 | c    |
+----+------+
```

### Start drainer

1. Modify the `tidb-ansible/inventory.ini` file.

    Add the deployment machine IPs for `drainer_servers`. Set `initial_commit_ts` to the value you have obtained, which is only used for the initial start of Drainer.

    - Assume that the downstream is MySQL with the alias `drainer_mysql`:

        ```ini
        [drainer_servers]
        drainer_mysql ansible_host=172.16.10.71 initial_commit_ts="402899541671542785"
        ```

    - Assume that the downstream is `file` with the alias `drainer_file`:

        ```ini
        [drainer_servers]
        drainer_file ansible_host=172.16.10.71 initial_commit_ts="402899541671542785"
        ```

2. Modify the configuration file.

    - Assume that the downstream is MySQL:

        ```bash
        $ cd /home/tidb/tidb-ansible/conf
        $ cp drainer-cluster.toml drainer_mysql_drainer-cluster.toml
        $ vi drainer_mysql_drainer-cluster.toml
        ```

        > **Note:**
        >
        > Name the configuration file as `alias_drainer-cluster.toml`. Otherwise, the customized configuration file cannot be found during the deployment process.
        
        Set `db-type` to `mysql` and configure the downstream MySQL information:

        ```toml
        # downstream storage, equal to --dest-db-type
        # Valid values are "mysql", "file", "kafka", and "flash".
        db-type = "mysql"

        # the downstream MySQL protocol database
        [syncer.to]
        host = "172.16.10.72"
        user = "root"
        password = "123456"
        port = 3306
        # Time and size limits for flash batch write
        ```

    - Assume that the downstream is incremental backup data:

        ```bash
        $ cd /home/tidb/tidb-ansible/conf
        $ cp drainer-cluster.toml drainer_file_drainer-cluster.toml
        $ vi drainer_file_drainer-cluster.toml
        ```

        Set `db-type` to `file`.

        ```toml
        # downstream storage, equal to --dest-db-type
        # Valid values are "mysql", "file", "kafka", and "flash".
        db-type = "file"

        # Uncomment this if you want to use `file` as `db-type`. 
        # The value can be `gzip`. Leave it empty to disable compression. 
        [syncer.to]
        # default data directory: "{{ deploy_dir }}/data.drainer"
        dir = "data.drainer"
        ```

3. Deploy Drainer.

    ```bash
    $ ansible-playbook deploy_drainer.yml
    ```

4. Start Drainer.

    ```bash
    $ ansible-playbook start_drainer.yml
    ```