---
title: DM Safe Mode
summary: Introduces the DM safe mode, its purpose, working principles and how to use it.
---

# DMセーフモード {#dm-safe-mode}

セーフ モードは、DM が増分レプリケーションを実行するための特別な操作モードです。セーフ モードでは、DM 増分レプリケーションコンポーネントがbinlogイベントをレプリケートするときに、DM は`INSERT`と`UPDATE`のすべてのステートメントをダウンストリームで実行する前に強制的に書き換えます。

セーフ モードでは、べき等性が保証された状態で、1 つのbinlogイベントをダウンストリームに繰り返しレプリケートできます。したがって、増分レプリケーションは*安全*です。

チェックポイントからデータ レプリケーション タスクを再開した後、DM はいくつかのbinlogイベントを繰り返しレプリケートする場合があり、これにより次の問題が発生します。

-   増分レプリケーション中、DML を実行する操作とチェックポイントを書き込む操作は同時ではありません。チェックポイントの書き込み操作と下流のデータベースへのデータの書き込み操作は、アトミックではありません。したがって、 **DM が異常終了した場合、チェックポイントは終了ポイントの前の復元ポイントのみを記録する可能性があります**。
-   DM がレプリケーション タスクを再開し、チェックポイントからインクリメンタル レプリケーションを再開する場合、チェックポイントと終了ポイントの間の一部のデータは、異常終了の前にすでに処理されている可能性があります。これにより、**一部の SQL ステートメントが繰り返し実行されます**。
-   `INSERT`ステートメントが繰り返し実行されると、主キーまたは一意のインデックスで競合が発生し、レプリケーションの失敗につながる可能性があります。 `UPDATE`ステートメントが繰り返し実行されると、フィルター条件は以前に更新されたレコードを見つけることができない場合があります。

セーフ モードでは、DM は SQL ステートメントを書き換えて、前述の問題を解決できます。

## 動作原理 {#working-principle}

セーフ モードでは、DM は SQL ステートメントを書き換えることでbinlogイベントのべき等性を保証します。具体的には、次の SQL ステートメントが書き直されます。

-   `INSERT`ステートメントは`REPLACE`ステートメントに書き換えられます。
-   主キーの値または更新された行の一意のインデックスを取得するために、 `UPDATE`ステートメントが分析されます。 `UPDATE`ステートメントは、次の 2 つの手順で`DELETE` + `REPLACE`ステートメントに書き換えられます。DM は、主キーまたは一意のインデックスを使用して古いレコードを削除し、 `REPLACE`ステートメントを使用して新しいレコードを挿入します。

