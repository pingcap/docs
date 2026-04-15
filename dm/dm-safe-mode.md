---
title: DM Safe Mode
summary: DMセーフモードについて、その目的、動作原理、および使用方法を紹介します。
---

# DMセーフモード {#dm-safe-mode}

セーフモードは、DMが増分レプリケーションを実行するための特別な動作モードです。セーフモードでは、DMの増分レプリケーションコンポーネントがbinlogイベントをレプリケートする際に、DMは下流で実行する前に、 `INSERT`および`UPDATE`ステートメントを強制的に書き換えます。

セーフモード中は、1つのbinlogイベントを冪等性が保証された状態でダウンストリームに繰り返し複製できます。したがって、増分複製は*安全*です。

チェックポイントからデータレプリケーションタスクを再開した後、DMは一部のbinlogイベントを繰り返しレプリケートする可能性があり、その結果、以下の問題が発生します。

-   増分レプリケーションでは、DMLの実行操作とチェックポイントの書き込み操作は同時に行われません。チェックポイントの書き込み操作とダウンストリームデータベースへのデータの書き込み操作はアトミックではありません。そのため、 **DMが異常終了した場合、チェックポイントには終了ポイントの直前の復元ポイントのみが記録される可能性があります**。
-   DMがレプリケーションタスクを再開し、チェックポイントから増分レプリケーションを再開する場合、チェックポイントと終了ポイントの間のデータの一部は、異常終了前に既に処理されている可能性があります。これにより**、一部のSQLステートメントが繰り返し実行されること**があります。
-   `INSERT`ステートメントが繰り返し実行されると、主キーまたは一意インデックスで競合が発生し、レプリケーションエラーが発生する可能性があります。 `UPDATE`ステートメントが繰り返し実行されると、フィルタ条件が以前に更新されたレコードを見つけられない可能性があります。

セーフモードでは、DMはSQL文を書き換えて上記の問題を解決できます。

## 動作原理 {#working-principle}

セーフモードでは、DMはSQL文を書き換えることでbinlogイベントの冪等性を保証します。具体的には、以下のSQL文が書き換えられます。

