---
title: DM Safe Mode
summary: Introduces the DM safe mode, its purpose, working principles and how to use it.
---

# DMセーフモード {#dm-safe-mode}

セーフ モードは、DM が増分レプリケーションを実行するための特別な操作モードです。セーフ モードでは、DM 増分レプリケーションコンポーネントがbinlogイベントをレプリケートするときに、DM はダウンストリームで実行する前に`INSERT`と`UPDATE`ステートメントをすべて強制的に書き換えます。

セーフ モードでは、冪等性が保証された状態で、1 つのbinlogイベントをダウンストリームに繰り返し複製できます。したがって、増分レプリケーションは*安全*です。

データ レプリケーション タスクをチェックポイントから再開した後、DM は一部のbinlogイベントを繰り返しレプリケートする可能性があり、これにより次の問題が発生します。

-   インクリメンタル レプリケーション中、DML の実行操作とチェックポイントの書き込み操作は同時に行われません。チェックポイントの書き込みおよびダウンストリーム データベースへのデータの書き込み操作はアトミックではありません。したがって、 **DM が異常終了した場合、チェックポイントは終了ポイントより前の復元ポイントのみを記録する可能性があります**。
-   DM がレプリケーション タスクを再開し、チェックポイントから増分レプリケーションを再開すると、チェックポイントと終了ポイントの間の一部のデータが異常終了する前にすでに処理されている可能性があります。これにより、**一部の SQL ステートメントが繰り返し実行されます**。
-   `INSERT`ステートメントが繰り返し実行されると、主キーまたは一意のインデックスで競合が発生し、レプリケーションの失敗につながる可能性があります。 `UPDATE`ステートメントが繰り返し実行されると、フィルター条件で以前に更新されたレコードを見つけることができない可能性があります。

セーフ モードでは、DM は SQL ステートメントを書き換えて前述の問題を解決できます。

## 動作原理 {#working-principle}

セーフ モードでは、DM は SQL ステートメントを書き換えることによってbinlogイベントの冪等性を保証します。具体的には、次の SQL ステートメントが書き換えられます。

-   `INSERT`のステートメントは`REPLACE`のステートメントに書き換えられます。
-   `UPDATE`ステートメントが分析されて、主キーの値または更新された行の一意のインデックスが取得されます。次に、次の 2 つの手順で`UPDATE`ステートメントが`DELETE` + `REPLACE`ステートメントに書き換えられます。DM は主キーまたは一意のインデックスを使用して古いレコードを削除し、 `REPLACE`ステートメントを使用して新しいレコードを挿入します。

