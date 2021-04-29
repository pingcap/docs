---
title: Loadbalancing
summary: How to use loadbalancing with TiDB
---

# Loadbalancing

Loadbalancing is used to distribute connections from applications to TiDB Server instances. This helps to distribute the load over multiple machines and (depending on the loadbalancing option selected) can automatically re-route connections should a TiDB instance become unavailable.

## Loadbalancing types

There are many different ways implementing loadbalancer. In this section the most common types of loadbalancing are described.

| Loadbalancer type | Usage scenarios | Benefits | Drawbacks |
| ------------------|-----------------|----------|-----------|
| Connector based, such as MySQL Connector/J and MySQL Connector/C++   | Load balancing a specific application | No need for extra components | Connector specific implementation and behavior |
| DNS (Round-robin or SRV) | Simple loadbalancing without requiring application modifications  | Re-using existing components and methods | Not automatically removing failed nodes from service |
| Kubernetes Loadbalancer (e.g. metallb or Amazon ELB) | Load balancing in the cloud | Well integrated with Kubernetes | Requires Kubernetes |
| Software based loadbalancer | A daemon that implements loadbalancing | Flexible | Often service specific |
| Hardware based loadbalancer (e.g. F5) | A hardware loadbalancer | Can use hardware accelleration | Expensive |

The first type of loadbalancing that is available is **connector based loadbalancing**. Many of the MySQL connectors like MySQL Connector/J and MySQL Connector/C++. The benefits from this are that there is no extra network hop and the application has more information about which server it is connected to. The drawback of this is that there is no central administration and when changing the configuration you have to do this on all your application hosts. Depending on the programming language you are using the loadbalancing might not be available or not offer more advanced options. This can work with most third-party applications as this is often configured in the connection string (JDBC url for Java for example).

It is also possible to use **DNS round-robin**. However this is not advisable as this won't prevent connections from going to a machine that is unavailable. This means that your application might have to re-try connections more often if not all servers are available. Some of the newer MySQL connectors have support for **[DNS SRV](https://dev.mysql.com/doc/refman/8.0/en/connecting-using-dns-srv.html)**. This is somewhat similar to round-robin DNS, but allows you to set priorities. The benefit from this is that it is an industry standard and that this makes the client-side configuration easier.

