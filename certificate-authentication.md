---
title: Certificate-Based Authentication for Login
summary: Learn the certificate-based authentication used for login.
---

# ログイン用の証明書ベースの認証 {#certificate-based-authentication-for-login}

TiDBは、ユーザーがTiDBにログインするための証明書ベースの認証方法をサポートしています。この方法では、TiDBはさまざまなユーザーに証明書を発行し、暗号化された接続を使用してデータを転送し、ユーザーがログインするときに証明書を検証します。このアプローチは、MySQLユーザーが一般的に使用する従来のパスワードベースの認証方法よりも安全であるため、ユーザー数の増加。

証明書ベースの認証を使用するには、次の操作を実行する必要がある場合があります。

-   セキュリティキーと証明書を作成する
-   TiDBとクライアントの証明書を構成する
-   ユーザーがログインしたときに検証されるユーザー証明書情報を構成します
-   証明書の更新と置換

ドキュメントの残りの部分では、これらの操作を実行する方法を詳しく紹介します。

## セキュリティキーと証明書を作成する {#create-security-keys-and-certificates}

キーと証明書の作成には[OpenSSL](https://www.openssl.org/)を使用することをお勧めします。証明書の生成プロセスは、 [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)で説明したプロセスと同様です。次の段落では、証明書で検証する必要のある属性フィールドをさらに構成する方法について説明します。

### CAキーと証明書を生成する {#generate-ca-key-and-certificate}

1.  次のコマンドを実行して、CAキーを生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

    上記のコマンドの出力：

    ```
    Generating RSA private key, 2048 bit long modulus (2 primes)
    ....................+++++
    ...............................................+++++
    e is 65537 (0x010001)
    ```

2.  次のコマンドを実行して、CAキーに対応する証明書を生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.pem
    ```

3.  詳細な証明書情報を入力します。例えば：

    {{< copyable "" >}}

    ```bash
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Locality Name (e.g. city) []:San Francisco
    Organization Name (e.g. company) [Internet Widgits Pty Ltd]:PingCAP Inc.
    Organizational Unit Name (e.g. section) []:TiDB
    Common Name (e.g. server FQDN or YOUR name) []:TiDB admin
    Email Address []:s@pingcap.com
    ```

    > **ノート：**
    >
    > 上記の証明書の詳細では、 `:`の後のテキストが入力された情報です。

### サーバーキーと証明書を生成する {#generate-server-key-and-certificate}

1.  次のコマンドを実行して、サーバーキーを生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.pem -out server-req.pem
    ```

2.  詳細な証明書情報を入力します。例えば：

    {{< copyable "" >}}

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

3.  次のコマンドを実行して、サーバーのRSAキーを生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl rsa -in server-key.pem -out server-key.pem
    ```

    上記のコマンドの出力：

    ```bash
    writing RSA key
    ```

4.  CA証明書の署名を使用して、署名されたサーバー証明書を生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl x509 -req -in server-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem
    ```

    上記のコマンドの出力（例）：

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiKV, CN = TiKV Test Server, emailAddress = k@pingcap.com
    Getting CA Private Key
    ```

    > **ノート：**
    >
    > ログインすると、TiDBは上記の出力の`subject`セクションの情報に一貫性があるかどうかを確認します。

### クライアントキーと証明書を生成する {#generate-client-key-and-certificate}

サーバーのキーと証明書を生成した後、クライアントのキーと証明書を生成する必要があります。多くの場合、ユーザーごとに異なるキーと証明書を生成する必要があります。

1.  次のコマンドを実行して、クライアントキーを生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.pem -out client-req.pem
    ```

2.  詳細な証明書情報を入力します。例えば：

    {{< copyable "" >}}

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

3.  次のコマンドを実行して、クライアントのRSAキーを生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl rsa -in client-key.pem -out client-key.pem
    ```

    上記のコマンドの出力：

    ```bash
    writing RSA key
    ```

4.  CA証明書の署名を使用して、クライアント証明書を生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl x509 -req -in client-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.pem
    ```

    上記のコマンドの出力（例）：

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiDB, CN = tpch-user1, emailAddress = zz@pingcap.com
    Getting CA Private Key
    ```

    > **ノート：**
    >
    > 上記の出力の`subject`セクションの情報は、 `require`セクションの[ログイン検証用の証明書構成](#configure-the-user-certificate-information-for-login-verification)に使用されます。

### 証明書を確認する {#verify-certificate}

次のコマンドを実行して、証明書を確認します。

{{< copyable "" >}}

```bash
openssl verify -CAfile ca-cert.pem server-cert.pem client-cert.pem
```

証明書が検証されると、次の結果が表示されます。

```
server-cert.pem: OK
client-cert.pem: OK
```

## 証明書を使用するようにTiDBとクライアントを構成する {#configure-tidb-and-the-client-to-use-certificates}

証明書を生成した後、対応するサーバー証明書またはクライアント証明書を使用するようにTiDBサーバーとクライアントを構成する必要があります。

### サーバー証明書を使用するようにTiDBを構成する {#configure-tidb-to-use-server-certificate}

TiDB構成ファイルの`[security]`セクションを変更します。この手順では、CA証明書、サーバーキー、およびサーバー証明書が保存されているディレクトリを指定します。 `path/to/server-cert.pem`を独自のディレクトリに`path/to/ca-cert.pem`ことができ`path/to/server-key.pem` 。

{{< copyable "" >}}

```
[security]
ssl-cert ="path/to/server-cert.pem"
ssl-key ="path/to/server-key.pem"
ssl-ca="path/to/ca-cert.pem"
```

TiDBを起動し、ログを確認します。次の情報がログに表示されている場合、構成は成功しています。

```
[INFO] [server.go:264] ["secure connection is enabled"] ["client verification enabled"=true]
```

### クライアント証明書を使用するようにクライアントを構成する {#configure-the-client-to-use-client-certificate}

クライアントがログインにクライアントキーと証明書を使用するようにクライアントを構成します。

MySQLクライアントを例にとると、 `ssl-cert` 、および`ssl-key`を指定することで、新しく作成されたクライアント証明書、クライアントキー、およびCAを使用でき`ssl-ca` 。

{{< copyable "" >}}

```bash
mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
```

> **ノート：**
>
> `/path/to/client-cert.new.pem` 、および`/path/to/client-key.new.pem`は、CA証明書、クライアントキー、およびクライアント証明書のディレクトリ`/path/to/ca-cert.pem` 。それらを独自のディレクトリに置き換えることができます。

## ログイン検証用のユーザー証明書情報を構成する {#configure-the-user-certificate-information-for-login-verification}

まず、クライアントを使用してTiDBに接続し、ログイン検証を構成します。次に、検証するユーザー証明書情報を取得して構成できます。

### ユーザー証明書情報を取得する {#get-user-certificate-information}

ユーザー証明書情報は、X509証明書の属性を確認するために使用される`require subject` 、および`require issuer`で`require cipher`でき`require san` 。

-   `require subject` ：ログイン時にクライアント証明書の`subject`の情報を指定します。このオプションを指定すると、 `require ssl`またはx509を構成する必要はありません。指定する情報は、 [クライアントキーと証明書を生成する](#generate-client-key-and-certificate)に入力した`subject`の情報と一致しています。

    このオプションを取得するには、次のコマンドを実行します。

    {{< copyable "" >}}

    ```bash
    openssl x509 -noout -subject -in client-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'
    ```

-   `require issuer` ：ユーザー証明書を発行するCA証明書の`subject`の情報を指定します。指定する情報は、 [CAキーと証明書を生成する](#generate-ca-key-and-certificate)に入力した`subject`の情報と一致しています。

    このオプションを取得するには、次のコマンドを実行します。

    {{< copyable "" >}}

    ```bash
    openssl x509 -noout -subject -in ca-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'
    ```

-   `require san` ：ユーザー証明書を発行するCA証明書の`Subject Alternative Name`の情報を指定します。指定する情報は、クライアント証明書の生成に使用される[`alt_names`構成ファイルの<code>openssl.cnf</code>](/generate-self-signed-certificates.md)と一致しています。

    -   次のコマンドを実行して、生成された証明書の`require san`の項目の情報を取得します。

        {{< copyable "" >}}

        ```shell
        openssl x509 -noout -extensions subjectAltName -in client.crt
        ```

    -   `require san`は現在、次の`Subject Alternative Name`のチェック項目をサポートしています。

        -   URI
        -   IP
        -   DNS

    -   複数のチェック項目は、コンマで接続した後に設定できます。たとえば、 `u1`のユーザーに対して次のように`require san`を構成します。

        {{< copyable "" >}}

        ```sql
        create user 'u1'@'%' require san 'DNS:d1,URI:spiffe://example.org/myservice1,URI:spiffe://example.org/myservice2'
        ```

        上記の構成では、 `u1`人のユーザーがURI項目`spiffe://example.org/myservice1`または`spiffe://example.org/myservice2`とDNS項目`d1`の証明書を使用してTiDBにログインすることのみが許可されています。

-   `require cipher` ：クライアントがサポートしている暗号方式を確認します。次のステートメントを使用して、サポートされている暗号化方式のリストを確認します。

    {{< copyable "" >}}

    ```sql
    SHOW SESSION STATUS LIKE 'Ssl_cipher_list';
    ```

### ユーザー証明書情報を構成する {#configure-user-certificate-information}

ユーザー証明書情報（ `require subject` ）を`require cipher`し`require san` 、ユーザーの作成、特権の付与、またはユーザーの変更時に検証されるようにこれらの情報を構成し`require issuer` 。 `<replaceable>`を次のステートメントの対応する情報に置き換えます。

スペースまたは`and`を区切り文字として使用して、1つまたは複数のオプションを構成できます。

-   ユーザーを作成するときにユーザー証明書を構成する（ `create user` ）：

    {{< copyable "" >}}

    ```sql
    create user 'u1'@'%' require issuer '<replaceable>' subject '<replaceable>' san '<replaceable>' cipher '<replaceable>';
    ```

-   特権を付与するときにユーザー証明書を構成します。

    {{< copyable "" >}}

    ```sql
    grant all on *.* to 'u1'@'%' require issuer '<replaceable>' subject '<replaceable>' san '<replaceable>' cipher '<replaceable>';
    ```

-   ユーザーを変更するときにユーザー証明書を構成します。

    {{< copyable "" >}}

    ```sql
    alter user 'u1'@'%' require issuer '<replaceable>' subject '<replaceable>' san '<replaceable>' cipher '<replaceable>';
    ```

上記の設定後、ログイン時に次の項目が確認されます。

-   SSLが使用されます。クライアント証明書を発行するCAは、サーバで設定されているCAと一致しています。
-   クライアント証明書の`issuer`情報は、 `require issuer`で指定された情報と一致します。
-   クライアント証明書の`subject`情報は、 `require cipher`で指定された情報と一致します。
-   クライアント証明書の`Subject Alternative Name`情報は、 `require san`で指定された情報と一致します。

上記のすべての項目が確認された後にのみ、TiDBにログインできます。それ以外の場合は、 `ERROR 1045 (28000): Access denied`エラーが返されます。次のコマンドを使用して、TLSバージョン、暗号化アルゴリズム、および現在の接続がログインに証明書を使用しているかどうかを確認できます。

MySQLクライアントを接続し、次のステートメントを実行します。

{{< copyable "" >}}

```sql
\s
```

出力：

```
--------------
mysql  Ver 15.1 Distrib 10.4.10-MariaDB, for Linux (x86_64) using readline 5.1

Connection id:       1
Current database:    test
Current user:        root@127.0.0.1
SSL:                 Cipher in use is TLS_AES_256_GCM_SHA384
```

次に、次のステートメントを実行します。

{{< copyable "" >}}

```sql
show variables like '%ssl%';
```

出力：

```
+---------------+----------------------------------+
| Variable_name | Value                            |
+---------------+----------------------------------+
| ssl_cert      | /path/to/server-cert.pem         |
| ssl_ca        | /path/to/ca-cert.pem             |
| have_ssl      | YES                              |
| have_openssl  | YES                              |
| ssl_key       | /path/to/server-key.pem          |
+---------------+----------------------------------+
6 rows in set (0.067 sec)
```

## 証明書の更新と交換 {#update-and-replace-certificate}

キーと証明書は定期的に更新されます。次のセクションでは、キーと証明書を更新する方法を紹介します。

CA証明書は、クライアントとサーバー間の相互検証の基礎です。 CA証明書を置き換えるには、古い証明書と新しい証明書の両方の認証をサポートする結合証明書を生成します。クライアントとサーバーで、最初にCA証明書を置き換え、次にクライアント/サーバーキーと証明書を置き換えます。

### CAキーと証明書を更新します {#update-ca-key-and-certificate}

1.  古いCAキーと証明書をバックアップします（ `ca-key.pem`が盗まれたと仮定します）。

    {{< copyable "" >}}

    ```bash
    mv ca-key.pem ca-key.old.pem && \
    mv ca-cert.pem ca-cert.old.pem
    ```

2.  新しいCAキーを生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

3.  新しく生成されたCAキーを使用して新しいCA証明書を生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.new.pem
    ```

    > **ノート：**
    >
    > 新しいCA証明書を生成することは、クライアントとサーバーのキーと証明書を置き換え、オンラインユーザーが影響を受けないようにすることです。したがって、上記のコマンドに追加される情報は、 `require issuer`の情報と一致している必要があります。

4.  結合されたCA証明書を生成します。

    {{< copyable "" >}}

    ```bash
    cat ca-cert.new.pem ca-cert.old.pem > ca-cert.pem
    ```

上記の操作の後、新しく作成された結合CA証明書を使用してTiDBサーバーを再起動します。次に、サーバーは新しいCA証明書と古いCA証明書の両方を受け入れます。

また、クライアントが古いCA証明書と新しいCA証明書の両方を受け入れるように、古いCA証明書を結合された証明書に置き換えます。

### クライアントキーと証明書を更新する {#update-client-key-and-certificate}

> **ノート：**
>
> 次の手順は、クライアントとサーバーの古いCA証明書を結合されたCA証明書に置き換えた**後でのみ**実行してください。

1.  クライアントの新しいRSAキーを生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.new.pem -out client-req.new.pem && \
    sudo openssl rsa -in client-key.new.pem -out client-key.new.pem
    ```

    > **ノート：**
    >
    > 上記のコマンドは、クライアントキーと証明書を置き換え、オンラインユーザーが影響を受けないようにするためのものです。したがって、上記のコマンドに追加される情報は、 `require subject`の情報と一致している必要があります。

2.  結合された証明書と新しいCAキーを使用して、新しいクライアント証明書を生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl x509 -req -in client-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.new.pem
    ```

3.  クライアント（たとえば、MySQL）がTiDBを新しいクライアントキーと証明書に接続するようにします。

    {{< copyable "" >}}

    ```bash
    mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
    ```

    > **ノート：**
    >
    > `/path/to/client-cert.new.pem` 、および`/path/to/client-key.new.pem`は、CA証明書、クライアントキー、およびクライアント証明書のディレクトリを指定し`/path/to/ca-cert.pem` 。それらを独自のディレクトリに置き換えることができます。

### サーバーキーと証明書を更新します {#update-the-server-key-and-certificate}

1.  サーバーの新しいRSAキーを生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.new.pem -out server-req.new.pem && \
    sudo openssl rsa -in server-key.new.pem -out server-key.new.pem
    ```

2.  結合されたCA証明書と新しいCAキーを使用して、新しいサーバー証明書を生成します。

    {{< copyable "" >}}

    ```bash
    sudo openssl x509 -req -in server-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.new.pem
    ```

3.  新しいサーバーキーと証明書を使用するようにTiDBサーバーを構成します。詳細については、 [TiDBサーバーを構成する](#configure-tidb-and-the-client-to-use-certificates)を参照してください。
