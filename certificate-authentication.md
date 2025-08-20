---
title: Certificate-Based Authentication for Login
summary: ログインに使用される証明書ベースの認証について学習します。
---

# ログインのための証明書ベースの認証 {#certificate-based-authentication-for-login}

TiDBは、ユーザーがTiDBにログインするための証明書ベースの認証方式をサポートしています。この方式では、TiDBはユーザーごとに証明書を発行し、暗号化された接続を使用してデータを転送し、ユーザーのログイン時に証明書を検証します。このアプローチは、MySQLユーザーが一般的に使用する従来のパスワードベースの認証方式よりも安全であるため、ますます多くのユーザーに採用されています。

証明書ベースの認証を使用するには、次の操作を実行する必要がある場合があります。

-   セキュリティキーと証明書を作成する
-   TiDBとクライアントの証明書を構成する
-   ユーザーがログインするときに検証されるユーザー証明書情報を構成する
-   証明書の更新と置き換え

ドキュメントの残りの部分では、これらの操作を実行する方法について詳しく説明します。

## セキュリティキーと証明書を作成する {#create-security-keys-and-certificates}

<CustomContent platform="tidb">

鍵と証明書の作成には[オープンSSL](https://www.openssl.org/)使用することをお勧めします。証明書の生成プロセスは[TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)で説明したプロセスと同様です。以下の段落では、証明書で検証する必要がある追加の属性フィールドを設定する方法を説明します。

</CustomContent>

<CustomContent platform="tidb-cloud">

鍵と証明書の作成には[オープンSSL](https://www.openssl.org/)使用することをお勧めします。証明書の生成プロセスは[TiDBクライアントとサーバー間のTLSを有効にする](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers)で説明したプロセスと同様です。以下の段落では、証明書で検証する必要がある追加の属性フィールドを設定する方法を説明します。

</CustomContent>

### CAキーと証明書を生成する {#generate-ca-key-and-certificate}

1.  CA キーを生成するには、次のコマンドを実行します。

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

    上記のコマンドの出力:

        Generating RSA private key, 2048 bit long modulus (2 primes)
        ....................+++++
        ...............................................+++++
        e is 65537 (0x010001)

2.  次のコマンドを実行して、CA キーに対応する証明書を生成します。

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.pem
    ```

3.  詳細な証明書情報を入力します。例:

    ```bash
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Locality Name (e.g. city) []:San Francisco
    Organization Name (e.g. company) [Internet Widgits Pty Ltd]:PingCAP Inc.
    Organizational Unit Name (e.g. section) []:TiDB
    Common Name (e.g. server FQDN or YOUR name) []:TiDB admin
    Email Address []:s@pingcap.com
    ```

    > **注記：**
    >
    > 上記の証明書の詳細において、 `:`以降のテキストは入力された情報です。

### サーバーキーと証明書を生成する {#generate-server-key-and-certificate}

1.  次のコマンドを実行してサーバーキーを生成します。

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.pem -out server-req.pem
    ```

2.  詳細な証明書情報を入力します。例:

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

3.  サーバーの RSA キーを生成するには、次のコマンドを実行します。

    ```bash
    sudo openssl rsa -in server-key.pem -out server-key.pem
    ```

    上記のコマンドの出力:

    ```bash
    writing RSA key
    ```

4.  CA 証明書の署名を使用して、署名されたサーバー証明書を生成します。

    ```bash
    sudo openssl x509 -req -in server-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem
    ```

    上記のコマンドの出力（例）:

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiKV, CN = TiKV Test Server, emailAddress = k@pingcap.com
    Getting CA Private Key
    ```

    > **注記：**
    >
    > ログインすると、TiDB は上記の出力の`subject`セクションの情報が一貫しているかどうかを確認します。

### クライアントキーと証明書を生成する {#generate-client-key-and-certificate}

サーバーの鍵と証明書を生成したら、クライアントの鍵と証明書を生成する必要があります。多くの場合、ユーザーごとに異なる鍵と証明書を生成する必要があります。

1.  次のコマンドを実行してクライアント キーを生成します。

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.pem -out client-req.pem
    ```

2.  詳細な証明書情報を入力します。例:

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

3.  次のコマンドを実行して、クライアントの RSA キーを生成します。

    ```bash
    sudo openssl rsa -in client-key.pem -out client-key.pem
    ```

    上記のコマンドの出力:

    ```bash
    writing RSA key
    ```

4.  CA 証明書の署名を使用してクライアント証明書を生成します。

    ```bash
    sudo openssl x509 -req -in client-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.pem
    ```

    上記のコマンドの出力（例）:

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiDB, CN = tpch-user1, emailAddress = zz@pingcap.com
    Getting CA Private Key
    ```

    > **注記：**
    >
    > 上記出力のセクション`subject`の情報は、セクション`require`のセクション[ログイン検証用の証明書設定](#configure-the-user-certificate-information-for-login-verification)に使用されます。

### 証明書を確認する {#verify-certificate}

証明書を検証するには、次のコマンドを実行します。

```bash
openssl verify -CAfile ca-cert.pem server-cert.pem client-cert.pem
```

証明書が検証されると、次の結果が表示されます。

    server-cert.pem: OK
    client-cert.pem: OK

## 証明書を使用するようにTiDBとクライアントを構成する {#configure-tidb-and-the-client-to-use-certificates}

証明書を生成した後、対応するサーバー証明書またはクライアント証明書を使用するように TiDBサーバーとクライアントを構成する必要があります。

### サーバー証明書を使用するように TiDB を構成する {#configure-tidb-to-use-server-certificate}

TiDB設定ファイルの`[security]`セクションを変更します。この手順では`path/to/ca-cert.pem` CA証明書、サーバー鍵、サーバー証明書`path/to/server-key.pem`保存されるディレクトリを指定します。3、5、7 `path/to/server-cert.pem`任意のディレクトリに置き換えることができます。

    [security]
    ssl-cert ="path/to/server-cert.pem"
    ssl-key ="path/to/server-key.pem"
    ssl-ca="path/to/ca-cert.pem"

TiDBを起動し、ログを確認します。ログに以下の情報が表示されていれば、設定は成功です。

    [INFO] [server.go:286] ["mysql protocol server secure connection is enabled"] ["client verification enabled"=true]

### クライアント証明書を使用するようにクライアントを構成する {#configure-the-client-to-use-client-certificate}

クライアントがログインにクライアント キーと証明書を使用するようにクライアントを構成します。

MySQL クライアントを例にとると、 `ssl-cert` 、 `ssl-key` 、 `ssl-ca`指定して、新しく作成したクライアント証明書、クライアント キー、および CA を使用できます。

```bash
mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
```

> **注記：**
>
> `/path/to/client-cert.new.pem` 、 `/path/to/client-key.new.pem` 、 `/path/to/ca-cert.pem` 、CA証明書、クライアント鍵、クライアント証明書のディレクトリです。これらは任意のディレクトリに置き換えることができます。

## ログイン検証用のユーザー証明書情報を構成する {#configure-the-user-certificate-information-for-login-verification}

まず、クライアントを使用してTiDBに接続し、ログイン認証を設定します。その後、認証するユーザー証明書情報を取得して設定します。

### ユーザー証明書情報を取得する {#get-user-certificate-information}

ユーザー証明書情報は、X.509 証明書属性を確認するために使用される`REQUIRE SUBJECT` 、 `REQUIRE ISSUER` 、 `REQUIRE SAN` 、および`REQUIRE CIPHER`で指定できます。

-   `REQUIRE SUBJECT` : ログイン時のクライアント証明書のサブジェクト情報を指定します。このオプションを指定すると、 `require ssl`またはx509を設定する必要はありません。指定する情報は、 [クライアントキーと証明書を生成する](#generate-client-key-and-certificate)で入力したサブジェクト情報と一致します。

    このオプションを取得するには、次のコマンドを実行します。

    ```bash
    openssl x509 -noout -subject -in client-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'
    ```

-   `require issuer` : ユーザー証明書を発行するCA証明書の`subject`情報を指定します。指定する情報は、 [CAキーと証明書を生成する](#generate-ca-key-and-certificate)で入力した`subject`情報と一致します。

    このオプションを取得するには、次のコマンドを実行します。

    ```bash
    openssl x509 -noout -subject -in ca-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'
    ```

-   `require san` : ユーザー証明書を発行するCA証明書の`Subject Alternative Name`情報を指定します。指定する情報は、クライアント証明書の生成に使用された[`openssl.cnf`設定ファイルの`alt_names`](https://docs.pingcap.com/tidb/stable/generate-self-signed-certificates)の情報と一致します。

    -   生成された証明書の`REQUIRE SAN`項目の情報を取得するには、次のコマンドを実行します。

        ```shell
        openssl x509 -noout -extensions subjectAltName -in client.crt
        ```

    -   `REQUIRE SAN`現在、次の`Subject Alternative Name`チェック項目をサポートしています。

        -   URI
        -   IP
        -   DNS

    -   複数のチェック項目は、カンマで区切って設定できます。例えば、ユーザー`u1`の場合は、 `REQUIRE SAN`以下のように設定します。

        ```sql
        CREATE USER 'u1'@'%' REQUIRE SAN 'DNS:d1,URI:spiffe://example.org/myservice1,URI:spiffe://example.org/myservice2';
        ```

        上記の構成では、URI 項目`spiffe://example.org/myservice1`または`spiffe://example.org/myservice2`と DNS 項目`d1`を持つ証明書を使用して`u1`ユーザーのみが TiDB にログインできます。

-   `REQUIRE CIPHER` : クライアントがサポートする暗号方式をチェックします。サポートされている暗号方式のリストを確認するには、次のステートメントを使用します。

    ```sql
    SHOW SESSION STATUS LIKE 'Ssl_cipher_list';
    ```

### ユーザー証明書情報を構成する {#configure-user-certificate-information}

ユーザー証明書情報（ `REQUIRE SUBJECT` ）を取得したら、ユーザー`REQUIRE ISSUER`作成、権限`REQUIRE SAN`付与、またはユーザーの変更時にこれらの情報`REQUIRE CIPHER`検証されるように設定します。以下の文の`<replaceable>`対応する情報に置き換えてください。

スペースまたは`and`区切り文字として使用して、1 つのオプションまたは複数のオプションを設定できます。

-   ユーザー作成時にユーザー証明書を設定します（ `CREATE USER` ）：

    ```sql
    CREATE USER 'u1'@'%' REQUIRE ISSUER '<replaceable>' SUBJECT '<replaceable>' SAN '<replaceable>' CIPHER '<replaceable>';
    ```

-   ユーザーを変更するときにユーザー証明書を構成します。

    ```sql
    ALTER USER 'u1'@'%' REQUIRE ISSUER '<replaceable>' SUBJECT '<replaceable>' SAN '<replaceable>' CIPHER '<replaceable>';
    ```

上記の設定後、ログイン時に以下の項目が検証されます。

-   SSL が使用され、クライアント証明書を発行する CA はサーバーで構成された CA と一致します。
-   クライアント証明書の`issuer`情報が`REQUIRE ISSUER`で指定された情報と一致します。
-   クライアント証明書の`subject`情報が`REQUIRE CIPHER`で指定された情報と一致します。
-   クライアント証明書の`Subject Alternative Name`情報が`REQUIRE SAN`で指定された情報と一致します。

上記のすべての項目が検証された場合にのみ、TiDBにログインできます。そうでない場合は、エラー`ERROR 1045 (28000): Access denied`が返されます。以下のコマンドを使用して、TLSバージョン、暗号アルゴリズム、および現在の接続でログインに証明書が使用されているかどうかを確認できます。

MySQL クライアントに接続し、次のステートメントを実行します。

```sql
\s
```

出力:

    --------------
    mysql  Ver 8.5.3 for Linux on x86_64 (MySQL Community Server - GPL)

    Connection id:       1
    Current database:    test
    Current user:        root@127.0.0.1
    SSL:                 Cipher in use is TLS_AES_128_GCM_SHA256

次に、次のステートメントを実行します。

```sql
SHOW VARIABLES LIKE '%ssl%';
```

出力:

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

## 証明書の更新と置き換え {#update-and-replace-certificate}

鍵と証明書は定期的に更新されます。以下のセクションでは、鍵と証明書の更新方法について説明します。

CA証明書は、クライアントとサーバー間の相互検証の基盤となります。CA証明書を置き換えるには、古い証明書と新しい証明書の両方の認証をサポートする統合証明書を生成します。クライアントとサーバーでは、まずCA証明書を置き換え、次にクライアント/サーバーの鍵と証明書を置き換えます。

### CAキーと証明書を更新する {#update-ca-key-and-certificate}

1.  古い CA キーと証明書をバックアップします ( `ca-key.pem`が盗まれたと仮定します)。

    ```bash
    mv ca-key.pem ca-key.old.pem && \
    mv ca-cert.pem ca-cert.old.pem
    ```

2.  新しい CA キーを生成します。

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

3.  新しく生成された CA キーを使用して新しい CA 証明書を生成します。

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.new.pem
    ```

    > **注記：**
    >
    > 新しいCA証明書を生成することは、クライアントとサーバーの鍵と証明書を置き換え、オンラインユーザーに影響を与えないようにするためです。したがって、上記のコマンドに追加される情報は、 `require issuer`情報と一致している必要があります。

4.  結合された CA 証明書を生成します。

    ```bash
    cat ca-cert.new.pem ca-cert.old.pem > ca-cert.pem
    ```

上記の操作後、新しく作成された統合CA証明書を使用してTiDBサーバーを再起動します。サーバーは新しいCA証明書と古いCA証明書の両方を受け入れるようになります。

また、クライアントが古い CA 証明書と新しい CA 証明書の両方を受け入れるように、古い CA 証明書を結合された証明書に置き換えます。

### クライアントキーと証明書を更新する {#update-client-key-and-certificate}

> **注記：**
>
> クライアントとサーバーの古い CA 証明書を結合された CA 証明書に置き換えた**後にのみ、**以下の手順を実行してください。

1.  クライアントの新しい RSA キーを生成します。

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.new.pem -out client-req.new.pem && \
    sudo openssl rsa -in client-key.new.pem -out client-key.new.pem
    ```

    > **注記：**
    >
    > 上記のコマンドは、クライアントの鍵と証明書を置き換え、オンラインユーザーに影響を与えないようにするためのものです。そのため、上記のコマンドに追加される情報は、 `require subject`情報と一致している必要があります。

2.  結合された証明書と新しい CA キーを使用して、新しいクライアント証明書を生成します。

    ```bash
    sudo openssl x509 -req -in client-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.new.pem
    ```

3.  クライアント (MySQL など) が新しいクライアント キーと証明書を使用して TiDB に接続できるようにします。

    ```bash
    mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
    ```

    > **注記：**
    >
    > `/path/to/client-cert.new.pem` 、 `/path/to/client-key.new.pem` 、 `/path/to/ca-cert.pem` 、CA証明書、クライアント鍵、クライアント証明書のディレクトリを指定します。これらは任意のディレクトリに置き換えることができます。

### サーバーのキーと証明書を更新する {#update-the-server-key-and-certificate}

1.  サーバーの新しい RSA キーを生成します:

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.new.pem -out server-req.new.pem && \
    sudo openssl rsa -in server-key.new.pem -out server-key.new.pem
    ```

2.  結合された CA 証明書と新しい CA キーを使用して、新しいサーバー証明書を生成します。

    ```bash
    sudo openssl x509 -req -in server-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.new.pem
    ```

3.  新しいサーバーキーと証明書を使用するようにTiDBサーバーを設定します。詳細は[TiDBサーバーを構成する](#configure-tidb-and-the-client-to-use-certificates)参照してください。

## 証明書のポリシーベースのアクセス制御 {#policy-based-access-control-for-certificates}

TiDBは、基盤となる鍵管理サーバーによって定義されたポリシーを活用し、証明書に対するポリシーベースのアクセス制御（PBAC）をサポートします。これにより、時間ベースのポリシー（例えば、証明書を特定の時間帯のみ有効にする）、場所ベースのポリシー（例えば、特定の地理的な場所へのアクセスを制限する）、その他のカスタマイズ可能な条件など、様々な基準に基づいてきめ細かなアクセス制御が可能になり、証明書管理におけるセキュリティと柔軟性が向上します。
