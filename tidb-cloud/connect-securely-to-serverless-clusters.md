---
title: Connect Securely to Serverless Tier Clusters
summary: Introduce TLS connection in TiDB Serverless.
---

# Connect Securely to Serverless Tier Clusters

This document introduces the core information about TLS in TiDB Serverless Tier.

## Can I disable TLS in Serverless?

No.

Serverless clusters allow only TLS connections and reject normal connections. The reason for this is that users connect to Serverless Tier clusters through a public network, so communication security is really important.

## What TLS versions can I use?

TiDB Serverless only supports TLS 1.2 and TLS 1.3. 

You can specify the version in the connection strings. For example, If you use MySQL Client to connect TiDB Serverless, you can set `--tls-version=TLSv1.3` to enforce the TLS 1.3 version.

## What certificates do I need？

TiDB Serverless uses certificates from [Let's Encrypt](https://letsencrypt.org/) as a Certificate Authority (CA) for TLS connection between clients and TiDB Serverless. Usually, Let's Encrypt's root certificate is present in your system's root CA stores. If the client uses the system's root CA stores by default, such as Java and Go, you can easily connect securely to TiDB Serverless without specifying the path of CA roots.

However, some drivers and ORMs do not use the system root CA stores. In those cases, you should configure ca root path of the drivers or ORMs to your system root CA stores. For example, when you use MySQLdb to connect TiDB Serverless in Python, you should set `ca: /etc/ssl/cert.pem` in ssl configurations.

> **Note**
> 
> TiDB Serverless does not provide a CA root certificate download, because we don't guarantee that the same CA will be used to issue a certificate in the future, which will cause the CA root certificate to change. 
> 
> TiDB Serverless promises to always use the CA root certificate that is normally available, which is provided on all common systems. 

## How do I connect to TiDB Serverless in TLS connection?

TiDB Cloud provides some connection examples in the **Connect** tab. You can follow the instructions in [Connect via standard connection](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) to connect to TiDB Serverless Tier.

Generally, enable TLS and offer a CA root path to authenticate the server. This helps you prevent a man-in-the-middle attack. Different clients have different operations in the TLS connection. Enable TLS and verify the server according to your actual use of the client.

The following examples show the connection string in MySQL Client, MyCLI client, Java, Python, Go, and Node.js

<SimpleTab>
<div label="MySQL Client">

MySQL Client attempts to establish TLS connection by default. Besides, we should set `ssl-mode` and `ssl-ca` when connecting to TiDB Serverless.

- With `--ssl-mode=VERIFY_IDENTITY`, MySQL Client forces to enable TLS, and validate TiDB Serverless.
- Use `--ssl-ca=<CA_root_path>` to set the CA root path in your system.

```shell
mysql --connect-timeout 15 -u <username> -h <host> -P 4000 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -D test -p
```

</div>

<div label="MyCLI Client">

[MyCLI](https://www.mycli.net/) enables TLS automatically with `ssl` flag. We set `ssl-ca` to enable TLS and validate TiDB serverless.

- Use `--ssl-ca=<CA_root_path>` to set the CA root path in your system.

```shell
mycli -u <username> -h <host> -P 4000 -D test --ssl-ca=<CA_root_path>
```

</div>

<div label="Java">

We recommend using [MySQL Connector/J 8.0](https://dev.mysql.com/doc/connector-j/8.0/en/) or up than, to connect with TiDB Serverless in Java. Set `sslMode` in connection string to enable TLS and validate TiDB Serverless. JDBC trust system CA root certificates by default, so we don't need to configure certificates anymore.

- With `--ssl-mode=VERIFY_IDENTITY`, JDBC forces to enable TLS, and validate TiDB Serverless.

```
jdbc:mysql://<host>:4000/test?user=<username>&password=<your_password>&sslMode=VERIFY_IDENTITY
```

</div>

<div label="Python">

We recommend using [mysqlclient](https://pypi.org/project/mysqlclient/) to connect with TiDB Serverless in Python. Set `ssl.ca` in connection string to enable TLS and validate TiDB Serverless.

- Use `ssl={"ca": "<CA_root_path>"}` to set the CA root path in your system.

```
host="<host>", user="<username>", password="<your_password>", port=4000, database="test", ssl={"ca": "<CA_root_path>"}
```

</div>

<div label="Go">

We recommend using the [Go-MySQL-Driver](https://github.com/go-sql-driver/mysql) to connect with TiDB Serverless in Go. Register `tls.Config` in connection to enable TLS and validate TiDB Serverless. Go use system CA root certificates by default, so we don't need to configure certificates anymore.

- Register `tidb` TLS configuration. Set `ServerName: "<host>"` to verify TiDB Serverless hostname.
- If you don't want to register a new TLS configuration, you can just set `tls=true` in connection string.

```
mysql.RegisterTLSConfig("tidb", &tls.Config{
  MinVersion: tls.VersionTLS12,
  ServerName: "<host>",
})

db, err := sql.Open("mysql", "<usename>:<your_password>@tcp(<host>:4000)/test?tls=tidb")
```

</div>

<div label="Node.js">

We recommend using [mysql2](https://www.npmjs.com/package/mysql2) to connect with TiDB Serverless in Node.js. Set `ssl.rejectUnauthorized` in connection to validate TiDB Serverless. Node.js use system CA root certificates by default, so we don't need to configure certificates anymore.

- Set `ssl: {"rejectUnauthorized": true}` to validate TiDB Serverless hostname.

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

## Can TiDB Serverless verify the client's identity?

No.

Now, TiDB Serverless uses one-way TLS authentication, which means only client uses the public certificate pair to validate the server while server does not validate the client. For example, when you use MySQL Client, you cannot configure `--ssl-cert` and `--ssl-key` in connection strings.