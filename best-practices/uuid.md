---
title: UUID Best Practices
summary: Learn best practice and strategy for using UUIDs with TiDB.
---

# UUID のベスト プラクティス {#uuid-best-practices}

## UUID の概要 {#overview-of-uuids}

Universally Unique Identifier (UUID) を`AUTO_INCREMENT`整数値の代わりに主キーとして使用すると、次の利点があります。

-   UUID は、競合の危険を冒さずに複数のシステムで生成できます。場合によっては、これは TiDB へのネットワーク トリップの回数を減らすことができ、パフォーマンスの向上につながることを意味します。
-   UUID は、ほとんどのプログラミング言語とデータベース システムでサポートされています。
-   URL の一部として使用される場合、UUID は列挙攻撃に対して脆弱ではありません。これに対し、数字が`auto_increment`場合は、請求書 ID やユーザー ID を推測できます。

## ベストプラクティス {#best-practices}

### バイナリとして保存 {#store-as-binary}

テキストの UUID 形式は次のようになります: `ab06f63e-8fe7-11ec-a514-5405db7aad56` 、これは 36 文字の文字列です。 `UUID_TO_BIN()`を使用すると、テキスト形式を 16 バイトのバイナリ形式に変換できます。これにより、テキストを`BINARY(16)`列に格納できます。 UUID を取得するときは、 `BIN_TO_UUID()`関数を使用してテキスト形式に戻すことができます。

### UUID 形式のバイナリ順序とクラスター化された PK {#uuid-format-binary-order-and-a-clustered-pk}

`UUID_TO_BIN()`関数は、1 つの引数、UUID、または 2 番目の引数が`swap_flag`である 2 つの引数と共に使用できます。

<CustomContent platform="tidb">

[ホットスポット](/best-practices/high-concurrency-best-practices.md)を回避するために、TiDB で`swap_flag`設定しないことをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

ホットスポットを避けるために、TiDB で`swap_flag`設定しないことをお勧めします。

</CustomContent>

ホットスポットを回避するために、UUID ベースの主キーに明示的に[`CLUSTERED`オプション](/clustered-indexes.md)を設定することもできます。

`swap_flag`の効果を示すために、同じ構造を持つ 2 つのテーブルを次に示します。違いは、 `uuid_demo_1`に挿入されたデータが`UUID_TO_BIN(?, 0)`を使用し、 `uuid_demo_2` `UUID_TO_BIN(?, 1)`を使用することです。

<CustomContent platform="tidb">

以下の[キー ビジュアライザー](/dashboard/dashboard-key-visualizer.md)のスクリーンショットでは、バイナリ形式でフィールドの順序が入れ替わっている`uuid_demo_2`テーブルの 1 つの領域に書き込みが集中していることがわかります。

</CustomContent>

<CustomContent platform="tidb-cloud">

以下の[キー ビジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)のスクリーンショットでは、バイナリ形式でフィールドの順序が入れ替わっている`uuid_demo_2`テーブルの 1 つの領域に書き込みが集中していることがわかります。

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

## MySQL の互換性 {#mysql-compatibility}

UUID は MySQL でも使用できます。 `BIN_TO_UUID()`および`UUID_TO_BIN()`関数は、 MySQL 8.0 で導入されました。 `UUID()`関数は、以前の MySQL バージョンでも使用できます。
