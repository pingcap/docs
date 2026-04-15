---
title: Full-Text Search with SQL
summary: 全文検索では、正確なキーワードに基づいて文書を検索できます。検索拡張生成（RAG）シナリオでは、全文検索とベクトル検索を組み合わせて使用​​することで、検索精度を向上させることができます。
aliases: ['/ja/tidb/stable/vector-search-full-text-search-sql/','/ja/tidbcloud/vector-search-full-text-search-sql/']
---

# SQLによる全文検索 {#full-text-search-with-sql}

意味的な類似性に焦点を当てる[ベクトル検索](/ai/concepts/vector-search-overview.md)とは異なり、全文検索では正確なキーワードに基づいて文書を取得できます。検索拡張生成（RAG）シナリオでは、全文検索とベクトル検索を組み合わせて使用​​することで、検索品質を向上させることができます。

TiDBの全文検索機能は、以下の機能を提供します。

-   **テキストデータを直接クエリする**：埋め込み処理を行わずに、任意の文字列列を直接検索できます。

-   **多言語対応**：高品質な検索を行うために言語を指定する必要はありません。TiDBのテキストアナラ​​イザーは、同一テーブル内に複数の言語で記述された文書が混在する場合でも対応し、各文書に最適なアナライザーを自動的に選択します。

