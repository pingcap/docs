---
title: Follower Read
summary: Learn how to use Follower Read to optimize query performance.
---

# フォロワーの読み取り {#follower-read}

このドキュメントでは、フォロワー読み取りを使用してクエリのパフォーマンスを最適化する方法を紹介します。

## 序章 {#introduction}

TiDBは、 [リージョン](/tidb-storage.md#region)を基本単位として使用して、クラスタのすべてのノードにデータを分散します。リージョンには複数のレプリカを含めることができ、レプリカはリーダーと複数のフォロワーに分割されます。リーダーのデータが変更されると、TiDBはデータをフォロワーに同期的に更新します。

デフォルトでは、TiDBは同じリージョンのリーダーでのみデータの読み取りと書き込みを行います。リージョンリージョンがシステム全体の読み取りボトルネックになる可能性があります。この状況で、フォロワー読み取り機能を有効にすると、リーダーの負荷が大幅に軽減され、複数のフォロワー間で負荷が分散されるため、システム全体のスループットが向上します。

## いつ使用するか {#when-to-use}

アプリケーションのホットスポットリージョンが[TiDBダッシュボードキービジュアライザーページ](/dashboard/dashboard-key-visualizer.md)にあるかどうかを視覚的に分析できます。 「メトリック選択ボックス」を`Read (bytes)`または`Read (keys)`に選択すると、読み取りホットスポットが発生するかどうかを確認できます。

ホットスポットの処理の詳細については、 [TiDBホットスポットの問題処理](/troubleshoot-hot-spot-issues.md)を参照してください。

読み取りホットスポットが避けられない場合、またはコストの変更が非常に高い場合は、フォロワー読み取り機能を使用して、フォロワーリージョンへの読み取り要求のバランスをより適切にロードしてみてください。

## フォロワー読み取りを有効にする {#enable-follower-read}

<SimpleTab>
<div label="SQL">

フォロワー読み取りを有効にするには、変数`tidb_replica_read` （デフォルト値は`leader` ）を`follower`または`leader-and-follower`に設定します。

{{< copyable "" >}}

```sql
SET [GLOBAL] tidb_replica_read = 'follower';
```

この変数の詳細については、 [フォロワー読み取りの使用法](/follower-read.md#usage)を参照してください。

</div>
<div label="Java">

Javaでは、フォロワー読み取りを有効にするには、 `FollowerReadHelper`のクラスを定義します。

{{< copyable "" >}}

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

フォロワーノードからデータを読み取るときは、 `setSessionReplicaRead(conn, FollowReadMode.LEADER_AND_FOLLOWER)`つの方法を使用してフォロワー読み取り機能を有効にします。これにより、現在のセッションでリーダーノードとフォロワーノードの間の負荷を分散できます。接続が切断されると、元のモードに戻ります。

{{< copyable "" >}}

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

-   [フォロワーの読み取り](/follower-read.md)
-   [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)
-   [TiDBダッシュボード-主要なビジュアライザーページ](/dashboard/dashboard-key-visualizer.md)
