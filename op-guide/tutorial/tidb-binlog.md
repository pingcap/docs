https://pingcap.com/docs/tools/tidb-binlog-cluster/

TiDB Binlog is a stack of components that form a solution to push incremental updates to a TiDB Server cluster into any of a variety of downstream platforms. TiDB Binlog is distributed as a part of TiDB Enterprise Tools.

TiDB Binlog comprises two components: the *pump* and the *drainer*. Several pump nodes make up a pump cluster. Each pump node connects to TiDB Server instances and receives updates made to each of the TiDB Server instances in a cluster. A drainer connects to the pump cluster and transforms updates into the correct format for a particular downstream destination, be if Kafka or another TiDB Cluster or a MySQL/MariaDB server. 

The clustered architecture of the pump component ensures that updates won't be lost as new TiDB Server instances join or leave the TiDB Cluster or pump nodes join or leave the pump cluster.

This tutorial will start with a very simple TiDB Binlog deployment with a single node of each component (PD, TiKV Server, TiDB Server, pump, and drainer), set up to push data into a MariaDB Server instance. Later, we'll make the topology a little bit more complex by adding additional TiDB Server and pump nodes, and an additional drainer. This tutorial assumes you're using a modern Linux distribution on x86-64. I'll use a minimal CentOS 7 installation running in VMware for the examples.

We're using MariaDB Server in this case instead of MySQL Server because RHEL/CentOS 7 include MariaDB Server in their default package repositories. We'll need the client as well as the server for later, so let's install them now:

```
[kolbe@localhost ~]$ sudo yum install -y mariadb-server
```

Even if you've already started a TiDB Cluster, it might be easier to follow along with this tutorial if you set up a new, very simple cluster. The first step of that will be to download the latest TiDB Platform package: http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz. That package contains all the files we'll need to get started.

```
[kolbe@localhost ~]$ curl -LO http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  368M  100  368M    0     0  8394k      0  0:00:44  0:00:44 --:--:-- 11.1M
[kolbe@localhost ~]$ tar xf tidb-latest-linux-amd64.tar.gz
[kolbe@localhost ~]$ cd tidb-latest-linux-amd64
[kolbe@localhost tidb-latest-linux-amd64]$
```

Now we'll start a very simple TiDB Cluster, with a single instance each of `pd-server`, `tikv-server`, and `tidb-server`:

```
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/pd-server --log-file=pd.log --data-dir=pd.data &
[1] 7831
[kolbe@localhost tidb-latest-linux-amd64]$ printf %s\\n '[rocksdb]' max-open-files=1024 '[raftdb]' max-open-files=1024 > tikv.toml
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/tikv-server --log-file=tikv.log --data-dir=tikv.data --pd-endpoints=127.0.0.1:2379 --config=tikv.toml &
[2] 7873
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/pump --log-file=pump.log --data-dir=pump.data --socket=/tmp/pump.sock &
[3] 8019
[kolbe@localhost tidb-latest-linux-amd64]$ printf %s\\n 'store="tikv"' 'path="127.0.0.1:2379"' '[binlog]' 'enable=true' 'binlog-socket="/tmp/pump.sock"' > tidb.toml
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/tidb-server --log-file=tidb.log --config=tidb.toml &
[4] 8028
```

First, set up the config files we'll use:

```
printf %s\\n 'log-file="pd.log"' 'data-dir="pd.data"' > pd.toml
printf %s\\n 'log-file="tikv.log"' '[storage]' 'data-dir="tikv.data"' '[pd]' 'endpoints=["127.0.0.1:2379"]' '[rocksdb]' max-open-files=1024 '[raftdb]' max-open-files=1024 > tikv.toml
printf %s\\n 'log-file="pump.log"' 'socket="/tmp/pump.sock"' 'data-dir="pump.data"' > pump.toml
printf %s\\n 'store="tikv"' 'path="127.0.0.1:2379"' '[log.file]' 'filename="tidb.log"' '[binlog]' 'enable=true' 'binlog-socket="/tmp/pump.sock"' > tidb.toml
```

```
$ for f in \*.toml; do echo "$f:"; cat "$f"; echo; done
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

```
[1]   Running                 ./bin/pd-server --config=pd.toml &\>pd.out &
[2]   Running                 ./bin/tikv-server --config=tikv.toml &\>tikv.out &
[4]-  Running                 ./bin/pump --config=pump.toml &\>pump.out &
[5]+  Running                 ./bin/tidb-server --config=tidb.toml &\>tidb.out &
```

```
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/pd-server --log-file=pd.log --data-dir=pd.data &>pd.out &
[1] 8202
[kolbe@localhost tidb-latest-linux-amd64]$ printf %s\\n '[rocksdb]' max-open-files=1024 '[raftdb]' max-open-files=1024 > tikv.toml
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/tikv-server --log-file=tikv.log --data-dir=tikv.data --pd-endpoints=127.0.0.1:2379 --config=tikv.toml &>tikv.out &
[2] 8210
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/pump --log-file=pump.log --data-dir=pump.data --socket=/tmp/pump.sock &>pump.out &
[3] 8315
[kolbe@localhost tidb-latest-linux-amd64]$ printf %s\\n 'store="tikv"' 'path="127.0.0.1:2379"' '[binlog]' 'enable=true' 'binlog-socket="/tmp/pump.sock"' > tidb.toml
[kolbe@localhost tidb-latest-linux-amd64]$ ./bin/tidb-server --log-file=tidb.log --config=tidb.toml &>tidb.out &
[4] 8347
[kolbe@localhost tidb-latest-linux-amd64]$ jobs
[1]   Running                 ./bin/pd-server --log-file=pd.log --data-dir=pd.data &>pd.out &
[2]   Running                 ./bin/tikv-server --log-file=tikv.log --data-dir=tikv.data --pd-endpoints=127.0.0.1:2379 --config=tikv.toml &>tikv.out &
[3]-  Running                 ./bin/pump --log-file=pump.log --data-dir=pump.data --socket=/tmp/pump.sock &>pump.out &
[4]+  Running                 ./bin/tidb-server --log-file=tidb.log --config=tidb.toml &>tidb.out &
```

You should see all 4 components of our TiDB Cluster running now, and you can now connect to the TiDB Server on port 4000 using the MariaDB/MySQL command-line client.

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

```
[kolbe@localhost tidb-latest-linux-amd64]$ sudo systemctl start mariadb
[kolbe@localhost tidb-latest-linux-amd64]$ mysql
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 3
Server version: 5.5.60-MariaDB MariaDB Server

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> select version();
+----------------+
| version()      |
+----------------+
| 5.5.60-MariaDB |
+----------------+
1 row in set (0.00 sec)
```
