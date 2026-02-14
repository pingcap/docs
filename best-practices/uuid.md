---
title: Best Practices for Using UUIDs as Primary Keys
summary: UUIDを主キーとして使用すると、ネットワーク通信の削減、ほとんどのプログラミング言語とデータベースでのサポート、列挙攻撃からの保護などの利点が得られます。UUIDはバイナリ形式でBINARY(16)`列に保存することをお勧めします。また、ホットスポットの発生を防ぐため、TiDBでは`swap_flag`の設定を避けることをお勧めします。UUIDはMySQLと互換性があります。
aliases: ['/ja/tidb/stable/uuid/','/ja/tidbcloud/uuid/']
---

# UUIDを主キーとして使用するベストプラクティス {#best-practices-for-using-uuids-as-primary-keys}

UUID（Universally Unique Identifiers）は、分散データベースにおける主キーとして、自動増分整数の代替として広く利用されています。このドキュメントでは、TiDBでUUIDを使用するメリットを概説し、UUIDを効率的に保存およびインデックス化するためのベストプラクティスを紹介します。

## UUIDの概要 {#overview-of-uuids}

UUID を主キーとして使用すると、 [`AUTO_INCREMENT`](/auto-increment.md)整数と比較して次の利点があります。

-   UUIDは複数のシステムで競合のリスクなく生成できます。場合によっては、TiDBへのネットワーク通信回数を削減し、パフォーマンスを向上させることができます。
-   UUID は、ほとんどのプログラミング言語とデータベース システムでサポートされています。
-   URLの一部として使用される場合、UUIDは列挙攻撃に対して脆弱ではありません。一方、 `AUTO_INCREMENT`数字を使用すると、請求書IDやユーザーIDを推測される可能性があります。

## ベストプラクティス {#best-practices}

このセクションでは、TiDB で UUID を保存およびインデックス付けするためのベスト プラクティスについて説明します。

### バイナリとして保存 {#store-as-binary}

テキスト形式のUUID形式は次のようになります`ab06f63e-8fe7-11ec-a514-5405db7aad56`は36文字の文字列です。3 [`UUID_TO_BIN()`](/functions-and-operators/miscellaneous-functions.md#uuid_to_bin)使用すると、テキスト形式を16バイトのバイナリ形式に変換できます。これにより、テキストを[`BINARY(16)`](/data-type-string.md#binary-type)列に格納できます。UUIDを取得する際には、 [`BIN_TO_UUID()`](/functions-and-operators/miscellaneous-functions.md#bin_to_uuid)関数を使用してテキスト形式に戻すことができます。

### UUID形式のバイナリ順序とクラスター化された主キー {#uuid-format-binary-order-and-clustered-primary-keys}

`UUID_TO_BIN()`関数は、 1 つの引数 (UUID)、または 2 つの引数 (2 番目の引数は`swap_flag`とともに使用できます。

[ホットスポット](/best-practices/high-concurrency-best-practices.md)回避するために、 TiDB で`swap_flag`設定しないことをお勧めします。

ホットスポットを回避するために、UUID ベースの主キーに[`CLUSTERED`オプション](/clustered-indexes.md)明示的に設定することもできます。

`swap_flag`の効果を示すために、同じ構造を持つ2つのテーブルを示します。違いは、 `uuid_demo_1`に挿入されたデータは`UUID_TO_BIN(?, 0)`使用し、 `uuid_demo_2` `UUID_TO_BIN(?, 1)`使用していることです。

以下の Key Visualizer のスクリーンショットでは、バイナリ形式でフィールドの順序が入れ替わった`uuid_demo_2`テーブルの 1 つの領域に書き込みが集中していることがわかります。

![Key Visualizer](/media/best-practices/uuid_keyviz.png)

```sql
CREATE TABLE `uuid_demo_1` (
  `uuid` varbinary(16) NOT NULL,
  `c1` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`) CLUSTERED
)
```

```sql
CREATE TABLE `uuid_demo_2` (
  `uuid` varbinary(16) NOT NULL,
  `c1` varchar(255) NOT NULL,
  PRIMARY KEY (`uuid`) CLUSTERED
)
```

Key Visualizer の詳細については、次のドキュメントを参照してください。

-   TiDBセルフマネージドの場合は[キービジュアライザー](/dashboard/dashboard-key-visualizer.md)
-   TiDB Cloudの場合は[キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)

## MySQLの互換性 {#mysql-compatibility}

UUIDはMySQLでも使用できます。1と`UUID_TO_BIN()` `BIN_TO_UUID()`はMySQL 8.0で導入されました。5 `UUID()`関数はそれ以前のMySQLバージョンでも使用できます。
