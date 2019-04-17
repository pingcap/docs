TiDB Binlog is a stack of components that form a solution to push incremental updates to a TiDB Server cluster into any of a variety of downstream platforms. TiDB Binlog is distributed as a part of TiDB Enterprise Tools.

TODO: add real-world use case description

https://pingcap.com/docs/tools/tidb-binlog-cluster/

# Overview

TiDB Binlog comprises two components: the *pump* and the *drainer*. Several pump nodes make up a pump cluster. Each pump node connects to TiDB Server instances and receives updates made to each of the TiDB Server instances in a cluster. A drainer connects to the pump cluster and transforms updates into the correct format for a particular downstream destination, be it Kafka or another TiDB Cluster or a MySQL/MariaDB server.

The clustered architecture of the pump component ensures that updates won't be lost as new TiDB Server instances join or leave the TiDB Cluster or pump nodes join or leave the pump cluster.

This tutorial will start with a very simple TiDB Binlog deployment with a single node of each component (PD, TiKV Server, TiDB Server, pump, and drainer), set up to push data into a MariaDB Server instance. Later, we'll make the topology a little bit more complex by adding additional TiDB Server and pump nodes, and an additional drainer. This tutorial assumes you're using a modern Linux distribution on x86-64. I'll use a minimal CentOS 7 installation running in VMware for the examples. If you don't want to use local virtualization, you can easily and inexpensively start a CentOS 7 VM in your favorite cloud provider.

# Installation

We're using MariaDB Server in this case instead of MySQL Server because RHEL/CentOS 7 include MariaDB Server in their default package repositories. We'll need the client as well as the server for later, so let's install them now:

```
[kolbe@localhost ~]$ sudo yum install -y mariadb-server
```

Even if you've already started a TiDB Cluster, it might be easier to follow along with this tutorial if you set up a new, very simple cluster. The first step of that will be to download the latest TiDB Platform package: http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz. That package contains all the files we'll need to get started.

```
curl -LO http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
tar xf tidb-latest-linux-amd64.tar.gz
cd tidb-latest-linux-amd64
```


```
[kolbe@localhost ~]$ curl -LO http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  368M  100  368M    0     0  8394k      0  0:00:44  0:00:44 --:--:-- 11.1M
[kolbe@localhost ~]$ tar xf tidb-latest-linux-amd64.tar.gz
[kolbe@localhost ~]$ cd tidb-latest-linux-amd64
[kolbe@localhost tidb-latest-linux-amd64]$
```

# Configuration

Now we'll start a very simple TiDB Cluster, with a single instance each of `pd-server`, `tikv-server`, and `tidb-server`. First, let's populate the config files we'll use:
```
printf %s\\n 'log-file="pd.log"' 'data-dir="pd.data"' > pd.toml
printf %s\\n 'log-file="tikv.log"' '[storage]' 'data-dir="tikv.data"' '[pd]' 'endpoints=["127.0.0.1:2379"]' '[rocksdb]' max-open-files=1024 '[raftdb]' max-open-files=1024 > tikv.toml
printf %s\\n 'log-file="pump.log"' 'socket="/tmp/pump.sock"' 'data-dir="pump.data"' > pump.toml
printf %s\\n 'store="tikv"' 'path="127.0.0.1:2379"' '[log.file]' 'filename="tidb.log"' '[binlog]' 'enable=true' 'binlog-socket="/tmp/pump.sock"' > tidb.toml
printf %s\\n 'log-file="drainer.log"' '[syncer]' 'db-type="mysql"' '[syncer.to]' 'host="127.0.0.1"' 'user="root"' 'password=""' 'port=3306' > drainer.toml

```

```
$ for f in *.toml; do echo "$f:"; cat "$f"; echo; done
drainer.toml:
log-file="drainer.log"
[syncer]
db-type="mysql"
[syncer.to]
host="127.0.0.1"
user="root"
password=""
port=3306

pd.toml:
log-file="pd.log"
data-dir="pd.data"

pump.toml:
log-file="pump.log"
socket="/tmp/pump.sock"
data-dir="pump.data"

tidb.toml:
store="tikv"
path="127.0.0.1:2379"
[log.file]
filename="tidb.log"
[binlog]
enable=true
binlog-socket="/tmp/pump.sock"

tikv.toml:
log-file="tikv.log"
[storage]
data-dir="tikv.data"
[pd]
endpoints=["127.0.0.1:2379"]
[rocksdb]
max-open-files=1024
[raftdb]
max-open-files=1024
```

