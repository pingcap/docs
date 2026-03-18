---
title: TiProxy Performance Test Report
summary: Learn the performance of TiProxy and the comparison with HAProxy.
---

# TiProxy Performance Test Report

This report tests the performance of TiProxy in the OLTP scenario of Sysbench and compares it with [HAProxy](https://www.haproxy.org/).

The results are as follows:

- The QPS upper limit of TiProxy is affected by the type of workload. When client concurrency is the same and the TiProxy CPU usage is below 80%, the QPS is less than 5% lower than that of HAProxy. In such cases, you can often increase the client concurrency to improve QPS. Under the same QPS, TiProxy's CPU usage is about 25% higher than HAProxy's. Therefore, you need to reserve more CPU resources.
- The number of TiDB server instances that TiProxy can hold varies according to the type of workload. Under the basic workloads of Sysbench, a TiProxy can hold 5 to 12 TiDB server instances of the same model.
- The row number of the query result set has a significant impact on the QPS of TiProxy, and the impact is the same as that of HAProxy.
- The performance of TiProxy increases almost linearly with the number of vCPUs. Therefore, increasing the number of vCPUs can effectively improve the QPS upper limit.
- The number of long connections and the frequency of creating short connections have minimal impact on the QPS of TiProxy.
- The higher the CPU usage of TiProxy, the greater the impact of enabling [traffic capture](/tiproxy/tiproxy-traffic-replay.md) on QPS. When the CPU usage of TiProxy is about 70%, enabling traffic capture leads to approximately 3% decrease in average QPS and 7% decrease in minimum QPS. The latter decrease is caused by periodic QPS drops during traffic file compression.

## Test environment

### Hardware configuration

| Service | Machine type | CPU model | Instance count |
| --- | --- | --- | --- |
| TiProxy | 4C8G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 1 |
| HAProxy | 4C8G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 1 |
| PD | 4C8G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 3 |
| TiDB | 8C16G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 8 |
| TiKV | 8C16G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 8 |
| Sysbench | 8C16G | Intel(R) Xeon(R) Silver 4214R CPU @ 2.40GHz | 1 |

### Software

| Service | Software version |
| --- | --- |
| TiProxy | v1.0.0 |
| HAProxy | 2.9.0 |
| PD | v8.0.0 |
| TiDB | v8.0.0 |
| TiKV | v8.0.0 |
| Sysbench | 1.0.17 |

### Configuration

#### TiProxy configuration

In the test, TLS is not enabled between the client and TiProxy, or between TiProxy and TiDB server.

```yaml
proxy.conn-buffer-size: 131072
```

#### HAProxy configuration - `haproxy.cfg` file

```yaml
global                                      # Global configuration.
    log         127.0.0.1 local2            # Specifies the global syslog server. You can define up to two.
    pidfile     /var/run/haproxy.pid        # Write the PID of the HAProxy process to pidfile.
    maxconn     4096                        # The maximum number of concurrent connections that a single HAProxy process can accept, equivalent to the command line parameter "-n".
    nbthread    4                           # The maximum number of threads. The upper limit of the number of threads is the same as the number of CPUs.
    user        haproxy                     # Same as UID parameter.
    group       haproxy                     # Same as GID parameter. A dedicated user group is recommended.
    daemon                                  # Run HAProxy as a daemon in the background, which is equivalent to the command line parameter "-D". You can also disable it with the "-db" parameter on the command line.
    stats socket /var/lib/haproxy/stats     # The location where the statistics are saved.

defaults                                    # Default configuration.
    log global                              # Inherit the settings of the global configuration section.
    retries 2                               # The maximum number of times to try to connect to the upstream server. If the number of retries exceeds this value, the backend server is considered unavailable.
    timeout connect  2s                     # The timeout period for HAProxy to connect to the backend server. If the server is located on the same LAN as HAProxy, set it to a shorter time.
    timeout client 30000s                   # The timeout period for the client to be inactive after the data transmission is completed.
    timeout server 30000s                   # The timeout period for the server to be inactive.

listen tidb-cluster                         # Configure database load balancing.
    bind 0.0.0.0:3390                       # Floating IP address and listening port.
    mode tcp                                # HAProxy uses layer 4, the transport layer.
    balance leastconn                      # The server with the least number of connections receives the connection first. `leastconn` is recommended for long session services, such as LDAP, SQL, and TSE, rather than short session protocols, such as HTTP. This algorithm is dynamic, and the server weight is adjusted during operation for slow-start servers.
    server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3      # Detects port 4000 at a frequency of once every 2000 milliseconds. If it is detected as successful twice, the server is considered available; if it is detected as failed three times, the server is considered unavailable.
    server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
    server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

## Basic workload test

### Test plan

This test aims to compare the QPS of TiProxy and HAProxy under four types of workloads: point select, read only, write only, and read write. Each type of workload is tested with different concurrency to compare the QPS of TiProxy and HAProxy.

The following command is used to perform the test:

```bash
sysbench $testname \
    --threads=$threads \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### Point Select

TiProxy test results:

| Threads | QPS     | Avg latency (ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU usage |
|---------|---------|------------------|------------------|-------------------|------------------------|
| 20      | 41273   | 0.48             | 0.64             | 190%              | 900%                   |
| 50      | 100255  | 0.50             | 0.62             | 330%              | 1900%                  |
| 100     | 137688  | 0.73             | 1.01             | 400%              | 2600%                  |

HAProxy test results:

| Threads | QPS    | Avg latency (ms) | P95 latency (ms) | HAProxy CPU usage | TiDB overall CPU usage |
|---------|--------|------------------|------------------|-------------------|------------------------|
| 20      | 44833  | 0.45             | 0.61             | 140%              | 1000%                  |
| 50      | 103631 | 0.48             | 0.61             | 270%              | 2100%                  |
| 100     | 163069 | 0.61             | 0.77             | 360%              | 3100%                  |

### Read Only

TiProxy test results:

| Threads | QPS    | Avg latency (ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU usage |
|---------|--------|------------------|------------------|-------------------|------------------------|
| 50      | 72076  | 11.09            | 12.75            | 290%              | 2500%                  |
| 100     | 109704 | 14.58            | 17.63            | 370%              | 3800%                  |
| 200     | 117519 | 27.21            | 32.53            | 400%              | 4100%                  |

HAProxy test results:

| Threads | QPS     | Avg latency (ms) | P95 latency (ms) | HAProxy CPU usage | TiDB overall CPU usage |
|---------|---------|------------------|------------------|-------------------|------------------------|
| 50      | 75760   | 10.56            | 12.08            | 250%              | 2600%                  |
| 100     | 121730  | 13.14            | 15.83            | 350%              | 4200%                  |
| 200     | 131712  | 24.27            | 30.26            | 370%              | 4500%                  |

### Write Only

TiProxy test results:

| Threads | QPS     | Avg latency (ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU usage |
|---------|---------|------------------|------------------|-------------------|------------------------|
| 100     | 81957   | 7.32             | 10.27            | 290%              | 3900%                  |
| 300     | 103040  | 17.45            | 31.37            | 330%              | 4700%                  |
| 500     | 104869  | 28.59            | 52.89            | 340%              | 4800%                  |

HAProxy test results:

| Threads | QPS     | Avg latency (ms) | P95 latency (ms) | HAProxy CPU usage | TiDB overall CPU usage |
|---------|---------|------------------|------------------|-------------------|------------------------|
| 100     | 81708   | 7.34             | 10.65            | 240%              | 3700%                  |
| 300     | 106008  | 16.95            | 31.37            | 320%              | 4800%                  |
| 500     | 122369  | 24.45            | 47.47            | 350%              | 5300%                  |

### Read Write

TiProxy test results:

| Threads | QPS    | Avg latency (ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU usage |
|---------|--------|------------------|------------------|-------------------|------------------------|
| 50      | 58571  | 17.07            | 19.65            | 250%              | 2600%                  |
| 100     | 88432  | 22.60            | 29.19            | 330%              | 3900%                  |
| 200     | 108758 | 36.73            | 51.94            | 380%              | 4800%                  |

HAProxy test results:

| Threads | QPS     | Avg latency (ms) | P95 latency (ms) | HAProxy CPU usage | TiDB overall CPU usage |
|---------|---------|------------------|------------------|-------------------|------------------------|
| 50      | 61226   | 16.33            | 19.65            | 190%              | 2800%                  |
| 100     | 96569   | 20.70            | 26.68            | 290%              | 4100%                  |
| 200     | 120163  | 31.28            | 49.21            | 340%              | 5200%                  |

## Result set test

### Test plan

This test aims to compare the performance of TiProxy and HAProxy under different result set row numbers. This test uses 100 concurrency, and compares the QPS of TiProxy and HAProxy with result set row numbers of 10, 100, 1000, and 10000.

The following command is used to perform the test:

```bash
sysbench oltp_read_only \
    --threads=100 \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    --skip_trx=true \
    --point_selects=0 \
    --sum_ranges=0 \
    --order_ranges=0 \
    --distinct_ranges=0 \
    --simple_ranges=1 \
    --range_size=$range_size
    run --tables=32 --table-size=1000000
```

### Test results

TiProxy test results:

| Range size | QPS     | Avg latency (ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU usage | Inbound network (MiB/s) | Outbound network (MiB/s) |
|------------|---------|------------------|------------------|-------------------|------------------------|-------------------------|--------------------------|
| 10         | 80157   | 1.25             | 1.61             | 340%              | 2600%                  | 140                     | 140                      |
| 100        | 55936   | 1.79             | 2.43             | 370%              | 2800%                  | 820                     | 820                      |
| 1000       | 10313   | 9.69             | 13.70            | 310%              | 1500%                  | 1370                    | 1370                     |
| 10000      | 1064    | 93.88            | 142.39           | 250%              | 600%                   | 1430                    | 1430                     |

HAProxy test results:

| Range size | QPS    | Avg latency (ms) | P95 latency (ms) | HAProxy CPU usage | TiDB overall CPU usage | Inbound network (MiB/s) | Outbound network (MiB/s) |
|------------|--------|------------------|------------------|-------------------|------------------------|-------------------------|--------------------------|
| 10         | 94376  | 1.06             | 1.30             | 250%              | 4000%                  | 150                     | 150                      |
| 100        | 70129  | 1.42             | 1.76             | 270%              | 3300%                  | 890                     | 890                      |
| 1000       | 9501   | 11.18            | 14.73            | 240%              | 1500%                  | 1180                    | 1180                     |
| 10000      | 955    | 104.61           | 320.17           | 180%              | 1200%                  | 1200                    | 1200                     |

## Scalability test

### Test plan

This test aims to verify that the performance of TiProxy is proportional to its specifications, to ensure that upgrading the specifications of TiProxy can improve its QPS upper limit. This test uses TiProxy instances with different vCPU numbers and concurrency to compare the QPS.

The following command is used to perform the test:

```bash
sysbench oltp_point_select \
    --threads=$threads \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### Test results

| vCPU | Threads | QPS     | Avg latency (ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU usage |
|------|---------|---------|------------------|------------------|-------------------|------------------------|
| 2    | 40      | 58508   | 0.68             | 0.97             | 190%              | 1200%                  |
| 4    | 80      | 104890  | 0.76             | 1.16             | 390%              | 2000%                  |
| 6    | 120     | 155520  | 0.77             | 1.14             | 590%              | 2900%                  |
| 8    | 160     | 202134  | 0.79             | 1.18             | 800%              | 3900%                  |

## Long connection test

### Test plan

This test aims to verify that a large number of idle connections have minimal impact on the QPS when the client uses long connections. This test creates 5000, 10000, and 15000 idle long connections, and then executes `sysbench`.

This test uses the default value for the `conn-buffer-size` configuration:

```yaml
proxy.conn-buffer-size: 32768
```

Use the following command to perform the test:

```bash
sysbench oltp_point_select \
    --threads=50 \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### Test results

| Connection count | QPS   | Avg latency (ms) | P95 latency (ms) | TiProxy CPU usage | TiProxy memory usage (MB) | TiDB overall CPU usage |
|------------------|-------|------------------|------------------|-------------------|---------------------------|------------------------|
| 5000             | 96620 | 0.52             | 0.64             | 330%              | 920                       | 1800%                  |
| 10000            | 96143 | 0.52             | 0.65             | 330%              | 1710                      | 1800%                  |
| 15000            | 96048 | 0.52             | 0.65             | 330%              | 2570                      | 1900%                  |

## Short connection test

### Test plan

This test aims to verify that frequent creation and destruction of connections have minimal impact on the QPS when the client uses short connections. This test starts another client program to create and disconnect 100, 200, and 300 short connections per second while executing `sysbench`.

Use the following command to perform the test:

```bash
sysbench oltp_point_select \
    --threads=50 \
    --time=1200 \
    --report-interval=10 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### Test results

| New connections per second | QPS    | Avg latency (ms) | P95 latency (ms) | TiProxy CPU usage | TiDB overall CPU usage |
|----------------------------|--------|------------------|------------------|-------------------|------------------------|
| 100                        | 95597  | 0.52             | 0.65             | 330%              | 1800%                  |
| 200                        | 94692  | 0.53             | 0.67             | 330%              | 1800%                  |
| 300                        | 94102  | 0.53             | 0.68             | 330%              | 1900%                  |

## Traffic capture test

### Test plan

This test aims to evaluate the performance impact of [traffic capture](/tiproxy/tiproxy-traffic-replay.md) on TiProxy. It uses TiProxy v1.3.0 and compares QPS and TiProxy CPU usage with traffic capture enabled and disabled before executing `sysbench` with different concurrency. Due to periodic QPS fluctuations caused by traffic file compression, the test compares both the average and minimum QPS.

Use the following command to perform the test:

```bash
sysbench oltp_read_write \
    --threads=$threads \
    --time=1200 \
    --report-interval=5 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$host \
    --mysql-port=$port \
    run --tables=32 --table-size=1000000
```

### Test results

| Connection count | Traffic capture | Avg QPS | Min QPS | Avg latency (ms) | P95 latency (ms) | TiProxy CPU usage |
| - |-----| --- | --- |-----------|-------------|-----------------|
| 20 | Disabled | 27653 | 26999 | 14.46     | 16.12       | 140% |
| 20 | Enabled | 27519 | 26922 | 14.53     | 16.41       | 170% |
| 50 | Disabled | 58014 | 56416 | 17.23     | 20.74       | 270% |
| 50 | Enabled | 56211 | 52236 | 17.79     | 21.89       | 280% |
| 100 | Disabled | 85107 | 84369 | 23.48     | 30.26       | 370% |
| 100 | Enabled | 79819 | 69503 | 25.04     | 31.94       | 380% |