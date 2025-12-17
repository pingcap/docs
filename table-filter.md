---
title: Table Filter
summary: TiDB ツールでのテーブル フィルター機能の使用。
---

# テーブルフィルター {#table-filter}

TiDB移行ツールはデフォルトですべてのデータベースで動作しますが、多くの場合、一部のみが必要です。例えば、スキーマ`foo*`と`bar*`のみを扱い、それ以外のスキーマは使用したくない場合があります。

TiDB 4.0以降、すべてのTiDB移行ツールは、サブセットを定義するための共通のフィルター構文を共有しています。このドキュメントでは、テーブルフィルター機能の使用方法を説明します。

## 使用法 {#usage}

### コマンドライン {#cli}

テーブルフィルターは、 `-f`または`--filter`コマンドラインパラメータを複数指定することでツールに適用できます。各フィルターは`db.table`の形式で、各パラメータにはワイルドカードを使用できます（詳細は[次のセクション](#wildcards)を参照してください）。以下に使用例を示します。

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

TOMLファイル内のテーブルフィルターは[文字列の配列](https://toml.io/en/v1.0.0-rc.1#section-15)として指定されます。以下に使用例を示します。

-   TiDB Lightning:

    ```toml
    [mydumper]
    filter = ['foo*.*', 'bar*.*']
    ```

<CustomContent platform="tidb">

-   [TiCDC](/ticdc/ticdc-overview.md) :

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

各テーブルフィルタルールは、「スキーマパターン」と「テーブルパターン」で構成され、ドット（ `.` ）で区切られます。完全修飾名がルールに一致するテーブルが受け入れられます。

    db1.tbl1
    db2.tbl2
    db3.tbl3

プレーン名は、次のように有効な[識別子文字](/schema-object-names.md)のみで構成する必要があります。

-   数字（ `0` ～ `9` ）
-   文字（ `a` ～ `z` ～ `A` `Z`
-   `$`
-   `_`
-   非ASCII文字（U+0080からU+10FFFF）

その他のASCII文字はすべて予約されています。一部の句読点は特別な意味を持ちます。次のセクションで説明します。

### ワイルドカード {#wildcards}

名前の各部分には、 [fnmatch(3)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_13)で説明したワイルドカード記号を使用できます。

-   `*` — 0文字以上の文字に一致
-   `?` — 1文字に一致
-   `[a-z]` — 「a」から「z」までの間の1文字に一致します
-   `[!a-z]` — 「a」から「z」を除く 1 つの文字に一致します。

<!---->

    db[0-9].tbl[0-9a-f][0-9a-f]
    data.*
    *.backup_*

ここでの「文字」とは、次のような Unicode コード ポイントを意味します。

-   U+00E9 (é) は 1 文字です。
-   U+0065 U+0301 (é) は 2 文字です。
-   U+1F926 U+1F3FF U+200D U+2640 U+FE0F (🤦🏿‍♀️) は 5 つの文字です。

### ファイルのインポート {#file-import}

ファイルをフィルタールールとしてインポートするには、ルールの先頭にファイル名を指定するための「 `@`を追加します。テーブルフィルターパーサーは、インポートされたファイルの各行を追加のフィルタールールとして扱います。

たとえば、ファイル`config/filter.txt`内容が次の場合:

    employees.*
    *.WorkOrder

次の 2 つの呼び出しは同等です。

```bash
tiup dumpling -f '@config/filter.txt'
tiup dumpling -f 'employees.*' -f '*.WorkOrder'
```

フィルター ファイルでは、さらに別のファイルをインポートすることはできません。

### コメントと空白行 {#comments-and-blank-lines}

フィルターファイル内では、各行の先頭と末尾の空白文字は削除されます。また、空行（空文字列）は無視されます。

先頭の`#`はコメントを示すため無視されます。行の先頭に`#`ない場合は構文エラーとみなされます。

    # this line is a comment
    db.table   # but this part is not comment and may cause error

### 除外 {#exclusion}

ルールの先頭に「 `!`がある場合、その直後のパターンは処理対象からテーブルを除外するために使用されます。これにより、フィルターは実質的にブロックリストになります。

    *.*
    #^ note: must add the *.* to include all tables first
    !*.Password
    !employees.salaries

### エスケープ文字 {#escape-character}

特殊文字を識別子文字に変換するには、その前にバックスラッシュ`\`を付けます。

    db\.with\.dots.*

簡潔性と将来の互換性のため、次のシーケンスは禁止されています。

-   空白をトリミングした後の行末に`\`ます (末尾のリテラル空白に一致させるには`[ ]`使用します)。
-   `\`に続く任意のASCII英数字（ `[0-9a-zA-Z]` ）。特に、 `\0` 、 `\r` 、 `\n` 、 `\t`のようなC言語風のエスケープシーケンスは、現時点では意味を持ちません。

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

これらの正規表現は[囲碁方言](https://pkg.go.dev/regexp/syntax?tab=doc)を使用します。識別子に正規表現に一致する部分文字列が含まれている場合、パターンは一致します。例えば、 `/b/`は`db01`一致します。

> **注記：**
>
> 正規表現内の`/`すべて`\/`にエスケープする必要があります（ `[…]`の中も含む）。 `\Q…\E`の間にエスケープされていない`/`を置くことはできません。

## 複数のルール {#multiple-rules}

テーブル名がフィルター リスト内のどのルールにも一致しない場合は、デフォルトの動作ではそのような一致しないテーブルは無視されます。

ブロック リストを作成するには、最初のルールとして明示的に`*.*`使用する必要があります。そうしないと、すべてのテーブルが除外されます。

```bash
# every table will be filtered out
tiup dumpling -f '!*.Password'

# only the "Password" table is filtered out, the rest are included.
tiup dumpling -f '*.*' -f '!*.Password'
```

フィルターリストでは、テーブル名が複数のパターンに一致する場合、最後に一致したパターンに基づいて結果が決定されます。例:

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
| else.部門 |      | ✓    | ✓    | ルール3（受け入れる） |

> **注記：**
>
> TiDBツールでは、システムスキーマはデフォルト設定では常に除外されます。システムスキーマは以下のとおりです。
>
> -   `INFORMATION_SCHEMA`
> -   `PERFORMANCE_SCHEMA`
> -   `METRICS_SCHEMA`
> -   `INSPECTION_SCHEMA`
> -   `mysql`
> -   `sys`
