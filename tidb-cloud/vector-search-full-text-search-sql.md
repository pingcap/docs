---
title: Full-Text Search with SQL
summary: 全文検索を使用すると、キーワードに完全一致するドキュメントを検索できます。検索拡張生成（RAG）シナリオでは、全文検索とベクター検索を併用することで、検索品質を向上させることができます。
---

# SQLによる全文検索 {#full-text-search-with-sql}

意味的類似性に重点を置く[ベクトル検索](/tidb-cloud/vector-search-overview.md)とは異なり、全文検索では正確なキーワードで文書を検索できます。検索拡張生成（RAG）シナリオでは、全文検索とベクトル検索を併用することで、検索品質を向上させることができます。

TiDB の全文検索機能は、次の機能を提供します。

-   **テキスト データを直接クエリします**。埋め込みプロセスなしで任意の文字列列を直接検索できます。

-   **複数言語のサポート**：高品質な検索のために言語を指定する必要はありません。TiDBのテキストアナライザーは、同一テーブル内に複数言語の文書が混在していてもサポートし、各文書に最適なアナライザーを自動的に選択します。

-   **関連性による並べ替え**: 広く採用されている[BM25ランキング](https://en.wikipedia.org/wiki/Okapi_BM25)アルゴリズムを使用して、検索結果を関連性によって並べ替えることができます。

-   **SQL と完全に互換性があります**。事前フィルタリング、事後フィルタリング、グループ化、結合などのすべての SQL 機能をフルテキスト検索で使用できます。

> **ヒント：**
>
> Python の使用方法については、 [Pythonによる全文検索](/tidb-cloud/vector-search-full-text-search-python.md)参照してください。
>
> AI アプリで全文検索とベクトル検索を併用するには、 [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)参照してください。

## 始めましょう {#get-started}

全文検索機能はまだ初期段階にあり、今後もさらに多くのお客様にご利用いただけるよう順次展開していきます。現在、全文検索機能は下記の製品オプションとリージョンでのみご利用いただけます。

-   TiDB Cloudサーバーレス: フランクフルト (eu-central-1)

全文検索を使用する前に、 TiDB Cloud Serverless クラスターがサポート対象リージョンに作成されていることを確認してください。まだ作成していない場合は、手順[TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って作成してください。

全文検索を実行するには、次の手順に従います。

1.  [**全文インデックスを作成する**](#create-a-full-text-index) : フルテキスト インデックスを持つテーブルを作成するか、既存のテーブルにフルテキスト インデックスを追加します。

2.  [**テキストデータを挿入する**](#insert-text-data) : テーブルにテキストデータを挿入します。

3.  [**全文検索を実行する**](#perform-a-full-text-search) : テキスト クエリと全文検索関数を使用して全文検索を実行します。

### 全文インデックスを作成する {#create-a-full-text-index}

全文検索を実行するには、効率的な検索とランキングに必要なデータ構造を提供する全文インデックスが必要です。全文インデックスは、新しいテーブルに作成することも、既存のテーブルに追加することもできます。

フルテキスト インデックスを持つテーブルを作成します。

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT,
    FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
);
```

または、既存のテーブルにフルテキスト インデックスを追加します。

```sql
CREATE TABLE stock_items(
    id INT,
    title TEXT
);

-- You might insert some data here.
-- The full-text index can be created even if data is already in the table.

ALTER TABLE stock_items ADD FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL ADD_COLUMNAR_REPLICA_ON_DEMAND;
```

`WITH PARSER <PARSER_NAME>`節では次のパーサーが受け入れられます。

-   `STANDARD` : 高速、英語コンテンツに適しており、スペースと句読点で単語を分割します。

-   `MULTILINGUAL` : 英語、中国語、日本語、韓国語など複数の言語をサポートします。

### テキストデータを挿入する {#insert-text-data}

フルテキスト インデックスを持つテーブルにデータを挿入する方法は、他のテーブルにデータを挿入する方法と同じです。

例えば、以下のSQL文を実行すると、複数の言語でデータを挿入できます。TiDBの多言語パーサーがテキストを自動的に処理します。

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

**例: 最も関連性の高い10件の文書を検索する**

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

**例: ユーザークエリに一致するドキュメントの数を数える**

```sql
SELECT COUNT(*) FROM stock_items
    WHERE fts_match_word("bluetoothイヤホン", title);

+----------+
| COUNT(*) |
+----------+
|        5 |
+----------+
```

## 高度な例: 検索結果を他のテーブルと結合する {#advanced-example-join-search-results-with-other-tables}

全文検索を、結合やサブクエリなどの他の SQL 機能と組み合わせることができます。

`users`テーブルと`tickets`テーブルがあり、作成者の名前の全文検索に基づいて作成者によって作成されたチケットを見つけたいとします。

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

サブクエリを使用して、作成者の名前に基づいて一致するユーザー ID を見つけ、これらの ID を外部クエリで使用して、関連するチケット情報を取得および結合することができます。

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

## 参照 {#see-also}

-   [ハイブリッド検索](/tidb-cloud/vector-search-hybrid-search.md)

## フィードバックとヘルプ {#feedback-x26-help}

全文検索はまだ初期段階にあり、アクセス範囲が限られています。まだご利用いただけない地域で全文検索をお試しになりたい場合、またはフィードバックやサポートが必要な場合は、お気軽にお問い合わせください。

<CustomContent platform="tidb">

-   [Discordに参加する](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [Discordに参加する](https://discord.gg/zcqexutz2R)
-   [サポートポータルをご覧ください](https://tidb.support.pingcap.com/)

</CustomContent>
