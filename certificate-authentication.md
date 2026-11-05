---
title: Certificate-Based Authentication for Login
summary: Learn the certificate-based authentication used for login.
aliases: ['/docs/dev/certificate-authentication/','/docs/dev/reference/security/cert-based-authentication/']
---

# Certificate-Based Authentication for Login

TiDB supports a certificate-based authentication method for users to log into TiDB. With this method, TiDB issues certificates to different users, uses encrypted connections to transfer data, and verifies certificates when users log in. This approach is more secure than the traditional password-based authentication method commonly used by MySQL users and is thus adopted by an increasing number of users.

To use certificate-based authentication, you might need to perform the following operations:

+ Create security keys and certificates
+ Configure certificates for TiDB and the client
+ Configure the user certificate information to be verified when the user logs in
+ Update and replace certificates

The rest of the document introduces in detail how to perform these operations.

## Create security keys and certificates

<CustomContent platform="tidb">

It is recommended that you use [OpenSSL](https://www.openssl.org/) to create keys and certificates. The certificate generation process is similar to the process described in [Enable TLS Between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md). The following paragraphs demonstrate how to configure more attribute fields that need to be verified in the certificate.

</CustomContent>

<CustomContent platform="tidb-cloud">

It is recommended that you use [OpenSSL](https://www.openssl.org/) to create keys and certificates. The certificate generation process is similar to the process described in [Enable TLS Between TiDB Clients and Servers](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers). The following paragraphs demonstrate how to configure more attribute fields that need to be verified in the certificate.

</CustomContent>

### Generate CA key and certificate

1. Execute the following command to generate the CA key:

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

    The output of the above command:

    ```
    Generating RSA private key, 2048 bit long modulus (2 primes)
    ....................+++++
    ...............................................+++++
    e is 65537 (0x010001)
    ```

2. Execute the following command to generate the certificate corresponding to the CA key:

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.pem
    ```

3. Enter detailed certificate information. For example:

    ```bash
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Locality Name (e.g. city) []:San Francisco
    Organization Name (e.g. company) [Internet Widgits Pty Ltd]:PingCAP Inc.
    Organizational Unit Name (e.g. section) []:TiDB
    Common Name (e.g. server FQDN or YOUR name) []:TiDB admin
    Email Address []:s@pingcap.com
    ```

    > **Note:**
    >
    > In the above certificate details, texts after `:` are the entered information.

### Generate server key and certificate

1. Execute the following command to generate the server key:

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.pem -out server-req.pem
    ```

2. Enter detailed certificate information. For example:

    ```bash
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Locality Name (e.g. city) []:San Francisco
    Organization Name (e.g. company) [Internet Widgits Pty Ltd]:PingCAP Inc.
    Organizational Unit Name (e.g. section) []:TiKV
    Common Name (e.g. server FQDN or YOUR name) []:TiKV Test Server
    Email Address []:k@pingcap.com

    Please enter the following 'extra' attributes
    to be sent with your certificate request
    A challenge password []:
    An optional company name []:
    ```

3. Execute the following command to generate the RSA key of the server:

    ```bash
    sudo openssl rsa -in server-key.pem -out server-key.pem
    ```

    The output of the above command:

    ```bash
    writing RSA key
    ```

4. Use the CA certificate signature to generate the signed server certificate:

    ```bash
    sudo openssl x509 -req -in server-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem
    ```

    The output of the above command (for example):

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiKV, CN = TiKV Test Server, emailAddress = k@pingcap.com
    Getting CA Private Key
    ```

    > **Note:**
    >
    > When you log in, TiDB checks whether the information in the `subject` section of the above output is consistent or not.

### Generate client key and certificate

After generating the server key and certificate, you need to generate the key and certificate for the client. It is often necessary to generate different keys and certificates for different users.

1. Execute the following command to generate the client key:

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.pem -out client-req.pem
    ```

2. Enter detailed certificate information. For example:

    ```bash
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Locality Name (e.g. city) []:San Francisco
    Organization Name (e.g. company) [Internet Widgits Pty Ltd]:PingCAP Inc.
    Organizational Unit Name (e.g. section) []:TiDB
    Common Name (e.g. server FQDN or YOUR name) []:tpch-user1
    Email Address []:zz@pingcap.com

    Please enter the following 'extra' attributes
    to be sent with your certificate request
    A challenge password []:
    An optional company name []:
    ```

3. Execute the following command to generate the RSA key of the client:

    ```bash
    sudo openssl rsa -in client-key.pem -out client-key.pem
    ```

    The output of the above command:

    ```bash
    writing RSA key
    ```

4. Use the CA certificate signature to generate the client certificate:

    ```bash
    sudo openssl x509 -req -in client-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.pem
    ```

    The output of the above command (for example):

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiDB, CN = tpch-user1, emailAddress = zz@pingcap.com
    Getting CA Private Key
    ```

    > **Note:**
    >
    > The information of the `subject` section in the above output is used for [certificate configuration for login verification](#configure-the-user-certificate-information-for-login-verification) in the `REQUIRE` section.

### Verify certificate

Execute the following command to verify certificate:

```bash
openssl verify -CAfile ca-cert.pem server-cert.pem client-cert.pem
```

If the certificate is verified, you will see the following result:

```
server-cert.pem: OK
client-cert.pem: OK
```

## Configure TiDB and the client to use certificates

After generating the certificates, you need to configure the TiDB server and the client to use the corresponding server certificate or client certificate.

### Configure TiDB to use server certificate

Modify the `[security]` section in the TiDB configuration file. This step specifies the directory in which the CA certificate, the server key, and the server certificate are stored. You can replace `path/to/server-cert.pem`, `path/to/server-key.pem`, `path/to/ca-cert.pem` with your own directory.

```toml
[security]
ssl-cert = "path/to/server-cert.pem"
ssl-key = "path/to/server-key.pem"
ssl-ca = "path/to/ca-cert.pem"
```

Start TiDB and check logs. If the following information is displayed in the log, the configuration is successful:

```
[INFO] [server.go:286] ["mysql protocol server secure connection is enabled"] ["client verification enabled"=true]
```

### Configure the client to use client certificate

Configure the client so that the client uses the client key and certificate for login.

Taking the MySQL client as an example, you can use the newly created client certificate, client key and CA by specifying `ssl-cert`, `ssl-key`, and `ssl-ca`:

```bash
mysql -u test -h 0.0.0.0 -P 4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
```

> **Note:**
>
> `/path/to/client-cert.new.pem`, `/path/to/client-key.new.pem`, and `/path/to/ca-cert.pem` are the directory of the CA certificate, client key, and client certificate. You can replace them with your own directory.

## Configure the user certificate information for login verification

First, connect TiDB using the client to configure the login verification. Then, you can get and configure the user certificate information to be verified.

### Get user certificate information

The user certificate information can be specified by `REQUIRE SUBJECT`, `REQUIRE ISSUER`, `REQUIRE SAN`, and `REQUIRE CIPHER`, which are used to check the X.509 certificate attributes.

+ `REQUIRE SUBJECT`: Specifies the subject information of the client certificate when you log in. With this option specified, you do not need to configure `REQUIRE SSL` or `REQUIRE X509`. The information to be specified is consistent with the entered subject information in [Generate client keys and certificates](#generate-client-key-and-certificate).

    To get this option, execute the following command:

    ```bash
    openssl x509 -noout -subject -in client-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'
    ```

+ `REQUIRE ISSUER`: Specifies the `subject` information of the CA certificate that issues the user certificate. The information to be specified is consistent with the entered `subject` information in [Generate CA key and certificate](#generate-ca-key-and-certificate).

    To get this option, execute the following command:

    ```bash
    openssl x509 -noout -subject -in ca-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'
    ```

+ `REQUIRE SAN`: Specifies the `Subject Alternative Name` information of the CA certificate that issues the user certificate. The information to be specified is consistent with the [`alt_names` of the `openssl.cnf` configuration file](https://docs.pingcap.com/tidb/stable/generate-self-signed-certificates) used to generate the client certificate.

    + Execute the following command to get the information of the `REQUIRE SAN` item in the generated certificate:

        ```shell
        openssl x509 -noout -extensions subjectAltName -in client.crt
        ```

    + `REQUIRE SAN` currently supports the following `Subject Alternative Name` check items:

        - URI
        - IP
        - DNS

    + Multiple check items can be configured after they are connected by commas. For example, configure `REQUIRE SAN` as follows for the `u1` user:

        ```sql
        CREATE USER 'u1'@'%' REQUIRE SAN 'DNS:d1,URI:spiffe://example.org/myservice1,URI:spiffe://example.org/myservice2';
        ```

        The above configuration only allows the `u1` user to log in to TiDB using the certificate with the URI item `spiffe://example.org/myservice1` or `spiffe://example.org/myservice2` and the DNS item `d1`.

+ `REQUIRE CIPHER`: Checks the cipher method supported by the client. Use the following statement to check the list of supported cipher methods:

    ```sql
    SHOW SESSION STATUS LIKE 'Ssl_cipher_list';
    ```

### Configure user certificate information

After getting the user certificate information (`REQUIRE SUBJECT`, `REQUIRE ISSUER`, `REQUIRE SAN`, `REQUIRE CIPHER`), configure these information to be verified when creating a user, granting privileges, or altering a user. Replace `<replaceable>` with the corresponding information in the following statements.

You can configure one option or multiple options using the space or `and` as the separator.

+ Configure user certificate when creating a user (`CREATE USER`):

    ```sql
    CREATE USER 'u1'@'%' REQUIRE ISSUER '<replaceable>' SUBJECT '<replaceable>' SAN '<replaceable>' CIPHER '<replaceable>';
    ```

+ Configure user certificate when altering a user:

    ```sql
    ALTER USER 'u1'@'%' REQUIRE ISSUER '<replaceable>' SUBJECT '<replaceable>' SAN '<replaceable>' CIPHER '<replaceable>';
    ```

After the above configuration, the following items will be verified when you log in:

+ SSL is used; the CA that issues the client certificate is consistent with the CA configured in the server.
+ The `issuer` information of the client certificate matches the information specified in `REQUIRE ISSUER`.
+ The cipher used for the connection matches the one specified in `REQUIRE CIPHER`.
+ The `Subject Alternative Name` information of the client certificate matches the information specified in `REQUIRE SAN`.

You can log into TiDB only after all the above items are verified. Otherwise, the `ERROR 1045 (28000): Access denied` error is returned. You can use the following command to check the TLS version, the cipher algorithm and whether the current connection uses the certificate for the login.

Connect the MySQL client and execute the following statement:

```sql
\s
```

The output:

```
--------------
mysql  Ver 8.5.0 for Linux on x86_64 (MySQL Community Server - GPL)

Connection id:       1
Current database:    test
Current user:        root@127.0.0.1
SSL:                 Cipher in use is TLS_AES_128_GCM_SHA256
```

Then execute the following statement:

```sql
SHOW VARIABLES LIKE '%ssl%';
```

The output:

```
+---------------+----------------------------------+
| Variable_name | Value                            |
+---------------+----------------------------------+
| have_openssl  | YES                              |
| have_ssl      | YES                              |
| ssl_ca        | /path/to/ca-cert.pem             |
| ssl_cert      | /path/to/server-cert.pem         |
| ssl_cipher    |                                  |
| ssl_key       | /path/to/server-key.pem          |
+---------------+----------------------------------+
6 rows in set (0.06 sec)
```

## Update and replace certificate

The key and certificate are updated regularly. The following sections introduce how to update the key and certificate.

The CA certificate is the basis for mutual verification between the client and server. To replace the CA certificate, generate a combined certificate that supports the authentication for both old and new certificates. On the client and server, first replace the CA certificate, then replace the client/server key and certificate.

### Update CA key and certificate

1. Back up the old CA key and certificate (suppose that `ca-key.pem` is stolen):

    ```bash
    mv ca-key.pem ca-key.old.pem && \
    mv ca-cert.pem ca-cert.old.pem
    ```

2. Generate the new CA key:

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

3. Generate the new CA certificate using the newly generated CA key:

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.new.pem
    ```

    > **Note:**
    >
    > Generating the new CA certificate is to replace the keys and certificates on the client and server, and to ensure that online users are not affected. Therefore, the appended information in the above command must be consistent with the `REQUIRE ISSUER` information.

4. Generate the combined CA certificate:

    ```bash
    cat ca-cert.new.pem ca-cert.old.pem > ca-cert.pem
    ```

After the above operations, restart the TiDB server with the newly created combined CA certificate. Then the server accepts both the new and old CA certificates.

Also replace the old CA certificate with the combined certificate so that the client accepts both the old and new CA certificates.

### Update client key and certificate

> **Note:**
>
> Perform the following steps **only after** you have replaced the old CA certificate on the client and server with the combined CA certificate.

1. Generate the new RSA key of the client:

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.new.pem -out client-req.new.pem && \
    sudo openssl rsa -in client-key.new.pem -out client-key.new.pem
    ```

    > **Note:**
    >
    > The above command is to replace the client key and certificate, and to ensure that the online users are not affected. Therefore, the appended information in the above command must be consistent with the `REQUIRE SUBJECT` information.

2. Use the combined certificate and the new CA key to generate the new client certificate:

    ```bash
    sudo openssl x509 -req -in client-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.new.pem
    ```

3. Make the client (for example, MySQL) connect TiDB with the new client key and certificate:

    ```bash
    mysql -u test -h 0.0.0.0 -P 4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
    ```

    > **Note:**
    >
    > `/path/to/client-cert.new.pem`, `/path/to/client-key.new.pem`, and `/path/to/ca-cert.pem` specify the directory of the CA certificate, client key, and client certificate. You can replace them with your own directory.

### Update the server key and certificate

1. Generate the new RSA key of the server:

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.new.pem -out server-req.new.pem && \
    sudo openssl rsa -in server-key.new.pem -out server-key.new.pem
    ```

2. Use the combined CA certificate and the new CA key to generate the new server certificate:

    ```bash
    sudo openssl x509 -req -in server-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.new.pem
    ```

3. Configure the TiDB server to use the new server key and certificate. Place the files in the same directory specified in the [Configure TiDB to use server certificate](#configure-tidb-to-use-server-certificate) section.

    ```sql
    ALTER INSTANCE RELOAD TLS;
    ```

## Policy-based access control for certificates

TiDB supports policy-based access control (PBAC) for certificates, leveraging policies defined by the underlying key management server. This enables fine-grained control over access based on various criteria, such as time-based policies (for example, certificates only valid during specific hours), location-based policies (for example, restricting access to certain geographic locations), and other customizable conditions, ensuring enhanced security and flexibility in certificate management.
