TiDB-DM (Data Migration) is a platform that supports migrating large, complex, production data sets from MySQL or MariaDB to TiDB.

TiDB-DM can support migrating sharded topologies from in-production databases by merging tables from multiple separate MySQL/MariaDB instances/clusters and applying rolling production updates using the MySQL/MariaDB binary log.

In this tutorial, we'll see how to migrate a sharded table from multiple upstream MySQL instances. We'll do this a couple of different ways. First, we'll merge several tables/shards that do not conflict; that is, they're partitioned using a scheme that does not result in conflicting unique key values. Then, we'll merge several tables that **do** have conflicting unique key values.

=== Architecture
https://pingcap.com/images/docs/dm-architecture.png

https://pingcap.com/docs/tools/dm/overview/

=== Setup

First, install MySQL 5.7 and download/extract the TiDB packages we'll use: 
```bash
sudo yum install -y http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/mysql57-community-release-el7-10.noarch.rpm
sudo yum install -y mysql-community-server
curl http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz | tar xzf -
curl http://download.pingcap.org/dm-latest-linux-amd64.tar.gz | tar xzf -
# curl http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz | tar xzf -
```

Create some directories and symlinks:
```bash
mkdir -p bin data logs conf
ln -s -t bin/ "$HOME"/*/bin/*
```

Set up MySQL configuration for the 3 instances we'll run:
```bash
tee -a "$HOME/.my.cnf" <<EoCNF
[server]
socket=mysql.sock
pid-file=mysql.pid
log-error=mysql.err
log-bin
auto-increment-increment=5
[server1]
datadir=$HOME/data/mysql1
server-id=1
port=3307
auto-increment-offset=1
[server2]
datadir=$HOME/data/mysql2
server-id=2
port=3308
auto-increment-offset=2
[server3]
datadir=$HOME/data/mysql3
server-id=3
port=3309
auto-increment-offset=3
EoCNF
```

Initialize and start MySQL instances:
```bash
for i in 1 2 3
do
    echo  "mysql$i"
    mysqld --defaults-group-suffix="$i" --initialize-insecure
    mysqld --defaults-group-suffix="$i" &
done
```

=== Non-overlapping shards
Create MySQL schema:
```bash
for i in 1 2 3
do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root <<EoSQL
        create database dmtest1;
        create table dmtest1.t1 (id bigint unsigned not null auto_increment primary key, c char(32), port int);
EoSQL
done
```

Insert a few hundred rows into each of the MySQL instances:
```bash
for i in 1 2 3; do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root dmtest1 <<EoSQL
        insert into t1 values (),(),(),(),(),(),(),();
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        update t1 set c=md5(id), port=@@port;
EoSQL
done
```

Select the rows back from the MySQL instances to make sure things look right:
```bash
for i in 1 2 3; do
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'select * from dmtest1.t1'
done | sort -n
```

The port number in the right-hand columns shows which instance the rows are coming from):
```
...
1841    e8dfff4676a47048d6f0c4ef899593dd        3307
1842    57c0531e13f40b91b3b0f1a30b529a1d        3308
1843    4888241374e8c62ddd9b4c3cfd091f96        3309
1846    f45a1078feb35de77d26b3f7a52ef502        3307
1847    82cadb0649a3af4968404c9f6031b233        3308
1848    7385db9a3f11415bc0e9e2625fae3734        3309
1851    ff1418e8cc993fe8abcfe3ce2003e5c5        3307
1852    eb1e78328c46506b46a4ac4a1e378b91        3308
1853    7503cfacd12053d309b6bed5c89de212        3309
1856    3c947bc2f7ff007b86a9428b74654de5        3307
1857    a3545bd79d31f9a72d3a78690adf73fc        3308
1858    d7fd118e6f226a71b5f1ffe10efd0a78        3309
```

=== Starting TiDB-DM master, workers, and task1

Our goal in this exercise is to use DM to combine the data from these distinct MySQL instances into a single table in TiDB.

