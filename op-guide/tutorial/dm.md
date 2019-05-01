TiDB-DM (Data Migration) is a platform that supports migrating large, complex, production data sets from MySQL or MariaDB to TiDB.

TiDB-DM can support migrating sharded topologies from in-production databases by merging tables from multiple separate MySQL/MariaDB instances/clusters and applying rolling production updates using the MySQL/MariaDB binary log.

===Architecture
https://pingcap.com/images/docs/dm-architecture.png

https://pingcap.com/docs/tools/dm/overview/


```bash
sudo yum install -y http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/mysql57-community-release-el7-10.noarch.rpm
sudo yum install -y mysql-community-server
```

```bash
tee my.cnf <<EoCNF
[server]
socket=mysql.sock
log-error=mysql.err
pid-file=mysql.pid
auto-increment-increment=5
[server1]
datadir=$HOME/mysql1
port=3307
auto-increment-offset=1
[server2]
datadir=$HOME/mysql2
port=3308
auto-increment-offset=2
[server3]
datadir=$HOME/mysql3
port=3309
auto-increment-offset=3
EoCNF
```

```bash
for i in 1 2 3
do
    dir="$HOME/mysql$i"
    mkdir -p "$dir"
    echo "$dir"
    mysqld --defaults-file=my.cnf --defaults-group-suffix="$i" --initialize-insecure
    mysqld --defaults-file=my.cnf --defaults-group-suffix="$i" &
done
```

```
for i in 1 2 3
do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root <<EoSQL
        create database dmtest;
        create table dmtest.t1 (id bigint unsigned not null auto_increment primary key, c char(32));
EoSQL
done
```

```
for i in 1 2 3; do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root dmtest <<EoSQL
        insert into t1 values (),(),(),(),(),(),(),();
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
        insert into t1 (id) select null from t1;
EoSQL
done
```

```
for i in 1 2 3; do
    mysql -h 127.0.0.1 -P "$((3306+i))" -u root dmtest <<EoSQL
        update t1 set c=md5(id);
        select * from t1;
EoSQL
done
```
