---
title: AUTO_RANDOM
summary: Learn the AUTO_RANDOM attribute.
---

# AUTO_RANDOM <span class="version-mark">v3.1.0 の新機能</span> {#auto-random-span-class-version-mark-new-in-v3-1-0-span}

## ユーザーシナリオ {#user-scenario}

`AUTO_RANDOM`の値はランダムで一意であるため、TiDB が連続した ID を割り当てることによって発生する単一storageノードでの書き込みホットスポットを回避するために、 [`AUTO_INCREMENT`](/auto-increment.md)の代わりに`AUTO_RANDOM`よく使用されます。現在の`AUTO_INCREMENT`列が主キーで、タイプが`BIGINT`の場合、 `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);`ステートメントを実行して`AUTO_INCREMENT`から`AUTO_RANDOM`に切り替えることができます。

<CustomContent platform="tidb">

TiDB で同時書き込み負荷の高いワークロードを処理する方法の詳細については、 [高度な同時書き込みのベスト プラクティス](/best-practices/high-concurrency-best-practices.md)を参照してください。

</CustomContent>

## 基本概念 {#basic-concepts}

`AUTO_RANDOM`は、 `BIGINT`列に値を自動的に割り当てるために使用される列属性です。自動的に割り当てられる値は**ランダム**で<strong>一意</strong>です。

`AUTO_RANDOM`列のテーブルを作成するには、次のステートメントを使用できます。 `AUTO_RANDOM`列は主キーに含める必要があり、 `AUTO_RANDOM`列は主キーの最初の列です。

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a, b));
```

実行可能なコメントでキーワード`AUTO_RANDOM`をラップできます。詳細については、 [TiDB 固有のコメント構文](/comment-syntax.md#tidb-specific-comment-syntax)を参照してください。

```sql
CREATE TABLE t (a bigint /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255));
CREATE TABLE t (a BIGINT /*T![auto_rand] AUTO_RANDOM(6) */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT  /*T![auto_rand] AUTO_RANDOM(5, 54) */, b VARCHAR(255), PRIMARY KEY (a));
```

`INSERT`ステートメントを実行すると、次のようになります。

-   `AUTO_RANDOM`列の値を明示的に指定すると、そのままテーブルに挿入されます。
-   `AUTO_RANDOM`列の値を明示的に指定しない場合、TiDB はランダムな値を生成し、それをテーブルに挿入します。

```sql
tidb> CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
Query OK, 0 rows affected, 1 warning (0.01 sec)

tidb> INSERT INTO t(a, b) VALUES (1, 'string');
Query OK, 1 row affected (0.00 sec)

tidb> SELECT * FROM t;
+---+--------+
| a | b      |
+---+--------+
| 1 | string |
+---+--------+
1 row in set (0.01 sec)

tidb> INSERT INTO t(b) VALUES ('string2');
Query OK, 1 row affected (0.00 sec)

tidb> INSERT INTO t(b) VALUES ('string3');
Query OK, 1 row affected (0.00 sec)