We'll start a single dm-master process and one dm-worker process for each of the MySQL server instances (3 total).

```bash
tidb-server --log-file=logs/tidb-server.log &
for i in 1 2 3; do dm-worker --config=conf/dm-worker$i.toml & done
dm-master --config=conf/dm-master.toml &
```

The `dmctl` tool is an interactive client that facilitates interaction with the TiDB-DM cluster. You use it to start tasks, query task status, et cetera. Start the tool by executing `dmctl` to get the interactive prompt:
```
$ dmctl -master-addr :8261
Welcome to dmctl
Release Version: v1.0.0-alpha-69-g5134ad1
Git Commit Hash: 5134ad19fbf6c57da0c7af548f5ca2a890bddbe4
Git Branch: master
UTC Build Time: 2019-04-29 09:36:42
Go Version: go version go1.12 linux/amd64

»
```

To start dmtask1, execute `start-task conf/dmtask1.yaml`:
```
» start-task conf/dmtask1.yaml
{
    "result": true,
    "msg": "",
    "workers": [
        {
            "result": true,
            "worker": "127.0.0.1:8262",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.1:8263",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.1:8264",
            "msg": ""
        }
    ]
}
```

Starting the task will kick off the actions defined in the task configuration file. That includes executing instances of mydumper and loader, and connecting the workers to the upstream MySQL servers as replication slaves after the initial data dump has been loaded.



We can see that all rows have been migrated to the TiDB server:
```bash
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest1 | tail
```

Expect this output:
```
...
1843    4888241374e8c62ddd9b4c3cfd091f96        3309
1846    f45a1078feb35de77d26b3f7a52ef502        3307
1847    82cadb0649a3af4968404c9f6031b233        3308
1848    7385db9a3f11415bc0e9e2625fae3734        3309
1851    ff1418e8cc993fe8abcfe3ce2003e5c5        3307
1852    eb1e78328c46506b46a4ac4a1e378b91        3308
1853    7503cfacd12053d309b6bed5c89de212        3309
1856    3c947bc2f7ff007b86a9428b74654de5        3307
1857    a3545bd79d31f9a72d3a78690adf73fc        3308
1858    d7fd118e6f226a71b5f1ffe10efd0a78        3309
```

DM is now acting as a slave to each of the MySQL servers, reading their binary logs to apply updates in realtime to the downstream TiDB server:
```
$ for i in 1 2 3
do
     mysql -h 127.0.0.1 -P "$((3306+i))" -u root -e 'select host, command, state from information_schema.processlist where command="Binlog Dump"'
done
+-----------------+-------------+---------------------------------------------------------------+
| host            | command     | state                                                         |
+-----------------+-------------+---------------------------------------------------------------+
| localhost:42168 | Binlog Dump | Master has sent all binlog to slave; waiting for more updates |
+-----------------+-------------+---------------------------------------------------------------+
+-----------------+-------------+---------------------------------------------------------------+
| host            | command     | state                                                         |
+-----------------+-------------+---------------------------------------------------------------+
| localhost:42922 | Binlog Dump | Master has sent all binlog to slave; waiting for more updates |
+-----------------+-------------+---------------------------------------------------------------+
+-----------------+-------------+---------------------------------------------------------------+
| host            | command     | state                                                         |
+-----------------+-------------+---------------------------------------------------------------+
| localhost:56798 | Binlog Dump | Master has sent all binlog to slave; waiting for more updates |
+-----------------+-------------+---------------------------------------------------------------+
```

We can see that this is the case by inserting some rows into the upstream MySQL servers, selecting those rows from TiDB, updating those same rows in MySQL, and selecting them again:
```bash
for i in 1 2 3; do
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'insert into t1 (id) select null from t1' dmtest1
done
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest1 | tail
```

Expect this output:
```
6313    NULL    NULL
6316    NULL    NULL
6317    NULL    NULL
6318    NULL    NULL
6321    NULL    NULL
6322    NULL    NULL
6323    NULL    NULL
6326    NULL    NULL
6327    NULL    NULL
6328    NULL    NULL
```

