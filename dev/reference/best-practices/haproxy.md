---
title: HAProxy in TiDB
summary: This document describes the best configuration and usage of HAProxy in TiDB.
category: reference
---

# HAProxy in TiDB

This document describes the best configuration and usage of HAProxy in TiDB. HAProxy is a TCP load balancer. TiDB clients can manipulate data by connecting to the floating virtual IP address provided by HAProxy to achieve load balancing in the TiDB server layer.

![HAProxy Best Practices in TiDB](/media/haproxy.jpg)

## Introduction to HAProxy

[HAProxy](https://github.com/haproxy/haproxy) is free, open source software written in C language that provides a high availability load balancer and proxy server for TCP and HTTP-based applications. Because of its fast and efficient use of CPU and memory, HAProxy is now widely used by many well-known websites such as GitHub, Bitbucket, Stack Overflow, Reddit, Tumblr, Twitter and Tuenti, and Amazon Web Services.

HAProxy is written in year 2000 by Willy Tarreau, the core contributor to the Linux kernel, who is still responsible for the maintenance of the project and provides free software updates in the open source community. The latest stable version 2.0.0 was released on August 16, 2019, bringing more [excellent features](https://www.haproxy.com/blog/haproxy-2-0-and-beyond/).

## Basic Features

-[High Availability](http://cbonte.github.io/haproxy-dconv/1.9/intro.html#3.3.4): HAProxy provides high availability with support for a graceful shutdown and a seamless switchover;
-[Load Balancing](http://cbonte.github.io/haproxy-dconv/1.9/configuration.html#4.2-balance): Two major proxy modes are supported: TCP, also known as layer 4, and HTTP, also known as layer 7. No less than 9 load balancing algorithms are supported, such as roundrobin, leastconn and random;
-[Health Check](http://cbonte.github.io/haproxy-dconv/1.9/configuration.html#5.2-check): HAProxy periodically checks the status of HTTP or TCP mode of the server;
-[Sticky Session](http://cbonte.github.io/haproxy-dconv/1.9/intro.html#3.3.6): HAProxy can stick a client to a specific server for the duration of a session when the application does not support sticky sessions;
-[SSL](http://cbonte.github.io/haproxy-dconv/1.9/intro.Html#3.3.2): HTTPS communication and resolution are supported;
-[Monitoring and Statistics](http://cbonte.github.io/haproxy-dconv/1.9/intro.html#3.3.3): Through the web page, you can monitor servers state and specific traffic information in real time.

## Environment

The following environment is required before deploying HAProxy.

### Hardware requirements

According to the official documentation, it is recommended to apply the server hardware configuration of HAProxy below. You can also calculate according to the load balancing environment and improve the configuration of the server.

| Hardware Resource      | Minimum Configuration |
| :--------------------- | :-------------------- |
| CPU                    | 2 cores, 3.5 GHz      |
| Memory                 | 16 GB                 |
| Storage                | 50 GB (SATA)          |
| Network Interface Card | 10G Network Card      |

### Software requirements

According to the official documentation, the following operating systems and packages are recommended. If you use yum to install HAProxy, the packages are not required.

#### Operating systems

-Linux 2.4 on x86, x86_64, Alpha, SPARC, MIPS and PA-RISC
-Linux 2.6/3.x on x86, x86_64, ARM, SPARC and PPC64
-Solaris 8/9 on UltraSPARC II and III
-Solaris 10 on Opteron and UltraSPARC
-FreeBSD 4.10-10 on x86
-OpenBSD 3.1 to the latest on i386, AMD64, macppc, Alpha and SPARC64
-AIX 5.1-5.3 on Power™ architecture

#### Packages

-epel-release
-gcc
-systemd-devel

{{< copyable "shell-regular" >}}

```bash
Yum-y install epel-release gcc systemd-devel
```

## Deploy HAProxy

You can easily use HAProxy to configure and set up a load balanced database environment. The following deployment operations are universal. It is recommended to customize the [configuration file](http://cbonte.github.io/haproxy-dconv/1.9/configuration.html) based on the actual scenario.

### Install HAProxy

1. Use yum to install HAProxy：

   {{< copyable "shell-regular" >}}

    ```bash
    yum -y install haproxy
    ```

2. Check whether the installation is successful：

    {{< copyable "shell-regular" >}}

    ```bash
    which haproxy
    ```

#### HAProxy commands

Execute the following command to print a list of keywords and their basic usage:

{{< copyable "shell-regular" >}}

```bash
haproxy --help
```

| options | description |
| :-------| :---------|
| -v | reports the version and build date. |
| -vv | displays the version, build options, libraries versions and usable pollers. |
| -d | enables debug mode. |
| -db | disables background mode and multi-process mode. |
| -dM [\<byte>] | forces memory poisoning, which means that each and every memory region allocated with malloc() or pool_alloc2() will be filled with <byte> before being passed to the caller. |
| -V | enables verbose mode (disables quiet mode). |
| -D | starts as a daemon.|
| -C \<dir>| changes to directory <dir> before loading configuration files. |
| -W | master-worker mode. |
| -q | sets "quiet" mode: This disables some messages during the configuration parsing and during startup. |
| -c | only performs a check of the configuration files and exits before trying to bind. |
| -n \<limit> | limits the per-process connection limit to <limit>. |
| -m \<limit> | limit the total allocatable memory to <limit> megabytes across all processes. |
| -N \<limit>| sets the default per-proxy maxconn to <limit> instead of the builtin default value (usually 2000). |
| -L \<name> | changes the local peer name to <name>, which defaults to the local hostname. |
| -p \<file>| writes all processes' PIDs into <file> during startup. |
| -de | disables the use of epoll(7). epoll(7) is available only on Linux 2.6 and some custom Linux 2.4 systems. |
| -dp | disables the use of poll(2). select(2) might be used instead. |
| -dS | disables the use of splice(2), which is broken on older kernels. |
| -dR | disables SO_REUSEPORT usage. |
| -dr| ignores server address resolution failures. |
| -dV | disables SSL verify on the server side. |
| -sf \<pidlist> | sends the "finish" signal to the PIDs in pidlist after startup. The processes which receive this signal wait for all sessions to finish before exiting. This option must be specified last, followed by any number of PIDs. Technically speaking, SIGTTOU and SIGUSR1 are sent. |
| -st \<pidlist> | sends the "terminate" signal to the PIDs in pidlist after startup. The processes which receive this signal will terminate immediately, closing all active sessions. This option must be specified last, followed by any number of PIDs. Technically speaking, SIGTTOU and SIGTERM are sent. |
| -x \<unix_socket> | connects to the specified socket and retrieve all the listening sockets from the old process. Then, these sockets are used instead of binding new ones. |
| -S \<bind>[,<bind_options>...] | in master-worker mode, creates a master CLI. This CLI enables access to the CLI of every worker. Useful for debugging, it's a convenient way of accessing a leaving process. |

For detailed information, you can refer to [Management Guide of HAProxy](http://cbonte.github.io/haproxy-dconv/1.9/management.html) and [General Commands Manual of HAProxy](https://manpages.debian.org/buster-backports/haproxy/haproxy.1.en.html).

### Configure HAProxy

A configuration template is generated when using yum to install HAProxy. You can also customize the following configuration items according to your scenarios.

```yaml
global
   log         127.0.0.1 local2            # Global syslog servers (up to two).
   chroot      /var/lib/haproxy            # Changes the current directory and sets superuser privileges for the startup process to improve security.
   pidfile     /var/run/haproxy.pid        # Writes the PIDs of HAProxy processes into this file.
   maxconn     4000                        # The maximum number of concurrent connections for a single HAProxy process.
   user        haproxy                     # Same with the UID parameter.
   group       haproxy                     # Same with the GID parameter. A dedicated user group is recommended.
   nbproc      40                          # The number of processes created when going daemon. When starting multiple processes to forward requests, make sure the value is large enough so that HAProxy does not block processes.
   daemon                                  # Makes the process fork into background. It is equivalent to the command line "-D" argument. It can be disabled by the command line "-db" argument.
   stats socket /var/lib/haproxy/stats     # The directory where statistics outputs are saved.

defaults
   log global                              # Inherits the settings of the global configuration.
   retries 2                               # The maximum number of retries to connect to an upstream server. If the number of connection attempts exceeds the value, the backend server is considered unavailable.
   timeout connect  2s                     # The maximum time to wait for a connection attempt to a backend server to succeed. It should be set to a shorter time if the server is located on the same LAN as HAProxy.
   timeout client 30000s                   # The maximum inactivity time on the client side.
   timeout server 30000s                   # The maximum inactivity time on the server side.

listen admin_stats                         # The name of the Stats page reporting information from frontend and backend. You can customize the name according to your needs.
   bind 0.0.0.0:8080                       # The listening port.
   mode http                               # The monitoring mode.
   option httplog                          # Enables HTTP logging.
   maxconn 10                              # The maximum number of concurrent connections.
   stats refresh 30s                       # Automatically refreshes the Stats page every 30 seconds.
   stats uri /haproxy                      # The URL of the Stats page.
   stats realm HAProxy                     # The authentication realm of the Stats page.
   stats auth admin:pingcap123             # User name and password in the Stats page. You can have multiple user names.
   stats hide-version                      # Hides the version information of HAProxy on the Stats page.
   stats admin if TRUE                     # Manually enables or disables the backend server. <span class="version-mark">New in HAProxy 1.4.9 or later versions</span>

listen tidb-cluster                        # Database load balancing.
   bind 0.0.0.0:3390                       # Floating IP addresses and listening ports.
   mode tcp                                # HAProxy uses layer 4, the transport layer.
   balance leastconn                       # The server with the smallest number of connections receives the connection. `leastconn' is recommended where long sessions are expected, such as LDAP, SQL and TSE, rather than protocols using short sessions, such as HTTP. The algorithm is dynamic, which means that server weights might be adjusted on the fly for slow starts for instance.
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # Detects port 4000 at a frequency of once every 2000 milliseconds. If it is detected as successful twice, the server is considered available; if it is detected as failed three times, the server is considered unavailable.
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

### Use `systemd` to start HAProxy

There are two methods to start HAProxy.

Method 1: Execute `haproxy`.

{{< copyable "shell-regular" >}}

```bash
haproxy -f /etc/haproxy/haproxy.cfg
```

Method 2: Use `systemd` to start HAProxy. `/etc/haproxy/haproxy.cfg` is read by default (recommended).

{{< copyable "shell-regular" >}}

```bash
systemctl start haproxy.service
```

### Use `systemd` to stop HAProxy

There are two methods to stop HAProxy.

Method 1: Execute `kill -9`.

{{< copyable "shell-regular" >}}

```bash
ps -ef | grep haproxy
```

Then terminate the process of HAProxy:

{{< copyable "shell-regular" >}}

```bash
kill -9 ${haproxy.pid}
```

Method 2: Use `systemd` to stop HAProxy.

{{< copyable "shell-regular" >}}

```bash
systemctl stop haproxy.service
```