`REPLACE`データを挿入するための MySQL 固有の構文です。 `REPLACE`を使用してデータを挿入し、新しいデータと既存のデータに主キーまたは一意の制約の競合がある場合、MySQL は競合するすべてのレコードを削除し、「強制挿入」と同等の挿入操作を実行します。詳細については、MySQL ドキュメントの[`REPLACE`ステートメント](https://dev.mysql.com/doc/refman/8.0/en/replace.html)参照してください。

`dummydb.dummytbl`テーブルに主キー`id`があるとします。このテーブルで次の SQL ステートメントを繰り返し実行します。

```sql
INSERT INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
UPDATE dummydb.dummytbl SET int_value = 888999 WHERE int_value = 999;   -- Suppose there is no other record with int_value = 999
UPDATE dummydb.dummytbl SET id = 999 WHERE id = 888;    -- Update the primary key
```

セーフ モードが有効な場合、前の SQL ステートメントがダウンストリームで再度実行されると、次のように書き換えられます。

```sql
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 123;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 888999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 888;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (999, 888888, 'abc888');
```

前のステートメントで、 `UPDATE` `DELETE` + `INSERT`ではなく`DELETE` + `REPLACE`に書き換えられます。ここで`INSERT`が使用されている場合、 `id = 999`で重複レコードを挿入すると、データベースは主キーの競合を報告します。これが、代わりに`REPLACE`が使用される理由です。新しいレコードが既存のレコードを置き換えます。

SQL ステートメントを書き換えることにより、DM は、重複する挿入または更新操作を実行するときに、新しい行データを使用して既存の行データを上書きします。これにより、挿入操作と更新操作が繰り返し実行されることが保証されます。

## セーフモードを有効にする {#enable-safe-mode}

自動または手動でセーフモードを有効にすることができます。このセクションでは、詳細な手順について説明します。

### 自動的に有効にする {#automatically-enable}

DM がチェックポイント (たとえば、DM ワーカーの再起動またはネットワークの再接続) から増分レプリケーション タスクを再開すると、DM は一定期間 (既定では 60 秒) セーフ モードを自動的に有効にします。

セーフ モードを有効にするかどうかは、チェックポイントの`safemode_exit_point`に関連しています。増分レプリケーション タスクが異常に一時停止すると、DM はメモリ内のすべての DML ステートメントをダウンストリームにレプリケートしようとし、DML ステートメントの中で最新のbinlog位置を`safemode_exit_point`として記録します。これは最後のチェックポイントに保存されます。

詳細なロジックは次のとおりです。

-   チェックポイントに`safemode_exit_point`が含まれている場合、増分レプリケーション タスクは異常に一時停止しています。 DM がタスクを再開すると、再開されるチェックポイントのbinlog位置 (**開始位置**) は`safemode_exit_point`より前になります。これは、開始位置と`safemode_exit_point`の間のbinlogイベントがダウンストリームで処理された可能性があることを表します。そのため、再開プロセス中に、一部のbinlogイベントが繰り返し実行される場合があります。したがって、セーフモードを有効にすると、これらのbinlogの位置を<strong>安全に</strong>することができます。 binlog の位置が`safemode_exit_point`を超えると、セーフ モードを手動で有効にしない限り、DM は自動的にセーフ モードを無効にします。

-   チェックポイントに`safemode_exit_point`含まれていない場合は、次の 2 つのケースがあります。

    1.  これは新しいタスクです。または、このタスクは予想どおり一時停止しています。
    2.  このタスクは異常に一時停止されますが、DM は`safemode_exit_point`記録に失敗するか、DM プロセスが異常終了します。

    2 番目のケースでは、DM は、チェックポイントの後のどのbinlogイベントがダウンストリームで実行されるかを知りません。繰り返し実行されるbinlogイベントによって問題が発生しないようにするために、DM は最初の 2 つのチェックポイント間隔で自動的にセーフ モードを有効にします。 2 つのチェックポイント間のデフォルトの間隔は 30 秒です。これは、通常の増分レプリケーション タスクが開始されると、セーフ モードが最初の 60 秒間 (2 * 30 秒) 適用されることを意味します。

    通常、増分レプリケーション タスクの開始時にセーフ モード期間を調整するためにチェックポイント間隔を変更することはお勧めしません。ただし、変更が必要な場合は、 [セーフモードを手動で有効にする](#manually-enable) (推奨) または syncer 構成の`checkpoint-flush-interval`項目を変更できます。

### 手動で有効にする {#manually-enable}

syncer 構成で`safe-mode`項目を設定して、レプリケーション プロセス全体でセーフ モードを有効にすることができます。 `safe-mode`は bool 型のパラメータで、デフォルトは`false`です。 `true`に設定すると、DM は増分レプリケーション プロセス全体でセーフ モードを有効にします。

以下は、セーフ モードを有効にしたタスク構成の例です。

```
syncers:                              # The running configurations of the sync processing unit.
  global:                            # Configuration name.
    # Other configuration items are not provided in this example.
    safe-mode: true                  # Enables safe mode for the whole incremental replication process.
    # Other configuration items are not provided in this example.
# ----------- Instance configuration -----------
mysql-instances:
  -
    source-id: "mysql-replica-01"
    # Other configuration items are not provided in this example.
    syncer-config-name: "global"            # Name of the syncers configuration.
```

## セーフモードの注意事項 {#notes-for-safe-mode}

安全上の理由から、レプリケーション プロセス全体でセーフ モードを有効にする場合は、次の点に注意してください。

-   **セーフ モードでの増分レプリケーションは、余分なオーバーヘッドを消費します。** `DELETE` + `REPLACE`操作を頻繁に行うと、主キーまたは一意のインデックスが頻繁に変更され、 `UPDATE`ステートメントのみを実行する場合よりもパフォーマンスのオーバーヘッドが大きくなります。
-   **セーフ モードでは、レコードが同じ主キーに強制的に置き換えられるため、ダウンストリームでデータが失われる可能性があります。**アップストリームからダウンストリームにシャードをマージして移行する場合、構成が正しくないと、多数の主キーまたは一意のキーの競合が発生する可能性があります。この状況でセーフ モードが有効になっている場合、ダウンストリームは例外を示さずに大量のデータを失い、深刻なデータの不整合が発生する可能性があります。
-   **セーフ モードは、主キーまたは一意のインデックスに依存して競合を検出します。**ダウンストリーム テーブルに主キーまたは一意のインデックスがない場合、DM は`REPLACE`を使用してレコードを置換および挿入できません。この場合、セーフ モードが有効になっており、DM が`INSERT` ～ `REPLACE`個のステートメントを書き換えても、重複したレコードが下流に挿入されます。

要約すると、アップストリーム データベースに重複した主キーを持つデータがあり、アプリケーションが重複レコードの損失とパフォーマンス オーバーヘッドを許容する場合は、セーフ モードを有効にしてデータの重複を無視できます。