Now update those rows, so we can see that changes to data are correctly propagated to TiDB:
```bash
for i in 1 2 3; do
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'update t1 set c=md5(id), port=@@port' dmtest1
done | sort -n
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest1 | tail
```

Expect this output:
```
6313    2118d8a1b7004ed5baf5347a4f99f502        3309
6316    6107d91fc9a0b04bc044aa7d8c1443bd        3307
6317    0e9b734aa25ca8096cb7b56dc0dd8929        3308
6318    b0eb9a95e8b085e4025eae2f0d76a6a6        3309
6321    7cb36e23529e4de4c41460940cc85e6e        3307
6322    fe1f9c70bdf347497e1a01b6c486bdb9        3308
6323    14eac0d254a6ccaf9b67584c7830a5c0        3309
6326    17b65afe58c49edc1bdd812c554ee3bb        3307
6327    c54bc2ded4480856dc9f39bdcf35a3e7        3308
6328    b294504229c668e750dfcc4ea9617f0a        3309
```

As long as the DM master and workers are running the "dmtest1" task, they'll continue to keep the downstream TiDB server synchronized with the upstream MySQL server instances.


=== Overlapping shards

The first step of the next exercise will be to create a second database and set of tables across the MySQL instances.
```bash
for i in 1 2 3
do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root <<EoSQL
        create database dmtest2;
        create table dmtest2.t1 (id bigint unsigned not null auto_increment primary key, c char(32), port int);
EoSQL
done
```

Insert a few hundred rows into each of the MySQL instances. By setting `auto_increment_increment=1` and `auto_increment_offset=1`, we'll ensure that all 3 MySQL servers allocate the same auto-increment IDs:
```bash
for i in 1 2 3; do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root dmtest2 <<EoSQL
        set auto_increment_increment=1, auto_increment_offset=1;
        insert into t1 values (),(),(),(),(),(),(),();
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        update t1 set c=md5(id), port=@@port;
EoSQL
done
```

Select the rows back from the MySQL instances to make sure things look right:
```bash
for i in 1 2 3; do
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root -e 'select * from t1' dmtest2
done | sort -n
```

Unlike the last exercise, this time you can see that the same auto-increment IDs (the left-most column) are duplicated across multiple upstream instances (identified by the port number in the right-most column):
```
EoSQL
...
370     d709f38ef758b5066ef31b18039b8ce5        3307
370     d709f38ef758b5066ef31b18039b8ce5        3308
370     d709f38ef758b5066ef31b18039b8ce5        3309
371     41f1f19176d383480afa65d325c06ed0        3307
371     41f1f19176d383480afa65d325c06ed0        3308
371     41f1f19176d383480afa65d325c06ed0        3309
372     24b16fede9a67c9251d3e7c7161c83ac        3307
372     24b16fede9a67c9251d3e7c7161c83ac        3308
372     24b16fede9a67c9251d3e7c7161c83ac        3309
```

If we try to migrate these rows as-is into a single table in a downstream TiDB instance, the Primary Key auto-increment values will collide and cause duplicate key errors to be issued. We'll use the "partition id" expression of the "column mappings" feature of DM to transform the auto-increment values so that they no longer collide. 

```bash
dmctl -master-addr :8261 <<<"start-task conf/dmtask2.yaml"
```

```bash
mysql -h 127.0.0.1 -P 4000 -u root -e 'select * from t1' dmtest2 | tail
```

