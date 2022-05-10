---
title: Follower Read
---

# Follower Read

## Introduction

In TiDB, data is stored in units of [Region](/tidb-storage.md#region), which are dispersed on all nodes in the cluster. A Region can have multiple replicas, and the replicas are divided into a leader and multiple followers. When the data on the leader changes, TiDB will update the data to the followers synchronously.

By default, TiDB will only read and write data on the leader of the same Region. When there is a read hotspot Region in the system, the leader resource is tight and becomes the reading bottleneck of the whole system. Enabling the Follower Read feature can significantly reduce the burden on the leader, and significantly improve the overall system throughput by balancing the load among multiple followers. .

## When to use

You can visually analyze whether your application has hotspot regions on the [TiDB Dashboard Key Visualizer Page](/dashboard-key-visualizer.md). You can check whether there is a read hotspot region by selecting the "metrics selection box" to `Read (bytes)` or `Read (keys)`.

If you find that there is indeed a hotspot problem, you can avoid it from the application level by reading the chapter [TiDB Hotspot Problem Handling](https://docs.pingcap.com/zh/tidb/stable/troubleshoot-hot-spot-issues) to troubleshoot it one by one.

If read hotspots are unavoidable or the cost of changes is very high, you can try to use the Follower Read function to better load balance read requests to the follower region.

## Enable follower read

<SimpleTab>
<div label="SQL">

You can set the value of the variable `tidb_replica_read` (the default is `leader`) to `follower` or `leader-and-follower` to enable TiDB's Follower Read feature:

```sql
SET [GLOBAL] tidb_replica_read = 'follower';
```

You can checkout the [Follower Read - Usage](/follower-read.md#usage) section for more details on this variable.

</div>
<div label="Java">

In the Java language, we can define a `FollowerReadHelper` class to enable the Follower Read feature:

```java
public enum FollowReadMode {
    LEADER("leader"),
    FOLLOWER("follower"),
    LEADER_AND_FOLLOWER("leader-and-follower");

    private final String mode;

    FollowReadMode(String mode) {
        this.mode = mode;
    }

    public String getMode() {
        return mode;
    }
}

public class FollowerReadHelper {

    public static void setSessionReplicaRead(Connection conn, FollowReadMode mode) throws SQLException {
        if (mode == null) mode = FollowReadMode.LEADER;
        PreparedStatement stmt = conn.prepareStatement(
            "SET @@tidb_replica_read = ?;"
        );
        stmt.setString(1, mode.getMode());
        stmt.execute();
    }

    public static void setGlobalReplicaRead(Connection conn, FollowReadMode mode) throws SQLException {
        if (mode == null) mode = FollowReadMode.LEADER;
        PreparedStatement stmt = conn.prepareStatement(
            "SET GLOBAL @@tidb_replica_read = ?;"
        );
        stmt.setString(1, mode.getMode());
        stmt.execute();
    }

}
```

When you need to read data from the follower node, use the `setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER)` method to enable the Follower Read feature that can load balance between the leader node and the follower node in the current session. When the connection is disconnected, it will be restored to the original mode.

```java
public static class AuthorDAO {

    // Omit initialization of instance variables...

    public void getAuthorsByFollowerRead() throws SQLException {
        try (Connection conn = ds.getConnection()) {
            // Enable the follower read feature.
            FollowerReadHelper.setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER);

            // Read the authors list for 100000 times.
            Random random = new Random();
            for (int i = 0; i < 100000; i++) {
                Integer birthYear = 1920 + random.nextInt(100);
                List<Author> authors = this.getAuthorsByBirthYear(birthYear);
                System.out.println(authors.size());
            }
        }
    }

    public List<Author> getAuthorsByBirthYear(Integer birthYear) throws SQLException {
        List<Author> authors = new ArrayList<>();
        try (Connection conn = ds.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("SELECT id, name FROM authors WHERE birth_year = ?");
            stmt.setInt(1, birthYear);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                Author author = new Author();
                author.setId( rs.getLong("id"));
                author.setName(rs.getString("name"));
                authors.add(author);
            }
        }
        return authors;
    }
}
```

</div>
</SimpleTab>

## Read more

- [Follower Read](/follower-read.md)
- [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md)
- [TiDB Dashboard - Key Visualizer Page](/dashboard-key-visualizer.md)
