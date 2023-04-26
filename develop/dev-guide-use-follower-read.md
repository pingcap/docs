---
title: Follower Read
summary: Learn how to use Follower Read to optimize query performance.
---

# Follower Read {#follower-read}

このドキュメントでは、 Follower Read を使用してクエリのパフォーマンスを最適化する方法を紹介します。

## 序章 {#introduction}

TiDB は、クラスター内のすべてのノードにデータを分散するための基本単位として[リージョン](/tidb-storage.md#region)を使用します。リージョンは複数のレプリカを持つことができ、レプリカはリーダーと複数のフォロワーに分割されます。リーダーのデータが変更されると、TiDB はフォロワーのデータを同期的に更新します。

デフォルトでは、TiDB は同じリージョンのリーダーでのみデータの読み取りと書き込みを行います。 リージョンで読み取りホットスポットが発生すると、 リージョンリーダーがシステム全体の読み取りボトルネックになる可能性があります。このような状況では、Follower Read機能を有効にすると、リーダーの負荷が大幅に軽減され、複数のフォロワー間で負荷が分散されるため、システム全体のスループットが向上します。

## いつ使用するか {#when-to-use}

### 読み取りホットスポットを減らす {#reduce-read-hotspots}

<CustomContent platform="tidb">

アプリケーションが[TiDB ダッシュボード キー ビジュアライザー ページ](/dashboard/dashboard-key-visualizer.md)にホットスポットリージョンを持っているかどうかを視覚的に分析できます。 「メトリック選択ボックス」を`Read (bytes)`または`Read (keys)`に選択すると、読み取りホットスポットが発生するかどうかを確認できます。

ホットスポットの処理の詳細については、 [TiDB Hotspot の問題処理](/troubleshoot-hot-spot-issues.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

アプリケーションが[TiDB Cloudキー ビジュアライザー ページ](/tidb-cloud/tune-performance.md#key-visualizer)にホットスポットリージョンを持っているかどうかを視覚的に分析できます。 「メトリック選択ボックス」を`Read (bytes)`または`Read (keys)`に選択すると、読み取りホットスポットが発生するかどうかを確認できます。

ホットスポットの処理の詳細については、 [TiDB Hotspot の問題処理](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)を参照してください。

</CustomContent>

読み取りホットスポットが避けられない場合、または変更コストが非常に高い場合は、Follower Read機能を使用して、フォロワーリージョンへの読み取り要求のバランスを改善することができます。

### 地理的に分散した展開のレイテンシーを短縮 {#reduce-latency-for-geo-distributed-deployments}

TiDB クラスターが複数の地区またはデータ センターにデプロイされている場合、リージョンの異なるレプリカが異なる地区またはデータ センターに分散されます。この場合、 Follower Read を`closest-adaptive`または`closest-replicas`として構成して、TiDB が現在のデータ センターからの読み取りを優先できるようにすることができます。これにより、読み取り操作のレイテンシーとトラフィック オーバーヘッドを大幅に削減できます。実装の詳細については、 [Follower Read](/follower-read.md)を参照してください。

## Follower Readを有効にする {#enable-follower-read}

<SimpleTab groupId="language">
<div label="SQL" value="sql">

Follower Readを有効にするには、変数`tidb_replica_read` (デフォルト値は`leader` ) を`follower` 、 `leader-and-follower` 、 `closest-replicas` 、または`closest-adaptive`に設定します。

```sql
SET [GLOBAL] tidb_replica_read = 'follower';
```

この変数の詳細については、 [Follower Readの使用](/follower-read.md#usage)を参照してください。

</div>
<div label="Java" value="java">

JavaでFollower Read を有効にするには、 `FollowerReadHelper`クラスを定義します。

```java
public enum FollowReadMode {
    LEADER("leader"),
    FOLLOWER("follower"),
    LEADER_AND_FOLLOWER("leader-and-follower"),
    CLOSEST_REPLICA("closest-replica"),
    CLOSEST_ADAPTIVE("closest-adaptive");

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

Followerノードからデータを読み取る場合は、 `setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER)`メソッドを使用してFollower Read機能を有効にします。これにより、現在のセッションでLeaderノードとFollowerノード間の負荷を分散できます。接続が切断されると、元のモードに戻ります。

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

## 続きを読む {#read-more}

-   [Follower Read](/follower-read.md)

<CustomContent platform="tidb">

-   [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)
-   [TiDB ダッシュボード - キー ビジュアライザー ページ](/dashboard/dashboard-key-visualizer.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)
-   [TiDB Cloudキー ビジュアライザー ページ](/tidb-cloud/tune-performance.md#key-visualizer)

</CustomContent>
