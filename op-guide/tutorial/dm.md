TiDB-DM (Data Migration) is a platform that supports migrating large, complex, production data sets from MySQL or MariaDB to TiDB.

TiDB-DM can support migrating sharded topologies from in-production databases by merging tables from multiple separate MySQL/MariaDB instances/clusters and applying rolling production updates using the MySQL/MariaDB binary log.

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
ln -s -t bin/ */bin/*
```

Set up MySQL configuration for the 3 instances we'll run:
```bash
tee -a "$HOME/.my.cnf" <<EoCNF
[server]
socket=mysql.sock
pid-file=mysql.pid
log-error=mysql.err
log-bin
[server1]
datadir=$HOME/data/mysql1
server-id=1
port=3307
[server2]
datadir=$HOME/data/mysql2
server-id=2
port=3308
[server3]
datadir=$HOME/data/mysql3
server-id=3
port=3309
EoCNF
```

Initialize and start MySQL instances:
```bash
for i in 1 2 3
do
    ech  "mysql$i"
    mysqld --defaults-group-suffix="$i" --initialize-insecure
    mysqld --defaults-group-suffix="$i" &
done
```

Create MySQL schema:
```bash
for i in 1 2 3
do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root <<EoSQL
        create database dmtest;
        create table dmtest.t1 (id bigint unsigned not null auto_increment primary key, c char(32), port int);
EoSQL
done
```

Insert a few hundred rows into each of the MySQL instances:
```bash
for i in 1 2 3; do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root dmtest <<EoSQL
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
    mysql -N -h 127.0.0.1 -P "$((3306+i))" -u root dmtest <<EoSQL
        select * from t1;
EoSQL
done | sort -n
```

Notice that the auto-increment IDs conflict between the several instances (the port number in the right-hand columns shows which instance the rows are coming from):
```
...
369     0c74b7f78409a4022a2c4c5a5ca3ee19        3307
369     0c74b7f78409a4022a2c4c5a5ca3ee19        3308
369     0c74b7f78409a4022a2c4c5a5ca3ee19        3309
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

Our goal in this exercise is to use DM to combine the data from these distinct MySQL instances into a single table in TiDB, while resolving the conflicts between the auto-increment IDs.

```bash
tidb-server --log-file=log/tidb-server.log &
for i in 1 2 3; do dm-worker --config=conf/dm-worker$i.toml & done
dm-master --config=conf/dm-master.toml &
dmctl -master-addr :8261 <<<"start-task conf/task.yaml"
```

TODO:
* PR/FR for command-line behavior of dmctl
* PR/FR for default value of dmctl -master-address
* clarify expected behavior of column-mappings/./arguments
