---
title: Secure Connections to Serverless Tier Clusters
summary: Introduce TLS connection in TiDB Serverless Tier clusters.
---

# Secure Connections to Serverless Tier Clusters

This document introduces the core information about TLS in TiDB Serverless Tier.

## Can I disable TLS in TiDB Serverless Tier?

No.

TiDB Serverless Tier allows only TLS connections and rejects non-TLS connections. The reason is that users connect to TiDB Serverless Tier clusters through a public network, so it is really important to use TLS to improve communication security.

## What TLS versions can I use?

TiDB Serverless Tier only supports TLS 1.2 and TLS 1.3. 

## What certificates do I need？

TiDB Serverless Tier uses certificates from [Let's Encrypt](https://letsencrypt.org/) as a Certificate Authority (CA) for TLS connection between clients and TiDB Serverless Tier clusters. Usually, the root certificate ([ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt)) of Let's Encrypt is present in your system's root CA stores. If the client uses the system's root CA stores by default, such as Java and Go, you can easily connect securely to TiDB Serverless Tier clusters without specifying the path of CA roots.

However, some drivers and ORMs do not use the system root CA stores. In those cases, you should configure the CA root path of the drivers or ORMs to your system root CA stores. For example, when you use MySQLdb to connect a TiDB Serverless Tier cluster in Python, you should set `ca: /etc/ssl/cert.pem` in ssl configurations.

> **Note:**
> 
> TiDB Serverless Tier does not provide a CA root certificate download, because we don't guarantee that the same CA will be used to issue a certificate in the future, which will cause the CA root certificate to change. 
> While, TiDB Serverless Tier can always use the CA root certificate that is normally available, which is provided in all common systems. 
> 
> If you really need the CA certificate of a TiDB Serverless Tier cluster, it is recommended that you download the [Mozilla CA Certificate bundle](https://curl.se/docs/caextract.html) instead of a single CA certificate.

## How do I connect to a TiDB Serverless Tier cluster in TLS connection?

TiDB Cloud provides some connection examples in the **Connect** tab. You can follow the instructions in [Connect via standard connection](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) to connect to a TiDB Serverless Tier cluster.

Generally, enabling TLS and offering a CA root path to authenticate the server is a good practice to prevent a man-in-the-middle attack. Different clients have different operations in the TLS connection. Enable TLS and verify the server according to your actual use of the client.

The following examples show the connection string in MySQL Client, MyCLI client, Java, Python, Go, and Node.js:

<SimpleTab>
<div label="MySQL Client">

MySQL Client attempts to establish TLS connection by default. When you connect to TiDB Serverless Tier clusters, you must set `ssl-mode` and `ssl-ca`.

- With `--ssl-mode=VERIFY_IDENTITY`, MySQL Client forces to enable TLS and validate TiDB Serverless Tier clusters.
- Use `--ssl-ca=<CA_root_path>` to set the CA root path in your system.

```shell
mysql --connect-timeout 15 -u <username> -h <host> -P 4000 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -D test -p
```

</div>

<div label="MyCLI Client">

[MyCLI](https://www.mycli.net/) enables TLS automatically with the `ssl` flag. You can set `ssl-ca` to enable TLS and validate TiDB serverless Tier clusters.

- Use `--ssl-ca=<CA_root_path>` to set the CA root path in your system.

```shell
mycli -u <username> -h <host> -P 4000 -D test --ssl-ca=<CA_root_path>
```

</div>

<div label="Java">

We recommend using [MySQL Connector/J 8.0](https://dev.mysql.com/doc/connector-j/8.0/en/) or later versions to connect to TiDB Serverless Tier clusters in Java.

- Set `sslMode` in connection string to enable TLS and validate TiDB Serverless Tier clusters. JDBC trusts system CA root certificates by default, so you do not need to configure certificates.
- With `--ssl-mode=VERIFY_IDENTITY`, JDBC forces to enable TLS and validate TiDB Serverless Tier clusters.

```
jdbc:mysql://<host>:4000/test?user=<username>&password=<your_password>&sslMode=VERIFY_IDENTITY
```

</div>

<div label="Python">

We recommend using [mysqlclient](https://pypi.org/project/mysqlclient/) to connect to TiDB Serverless Tier clusters in Python. 

- Set `ssl.ca` in the connection string to enable TLS and validate TiDB Serverless Tier clusters.
- Use `ssl={"ca": "<CA_root_path>"}` to set the CA root path in your system.

```
host="<host>", user="<username>", password="<your_password>", port=4000, database="test", ssl={"ca": "<CA_root_path>"}
```

</div>

<div label="Go">

It is recommended to use the [Go-MySQL-Driver](https://github.com/go-sql-driver/mysql) to connect to TiDB Serverless Tier clusters in Go.

- Register `tls.Config` in connection to enable TLS and validate TiDB Serverless Tier clusters. Go uses system CA root certificates by default, so you do not need to configure certificates.
- Register `tidb` TLS configuration. Set `ServerName: "<host>"` to verify TiDB Serverless Tier's hostname.
- If you do not want to register a new TLS configuration, you can just set `tls=true` in the connection string.

```
mysql.RegisterTLSConfig("tidb", &tls.Config{
  MinVersion: tls.VersionTLS12,
  ServerName: "<host>",
})

db, err := sql.Open("mysql", "<usename>:<your_password>@tcp(<host>:4000)/test?tls=tidb")
```

</div>

<div label="Node.js">

It is recommended to use [mysql2](https://www.npmjs.com/package/mysql2) to connect with TiDB Serverless Tier clusters in Node.js. Node.js use system CA root certificates by default, so you do not need to configure certificates anymore.

- Set `ssl: {"rejectUnauthorized": true}` to validate TiDB Serverless Tier's hostname.

```
host: '<host>', port: 4000,user: '<username>', password: '<your_password>', database: 'test', ssl: {"rejectUnauthorized": true}
```

</div>
</SimpleTab>

## Where is the CA root path in my system?

The following lists the CA root paths in common platforms.

**MacOS**

```
/etc/ssl/cert.pem
```

**Debian / Ubuntu / Arch**
```
/etc/ssl/certs/ca-certificates.crt
```

**RedHat / Fedora / CentOS / Mageia / Vercel / Netlify**

```
/etc/pki/tls/certs/ca-bundle.crt
```

**Alpine**

```
/etc/ssl/cert.pem
```

**OpenSUSE**

```
/etc/ssl/ca-bundle.pem
```

## Can TiDB Serverless Tier verify the client's identity?

No.

Currently, TiDB Serverless Tier uses one-way TLS authentication, which means only the client uses the public certificate pair to validate the server while the server does not validate the client. For example, when you use MySQL Client, you cannot configure `--ssl-cert` or `--ssl-key` in connection strings.