---
title: TLS connection to Dedicated Tier
summary: Introduce TLS connection in TiDB Dedicated Tier.
---

# TLS connection to Dedicated Tier

On TiDB Cloud, TLS connections are one of the basic security practices for connecting to Dedicated Tier clusters. We support you to configure multiple TLS connections from client, application and development tools to protect your data transmission security.

Each Dedicated Tier cluster server TLS certificate is hosted on [AWS Certificate Manager (ACM)](https://aws.amazon.com/certificate-manager/), ACM Private CA keys are stored securely in AWS managed hardware security modules (HSMs) that adhere to [FIPS 140-2 Level 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139) security standards in order to protect your TLS private keys when Dedicated Tier request AWS ACM to create it.

> **Note:**
>
> Best practices for network access security include three steps:
> Step1: Set up [IP Access List](/tidb-cloud/configure-ip-access-list.md)
> Step2: Set up [Private Link](/tidb-cloud/set-up-private-endpoint-connections.md)
> Step3: Set up TLS Connection

## Prerequisites

Before connecting to your dedicated cluster, Log in to TiDB Cloud via [Password Authentication](/tidb-cloud-password-authentication.md) or [SSO Authentication](/tidb-cloud/tidb-cloud-sso-authentication.md),and then [Create a TiDB Cloud Serveless Tier cluster](/tidb-cloud/tidb-cloud-quickstart.md).

## Secure connection to a Dedicated Tier cluster

In the [TiDB Cloud console](https://tidbcloud.com/), you can get examples of different connection methods and connect to your Dedicated Tier cluster as follows:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, and then click the name of your Dedicated Tier cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A dialog named standard connection tap is displayed.

3. In this dialog, you should setup three steps:
   - Step 1：Create traffic filter
   - Step 2：Download TiDB cluster CA
   - Step 3：Connect with an SQL client

4. In the Step1：Create traffic filter

Specify the traffic allowed to connect the cluster. Traffic matching any filter is allowed, and all other traffic is denied. For detailed configuration, see: Configure your [IP Access List](/tidb-cloud/configure-ip-access-list.md)

5. In the Step 2：Download TiDB cluster CA

You should click **"**Download TiDB Cluster CA** to download it locally for client TLS configuration.Because of verifying the TiDB cluster CA can ensure the TLS connection is secure and reliable.

6. In the Step 3：Connect with an SQL client

Connect with a SQL client in the dialog, click the tab of your preferred connection method, and then refer to the connection string and sample code on the tab to connect to your cluster.

   - Support Mysql CLI, MyCLI, JDBC, Python, Go, Node.js and other six ways to connect to your Dedicated Tier cluster
   - Provide MacOS, Debian, RedHat, Alpine, OpenSUSE, Windows and other operating system configuration parameters

The following examples show the connection string in MySQL CLI , MyCLI , JDBC, Python, Go and Node.js:

<SimpleTab>
<div label="MySQL CLI">

MySQL CLI client attempts to establish TLS connection by default. When you connect to Dedicated Tier clusters, you should set `ssl-mode` and `ssl-ca`.

```shell
mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=ca.pem --tls-version="TLSv1.2" -u root -h tidb.eqlfbdgthh8.clusters.staging.tidb-cloud.com -P 4000 -D test -p
```

Parameter description：

- With `--ssl-mode=VERIFY_IDENTITY`, MySQL CLI client forces to enable TLS and validate TiDB Dedicated Tier clusters.
- Use `--ssl-ca=<CA_root_path>` to set the CA root path on your system.
- Use `--tls-version=TLSv1.2,TLSv1.3` to restrict the versions of TLS protocol.

</div>

<div label="MyCLI">

[MyCLI](https://www.mycli.net/) automatically enables TLS when using TLS related parameters. When you connect to TiDB Dedicated Tier clusters, you need to set `ssl-ca` and `ssl-verify-server-cert`.

```shell
mycli --ssl-ca=ca.pem --ssl-verify-server-cert -u root -h tidb.eqlfbdgthh8.clusters.staging.tidb-cloud.com -P 4000 -D test
```

Parameter description：

- Use `--ssl-ca=<CA_root_path>` to set the CA root path on your system.
- With `--ssl-verify-server-cert` to validate TiDB Dedicated Tier clusters.

</div>

<div label="JDBC">

[MySQL Connector/J](https://dev.mysql.com/doc/connector-j/8.0/en/)'s TLS connection configurations are used here as an example.

After downloaded TLS,if you want to import your downloaded TLS Certificate Template,Please refer to the order **keytool -importcert -alias TiDBCACert -file ca.pem -keystore <your_custom_truststore_path> -storepass <your_truststore_password>** 

```shell
/* Be sure to replace the parameters in the following connection string. */
/* version >= 8.0.28 */
jdbc:mysql://tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000/test?user=root&password=<your_password>&sslMode=VERIFY_IDENTITY&tlsVersions=TLSv1.2&trustCertificateKeyStoreUrl=file:<your_custom_truststore_path>&trustCertificateKeyStorePassword=<your_truststore_password>
```
You can select "show example usage" to view detailed code examples

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

- Set `sslMode=VERIFY_IDENTITY` to enable TLS and validate TiDB Dedicated Tier clusters. JDBC trusts system CA root certificates by default, so you do not need to configure certificates.
- Set `enabledTLSProtocols=TLSv1.2,TLSv1.3` to restrict the versions of TLS protocol.


</div>

<div label="Python">

[mysqlclient](https://pypi.org/project/mysqlclient/)'s TLS connection configurations are used here as an example.

```
host="tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com", user="root", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "ca.pem"}
```

You can select "show example usage" to view detailed code examples

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
- Set `ssl={"ca": "<CA_root_path>"}` to set the CA root path on your system.

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

You can select "show example usage" to view detailed code examples

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

- Register `tls.Config` in connection to enable TLS and validate TiDB Dedicated Tier clusters. Go-MySQL-Driver uses system CA root certificates by default, so you do not need to configure certificates.
- Set `MinVersion: tls.VersionTLS12，TLS13` to restrict the versions of TLS protocol.
- Set `ServerName: "<host>"` to verify TiDB Dedicated Tier's hostname.
- If you do not want to register a new TLS configuration, you can just set `tls=true` in the connection string.

</div>

<div label="Node.js">

[Mysql](https://www.npmjs.com/package/mysql2)'s TLS connection configurations are used here as an example.

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

You can select "show example usage" to view detailed code examples

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

- Set `ssl: {minVersion: 'TLSv1.2,TLS1.3'}` to restrict the versions of TLS protocol.

</div>
</SimpleTab>

## Create and Reset Dedicated database password

When you connect to your cluster for the first time,You should click **Security Setting** to automatically generate a root password with a length of 16 characters, including numbers, uppercase and lowercase characters, and special characters. 

## Root Digital certificate management of Dedicated Tier 

### Root Digital certificate‘s issuance and validity  

TiDB Dedicated Tier uses certificates from [AWS Certificate Manager (ACM)](https://aws.amazon.com/certificate-manager/) as a Certificate Authority (CA) for TLS connection between clients and TiDB Dedicated Tier clusters. Usually, the root certificate of ACM are stored securely in AWS managed hardware security modules (HSMs) that adhere to [FIPS 140-2 Level 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139) security standards. 

> **Note:**
>
After you download your Dedicated Tier cluster CA to the local operating system, you can store it in the system default storage directory, or customize the TiDB Cluster CA storage directory. It should be noted that you need to add your local real TiDB Cluster CA path to the code example.

## FAQs

### Which TLS versions should be supported to connect to my TiDB Dedicated Tier cluster?

TiDB Dedicated cluster only supports TLS 1.2 or TLS 1.3, and does not support TLS 1.0 and TLS 1.1 versions for security reasons. Refer to see IETF [Deprecating TLS 1.0 and TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/) for ditails.

### Does TiDB Dedicated Tier support two-way TLS authentication between my client and TiDB Dedicated Tier cluster?

No.

Currently,TiDB Dedicated Tier support one-way TLS authentication, which means your client uses public key to verify the signature of your TiDB Dedicated Tier Cluster Server certificate's private key,while the server does not validate the client.

### Does TiDB Dedicated Tier cluster have to configure TLS to establish a secure connection?

Yes.

TiDB Dedicated Tier allows TLS connections. The reason is that SSL/TLS is one of the most basic security measures for you to connect to the TiDB Dedicated Tier cluster via internet and intranet , so as to reduce the risk of data exposure to internet and intranet.