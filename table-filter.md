---
title: Table Filter
summary: Usage of table filter feature in TiDB tools.
---

# テーブルフィルター {#table-filter}

TiDB移行ツールは、デフォルトですべてのデータベースで動作しますが、多くの場合、サブセットのみが必要です。たとえば、 `foo*`と`bar*`の形式のスキーマのみを操作し、それ以外は何も操作したくないとします。

TiDB 4.0以降、すべてのTiDB移行ツールは、サブセットを定義するための共通のフィルター構文を共有しています。このドキュメントでは、テーブルフィルタ機能の使用方法について説明します。

## 使用法 {#usage}

### CLI {#cli}

テーブルフィルターは、複数の`-f`または`--filter`コマンドラインパラメーターを使用してツールに適用できます。各フィルターは`db.table`の形式であり、各部分はワイルドカードにすることができます（ [次のセクション](#wildcards)でさらに説明されています）。以下に、各ツールの使用例を示します。

-   [BR](/br/backup-and-restore-tool.md) ：

    {{< copyable "" >}}

    ```shell
    ./br backup full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    #                ^~~~~~~~~~~~~~~~~~~~~~~
    ./br restore full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    #                 ^~~~~~~~~~~~~~~~~~~~~~~
    ```

-   [Dumpling](/dumpling-overview.md) ：

    {{< copyable "" >}}

    ```shell
    ./dumpling -f 'foo*.*' -f 'bar*.*' -P 3306 -o /tmp/data/
    #          ^~~~~~~~~~~~~~~~~~~~~~~
    ```

-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) ：

    {{< copyable "" >}}

    ```shell
    ./tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    #                ^~~~~~~~~~~~~~~~~~~~~~~
    ```

### TOML構成ファイル {#toml-configuration-files}

