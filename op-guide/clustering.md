# Clustering

## Overview

A TiDB cluster contains PD, TiKV, TiDB. The start-up sequence is PD -> TiKV -> TiDB.

## A standalone cluster

1. Start PD.
    ```bash
    pd-server --cluster-id=1 \
              --host=127.0.0.1 \
              --data-dir=pd 
    ```
2. Start TiKV.
    ```bash
    tikv-server -I 1 \
                -S raftkv \
                --addr 127.0.0.1:20160 \
                --pd 127.0.0.1:2379 \
                -S tikv 
    ```

3. Start TiDB.
    ```bash
    tidb-server --store=tikv \
                --path="127.0.0.1:2379/pd?cluster=1"
                -P 5001
    ```

4. Use the official `mysql` client to connect to TiDB and enjoy it. 

    ```sh
    mysql -h 127.0.0.1 -P 5001 -u root -D test
    ```

## A 3-nodes multi-machine cluster

Assume we have three machines with the following details:

|Name|Address|
|----|-------|
|node1|192.168.199.113|
|node2|192.168.199.114|
|node3|192.168.199.115|

In every node, we will run one PD and one TiKV. We will run one TiDB in node1. 

1. Start PDs.

    ```bash
    pd-server --host=192.168.199.113 \
              --cluster-id=1 \
              --name=pd1 \
              --data-dir=pd1 \
              --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
              
    pd-server --host=192.168.199.114 \
              --cluster-id=1 \
              --name=pd2 \
              --data-dir=pd2 \
              --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
              
    pd-server --host=192.168.199.115 \
              --cluster-id=1 \
              --name=pd3 \
              --data-dir=pd3 \
              --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
    ```

2. Start TiKVs.

    ```bash
    tikv-server -S raftkv \
                -I 1 \
                --pd 192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379 \
                -A 192.168.199.113:20160 \
                -s tikv1
    
    tikv-server -S raftkv \
                -I 1 \
                --pd 192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379 \
                -A 192.168.199.114:20160 \
                -s tikv2
                
    tikv-server -S raftkv \
                -I 1 \
                --pd 192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379 \
                -A 192.168.199.115:20160 \
                -s tikv3
    ```

3. Start TiDB.

    ```bash
    tidb-server --store=tikv \
                --path="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379/pd?cluster=1" 
    ```

4. Use the official `mysql` client to connect to TiDB and enjoy it. 

    ```sh
    mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```

## A local cluster with `docker-compose`

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
      - --host=pd1 
      - --name=pd1 
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380

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
      - --host=pd2
      - --name=pd2 
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380

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
      - --host=pd3
      - --name=pd3 
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380 

    privileged: true

  tikv1:
    image: pingcap/tikv
    ports:
      - "20160"

    command:
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv1:20160
      - --cluster-id=1
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
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv2:20160
      - --cluster-id=1
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
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv3:20160
      - --cluster-id=1
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

    command:
      - --store=tikv 
      - --path=pd1:2379,pd2:2379,pd3:2379/pd?cluster=1
      - -L=warn

    depends_on:
      - "tikv1"
      - "tikv2"
      - "tikv3"

    privileged: true
```

+ Use `docker-compose up -d` to create and start the cluster. 
+ Use `docker-compose port tidb 4000` to print the TiDB host port. For example, if the output is `0.0.0.0:32966`, the TiDB host port is `32966`.
+ Use `mysql -h 127.0.0.1 -P 32966 -u root -D test` to connect to TiDB and enjoy it. 
+ Use `docker-compose down` to stop and remove the cluster.