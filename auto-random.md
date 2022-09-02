---
title: AUTO_RANDOM
summary: Learn the AUTO_RANDOM attribute.
---

# AUTO_RANDOM v3.1.0<span class="version-mark">の新機能</span> {#auto-random-span-class-version-mark-new-in-v3-1-0-span}

> **ノート：**
>
> `AUTO_RANDOM`は v4.0.3 以降で一般提供されています。

## ユーザーシナリオ {#user-scenario}

TiDB にデータを集中的に書き込み、TiDB に自動インクリメント整数型の主キーを持つテーブルがある場合、ホットスポットの問題が発生する可能性があります。ホットスポットの問題を解決するには、 `AUTO_RANDOM`属性を使用できます。

<CustomContent platform="tidb">

詳細については、 [高度な同時書き込みのベスト プラクティス](/best-practices/high-concurrency-best-practices.md#complex-hotspot-problems)を参照してください。

</CustomContent>

例として、次の作成済みテーブルを取り上げます。

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_INCREMENT, b varchar(255))
```

この`t`のテーブルで、次のように主キーの値を指定しない`INSERT`のステートメントを大量に実行します。

{{< copyable "" >}}

```sql
INSERT INTO t(b) VALUES ('a'), ('b'), ('c')
```

上記のステートメントでは、主キー (列`a` ) の値が指定されていないため、TiDB は連続自動インクリメント行の値を行 ID として使用します。これにより、単一の TiKV ノードで書き込みホットスポットが発生し、パフォーマンスに影響を与える可能性があります。このような書き込みホットスポットを回避するには、テーブルを作成するときに、列`a`に`AUTO_INCREMENT`属性ではなく`AUTO_RANDOM`属性を指定できます。次の例を参照してください。

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM, b varchar(255))
```

また

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint AUTO_RANDOM, b varchar(255), PRIMARY KEY (a))
```

次に、 `INSERT INTO t(b) VALUES...`などの`INSERT`ステートメントを実行します。結果は次のようになります。

-   暗黙的な値の割り当て: `INSERT`ステートメントで整数の主キー列 (列`a` ) の値が指定されていないか、値が`NULL`として指定されていない場合、TiDB はこの列に値を自動的に割り当てます。これらの値は必ずしも自動インクリメントまたは連続ではありませんが、一意であるため、連続する行 ID によって引き起こされるホットスポットの問題を回避できます。
-   明示的な値の挿入: `INSERT`ステートメントが整数の主キー列の値を明示的に指定する場合、TiDB はこれらの値を保存します。これは`AUTO_INCREMENT`属性と同様に機能します。 `@@sql_mode`システム変数に`NO_AUTO_VALUE_ON_ZERO`を設定しない場合、整数の主キー列の値を`0`として明示的に指定したとしても、TiDB は自動的にこの列に値を割り当てることに注意してください。

> **ノート：**
>
> v4.0.3 以降、値を明示的に挿入する場合は、システム変数`@@allow_auto_random_explicit_insert`の値を`1` (デフォルトでは`0` ) に設定します。この明示的な挿入はデフォルトではサポートされておらず、その理由は[制限](#restrictions)セクションに記載されています。

TiDB は、次の方法で値を自動的に割り当てます。

バイナリ (つまり、シャード ビット) の行値の上位 5 桁 (符号ビットを無視) は、現在のトランザクションの開始時間によって決定されます。残りの桁には、自動インクリメント順で値が割り当てられます。

異なる数のシャード ビットを使用するには、括弧のペアを`AUTO_RANDOM`に追加し、括弧内に目的のシャード ビット数を指定します。次の例を参照してください。

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM(3), b varchar(255))
```

上記の`CREATE TABLE`のステートメントでは、 `3`のシャード ビットが指定されています。シャード ビット数の範囲は`[1, 16)`です。

テーブルを作成したら、 `SHOW WARNINGS`ステートメントを使用して、現在のテーブルでサポートされている暗黙的な割り当ての最大数を確認します。

{{< copyable "" >}}

```sql
SHOW WARNINGS
```

```sql
+-------+------+----------------------------------------------------------+
| Level | Code | Message                                                  |
+-------+------+----------------------------------------------------------+
| Note  | 1105 | Available implicit allocation times: 1152921504606846976 |
+-------+------+----------------------------------------------------------+
```

> **ノート：**
>
> v4.0.3 以降、 `AUTO_RANDOM`列の型は`BIGINT`のみです。これは、暗黙的な割り当ての最大数を確保するためです。

さらに、 `AUTO_RANDOM`属性を持つテーブルのシャード ビット数を表示するには、 `information_schema.tables`システム テーブルの`TIDB_ROW_ID_SHARDING_INFO`列で`PK_AUTO_RANDOM_BITS=x`モードの値を確認できます。 `x`はシャード ビットの数です。

`AUTO_RANDOM`列に割り当てられた値は`last_insert_id()`に影響します。 `SELECT last_insert_id ()`を使用して、TiDB が最後に暗黙的に割り当てた ID を取得できます。例えば：

{{< copyable "" >}}

```sql
INSERT INTO t (b) VALUES ("b")
SELECT * FROM t;
SELECT last_insert_id()
```

次の結果が表示される場合があります。

```
+------------+---+
| a          | b |
+------------+---+
| 1073741825 | b |
+------------+---+
+------------------+
| last_insert_id() |
+------------------+
| 1073741825       |
+------------------+
```

## 互換性 {#compatibility}

TiDB は、バージョン コメント構文の解析をサポートしています。次の例を参照してください。

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] auto_random */)
```

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM)
```

上記の 2 つのステートメントは同じ意味です。

`SHOW CREATE TABLE`の結果では、 `AUTO_RANDOM`属性がコメントアウトされています。このコメントには、属性識別子 ( `/*T![auto_rand] auto_random */`など) が含まれます。ここで、 `auto_rand`は`AUTO_RANDOM`属性を表します。この識別子に対応する機能を実装する TiDB のバージョンのみが、SQL ステートメントのフラグメントを適切に解析できます。

この属性は、前方互換性、つまりダウングレード互換性をサポートします。この機能を実装していない以前のバージョンの TiDB は、テーブルの`AUTO_RANDOM`属性 (上記のコメント付き) を無視し、属性を持つテーブルを使用することもできます。

## 制限 {#restrictions}

`AUTO_RANDOM`を使用する場合は、次の制限に注意してください。

-   この属性は、 `bigint`型の主キー列**のみ**に指定します。そうしないと、エラーが発生します。また、主キーの属性が`NONCLUSTERED`の場合、整数の主キーでも`AUTO_RANDOM`はサポートされません。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   この属性の追加または削除を含め、 `ALTER TABLE`を使用して`AUTO_RANDOM`属性を変更することはできません。
-   最大値が列タイプの最大値に近い場合、 `ALTER TABLE`を使用して`AUTO_INCREMENT`から`AUTO_RANDOM`に変更することはできません。
-   `AUTO_RANDOM`属性で指定された主キー列の列型は変更できません。
-   同じ列に`AUTO_RANDOM`と`AUTO_INCREMENT`を同時に指定することはできません。
-   同じ列に`AUTO_RANDOM`と`DEFAULT` (列のデフォルト値) を同時に指定することはできません。
-   列で`AUTO_RANDOM`を使用すると、自動生成された値が非常に大きくなる可能性があるため、列属性を`AUTO_INCREMENT`に戻すのは困難です。
-   データを挿入するときに、 `AUTO_RANDOM`属性を使用して列の値を明示的に指定することは**お**勧めしません。そうしないと、このテーブルに自動的に割り当てられる数値が事前に使い果たされる可能性があります。
