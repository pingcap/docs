---
title: DM Safe Mode
summary: DM セーフ モード、その目的、動作原理、および使用方法について説明します。
---

# DMセーフモード {#dm-safe-mode}

セーフモードは、DMが増分レプリケーションを実行するための特別な動作モードです。セーフモードでは、DMの増分レプリケーションコンポーネントがbinlogイベントをレプリケートする際、DMは下流で実行する前に、すべてのステートメント`INSERT`と`UPDATE`を強制的に書き換えます。

セーフモードでは、1つのbinlogイベントを下流に繰り返し複製することができ、冪等性が保証されます。したがって、増分レプリケーションは*安全*です。

チェックポイントからデータ レプリケーション タスクを再開した後、DM が一部のbinlogイベントを繰り返しレプリケートすることがあり、次の問題が発生します。

-   増分レプリケーションでは、DML実行操作とチェックポイント書き込み操作は同時に行われません。チェックポイント書き込み操作と下流データベースへのデータ書き込み操作はアトミックではありません。そのため、 **DMが異常終了した場合、チェックポイントは終了ポイントの前の復元ポイントのみを記録する可能性があります**。
-   DMがレプリケーションタスクを再開し、チェックポイントから増分レプリケーションを再開すると、チェックポイントと終了ポイントの間の一部のデータが異常終了前に既に処理されている可能性があります。これにより**、一部のSQL文が繰り返し実行されます**。
-   `INSERT`ステートメントが繰り返し実行されると、主キーまたは一意のインデックスに競合が発生し、レプリケーションが失敗する可能性があります。3 `UPDATE`ステートメントが繰り返し実行されると、フィルター条件で以前に更新されたレコードを見つけられない可能性があります。

セーフ モードでは、DM は SQL ステートメントを書き換えて、前述の問題を解決できます。

## 動作原理 {#working-principle}

セーフモードでは、DM は SQL 文を書き換えることで、 binlogイベントの冪等性を保証します。具体的には、以下の SQL 文が書き換えられます。

-   `INSERT`ステートメントが`REPLACE`ステートメントに書き換えられます。
-   `UPDATE`ステートメントが分析され、更新された行の主キーまたは一意のインデックスの値を取得します。次に、 `UPDATE`ステートメントが次の 2 つの手順で`DELETE` + `REPLACE`ステートメントに書き換えられます。DM は主キーまたは一意のインデックスを使用して古いレコードを削除し、 `REPLACE`ステートメントを使用して新しいレコードを挿入します。

