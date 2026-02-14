---
title: TLS Connections to TiDB Cloud Dedicated
summary: TiDB Cloud Dedicated に TLS 接続を導入します。
aliases: ['/ja/tidbcloud/tidb-cloud-tls-connect-to-dedicated-tier']
---

# TiDB Cloud専用へのTLS接続 {#tls-connections-to-tidb-cloud-dedicated}

TiDB Cloudでは、TLS 接続の確立はTiDB Cloud Dedicated クラスタへの接続における基本的なセキュリティ対策の一つです。クライアント、アプリケーション、開発ツールからTiDB Cloud Dedicated クラスタへの複数の TLS 接続を設定することで、データ転送のセキュリティを保護できます。セキュリティ上の理由から、 TiDB Cloud Dedicated は TLS 1.2 および TLS 1.3 のみをサポートし、TLS 1.0 および TLS 1.1 はサポートしていません。

データのセキュリティを確保するため、 TiDB Cloud Dedicated クラスターの CA 証明書は[AWS プライベート認証局](https://aws.amazon.com/private-ca/)でホストされています。CA 証明書の秘密鍵は、 [FIPS 140-2 レベル 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139)セキュリティ標準を満たす AWS 管理のハードウェアセキュリティモジュール (HSM) に保存されます。

## 前提条件 {#prerequisites}

-   [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)または[SSO認証](/tidb-cloud/tidb-cloud-sso-authentication.md)経由してTiDB Cloudにログインし、次に[TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)経由してログインします。

-   安全な設定でクラスターにアクセスするためのパスワードを設定します。

    これを行うには、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、 TiDB Cloud Dedicatedクラスターの行にある**「...」**をクリックし、 **「パスワード設定」**を選択します。パスワード設定で「パスワードの**自動生成」**をクリックすると、数字、大文字、小文字、特殊文字を含む16文字のルートパスワードが自動的に生成されます。

## TiDB Cloud専用クラスタへのセキュリティ接続 {#secure-connection-to-a-tidb-cloud-dedicated-cluster}

[TiDB Cloudコンソール](https://tidbcloud.com/)では、さまざまな接続方法の例を取得し、次のようにTiDB Cloud Dedicated クラスターに接続できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、 TiDB Cloud Dedicated クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択します。

    IPアクセスリストを設定していない場合は、初回接続前に**「IPアクセスリストの設定**」をクリックして設定してください。詳細については、 [IPアクセスリストを設定する](/tidb-cloud/configure-ip-access-list.md)参照してください。

4.  **「CA証明書」**をクリックして、TiDBクラスタへのTLS接続用のCA証明書をダウンロードしてください。CA証明書はデフォルトでTLS 1.2バージョンをサポートしています。

    > **注記：**
    >
    > -   ダウンロードしたCA証明書は、オペレーティングシステムのデフォルトのstorageパスに保存することも、別のstorageパスを指定することもできます。以降の手順では、コード例のCA証明書パスをご自身のCA証明書パスに置き換える必要があります。
    > -   TiDB Cloud Dedicated では、クライアントに TLS 接続の使用を強制しません。また、 [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)変数のユーザー定義構成は現在TiDB Cloud Dedicated ではサポートされていません。

5.  希望する接続方法を選択し、タブ上の接続文字列とサンプル コードを参照してクラスターに接続します。

次の例は、MySQL、MyCLI、JDBC、Python、Go、Node.js の接続文字列を示しています。

<SimpleTab>
<div label="MySQL CLI">

MySQL CLIクライアントはデフォルトでTLS接続を確立しようとします。TiDB TiDB Cloud Dedicatedクラスタに接続する場合は、 `ssl-mode`と`ssl-ca`設定する必要があります。

```shell
mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=ca.pem --tls-version="TLSv1.2" -u root -h tidb.eqlfbdgthh8.clusters.staging.tidb-cloud.com -P 4000 -D test -p
```

パラメータの説明：

-   `--ssl-mode=VERIFY_IDENTITY`では、MySQL CLI クライアントは TLS を有効にし、 TiDB Cloud Dedicated クラスターを検証することを強制します。
-   `--ssl-ca=<CA_path>`使用して、ダウンロードした TiDB クラスター`ca.pem`のローカル パスを指定します。
-   TLSプロトコルのバージョンを制限するには、 `--tls-version=TLSv1.2`使用します。TLS 1.3を使用する場合は、バージョンを`TLSv1.3`に設定できます。

</div>

<div label="MyCLI">

[マイクリ](https://www.mycli.net/)指定すると、TLS関連のパラメータを使用する際にTLSが自動的に有効になります。TiDB TiDB Cloud Dedicatedクラスタに接続する場合は、 `ssl-ca`と`ssl-verify-server-cert`設定する必要があります。

```shell
mycli --ssl-ca=ca.pem --ssl-verify-server-cert -u root -h tidb.eqlfbdgthh8.clusters.staging.tidb-cloud.com -P 4000 -D test
```

パラメータの説明：

-   `--ssl-ca=<CA_path>`使用して、ダウンロードした TiDB クラスター`ca.pem`のローカル パスを指定します。
-   `--ssl-verify-server-cert`でTiDB Cloud Dedicated クラスターを検証します。

</div>

<div label="JDBC">

ここでは、 [MySQL コネクタ/J](https://dev.mysql.com/doc/connector-j/en/)の TLS 接続構成が例として使用されています。

TiDB クラスター CA をダウンロードした後、それをオペレーティング システムにインポートする場合は、 `keytool -importcert -alias TiDBCACert -file ca.pem -keystore <your_custom_truststore_path> -storepass <your_truststore_password>`コマンドを使用できます。

```shell
/* Be sure to replace the parameters in the following connection string. */
/* version >= 8.0.28 */
jdbc:mysql://tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000/test?user=root&password=<your_password>&sslMode=VERIFY_IDENTITY&tlsVersions=TLSv1.2&trustCertificateKeyStoreUrl=file:<your_custom_truststore_path>&trustCertificateKeyStorePassword=<your_truststore_password>
```

詳細なコード例を表示するには、 **「使用例を表示」**をクリックします。

    import com.mysql.jdbc.Driver;
    import java.sql.*;

    class Main {
      public static void main(String args[]) throws SQLException, ClassNotFoundException {
        Class.forName("com.mysql.cj.jdbc.Driver");
        try {
          Connection conn = DriverManager.getConnection("jdbc:mysql://tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000/test?user=root&password=<your_password>&sslMode=VERIFY_IDENTITY&tlsVersions=TLSv1.2&trustCertificateKeyStoreUrl=file:<your_custom_truststore_path>&trustCertificateKeyStorePassword=<your_truststore_password>");
          Statement stmt = conn.createStatement();
          try {
            ResultSet rs = stmt.executeQuery("SELECT DATABASE();");
            if (rs.next()) {
              System.out.println("using db:" + rs.getString(1));
            }
          } catch (Exception e) {
            System.out.println("exec error:" + e);
          }
        } catch (Exception e) {
          System.out.println("connect error:" + e);
        }
      }
    }

パラメータの説明：

-   TLS を有効にしてTiDB Cloud Dedicated クラスターを検証するには、 `sslMode=VERIFY_IDENTITY`設定します。
-   TLSプロトコルのバージョンを制限するには、 `enabledTLSProtocols=TLSv1.2`設定します。TLS 1.3を使用する場合は、バージョンを`TLSv1.3`に設定できます。
-   カスタム トラストストアのパスに`trustCertificateKeyStoreUrl`設定します。
-   トラストストアのパスワードを`trustCertificateKeyStorePassword`に設定します。

</div>

<div label="Python">

ここでは、 [mysqlクライアント](https://pypi.org/project/mysqlclient/)の TLS 接続構成が例として使用されています。

    host="tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com", user="root", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "ca.pem"}

詳細なコード例を表示するには、 **「使用例を表示」**をクリックします。

    import MySQLdb

    connection = MySQLdb.connect(host="tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com", port=4000, user="root", password="<your_password>", database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "ca.pem"})

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            m = cursor.fetchone()
            print(m[0])

パラメータの説明：

-   TLS を有効にしてTiDB Cloud Dedicated クラスターを検証するには、 `ssl_mode="VERIFY_IDENTITY"`設定します。
-   `ssl={"ca": "<CA_path>"}`使用して、ダウンロードした TiDB クラスター`ca.pem`のローカル パスを指定します。

</div>

<div label="Go">

ここでは、 [Go-MySQL-ドライバー](https://github.com/go-sql-driver/mysql)の TLS 接続構成が例として使用されています。

    rootCertPool := x509.NewCertPool()
    pem, err := ioutil.ReadFile("ca.pem")
    if err != nil {
        log.Fatal(err)
    }
    if ok := rootCertPool.AppendCertsFromPEM(pem); !ok {
        log.Fatal("Failed to append PEM.")
    }
    mysql.RegisterTLSConfig("tidb", &tls.Config{
        RootCAs:    rootCertPool,
        MinVersion: tls.VersionTLS12,
        ServerName: "tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com",
    })

    db, err := sql.Open("mysql", "root:<your_password>@tcp(tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000)/test?tls=tidb")

詳細なコード例を表示するには、 **「使用例を表示」**をクリックします。

    package main
    import (
      "crypto/tls"
      "crypto/x509"
      "database/sql"
      "fmt"
      "io/ioutil"
      "log"

      "github.com/go-sql-driver/mysql"
    )
    func main() {
      rootCertPool := x509.NewCertPool()
      pem, err := ioutil.ReadFile("ca.pem")
      if err != nil {
        log.Fatal(err)
      }
      if ok := rootCertPool.AppendCertsFromPEM(pem); !ok {
        log.Fatal("Failed to append PEM.")
      }
      mysql.RegisterTLSConfig("tidb", &tls.Config{
        RootCAs:    rootCertPool,
        MinVersion: tls.VersionTLS12,
        ServerName: "tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com",
      })
      db, err := sql.Open("mysql", "root:<your_password>@tcp(tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000)/test?tls=tidb")
      if err != nil {
        log.Fatal("failed to connect database", err)
      }
      defer db.Close()

      var dbName string
      err = db.QueryRow("SELECT DATABASE();").Scan(&dbName)
      if err != nil {
        log.Fatal("failed to execute query", err)
      }
      fmt.Println(dbName)
    }

パラメータの説明：

-   TLS 接続構成に`tls.Config`登録して、TLS を有効にし、 TiDB Cloud Dedicated クラスターを検証します。
-   TLS プロトコルのバージョンを制限するには`MinVersion: tls.VersionTLS12`設定します。
-   TiDB Cloud Dedicated のホスト名を確認するには`ServerName: "<host>"`設定します。
-   新しい TLS 構成を登録したくない場合は、接続文字列に`tls=true`設定するだけです。

</div>

<div label="Node.js">

ここでは、 [MySQL2](https://www.npmjs.com/package/mysql2)の TLS 接続構成が例として使用されています。

    var connection = mysql.createConnection({
      host: 'tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com',
      port: 4000,
      user: 'root',
      password: '<your_password>',
      database: 'test',
      ssl: {
        ca: fs.readFileSync('ca.pem'),
        minVersion: 'TLSv1.2',
        rejectUnauthorized: true
      }
    });

詳細なコード例を表示するには、 **「使用例を表示」**をクリックします。

    var mysql = require('mysql2');
    var fs = require('fs');
    var connection = mysql.createConnection({
      host: 'tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com',
      port: 4000,
      user: 'root',
      password: '<your_password>',
      database: 'test',
      ssl: {
        ca: fs.readFileSync('ca.pem'),
        minVersion: 'TLSv1.2',
        rejectUnauthorized: true
      }
    });
    connection.connect(function(err) {
      if (err) {
        throw err
      }
      connection.query('SELECT DATABASE();', function(err, rows) {
        if (err) {
          throw err
        }
        console.log(rows[0]['DATABASE()']);
        connection.end()
      });
    });

パラメータの説明：

-   TLSプロトコルのバージョンを制限するには、 `ssl: {minVersion: 'TLSv1.2'}`設定します。TLS 1.3を使用する場合は、バージョンを`TLSv1.3`に設定できます。
-   ダウンロードした TiDB クラスター`ca.pem`のローカル CA パスを読み取るには`ssl: {ca: fs.readFileSync('<CA_path>')}`設定します。

</div>
</SimpleTab>

## TiDB Cloud Dedicatedのルート証明書を管理する {#manage-root-certificates-for-tidb-cloud-dedicated}

TiDB Cloud Dedicated は、クライアントとTiDB Cloud Dedicated クラスター間の TLS 接続に、 [AWS プライベート認証局](https://aws.amazon.com/private-ca/)の証明書を認証局 (CA) として使用します。通常、CA 証明書の秘密鍵は、 [FIPS 140-2 レベル 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139)セキュリティ標準を満たす AWS マネージドハードウェアセキュリティモジュール (HSM) に安全に保管されます。

## よくある質問 {#faqs}

### TiDB Cloud Dedicated クラスターに接続するためにサポートされている TLS バージョンはどれですか? {#which-tls-versions-are-supported-to-connect-to-my-tidb-cloud-dedicated-cluster}

セキュリティ上の理由から、 TiDB Cloud Dedicated は TLS 1.2 および TLS 1.3 のみをサポートし、TLS 1.0 および TLS 1.1 はサポートしていません。詳細は IETF [TLS 1.0 および TLS 1.1 の廃止](https://datatracker.ietf.org/doc/rfc8996/)をご覧ください。

### クライアントとTiDB Cloud Dedicated 間の双方向 TLS 認証はサポートされていますか? {#is-two-way-tls-authentication-between-my-client-and-tidb-cloud-dedicated-supported}

いいえ。

TiDB Cloud Dedicatedは現在、片方向TLS認証のみをサポートしており、双方向TLS認証はサポートしていません。双方向TLS認証が必要な場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。
