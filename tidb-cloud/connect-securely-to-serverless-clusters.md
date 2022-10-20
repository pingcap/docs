---
title: Connect Securely to Serverless Tier Clusters
summary: Introduce TLS connection in TiDB Serverless.
---

# Connect Securely to Serverless Tier Clusters

This document introduces the core information about TLS in TiDB Serverless Tier.

## How do I connect to TiDB Serverless in TLS connection?

TiDB Cloud provides some connection examples in the **Connect** tab. You can follow the instructions in [Connect via standard connection](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) to connect to TiDB Serverless Tier.

Generally, enable TLS and offer a CA root path to authenticate the server. This helps you prevent a man-in-the-middle attack. Different clients have different operations in the TLS connection. Enable TLS and verify the server according to your actual use of the client.

## Can I disable TLS in Serverless?

No.

Serverless clusters allows only TLS connections and rejects normal connections. The reason for this is that users connect to Serverless Tier clusters through a public network, so communication security is really important.

## What TLS versions can I use?

TiDB Serverless only supports TLSv1.2 and TLSv1.3. 

TiDB Serverless uses TLSv1.2 as the default version. If you want another TLS version, you can specify the version in the connection strings. For example, If you use MySQL Client to connect TiDB Serverless, you can set `--tls-version=TLSv1.3` to enforce the TLSv1.3 version.

TiDB Serverless does not allow you to manually use other unsupported TLS versions.

## What certificates do I need？

TiDB Serverless uses certificates from [Let's Encrypt](https://letsencrypt.org/) as a Certificate Authority (CA) for TLS connection between clients and TiDB Serverless gateway. Usually, Let's Encrypt's root certificate is present in your system's root CA stores. You can easily connect securely to TiDB Serverless without specifying the path of CA roots, such as JAVA, Go, etc.

However, some drivers and ORMs do not use the system root CA stores. So you should make sure to add Let's Encrypt's root Certificate Authority ([ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt)) to your drivers' or ORMs' certificate store.

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

Now, TiDB Serverless uses one-sided TLS authentication, which means the server uses the public certificate pair to verify identity while the client can not. The client uses a username and password to authenticate itself. For example, when you use MySQL Client, you cannot configure `--ssl-cert` and `--ssl-key` in connection strings.