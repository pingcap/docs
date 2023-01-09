---
title: TLS connects to Serverless Tier
summary: Introduce TLS connection in TiDB Serverless Tier.
---

# TLS connects to Serverless Tier

Establishing a secure TLS connection between your client and your Serverless database cluster is one of the basic security practices for connecting to your database cluster. The server certificate is issued by an independent third-party certificate provider [Let's Encrypt](https://letsencrypt.org/). You can easily connect to your database cluster without downloading a server-side digital certificate.

## Connection prerequisites

Before connecting to your serverless cluster, you can refer to [Password authentication](tidb-cloud-password-authentication.md) or [SSO authentication]() to log in to TiDB Cloud.

We simplify the operation process of setting database passwords, allowing you to more conveniently and securely set and reset database cluster passwords on the connect page of your Serverless cluster.

## Secure connection to TiDB database cluster

TiDB Cloud provides different connection examples in the **Connect** dialog. After creating your TiDB Serverless Tier Cluster, click Cluster to see detailed cluster information, and you can see the "Connect" label in the upper right corner. After clicking, you will enter the function page for setting the client, application, or development tool to connect to the database.
   - Support Mysql CLI, MyCLI, JDBC, Python, Go, Node.js and other six ways to connect to your Serverless cluster
   - Provide MacOS, Debian, RedHat, Alpine, OpenSUSE, Windows and other operating system configuration parameters

The following examples show the connection string in MySQL CLI, MyCLI , JDBC, Python, Go and Node.js:

<SimpleTab>
<div label="MySQL CLI">

MySQL CLI client attempts to establish TLS connection by default. When you connect to TiDB Serverless Tier clusters, you should set `ssl-mode` and `ssl-ca`.

```shell
mysql --connect-timeout 15 -u <username> -h <host> -P 4000 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -D test -p
```

- With `--ssl-mode=VERIFY_IDENTITY`, MySQL CLI client forces to enable TLS and validate TiDB Serverless Tier clusters.
- Use `--ssl-ca=<CA_root_path>` to set the CA root path on your system.

</div>

<div label="MyCLI">

[MyCLI](https://www.mycli.net/) automatically enables TLS when using TLS related parameters. When you connect to TiDB Serverless Tier clusters, you need to set `ssl-ca` and `ssl-verify-server-cert`.

```shell
mycli -u <username> -h <host> -P 4000 -D test --ssl-ca=<CA_root_path> --ssl-verify-server-cert
```

- Use `--ssl-ca=<CA_root_path>` to set the CA root path on your system.
- With `--ssl-verify-server-cert` to validate TiDB Serverless Tier clusters.

</div>

<div label="JDBC">

[MySQL Connector/J](https://dev.mysql.com/doc/connector-j/8.0/en/)'s TLS connection configurations are used here as an example.

```
jdbc:mysql://<host>:4000/test?user=<username>&password=<your_password>&sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3
```

- Set `sslMode=VERIFY_IDENTITY` to enable TLS and validate TiDB Serverless Tier clusters. JDBC trusts system CA root certificates by default, so you do not need to configure certificates.
- Set `enabledTLSProtocols=TLSv1.2,TLSv1.3` to restrict the versions of TLS protocol.

</div>

<div label="Python">

[mysqlclient](https://pypi.org/project/mysqlclient/)'s TLS connection configurations are used here as an example.

```
host="<host>", user="<username>", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<CA_root_path>"}
```

- Set `ssl_mode="VERIFY_IDENTITY"` to enable TLS and validate TiDB Serverless Tier clusters.
- Set `ssl={"ca": "<CA_root_path>"}` to set the CA root path on your system.

</div>

<div label="Go">

[Go-MySQL-Driver](https://github.com/go-sql-driver/mysql)'s TLS connection configurations are used here as an example.

```
mysql.RegisterTLSConfig("tidb", &tls.Config{
  MinVersion: tls.VersionTLS12,
  ServerName: "<host>",
})

db, err := sql.Open("mysql", "<usename>:<your_password>@tcp(<host>:4000)/test?tls=tidb")
```

- Register `tls.Config` in connection to enable TLS and validate TiDB Serverless Tier clusters. Go-MySQL-Driver uses system CA root certificates by default, so you do not need to configure certificates.
- Set `MinVersion: tls.VersionTLS12` to restrict the versions of TLS protocol.
- Set `ServerName: "<host>"` to verify TiDB Serverless Tier's hostname.
- If you do not want to register a new TLS configuration, you can just set `tls=true` in the connection string.

</div>

<div label="Node.js">

[Mysql](https://www.npmjs.com/package/mysql2)'s TLS connection configurations are used here as an example.

```
host: '<host>', port: 4000,user: '<username>', password: '<your_password>', database: 'test', ssl: {minVersion: 'TLSv1.2', rejectUnauthorized: true}
```

- Set `ssl: {minVersion: 'TLSv1.2'}` to restrict the versions of TLS protocol.
- Set `ssl: {rejectUnauthorized: true}` to validate TiDB Serverless Tier clusters. Mysql2 uses system CA root certificates by default, so you do not need to configure certificates.

</div>
</SimpleTab>

## Create and Reset Serverless database password

When you connect to your cluster for the first time, click "Create Password" to automatically generate a password with a length of 16 characters, including numbers, uppercase and lowercase characters, and special characters. The password will be automatically embedded in the sample code for connecting to your cluster easily .

You should copy the password after you create it, and only reset the password after leaving the connect page. Since the serverless cluster is accessed through the Internet,if you need to use the password elsewhere, every time you click on your cluster connection, you need to reset the password of your database cluster to ensure the security and compliance of the database password.

## Root Digital certificate management of Serverless Tier 

### Root Digital certificate‘s issuance and validity  

TiDB Serverless Tier uses certificates from [Let's Encrypt](https://letsencrypt.org/) as a Certificate Authority (CA) for TLS connection between clients and TiDB Serverless Tier clusters. Usually, the root certificate ([ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt)) of Let's Encrypt is present in your system's root CA stores. Let's Encrypt issues Serverless Tier Server digital certificates that are valid for 90 days and will be automatically rotated upon expiration.

TiDB Serverless Tier does not provide a CA root certificate download, because we don't guarantee that the same CA will be used to issue a certificate in the future, which will cause the CA root certificate to change.

If the client uses the system's root CA stores by default, such as Java and Go, you can easily connect securely to TiDB Serverless Tier clusters without specifying the path of CA roots.

However, some drivers and ORMs do not use the system root CA stores. In those cases, you need to configure the CA root path of the drivers or ORMs to your system root CA stores. For example, when you use [mysqlclient](https://github.com/PyMySQL/mysqlclient) to connect a TiDB Serverless Tier cluster in Python on macOS, you need to set `ca: /etc/ssl/cert.pem` in the `ssl` argument.

If you are using a GUI client, such as DBeaver, which does not accept a certificate file with multiple certificates inside, you must download the [ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt) certificate.

### Root Digital certificate‘s default path 

In different operating systems, the automatic download storage path of the root certificate is as follows：

**MacOS**

```
/etc/ssl/ca_root.pem
```

**Debian / Ubuntu / Arch**

```
/etc/ssl/certs/ca_root.crt
```

**RedHat / Fedora / CentOS / Mageia**

```
/etc/pki/tls/certs/ca_root.crt
```

**Alpine**

```
/etc/ssl/ca_root.pem
```

**OpenSUSE**

```
/etc/ssl/ca_root.pem
```

**Windows**

Windows does not offer a specific path to the CA root. Instead, it uses the [registry](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores) to store certificates. For this reason, to specify the CA root path on Windows, take the following steps:

1. Download the [Mozilla CA Certificate bundle](https://curl.se/docs/caextract.html) and save it in a path you prefer, such as `<path_to_mozilla_ca_cert_bundle>`.
2. Use the path (`<path_to_mozilla_ca_cert_bundle>`) as your CA root path when you connect to a Serverless Tier cluster.

## FAQ

### Which TLS versions are supported to connect to my TiDB Serverless cluster?

TiDB Serverless database cluster only supports TLS 1.2 and TLS 1.3, and does not support TLS 1.0 and TLS 1.1 versions for security reasons. Refer to see IETF [Deprecating TLS 1.0 and TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/) for ditails.

### Does TiDB Serverless Tier support two-way TLS authentication between my connect client and TiDB Serverless cluster?

No.

TiDB Serverless Tier only support one-way TLS authentication, which means your client uses public key to verify the signature of your TiDB database server certificate's private key
 while the server does not validate the client.

### Does TiDB Serverless Tier have to configure TLS to establish a secure connection?

Yes.

TiDB Serverless Tier only allows TLS connections and prohibits non-SSL/TLS connections. The reason is that SSL/TLS is one of the most basic security measures for you to connect to the TiDB Serverless database cluster through internet, so as to reduce the risk of data exposure to internet.