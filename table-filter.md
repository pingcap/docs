---
title: Table Filter
summary: Usage of table filter feature in TiDB tools.
---

# テーブル フィルター {#table-filter}

TiDB 移行ツールは、デフォルトですべてのデータベースで動作しますが、多くの場合、サブセットのみが必要です。たとえば、 `foo*`と`bar*`の形式のスキーマのみを操作し、それ以外は何も操作したくないとします。

TiDB 4.0 以降、すべての TiDB 移行ツールは共通のフィルター構文を共有してサブセットを定義しています。このドキュメントでは、テーブル フィルタ機能の使用方法について説明します。

## 使用法 {#usage}

### CLI {#cli}

複数の`-f`または`--filter`コマンド ライン パラメーターを使用して、テーブル フィルターをツールに適用できます。各フィルターは`db.table`の形式で、各部分はワイルドカードにすることができます ( [次のセクション](#wildcards)で詳しく説明します)。以下に使用例を示します。

<CustomContent platform="tidb">

-   [BR](/br/backup-and-restore-overview.md) :

    ```shell
    ./br backup full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    ```

    ```shell
    ./br restore full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    ```

</CustomContent>

-   [Dumpling](/dumpling-overview.md) :

    ```shell
    ./dumpling -f 'foo*.*' -f 'bar*.*' -P 3306 -o /tmp/data/
    ```

<CustomContent platform="tidb">

-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) :

    ```shell
    ./tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    ```

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview) :

    ```shell
    ./tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    ```

</CustomContent>

### TOML 構成ファイル {#toml-configuration-files}