# Bootstrapping

Now we can start each component. This is best done in a specific order, first bringing up the PD (Placement Driver), then TiKV Server (the backend key/value store used by TiDB Platform), then pump (because TiDB must connect to the pump service to send the binary log), and finally TiDB Server (the frontend that receives SQL from applications). To give the services a little time to start up, well sleep for a few seconds between each.

```
./bin/pd-server --config=pd.toml &>pd.out &
sleep 3
./bin/tikv-server --config=tikv.toml &>tikv.out &
sleep 3
./bin/pump --config=pump.toml &>pump.out &
sleep 3
./bin/tidb-server --config=tidb.toml &>tidb.out &
```

```
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/pd-server --config=pd.toml &>pd.out &
[1] 20935
[kolbe@localhost tidb-latest-linux-amd64]$ sleep 3
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/tikv-server --config=tikv.toml &>tikv.out &
[2] 20944
[kolbe@localhost tidb-latest-linux-amd64]$ sleep 3
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/pump --config=pump.toml &>pump.out &
[3] 21050
[kolbe@localhost tidb-latest-linux-amd64]$ sleep 3
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/tidb-server --config=tidb.toml &>tidb.out &
[4] 21058
```

And if you execute `jobs`, you should see the list of running daemons:
```
[kolbe@localhost tidb-latest-linux-amd64]$$ jobs
[1]   Running                 ./bin/pd-server --config=pd.toml &>pd.out &
[2]   Running                 ./bin/tikv-server --config=tikv.toml &>tikv.out &
[3]-  Running                 ./bin/pump --config=pump.toml &>pump.out &
[4]+  Running                 ./bin/tidb-server --config=tidb.toml &>tidb.out &

```



# Connecting

You should have all 4 components of our TiDB Cluster running now, and you can now connect to the TiDB Server on port 4000 using the MariaDB/MySQL command-line client.

```
[kolbe@localhost tidb-latest-linux-amd64]$ mysql -h 127.0.0.1 -P 4000 -u root test
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.25-TiDB-v3.0.0-beta.1-94-g5a34c4b9d MySQL Community Server (Apache License 2.0)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [test]> select tidb_version()\G
*************************** 1. row ***************************
tidb_version(): Release Version: v3.0.0-beta.1-94-g5a34c4b9d
Git Commit Hash: 5a34c4b9d2e9aebb2ba132745af5634a52cdefe8
Git Branch: master
UTC Build Time: 2019-04-11 03:15:28
GoVersion: go version go1.12 linux/amd64
Race Enabled: false
TiKV Min Version: 2.1.0-alpha.1-ff3dd160846b7d1aed9079c389fc188f7f5ea13e
Check Table Before Drop: false
1 row in set (0.00 sec)
```

At this point we have a TiDB Cluster running, and we have `pump` reading binary logs from the cluster and storing them as relay logs in its data directory. The next pieces of the puzzle are to start a MariaDB server that `drainer` can write to. If you are using an operating system that makes it easier to install MySQL server, that's also OK -- just make sure it's listening on port 3306 and that you can either connect to it as user "root" with an empty password, or adjust drainer.toml as necessary.

```
[kolbe@localhost ~]$ mysql -h 127.0.0.1 -P 3306 -u root
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 20
Server version: 5.5.60-MariaDB MariaDB Server

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| test               |
| tidb_binlog        |
+--------------------+
5 rows in set (0.01 sec)
```

Here we can already see the `tidb_binlog` database, which contains the `checkpoint` table used by `drainer` to record up to what point binary logs from the TiDB Cluster have been applied.

```
MariaDB [tidb_binlog]> use tidb_binlog;
Database changed
MariaDB [tidb_binlog]> select * from checkpoint;
+---------------------+---------------------------------------------+
| clusterID           | checkPoint                                  |
+---------------------+---------------------------------------------+
| 6678715361817107733 | {"commitTS":407637466476445697,"ts-map":{}} |
+---------------------+---------------------------------------------+
1 row in set (0.00 sec)
```

Now, let's open another client to the TiDB Server, so that we can create a table and insert some rows into it. It's easiest to do this under GNU screen so you can keep multiple clients open at the same time.

