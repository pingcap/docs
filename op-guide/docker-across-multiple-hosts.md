# Run TiDB in Docker across Multiple Hosts

This page shows you a example of manually deploying a TiDB cluster using docker on multiple machines.


## Preparation
Assume we have 3 machines with the following details:

|Name|Host IP|
|----|-------|
|**host1**|192.168.1.100|
|**host2**|192.168.1.101|
|**host3**|192.168.1.102|

Every host has already installed newest version docker, and pulled the latest docker images of TiDB/TiKV/PD.

## Start `busybox` container as storage volume for each host

Run this command on **host1**, **host2**, **host3** respectively:

```bash
export host1=192.168.1.100
export host2=192.168.1.101
export host3=192.168.1.102

docker run -d --name ti-storage \
  -v /tidata \
  busybox
```

## Start PD on every host

**host1:**
```bash
docker run -d --name pd1 \
  -p 1234:1234 \
  -p 9090:9090 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd1" \
  --data-dir="/tidata/pd1" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://${host1}:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://${host1}:2380" \
  --initial-cluster="pd1=http://${host1}:2380,pd2=http://${host2}:2380,pd3=http://${host3}:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="${host1}:1234"
```

**host2:**
```bash
docker run -d --name pd2 \
  -p 1234:1234 \
  -p 9090:9090 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd2" \
  --data-dir="/tidata/pd2" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://${host2}:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://${host2}:2380" \
  --initial-cluster="pd1=http://${host1}:2380,pd2=http://${host2}:2380,pd3=http://${host3}:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="${host2}:1234"
```

**host3:**
```bash
docker run -d --name pd3 \
  -p 1234:1234 \
  -p 9090:9090 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /usr/share/ca­certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd3" \
  --data-dir="/tidata/pd3" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://${host3}:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://${host3}:2380" \
  --initial-cluster="pd1=http://${host1}:2380,pd2=http://${host2}:2380,pd3=http://${host3}:2380" \
  --addr="0.0.0.0:1234" \
  --advertise-addr="${host3}:1234"
```

## Start TiKV on every host

**host1:**
```bash
docker run -d --name tikv1 \
  -p 20160:20160
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="${host1}:20160" \
  --store="/tidata/tikv1" \
  --dsn=raftkv \
  --pd="${host1}:2379,${host2}:2379,${host3}:2379" \
  --cluster-id=1
```

**host2:**
```bash
docker run -d --name tikv2 \
  -p 20160:20160
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="${host2}:20160" \
  --store="/tidata/tikv2" \
  --dsn=raftkv \
  --pd="${host1}:2379,${host2}:2379,${host3}:2379" \
  --cluster-id=1
```

**host3:**
```bash
docker run -d --name tikv3 \
  -p 20160:20160
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="${host3}:20160" \
  --store="/tidata/tikv3" \
  --dsn=raftkv \
  --pd="${host1}:2379,${host2}:2379,${host3}:2379" \
  --cluster-id=1
```

## Start TiDB on any one host

```bash
docker run -d --name tidb \
  -p 4000:4000 \
  -p 10080:10080 \
  -v /etc/localtime:/etc/localtime:ro \
  pingcap/tidb \
  --store=tikv \
  --path="${host1}:2379,${host2}:2379,${host3}:2379?cluster=1" \
  -L warn
```

## Use the official mysql client to connect to TiDB and enjoy it.

```bash
mysql -h ${host1} -P 4000 -u root -D test
```
