---
title: UUID Best Practices
summary: UUID を主キーとして使用すると、ネットワーク トリップの削減、ほとんどのプログラミング言語とデータベースのサポート、列挙攻撃からの保護などの利点が得られます。UUID は `BINARY(16)` 列にバイナリとして保存することをお勧めします。また、ホットスポットを防ぐために、TiDB で `swap_flag` を設定しないようにすることをお勧めします。UUID には MySQL 互換性があります。
---

# UUID のベスト プラクティス {#uuid-best-practices}

## UUIDの概要 {#overview-of-uuids}

`AUTO_INCREMENT`整数値の代わりに主キーとして使用すると、ユニバーサル一意識別子 (UUID) には次の利点があります。

-   UUID は、競合のリスクなしに複数のシステムで生成できます。場合によっては、これにより TiDB へのネットワーク トリップの回数が減り、パフォーマンスが向上します。
-   UUID は、ほとんどのプログラミング言語とデータベース システムでサポートされています。
-   URL の一部として使用される場合、UUID は列挙攻撃に対して脆弱ではありません。比較すると、 `auto_increment`数字の場合、請求書 ID またはユーザー ID を推測することが可能です。

## ベストプラクティス {#best-practices}

### バイナリとして保存 {#store-as-binary}

テキスト UUID 形式は次のようになります: `ab06f63e-8fe7-11ec-a514-5405db7aad56` 、これは 36 文字の文字列です。 `UUID_TO_BIN()`を使用すると、テキスト形式を 16 バイトのバイナリ形式に変換できます。これにより、テキストを`BINARY(16)`列に格納できます。 UUID を取得するときは、 `BIN_TO_UUID()`関数を使用してテキスト形式に戻すことができます。

### UUID形式のバイナリ順序とクラスター化されたPK {#uuid-format-binary-order-and-a-clustered-pk}

`UUID_TO_BIN()`関数は、 1 つの引数 (UUID) または 2 つの引数 (2 番目の引数が`swap_flag`とともに使用できます。

<CustomContent platform="tidb">

[ホットスポット](/best-practices/high-concurrency-best-practices.md)回避するために、 TiDB で`swap_flag`設定しないことをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

ホットスポットを回避するために、TiDB では`swap_flag`設定しないことをお勧めします。

</CustomContent>

ホットスポットを回避するために、UUID ベースの主キーに[`CLUSTERED`オプション](/clustered-indexes.md)明示的に設定することもできます。

`swap_flag`の効果を示すために、同じ構造を持つ 2 つのテーブルを示します。違いは、 `uuid_demo_1`に挿入されたデータは`UUID_TO_BIN(?, 0)`使用し、 `uuid_demo_2` `UUID_TO_BIN(?, 1)`を使用することです。

<CustomContent platform="tidb">

以下の[キービジュアライザー](/dashboard/dashboard-key-visualizer.md)のスクリーンショットでは、バイナリ形式でフィールドの順序が入れ替わった`uuid_demo_2`のテーブルの単一の領域に書き込みが集中していることがわかります。

</CustomContent>

<CustomContent platform="tidb-cloud">

以下の[キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)のスクリーンショットでは、バイナリ形式でフィールドの順序が入れ替わった`uuid_demo_2`のテーブルの単一の領域に書き込みが集中していることがわかります。

</CustomContent>

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

## MySQL 互換性 {#mysql-compatibility}

UUID は MySQL でも使用できます。1 および`BIN_TO_UUID()`関数は`UUID_TO_BIN()` 8.0 で導入されました。5 関数`UUID()`以前のバージョンの MySQL でも使用できます。
