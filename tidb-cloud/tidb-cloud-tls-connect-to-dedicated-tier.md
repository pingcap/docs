---
title: TLS Connections to Dedicated Tier
summary: Introduce TLS connections in TiDB Dedicated Tier.
---

# Dedicated Tierへの TLS 接続 {#tls-connections-to-dedicated-tier}

TiDB Cloudでは、TLS 接続の確立は、 Dedicated Tierクラスターに接続するための基本的なセキュリティ プラクティスの 1 つです。クライアント、アプリケーション、および開発ツールからDedicated Tierクラスターへの複数の TLS 接続を構成して、データ転送のセキュリティを保護できます。セキュリティ上の理由から、 TiDB Cloud Dedicated Tier はTLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 と TLS 1.1 のバージョンはサポートしていません。

データのセキュリティを確保するために、 Dedicated Tierクラスターの TiDB クラスター CA は[AWS 証明書マネージャー (ACM)](https://aws.amazon.com/certificate-manager/)でホストされ、TiDB クラスターの秘密鍵は[FIPS 140-2 レベル 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139)セキュリティ基準を満たす AWS マネージド ハードウェア セキュリティ モジュール (HSM) に保存されます。

## 前提条件 {#prerequisites}

-   [パスワード認証](/tidb-cloud/tidb-cloud-password-authentication.md)または[SSO 認証](/tidb-cloud/tidb-cloud-sso-authentication.md)を介してTiDB Cloudにログインし、次に[TiDB Cloud Dedicated Tierクラスターを作成する](/tidb-cloud/create-tidb-cluster.md)介してログインします。

-   安全な設定でクラスターにアクセスするためのパスワードを設定します。

    これを行うには、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、 Dedicated Tierクラスターの行で**[...]**をクリックして、 <strong>[Security Settings]</strong>を選択します。セキュリティ設定で、 <strong>[生成]</strong>をクリックして、数字、大文字と小文字、および特殊文字を含む 16 文字の長さのルート パスワードを自動的に生成できます。

## Dedicated Tierクラスターへのセキュリティ接続 {#secure-connection-to-a-dedicated-tier-cluster}

[TiDB Cloudコンソール](https://tidbcloud.com/)では、さまざまな接続方法の例を取得し、次のようにDedicated Tierクラスターに接続できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、 Dedicated Tierクラスターの名前をクリックして概要ページに移動します。

2.  右上隅にある**[接続]**をクリックします。ダイアログが表示されます。

3.  このダイアログの**[標準接続]**タブで、3 つの手順に従って TLS 接続をセットアップします。
    -   ステップ 1：トラフィック フィルターを作成する
    -   ステップ 2：TiDB クラスター CA のダウンロード
    -   ステップ 3：SQL クライアントに接続する

4.  ダイアログの**[ステップ 1: トラフィック フィルターの作成]**で、クラスターへのアクセスを許可する IP アドレスを構成します。詳細については、 [標準接続で IP アクセス リストを構成する](/tidb-cloud/configure-ip-access-list.md#configure-an-ip-access-list-in-standard-connection)を参照してください。

5.  **[ステップ 2: TiDB クラスター CA のダウンロード] で**、 <strong>[TiDB クラスター CA のダウンロード</strong>] をクリックして、クライアント TLS 構成用にローカルにダウンロードします。 TiDB クラスター CA は、TLS 接続が安全で信頼できるものであることを保証します。

    > **ノート：**
    >
    > Dedicated Tierクラスター CA をダウンロードしたら、オペレーティング システムの既定のstorageパスに保存するか、別のstorageパスを指定できます。以降の手順では、コード例の CA パスを独自のクラスター CA パスに置き換える必要があります。

6.  ダイアログの**[ステップ 3: SQL クライアントに接続する]**で、希望する接続方法のタブをクリックし、タブの接続文字列とサンプル コードを参照してクラスターに接続します。

次の例は、MySQL、MyCLI、JDBC、Python、Go、および Node.js の接続文字列を示しています。

<SimpleTab>
<div label="MySQL CLI">

MySQL CLI クライアントは、デフォルトで TLS 接続を確立しようとします。 Dedicated Tierクラスターに接続する場合は、 `ssl-mode`と`ssl-ca`を設定する必要があります。

```shell
mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=ca.pem --tls-version="TLSv1.2" -u root -h tidb.eqlfbdgthh8.clusters.staging.tidb-cloud.com -P 4000 -D test -p
```

パラメータの説明：

-   `--ssl-mode=VERIFY_IDENTITY`を指定すると、MySQL CLI クライアントは強制的に TLS を有効にし、TiDB Dedicated Tierクラスターを検証します。
-   `--ssl-ca=<CA_path>`を使用して、ダウンロードした TiDB クラスターのローカル パスを指定します`ca.pem` 。
-   TLS プロトコルのバージョンを制限するには、 `--tls-version=TLSv1.2`を使用します。 TLS 1.3 を使用する場合は、バージョンを`TLSv1.3`に設定できます。

</div>

<div label="MyCLI">

[MyCLI](https://www.mycli.net/) TLS 関連のパラメーターを使用するときに TLS を自動的に有効にします。 TiDB Dedicated Tierクラスターに接続する場合は、 `ssl-ca`と`ssl-verify-server-cert`を設定する必要があります。

```shell
mycli --ssl-ca=ca.pem --ssl-verify-server-cert -u root -h tidb.eqlfbdgthh8.clusters.staging.tidb-cloud.com -P 4000 -D test
```

パラメータの説明：

-   `--ssl-ca=<CA_path>`を使用して、ダウンロードした TiDB クラスターのローカル パスを指定します`ca.pem` 。
-   `--ssl-verify-server-cert`を指定すると、TiDB Dedicated Tierクラスターが検証されます。

</div>

<div label="JDBC">

ここでは、例として[MySQL コネクタ/J](https://dev.mysql.com/doc/connector-j/8.0/en/)の TLS 接続構成が使用されています。

TiDB クラスター CA をダウンロードした後、それをオペレーティング システムにインポートする場合は、 `keytool -importcert -alias TiDBCACert -file ca.pem -keystore <your_custom_truststore_path> -storepass <your_truststore_password>`コマンドを使用できます。

```shell
/* Be sure to replace the parameters in the following connection string. */
/* version >= 8.0.28 */
jdbc:mysql://tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000/test?user=root&password=<your_password>&sslMode=VERIFY_IDENTITY&tlsVersions=TLSv1.2&trustCertificateKeyStoreUrl=file:<your_custom_truststore_path>&trustCertificateKeyStorePassword=<your_truststore_password>
```

**[使用例の表示]**をクリックして、詳細なコード例を表示できます。

```
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
```

パラメータの説明：

-   `sslMode=VERIFY_IDENTITY`を設定して TLS を有効にし、TiDB Dedicated Tierクラスターを検証します。
-   TLS プロトコルのバージョンを制限するには、 `enabledTLSProtocols=TLSv1.2`を設定します。 TLS 1.3 を使用する場合は、バージョンを`TLSv1.3`に設定できます。
-   カスタム トラストストア パスに`trustCertificateKeyStoreUrl`を設定します。
-   トラストストアのパスワードに`trustCertificateKeyStorePassword`を設定します。

</div>

<div label="Python">

ここでは、例として[mysql クライアント](https://pypi.org/project/mysqlclient/)の TLS 接続構成が使用されています。

```
host="tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com", user="root", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "ca.pem"}
```

**[使用例の表示]**をクリックして、詳細なコード例を表示できます。

```
import MySQLdb

connection = MySQLdb.connect(host="tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com", port=4000, user="root", password="<your_password>", database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "ca.pem"})

with connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        m = cursor.fetchone()
        print(m[0])
```

パラメータの説明：

-   `ssl_mode="VERIFY_IDENTITY"`を設定して TLS を有効にし、TiDB Dedicated Tierクラスターを検証します。
-   `ssl={"ca": "<CA_path>"}`を使用して、ダウンロードした TiDB クラスターのローカル パスを指定します`ca.pem` 。

</div>

<div label="Go">

ここでは、例として[Go-MySQL-ドライバー](https://github.com/go-sql-driver/mysql)の TLS 接続構成が使用されています。

```
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
```

**[使用例の表示]**をクリックして、詳細なコード例を表示できます。

```
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
```

パラメータの説明：

-   TLS 接続構成に`tls.Config`登録して、TLS を有効にし、TiDB Dedicated Tierクラスターを検証します。
-   TLS プロトコルのバージョンを制限するには、 `MinVersion: tls.VersionTLS12`を設定します。
-   TiDB Dedicated Tier のホスト名を確認するには、 `ServerName: "<host>"`を設定します。
-   新しい TLS 構成を登録したくない場合は、接続文字列に`tls=true`を設定するだけです。

</div>

<div label="Node.js">

ここでは、例として[Mysql2](https://www.npmjs.com/package/mysql2)の TLS 接続構成が使用されています。

```
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
```

**[使用例の表示]**をクリックして、詳細なコード例を表示できます。

```
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
```

パラメータの説明：

-   TLS プロトコルのバージョンを制限するには、 `ssl: {minVersion: 'TLSv1.2'}`を設定します。 TLS 1.3 を使用する場合は、バージョンを`TLSv1.3`に設定できます。
-   `ssl: {ca: fs.readFileSync('<CA_path>')}`を設定して、ダウンロードした TiDB クラスターのローカル CA パスを読み取ります`ca.pem` 。

</div>
</SimpleTab>

## Dedicated Tierのルート証明書を管理する {#manage-root-certificates-for-dedicated-tier}

TiDB Dedicated Tier は、クライアントと TiDB Dedicated Tierクラスター間の TLS 接続の認証局 (CA) として[AWS 証明書マネージャー (ACM)](https://aws.amazon.com/certificate-manager/)からの証明書を使用します。通常、ACM のルート証明書は、 [FIPS 140-2 レベル 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139)セキュリティ基準を満たす AWS 管理のハードウェア セキュリティ モジュール (HSM) に安全に保存されます。

## よくある質問 {#faqs}

### TiDB Cloud Dedicated Tierクラスターに接続するためにサポートされている TLS バージョンはどれですか? {#which-tls-versions-are-supported-to-connect-to-my-tidb-cloud-dedicated-tier-cluster}

セキュリティ上の理由から、 TiDB Cloud Dedicated Tier はTLS 1.2 と TLS 1.3 のみをサポートし、TLS 1.0 と TLS 1.1 のバージョンはサポートしていません。詳細については、IETF [TLS 1.0 と TLS 1.1 の廃止](https://datatracker.ietf.org/doc/rfc8996/)を参照してください。

### クライアントとTiDB Cloud Dedicated Tier間の双方向 TLS 認証はサポートされていますか? {#is-two-way-tls-authentication-between-my-client-and-tidb-cloud-dedicated-tier-supported}

いいえ。

TiDB Cloud Dedicated Tier は一方向の TLS 認証のみをサポートし、現在双方向の TLS 認証をサポートしていません。双方向の TLS 認証が必要な場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。
