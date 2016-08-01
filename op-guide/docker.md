# Run a TiDB Cluster in Docker on a Single Host

## Preparation

Before you start, make sure that:

+ Installed the latest version of [Docker](https://www.docker.com/products/docker) 
+ Pulled the TiDB/TiKV/PD docker images from PingCAP's Docker Hub repositories
`docker pull pingcap/tidb:latest`
`docker pull pingcap/tikv:latest`
`docker pull pingcap/pd:latest`

## Create a docker bridge network

```bash
net="isolated_nw"
docker network rm ${net}
docker network create --driver bridge ${net} 
```

After creating a docker network, we will make all the TiDB containers added to it, which composed a standalone cluster.
The service in cluster can communicate with each other using the name instead of IP addresss.
In addition, you can replace the network name above with any you like.

## Using `Busybox` container as storage volume

```bash
docker run -d --name ti-storage \
  -v /tidata \
  busybox
```

## Start PD service

First we start up 3 pd-servers, respectively named as **pd1**, **pd2**, **pd3**.

**pd1:** 

```bash
docker run --net ${net} -d --name pd1 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd1" \
  --data-dir="/tidata/pd1" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd1:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd1:2380" \
  --initial-cluster="pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="pd1:1234"
```

**pd2:**

```bash
docker run --net ${net} -d --name pd2 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd2" \
  --data-dir="/tidata/pd2" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd2:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd2:2380" \
  --initial-cluster="pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="pd2:1234"
```

**pd3:**

```bash
docker run --net ${net} -d --name pd3 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd3" \
  --data-dir="/tidata/pd3" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd3:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd3:2380" \
  --initial-cluster="pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="pd3:1234"
```

After that, if you need to add **pd4** into the existing cluster, just use `--join` flag, and specify any one of the available **advertise-client-urls** above.
Notice that the **advertise-client-urls** is needed here, not **advertise-peer-urls**.

**pd4:**

```bash
docker run --net ${net} -d --name pd4 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd4" \
  --data-dir="/tidata/pd4" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd4:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd4:2380" \
  --join="http://pd1:2379" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="pd4:1234"
```

## Start TiKV service

Next you can run any number of TiKV instances, which is the underlying distributed storage.

**tikv1:**

```bash
docker run --net ${net} -d --name tikv1 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="tikv1:20160" \
  --store="/tidata/tikv1" \
  --dsn=raftkv \
  --pd="pd1:2379,pd2:2379,pd3:2379" \
  --cluster-id=1
```

**tikv2:**

```bash
docker run --net ${net} -d --name tikv2 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="tikv2:20160" \
  --store="/tidata/tikv2" \
  --dsn=raftkv \
  --pd="pd1:2379,pd2:2379,pd3:2379" \
  --cluster-id=1
```

**tikv3:**

```bash
docker run --net ${net} -d --name tikv3 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="tikv3:20160" \
  --store="/tidata/tikv3" \
  --dsn=raftkv \
  --pd="pd1:2379,pd2:2379,pd3:2379" \
  --cluster-id=1
```

## Start TiDB service

The **tidb-server** as the SQL Layer is stateless, and accept client connections from users.
Using `-p 4000:4000` to expose port of 4000 to the host server.

```bash
docker run --net ${net} -d --name tidb \
  -p 4000:4000 \
  -v /etc/localtime:/etc/localtime:ro \
  pingcap/tidb \
  --store=tikv \
  --path="pd1:2379,pd2:2379,pd3:2379?cluster=1" \
  -L warn
```

## Use SQL client
After you started a TiDB cluster, you can use official mysql client connecting to TiDB for a test immediately.

```bash
mysql -h 127.0.0.1 -P 4000 -u root -D test
```

## In another way, using `docker-compose`

A simple `docker-compose.yml`:

```bash
version: '2'

services:
  pd1:
    image: pingcap/pd
    ports:
      - "1234"
      - "9090"
      - "2379"
      - "2380"

    command:
      - --cluster-id=1 
      - --name=pd1 
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd1:2379
      - --advertise-peer-urls=http://pd1:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380
      - --addr=0.0.0.0:1234
      - --advertise-addr=pd1:1234
      
    privileged: true

  pd2:
    image: pingcap/pd
    ports:
      - "1234"
      - "9090"
      - "2379"
      - "2380"

    command:
      - --cluster-id=1 
      - --name=pd2 
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd2:2379
      - --advertise-peer-urls=http://pd2:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380
      - --addr=0.0.0.0:1234
      - --advertise-addr=pd2:1234
      
    privileged: true

  pd3:
    image: pingcap/pd
    ports:
      - "1234"
      - "9090"
      - "2379"
      - "2380"

    command:
      - --cluster-id=1 
      - --name=pd3 
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd3:2379
      - --advertise-peer-urls=http://pd3:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380 
      - --addr=0.0.0.0:1234
      - --advertise-addr=pd3:1234
      
    privileged: true

  tikv1:
    image: pingcap/tikv
    ports:
      - "20160"

    command:
      - --cluster-id=1
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv1:20160
      - --dsn=raftkv
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tikv2:
    image: pingcap/tikv
    ports:
      - "20160"

    command:
      - --cluster-id=1
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv2:20160
      - --dsn=raftkv
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tikv3:
    image: pingcap/tikv
    ports:
      - "20160"

    command:
      - --cluster-id=1
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv3:20160
      - --dsn=raftkv
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tidb:
    image: pingcap/tidb
    ports:
      - "4000"
      - "10080"

    command:
      - --store=tikv 
      - --path=pd1:2379,pd2:2379,pd3:2379?cluster=1
      - -L=warn

    depends_on:
      - "tikv1"
      - "tikv2"
      - "tikv3"

    privileged: true
```

+ Use `docker-compose up -d` to create and start the cluster. 
+ Use `docker-compose port tidb 4000` to print the TiDB public port. For example, if the output is `0.0.0.0:32966`, the TiDB public port is `32966`.
+ Use `mysql -h 127.0.0.1 -P 32966 -u root -D test` to connect to TiDB and enjoy it. 
+ Use `docker-compose down` to stop and remove the cluster.