`REPLACE`データを挿入するための MySQL 固有の構文です。 `REPLACE`を使用してデータを挿入し、新しいデータと既存のデータに主キーまたは一意制約の競合がある場合、MySQL は競合するレコードをすべて削除し、「強制挿入」と同等の挿入操作を実行します。詳細については、MySQL ドキュメントの[`REPLACE`文](https://dev.mysql.com/doc/refman/8.0/en/replace.html)参照してください。

`dummydb.dummytbl`テーブルに主キー`id`があるとします。このテーブルに対して次の SQL ステートメントを繰り返し実行します。

```sql
INSERT INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
UPDATE dummydb.dummytbl SET int_value = 888999 WHERE int_value = 999;   -- Suppose there is no other record with int_value = 999
UPDATE dummydb.dummytbl SET id = 999 WHERE id = 888;    -- Update the primary key
```

セーフ モードを有効にすると、前述の SQL ステートメントがダウンストリームで再度実行されると、次のように書き換えられます。

```sql
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 123;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 888999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 888;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (999, 888888, 'abc888');
```

前述のステートメントでは、 `UPDATE` `DELETE` + `INSERT`ではなく`DELETE` + `REPLACE`に書き換えられます。ここで`INSERT`が使用されている場合、 `id = 999`を含む重複レコードを挿入すると、データベースは主キーの競合を報告します。このため、代わりに`REPLACE`が使用されます。新しいレコードは既存のレコードを置き換えます。

SQL ステートメントを書き換えることにより、DM は重複した挿入または更新操作を実行するときに、新しい行データを使用して既存の行データを上書きします。これにより、挿入操作と更新操作が繰り返し実行されることが保証されます。

## セーフモードを有効にする {#enable-safe-mode}

セーフ モードは自動または手動で有効にできます。このセクションでは、詳細な手順について説明します。

### 自動的に有効にする {#automatically-enable}

DM がチェックポイントから増分レプリケーション タスクを再開すると (DM ワーカーの再起動やネットワークの再接続など)、DM は一定期間 (デフォルトでは 60 秒) セーフ モードを自動的に有効にします。

セーフモードを有効にするかどうかはチェックポイントの`safemode_exit_point`に関係します。増分レプリケーション タスクが異常停止すると、DM はメモリ内のすべての DML ステートメントをダウンストリームにレプリケートしようとし、DML ステートメント内の最新のbinlog位置を`safemode_exit_point`として記録し、最後のチェックポイントに保存されます。

詳細なロジックは次のとおりです。

-   チェックポイントに`safemode_exit_point`が含まれている場合、増分レプリケーション タスクは異常に一時停止されます。 DM がタスクを再開すると、再開されるチェックポイントのbinlog位置 (**開始位置**) は`safemode_exit_point`より前になります。これは、開始位置と`safemode_exit_point`の間のbinlogイベントがダウンストリームで処理された可能性があることを表します。そのため、再開プロセス中に、一部のbinlogイベントが繰り返し実行される可能性があります。したがって、セーフ モードを有効にすると、これらのbinlogの位置を**安全に**することができます。binlog位置が`safemode_exit_point`を超えると、セーフ モードが手動で有効にされない限り、DM はセーフ モードを自動的に無効にします。

-   チェックポイントに`safemode_exit_point`含まれていない場合は、次の 2 つのケースが考えられます。

    1.  これは新しいタスクであるか、このタスクは予想どおり一時停止されています。
    2.  このタスクは異常に一時停止されましたが、DM が`safemode_exit_point`を記録できなかったか、DM プロセスが異常終了しました。

    2 番目のケースでは、DM はチェックポイント後のどのbinlogイベントがダウンストリームで実行されるかを知りません。繰り返し実行されるbinlogイベントによって問題が発生しないようにするために、DM は最初の 2 つのチェックポイント間隔でセーフ モードを自動的に有効にします。 2 つのチェックポイント間のデフォルトの間隔は 30 秒です。つまり、通常の増分レプリケーション タスクが開始されると、最初の 60 秒 (2 * 30 秒) はセーフ モードが適用されます。

    通常、増分レプリケーション タスクの開始時にセーフ モード期間を調整するためにチェックポイント間隔を変更することはお勧めできません。ただし、変更が必要な場合は、シンサー構成の[セーフモードを手動で有効にする](#manually-enable) (推奨) または`checkpoint-flush-interval`項目を変更できます。

### 手動で有効にする {#manually-enable}

シンサー構成の`safe-mode`項目を設定して、レプリケーション プロセス全体でセーフ モードを有効にすることができます。 `safe-mode`は bool 型パラメータで、デフォルトは`false`です。 `true`に設定すると、DM は増分レプリケーション プロセス全体に対してセーフ モードを有効にします。

以下は、セーフ モードが有効になっているタスク構成の例です。

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

## セーフモードに関する注意事項 {#notes-for-safe-mode}

安全上の理由から、レプリケーション プロセス全体でセーフ モードを有効にする場合は、次の点に注意してください。

-   **セーフ モードでの増分レプリケーションは、余分なオーバーヘッドを消費します。** `DELETE` + `REPLACE`の操作を頻繁に行うと、主キーまたは一意のインデックスが頻繁に変更されるため、 `UPDATE`ステートメントのみを実行する場合よりもパフォーマンスのオーバーヘッドが大きくなります。
-   **セーフ モードでは、同じ主キーを持つレコードの置換が強制されるため、ダウンストリームでデータが失われる可能性があります。**シャードを上流から下流にマージして移行する場合、構成が正しくないと、主キーまたは一意キーの多数の競合が発生する可能性があります。この状況でセーフ モードが有効になっていると、ダウンストリームで例外が表示されずに大量のデータが失われる可能性があり、その結果、深刻なデータの不整合が発生します。
-   **セーフ モードは、主キーまたは一意のインデックスに依存して競合を検出します。**ダウンストリーム テーブルに主キーまたは一意のインデックスがない場合、DM は`REPLACE`を使用してレコードを置換および挿入できません。この場合、セーフ モードが有効になっていて DM が`INSERT` ～ `REPLACE`個のステートメントを書き換えたとしても、重複レコードは引き続きダウンストリームに挿入されます。

要約すると、アップストリーム データベースに重複した主キーを持つデータがあり、アプリケーションが重複レコードの損失とパフォーマンスのオーバーヘッドを許容する場合は、セーフ モードを有効にしてデータの重複を無視できます。