-   **関連性順に並べる**: 広く採用されている[BM25ランキング](https://en.wikipedia.org/wiki/Okapi_BM25)アルゴリズムを使用して、検索結果を関連性順に並べ替えることができます。

-   **SQLとの完全な互換性**：事前フィルタリング、事後フィルタリング、グループ化、結合など、すべてのSQL機能を全文検索で使用できます。

> **ヒント：**
>
> Python の使い方については、 [Pythonによる全文検索](/ai/guides/vector-search-full-text-search-python.md)ご覧ください。
>
> AI アプリで全文検索とベクトル検索を併用するには、 [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)参照してください。

## さあ始めましょう {#get-started}

全文検索機能はまだ開発初期段階にあり、より多くのお客様に順次展開していく予定です。現在、全文検索機能は、以下のリージョンにおけるTiDB Cloud StarterおよびTiDB Cloud Essentialでのみご利用いただけます。

-   AWS: `Frankfurt (eu-central-1)`および`Singapore (ap-southeast-1)`

全文検索を使用する前に、 TiDB Cloud Starterインスタンスがサポートされているリージョンで作成されていることを確認してください。お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

全文検索を実行するには、以下の手順に従ってください。

1.  [**全文索引を作成する**](#create-a-full-text-index): フルテキスト インデックスを持つテーブルを作成するか、既存のテーブルにフルテキスト インデックスを追加します。

2.  テキストデータ[**テキストデータを挿入する**](#insert-text-data): テーブルにテキストデータを挿入します。

3.  [**全文検索を実行する**](#perform-a-full-text-search): テキストクエリと全文検索関数を使用して全文検索を実行します。

### 全文索引を作成する {#create-a-full-text-index}

全文検索を実行するには、効率的な検索とランキングに必要なデータ構造を提供する全文インデックスが必要です。全文インデックスは、新規テーブルに作成することも、既存のテーブルに追加することもできます。

全文検索インデックス付きのテーブルを作成します。

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT,
    FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
);
```

または、既存のテーブルに全文検索インデックスを追加します。

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT
);

-- You might insert some data here.
-- The full-text index can be created even if data is already in the table.

ALTER TABLE stock_items ADD FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL ADD_COLUMNAR_REPLICA_ON_DEMAND;
```

`WITH PARSER <PARSER_NAME>`句では、以下のパーサーが受け入れられます。

-   `STANDARD` : 高速で、英語コンテンツに対応し、スペースと句読点によって単語を分割します。

-   `MULTILINGUAL` : 英語、中国語、日本語、韓国語など、複数の言語をサポートしています。

### テキストデータを挿入する {#insert-text-data}

全文検索インデックスを持つテーブルにデータを挿入する方法は、他のテーブルにデータを挿入する方法と全く同じです。

例えば、以下のSQL文を実行することで、複数の言語でデータを挿入できます。TiDBの多言語パーサーがテキストを自動的に処理します。

```sql
INSERT INTO stock_items VALUES (1, "イヤホン bluetooth ワイヤレスイヤホン ");
INSERT INTO stock_items VALUES (2, "完全ワイヤレスイヤホン/ウルトラノイズキャンセリング 2.0 ");
INSERT INTO stock_items VALUES (3, "ワイヤレス ヘッドホン Bluetooth 5.3 65時間再生 ヘッドホン 40mm HD ");
INSERT INTO stock_items VALUES (4, "楽器用 オンイヤーヘッドホン 密閉型【国内正規品】");
INSERT INTO stock_items VALUES (5, "ワイヤレスイヤホン ハイブリッドANC搭載 40dBまでアクティブノイズキャンセル");
INSERT INTO stock_items VALUES (6, "Lightweight Bluetooth Earbuds with 48 Hours Playtime");
INSERT INTO stock_items VALUES (7, "True Wireless Noise Cancelling Earbuds - Compatible with Apple & Android, Built-in Microphone");
INSERT INTO stock_items VALUES (8, "In-Ear Earbud Headphones with Mic, Black");
INSERT INTO stock_items VALUES (9, "Wired Headphones, HD Bass Driven Audio, Lightweight Aluminum Wired in Ear Earbud Headphones");
INSERT INTO stock_items VALUES (10, "LED Light Bar, Music Sync RGB Light Bar, USB Ambient Lamp");
INSERT INTO stock_items VALUES (11, "无线消噪耳机-黑色 手势触控蓝牙降噪 主动降噪头戴式耳机（智能降噪 长久续航）");
INSERT INTO stock_items VALUES (12, "专业版USB7.1声道游戏耳机电竞耳麦头戴式电脑网课办公麦克风带线控");
INSERT INTO stock_items VALUES (13, "投影仪家用智能投影机便携卧室手机投影");
INSERT INTO stock_items VALUES (14, "无线蓝牙耳机超长续航42小时快速充电 流光金属耳机");
INSERT INTO stock_items VALUES (15, "皎月银 国家补贴 心率血氧监测 蓝牙通话 智能手表 男女表");
```

### 全文検索を実行する {#perform-a-full-text-search}

全文検索を実行するには、 `FTS_MATCH_WORD()`関数を使用できます。

**例：最も関連性の高い10件の文書を検索する**

```sql
SELECT * FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title)
    ORDER BY fts_match_word("bluetoothイヤホン", title)
    DESC LIMIT 10;

-- Results are ordered by relevance, with the most relevant documents first.

+------+-----------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                     |
+------+-----------------------------------------------------------------------------------------------------------+
|    1 | イヤホン bluetooth ワイヤレスイヤホン                                                                         |
|    6 | Lightweight Bluetooth Earbuds with 48 Hours Playtime                                                      |
|    2 | 完全ワイヤレスイヤホン/ウルトラノイズキャンセリング 2.0                                                           |
|    3 | ワイヤレス ヘッドホン Bluetooth 5.3 65時間再生 ヘッドホン 40mm HD                                               |
|    5 | ワイヤレスイヤホン ハイブリッドANC搭載 40dBまでアクティブノイズキャンセル                                            |
+------+-----------------------------------------------------------------------------------------------------------+

-- Try searching in another language:
SELECT * FROM stock_items
    WHERE fts_match_word("蓝牙耳机", title)
    ORDER BY fts_match_word("蓝牙耳机", title)
    DESC LIMIT 10;

-- Results are ordered by relevance, with the most relevant documents first.

+------+---------------------------------------------------------------------------------------------------------------+
| id   | title                                                                                                         |
+------+---------------------------------------------------------------------------------------------------------------+
|   14 | 无线蓝牙耳机超长续航42小时快速充电 流光金属耳机                                                                      |
|   11 | 无线消噪耳机-黑色 手势触控蓝牙降噪 主动降噪头戴式耳机（智能降噪 长久续航）                                                |
|   15 | 皎月银 国家补贴 心率血氧监测 蓝牙通话 智能手表 男女表                                                                 |
+------+---------------------------------------------------------------------------------------------------------------+
```

**例：ユーザーのクエリに一致するドキュメントの数をカウントする**

```sql
SELECT COUNT(*) FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title);

+----------+
| COUNT(*) |
+----------+
|        5 |
+----------+
```

## 高度な例：検索結果を他のテーブルと結合する {#advanced-example-join-search-results-with-other-tables}

全文検索は、結合やサブクエリなどの他のSQL機能と組み合わせることができます。

`users`テーブルと`tickets`テーブルがあり、著者の名前を全文検索して、著者が作成したチケットを見つけたいとします。

```sql
CREATE TABLE users(
    id INT,
    name TEXT,
    FULLTEXT INDEX (name) WITH PARSER STANDARD
);

INSERT INTO users VALUES (1, "Alice Smith");
INSERT INTO users VALUES (2, "Bob Johnson");

CREATE TABLE tickets(
    id INT,
    title TEXT,
    author_id INT
);

INSERT INTO tickets VALUES (1, "Ticket 1", 1);
INSERT INTO tickets VALUES (2, "Ticket 2", 1);
INSERT INTO tickets VALUES (3, "Ticket 3", 2);
```

サブクエリを使用して作成者名に基づいて一致するユーザーIDを検索し、これらのIDを外部クエリで使用して関連するチケット情報を取得および結合することができます。

```sql
SELECT t.title AS TICKET_TITLE, u.id AS AUTHOR_ID, u.name AS AUTHOR_NAME FROM tickets t
LEFT JOIN users u ON t.author_id = u.id
WHERE t.author_id IN
(
    SELECT id FROM users
    WHERE fts_match_word("Alice", name)
);

+--------------+-----------+-------------+
| TICKET_TITLE | AUTHOR_ID | AUTHOR_NAME |
+--------------+-----------+-------------+
| Ticket 1     |         1 | Alice Smith |
| Ticket 2     |         1 | Alice Smith |
+--------------+-----------+-------------+
```

## 関連項目 {#see-also}

-   [ハイブリッド検索](/ai/guides/vector-search-hybrid-search.md)

## フィードバックとヘルプ {#feedback-x26-help}

全文検索はまだ開発初期段階であり、利用できる地域が限られています。まだ利用できない地域で全文検索を試してみたい場合、またはご意見やご質問がある場合は、お気軽にお問い合わせください。

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