```
1729382256910270827     00411460f7c92d2124a67ea0f4cb5f85        3309
1729382256910270828     bac9162b47c56fc8a4d2a519803d51b3        3309
1729382256910270829     9be40cee5b0eee1462c82c6964087ff9        3309
1729382256910270830     5ef698cd9fe650923ea331c15af3b160        3309
1729382256910270831     05049e90fa4f5039a8cadc6acbb4b2cc        3309
1729382256910270832     cf004fdc76fa1a4f25f62e0eb5261ca3        3309
1729382256910270833     0c74b7f78409a4022a2c4c5a5ca3ee19        3309
1729382256910270834     d709f38ef758b5066ef31b18039b8ce5        3309
1729382256910270835     41f1f19176d383480afa65d325c06ed0        3309
1729382256910270836     24b16fede9a67c9251d3e7c7161c83ac        3309
```

TiDB-DM uses an algorithm to bit-shift the ID assigned by the upstream MySQL instances to generate a unique ID for the downstream TiDB instance. In our test case, the partition ID consists only of the "instance ID", because the schema and table names are the same on each of the upstream MySQL servers. We leave the "schema ID" and "table ID" components of the partition id expression arguments blank:

```
$ grep arguments conf/dmtask2.yaml
    arguments: ["1", null, null]
    arguments: ["2", null, null]
    arguments: ["3", null, null]
```

The last auto-increment ID assigned by the upstream MySQL servers was 372. The rows with the highest transformed auto-increment IDs after migration to the TiDB server are from instance 3 (identified by port number 3309 in the right-most column). The last row has the same value in the middle column as the rows with ID 372 in the MySQL instances. The algorithm allots 44 bits of the 64 bit integer for the auto-increment ID that comes from upstream, which means that values above 2^44 (about 17.5 trillion) can't be handled by the default implementation of the partition id column mapping scheme. 1 bit is reserved for the sign, 4 for the instance ID, 7 for the schema ID, and 8 for the table ID (44 + 1 + 4 + 7 + 8 = 64 bits). Customizations of the algorithm are trivial, so please contact PingCAP if you have a use case that can't be accommodated by this implementation.

Here we can see the algorithm in action for our use case, taking an auto-increment ID of 372 and instance ID of 3:
```bash
id=372 instance_id=3 schema_id=0 table_id=0
echo $(( instance_id << (64-1-4) | schema_id << (64-1-4-7) | table_id << 44 | id ))
```

Expected output:
```
1729382256910270836
```

Because only 44 bits correspond to the original auto-increment value, we can discard the rest of them to convert the transofmred values back to what they were originally:

```bash
echo $(( 1729382256910270836 & (1<<45)-1 ))
```

Expected output:
```
372
```

And we can even use that expression in an SQL query to see the transformed IDs along the original IDs:
```bash
mysql -h 127.0.0.1 -P 4000 -u root -e 'select id, id&(1<<45)-1 as orig_id, c, port from t1 order by orig_id' dmtest2 | tail
```

Expected output:
```
576460752303423857      369     0c74b7f78409a4022a2c4c5a5ca3ee19        3307
576460752303423858      370     d709f38ef758b5066ef31b18039b8ce5        3307
1152921504606847346     370     d709f38ef758b5066ef31b18039b8ce5        3308
1729382256910270834     370     d709f38ef758b5066ef31b18039b8ce5        3309
576460752303423859      371     41f1f19176d383480afa65d325c06ed0        3307
1729382256910270835     371     41f1f19176d383480afa65d325c06ed0        3309
1152921504606847347     371     41f1f19176d383480afa65d325c06ed0        3308
576460752303423860      372     24b16fede9a67c9251d3e7c7161c83ac        3307
1729382256910270836     372     24b16fede9a67c9251d3e7c7161c83ac        3309
1152921504606847348     372     24b16fede9a67c9251d3e7c7161c83ac        3308
```



TODO:
* PR/FR for command-line behavior of dmctl
* PR/FR for default value of dmctl -master-address
* clarify expected behavior of column-mappings/./arguments


for i in 1 2 3; do mysql -h 127.0.0.1 -P "$((3306+i))" -u root -e 'show databases; drop database if exists dmtest2; drop database if exists dmtest1; drop database if exists dmtest; drop database if exists dm_heartbeat; show databases; '; done
