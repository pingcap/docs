---
title: Time Zone Support
summary: Learn how to set the time zone and its format.
---

# タイムゾーンのサポート {#time-zone-support}

TiDB のタイム ゾーンは、グローバル`time_zone`システム変数とセッション`time_zone`システム変数によって決定されます。デフォルト値の`time_zone`は`SYSTEM`です。 `System`に対応する実際のタイム ゾーンは、TiDB クラスターのブートストラップが初期化されるときに構成されます。詳細なロジックは次のとおりです。

-   `TZ`環境変数の使用を優先します。
-   `TZ`環境変数が失敗した場合は、 `/etc/localtime`の実際のソフト リンク アドレスからタイム ゾーンを抽出します。
-   上記の方法が両方とも失敗した場合は、システムのタイム ゾーンとして`UTC`を使用します。

次のステートメントを使用して、実行時にグローバルサーバー`time_zone`値を設定できます。

{{< copyable "" >}}

```sql
SET GLOBAL time_zone = timezone;
```

各クライアントには、セッション`time_zone`変数によって指定される独自のタイム ゾーン設定があります。最初に、セッション変数はグローバル`time_zone`変数から値を取得しますが、クライアントは次のステートメントで独自のタイム ゾーンを変更できます。

{{< copyable "" >}}

```sql
SET time_zone = timezone;
```

次のステートメントを使用して、グローバル、クライアント固有、およびシステムのタイム ゾーンの現在の値を表示できます。

{{< copyable "" >}}

```sql
SELECT @@global.time_zone, @@session.time_zone, @@global.system_time_zone;
```

`time_zone`の値の形式を設定するには:

-   値「SYSTEM」は、タイムゾーンがシステムのタイムゾーンと同じであることを示します。
-   値は、「+10:00」や「-6:00」など、UTC からのオフセットを示す文字列として指定できます。
-   値は、&#39;Europe/Helsinki&#39;、&#39;US/Eastern&#39;、または &#39;MET&#39; などの名前付きタイム ゾーンとして指定できます。

現在のセッションのタイム ゾーン設定は、ゾーンに依存する時間値の表示とstorageに影響します。これには、 `NOW()`や`CURTIME()`などの関数によって表示される値が含まれます。

> **ノート：**
>
> Timestamp データ型の値のみがタイム ゾーンの影響を受けます。これは、Timestamp データ型がリテラル値 + タイム ゾーン情報を使用するためです。 Datetime/Date/Time などのその他のデータ型にはタイム ゾーン情報がないため、それらの値はタイム ゾーンの変更の影響を受けません。

{{< copyable "" >}}

```sql
create table t (ts timestamp, dt datetime);
```

```
Query OK, 0 rows affected (0.02 sec)
```

{{< copyable "" >}}

```sql
set @@time_zone = 'UTC';
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "" >}}

```sql
insert into t values ('2017-09-30 11:11:11', '2017-09-30 11:11:11');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "" >}}

```sql
set @@time_zone = '+8:00';
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "" >}}

```sql
select * from t;
```

```
+---------------------|---------------------+
| ts                  | dt                  |
+---------------------|---------------------+
| 2017-09-30 19:11:11 | 2017-09-30 11:11:11 |
+---------------------|---------------------+
1 row in set (0.00 sec)
```

この例では、タイム ゾーンの値をどのように調整しても、Datetime データ型の値は影響を受けません。ただし、タイム ゾーン情報が変更されると、タイムスタンプ データ型の表示値が変更されます。実際、storageに保存されている値は変更されません。異なるタイム ゾーン設定に従って表示が異なるだけです。

> **ノート：**
>
> -   セッションの現在の`time_zone`に基づいて処理される Timestamp と Datetime の値の変換中にタイム ゾーンが関係します。
> -   データ移行では、プライマリ データベースとセカンダリ データベースのタイム ゾーン設定に特に注意する必要があります。
