---
title: AUTO_RANDOM
summary: Learn the AUTO_RANDOM attribute.
---

# AUTO_RANDOMv3.1.0<span class="version-mark">の新機能</span> {#auto-random-span-class-version-mark-new-in-v3-1-0-span}

> **ノート：**
>
> `AUTO_RANDOM`は、v4.0.3以降安定しているとマークされています。

## ユーザーシナリオ {#user-scenario}

データをTiDBに集中的に書き込む場合、TiDBに自動インクリメント整数型の主キーを持つテーブルがあると、ホットスポットの問題が発生する可能性があります。ホットスポットの問題を解決するには、 `AUTO_RANDOM`属性を使用できます。

<CustomContent platform="tidb">

詳細については、 [非常に同時の書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md#complex-hotspot-problems)を参照してください。

</CustomContent>

例として、次の作成されたテーブルを取り上げます。

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_INCREMENT, b varchar(255))
```

この`t`のテーブルで、次のように主キーの値を指定しない`INSERT`のステートメントを多数実行します。

{{< copyable "" >}}

```sql
INSERT INTO t(b) VALUES ('a'), ('b'), ('c')
```

上記のステートメントでは、主キー（列`a` ）の値が指定されていないため、TiDBは行IDとして連続自動インクリメント行値を使用します。これにより、単一のTiKVノードで書き込みホットスポットが発生し、パフォーマンスに影響を与える可能性があります。このような書き込みホットスポットを回避するために、テーブルの作成時に列`a`の`AUTO_INCREMENT`属性ではなく`AUTO_RANDOM`属性を指定できます。次の例を参照してください。

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM, b varchar(255))
```

また

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint AUTO_RANDOM, b varchar(255), PRIMARY KEY (a))
```

次に、 `INSERT INTO t(b) VALUES...`などの`INSERT`ステートメントを実行します。これで、結果は次のようになります。

-   値の暗黙的な割り当て： `INSERT`ステートメントが整数主キー列（列`a` ）の値を指定しない場合、または値を`NULL`として指定しない場合、TiDBはこの列に値を自動的に割り当てます。これらの値は、必ずしも自動インクリメントまたは連続である必要はありませんが、一意であるため、連続行IDによって引き起こされるホットスポットの問題を回避できます。
-   値の明示的な挿入： `INSERT`ステートメントが整数主キー列の値を明示的に指定する場合、TiDBはこれらの値を保存します。これは、 `AUTO_INCREMENT`属性と同様に機能します。 `@@sql_mode`システム変数に`NO_AUTO_VALUE_ON_ZERO`を設定しない場合、整数主キー列の値を`0`として明示的に指定しても、TiDBはこの列に値を自動的に割り当てることに注意してください。

> **ノート：**
>
> v4.0.3以降、値を明示的に挿入する場合は、 `@@allow_auto_random_explicit_insert`システム変数の値を`1` （デフォルトでは`0` ）に設定します。この明示的な挿入はデフォルトではサポートされておらず、その理由は[制限](#restrictions)セクションに記載されています。

TiDBは、次の方法で値を自動的に割り当てます。

バイナリ（つまり、シャードビット）の行値の上位5桁（符号ビットを無視）は、現在のトランザクションの開始時刻によって決定されます。残りの桁には、自動インクリメント順に値が割り当てられます。

異なる数のシャードビットを使用するには、 `AUTO_RANDOM`に括弧のペアを追加し、括弧内に必要な数のシャードビットを指定します。次の例を参照してください。

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM(3), b varchar(255))
```

上記の`CREATE TABLE`のステートメントでは、 `3`のシャードビットが指定されています。シャードビット数の範囲は`[1, 16)`です。

テーブルを作成した後、 `SHOW WARNINGS`ステートメントを使用して、現在のテーブルでサポートされている暗黙的な割り当ての最大数を確認します。

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
> v4.0.3以降、 `AUTO_RANDOM`列のタイプは`BIGINT`のみになります。これは、暗黙的な割り当ての最大数を確保するためです。

さらに、 `AUTO_RANDOM`属性を持つテーブルのシャードビット番号を表示するには、 `information_schema.tables`システムテーブルの`TIDB_ROW_ID_SHARDING_INFO`列に`PK_AUTO_RANDOM_BITS=x`モードの値を表示できます。 `x`はシャードビットの数です。

`AUTO_RANDOM`列に割り当てられた値は`last_insert_id()`に影響します。 `SELECT last_insert_id ()`を使用して、TiDBが最後に暗黙的に割り当てるIDを取得できます。例えば：

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

TiDBは、バージョンコメント構文の解析をサポートしています。次の例を参照してください。

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] auto_random */)
```

{{< copyable "" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM)
```

上記の2つのステートメントは同じ意味です。

`SHOW CREATE TABLE`の結果では、 `AUTO_RANDOM`属性がコメント化されています。このコメントには、属性識別子（たとえば、 `/*T![auto_rand] auto_random */` ）が含まれます。ここで、 `auto_rand`は`AUTO_RANDOM`属性を表します。この識別子に対応する機能を実装するバージョンのTiDBのみが、SQLステートメントフラグメントを適切に解析できます。

この属性は、上位互換性、つまりダウングレード互換性をサポートします。この機能を実装していない以前のバージョンのTiDBは、テーブルの`AUTO_RANDOM`属性（上記のコメント付き）を無視し、その属性でテーブルを使用することもできます。

## 制限 {#restrictions}

`AUTO_RANDOM`を使用する場合は、次の制限に注意してください。

-   この属性は、整数型の主キー列に**のみ**指定してください。そうしないと、エラーが発生する可能性があります。また、主キーの属性が`NONCLUSTERED`の場合、整数の主キーでも`AUTO_RANDOM`はサポートされません。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化されたインデックス](/clustered-indexes.md)を参照してください。
-   `ALTER TABLE`を使用して、この属性の追加または削除を含め、 `AUTO_RANDOM`属性を変更することはできません。
-   `AUTO_RANDOM`属性で指定された主キー列の列タイプは変更できません。
-   同じ列に`AUTO_RANDOM`と`AUTO_INCREMENT`を同時に指定することはできません。
-   同じ列に`AUTO_RANDOM`と`DEFAULT` （列のデフォルト値）を同時に指定することはできません。
-   データを挿入するときに、 `AUTO_RANDOM`属性を持つ列の値を明示的に指定することは**お**勧めしません。そうしないと、このテーブルに自動的に割り当てられる数値が事前に使い果たされる可能性があります。