`REPLACE`は、MySQL固有のデータ挿入構文です。2 `REPLACE`使用してデータを挿入し、新規データと既存データに主キーまたは一意制約の競合がある場合、MySQLは競合するレコードをすべて削除し、挿入操作を実行します。これは「強制挿入」と同等です。詳細については、MySQLドキュメントの[`REPLACE`文](https://dev.mysql.com/doc/refman/8.0/en/replace.html)参照してください。

テーブル`dummydb.dummytbl`主キー`id`があると仮定します。このテーブルに対して、次の SQL 文を繰り返し実行します。

```sql
INSERT INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
UPDATE dummydb.dummytbl SET int_value = 888999 WHERE int_value = 999;   -- Suppose there is no other record with int_value = 999
UPDATE dummydb.dummytbl SET id = 999 WHERE id = 888;    -- Update the primary key
```

セーフ モードを有効にすると、前述の SQL ステートメントがダウンストリームで再度実行されるときに、次のように書き換えられます。

```sql
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 123;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 888999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 888;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (999, 888888, 'abc888');
```

上記の文では、 `UPDATE` `DELETE` + `INSERT`ではなく`DELETE` + `REPLACE`に書き換えられています。ここで`INSERT`使用すると、 `id = 999`の重複レコードを挿入すると、データベースは主キーの競合を報告します。そのため、代わりに`REPLACE`使用されます。新しいレコードは既存のレコードを置き換えます。

DMはSQL文を書き換えることで、重複する挿入または更新操作を実行する際に、既存の行データを新しい行データで上書きします。これにより、挿入および更新操作が繰り返し実行されることが保証されます。

## セーフモードを有効にする {#enable-safe-mode}

セーフモードは自動または手動で有効にできます。このセクションでは詳細な手順を説明します。

### 自動的に有効にする {#automatically-enable}

DM がチェックポイントから増分レプリケーション タスクを再開すると (たとえば、DM ワーカーの再起動やネットワークの再接続)、DM は一定期間 (デフォルトでは 60 秒) 自動的にセーフ モードを有効にします。

セーフモードを有効にするかどうかは、チェックポイントの`safemode_exit_point`と関連しています。増分レプリケーションタスクが異常停止した場合、DM はメモリ内のすべての DML 文を下流にレプリケーションしようとし、DML 文の中で最新のbinlog位置を`safemode_exit_point`として記録します。これは最後のチェックポイントに保存されます。

詳細なロジックは次のとおりです。

-   チェックポイントに`safemode_exit_point`が含まれている場合、増分レプリケーションタスクは異常停止しています。DM がタスクを再開すると、再開対象のチェックポイントのbinlog位置（**開始位置**）が`safemode_exit_point`より前になります。これは、開始位置から`safemode_exit_point`のbinlogイベントが下流で処理されている可能性があることを示しています。そのため、再開プロセス中に、一部のbinlogイベントが繰り返し実行される可能性があります。したがって、セーフモードを有効にすると、これらのbinlog位置を**安全に**することができます。binlog位置が`safemode_exit_point`超えると、手動でセーフモードを有効にしない限り、DM は自動的にセーフモードを無効にします。

-   チェックポイントに`safemode_exit_point`が含まれていない場合、次の 2 つのケースが考えられます。

    1.  これは新しいタスクです。または、このタスクは予想どおり一時停止されています。
    2.  このタスクは異常一時停止されていますが、DM は`safemode_exit_point`記録できないか、DM プロセスが異常終了します。

    2番目のケースでは、DMはチェックポイント後のどのbinlogイベントが下流で実行されるかを把握できません。繰り返し実行されるbinlogイベントによる問題を回避するため、DMは最初の2つのチェックポイント間隔で自動的にセーフモードを有効にします。2つのチェックポイント間のデフォルトの間隔は30秒です。つまり、通常の増分レプリケーションタスクが開始されると、最初の60秒間（2×30秒）はセーフモードが適用されます。

    通常、増分レプリケーションタスクの開始時にセーフモード期間を調整するためにチェックポイント間隔を変更することは推奨されません。ただし、変更が必要な場合は、Syncer設定の項目[セーフモードを手動で有効にする](#manually-enable) （推奨）または項目`checkpoint-flush-interval`を変更することができます。

### 手動で有効にする {#manually-enable}

Syncer設定の項目`safe-mode`設定すると、レプリケーションプロセス全体でセーフモードが有効になります。3 `safe-mode`ブール型のパラメータで、デフォルトは`false`です`true`に設定すると、DMは増分レプリケーションプロセス全体でセーフモードを有効にします。

以下は、セーフ モードを有効にしたタスク構成の例です。

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

-   **セーフモードでの増分レプリケーションは、余分なオーバーヘッドを消費します。2** + `REPLACE`操作`DELETE`頻繁に実行すると、主キーまたは一意のインデックスが頻繁に変更されるため、 `UPDATE`ステートメントのみを実行する場合よりもパフォーマンスのオーバーヘッドが大きくなります。
-   **セーフモードでは、同じ主キーを持つレコードが強制的に置換されるため、下流でデータ損失が発生する可能性があります。**上流から下流へシャードをマージして移行する際、不適切な設定によって主キーまたは一意キーの競合が多数発生する可能性があります。このような状況でセーフモードを有効にすると、下流で例外が表示されずに大量のデータが失われ、深刻なデータ不整合が発生する可能性があります。
-   **セーフモードは、主キーまたは一意のインデックスに基づいて競合を検出します。**下流テーブルに主キーまたは一意のインデックスがない場合、DMは`REPLACE`使用してレコードの置換と挿入を行うことができません。この場合、セーフモードが有効でDMが`INSERT` ～ `REPLACE`ステートメントを書き換えても、下流テーブルに重複レコードが挿入されてしまいます。

要約すると、アップストリーム データベースに重複した主キーを持つデータがあり、アプリケーションが重複レコードの損失とパフォーマンスのオーバーヘッドを許容する場合は、セーフ モードを有効にしてデータの重複を無視できます。
