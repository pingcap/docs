---
title: TLS Connection to Serverless Tier
summary: Introduce TLS connection in TiDB Serverless Tier.
---

# TLS Connection to Serverless Tier

Establishing a secure TLS connection between your client and your TiDB Cloud Serverless Tier cluster is one of the basic security practices for connecting to your databases. The server certificate is issued by an independent third-party certificate provider [Let's Encrypt](https://letsencrypt.org/). Hence, you can easily connect to your Serverless Tier cluster without downloading a server-side digital certificate.

## Prerequisites

Before connecting to your Serverless Tier cluster, you need to log in to TiDB Cloud via [Password Authentication](tidb-cloud-password-authentication.md) or [SSO Authentication](/tidb-cloud/tidb-cloud-sso-authentication.md).


## Secure connection to TiDB database cluster

The TiDB Cloud console provides different connection examples in the **Connect** dialog. 

After creating your TiDB Serverless Tier cluster, you can click your cluster name to go to your cluster overview page, and then click **Connect** in the upper-right corner to open the **Connect** dialog. In this dialog, you can choose a connection method and your operating system.
   - Supported connection methods: MySQL CLI, MyCLI, JDBC, Python, Go, and Node.js.
   - Supported operating systems: MacOS, Debian, CentOS/RedHat/Fedora, Alpine, OpenSUSE, and Windows.

The following examples show the connection string in MySQL CLI, MyCLI, JDBC, Python, Go and Node.js:

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

## Root certificate management

### Root certificate issuance and validity  

TiDB Serverless Tier uses certificates from [Let's Encrypt](https://letsencrypt.org/) as a Certificate Authority (CA) for TLS connection between clients and TiDB Serverless Tier clusters. Usually, the root certificate ([ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt)) of Let's Encrypt is present in your system's root CA stores. The Serverless Tier Server digital certificates issued by Let's Encrypt are valid for 90 days and will be automatically rotated upon expiration.

> **Note:**
>
> TiDB Serverless Tier does not provide a CA root certificate download, because we don't guarantee that the same CA will be used to issue a certificate in the future, which will cause the CA root certificate to change.

If the client uses the system's root CA stores by default, such as Java and Go, you can easily connect securely to TiDB Serverless Tier clusters without specifying the path of CA roots.

However, some drivers and ORMs do not use the system root CA stores. In those cases, you need to configure the CA root path of the drivers or ORMs to your system root CA stores. For example, when you use [mysqlclient](https://github.com/PyMySQL/mysqlclient) to connect a TiDB Serverless Tier cluster in Python on macOS, you need to set `ca: /etc/ssl/cert.pem` in the `ssl` argument.

If you are using a GUI client, such as DBeaver, which does not accept a certificate file with multiple certificates inside, you must download the [ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt) certificate.

### Root certificate default path 

In different operating systems, the default download storage paths of the root certificate are as follows：

**MacOS**

```
/etc/ssl/cert.pem
```

**Debian / Ubuntu / Arch**

```
/etc/ssl/certs/ca-certificates.crt
```

**RedHat / Fedora / CentOS / Mageia**

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

**Windows**

Windows does not offer a specific path to the CA root. Instead, it uses the [registry](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores) to store certificates. For this reason, to specify the CA root path on Windows, take the following steps:

1. Download the [Mozilla CA Certificate bundle](https://curl.se/docs/caextract.html) and save it in a path you prefer, such as `<path_to_mozilla_ca_cert_bundle>`.
2. Use the path (`<path_to_mozilla_ca_cert_bundle>`) as your CA root path when you connect to a Serverless Tier cluster.

## FAQ

### Which TLS versions are supported to connect to my TiDB Cloud Serverless Tier cluster?

For security reasons, TiDB Cloud Serverless Tier clusters only support TLS 1.2 and TLS 1.3, and does not support TLS 1.0 and TLS 1.1 versions. See IETF [Deprecating TLS 1.0 and TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/) for details.

### Is two-way TLS authentication between my connection client and TiDB Cloud Serverless Tier supported?

No.

TiDB Serverless Tier only supports one-way TLS authentication, which means your client uses the public key to verify the signature of your TiDB Cloud cluster certificate's private key while the cluster does not validate the client.

### Does TiDB Serverless Tier have to configure TLS to establish a secure connection?

Yes.

TiDB Serverless Tier only allows TLS connections and prohibits non-SSL/TLS connections. The reason is that SSL/TLS is one of the most basic security measures for you to reduce the risk of data exposure to internet when you connect to the TiDB Serverless Tier cluster through internet.