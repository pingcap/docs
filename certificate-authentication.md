---
title: Certificate-Based Authentication for Login
summary: Learn the certificate-based authentication used for login.
---

# ログイン用の証明書ベースの認証 {#certificate-based-authentication-for-login}

TiDB は、ユーザーが TiDB にログインするための証明書ベースの認証方法をサポートしています。この方法を使用すると、TiDB はさまざまなユーザーに証明書を発行し、暗号化された接続を使用してデータを転送し、ユーザーがログインするときに証明書を検証します。このアプローチは、MySQL ユーザーが一般的に使用する従来のパスワードベースの認証方法よりも安全であるため、MySQL ユーザーによって採用されています。ユーザー数の増加。

証明書ベースの認証を使用するには、次の操作を実行する必要がある場合があります。

-   セキュリティキーと証明書を作成する
-   TiDB とクライアントの証明書を構成する
-   ユーザーのログイン時に検証するユーザー証明書情報を設定します。
-   証明書の更新と置き換え

ドキュメントの残りの部分では、これらの操作を実行する方法を詳しく紹介します。

## セキュリティキーと証明書を作成する {#create-security-keys-and-certificates}

<CustomContent platform="tidb">

キーと証明書を作成するには[OpenSSL](https://www.openssl.org/)を使用することをお勧めします。証明書の生成プロセスは、 [TiDB クライアントとサーバー間で TLS を有効にする](/enable-tls-between-clients-and-servers.md)で説明したプロセスと同様です。次の段落では、証明書で検証する必要があるその他の属性フィールドを構成する方法を示します。

</CustomContent>

<CustomContent platform="tidb-cloud">

キーと証明書を作成するには[OpenSSL](https://www.openssl.org/)を使用することをお勧めします。証明書の生成プロセスは、 [TiDB クライアントとサーバー間で TLS を有効にする](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers)で説明したプロセスと同様です。次の段落では、証明書で検証する必要があるその他の属性フィールドを構成する方法を示します。

</CustomContent>

### CA キーと証明書を生成する {#generate-ca-key-and-certificate}

1.  次のコマンドを実行して CA キーを生成します。

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

    上記のコマンドの出力は次のとおりです。

        Generating RSA private key, 2048 bit long modulus (2 primes)
        ....................+++++
        ...............................................+++++
        e is 65537 (0x010001)

2.  次のコマンドを実行して、CA キーに対応する証明書を生成します。

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.pem
    ```

3.  詳細な証明書情報を入力します。例えば：

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
    > 上記証明書詳細の`:`以降が入力情報となります。

### サーバーキーと証明書を生成する {#generate-server-key-and-certificate}

1.  次のコマンドを実行してサーバーキーを生成します。

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.pem -out server-req.pem
    ```

2.  詳細な証明書情報を入力します。例えば：

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

3.  次のコマンドを実行して、サーバーの RSA キーを生成します。

    ```bash
    sudo openssl rsa -in server-key.pem -out server-key.pem
    ```

    上記のコマンドの出力は次のとおりです。

    ```bash
    writing RSA key
    ```

4.  CA 証明書の署名を使用して、署名付きサーバー証明書を生成します。

    ```bash
    sudo openssl x509 -req -in server-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem
    ```

    上記のコマンドの出力 (例):

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiKV, CN = TiKV Test Server, emailAddress = k@pingcap.com
    Getting CA Private Key
    ```

    > **注記：**
    >
    > ログインすると、TiDB は上記の出力の`subject`セクションの情報が一貫しているかどうかをチェックします。

### クライアントキーと証明書を生成する {#generate-client-key-and-certificate}

サーバーのキーと証明書を生成した後、クライアントのキーと証明書を生成する必要があります。多くの場合、ユーザーごとに異なるキーと証明書を生成する必要があります。

1.  次のコマンドを実行してクライアント キーを生成します。

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.pem -out client-req.pem
    ```

2.  詳細な証明書情報を入力します。例えば：

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

    上記のコマンドの出力は次のとおりです。

    ```bash
    writing RSA key
    ```

4.  CA 証明書の署名を使用してクライアント証明書を生成します。

    ```bash
    sudo openssl x509 -req -in client-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.pem
    ```

    上記のコマンドの出力 (例):

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiDB, CN = tpch-user1, emailAddress = zz@pingcap.com
    Getting CA Private Key
    ```

    > **注記：**
    >
    > 上記の出力の`subject`セクションの情報は、 `require`セクションの[ログイン検証のための証明書の構成](#configure-the-user-certificate-information-for-login-verification)に使用されます。

### 証明書を検証する {#verify-certificate}

次のコマンドを実行して証明書を確認します。

```bash
openssl verify -CAfile ca-cert.pem server-cert.pem client-cert.pem
```

証明書が検証されると、次の結果が表示されます。

    server-cert.pem: OK
    client-cert.pem: OK

## 証明書を使用するように TiDB とクライアントを構成する {#configure-tidb-and-the-client-to-use-certificates}

証明書を生成した後、対応するサーバー証明書またはクライアント証明書を使用するように TiDBサーバーとクライアントを構成する必要があります。

### サーバー証明書を使用するように TiDB を構成する {#configure-tidb-to-use-server-certificate}

TiDB 構成ファイルの`[security]`セクションを変更します。この手順では、CA 証明書、サーバーキー、およびサーバー証明書が保存されているディレクトリを指定します。 `path/to/server-cert.pem` 、 `path/to/server-key.pem` 、 `path/to/ca-cert.pem`独自のディレクトリに置き換えることができます。

    [security]
    ssl-cert ="path/to/server-cert.pem"
    ssl-key ="path/to/server-key.pem"
    ssl-ca="path/to/ca-cert.pem"

TiDB を起動してログを確認します。次の情報がログに表示されれば、構成は成功しています。

    [INFO] [server.go:264] ["secure connection is enabled"] ["client verification enabled"=true]

### クライアント証明書を使用するようにクライアントを構成する {#configure-the-client-to-use-client-certificate}

クライアントがログインにクライアント キーと証明書を使用するようにクライアントを構成します。

MySQL クライアントを例に挙げると、 `ssl-cert` 、 `ssl-key` 、および`ssl-ca`を指定することで、新しく作成したクライアント証明書、クライアント キー、および CA を使用できます。

```bash
mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
```

> **注記：**
>
> `/path/to/client-cert.new.pem` 、 `/path/to/client-key.new.pem` 、および`/path/to/ca-cert.pem` 、CA 証明書、クライアント キー、およびクライアント証明書のディレクトリです。これらを独自のディレクトリに置き換えることができます。

## ログイン認証用のユーザー証明書情報を設定する {#configure-the-user-certificate-information-for-login-verification}

まず、クライアントを使用して TiDB に接続し、ログイン検証を構成します。次に、検証するユーザー証明書情報を取得して構成できます。

### ユーザー証明書情報の取得 {#get-user-certificate-information}

ユーザー証明書情報は`require subject` 、 `require issuer` 、 `require san` 、および`require cipher`で指定でき、X509 証明書の属性を確認するために使用されます。

-   `require subject` : ログイン時にクライアント証明書の`subject`情報を指定します。このオプションを指定すると、 `require ssl`またはx509の設定は不要です。指定する情報は、 [クライアントキーと証明書を生成する](#generate-client-key-and-certificate)で入力した`subject`情報と一致します。

    このオプションを取得するには、次のコマンドを実行します。

    ```bash
    openssl x509 -noout -subject -in client-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'
    ```

-   `require issuer` : ユーザー証明書を発行するCA証明書の`subject`情報を指定します。指定する情報は、 [CA キーと証明書を生成する](#generate-ca-key-and-certificate)で入力した`subject`情報と一致します。

    このオプションを取得するには、次のコマンドを実行します。

    ```bash
    openssl x509 -noout -subject -in ca-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'
    ```

-   `require san` : ユーザー証明書を発行するCA証明書の情報`Subject Alternative Name`を指定します。指定する情報は、クライアント証明書の生成に使用した[`openssl.cnf`構成ファイルの`alt_names`](https://docs.pingcap.com/tidb/stable/generate-self-signed-certificates)と一致します。

    -   次のコマンドを実行して、生成された証明書の`require san`項目の情報を取得します。

        ```shell
        openssl x509 -noout -extensions subjectAltName -in client.crt
        ```

    -   `require san`では現在、次の`Subject Alternative Name`チェック項目がサポートされています。

        -   URI
        -   IP
        -   DNS

    -   チェック項目はカンマで区切って複数設定できます。たとえば、ユーザー`u1`に対して`require san`次のように設定します。

        ```sql
        create user 'u1'@'%' require san 'DNS:d1,URI:spiffe://example.org/myservice1,URI:spiffe://example.org/myservice2';
        ```

        上記の構成では、URI 項目`spiffe://example.org/myservice1`または`spiffe://example.org/myservice2`と DNS 項目`d1`の証明書を使用して TiDB にログインできるのは`u1`人のユーザーのみです。

-   `require cipher` : クライアントがサポートする暗号方式を確認します。次のステートメントを使用して、サポートされている暗号方式のリストを確認します。

    ```sql
    SHOW SESSION STATUS LIKE 'Ssl_cipher_list';
    ```

### ユーザー証明書情報の構成 {#configure-user-certificate-information}

ユーザー証明書情報 ( `require subject` 、 `require issuer` 、 `require san` 、 `require cipher` ) を取得したら、ユーザーの作成、権限の付与、またはユーザーの変更時に検証されるようにこれらの情報を構成します。 `<replaceable>`次のステートメントの対応する情報に置き換えます。

スペースまたは`and`を区切り文字として使用して、1 つのオプションまたは複数のオプションを設定できます。

-   ユーザーの作成時にユーザー証明書を構成します ( `create user` ):

    ```sql
    create user 'u1'@'%' require issuer '<replaceable>' subject '<replaceable>' san '<replaceable>' cipher '<replaceable>';
    ```

-   権限を付与するときにユーザー証明書を構成します。

    ```sql
    grant all on *.* to 'u1'@'%' require issuer '<replaceable>' subject '<replaceable>' san '<replaceable>' cipher '<replaceable>';
    ```

-   ユーザーを変更するときにユーザー証明書を構成します。

    ```sql
    alter user 'u1'@'%' require issuer '<replaceable>' subject '<replaceable>' san '<replaceable>' cipher '<replaceable>';
    ```

上記の設定後、ログイン時に次の項目が確認されます。

-   SSL が使用されます。クライアント証明書を発行する CA は、サーバーに構成されている CA と一致します。
-   クライアント証明書の`issuer`情報は、 `require issuer`で指定した情報と一致します。
-   クライアント証明書の`subject`情報は、 `require cipher`で指定した情報と一致します。
-   クライアント証明書の`Subject Alternative Name`情報は、 `require san`で指定した情報と一致します。

上記のすべての項目が確認された場合にのみ、TiDB にログインできます。それ以外の場合は、 `ERROR 1045 (28000): Access denied`エラーが返されます。次のコマンドを使用して、TLS バージョン、暗号アルゴリズム、および現在の接続でログインに証明書が使用されているかどうかを確認できます。

MySQL クライアントに接続し、次のステートメントを実行します。

```sql
\s
```

出力：

    --------------
    mysql  Ver 15.1 Distrib 10.4.10-MariaDB, for Linux (x86_64) using readline 5.1

    Connection id:       1
    Current database:    test
    Current user:        root@127.0.0.1
    SSL:                 Cipher in use is TLS_AES_256_GCM_SHA384

次に、次のステートメントを実行します。

```sql
show variables like '%ssl%';
```

出力：

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

## 証明書の更新と置き換え {#update-and-replace-certificate}

キーと証明書は定期的に更新されます。次のセクションでは、キーと証明書を更新する方法を紹介します。

CA 証明書は、クライアントとサーバー間の相互検証の基礎となります。 CA 証明書を置き換えるには、古い証明書と新しい証明書の両方の認証をサポートする結合証明書を生成します。クライアントとサーバーで、まず CA 証明書を置き換えてから、クライアント/サーバーのキーと証明書を置き換えます。

### CA キーと証明書を更新する {#update-ca-key-and-certificate}

1.  古い CA キーと証明書をバックアップします ( `ca-key.pem`が盗まれたと仮定します)。

    ```bash
    mv ca-key.pem ca-key.old.pem && \
    mv ca-cert.pem ca-cert.old.pem
    ```

2.  新しい CA キーを生成します。

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

3.  新しく生成された CA キーを使用して、新しい CA 証明書を生成します。

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.new.pem
    ```

    > **注記：**
    >
    > 新しい CA 証明書を生成すると、クライアントとサーバー上のキーと証明書が置き換えられ、オンライン ユーザーが影響を受けないようになります。したがって、上記のコマンドに追加される情報は、 `require issuer`情報と一致している必要があります。

4.  結合された CA 証明書を生成します。

    ```bash
    cat ca-cert.new.pem ca-cert.old.pem > ca-cert.pem
    ```

上記の操作の後、新しく作成した結合 CA 証明書を使用して TiDBサーバーを再起動します。その後、サーバーは新しい CA 証明書と古い CA 証明書の両方を受け入れます。

また、クライアントが古い CA 証明書と新しい CA 証明書の両方を受け入れるように、古い CA 証明書を結合された証明書に置き換えます。

### クライアントキーと証明書を更新する {#update-client-key-and-certificate}

> **注記：**
>
> クライアントとサーバー上の古い CA 証明書を結合された CA 証明書に置き換えた**後にのみ、**次の手順を実行してください。

1.  クライアントの新しい RSA キーを生成します。

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.new.pem -out client-req.new.pem && \
    sudo openssl rsa -in client-key.new.pem -out client-key.new.pem
    ```

    > **注記：**
    >
    > 上記のコマンドは、クライアント キーと証明書を置き換え、オンライン ユーザーが影響を受けないようにします。したがって、上記のコマンドに追加される情報は、 `require subject`情報と一致している必要があります。

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
    > `/path/to/client-cert.new.pem` 、 `/path/to/client-key.new.pem` 、および`/path/to/ca-cert.pem` 、CA 証明書、クライアント キー、およびクライアント証明書のディレクトリを指定します。これらを独自のディレクトリに置き換えることができます。

### サーバーキーと証明書を更新する {#update-the-server-key-and-certificate}

1.  サーバーの新しい RSA キーを生成します。

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.new.pem -out server-req.new.pem && \
    sudo openssl rsa -in server-key.new.pem -out server-key.new.pem
    ```

2.  結合された CA 証明書と新しい CA キーを使用して、新しいサーバー証明書を生成します。

    ```bash
    sudo openssl x509 -req -in server-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.new.pem
    ```

3.  新しいサーバーキーと証明書を使用するように TiDBサーバーを構成します。詳細については[TiDBサーバーを構成する](#configure-tidb-and-the-client-to-use-certificates)を参照してください。
