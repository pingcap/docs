---
title: Time Zone Support
summary: TiDB のタイムゾーン設定は、セッションレベルまたはグローバルレベルで設定できる time_zone` システム変数によって制御されます。 `TIMESTAMP` データ型の表示値はタイムゾーン設定の影響を受けますが、`DATETIME`、`DATE`、および `TIME` データ型は影響を受けません。データ移行では、プライマリデータベースとセカンダリデータベースのタイムゾーン設定が一致しているかどうかに特に注意する必要があります。
---

# タイムゾーンのサポート {#time-zone-support}

TiDB のタイムゾーンは、 [`time_zone`](/system-variables.md#time_zone)システム変数によって決定されます。セッションレベルまたはグローバルレベルで設定できます。 `time_zone`のデフォルト値は`SYSTEM`です。 `SYSTEM`に対応する実際のタイムゾーンは、TiDB クラスターのブートストラップが初期化されるときに構成されます。詳細なロジックは次のとおりです。

1.  TiDB は`TZ`環境変数の使用を優先します。
2.  `TZ`環境変数が失敗した場合、TiDB は`/etc/localtime`のソフト リンクからタイム ゾーンを読み取ります。
3.  上記の両方の方法が失敗した場合、TiDB はシステム タイム ゾーンとして`UTC`使用します。

## タイムゾーン設定をビュー {#view-time-zone-settings}

グローバル、クライアント固有、およびシステムのタイムゾーンの現在の値を表示するには、次のステートメントを実行します。

```sql
SELECT @@global.time_zone, @@session.time_zone, @@global.system_time_zone;
```

## タイムゾーンを設定する {#set-the-time-zone}

TiDB では、 `time_zone`システム変数の値は次のいずれかの形式で設定できます。

-   `SYSTEM` (デフォルト値) は、タイム ゾーンがシステムのタイム ゾーンと同じであることを示します。
-   UTC オフセット ( `'+10:00'`や`'-6:00'`など)。
-   `'Europe/Helsinki'` 、 `'US/Eastern'` 、 `'MET'`などの名前付きタイムゾーン。

ニーズに応じて、次のように TiDB のタイムゾーンをグローバル レベルまたはセッション レベルで設定できます。

-   TiDB のタイムゾーンをグローバル レベルで設定します。

    ```sql
    SET GLOBAL time_zone = ${time-zone-value};
    ```

    たとえば、グローバル タイム ゾーンを UTC に設定します。

    ```sql
    SET GLOBAL time_zone = 'UTC';
    ```

-   セッション レベルで TiDB のタイム ゾーンを設定します。

    ```sql
    SET time_zone = ${time-zone-value};
    ```

    たとえば、現在のセッションのタイムゾーンを US/Pacific に設定します。

    ```sql
    SET time_zone = 'US/Pacific';
    ```

## タイムゾーン設定の影響を受ける関数とデータ型 {#functions-and-data-types-affected-by-time-zone-settings}

現在のセッションのタイム ゾーン設定は、 [`NOW()`](/functions-and-operators/date-and-time-functions.md)および`CURTIME()`関数によって返される値など、ゾーンに依存する時間値の表示と解釈に影響します。タイム ゾーンを変換するには、 `CONVERT_TZ()`関数を使用します。UTC に基づくタイムスタンプを取得するには、 `UTC_TIMESTAMP()`関数を使用します。これにより、タイム ゾーン関連の問題を回避できます。

TiDB では、 `TIMESTAMP`データ型の表示値はタイムゾーン設定の影響を受けます。これは、 `TIMESTAMP`データ型がリテラル値とタイムゾーン情報を使用するためです。 `DATETIME` 、 `DATE` 、 `TIME`などの他のデータ型にはタイムゾーン情報がないため、それらの値はタイムゾーンの変更の影響を受けません。

例えば：

```sql
create table t (ts timestamp, dt datetime);
```

    Query OK, 0 rows affected (0.02 sec)

```sql
set @@time_zone = 'UTC';
```

    Query OK, 0 rows affected (0.00 sec)

```sql
insert into t values ('2017-09-30 11:11:11', '2017-09-30 11:11:11');
```

    Query OK, 1 row affected (0.00 sec)

```sql
set @@time_zone = '+8:00';
```

    Query OK, 0 rows affected (0.00 sec)

```sql
select * from t;
```

    +---------------------|---------------------+
    | ts                  | dt                  |
    +---------------------|---------------------+
    | 2017-09-30 19:11:11 | 2017-09-30 11:11:11 |
    +---------------------|---------------------+
    1 row in set (0.00 sec)

この例では、タイムゾーンの値をどのように調整しても、 `DATETIME`データ型の値は影響を受けません。ただし、 `TIMESTAMP`データ型の表示値はタイムゾーンの変更を反映しています。実際、データベースに保存されている`TIMESTAMP`値は変更されませんが、タイムゾーンの設定に応じて表示が異なります。

## タイムゾーン設定に関する重要な考慮事項 {#important-considerations-for-time-zone-settings}

-   `TIMESTAMP`と`DATETIME`の値の変換時にはタイムゾーンが関係し、これは現在のセッションの`time_zone`に基づいて処理されます。
-   データ移行では、プライマリ データベースとセカンダリ データベースのタイム ゾーン設定が一致しているかどうかに特に注意する必要があります。
-   正確なタイムスタンプを取得するには、ネットワーク タイム プロトコル (NTP) または高精度時間プロトコル (PTP) サービスを使用して信頼性の高いクロックを構成することを強くお勧めします。NTP サービスを確認する方法については、 [NTPサービスを確認してインストールする](/check-before-deployment.md#check-and-install-the-ntp-service)参照してください。
-   夏時間を採用しているタイムゾーンを使用すると、特にそれらのタイムスタンプを使用して計算を実行する場合に、タイムスタンプがあいまいになったり、タイムスタンプが存在しなくなったりする可能性があることに注意してください。
-   MySQL は[`mysql_tzinfo_to_sql`](https://dev.mysql.com/doc/refman/8.4/en/mysql-tzinfo-to-sql.html)使用して、オペレーティング システムのタイム ゾーン データベースを`mysql`データベースのテーブルに変換します。一方、TiDB は、オペレーティング システムのタイム ゾーン データベースからタイム ゾーン データ ファイルを直接読み取り、Go プログラミング言語に組み込まれたタイム ゾーン処理機能を活用します。

## 参照 {#see-also}

-   [日付と時刻のデータ型](/data-type-date-and-time.md)
-   [データと時間関数](/functions-and-operators/date-and-time-functions.md)
