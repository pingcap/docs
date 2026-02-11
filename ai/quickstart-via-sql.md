---
title: Get Started with TiDB + AI via SQL
summary: SQL ステートメントを使用して TiDB で Vector Search をすぐに開始し、生成 AI アプリケーションを強化する方法を学習します。
aliases: ['/tidb/stable/vector-search-get-started-using-sql/','/tidb/dev/vector-search-get-started-using-sql/','/tidbcloud/vector-search-get-started-using-sql/']
---

# SQL経由でTiDB + AIを使い始める {#get-started-with-tidb-ai-via-sql}

TiDB は MySQL 構文を拡張して[ベクトル検索](/ai/concepts/vector-search-overview.md)サポートし、新しい[ベクトルデータ型](/ai/reference/vector-search-data-types.md)といくつかの[ベクトル関数](/ai/reference/vector-search-functions-and-operators.md)を導入します。

このドキュメントでは、SQL文のみを使ってTiDB Vector Searchを使い始める方法を説明します。1 [MySQLコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.4/en/mysql.html)使って以下の操作を実行する方法を学びます。

-   TiDB クラスターに接続します。
-   ベクターテーブルを作成します。
-   ベクトル埋め込みを保存します。
-   ベクター検索クエリを実行します。

> **注記：**
>
> -   ベクター検索機能はベータ版であり、予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。
> -   ベクトル検索機能は[TiDBセルフマネージド](/overview.md) 、 [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential) 、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用可能です。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## 前提条件 {#prerequisites}

このドキュメントの手順を完了するには、次のものが必要です。

-   [MySQLコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.4/en/mysql.html) (MySQL CLI) がマシンにインストールされています。
-   TiDB クラスター。

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Starter クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

## 始めましょう {#get-started}

### ステップ1. TiDBクラスターに接続する {#step-1-connect-to-the-tidb-cluster}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **「接続先」**ドロップダウンリストから**「MySQL CLI」**を選択し、 **「接続タイプ」**のデフォルト設定を**「パブリック」**のままにします。

4.  まだパスワードを設定していない場合は、 **「パスワードの生成」をクリックしてランダムなパスワード**を生成します。

5.  接続コマンドをコピーしてターミナルに貼り付けます。以下はmacOSの例です。

    ```bash
    mysql -u '<prefix>.root' -h '<host>' -P 4000 -D 'test' --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p'<password>'
    ```

</div>
<div label="TiDB Self-Managed" value="tidb">

TiDB セルフマネージド クラスターが起動したら、ターミナルでクラスター接続コマンドを実行します。

以下は macOS の接続コマンドの例です。

```bash
mysql --comments --host 127.0.0.1 --port 4000 -u root
```

</div>

</SimpleTab>

### ステップ2.ベクターテーブルを作成する {#step-2-create-a-vector-table}

テーブルを作成するときに、 `VECTOR`データ型を指定して列を[ベクター](/ai/concepts/vector-search-overview.md#vector-embedding)列として定義できます。

たとえば、3 次元の`VECTOR`列を持つテーブル`embedded_documents`を作成するには、MySQL CLI を使用して次の SQL ステートメントを実行します。

```sql
USE test;
CREATE TABLE embedded_documents (
    id        INT       PRIMARY KEY,
    -- Column to store the original content of the document.
    document  TEXT,
    -- Column to store the vector representation of the document.
    embedding VECTOR(3)
);
```

期待される出力は次のとおりです。

```text
Query OK, 0 rows affected (0.27 sec)
```

### ステップ3. テーブルにベクトル埋め込みを挿入する {#step-3-insert-vector-embeddings-to-the-table}

[ベクトル埋め込み](/ai/concepts/vector-search-overview.md#vector-embedding)を持つ 3 つのドキュメントを`embedded_documents`つのテーブルに挿入します。

```sql
INSERT INTO embedded_documents
VALUES
    (1, 'dog', '[1,2,1]'),
    (2, 'fish', '[1,2,4]'),
    (3, 'tree', '[1,0,0]');
```

期待される出力は次のとおりです。

    Query OK, 3 rows affected (0.15 sec)
    Records: 3  Duplicates: 0  Warnings: 0

> **注記**
>
> この例では、ベクトル埋め込みの次元を簡略化し、デモンストレーションの目的で 3 次元ベクトルのみを使用します。
>
> 実際のアプリケーションでは、数百または数千の次元を持つ[埋め込みモデル](/ai/concepts/vector-search-overview.md#embedding-model)埋め込みが生成されることがよくあります。

### ステップ4.ベクターテーブルをクエリする {#step-4-query-the-vector-table}

ドキュメントが正しく挿入されたことを確認するには、 `embedded_documents`テーブルをクエリします。

```sql
SELECT * FROM embedded_documents;
```

期待される出力は次のとおりです。

```sql
+----+----------+-----------+
| id | document | embedding |
+----+----------+-----------+
|  1 | dog      | [1,2,1]   |
|  2 | fish     | [1,2,4]   |
|  3 | tree     | [1,0,0]   |
+----+----------+-----------+
3 rows in set (0.15 sec)
```

### ステップ5.ベクター検索クエリを実行する {#step-5-perform-a-vector-search-query}

全文検索と同様に、ベクター検索を使用する場合、ユーザーはアプリケーションに検索用語を提供します。

この例では、検索語は「泳ぐ動物」であり、対応するベクトル埋め込みは`[1,2,3]`と仮定されています。実際のアプリケーションでは、埋め込みモデルを使用してユーザーの検索語をベクトル埋め込みに変換する必要があります。

次のSQL文を実行すると、TiDBはテーブル内のベクトル埋め込み間のコサイン距離（ `vec_cosine_distance` ）を計算してソートし、 `[1,2,3]`に最も近い上位3つのドキュメントを識別します。

```sql
SELECT id, document, vec_cosine_distance(embedding, '[1,2,3]') AS distance
FROM embedded_documents
ORDER BY distance
LIMIT 3;
```

期待される出力は次のとおりです。

```plain
+----+----------+---------------------+
| id | document | distance            |
+----+----------+---------------------+
|  2 | fish     | 0.00853986601633272 |
|  1 | dog      | 0.12712843905603044 |
|  3 | tree     |  0.7327387580875756 |
+----+----------+---------------------+
3 rows in set (0.15 sec)
```

検索結果の 3 つの用語は、クエリされたベクトルからのそれぞれの距離によって並べ替えられます。距離が小さいほど、対応する`document`関連性が高くなります。

したがって、出力によれば、泳いでいる動物は魚、または泳ぐ才能のある犬である可能性が最も高いです。

## 参照 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクター検索インデックス](/ai/reference/vector-search-index.md)
