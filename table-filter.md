---
title: Table Filter
summary: TiDB ツールでのテーブル フィルター機能の使用。
---

# テーブルフィルター {#table-filter}

TiDB 移行ツールは、デフォルトではすべてのデータベースで動作しますが、多くの場合、サブセットのみが必要になります。たとえば、 `foo*`と`bar*`の形式のスキーマのみを操作し、他のスキーマは操作しないという場合です。

TiDB 4.0 以降、すべての TiDB 移行ツールはサブセットを定義するための共通のフィルター構文を共有しています。このドキュメントでは、テーブル フィルター機能の使用方法について説明します。

## 使用法 {#usage}

### コマンドライン {#cli}

テーブル フィルターは、複数の`-f`または`--filter`コマンド ライン パラメーターを使用してツールに適用できます。各フィルターは`db.table`の形式であり、各部分はワイルドカードにすることができます ( [次のセクション](#wildcards)でさらに詳しく説明します)。次に使用例を示します。

<CustomContent platform="tidb">

-   [BR](/br/backup-and-restore-overview.md) :

    ```shell
    tiup br backup full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    ```

    ```shell
    tiup br restore full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    ```

</CustomContent>

-   [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) :

    ```shell
    tiup dumpling -f 'foo*.*' -f 'bar*.*' -P 3306 -o /tmp/data/
    ```

<CustomContent platform="tidb">

-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) :

    ```shell
    tiup tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    ```

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview) :

    ```shell
    tiup tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    ```

</CustomContent>

### TOML設定ファイル {#toml-configuration-files}

