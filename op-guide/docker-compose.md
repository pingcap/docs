---
title: TiDB Docker Compose
category: deployment
---

# TiDB Docker Compose

## Use `docker-compose`

Note: If you are using `docker-compose`, you don't need to create a Docker network and start TiDB,TiKV and PD containers separately.
The following `docker-compose.yml` file is enough.

```yaml
version: '2'

services:
  pd1:
    image: pingcap/pd
    ports:
      - "2379"
      - "2380"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --name=pd1
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd1:2379
      - --advertise-peer-urls=http://pd1:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380

    privileged: true

  pd2:
    image: pingcap/pd
    ports:
      - "2379"
      - "2380"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --name=pd2
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd2:2379
      - --advertise-peer-urls=http://pd2:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380

    privileged: true

  pd3:
    image: pingcap/pd
    ports:
      - "2379"
      - "2380"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --name=pd3
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd3:2379
      - --advertise-peer-urls=http://pd3:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380

    privileged: true

  tikv1:
    image: pingcap/tikv
    ports:
      - "20160"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv1:20160
      - --data-dir=/var/tikv
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
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv2:20160
      - --data-dir=/var/tikv
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
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv3:20160
      - --data-dir=/var/tikv
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
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --store=tikv
      - --path=pd1:2379,pd2:2379,pd3:2379
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