-   `INSERT`ステートメントは`REPLACE`ステートメントに書き換えられます。
-   `UPDATE`ステートメントが分析され、更新された行の主キーまたは一意インデックスの値を取得します。次に`UPDATE`ステートメントが、次の 2 つのステップで`DELETE` + `REPLACE`ステートメントに書き換えられます。DM は、主キーまたは一意インデックスを使用して古いレコードを削除し、 `REPLACE`を使用して新しいレコードを挿入します。

    バージョン8.5.6以降、タスクセッションで`foreign_key_checks=1`を設定すると、DMは主キーまたは一意インデックス値を変更しない`DELETE` `UPDATE`ステップをスキップします。詳細については、[外部キーの処理](#foreign-key-handling-new-in-v856)キー を参照してください。

`REPLACE`は、MySQL でデータを挿入するための固有の構文です。 `REPLACE`を使用してデータを挿入し、新しいデータと既存のデータに主キーまたは一意制約の競合がある場合、MySQL は競合するすべてのレコードを削除し、挿入操作を実行します。これは「強制挿入」と同等です。詳細については、MySQL ドキュメントの[`REPLACE`文](https://dev.mysql.com/doc/refman/8.0/en/replace.html)参照してください。

`dummydb.dummytbl`テーブルに主キー`id`があると仮定します。このテーブルに対して、次の SQL ステートメントを繰り返し実行します。

```sql
INSERT INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
UPDATE dummydb.dummytbl SET int_value = 888999 WHERE int_value = 999;   -- Suppose there is no other record with int_value = 999
UPDATE dummydb.dummytbl SET id = 999 WHERE id = 888;    -- Update the primary key
```

セーフモードが有効になっている場合、ダウンストリームで前述のSQL文が再度実行されると、次のように書き換えられます。

```sql
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 123;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 888999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 888;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (999, 888888, 'abc888');
```

上記の記述では、 `UPDATE`は`DELETE` + `REPLACE`と書き換えられ、 `DELETE` + `INSERT`とは書き換えられません。ここで`INSERT`を使用した場合、 `id = 999`で重複レコードを挿入すると、データベースで主キーの競合が報告されます。そのため、代わりに`REPLACE`が使用されます。新しいレコードは既存のレコードを置き換えます。

DMはSQL文を書き換えることで、重複挿入または更新操作を実行する際に、既存の行データを新しい行データで上書きします。これにより、挿入および更新操作が確実に繰り返し実行されるようになります。

## セーフモードを有効にする {#enable-safe-mode}

セーフモードは、自動または手動で有効にできます。このセクションでは、その詳細な手順を説明します。

### 自動的に有効にする {#automatically-enable}

DMがチェックポイントから増分レプリケーションタスクを再開する場合（例えば、DMワーカーの再起動やネットワークの再接続など）、DMは自動的に一定期間（デフォルトでは60秒）セーフモードを有効にします。

セーフモードを有効にするかどうかは、チェックポイント内の`safemode_exit_point`に関連しています。増分レプリケーション タスクが異常に一時停止された場合、DM はメモリ内のすべての DML ステートメントをダウンストリームにレプリケートしようとし、DML ステートメントの中で最新のbinlog位置を`safemode_exit_point`として記録し、最後のチェックポイントに保存します。

詳細なロジックは以下のとおりです。

-   チェックポイントに`safemode_exit_point`が含まれている場合、増分レプリケーション タスクは異常に一時停止されます。 DM がタスクを再開すると、再開するチェックポイントのbinlog位置 (**開始位置**) が`safemode_exit_point`より前になります。これは、開始位置と`safemode_exit_point`の間のbinlogイベントが下流で処理されている可能性があることを示しています。そのため、再開処理中に一部のbinlogイベントが繰り返し実行される可能性があります。したがって、セーフ モードを有効にすると、これらのbinlog位置を**安全**にすることができます。binlog位置が`safemode_exit_point`を超えると、セーフ モードが手動で有効にされない限り、DM は自動的にセーフ モードを無効にします。

-   チェックポイントに`safemode_exit_point`が含まれていない場合、次の 2 つのケースが考えられます。

    1.  これは新規タスクです。もしくは、このタスクは想定どおり一時停止されています。
    2.  このタスクは異常に一時停止されましたが、DM は`safemode_exit_point`を記録できませんでした。または、DM プロセスが異常終了しました。

    2番目のケースでは、DMはチェックポイント後のどのbinlogイベントがダウンストリームで実行されるかを把握できません。繰り返し実行されるbinlogイベントが問題を引き起こさないようにするため、DMは最初の2つのチェックポイント間隔の間、自動的にセーフモードを有効にします。2つのチェックポイント間のデフォルトの間隔は30秒です。つまり、通常の増分レプリケーションタスクが開始されると、最初の60秒間（2×30秒）はセーフモードが適用されます。

    通常、増分レプリケーション タスクの開始時にセーフ モード期間を調整するためにチェックポイント間隔を変更することはお勧めできません。ただし、変更が必要な場合は、[セーフモードを手動で有効にする](#manually-enable)(推奨)か、同期設定の`checkpoint-flush-interval`項目を変更できます。

### 手動で有効化 {#manually-enable}

同期設定で`safe-mode`項目を設定すると、レプリケーション処理全体を通してセーフモードが有効になります。 `safe-mode`はブール型のパラメーターで、デフォルト値は`false`です。 `true`に設定すると、DM は増分レプリケーション処理全体を通してセーフモードを有効にします。

以下は、セーフモードを有効にしたタスク構成の例です。

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

## 外部キーの処理<span class="version-mark">（v8.5.6の新機能）</span> {#foreign-key-handling-span-class-version-mark-new-in-v8-5-6-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。予告なく変更または削除される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tiflow/issues)を報告してください。

セーフ モードを有効にしてダウンストリーム タスク セッションで`foreign_key_checks=1`を設定すると、 `DELETE`ステートメントのデフォルトの`REPLACE` + `UPDATE`書き換えにより、子行に意図しない`ON DELETE CASCADE`影響が発生する可能性があります。v8.5.6 以降、DM ではこの問題に対処するために以下の改善が導入されています。

### 非キー<code>UPDATE</code>最適化 {#non-key-code-update-code-optimization}

主キーまたは一意キーの値を変更しない`UPDATE`ステートメントの場合、DM は`DELETE`ステップをスキップし、 `REPLACE INTO`のみを実行します。主キーは変更されないため、 `REPLACE INTO`外部キーのカスケード削除をトリガーすることなく既存の行を上書きします。この最適化はセーフモードで自動的に適用されます。

次のアップストリームステートメントを例として挙げます。ここで、 `id`は主キーです。

```sql
UPDATE dummydb.dummytbl SET int_value = 888999 WHERE id = 123;
```

バージョン8.5.6より前のバージョンでは、セーフモードではこの記述が次のように書き換えられます。

```sql
DELETE FROM dummydb.dummytbl WHERE id = 123;       -- Triggers ON DELETE CASCADE
REPLACE INTO dummydb.dummytbl (id, int_value, ...) VALUES (123, 888999, ...);
```

バージョン8.5.6以降、セーフモードでは、この記述が次のように書き換えられます。

```sql
REPLACE INTO dummydb.dummytbl (id, int_value, ...) VALUES (123, 888999, ...);  -- No cascade
```

> **警告：**
>
> `foreign_key_checks=1`の場合、DM は主キーまたは一意キーの値を変更する`UPDATE`ステートメントの複製をサポートしません。この場合、複製タスクはエラー`safe-mode update with foreign_key_checks=1 and PK/UK changes is not supported`で一時停止されます。外部キーを持つテーブルでそのような`UPDATE`ステートメントを複製するには、 `safe-mode: false`を設定します。

### セッションレベルの<code>foreign_key_checks</code> {#session-level-code-foreign-key-checks-code}

セーフモードでのバッチ実行中、DM は`SET SESSION foreign_key_checks=0`および`INSERT`バッチを実行する前に`UPDATE`を実行し、その後`foreign_key_checks`の元の値を復元します。これにより`REPLACE INTO` (内部で`DELETE` + `INSERT`を実行) が下流で外部キーのカスケード操作をトリガーするのを防ぎます。

このセッションレベルの設定では`SET SESSION`バッチごとにわずかなオーバーヘッド（2回の往復）が発生します。ほとんどのワークロードでは、このオーバーヘッドは無視できる程度です。

### 複数ワーカーの外部キー因果関係 {#multi-worker-foreign-key-causality}

`worker-count` 1 より大きい値に設定し、レプリケーション タスクに外部キーを持つテーブルが含まれている場合、タスクの開始時に DM は下流の`CREATE TABLE`スキーマから外部キーの関係を読み取ります。DM は、各 DML 操作に対して、これらの関係に基づいて因果関係キーを挿入します。これにより、親行とその子行に対する操作が同じ DML ワーカー キューに割り当てられることが保証されます。

詳細な制約については、 [DM互換性カタログ](/dm/dm-compatibility-catalog.md#foreign-key-cascade-operations)を参照してください。

## セーフモードに関する注意事項 {#notes-for-safe-mode}

安全上の理由から、レプリケーションプロセス全体を通してセーフモードを有効にする場合は、以下の点に注意してください。

-   **セーフモードでの増分レプリケーションは、余分なオーバーヘッドを消費します。** `DELETE` + `REPLACE`操作が頻繁に行われると、主キーまたは一意インデックスが頻繁に変更されるため、 `UPDATE`ステートメントのみを実行する場合よりもパフォーマンスのオーバーヘッドが大きくなります。
-   **セーフモードでは、同じプライマリキーを持つレコードの置換が強制されるため、ダウンストリームでデータ損失が発生する可能性があります。**アップストリームからダウンストリームへシャードをマージおよび移行する際に、設定が誤っていると、多数のプライマリキーまたはユニークキーの競合が発生する可能性があります。このような状況でセーフモードが有効になっている場合、ダウンストリームでは例外が表示されないまま大量のデータが失われ、深刻なデータ不整合が発生する可能性があります。
-   **セーフモードは、競合を検出するために主キーまたは一意インデックスに依存します。**ダウンストリームテーブルに主キーまたは一意インデックスがない場合、DM は`REPLACE`を使用してレコードを置換および挿入できません。この場合、セーフモードが有効になっていて、DM が`INSERT`ステートメントを`REPLACE`に書き換えたとしても、重複レコードがダウンストリームに挿入されます。

要約すると、上流のデータベースに重複した主キーを持つデータが存在し、アプリケーションが重複レコードの損失とパフォーマンスのオーバーヘッドを許容できる場合、セーフモードを有効にしてデータの重複を無視することができます。