TOMLファイルのテーブルフィルターは[文字列の配列](https://toml.io/en/v1.0.0-rc.1#section-15)として指定されます。以下に、各ツールの使用例を示します。

-   TiDB Lightning：

    ```toml
    [mydumper]
    filter = ['foo*.*', 'bar*.*']
    ```

-   [TiCDC](/ticdc/ticdc-overview.md) ：

    ```toml
    [filter]
    rules = ['foo*.*', 'bar*.*']

    [[sink.dispatchers]]
    matcher = ['db1.*', 'db2.*', 'db3.*']
    dispatcher = 'ts'
    ```

## 構文 {#syntax}

### プレーンテーブル名 {#plain-table-names}

各テーブルフィルタールールは、ドット（ `.` ）で区切られた「スキーマパターン」と「テーブルパターン」で構成されます。完全修飾名がルールに一致するテーブルが受け入れられます。

```
db1.tbl1
db2.tbl2
db3.tbl3
```

プレーンな名前は、次のように有効な[識別子文字](/schema-object-names.md)のみで構成されている必要があります。

-   `9` `0`
-   文字（ `a`から`z` `Z` `A`
-   `$`
-   `_`
-   非ASCII文字（U+0080からU+10FFFF）

他のすべてのASCII文字は予約されています。次のセクションで説明するように、句読点の中には特別な意味を持つものがあります。

### ワイルドカード {#wildcards}

名前の各部分は、 [fnmatch（3）](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_13)で説明されているワイルドカード記号にすることができます。

-   `*`個以上の文字に一致します
-   `?`文字に一致
-   `[a-z]` —「a」と「z」の間の1文字に包括的に一致します
-   `[!a-z]` —「a」から「z」を除く1文字に一致します。

```
db[0-9].tbl[0-9a-f][0-9a-f]
data.*
*.backup_*
```

ここでの「文字」とは、次のようなUnicodeコードポイントを意味します。

-   U + 00E9（é）は1文字です。
-   U + 0065 U + 0301（é）は2文字です。
-   U + 1F926 U + 1F3FF U + 200D U + 2640 U + FE0F（🤦🏿‍♀️）は5文字です。

### ファイルのインポート {#file-import}

フィルタルールとしてファイルをインポートするには、ルールの先頭に`@`を含めて、ファイル名を指定します。テーブルフィルターパーサーは、インポートされたファイルの各行を追加のフィルタールールとして扱います。

たとえば、ファイル`config/filter.txt`に次の内容がある場合：

```
employees.*
*.WorkOrder
```

次の2つの呼び出しは同等です。

```bash
./dumpling -f '@config/filter.txt'
./dumpling -f 'employees.*' -f '*.WorkOrder'
```

フィルタファイルは、別のファイルをさらにインポートすることはできません。

### コメントと空白行 {#comments-and-blank-lines}

フィルタファイル内では、すべての行の先頭と末尾の空白が削除されます。さらに、空白行（空の文字列）は無視されます。

先頭の`#`はコメントをマークし、無視されます。 `#`行の先頭にない場合は、構文エラーと見なされます。

```
# this line is a comment
db.table   # but this part is not comment and may cause error
```

### 除外 {#exclusion}

ルールの先頭にある`!`は、テーブルを処理から除外するために使用された後のパターンを意味します。これにより、フィルターが効果的にブロックリストに変わります。

```
*.*
#^ note: must add the *.* to include all tables first
!*.Password
!employees.salaries
```

### エスケープ文字 {#escape-character}

特殊文字を識別子文字に変換するには、その前に円記号`\`を付けます。

```
db\.with\.dots.*
```

単純化と将来の互換性のために、次のシーケンスは禁止されています。

-   空白をトリミングした後の行の終わりに`\` （ `[ ]`を使用して最後のリテラル空白に一致させます）。
-   `\`の後にASCII英数字（ `[0-9a-zA-Z]` ）が続きます。特に、 `\0`のようなCのような`\t`シーケンスは現在意味があり`\r` `\n` 。

### 引用された識別子 {#quoted-identifier}

`\`の他に、 `"`または`` ` ``を使用して引用符で囲むことにより、特殊文字を抑制することもできます。

```
"db.with.dots"."tbl\1"
`db.with.dots`.`tbl\2`
```

引用符は、それ自体を2倍にすることで識別子に含めることができます。

```
"foo""bar".`foo``bar`
# equivalent to:
foo\"bar.foo\`bar
```

引用符で囲まれた識別子は複数行にまたがることはできません。

識別子を部分的に引用することは無効です。

```
"this is "invalid*.*
```

### 正規表現 {#regular-expression}

非常に複雑なルールが必要な場合は、各パターンを`/`で区切られた正規表現として記述できます。

```
/^db\d{2,}$/./^tbl\d{2,}$/
```

これらの正規表現は[方言に行く](https://pkg.go.dev/regexp/syntax?tab=doc)を使用します。識別子に正規表現に一致する部分文字列が含まれている場合、パターンは一致します。たとえば、 `/b/`は`db01`に一致します。

> **ノート：**
>
> 正規表現のすべての`/`は、 `[…]`の内部を含め、 `\/`としてエスケープする必要があります。エスケープされていない`/`を`\Q…\E`の間に配置することはできません。

## 複数のルール {#multiple-rules}

テーブル名がフィルターリストのどのルールにも一致しない場合、デフォルトの動作では、そのような一致しないテーブルは無視されます。

ブロックリストを作成するには、最初のルールとして明示的な`*.*`を使用する必要があります。そうしないと、すべてのテーブルが除外されます。

```bash
# every table will be filtered out
./dumpling -f '!*.Password'

# only the "Password" table is filtered out, the rest are included.
./dumpling -f '*.*' -f '!*.Password'
```

フィルタリストでは、テーブル名が複数のパターンに一致する場合、最後の一致が結果を決定します。例えば：

```
# rule 1
employees.*
# rule 2
!*.dep*
# rule 3
*.departments
```

フィルタリングされた結果は次のとおりです。

| テーブル名                 | ルール1 | ルール2 | ルール3 | 結果          |
| --------------------- | ---- | ---- | ---- | ----------- |
| irrelevant.table      |      |      |      | デフォルト（拒否）   |
| 従業員。従業員               | ✓✓   |      |      | ルール1（受け入れる） |
| employees.dept_emp    | ✓✓   | ✓✓   |      | ルール2（拒否）    |
| employees.departments | ✓✓   | ✓✓   | ✓✓   | ルール3（受け入れる） |
| else.departments      |      | ✓✓   | ✓✓   | ルール3（受け入れる） |

> **ノート：**
>
> TiDBツールでは、システムスキーマは常にデフォルト構成で除外されます。システムスキーマは次のとおりです。
>
> -   `INFORMATION_SCHEMA`
> -   `PERFORMANCE_SCHEMA`
> -   `METRICS_SCHEMA`
> -   `INSPECTION_SCHEMA`
> -   `mysql`
> -   `sys`
