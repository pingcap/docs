---
title: Use Encrypted Connections
category: user guide
---

# Use Encrypted Connections

The TiDB server uses unencrypted connections by default. Therefore, the third party with the ability to monitor channel traffic can get the data sent and received between the TiDB server and client, including but not limited to the query statements and results. If the channel is not trustworthy, for example, the client is connected to the TiDB server through public network, then the non-encrypted connection can lead to information leakage. It is recommended to use the encrypted connection to ensure security.

The TiDB server supports the encrypted connection based on the TLS (Transport Layer Security). The protocol is consistent with MySQL encrypted connections and is directly supported by existing MySQL clients such as MySQL operation tools and MySQL drivers. TLS is formerly SSL, and is sometimes called SSL. Because the SSL protocol has known security vulnerabilities, TiDB does not support it. The TLS/SSL protocol versions that TiDB supports are TLS 1.0, TLS 1.1 and TLS 1.2.

After using an encrypted connection, the connection has the following security properties:

- Confidentiality: the traffic plaintext cannot be eavesdropped
- Integrity: the traffic plaintext cannot be tampered
- Authentication: (optional) the client and the server can verify the identity of both parties to avoid man-in-the-middle attacks

The encrypted connections in TiDB are disabled by default. To use encrypted connections in the client, first enable encrypted connections on the TiDB server. In addition, similar to MySQL, the encrypted connections in TiDB consist of single optional connection. For a TiDB server that enables encrypted connections, you can choose to securely connect to the TiDB server through an encrypted connection, or to use a general unencrypted connection. Most MySQL clients do not use encrypted connections by default, so generally the client is explicitly required to use an encrypted connection.

In short, to use encrypted connections, both of the following conditions must be satisfied:

1. Enable encrypted connections in the TiDB server.
2. The client specifies to use an encrypted connection.

## Configure TiDB to Use Encrypted Connections

