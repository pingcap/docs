---
title: Connect to TiDB Cloud Lake Using Java
summary: This page describes how to connect to TiDB Cloud Lake using Java.
---

# Java JDBC Driver for Databend

The official JDBC driver providing standard JDBC 4.0 compatibility for seamless integration with Java applications.

## Installation

### Maven

```xml
<dependency>
    <groupId>com.databend</groupId>
    <artifactId>databend-jdbc</artifactId>
    <version>0.4.1</version>
</dependency>
```

### Gradle

```gradle
implementation 'com.databend:databend-jdbc:0.4.1'
```

**Connection String**: See [Drivers Overview](./index.md#connection-string-dsn) for DSN format and connection examples.

---

## Key Features

- ✅ **JDBC 4.0 Compatible**: Standard JDBC interface support
- ✅ **Connection Pooling**: Built-in connection management
- ✅ **Prepared Statements**: Efficient parameterized queries
- ✅ **Batch Operations**: Bulk insert and update supportations

## Data Type Mappings

| Databend | Java | Notes |
|----------|------|---------|
| **Integers** | | |
| `TINYINT` | `Byte` | |
| `SMALLINT` | `Short` | |
| `INT` | `Integer` | |
| `BIGINT` | `Long` | |
| `TINYINT UNSIGNED` | `Short` | |
| `SMALLINT UNSIGNED` | `Integer` | |
| `INT UNSIGNED` | `Long` | |
| `BIGINT UNSIGNED` | `BigInteger` | |
| **Floating Point** | | |
| `FLOAT` | `Float` | |
| `DOUBLE` | `Double` | |
| `DECIMAL` | `BigDecimal` | Precision preserved |
| **Other Types** | | |
| `BOOLEAN` | `Boolean` | |
| `STRING` | `String` | |
| `DATE` | `Date` | |
| `TIMESTAMP` | `Timestamp` | |
| `ARRAY(T)` | `String` | JSON encoded |
| `TUPLE(...)` | `String` | JSON encoded |
| `MAP(K,V)` | `String` | JSON encoded |
| `VARIANT` | `String` | JSON encoded |
| `BITMAP` | `String` | Base64 encoded |

---

## Basic Usage

```java
import java.sql.*;

// Connect to Databend
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

## Configuration Reference

For complete databend-jdbc driver configuration options including:
- Connection string parameters
- SSL/TLS configuration
- Authentication methods
- Performance tuning parameters

Please refer to the [official databend-jdbc Connection Guide](https://github.com/databendlabs/databend-jdbc/blob/main/docs/Connection.md).

## Resources

- **Maven Central**: [databend-jdbc](https://repo1.maven.org/maven2/com/databend/databend-jdbc/)
- **GitHub Repository**: [databend-jdbc](https://github.com/databendlabs/databend-jdbc)
- **JDBC Documentation**: [Oracle JDBC Guide](https://docs.oracle.com/javase/tutorial/jdbc/)
