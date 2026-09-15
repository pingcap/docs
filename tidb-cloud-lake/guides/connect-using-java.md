---
title: 使用 Java 连接 TiDB Cloud Lake
summary: 本页介绍如何使用 Java 连接 TiDB Cloud Lake。
---

# 使用 Java 连接 TiDB Cloud Lake

官方 JDBC 驱动提供标准的 JDBC 4.0 兼容性，可与 Java 应用程序无缝集成。

## 安装 {#installation}

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

**Connection String**：有关 DSN 格式和示例，请参见[驱动概览](/tidb-cloud-lake/guides/driver-overview.md)。

## 关键特性 {#key-features}

- ✅ **JDBC 4.0 Compatible**：支持标准 JDBC 接口
- ✅ **Connection Pooling**：内置连接管理
- ✅ **Prepared Statements**：高效的参数化查询
- ✅ **Batch Operations**：支持批量插入和修改操作

## 数据类型映射 {#data-type-mappings}

| {{{ .lake }}} | Java | 说明 |
|----------|------|---------|
| **整数型** | | |
| `TINYINT` | `Byte` | |
| `SMALLINT` | `Short` | |
| `INT` | `Integer` | |
| `BIGINT` | `Long` | |
| `TINYINT UNSIGNED` | `Short` | |
| `SMALLINT UNSIGNED` | `Integer` | |
| `INT UNSIGNED` | `Long` | |
| `BIGINT UNSIGNED` | `BigInteger` | |
| **浮点数** | | |
| `FLOAT` | `Float` | |
| `DOUBLE` | `Double` | |
| `DECIMAL` | `BigDecimal` | 保留精度 |
| **其他类型** | | |
| `BOOLEAN` | `Boolean` | |
| `STRING` | `String` | |
| `DATE` | `Date` | |
| `TIMESTAMP` | `Timestamp` | |
| `ARRAY(T)` | `String` | JSON 编码 |
| `TUPLE(...)` | `String` | JSON 编码 |
| `MAP(K,V)` | `String` | JSON 编码 |
| `VARIANT` | `String` | JSON 编码 |
| `BITMAP` | `String` | Base64 编码 |

---

## 基本用法 {#basic-usage}

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

## 配置参考 {#configuration-reference}

有关完整的 lake-jdbc 驱动配置选项，包括：

- 连接字符串参数
- SSL/TLS 配置
- 身份验证方法
- 性能调优参数

请参阅[官方 lake-jdbc Connection Guide](https://github.com/tidbcloud/lake-jdbc/blob/main/docs/Connection.md)。

## 资源 {#resources}

- **Maven Central**：[lake-jdbc](https://repo1.maven.org/maven2/com/tidbcloud/lake-jdbc/)
- **GitHub Repository**：[lake-jdbc](https://github.com/tidbcloud/lake-jdbc)
- **JDBC Documentation**：[Oracle JDBC Guide](https://docs.oracle.com/javase/tutorial/jdbc/)