When you start TiDB, specify at least the `ssl-cert` and `ssl-key` parameters in the configuration file to enable encrypted connections in the TiDB server. You can also specify the `ssl-ca` parameter for client authentication (see [Enable Authentication](#enable-authentication)).

- [`ssl-cert`](server-command-option.md#ssl-cert): specifies the file path of the SSL certificate
- [`ssl-key`](server-command-option.md#ssl-key): specifies the private key that matches the certificate
- [`ssl-ca`](server-command-option.md#ssl-ca): (optional) specifies the file path of the trusted CA certificate

All the files specified by the parameters are in PEM format. Currently, TiDB does not support the import of a password-protected private key, so it is required to provide a private key file without a password. If the certificate or private key is invalid, the TiDB server starts as usual, but the client cannot connect to the TiDB server through an encrypted connection.

The certificate or key above is signed and generated using OpenSSL, or quickly generated using the `mysql_ssl_rsa_setup` tool in MySQL:

```bash
mysql_ssl_rsa_setup --datadir=./certs
```

The command above generates the following files in the `certs` directory:

```
certs
├── ca-key.pem
├── ca.pem
├── client-cert.pem
├── client-key.pem
├── private_key.pem
├── public_key.pem
├── server-cert.pem
└── server-key.pem
```

The corresponding TiDB configuration file parameters are:

```toml
[security]
ssl-cert = "certs/server-cert.pem"
ssl-key = "certs/server-key.pem"
```

If the certificate parameters are correct, TiDB outputs `Secure connection is enabled` when started, otherwise it outputs `Secure connection is NOT ENABLED`.

## Configure the MySQL Client to Use Encrypted Connections

The client of MySQL 5.7 or higher versions attempts to establish an encrypted connection by default. If the server does not support encrypted connections, it automatically returns to unencrypted connections. The client of MySQL earlier than version 5.7 uses the unencrypted connection by default.

Update the connection behavior of the client using the following command line parameters:

- The client requires an encrypted connection and fails if one cannot be established (`--ssl-mode=REQUIRED`).
- The client attempts to connect using encryption, falling back to an unencrypted connection if an encrypted connection cannot be established.
- The client uses an unencrypted connection (`--ssl-mode=DISABLED`).

For more information, see [Client-Side Configuration for Encrypted Connections](https://dev.mysql.com/doc/refman/5.7/en/using-encrypted-connections.html#using-encrypted-connections-client-side-configuration) in MySQL.

## Enable Authentication

If the `ssl-ca` parameter is not specified in the TiDB server or MySQL client, the client or the server does not perform authentication by default and cannot prevent man-in-the-middle attack. For example, the client might "securely" connect to a disguised client. You can configure the `ssl-ca` parameter for authentication in the server and client. Generally, you only need to authenticate the identity of the server, but you can also authenticate the client identity to further enhance the security.

- To have the MySQL client authenticate the TiDB server identity, it is required to configure the `ssl-cert` and` ssl-key` parameters in the TiDB server, to specify the `--ssl-ca` parameter in the client, and to configure the `--ssl-mode` to `VERIFY_IDENTITY` at least. In addition, make sure that the certificate (`ssl-cert`) configured by the TiDB server is signed by the CA specified by the client `--ssl-ca` parameter, otherwise the authentication fails. 
- To have the TiDB server authenticate the MySQL client identity, it is required to configure the `ssl-cert`, `ssl-key` and `ssl-ca` parameters in the TiDB server and to specify the `--ssl-cert` and `--ssl-key` parameters in the client. In addition, make suer that the server-configured certificate and the client-configured certificate are both signed by the `ssl-ca` specified by the server.
- To perform mutual authentication, meet both of the above requirements. 

> **Note**: Currently, it is not required in TiDB to authenticate the client identity. In other words, it is optional to have the server authenticate the client identity. If the client does not present its identity certificate in the TLS handshake, the TLS connection can also be successfully established.

## Check Whether the Current Connection Uses Encryption

Use the `SHOW STATUS LIKE "%Ssl%";` statement to get the details of the current connection, including whether encryption is used, the encryption protocol used by encrypted connections, the TLS version number and so on.

The results of running the above statement in an encrypted connection are as follows. The results change according to different TLS versions or encryption protocols supported by the client.

```
mysql> SHOW STATUS LIKE "%Ssl%";
......
| Ssl_verify_mode | 5                            |
| Ssl_version     | TLSv1.2                      |
| Ssl_cipher      | ECDHE-RSA-AES128-GCM-SHA256  |
......
```

Besides, for the client that comes with MySQL, you can also use the `STATUS` or `\s` statement to view the connection status:

```
mysql> \s
...
SSL: Cipher in use is ECDHE-RSA-AES128-GCM-SHA256
...
```

## Supported TLS Versions, Key Exchange Protocols and Encryption Algorithms

The TLS versions, key exchange protocols and encryption algorithms supported by TiDB are determined by the official Golang.

### Supported TLS Versions

- TLS 1.0
- TLS 1.1
- TLS 1.2

### Supported Key Exchange Protocols and Encryption Algorithms

- TLS\_RSA\_WITH\_RC4\_128\_SHA
- TLS\_RSA\_WITH\_3DES\_EDE\_CBC\_SHA
- TLS\_RSA\_WITH\_AES\_128\_CBC\_SHA
- TLS\_RSA\_WITH\_AES\_256\_CBC\_SHA
- TLS\_RSA\_WITH\_AES\_128\_CBC\_SHA256
- TLS\_RSA\_WITH\_AES\_128\_GCM\_SHA256
- TLS\_RSA\_WITH\_AES\_256\_GCM\_SHA384
- TLS\_ECDHE\_ECDSA\_WITH\_RC4\_128\_SHA
- TLS\_ECDHE\_ECDSA\_WITH\_AES\_128\_CBC\_SHA
- TLS\_ECDHE\_ECDSA\_WITH\_AES\_256\_CBC\_SHA
- TLS\_ECDHE\_RSA\_WITH\_RC4\_128\_SHA
- TLS\_ECDHE\_RSA\_WITH\_3DES\_EDE\_CBC\_SHA
- TLS\_ECDHE\_RSA\_WITH\_AES\_128\_CBC\_SHA
- TLS\_ECDHE\_RSA\_WITH\_AES\_256\_CBC\_SHA
- TLS\_ECDHE\_ECDSA\_WITH\_AES\_128\_CBC\_SHA256
- TLS\_ECDHE\_RSA\_WITH\_AES\_128\_CBC\_SHA256
- TLS\_ECDHE\_RSA\_WITH\_AES\_128\_GCM\_SHA256
- TLS\_ECDHE\_ECDSA\_WITH\_AES\_128\_GCM\_SHA256
- TLS\_ECDHE\_RSA\_WITH\_AES\_256\_GCM\_SHA384
- TLS\_ECDHE\_ECDSA\_WITH\_AES\_256\_GCM\_SHA384
- TLS\_ECDHE\_RSA\_WITH\_CHACHA20\_POLY1305
- TLS\_ECDHE\_ECDSA\_WITH\_CHACHA20\_POLY1305