tidb> SELECT * FROM t;
+---------------------+---------+
| a                   | b       |
+---------------------+---------+
|                   1 | string  |
| 1152921504606846978 | string2 |
| 4899916394579099651 | string3 |
+---------------------+---------+
3 rows in set (0.00 sec)
```

TiDB によって自動的に割り当てられる`AUTO_RANDOM(S, R)`列の値は、合計 64 ビットです。

-   `S`はシャード ビットの数です。値の範囲は`1`から`15`です。デフォルト値は`5`です。
-   `R`は自動割り当て範囲の全長です。値の範囲は`32`から`64`です。デフォルト値は`64`です。

`AUTO_RANDOM`値の構造は次のとおりです。

| 総ビット数 | 符号ビット   | 予約ビット      | シャードビット | 自動インクリメント ビット |
| ----- | ------- | ---------- | ------- | ------------- |
| 64ビット | 0/1 ビット | (64-R) ビット | S ビット   | (R-1-S) ビット   |

-   符号ビットの長さは、 `UNSIGNED`属性の存在によって決まります。 `UNSIGNED`属性がある場合、長さは`0`です。それ以外の場合、長さは`1`です。
-   予約ビットの長さは`64-R`です。予約ビットは常に`0`です。
-   シャード ビットの内容は、現在のトランザクションの開始時刻のハッシュ値を計算することによって取得されます。別の長さのシャード ビット (10 など) を使用するには、テーブルの作成時に`AUTO_RANDOM(10)`を指定します。
-   自動インクリメント ビットの値は、storageエンジンに格納され、順番に割り当てられます。新しい値が割り当てられるたびに、値は 1 ずつインクリメントされます。自動インクリメント ビットは、 `AUTO_RANDOM`の値がグローバルに一意であることを保証します。自動インクリメント ビットが使い果たされると、値が再度割り当てられるときにエラー`Failed to read auto-increment value from storage engine`が報告されます。

> **ノート：**
>
> シャード ビットの選択 ( `S` ):
>
> -   合計 64 の使用可能なビットがあるため、シャード ビット長は自動インクリメント ビット長に影響します。つまり、シャード ビットの長さが増加すると、自動インクリメント ビットの長さが減少し、逆もまた同様です。したがって、割り当てられた値のランダム性と使用可能なスペースのバランスを取る必要があります。
> -   ベスト プラクティスは、シャード ビットを`log(2, x)`に設定することです。ここで、 `x`はstorageエンジンの現在の数です。たとえば、TiDB クラスターに 16 個の TiKV ノードがある場合、シャード ビットを`log(2, 16)` 、つまり`4`に設定できます。すべてのリージョンが各 TiKV ノードに均等にスケジュールされた後、バルク書き込みの負荷を異なる TiKV ノードに均等に分散して、リソースの使用率を最大化できます。
>
> 範囲の選択 ( `R` ):
>
> -   通常、アプリケーションの数値型が完全な 64 ビット整数を表すことができない場合は、 `R`パラメータを設定する必要があります。
> -   たとえば、JSON 番号の範囲は`[-2^53+1, 2^53-1]`です。 TiDB は、この範囲外の整数を`AUTO_RANDOM(5)`の列に簡単に割り当てることができ、アプリケーションが列を読み取るときに予期しない動作を引き起こします。この場合、 `AUTO_RANDOM(5)` `AUTO_RANDOM(5, 54)`に置き換えることができ、TiDB は列に`9007199254740991` (2^53-1) より大きい整数を割り当てません。

`AUTO_RANDOM`列に暗黙的に割り当てられた値は`last_insert_id()`に影響します。 TiDB が最後に暗黙的に割り当てた ID を取得するには、 `SELECT last_insert_id ()`ステートメントを使用できます。

`AUTO_RANDOM`列のテーブルのシャード ビット数を表示するには、 `SHOW CREATE TABLE`ステートメントを実行できます。また、 `information_schema.tables`システム テーブルの`TIDB_ROW_ID_SHARDING_INFO`列で`PK_AUTO_RANDOM_BITS=x`モードの値を確認できます。 `x`はシャード ビットの数です。

## 制限 {#restrictions}

`AUTO_RANDOM`を使用する場合は、次の制限に注意してください。

-   値を明示的に挿入するには、システム変数`@@allow_auto_random_explicit_insert`の値を`1` (デフォルトでは`0` ) に設定する必要があります。データを挿入するときに、属性`AUTO_RANDOM`を持つ列の値を明示的に指定することは**お**勧めしません。そうしないと、このテーブルに自動的に割り当てられる数値が事前に使い果たされる可能性があります。
-   この属性は、 `BIGINT`型として主キー列**のみ**に指定します。そうしないと、エラーが発生します。また、主キーの属性が`NONCLUSTERED`の場合、整数の主キーでも`AUTO_RANDOM`サポートされません。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   この属性の追加または削除を含め、 `ALTER TABLE`を使用して`AUTO_RANDOM`属性を変更することはできません。
-   最大値が列タイプの最大値に近い場合、 `ALTER TABLE`使用して`AUTO_INCREMENT`から`AUTO_RANDOM`に変更することはできません。
-   `AUTO_RANDOM`属性で指定された主キー列の列型は変更できません。
-   同じ列に`AUTO_RANDOM`と`AUTO_INCREMENT`同時に指定することはできません。
-   同じ列に`AUTO_RANDOM`と`DEFAULT` (列のデフォルト値) を同時に指定することはできません。
-   列で`AUTO_RANDOM`を使用すると、自動生成された値が非常に大きくなる可能性があるため、列属性を`AUTO_INCREMENT`に戻すのは困難です。
