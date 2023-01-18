---
title: TLS Connections to Dedicated Tier
summary: Introduce TLS connections in TiDB Dedicated Tier.
---

# TLS Connections to Dedicated Tier

On TiDB Cloud, establishing TLS connections is one of the basic security practices for connecting to Dedicated Tier clusters. You can configure multiple TLS connections from your client, application, and development tools to your Dedicated Tier cluster to protect data transmission security. 

For security reasons, TiDB Cloud Dedicated Tier only supports TLS 1.2 and TLS 1.3, and does not support TLS 1.0 and TLS 1.1 versions.

For each Dedicated Tier cluster, the server TLS certificate is hosted on [AWS Certificate Manager (ACM)](https://aws.amazon.com/certificate-manager/). ACM Private CA keys are stored securely in AWS-managed hardware security modules (HSMs) that meet [FIPS 140-2 Level 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139) security standards to protect your TLS private keys when Dedicated Tier requests AWS ACM to create it.

## Prerequisites

- Log in to TiDB Cloud via [Password Authentication](/tidb-cloud/tidb-cloud-password-authentication.md) or [SSO Authentication](/tidb-cloud/tidb-cloud-sso-authentication.md), and then [Create a TiDB Cloud Dedicated Tier cluster](/tidb-cloud/create-tidb-cluster.md).

- Set a password to access your cluster in secure settings.

    To do so, you can navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, click **...** in the row of your Dedicated Tier cluster, and then select **Security Settings**. In security settings, you can click **Generate** to automatically generate a root password with a length of 16 characters, including numbers, uppercase and lowercase characters, and special characters.

## Secure connection to a Dedicated Tier cluster

In the [TiDB Cloud console](https://tidbcloud.com/), you can get examples of different connection methods and connect to your Dedicated Tier cluster as follows:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, and then click the name of your Dedicated Tier cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A dialog is displayed.

3. On the **Standard Connection** tab of this dialog, follow the three steps to set up the TLS connctions.
   - Step 1：Create traffic filter
   - Step 2：Download TiDB cluster CA
   - Step 3：Connect with an SQL client

4. Under **Step 1：Create traffic filter** in the dialog, configure the IP addresses that are allowed to access your cluster. For more information, see [Configure an IP access list in standard connection](/tidb-cloud/configure-ip-access-list.md#configure-an-ip-access-list-in-standard-connection).

5. Under **Step 2: Download TiDB cluster CA**, click **Download TiDB cluster CA** to download it locally for client TLS configuration. Verifying the TiDB cluster CA can ensure the TLS connection is secure and reliable.

    > **Note:**
    > 
    > After downloading your Dedicated Tier cluster CA, you can store it in the default storage path of your operating system, or specify another storage path. Make sure that you need to replace the CA path in the code example with your own cluster CA path in the subsequent steps. 


6. Under **Step 3: Connect with an SQL client** in the dialog, click the tab of your preferred connection method, and then refer to the connection string and sample code on the tab to connect to your cluster.

The following examples show the connection strings in MySQL, MyCLI , JDBC, Python, Go, and Node.js:

<SimpleTab>
<div label="MySQL CLI">

MySQL CLI client attempts to establish a TLS connection by default. When you connect to Dedicated Tier clusters, you should set `ssl-mode` and `ssl-ca`.

```shell
mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=ca.pem --tls-version="TLSv1.2" -u root -h tidb.eqlfbdgthh8.clusters.staging.tidb-cloud.com -P 4000 -D test -p
```

Parameter description：

- With `--ssl-mode=VERIFY_IDENTITY`, MySQL CLI client forces to enable TLS and validate TiDB Dedicated Tier clusters.
- Update `ca.pem` in `--ssl-ca=ca.pem` to your local path of the downloaded TiDB cluster CA.
- Use `--tls-version=TLSv1.2` to restrict the versions of TLS protocol.

</div>

<div label="MyCLI">

[MyCLI](https://www.mycli.net/) automatically enables TLS when using TLS related parameters. When you connect to TiDB Dedicated Tier clusters, you need to set `ssl-ca` and `ssl-verify-server-cert`.

```shell
mycli --ssl-ca=ca.pem --ssl-verify-server-cert -u root -h tidb.eqlfbdgthh8.clusters.staging.tidb-cloud.com -P 4000 -D test
```

Parameter description：

- Update `ca.pem` in `--ssl-ca=ca.pem` to your local path of the downloaded TiDB cluster CA.
- With `--ssl-verify-server-cert` to validate TiDB Dedicated Tier clusters.

</div>

<div label="JDBC">

[MySQL Connector/J](https://dev.mysql.com/doc/connector-j/8.0/en/)'s TLS connection configurations are used here as an example.

After downloading TiDB cluster CA, if you want to import it into your operating system, you can use the `keytool -importcert -alias TiDBCACert -file ca.pem -keystore <your_custom_truststore_path> -storepass <your_truststore_password>` command.

```shell
/* Be sure to replace the parameters in the following connection string. */
/* version >= 8.0.28 */
jdbc:mysql://tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000/test?user=root&password=<your_password>&sslMode=VERIFY_IDENTITY&tlsVersions=TLSv1.2&trustCertificateKeyStoreUrl=file:<your_custom_truststore_path>&trustCertificateKeyStorePassword=<your_truststore_password>
```
You can click **show example usage** to view detailed code examples.

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

Parameter description：

- Set `sslMode=VERIFY_IDENTITY` to enable TLS and validate TiDB Dedicated Tier clusters.
- Set `enabledTLSProtocols=TLSv1.2` to restrict the versions of TLS protocol.
- Set `trustCertificateKeyStoreUrl` to your custom truststore path.
- Set `trustCertificateKeyStorePassword` to your truststore password.

</div>

<div label="Python">

[mysqlclient](https://pypi.org/project/mysqlclient/)'s TLS connection configurations are used here as an example.

```
host="tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com", user="root", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "ca.pem"}
```

You can click **show example usage** to view detailed code examples.

```
import MySQLdb

connection = MySQLdb.connect(host="tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com", port=4000, user="root", password="<your_password>", database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "ca.pem"})

with connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        m = cursor.fetchone()
        print(m[0])
```

Parameter description：

- Set `ssl_mode="VERIFY_IDENTITY"` to enable TLS and validate TiDB Dedicated Tier clusters.
- Update `ca.pem` in `ssl={"ca": "ca.pem"}` to your local path of the downloaded TiDB cluster CA.

</div>

<div label="Go">

[Go-MySQL-Driver](https://github.com/go-sql-driver/mysql)'s TLS connection configurations are used here as an example.

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

You can click **show example usage** to view detailed code examples.

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

Parameter description：

- Register `tls.Config` in connection to enable TLS and validate TiDB Dedicated Tier clusters. 
- Set `MinVersion: tls.VersionTLS12` to restrict the versions of TLS protocol.
- Set `ServerName: "<host>"` to verify TiDB Dedicated Tier's hostname.
- If you do not want to register a new TLS configuration, you can just set `tls=true` in the connection string.

</div>

<div label="Node.js">

[Mysql2](https://www.npmjs.com/package/mysql2)'s TLS connection configurations are used here as an example.

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

You can click **show example usage** to view detailed code examples.

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

Parameter description：

- Set `ssl: {minVersion: 'TLSv1.2'}` to restrict the versions of TLS protocol.
- Set `ssl: {ca: fs.readFileSync('<CA_root_path>')}` to read the content of cert.


</div>
</SimpleTab>

## Root Digital certificate management of Dedicated Tier 

### Root Digital certificate‘s issuance and validity  

TiDB Dedicated Tier uses certificates from [AWS Certificate Manager (ACM)](https://aws.amazon.com/certificate-manager/) as a Certificate Authority (CA) for TLS connections between clients and TiDB Dedicated Tier clusters. Usually, the root certificates of ACM are stored securely in AWS-managed hardware security modules (HSMs) that meet [FIPS 140-2 Level 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139) security standards. 

## FAQs

### Which TLS versions are supported to connect to my TiDB Cloud Dedicated Tier cluster?

For security reasons, TiDB Cloud Dedicated Tier only supports TLS 1.2 and TLS 1.3, and does not support TLS 1.0 and TLS 1.1 versions. See IETF [Deprecating TLS 1.0 and TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/) for details.

### Is two-way TLS authentication between my client and TiDB Cloud Dedicated Tier supported?

No.

TiDB Cloud Dedicated Tier only supports one-way TLS authentication, which means your client uses the public key to verify the signature of your TiDB Cloud cluster certificate's private key while the cluster does not validate the client.