TOML ファイル内のテーブル フィルターは[文字列の配列](https://toml.io/en/v1.0.0-rc.1#section-15)として指定されます。以下に使用例を示します。

-   TiDB Lightning:

    ```toml
    [mydumper]
    filter = ['foo*.*', 'bar*.*']
    ```

<CustomContent platform="tidb">

-   [ティCDC](/ticdc/ticdc-overview.md) :

    ```toml
    [filter]
    rules = ['foo*.*', 'bar*.*']

    [[sink.dispatchers]]
    matcher = ['db1.*', 'db2.*', 'db3.*']
    dispatcher = 'ts'
    ```

</CustomContent>

## 構文 {#syntax}

### プレーンテーブル名 {#plain-table-names}

各テーブル フィルタ ルールは、ドット ( `.` ) で区切られた「スキーマ パターン」と「テーブル パターン」で構成されます。完全修飾名がルールに一致するテーブルが受け入れられます。

    db1.tbl1
    db2.tbl2
    db3.tbl3

プレーン名は、次のように有効な[識別子文字](/schema-object-names.md)のみで構成する必要があります。

-   数字（ `0` ～ `9` ）
-   文字 ( `a`から`z` 、 `A`から`Z` )
-   `$`
-   `_`
-   非ASCII文字（U+0080からU+10FFFF）

その他の ASCII 文字はすべて予約されています。次のセクションで説明するように、一部の句読点には特別な意味があります。

### ワイルドカード {#wildcards}

名前の各部分には、 [fnmatch(3)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_13)で説明するワイルドカード記号を使用できます。

-   `*` — 0文字以上の文字に一致
-   `?` — 1文字に一致
-   `[a-z]` — 「a」から「z」までの間の1文字に一致します
-   `[!a-z]` — 「a」から「z」を除く 1 文字に一致します。

<!---->

    db[0-9].tbl[0-9a-f][0-9a-f]
    data.*
    *.backup_*

ここでの「文字」とは、次のような Unicode コード ポイントを意味します。

-   U+00E9 (é) は 1 文字です。
-   U+0065 U+0301 (é) は 2 文字です。
-   U+1F926 U+1F3FF U+200D U+2640 U+FE0F (🤦🏿‍♀️) は 5 文字です。

### ファイルのインポート {#file-import}

ファイルをフィルター ルールとしてインポートするには、ルールの先頭に`@`を追加してファイル名を指定します。テーブル フィルター パーサーは、インポートされたファイルの各行を追加のフィルター ルールとして扱います。

たとえば、ファイル`config/filter.txt`内容が次のとおりであるとします。

    employees.*
    *.WorkOrder

次の 2 つの呼び出しは同等です。

```bash
tiup dumpling -f '@config/filter.txt'
tiup dumpling -f 'employees.*' -f '*.WorkOrder'
```

フィルター ファイルでは、さらに別のファイルをインポートすることはできません。

### コメントと空白行 {#comments-and-blank-lines}

フィルター ファイル内では、各行の先頭と末尾の空白が削除されます。また、空白行 (空の文字列) は無視されます。

先頭の`#`コメントを表し、無視されます。行の先頭に`#`がない場合は、構文エラーと見なされます。

    # this line is a comment
    db.table   # but this part is not comment and may cause error

### 除外 {#exclusion}

ルールの先頭の`!` 、その後のパターンが処理対象からテーブルを除外するために使用されることを意味します。これにより、フィルターが実質的にブロック リストになります。

    *.*
    #^ note: must add the *.* to include all tables first
    !*.Password
    !employees.salaries

### エスケープ文字 {#escape-character}

特殊文字を識別子文字に変換するには、その前にバックスラッシュ`\`を付けます。

    db\.with\.dots.*

簡潔さと将来の互換性のため、次のシーケンスは禁止されています。

-   空白をトリミングした後の行末に`\` (末尾のリテラル空白に一致するには`[ ]`使用します)。
-   `\`の後に任意の ASCII 英数字が続きます ( `[0-9a-zA-Z]` )。特に、 `\0` 、 `\r` 、 `\n` 、 `\t`などの C のようなエスケープ シーケンスは現在意味がありません。

### 引用符付き識別子 {#quoted-identifier}

`\`以外にも、 `"`や`` ` ``を使って引用符で囲むことで特殊文字を抑制することもできます。

    "db.with.dots"."tbl\1"
    `db.with.dots`.`tbl\2`

引用符は、それ自体を二重にすることで識別子内に含めることができます。

    "foo""bar".`foo``bar`
    # equivalent to:
    foo\"bar.foo\`bar

引用符で囲まれた識別子は複数行にまたがることはできません。

識別子を部分的に引用することは無効です。

    "this is "invalid*.*

### 正規表現 {#regular-expression}

非常に複雑なルールが必要な場合は、各パターンを`/`で区切られた正規表現として記述できます。

    /^db\d{2,}$/./^tbl\d{2,}$/

これらの正規表現は[囲碁方言](https://pkg.go.dev/regexp/syntax?tab=doc)使用します。識別子に正規表現に一致する部分文字列が含まれている場合、パターンは一致します。たとえば、 `/b/`は`db01`と一致します。

> **注記：**
>
> 正規表現内のすべての`/` 、 `[…]`内も含めて`\/`としてエスケープする必要があります。 `\Q…\E`の間にエスケープされていない`/`を配置することはできません。

## 複数のルール {#multiple-rules}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションはTiDB Cloudには適用されません。現在、 TiDB Cloud は1 つのテーブル フィルター ルールのみをサポートしています。

</CustomContent>

テーブル名がフィルター リスト内のどのルールとも一致しない場合は、デフォルトの動作では、そのような一致しないテーブルは無視されます。

ブロック リストを作成するには、最初のルールとして明示的に`*.*`使用する必要があります。そうしないと、すべてのテーブルが除外されます。

```bash
# every table will be filtered out
tiup dumpling -f '!*.Password'

# only the "Password" table is filtered out, the rest are included.
tiup dumpling -f '*.*' -f '!*.Password'
```

フィルター リストでは、テーブル名が複数のパターンに一致する場合、最後の一致によって結果が決まります。例:

    # rule 1
    employees.*
    # rule 2
    !*.dep*
    # rule 3
    *.departments

フィルタリングされた結果は次のとおりです。

| テーブル名   | ルール1 | ルール2 | ルール3 | 結果          |
| ------- | ---- | ---- | ---- | ----------- |
| 無関係な表   |      |      |      | デフォルト（拒否）   |
| 従業員。従業員 | ✓    |      |      | ルール1（受け入れる） |
| 従業員.部門  | ✓    | ✓    |      | ルール2（拒否）    |
| 従業員.部門  | ✓    | ✓    | ✓    | ルール3（受け入れる） |
| それ以外の場合 |      | ✓    | ✓    | ルール3（受け入れる） |

> **注記：**
>
> TiDB ツールでは、システム スキーマはデフォルト構成では常に除外されます。システム スキーマは次のとおりです。
>
> -   `INFORMATION_SCHEMA`
> -   `PERFORMANCE_SCHEMA`
> -   `METRICS_SCHEMA`
> -   `INSPECTION_SCHEMA`
> -   `mysql`
> -   `sys`
