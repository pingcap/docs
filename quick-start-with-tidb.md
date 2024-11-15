---
title: Quick Start with TiDB Self-Managed
summary: Learn how to quickly get started with TiDB Self-Managed using TiUP playground and see if TiDB is the right choice for you.
aliases: ['/docs/dev/quick-start-with-tidb/','/docs/dev/test-deployment-using-docker/']
---

# Quick Start with TiDB Self-Managed

This guide provides the quickest way to get started with TiDB Self-Managed, walking you through setting up a local TiDB cluster for development and testing.

TiDB is a distributed SQL database built for both transactional and analytical workloads. Key features:

- MySQL compatible
- Horizontally scalable
- Real-time HTAP (Hybrid Transactional and Analytical Processing)
- Cloud-native architecture

> **Note:**
>
> - This deployment method is for development and testing only.
> - For the fastest way to get started, try [TiDB Cloud Serverless](https://tidbcloud.com/free-trial) - our fully managed service with a free tier.
> - For production deployments, see [Deploy a TiDB Cluster Using TiUP](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) or [Deploy a TiDB Cluster on Kubernetes](https://docs.pingcap.com/tidb/stable/tidb-in-kubernetes).

## Set up your environment

First, install TiUP, the package manager for TiDB:

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

The install script added `tiup` to your shell path. Open a new terminal or reload the shell profile:

<SimpleTab>
<div label="macOS">

For macOS:
```shell
source ~/.zshrc
```

</div>

<div label="Linux">

For Linux:

```shell
source ~/.bash_profile
```

</div>

## Start your database

Launch a local TiDB cluster with one command:

```shell
tiup playground
```

TiUP will automatically download the necessary binaries. Wait for the success message:

```log
TiDB Playground Cluster is started, enjoy!
```

Congratulations! You're running a distributed SQL database.

To proceed with the next steps, open another terminal and keep `tiup` running.

## Connect to TiDB

You can connect to TiDB using either the built-in TiUP client or any MySQL-compatible client.

### Using TiUP client

The TiUP client gives you a convenient way to interact with TiDB via the command line.

```shell
tiup client
```

Select the endpoint to connect, and try your first commands:

```sql
CREATE DATABASE hello;
USE hello;

CREATE TABLE hello_tidb (
     id   INT,
     name VARCHAR(50)
  );

INSERT INTO hello_tidb VALUES
    (1, 'Hello World');

SELECT * FROM hello_tidb;
```

You should see this output:

```
SELECT * FROM hello_tidb;
+----+-------------+
| id | name        |
+----+-------------+
|  1 | Hello World |
+----+-------------+
(1 row)
```

To exit the client, type `exit` or simply `\q`.

### Using standard MySQL client

You can install the standard MySQL client with:

<SimpleTab>
<div label="macOS">

macOS:
{{< copyable "sql-regular" >}}
```shell
brew install mysql-client
```

</div>

<div label="Linux">

Linux (Debian/Ubuntu):

```shell
sudo apt install mysql-client
```

Linux (RHEL/CentOS):

```shell
sudo yum install mysql
```
</div>

Check if the MySQL client is installed:

```shell
mysql --version
```

You should see an output indicating the MySQL client version number.

If you already have the MySQL client installed, you can connect to TiDB with:


```shell
mysql --host 127.0.0.1 --port 4000 -u root
```

## Understanding what just happened

You just started to use a fully functional distributed database cluster with:

- **TiDB Server:** SQL layer that processes queries and speaks MySQL protocol
- **TiKV:** Distributed storage layer that replicates data automatically and handles transactions across nodes
- **PD (Placement Driver):** Cluster orchestrator that works behind the scenes to coordinate TiDB, TiKV, and TiFlash components, managing cluster metadata and ensuring data is distributed optimally

Additionally, `tiup playground` installed optional components:

- **TiFlash:** Real-time analytics engine that accelerates complex queries and reporting without slowing down your live application
- Built-in **monitoring stack** with:
  - TiDB Dashboard (default: http://127.0.0.1:2379/dashboard, user: `root`, no password)
  - Grafana + Prometheus (default: http://127.0.0.1:3000, user: `admin`, password: `admin`)

You can verify your running database cluster components with:

```shell
tiup playground display
```

## Developer workflow

The previous steps gave you an ephemeral environment - perfect for first experiments but everything is lost when you stop the playground. Let's set up a more suitable environment for development.

### Persistent playground environments

Create a tagged playground that persists data between restarts:

```shell
tiup playground --tag dev-env
```

The `--tag` flag preserves your data after the playground environment restarts, and lets you run multiple environments using different tags (e.g., `dev-env`, `sample-app-env`).

Tags also makes cleanup explicit with:

```shell
tiup clean dev-env
```

### Customize your cluster

You can also use playground options to specify different TiDB versions, or components that better meet your development and testing goals. For example, to start a local environment with version 8.1.0, 2 TiDB servers, 3 TiKV, 1 PD, and no TiFlash with:

```shell
tiup playground v8.1.0 --tag sample-app-env --db 2 --kv 3 --pd 1 --tiflash 0
```

TiUP will download the necessary binaries for the specified version and start the cluster components for you.

### Manage your playground environments

You can list all your playground environments with:

```shell
tiup status
```

You will see an output similar to this:

```log
Name            Component  PID    Status  ... Args
sample-app-env  playground 30661  RUNNING ... tiup-playground v8.1.0 --tag sample-app-env --db 2 --kv 3 --pd 1 --tiflash 0
```

If you stop a tagged playground cluster by pressing <kbd>Ctrl+C</kbd> in the terminal where you started it, you can start it again without losing data.

To restart the environment, you can run `tiup playground` with the same arguments as in the `tiup status` output, as seen in the output above, or you can change them. This means that you have the flexibility to add and remove cluster components.

To add a TiProxy instance as a load balancer to your existing `sample-app-env` environment with:


```shell
tiup playground v8.1.0 --tag sample-app-env --db 2 --kv 3 --pd 1 --tiflash 0 --tiproxy 1
```

You should see the cluster starting normally, with an output like this:

```log
TiDB Playground Cluster is started, enjoy!
Connect TiDB: mysql --host 127.0.0.1 --port 4001 -u root
Connect TiDB: mysql --host 127.0.0.1 --port 4000 -u root
Connect TiProxy: mysql --host 127.0.0.1 --port 6000 -u root
```

Now you can connect through TiProxy:


```shell
mysql --host 127.0.0.1 --port 6000 -u root
```

See all TiUP playground options with:


```shell
tiup playground --help
```

Common options:

- `--*.host`: Bind to specific network interface
- `--*.port`: Change default ports
- `--without-monitor`: Start without monitoring stack

> **Tip:**
>
> Create different tagged environments for different projects or testing scenarios.

## Sample scalable database application

Let's create a simple weather monitoring system that stores data from weather stations worldwide.

### Create the schema

```sql
-- Create the schema/database for the weather monitoring app
CREATE DATABASE sample_weather;
USE sample_weather;

CREATE TABLE stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    latitude DECIMAL(8,6),
    longitude DECIMAL(9,6)
);

CREATE TABLE readings (
    station_id INT,
    temperature DECIMAL(4,1), -- in Celsius
    humidity INT, -- percentage
    pressure INT, -- in hPa
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_station_time(station_id, recorded_at)
);
```

### Create sample data

Generate sample data using the following script:

```sql
-- Insert some weather stations from different cities
INSERT INTO stations (name, location, latitude, longitude) VALUES
    ('Sydney Harbor', 'Sydney, Australia', -33.8688, 151.2093),
    ('Shibuya Weather', 'Tokyo, Japan', 35.6595, 139.7006),
    ('Beijing Station', 'Beijing, China', 39.9040, 116.4275),
    ('Singapore Central', 'Singapore', 1.3521, 103.8198),
    ('Mumbai Central', 'Mumbai, India', 18.9710, 72.8194),
    ('Cairo Station', 'Cairo, Egypt', 30.0629, 31.2474),
    ('Berlin Central', 'Berlin, Germany', 52.5251, 13.3694),
    ('London City', 'London, UK', 51.5074, -0.1278),
    ('Sao Paulo Central', 'Sao Paulo, Brazil', -23.5505, -46.6333),
    ('Central Park', 'New York, USA', 40.7829, -73.9654);
```

### Generate sample workload

Open two new terminal windows to generate write and read workloads through TiProxy.

Terminal 1: Write Workload

Run this command to continuously insert weather readings:

```shell
while true; do
    mysql -h 127.0.0.1 -P 6000 -u root -D sample_weather -vv -e "INSERT INTO readings
    (station_id, temperature, humidity, pressure) SELECT id as station_id, ROUND(10 + (RAND() *
    30), 1), ROUND(40 + (RAND() * 60)), ROUND(980 + (RAND() * 40)) FROM stations;"
    sleep 0.5
done
```

Terminal 2: Read Workload

Run this command to continuously query the data:

```shell
while true; do
    mysql -h 127.0.0.1 -P 6000 -u root -D sample_weather -e "SELECT s.name, s.location,
    r.temperature, r.humidity, r.recorded_at FROM stations s JOIN readings r ON s.id = r.station_id
    WHERE r.recorded_at >= NOW() - INTERVAL 5 MINUTE ORDER BY r.recorded_at DESC LIMIT 5;"
    sleep 1
    mysql -h 127.0.0.1 -P 6000 -u root -D sample_weather -e "SELECT s.name,
    ROUND(AVG(r.temperature), 1) as avg_temp, ROUND(AVG(r.humidity)) as avg_humidity,
    COUNT(*) as num_readings FROM stations s JOIN readings r ON s.id = r.station_id WHERE
    r.recorded_at >= NOW() - INTERVAL 1 HOUR GROUP BY s.id, s.name ORDER BY avg_temp DESC;"
    sleep 3
done
```

## Monitor your application

Now that you have a running application with active read and write workloads, let's use TiDB's built-in monitoring tools to understand what's happening.

### TiDB Dashboard: SQL insights

Access TiDB Dashboard by checking its URL on the terminal you are running TiUP playground (typically http://127.0.0.1:2379/dashboard - user: `root`, no password) to:

1. View your running queries:

    - Go to "SQL Statements" to see your weather data queries
    - Check execution times, and additional optional columns, and click on the statement for more execution details
    - Go to "Slow Queries" to identify queries that might need optimization

2. Monitor instance status:

    - Check "Overview" and "Cluster Info" for general topology, and resource usage
    - Check "Monitoring" to see the database load and other relevant metrics
    - Check "Search Logs" for any query errors

### Grafana: system performance

Access Grafana by checking its URL on the terminal you are running TiUP playground (typically http://127.0.0.1:3000 - user: `admin`, password: `admin`). Change the password or Skip. You can visualize the built-in dashboards by clicking on the Search icon and the folder "Test-Cluster":

1. Detailed TiDB metrics:

    Search for "Overview", for general cluster health status

2. TiProxy Load Balancing:

    Search for "TiProxy", and check the "Balance" row

> **Tip:**
>
> Keep these monitoring pages open while experimenting with different data volumes or query patterns to understand how your application behaves under load.

## Scaling your cluster

As your weather monitoring system grows, you'll need to handle more stations, readings, and queries. Let's scale the cluster while observing the process in real-time.

### Prepare monitoring views

Before scaling, set up these monitoring views to watch the scaling process:

1. Open TiDB Dashboard (typically http://127.0.0.1:2379/dashboard):

    Go to "Cluster Info", "Store Topology"

2. Open Grafana (typically http://127.0.0.1:3000):

    - Find "TiKV-Summary" dashboard
    - Look for the "Cluster" panel:
        - Store, Available, and Capacity size charts

### Add storage capacity (TiKV)

With monitoring in place, let's add two additional TiKV nodes (scale-out). Open a new terminal and run:

```shell
tiup playground scale-out --kv 2
```

Watch the expansion:

- In TiDB Dashboard, refresh the "Cluster Info", "Store Topology". You should see the new TiKV nodes in the topology
- In Grafana, watch TiKV size increase
- In your application terminals, verify continuous data ingestion without any disruption

### Remove storage capacity (TiKV)

Let's remove one TiKV node. For these scale-in operations, we specify the exact node we want to remove using its PID. First, in your available terminal, check the TiKV nodes PIDs:

```shell
tiup playground display
```

You should see something similar to:
```shell
Pid     Role    Uptime
...
51456   tikv    9m43.93267625s
...
```

You can scale-in your cluster by removing one TiKV node of your choice using its PID. For example, run the following replacing the `--pid` value with your `tikv` PID:

```shell
tiup playground scale-in --pid 51464
```

### Scale query processing (TiDB)

Now that storage is expanded, let's add TiDB nodes while watching query distribution:

```shell
tiup playground scale-out --db 1
```

Watch the query layer scaling:

- TiDB Dashboard, "Cluster Info", "Instances". Check the new TiDB instance
- Grafana, search for "TiProxy-Summary", and expand the "Query Summary" or "Traffic". You should see a new instance in the backend and the traffic is being balanced across them

### Add analytical processing (TiFlash)

TiDB supports real-time analytics through its columnar storage engine, TiFlash. Let's add it to our playground cluster:

1. Add TiFlash node:

    ```shell
    tiup playground scale-out --tiflash 1
    ```

2. Enable TiFlash replica for our weather data in the table `readings`. Using the MySQL client or `tiup client` run:

    ```sql
    USE sample_weather;
    ALTER TABLE readings SET TIFLASH REPLICA 1;
    ```

3. Check replication progress:

    ```sql
    SELECT table_schema, table_name,
        replica_count, available, progress
    FROM information_schema.tiflash_replica;
    ```

Once the replica is ready (progress=1.0), you can run analytical queries that will automatically use TiFlash when beneficial. Check the in the TiDB Dashboard, SQL Statements, "#Plans" columns. If there is a new plan, you can inspect the execution details to see if there is a task performed by `mpp[tiflash]`.

You may not notice too much performance difference because it is a local test environment with low concurrency. In a production environment with real workloads, TiFlash significantly improves analytical query performance while isolating these resource-intensive operations from your transactional workload. This separation enables real-time analytics without impacting your operational applications. If you are interested in testing in a production-like environment, see [Deploy a TiDB Cluster Using TiUP](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) or [Deploy a TiDB Cluster on Kubernetes](https://docs.pingcap.com/tidb/stable/tidb-in-kubernetes).

## Clean up (Optional)

If you want to clean up after experimenting:

1. Stop running workloads (<kbd>Ctrl+C</kbd> in Terminal 1 and 2)
2. Stop the playground cluster (<kbd>Ctrl+C</kbd> in the playground terminal)
3. Clean up the environment:

```shell
tiup clean sample-app-env
```

If you want to clean everything, all environments and components, run:

```shell
tiup clean --all
```

## What's next

You've successfully:

- Set up a distributed SQL database
- Built a sample weather monitoring application
- Explored monitoring and scaling
- Added analytical capabilities

Continue your learning journey!

### For Developers

- [Developer Guide](https://docs.pingcap.com/tidb/stable/dev-guide-overview) - guides by popular languages, frameworks, and tools
- [TiDB Developer Courses](https://www.pingcap.com/education/#developer-courses) - free self-paced courses

### For Operations

- [Deploy a TiDB Cluster Using TiUP](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)
- [Deploy a TiDB Cluster on Kubernetes](https://docs.pingcap.com/tidb/stable/tidb-in-kubernetes)
- [Migrate from MySQL-compatible databases to TiDB](https://docs.pingcap.com/tidb/stable/quick-start-with-dm)
- [Import Data from Files](https://docs.pingcap.com/tidb/stable/sql-statement-import-into)
- [Data Streaming and Change Data Capture with TiCDC](https://docs.pingcap.com/tidb/stable/deploy-ticdc)
- [Database Operations Courses](https://www.pingcap.com/education/#database-operation-courses) - deep dive into operations and get certified

### For Data Analytics

- [Use TiFlash for HTAP](https://docs.pingcap.com/tidb/stable/quick-start-with-htap)

### Community Resources

- [Join TiDB Community](https://tidb.io/community)
- [TiDB Blog](https://pingcap.com/blog)
- [GitHub](https://github.com/pingcap/tidb)