TOML ファイルのテーブル フィルターは[文字列の配列](https://toml.io/en/v1.0.0-rc.1#section-15)として指定されます。以下に使用例を示します。

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

### プレーンなテーブル名 {#plain-table-names}

各テーブル フィルター ルールは、ドット ( `.` ) で区切られた「スキーマ パターン」と「テーブル パターン」で構成されます。完全修飾名がルールに一致するテーブルが受け入れられます。

```
db1.tbl1
db2.tbl2
db3.tbl3
```

プレーンな名前は、次のような有効な[識別子文字](/schema-object-names.md)のみで構成する必要があります。

-   数字 ( `0` ～ `9` )
-   文字 ( `a` ～ `z` 、 `A` ～ `Z` )
-   `$`
-   `_`
-   非 ASCII 文字 (U+0080 から U+10FFFF)

他のすべての ASCII 文字は予約されています。次のセクションで説明するように、一部の句読点には特別な意味があります。

### ワイルドカード {#wildcards}

名前の各部分は、 [fnmatch(3)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_13)で説明されているワイルドカード記号にすることができます。

-   `*` — 0 個以上の文字に一致
-   `?` — 1 文字に一致
-   `[a-z]` — &quot;a&quot; と &quot;z&quot; の間の 1 文字に一致します。
-   `[!a-z]` — &quot;a&quot; から &quot;z&quot; を除く 1 文字に一致します。

```
db[0-9].tbl[0-9a-f][0-9a-f]
data.*
*.backup_*
```

ここでの「文字」は、次のような Unicode コード ポイントを意味します。

-   U+00E9 (é) は 1 文字です。
-   U+0065 U+0301 (é) は 2 文字です。
-   U+1F926 U+1F3FF U+200D U+2640 U+FE0F (🤦🏿‍♀️)は5文字です。

### ファイルのインポート {#file-import}

ファイルをフィルタ ルールとしてインポートするには、ルールの先頭に`@`を含めてファイル名を指定します。テーブル フィルター パーサーは、インポートされたファイルの各行を追加のフィルター ルールとして扱います。

たとえば、ファイル`config/filter.txt`に次の内容があるとします。

```
employees.*
*.WorkOrder
```

次の 2 つの呼び出しは同等です。

```bash
./dumpling -f '@config/filter.txt'
./dumpling -f 'employees.*' -f '*.WorkOrder'
```

フィルター ファイルは、別のファイルをさらにインポートすることはできません。

### コメントと空行 {#comments-and-blank-lines}

フィルター ファイル内では、すべての行の先頭と末尾の空白が削除されます。また、空行（空文字列）は無視されます。

先頭の`#`コメントを示し、無視されます。行頭にない`#`は、構文エラーと見なされます。

```
# this line is a comment
db.table   # but this part is not comment and may cause error
```

### 除外 {#exclusion}

ルールの先頭にある`!`テーブルを処理対象から除外するために使用された後のパターンを意味します。これにより、フィルタが効果的にブロック リストに変わります。

```
*.*
#^ note: must add the *.* to include all tables first
!*.Password
!employees.salaries
```

### エスケープ文字 {#escape-character}

特殊文字を識別子文字に変えるには、その前にバックスラッシュ`\`を付けます。

```
db\.with\.dots.*
```

簡素化と将来の互換性のために、次のシーケンスは禁止されています。

-   空白をトリミングした後の行末の`\` (末尾の文字どおりの空白に一致させるには`[ ]`を使用)。
-   `\`の後に任意の ASCII 英数字 ( `[0-9a-zA-Z]` ) が続きます。特に、 `\0` 、 `\r` 、 `\n` 、 `\t`などの C ライクなエスケープ シーケンスは、現在のところ意味がありません。

### 引用識別子 {#quoted-identifier}

`\`の他に、特殊文字も`"`または`` ` ``を使用して引用することで抑制できます。

```
"db.with.dots"."tbl\1"
`db.with.dots`.`tbl\2`
```

引用符は、それ自体を 2 倍にすることにより、識別子内に含めることができます。

```
"foo""bar".`foo``bar`
# equivalent to:
foo\"bar.foo\`bar
```

引用符で囲まれた識別子は、複数行にまたがることはできません。

識別子を部分的に引用することは無効です:

```
"this is "invalid*.*
```

### 正規表現 {#regular-expression}

非常に複雑なルールが必要な場合は、各パターンを`/`で区切られた正規表現として記述できます。

```
/^db\d{2,}$/./^tbl\d{2,}$/
```

これらの正規表現は[方言を行く](https://pkg.go.dev/regexp/syntax?tab=doc)を使用します。正規表現に一致する部分文字列が識別子に含まれている場合、パターンは一致します。たとえば、 `/b/` `db01`に一致します。

> **ノート：**
>
> 正規表現のすべての`/` `[…]`内を含めて`\/`としてエスケープする必要があります。エスケープされていない`/` `\Q…\E`の間に配置することはできません。

## 複数のルール {#multiple-rules}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> このセクションはTiDB Cloudには適用されません。現在、 TiDB Cloud は1 つのテーブル フィルター ルールのみをサポートしています。

</CustomContent>

テーブル名がフィルタ リスト内のどのルールにも一致しない場合、デフォルトの動作では、そのような一致しないテーブルは無視されます。

ブロック リストを作成するには、明示的な`*.*`最初のルールとして使用する必要があります。そうしないと、すべてのテーブルが除外されます。

```bash
# every table will be filtered out
./dumpling -f '!*.Password'

# only the "Password" table is filtered out, the rest are included.
./dumpling -f '*.*' -f '!*.Password'
```

フィルタ リストでは、テーブル名が複数のパターンに一致する場合、最後の一致が結果を決定します。例えば：

```
# rule 1
employees.*
# rule 2
!*.dep*
# rule 3
*.departments
```

フィルタリングされた結果は次のとおりです。

| テーブル名              | ルール 1 | ルール 2 | ルール 3 | 結果            |
| ------------------ | ----- | ----- | ----- | ------------- |
| 無関係なテーブル           |       |       |       | デフォルト (拒否)    |
| 従業員.従業員            | ✓     |       |       | ルール 1 (受け入れる) |
| employees.dept_emp | ✓     | ✓     |       | ルール 2 (拒否)    |
| 従業員.部門             | ✓     | ✓     | ✓     | ルール 3 (受け入れる) |
| 他の部門               |       | ✓     | ✓     | ルール 3 (受け入れる) |

> **ノート：**
>
> TiDB ツールでは、システム スキーマは常にデフォルト設定で除外されます。システム スキーマは次のとおりです。
>
> -   `INFORMATION_SCHEMA`
> -   `PERFORMANCE_SCHEMA`
> -   `METRICS_SCHEMA`
> -   `INSPECTION_SCHEMA`
> -   `mysql`
> -   `sys`
