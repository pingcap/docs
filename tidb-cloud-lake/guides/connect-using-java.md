---
title: Java を使用して TiDB Cloud Lake に接続する
summary: このページでは、Java を使用して TiDB Cloud Lake に接続する方法について説明します。
---

# Java を使用して TiDB Cloud Lake に接続する

公式の JDBC ドライバーは標準の JDBC 4.0 互換性を提供し、Java アプリケーションとのシームレスな統合を実現します。

## Installation {#installation}

### Maven {#maven}

```xml
<dependency>
    <groupId>com.tidbcloud</groupId>
    <artifactId>lake-jdbc</artifactId>
    <version>0.4.6</version>
</dependency>
```

### Gradle {#gradle}

```gradle
implementation 'com.tidbcloud:lake-jdbc:0.4.6'
```

**Connection String**: DSN の形式と例については、[ドライバー概要](/tidb-cloud-lake/guides/driver-overview.md)を参照してください。

## Key Features {#key-features}

- ✅ **JDBC 4.0 Compatible**: 標準 JDBC インターフェースをサポート
- ✅ **Connection Pooling**: 組み込みの接続管理
- ✅ **Prepared Statements**: 効率的なパラメーター化クエリ
- ✅ **Batch Operations**: 一括挿入および更新をサポート

## Data Type Mappings {#data-type-mappings}

| {{{ .lake }}} | Java | 注記 |
|----------|------|---------|
| **整数** | | |
| `TINYINT` | `Byte` | |
| `SMALLINT` | `Short` | |
| `INT` | `Integer` | |
| `BIGINT` | `Long` | |
| `TINYINT UNSIGNED` | `Short` | |
| `SMALLINT UNSIGNED` | `Integer` | |
| `INT UNSIGNED` | `Long` | |
| `BIGINT UNSIGNED` | `BigInteger` | |
| **浮動小数点** | | |
| `FLOAT` | `Float` | |
| `DOUBLE` | `Double` | |
| `DECIMAL` | `BigDecimal` | 精度を保持 |
| **その他の型** | | |
| `BOOLEAN` | `Boolean` | |
| `STRING` | `String` | |
| `DATE` | `Date` | |
| `TIMESTAMP` | `Timestamp` | |
| `ARRAY(T)` | `String` | JSON エンコード |
| `TUPLE(...)` | `String` | JSON エンコード |
| `MAP(K,V)` | `String` | JSON エンコード |
| `VARIANT` | `String` | JSON エンコード |
| `BITMAP` | `String` | Base64 エンコード |

---

## Basic Usage {#basic-usage}

```java
import java.sql.*;

// Connect to {{{ .lake }}}
Connection conn = DriverManager.getConnection("<your-dsn>");

// DDL: Create table
Statement stmt = conn.createStatement();
stmt.execute("CREATE TABLE users (id INT, name STRING, email STRING)");

// Write: Insert data
PreparedStatement pstmt = conn.prepareStatement("INSERT INTO users VALUES (?, ?, ?)");
pstmt.setInt(1, 1);
pstmt.setString(2, "Alice");
pstmt.setString(3, "alice@example.com");
int result = pstmt.executeUpdate();

// Write: Insert data with executeBatch
pstmt = conn.prepareStatement("INSERT INTO users VALUES (?, ?, ?)");
pstmt.setInt(1, 2);
pstmt.setString(2, "Bob");
pstmt.setString(3, "Bob@example.com");
pstmt.addBatch();
pstmt.setInt(1, 3);
pstmt.setString(2, "John");
pstmt.setString(3, "John@example.com");
pstmt.addBatch();
int[] results = pstmt.executeBatch();

// Query: Select data
ResultSet rs = stmt.executeQuery("SELECT id, name, email FROM users WHERE id = 1");
while (rs.next()) {
    System.out.println("User: " + rs.getInt("id") + ", " +
                      rs.getString("name") + ", " +
                      rs.getString("email"));
}

// Close connections
rs.close();
stmt.close();
pstmt.close();
conn.close();
```

## Configuration Reference {#configuration-reference}

以下を含む lake-jdbc ドライバーの完全な設定オプションについては、次を参照してください。

- 接続文字列パラメーター
- SSL/TLS 設定
- 認証方式
- 性能チューニングパラメーター

[公式の lake-jdbc Connection Guide](https://github.com/tidbcloud/lake-jdbc/blob/main/docs/Connection.md) を参照してください。

## リソース {#resources}

- **Maven Central**: [lake-jdbc](https://repo1.maven.org/maven2/com/tidbcloud/lake-jdbc/)
- **GitHub リポジトリ**: [lake-jdbc](https://github.com/tidbcloud/lake-jdbc)
- **JDBC ドキュメント**: [Oracle JDBC Guide](https://docs.oracle.com/javase/tutorial/jdbc/)
