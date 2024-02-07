---
title: Security Compatibility with MySQL
summary: Learn TiDB's security compatibilities with MySQL.
---

# Security Compatibility with MySQL

TiDB supports security features similar to MySQL 5.7, and also supports some security features of MySQL 8.0. The security features of TiDB are different from MySQL in implementation.

## Unsupported security features

- Column level permissions.
- These permission attributes: `max_questions`, `max_updated`, and `max_user_connections`.
- Password verification policy, which requires you to verify the current password when you change it.
- Dual password policy.
- Random password generation.
- Multi-factor authentication.

## Differences with MySQL

### Password expiration policy

The password expiration policies of TiDB and MySQL have the following differences:

- MySQL supports password expiration policy in v5.7 and v8.0.
- TiDB supports password expiration policy starting from v6.5.0.

The expiration mechanism of TiDB is different from MySQL in the following aspects:

- In MySQL v5.7 and v8.0, the configuration of the client and the server combined together determines whether to enable "sandbox mode" for the client connection.
- In TiDB, the [`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) configuration item alone determines whether to enable "sandbox mode" for the client connection.

### Password complexity policy

The password complexity policies of TiDB and MySQL have the following differences:

- MySQL v5.7 implements the password complexity policy by using the `validate_password` plugin.
- MySQL v8.0 re-implements the password complexity policy by using the `validate_password` component.
- TiDB introduces a built-in password complexity management feature starting from v6.5.0.

The feature implementation has the following differences:

- Enable the feature:

    - In MySQL v5.7, the feature is implemented by using the `validate_password` plugin. You can enable the feature by installing the plugin.
    - In MySQL v8.0, the feature is implemented by using the `validate_password` component. You can enable the feature by installing the component.
    - For TiDB, this feature is built-in. You can enable the feature using the system variable [`validate_password.enable`](/system-variables.md#validate_passwordenable-new-in-v650).

- Dictionary check:

    - In MySQL v5.7, you can specify a file path using the `validate_password_dictionary_file` variable. The file contains a list of words that are not allowed to exist in passwords.
    - In MySQL v8.0, you can specify a file path using the `validate_password.dictionary_file` variable. The file contains a list of words that are not allowed to exist in passwords.
    - In TiDB, you can specify a string using the [`validate_password.dictionary`](/system-variables.md#validate_passworddictionary-new-in-v650) system variable. The string contains a list of words that are not allowed to exist in passwords.

### Password failure tracking

The password failure tracking policies of TiDB and MySQL have the following differences:

- MySQL v5.7 does not support password failure tracking.
- MySQL v8.0 supports password failure tracking.
- TiDB supports password failure tracking starting from v6.5.0.

Because the number of failed attempts and lock status of accounts need to be globally consistent, and as a distributed database, TiDB cannot record the number of failed attempts and lock status in the server memory like MySQL, so the implementation mechanisms are different between TiDB and MySQL.

- For users that are not locked automatically, the count of failed attempts is reset in the following scenarios:

    + MySQL 8.0:

        - When the server is restarted, the count of failed attempts for all accounts is reset.
        - When `FLUSH PRIVILEGES` is executed, the count of failed attempts for all accounts is reset.
        - When you run `ALTER USER ... ACCOUNT UNLOCK` to unlock an account, the count is reset.
        - When an account logs in successfully, the count is reset.

    + TiDB:

        - When you run `ALTER USER ... ACCOUNT UNLOCK` to unlock an account, the count is reset.
        - When an account logs in successfully, the count is reset.

- For users that are locked automatically, the count of failed attempts is reset in the following scenarios:

    + MySQL 8.0:

        - When the server is restarted, the temporary locking for all accounts is reset.
        - When `FLUSH PRIVILEGES` is executed, the temporary locking for all accounts is reset.
        - If the lock time of an account ends, the temporary locking for the account is reset on the next login attempt.
        - When you run `ALTER USER ... ACCOUNT UNLOCK` to unlock an account, the temporary locking for the account is reset.

    + TiDB:

        - If the lock time of an account ends, the temporary locking for the account is reset on the next login attempt.
        - When you run `ALTER USER ... ACCOUNT UNLOCK` to unlock an account, the temporary locking for the account is reset.

### Password reuse policy

The password reuse policies of TiDB and MySQL have the following differences:

- MySQL v5.7 does not support password reuse management.
- MySQL v8.0 supports password reuse management.
- TiDB supports password reuse management starting from v6.5.0.

The implementation mechanisms are consistent between TiDB and MySQL. Both use the `mysql.password_history` system table to implement the password reuse management feature. However, when deleting a user that does not exist in the `mysql.user` system table, TiDB and MySQL have different behaviors:

- Scenario: A user (`user01`) is not created in a normal way; instead, it is created by using the `INSERT INTO mysql.password_history VALUES (...)` statement to append a record of `user01` to the `mysql.password_history` system table. In such cases, because the record of `user01` does not exist in the `mysql.user` system table, when you run `DROP USER` on `user01`, TiDB and MySQL have different behaviors.

    - MySQL: When you run `DROP USER user01`, MySQL tries to find `user01` in `mysql.user` and `mysql.password_history`. If either system table contains `user01`, the `DROP USER` statement is executed successfully and no error is reported.
    - TiDB: When you run `DROP USER user01`, TiDB tries to find `user01` only in `mysql.user`. If no related record is found, the `DROP USER` statement fails and an error is reported. If you want to execute the statement successfully and delete the `user01` record from `mysql.password_history`, use `DROP USER IF EXISTS user01` instead.

## Authentication plugin status

TiDB supports multiple authentication methods. These methods can be specified on a per user basis using [`CREATE USER`](/sql-statements/sql-statement-create-user.md) and [`ALTER USER`](/sql-statements/sql-statement-alter-user.md). These methods are compatible with the authentication methods of MySQL with the same names.

You can use one of the following supported authentication methods in the table. To specify a default method that the server advertises when the client-server connection is being established, set the [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin) variable. `tidb_sm3_password` is the SM3 authentication method only supported in TiDB. Therefore, to authenticate using this method, you must connect to TiDB using [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3). `tidb_auth_token` is a JSON Web Token (JWT) based authentication method used in TiDB Cloud, which can also be used for TiDB Self-Hosted after configuration.

<CustomContent platform="tidb">

The support for TLS authentication is configured differently. For detailed information, see [Enable TLS between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

The support for TLS authentication is configured differently. For detailed information, see [Enable TLS between TiDB Clients and Servers](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers).

</CustomContent>

| Authentication Method        | Supported        |
| :----------------------------| :--------------- |
| `mysql_native_password`      | Yes              |
| `sha256_password`            | No               |
| `caching_sha2_password`      | Yes, since 5.2.0 |
| `auth_socket`                | Yes, since 5.3.0 |
| `tidb_sm3_password`          | Yes, since 6.3.0 |
| `tidb_auth_token`            | Yes, since 6.4.0 |
| `authentication_ldap_sasl`   | Yes, since 7.1.0 |
| `authentication_ldap_simple` | Yes, since 7.1.0 |
| TLS Certificates             | Yes              |
| LDAP                         | Yes, since 7.1.0 |
| PAM                          | No               |
| ed25519 (MariaDB)            | No               |
| GSSAPI (MariaDB)             | No               |
| FIDO                         | No               |

### `tidb_auth_token`

`tidb_auth_token` is a passwordless authentication method based on [JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519). In v6.4.0, `tidb_auth_token` is only used for user authentication in TiDB Cloud. Starting from v6.5.0, you can also configure `tidb_auth_token` as a user authentication method for TiDB Self-Hosted. Different from password-based authentication methods such as `mysql_native_passsword` and `caching_sha2_password`, when creating users using `tidb_auth_token`, there is no need to set or store custom passwords. To log into TiDB, users only need to use a signed token instead of a password, which simplifies the authentication process and improves security.

JWT consists of 3 parts: Header, Payload, and Signature. After being encoded using base64, they are concatenated into a stirng separated by dots (`.`).

The Header describe the meta data of the JWT, including 3 parameters:

* `alg` means the algorithm for signature, default as `RS256`
* `typ` means the type of token, unified as `JWT`
* `kid` means the key id for generating token signature

Here is an example for Header:

```json
{
  "alg": "RS256",
  "kid": "the-key-id-0",
  "typ": "JWT"
}
```

The Payload is the main part of JWT, which stores the user information in *clains*. These claims are required by `tidb_auth_token` users:

* `iss`: if `TOKEN_ISSUER` is not set or set to empty when [`CREATE USER`](/sql-statements/sql-statement-create-user.md), this claim is not required; or this claim should be the same as the setting value
* `sub`: this claim is required to be the same as the user name
* `iat`: means `issued at`. In TiDB, it is required not to be later than the time of authentication and not earlier than 15 minutes before authentication
* `exp`: means `expiration time`. If it is earlier than the time of authentication, the authentication fails

In addition, some other claim(s) are required in TiDB:

* `email`: The email can be specified when creating user by `ATTRIBUTE '{"email": "xxxx@pingcap.com"}`. If no email was giving when creating user, this claim should be set as an empty string; or it should be the same as the specified value

Here are some valid Payload examples:

```json
{
  "email": "user@pingcap.com",
  "exp": 1703305494,
  "iat": 1703304594,
  "iss": "issuer-abc",
  "sub": "user@pingcap.com"
}
```

The Payload is allowed not to contain `iss` claim:

```json
{
  "email": "",
  "exp": 1703305494,
  "iat": 1703304594,
  "sub": "user@pingcap.com"
}
```

The Signature signs the above two parts.

> **Warning:**
>
> 1. The encoding of the Header and Payload in base64 is reversible. Please do not attach any sensitive information in them
> 2. The `tidb_auth_token` authentication requires that the client supports [`mysql_clear_password`](https://dev.mysql.com/doc/refman/8.0/en/cleartext-pluggable-authentication.html) plugin to send the token to TiDB in clear text. Therefore, please [enale TLS between clients and servers](/enable-tls-between-clients-and-servers.md) before using `tidb_auth_token`

Here are the steps to config before using `tidb_auth_token`:

1. Config [`auth-token-jwks`](/tidb-configuration-file.md#auth-token-jwks-new-in-v640) and [`auth-token-refresh-interval`](/tidb-configuration-file.md#auth-token-refresh-interval-new-in-v640) in the configuration file
2. Save the JWKS periodly to the path specified by `auth-token-jwks`
3. Create a user with `tidb_auth_token`, and sepcify `iss` and `email` by `REQUIRE TOKEN_ISSUER` and `ATTRIBUTE '{"email": "xxxx@pingcap.com"}`
4. Generate and sign a token used for authentication, authencating with mysql client's `mysql_clear_text` plugin

#### Example

1. Install JWT genration tool by `go install github.com/cbcwestwolf/generate_jwt`. This tool is only used for testing `tidb_auth_token`
2. Get the example JWKS: `wget https://raw.githubusercontent.com/CbcWestwolf/generate_jwt/master/JWKS.json`
3. Config the path of above JWKS in `config.toml`:

    ```toml
    [security]
    auth-token-jwks = "JWKS.json"
    ```

4. start `tidb-server`
5. create a user `user@pingcap.com` with `tidb_auth_token`

    ```sql
    CREATE USER 'user@pingcap.com' IDENTIFIED WITH 'tidb_auth_token' REQUIRE TOKEN_ISSUER 'issuer-abc' ATTRIBUTE '{"email": "user@pingcap.com"}';
    ```

##### Authentication

Generate a token by `generate_jwt`:

```text
generate_jwt --kid "the-key-id-0" --sub "user@pingcap.com" --email "user@pingcap.com" --iss "issuer-abc"
```

It prints the public key and token like:

```text
-----BEGIN PUBLIC KEY-----
MIIBCgKCAQEAq8G5n9XBidxmBMVJKLOBsmdOHrCqGf17y9+VUXingwDUZxRp2Xbu
LZLbJtLgcln1lC0L9BsogrWf7+pDhAzWovO6Ai4Aybu00tJ2u0g4j1aLiDdsy0gy
vSb5FBoL08jFIH7t/JzMt4JpF487AjzvITwZZcnsrB9a9sdn2E5B/aZmpDGi2+Is
f5osnlw0zvveTwiMo9ba416VIzjntAVEvqMFHK7vyHqXbfqUPAyhjLO+iee99Tg5
AlGfjo1s6FjeML4xX7sAMGEy8FVBWNfpRU7ryTWoSn2adzyA/FVmtBvJNQBCMrrA
hXDTMJ5FNi8zHhvzyBKHU0kBTS1UNUbP9wIDAQAB
-----END PUBLIC KEY-----

eyJhbGciOiJSUzI1NiIsImtpZCI6InRoZS1rZXktaWQtMCIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXJAcGluZ2NhcC5jb20iLCJleHAiOjE3MDMzMDU0OTQsImlhdCI6MTcwMzMwNDU5NCwiaXNzIjoiaXNzdWVyLWFiYyIsInN1YiI6InVzZXJAcGluZ2NhcC5jb20ifQ.T4QPh2hTB5on5xCuvtWiZiDTuuKvckggNHtNaovm1F4RvwUv15GyOqj9yMstE-wSoV5eLEcPC2HgE6eN1C6yH_f4CU-A6n3dm9F1w-oLbjts7aYCl8OHycVYnq609fNnb8JLsQAmd1Zn9C0JW899-WSOQtvjLqVSPe9prH-cWaBVDQXzUJKxwywQzk9v-Z1Njt9H3Rn9vvwwJEEPI16VnaNK38I7YG-1LN4fAG9jZ6Zwvz7vb_s4TW7xccFf3dIhWTEwOQ5jDPCeYkwraRXU8NC6DPF_duSrYJc7d7Nu9Z2cr-E4i1Rt_IiRTuIIzzKlcQGg7jd9AGEfGe_SowsA-w
```

Copy the above token in the last line for authentication:

```Shell
mycli -h 127.0.0.1 -P 4000 -u 'user@pingcap.com' -p '<the-token-generated>'
```

Note that the mysql client here should support `mysql_clear_password` plugin. [mycli](https://www.mycli.net/) supports and enable this plugin default. If using [mysql command-line client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html), an option `--enable-cleartext-plugin` is required to enable this plugin.

```Shell
mysql -h 127.0.0.1 -P 4000 -u 'user@pingcap.com' -p'<the-token-generated>' --enable-cleartext-plugin
```

If specifying wrong `--sub` when generating token, like `--sub "wronguser@pingcap.com`, the authentication using this token would fail.

You can encode and decode a token with the help of the debugger in [jwt.io](https://jwt.io/).