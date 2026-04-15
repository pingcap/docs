---
title: Get Started with TiDB + AI via SQL
summary: SQL文を使用してTiDBのベクトル検索を素早く使い始め、生成型AIアプリケーションを強化する方法を学びましょう。
aliases: ['/ja/tidb/stable/vector-search-get-started-using-sql/','/ja/tidb/dev/vector-search-get-started-using-sql/','/ja/tidbcloud/vector-search-get-started-using-sql/']
---

# SQL を介して TiDB + AI を使い始める {#get-started-with-tidb-ai-via-sql}

TiDB は、MySQL 構文を拡張して[ベクトル検索](/ai/concepts/vector-search-overview.md)をサポートし、新しい [ベクトルデータ型](/ai/reference/vector-search-data-types.md)といくつかの[ベクトル関数](/ai/reference/vector-search-functions-and-operators.md)を導入します。

このドキュメントでは、SQL ステートメントだけを使用して TiDB Vector Search を開始する方法を説明します。 [MySQLコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.4/en/mysql.html)を使用して、次の操作を実行する方法を学習します。

-   TiDBに接続します。
-   ベクターテーブルを作成します。
-   ベクトル埋め込みを保存する。
-   ベクトル検索クエリを実行します。

> **注記：**
>
> -   ベクトル検索機能はベータ版であり、予告なく変更される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。
> -   ベクトル検索機能は、 [TiDBセルフマネージド](/overview.md)[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 、および[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用できます。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBのバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## 前提条件 {#prerequisites}

この文書の手順を完了するには、以下が必要です。

-   [MySQLコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.4/en/mysql.html)(MySQL CLI)がマシンにインストールされています。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## さあ始めましょう {#get-started}

### ステップ1. TiDBに接続する {#step-1-connect-to-tidb}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、次に、対象のTiDB Cloud Starterインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、[接続**方法]**ドロップダウンリストから**[MySQL CLI]**を選択し、 **[接続タイプ]**のデフォルト設定を**[パブリック]**のままにします。

4.  まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成してください。

5.  接続コマンドをコピーしてターミナルに貼り付けてください。以下はmacOSの例です。

    ```bash
    mysql -u '<prefix>.root' -h '<host>' -P 4000 -D 'test' --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p'<password>'
    ```

</div>
<div label="TiDB Self-Managed" value="tidb">

TiDBセルフマネージドクラスタが起動したら、ターミナルでクラスタ接続コマンドを実行してください。

以下はmacOSにおける接続コマンドの例です。

```bash
mysql --comments --host 127.0.0.1 --port 4000 -u root
```

</div>

</SimpleTab>

### ステップ2. ベクターテーブルを作成する {#step-2-create-a-vector-table}

テーブルを作成する際、 `VECTOR`データ型を指定することで、列を[ベクター](/ai/concepts/vector-search-overview.md#vector-embedding)として定義できます。

例えば、3次元の列`embedded_documents`を持つテーブル`VECTOR` } を作成するには、MySQL CLI を使用して次の SQL ステートメントを実行します。

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

期待される出力は以下のとおりです。

```text
Query OK, 0 rows affected (0.27 sec)
```

### ステップ3. ベクトル埋め込みをテーブルに挿入する {#step-3-insert-vector-embeddings-to-the-table}

[ベクトル埋め込み](/ai/concepts/vector-search-overview.md#vector-embedding)だ 3 つのドキュメントを`embedded_documents`テーブルに挿入します。

```sql
INSERT INTO embedded_documents
VALUES
    (1, 'dog', '[1,2,1]'),
    (2, 'fish', '[1,2,4]'),
    (3, 'tree', '[1,0,0]');
```

期待される出力は以下のとおりです。

    Query OK, 3 rows affected (0.15 sec)
    Records: 3  Duplicates: 0  Warnings: 0

> **注記**
>
> この例では、ベクトル埋め込みの次元を簡略化し、説明のために3次元ベクトルのみを使用しています。
>
> 実際のアプリケーションでは、 [埋め込みモデル](/ai/concepts/vector-search-overview.md#embedding-model)は多くの場合、数百または数千の次元を持つベクトル埋め込みを生成します。

### ステップ4. ベクトルテーブルを照会する {#step-4-query-the-vector-table}

ドキュメントが正しく挿入されたことを確認するには、 `embedded_documents`テーブルを照会します。

```sql
SELECT * FROM embedded_documents;
```

期待される出力は以下のとおりです。

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

### ステップ5. ベクトル検索クエリを実行する {#step-5-perform-a-vector-search-query}

全文検索と同様に、ベクトル検索を使用する場合も、ユーザーはアプリケーションに検索語を入力します。

この例では、検索語は「泳ぐ動物」であり、それに対応するベクトル埋め込みは`[1,2,3]`であると想定されています。実際のアプリケーションでは、埋め込みモデルを使用して、ユーザーの検索語をベクトル埋め込みに変換する必要があります。

次の SQL ステートメントを実行すると、TiDB はテーブル内のベクトル埋め込み間のコサイン距離 ( `[1,2,3]`計算してソートすることにより、 `vec_cosine_distance` } に最も近い上位 3 つのドキュメントを特定します。

```sql
SELECT id, document, vec_cosine_distance(embedding, '[1,2,3]') AS distance
FROM embedded_documents
ORDER BY distance
LIMIT 3;
```

期待される出力は以下のとおりです。

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

検索結果の 3 つの用語は、クエリされたベクトルからのそれぞれの距離によってソートされます。距離が小さいほど、対応する`document`の関連性が高くなります。

したがって、出力結果から判断すると、泳いでいる動物は魚か、泳ぎの才能に恵まれた犬である可能性が最も高い。

## 関連項目 {#see-also}

-   [ベクトルデータ型](/ai/reference/vector-search-data-types.md)
-   [ベクトル検索インデックス](/ai/reference/vector-search-index.md)