```
mysql -h 127.0.0.1 -P 4000 --prompt='TiDB [\d]> ' -u root
TiDB [(none)]> create database tidbtest;
Query OK, 0 rows affected (0.12 sec)

TiDB [(none)]> use tidbtest;
Database changed
TiDB [tidbtest]> create table t1 (id int unsigned not null auto_increment primary key);
Query OK, 0 rows affected (0.11 sec)

TiDB [tidbtest]> insert into t1 () values (),(),(),(),();
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

Switching back to the MariaDB client, we should find the new database, new table, and the rows we've newly inserted:
```
MariaDB [(none)]> use tidbtest
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [tidbtest]> show tables;
+--------------------+
| Tables_in_tidbtest |
+--------------------+
| t1                 |
+--------------------+
1 row in set (0.00 sec)

MariaDB [tidbtest]> select * from t1;
+----+
| id |
+----+
|  1 |
|  2 |
|  3 |
|  4 |
|  5 |
+----+
5 rows in set (0.00 sec)
```

# binlogctl

There are a few extra pieces that are worth talking about. One is the `binlogctl` tool. For a full guide to the tool, see https://github.com/pingcap/docs/blob/master/tools/tidb-binlog-cluster.md#binlogctl-guide. Information about pumps and drainers that have joined the cluster is stored in pd, and the binlogctl tool is used to query and manipulate inforamtion about their states.

You can use `binlogctl` to get a view of the current status of pumps and drainers in the cluster:
```
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/binlogctl -cmd drainers
[2019/04/11 17:40:47.991 -04:00] [INFO] [nodes.go:47] ["query node"] [type=drainer] [node="{NodeID: localhost.localdomain:8249, Addr: 192.168.236.128:8249, State: offline, MaxCommitTS: 407638532237557761, UpdateTime: 2019-04-11 17:19:53 -0400 EDT}"]
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/binlogctl -cmd pumps
[2019/04/11 17:40:49.590 -04:00] [INFO] [nodes.go:47] ["query node"] [type=pump] [node="{NodeID: localhost.localdomain:8250, Addr: 192.168.236.128:8250, State: online, MaxCommitTS: 407638860495323137, UpdateTime: 2019-04-11 17:40:49 -0400 EDT}"]
```

```
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/binlogctl -cmd drainers
[2019/04/11 17:44:10.861 -04:00] [INFO] [nodes.go:47] ["query node"] [type=drainer] [node="{NodeID: localhost.localdomain:8249, Addr: 192.168.236.128:8249, State: online, MaxCommitTS: 407638907719778305, UpdateTime: 2019-04-11 17:44:10 -0400 EDT}"]
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/binlogctl -cmd pumps
[2019/04/11 17:44:13.904 -04:00] [INFO] [nodes.go:47] ["query node"] [type=pump] [node="{NodeID: localhost.localdomain:8250, Addr: 192.168.236.128:8250, State: online, MaxCommitTS: 407638914024079361, UpdateTime: 2019-04-11 17:44:13 -0400 EDT}"]
```

If I kill the drainer, the cluster puts it in the "paused" state, which means that the cluster expects it to rejoin.
```
[kolbe@localhost tidb-latest-linux-amd64]$ pkill drainer
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/binlogctl -cmd drainers
[2019/04/11 17:44:22.640 -04:00] [INFO] [nodes.go:47] ["query node"] [type=drainer] [node="{NodeID: localhost.localdomain:8249, Addr: 192.168.236.128:8249, State: paused, MaxCommitTS: 407638915597467649, UpdateTime: 2019-04-11 17:44:18 -0400 EDT}"]
```

You use "NodeIDs" with binlogctl to control individual nodes. In this case, the NodeID of the drainer is "localhost.localdomain:8249" and the NodeID of the puump is "localhost.localdomain:8250".

The main use of `binlogctl` in this tutorial is likely to be in the event of a cluster restart. If you end all processes in the TiDB cluster and try to restart them (but not the downstream MySQL/MariaDB server or the drainer), `pump` will believe that `drainer` is still "online" and will refuse to start, because it cannot contact `drainer`.

There are 3 solutions to that issue:

1. Stop drainer using `binlogctl` instead of killing the process: ```./bin/binlogctl --pd-urls=http://127.0.0.1:2379 --cmd=drainers
./bin/binlogctl --pd-urls=http://127.0.0.1:2379 --cmd=offline-drainer --node-id=localhost.localdomain:8249```
2. Start drainer _before_ starting pump.
3. Use `binlogctl` after starting pd (but before starting drainer or pump) to update the state of the paused drainer: `./bin/binlogctl --pd-urls=http://127.0.0.1:2379 --cmd=update-drainer --node-id=localhost.localdomain:8249 --state=offline`