If you are using Kubernetes you probably want to use the [LoadBalancer](https://docs.pingcap.com/tidb-in-kubernetes/stable/access-tidb#loadbalancer) service type that works with Amazon ELB and similar services from other cloud vendors. For on-premise Kubernetes something like [metallb](https://metallb.universe.tf/) can be used.

When you are not using Kubernetes to deploy on a cloud service you can still use the loadbalancing service from your cloud provider.

Another common option is to use a **software based** loadbalancer. Common ones are ProxySQL, haproxy and MySQL Router.

The last type of loadbalancing is **hardware based** loadbalancers. These are physical machines where you plug in a network cable. These are often costly, but also offer a high throughput.

## General loadbalancing requirements for TiDB

The requirements that TiDB puts on loadbalancers are in some ways different that what a typical MySQL setup requires.

Where loadbalancers might offer advanced features like read/write splitting for MySQL, this is not needed for TiDB. The loadbalancer does not need to be able to inspect the MySQL protocol. A TCP level loadbalacer works fine for TiDB.

The loadbalancer only needs access to the TiDB servers (TCP port 4000 by default) and doesn't need access to PD or TiKV servers. When using the [status API (TCP port 10080 by default)](https://docs.pingcap.com/tidb/stable/tidb-monitoring-api#use-the-state-interface) is also required.

It is recommended to use `http://<ip_of_tidb>:10080/status` as the health check since it supports the use of the _graceful shutdown_ feature. This feature allows you to first drain client connections before shutting down a TiDB Server and reduces the impact on applications. The [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50) variable needs to be set to a non-zero value to benefit from this feature.

Health checks that check for `read_only` or other MySQL or InnoDB specific variables should be avoided. This is because these variables are often implemented as "noop" on TiDB.

## Where to put your loadbalancer

For software-based loadbalancers you have the option to put your loadbalancer on the same host as your application or on separate hosts. Both have their own benefits.

Installing the loadbalancer on the same host as a _sidecar_ to your application is good for performance as it doesn't need an extra network hop. However having to administer many instances of your loadbalancing software makes this slightly more complicated to administer.

Installing the loadbalancer on separate hosts will typically increase latency as an extra network hop is required. There is also risk that (depending on your network) connectivity to and from the load balancer could become saturated. However, this method is less complicated to administer.

High availability is also an important consideration when deciding between these options. With the first setup an unavailable loadbalancer only impacts a single application host. With the second solution you probably have to take some steps to make your loadbalancer software high-available, which complicates the configuration.

## Testing loadbalancing

Beore deploying loadbalancing in production it is advised to first test the configuration to make sure everything works as expected. It is also advised to test bigger configuration changes, upgrades and other maintenance tasks before doing these on a production setup.

Local testing can be done with `tiup playground --db 2` to have two TiDB instances.

When connecting via a loadbalancer you might want to use this query to check on which instance you landed:

```
SELECT @@hostname, @@port
```

Note that depending on the Proxy solution and configuration the proxy might only listen on TCP and not on a UNIX socket or the location of the UNIX socket might be different than the default. When using `mysql -h localhost...` `mysql` will try to connect over a UNIX socket even if a TCP port is provided, which in this case might not work. Use `mysql -h 127.0.0.1 ...` instead to ensure TCP is used. This is not only true for the `mysql` command line client but also for many other applications.

## Example configurations

In this section you can find an example configuration for using some of the most popular loadbalancing solutions with TiDB.

### ProxySQL

ProxySQL is an open source high performance proxy for the MySQL protocol. As this knows the MySQL Protocol this brings a lot of MySQL specific features like query caching and query rewriting.

The first step is to install ProxySQL. More details and instructions for other platforms can be found in [the official docs](https://proxysql.com/documentation/installing-proxysql/).

```
sudo dnf install proxysql
```

To configure ProxySQL there are two options: via the configuration file (`/etc/proxysql.cnf`) or via the admin interface. The admin interface is using the MySQL protocol and is available on port 6032 and the default credentials are 'admin'/'admin'.

```
mysql -h 127.0.0.1 -P 6032 -u admin -padmin --prompt 'admin> '
```

The next step is to tell ProxySQL about the TiDB servers:

```
admin> INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES (1, '127.0.0.1', 4000);
Query OK, 1 row affected (0.00 sec)

admin> INSERT INTO mysql_servers(hostgroup_id, hostname, port) VALUES (1, '127.0.0.1', 4001);
Query OK, 1 row affected (0.00 sec)

admin> LOAD MYSQL SERVERS TO RUNTIME;
Query OK, 0 rows affected (0.00 sec)

admin> SAVE MYSQL SERVERS TO DISK;
Query OK, 0 rows affected (0.04 sec)
```

By default ProxySQL uses an account called 'monitor' to test connectivity to backend servers. So now create this user. The username and password for this user are set in ProxySQL via a variable, so you can change this if you want.

```
tidb> CREATE USER 'monitor'@'%' IDENTIFIED BY 'monitor';
Query OK, 0 rows affected (0.06 sec)
```

Now add a user to ProxySQL that matches the default 'root' user that is available in a `tiup playground`.

```
admin> INSERT INTO mysql_users(username,password,default_hostgroup) VALUES ('root','',1);
Query OK, 1 row affected (0.00 sec)

admin> LOAD MYSQL USERS TO RUNTIME;
Query OK, 0 rows affected (0.00 sec)

admin> SAVE MYSQL USERS TO DISK;
Query OK, 0 rows affected (0.04 sec)
```

Now try to connect:

```
$ mysql -h 127.0.0.1 -P 6033 -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 5.5.30 (ProxySQL)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> select version();
+--------------------+
| version()          |
+--------------------+
| 5.7.25-TiDB-v5.0.0 |
+--------------------+
1 row in set (0.00 sec)
```

The default port for application traffic for ProxySQL is 6033 (3306 in reverse!).

If you don't want to use query routing or query caching then you might want to enable `fast_forward` which is set in the `mysql_users` table as this reduces the amount of work the proxy has to do for each connection which lowers the latency a bit.

### HAProxy

HAProxy is a high performance loadbalancer that is mostly know for HTTP loadbalancing but it can also be used as TCP loadbalancer. Besides a basic health check it doesn't know about the MySQL Protocol.

Begin with installing HAProxy

```
sudo dnf install haproxy
```

Then configure HAProxy by editing `/etc/haproxy/haproxy.cfg`. Add the following to the file:

```
listen tidb
    mode tcp
    bind 127.0.0.1:3306
    balance leastconn
    option mysql-check user root

    server tidb1 127.0.0.1:4000 check
    server tidb2 127.0.0.1:4001 check

frontend stats
    bind 127.0.0.1:8080
    stats enable
    stats uri /
    stats refresh 10s
    stats admin if LOCALHOST
```

This adds a tidb service with two backend servers. This will route connections to the server with the least amount of connections. This enables a MySQL protocol specific check to see if backend servers are healthy.

The "stats" part is optional and enables a web interface to see statistics and manage servers.

Here 127.0.0.1 was used to bind to localhost only, use `bind ::3306` if you want to allow external connections.

The 3306 TCP port is labeled as `mysqld_port_t` on systems with SELinux enabled. To allow HAProxy to use this port use the following. This step can be skipped if SELinux is not enabled.

```
sudo setsebool -P haproxy_connect_any 1
```

Now start HAProxy

```
sudo systemctl enable haproxy --now
```

See also [Best Practices for Using HAProxy in TiDB](/best-practices/haproxy-best-practices.md)

### MySQL Router

MySQL Router is an open source loadbalancing solution for the MySQL protocol from the MySQL team at Oracle.

First install MySQL Router. Follow the [instructions from the documentaton](https://dev.mysql.com/doc/mysql-router/8.0/en/mysql-router-installation.html) for your platform of choice. For this example I'm using Linux.

```
sudo rpm -ivh https://dev.mysql.com/get/mysql80-community-release-fc34-1.noarch.rpm
sudo dnf install mysql-router
```

Now configure the router by adding the following to `/etc/mysqlrouter/mysqlrouter.conf`:

```
[routing:tidb]
bind_address = 127.0.0.1:6446
routing_strategy = round-robin
protocol = classic
destinations = 127.0.0.1:4000, 127.0.0.1:4001
```

```
sudo systemctl enable  mysqlrouter --now
```

Note that you need to use `protocol = classic` as TiDB does not support the [X Protocol](https://github.com/pingcap/tidb/issues/1109).

### MySQL Connector/J

MySQL Connector/J is the JDBC Driver that implements the MySQL protocol for Java an other JVM based languages.

MySQL Connector/J supports various kinds of [Multi-Host Connections](https://dev.mysql.com/doc/connectors/en/connector-j-multi-host-connections.html). In this example the `loadbalance` option is used as that distributes the load over multiple TiDB servers where the `failover` tries to use the first host from the list, resulting in an un-even distribution of load.

The `X Dev API` connection type of Connector/J can not be used with TiDB as [TiDB doesn't support the X Protocol](https://github.com/pingcap/tidb/issues/1109).

An example with MySQL Connector/J 8.0.24:

```
package com.pingcap.tidb_demo_java;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSet;

public class App
{
    public static void main( String[] args )
    {
        try {
                Class.forName("com.mysql.cj.jdbc.Driver").newInstance();
        } catch (Exception ex) {
                System.out.println("Failed to load driver: " + ex.getMessage());
        }

        try {
                Connection conn = DriverManager.getConnection("jdbc:mysql:loadbalance://127.0.0.1:4000,127.0.0.1:4001?user=root");
                Statement stmt = conn.createStatement();
                ResultSet rs = stmt.executeQuery("SELECT @@hostname, @@port");
                rs.next();
                System.out.println(rs.getString("@@hostname") + ":" + rs.getString("@@port"));
        } catch (SQLException ex) {
                System.out.println("SQLException: " + ex.getMessage());
        }
    }
}
```

See [Best Practices for Developing Java Applications with TiDB](/best-practices/java-app-best-practices.md) for more details about how to use TiDB with Java Applications.

### MySQL Connector/Python

MySQL Connector/Python is the offical MySQL driver for Python. Note that there are also other commonly used MySQL drivers for Python, but those don't support the loadbalancing configuration that is described here.

In this example MySQL Connector/Python 8.0.24 (`mysql-connector-python==8.0.24` according to `pip freeze` output) is used.

To install this connector see the [official installation instructions](https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html).

```
#!/usr/bin/python3
import mysql.connector

config = {
    "failover": [
        {"host": "127.0.0.1", "port": 4000, "user": "root"},
        {"host": "127.0.0.1", "port": 4001, "user": "root"},
    ],
}

for _ in range(5):
    c = mysql.connector.connect(**config)
    cur = c.cursor()
    cur.execute("select @@hostname, @@port")
    print(cur.fetchone())
    cur.close()
    c.close()
```

This outputs:

```
('myserver1', 4001)
('myserver1', 4000)
('myserver1', 4001)
('myserver1', 4001)
('myserver1', 4000)
```

### Amazon ELB

Amazon Elastic Load Balancer (ELB) is the loadbalancing service that is part of the Amazon Web Services (AWS) cloud.

You can create the loadbalancer manually with the AWS Dashboard or by using automation like CloudFormation. When using Kubernetes (EKS) deploying a LoadBalancer is done as part of the deployment.

Choose "Network Load Balancer" for the loadbalancer type. Depending on your requirements you need to select "Internet-facing" or "Internal".

Configure the listener to use TCP Port 3306 or 4000.

Create a target group with the IP-addresses of your TiDB instances. Choose port 3306 or 4000 depending on the port you have configured for TiDB.

You need to make sure that the security group of your TiDB machines allows access from your loadbalancer. It is recommended to configure the security group for the loadbalancer to allow access from your applications, but restrict access from the rest of the internet.

For more details see the [Network Load Balancer docs](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancer-getting-started.html).

## Advanced configuration

You might want to exclude specific servers from your loadbalancer pool or create a separate loadbalancer pool if they have a different hardware configuration (e.g. more memory and CPUs). This can be used to separate analytical or data loading tasks.

## Automation

To automate operations like adding or removing instances you might want to use the [TiDB HTTP API](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md).

If you do this you might want to filter based on the labels of the servers in case not all servers should be put in your loadbalancer pool.

```
$ curl -s http://127.0.0.1:10080/info/all | jq '.all_servers_info'
{
  "431ccb25-24a6-4311-b48d-613cac401b22": {
    "version": "5.7.25-TiDB-v5.0.1",
    "git_hash": "1145e347d3469d8e89f88dce86f6926ca44b3cd8",
    "ddl_id": "431ccb25-24a6-4311-b48d-613cac401b22",
    "ip": "127.0.0.1",
    "listening_port": 4000,
    "status_port": 10080,
    "lease": "45s",
    "binlog_status": "Off",
    "start_timestamp": 1620024407,
    "labels": {},
    "server_id": 0
  },
  "b830f979-c277-4e47-934e-87bb2063cf4d": {
    "version": "5.7.25-TiDB-v5.0.1",
    "git_hash": "1145e347d3469d8e89f88dce86f6926ca44b3cd8",
    "ddl_id": "b830f979-c277-4e47-934e-87bb2063cf4d",
    "ip": "127.0.0.1",
    "listening_port": 4001,
    "status_port": 10081,
    "lease": "45s",
    "binlog_status": "Off",
    "start_timestamp": 1620024407,
    "labels": {},
    "server_id": 0
  }
}
```
