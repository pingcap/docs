---
title: Continuous Data Validation in DM
summary: 継続的なデータ検証の使用方法と継続的なデータ検証の動作原理を学習します。
---

# DMにおける継続的なデータ検証 {#continuous-data-validation-in-dm}

このドキュメントでは、DM での継続的なデータ検証の使用方法、その動作原理、およびその制限について説明します。

## ユーザーシナリオ {#user-scenario}

上流データベースから下流データベースへのデータの段階的移行プロセスでは、データフローによってデータの破損や損失が発生する可能性がわずかにあります。信用取引や証券業界など、データの整合性が求められるシナリオでは、移行完了後に完全なデータ検証を実施し、データの整合性を確保することができます。

しかし、増分移行シナリオでは、上流と下流の両方で継続的にデータが書き込まれます。上流と下流の両方でデータが絶えず変化するため、テーブル内のすべてのデータに対して完全なデータ検証（例えば、 [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用する）を実行することは困難です。

増分移行シナリオでは、DMの継続的なデータ検証機能を使用できます。この機能は、データが下流に継続的に書き込まれる増分移行中に、データの整合性と一貫性を確保します。

## 継続的なデータ検証を有効にする {#enable-continuous-data-validation}

次のいずれかの方法を使用して、継続的なデータ検証を有効にすることができます。

-   タスク構成ファイルで有効にします。
-   dmctl を使用して有効にします。

### 方法1: タスク設定ファイルで有効にする {#method-1-enable-in-the-task-configuration-file}

継続的なデータ検証を有効にするには、タスク構成ファイルに次の構成項目を追加します。

```yaml
# Add the following configuration items to the upstream database that needs to be validated:
mysql-instances:
  - source-id: "mysql1"
    block-allow-list: "bw-rule-1"
    validator-config-name: "global"
validators:
  global:
    mode: full # "fast" is also allowed. "none" is the default mode, which means no validation is performed.
    worker-count: 4 # The number of validation workers in the background. The default value is 4.
    row-error-delay: 30m # If a row cannot pass the validation within the specified time, it will be marked as an error row. The default value is 30m, which means 30 minutes.
```

構成項目は次のとおりです。

-   `mode` : 検証モード。可能な値は`none` 、 `full` 、 `fast`です。
    -   `none` : デフォルト値。検証は実行されないことを意味します。
    -   `full` : 変更された行と下流データベースで取得された行を比較します。
    -   `fast` : 変更された行がダウンストリーム データベースに存在するかどうかのみを確認します。
-   `worker-count` : バックグラウンドで実行される検証ワーカーの数。各ワーカーはゴルーチンです。
-   `row-error-delay` : 指定された時間内に行が検証に合格できない場合、エラー行としてマークされます。デフォルト値は30分です。

完全な構成については、 [DM 高度なタスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

### 方法2: dmctlを使用して有効にする {#method-2-enable-using-dmctl}

継続的なデータ検証を有効にするには、 `dmctl validation start`コマンドを実行します。

    Usage:
      dmctl validation start [--all-task] [task-name] [flags]

    Flags:
          --all-task            whether applied to all tasks
      -h, --help                help for start
          --mode string         specify the mode of validation: full (default), fast; this flag will be ignored if the validation task has been ever enabled but currently paused (default "full")
          --start-time string   specify the start time of binlog for validation, e.g. '2021-10-21 00:01:00' or 2021-10-21T00:01:00

-   `--mode` : 検証モードを指定します。指定できる値は`fast`と`full`です。
-   `--start-time` : 検証の開始時刻を指定します。形式は`2021-10-21 00:01:00`または`2021-10-21T00:01:00`に従います。
-   `task` : 継続的検証を有効にするタスク名を指定します。2 `--all-task`指定すると、すべてのタスクに対して検証が有効になります。

例えば：

```shell
dmctl --master-addr=127.0.0.1:8261 validation start --start-time 2021-10-21T00:01:00 --mode full my_dm_task
```

## 継続的なデータ検証を使用する {#use-continuous-data-validation}

継続的なデータ検証を使用する場合、dmctl を使用して検証のステータスを表示し、エラー行を処理できます。「エラー行」とは、上流データベースと下流データベース間で不整合が検出された行を指します。

### 検証ステータスをビュー {#view-the-validation-status}

検証ステータスは、次のいずれかの方法で表示できます。

方法1：コマンド`dmctl query-status <task-name>`を実行します。継続的なデータ検証が有効になっている場合、検証結果は各サブタスクの`validation`フィールドに表示されます。出力例：

```json
"subTaskStatus": [
    {
        "name": "test",
        "stage": "Running",
        "unit": "Sync",
        "result": null,
        "unresolvedDDLLockID": "",
        "sync": {
            ...
        },
        "validation": {
            "task": "test", // Task name
            "source": "mysql-01", // Source id
            "mode": "full", // Validation mode
            "stage": "Running", // Current stage. "Running" or "Stopped".
            "validatorBinlog": "(mysql-bin.000001, 5989)", // The binlog position of the validation
            "validatorBinlogGtid": "1642618e-cf65-11ec-9e3d-0242ac110002:1-30", // The GTID position of the validation
            "cutoverBinlogPos": "", // The specified binlog position for cutover
            "cutoverBinlogGTID": "1642618e-cf65-11ec-9e3d-0242ac110002:1-30", // The specified GTID position for cutover
            "result": null, // When the validation is abnormal, show the error message
            "processedRowsStatus": "insert/update/delete: 0/0/0", // Statistics of the processed binlog rows.
            "pendingRowsStatus": "insert/update/delete: 0/0/0", // Statistics of the binlog rows that are not validated yet or that fail to be validated but are not marked as "error rows"
            "errorRowsStatus": "new/ignored/resolved: 0/0/0" // Statistics of the error rows. The three statuses are explained in the next section.
        }
    }
]
```

方法 2: コマンド`dmctl validation status <taskname>`を実行します。

    dmctl validation status [--table-stage stage] <task-name> [flags]
    Flags:
      -h, --help                 help for status
          --table-stage string   filter validation tables by stage: running/stopped

上記のコマンドで`--table-stage`使用すると、検証対象のテーブルをフィルタリングしたり、検証を停止したりできます。出力例:

```json
{
    "result": true,
    "msg": "",
    "validators": [
        {
            "task": "test",
            "source": "mysql-01",
            "mode": "full",
            "stage": "Running",
            "validatorBinlog": "(mysql-bin.000001, 6571)",
            "validatorBinlogGtid": "",
            "cutoverBinlogPos": "(mysql-bin.000001, 6571)",
            "cutoverBinlogGTID": "",
            "result": null,
            "processedRowsStatus": "insert/update/delete: 2/0/0",
            "pendingRowsStatus": "insert/update/delete: 0/0/0",
            "errorRowsStatus": "new/ignored/resolved: 0/0/0"
        }
    ],
    "tableStatuses": [
        {
            "source": "mysql-01", // Source id
            "srcTable": "`db`.`test1`", // Source table name
            "dstTable": "`db`.`test1`", // Target table name
            "stage": "Running", // Validation status
            "message": "" // Error message
        }
    ]
}
```

エラーの種類やエラー時間などのエラー行の詳細を表示するには、次の`dmctl validation show-error`コマンドを実行します。

    Usage:
      dmctl validation show-error [--error error-state] <task-name> [flags]

    Flags:
          --error string   filtering type of error: all, ignored, or unprocessed (default "unprocessed")
      -h, --help           help for show-error

出力例:

```json
{
    "result": true,
    "msg": "",
    "error": [
        {
            "id": "1", // Error row id, which will be used in processing error rows
            "source": "mysql-replica-01", // Source id
            "srcTable": "`validator_basic`.`test`", // Source table of the error row
            "srcData": "[0, 0]", // Data of the error row in the source table
            "dstTable": "`validator_basic`.`test`", // Target table of the error row
            "dstData": "[]", // Data of the error row in the target table
            "errorType": "Expected rows not exist", // Error type
            "status": "NewErr", // Error status
            "time": "2022-07-04 13:33:02", // Discovery time of the error row
            "message": "" // Additional information
        }
    ]
}
```

### エラー行を処理する {#handle-error-rows}

継続的なデータ検証でエラー行が返されたら、エラー行を手動で処理する必要があります。

継続的データ検証でエラー行が見つかった場合、検証はすぐには停止しません。代わりに、エラー行を記録して処理できるようにします。エラー行が処理される前のデフォルトのステータスは`unprocessed`です。下流でエラー行を手動で修正した場合、検証は修正されたデータの最新のステータスを自動的に取得しません。エラー行は引き続き`error`フィールドに記録されます。

検証ステータスにエラー行を表示したくない場合、またはエラー行を解決済みとしてマークしたい場合は、 `validation show-error`コマンドを使用してエラー行 ID を見つけ、その後、指定されたエラー ID を使用して処理することができます。

dmctl は 3 つのエラー処理コマンドを提供します。

-   `clear-error` : エラー行をクリアします。2 コマンド`show-error`実行すると、エラー行は表示されなくなります。

        Usage:
          dmctl validation clear-error <task-name> <error-id|--all> [flags]

        Flags:
              --all    all errors
          -h, --help   help for clear-error

-   `ignore-error` : エラー行を無視します。このエラー行は「無視」としてマークされます。

        Usage:
          dmctl validation ignore-error <task-name> <error-id|--all> [flags]

        Flags:
              --all    all errors
          -h, --help   help for ignore-error

-   `resolve-error` : エラー行は手動で処理され、「解決済み」としてマークされます。

        Usage:
          dmctl validation resolve-error <task-name> <error-id|--all> [flags]

        Flags:
              --all    all errors
          -h, --help   help for resolve-error

## 継続的なデータ検証を停止する {#stop-continuous-data-validation}

継続的なデータ検証を停止するには、コマンド`validation stop`を実行します。

    Usage:
      dmctl validation stop [--all-task] [task-name] [flags]

    Flags:
          --all-task   whether applied to all tasks
      -h, --help       help for stop

詳しい使用方法については[`dmctl validation start`](#method-2-enable-using-dmctl)を参照してください。

## 継続的なデータ検証のカットオーバーポイントを設定する {#set-the-cutover-point-for-continuous-data-validation}

アプリケーションを別のデータベースに切り替える前に、データが特定の位置に複製された直後に継続的なデータ検証を実行し、データの整合性を確保する必要がある場合があります。これを実現するには、この特定の位置を継続的検証の切り替えポイントとして設定します。

継続的なデータ検証のカットオーバー ポイントを設定するには、 `validation update`コマンドを使用します。

    Usage:
      dmctl validation update <task-name> [flags]

    Flags:
          --cutover-binlog-gtid string   specify the cutover binlog gtid for validation, only valid when source config's gtid is enabled, e.g. '1642618e-cf65-11ec-9e3d-0242ac110002:1-30'
          --cutover-binlog-pos string    specify the cutover binlog name for validation, should include binlog name and pos in brackets, e.g. '(mysql-bin.000001, 5989)'
      -h, --help                         help for update

-   `--cutover-binlog-gtid` : 検証のカットオーバー位置を`1642618e-cf65-11ec-9e3d-0242ac110002:1-30`形式で指定します。アップストリームクラスターでGTIDが有効になっている場合にのみ有効です。
-   `--cutover-binlog-pos` : 検証のカットオーバー位置を`(mysql-bin.000001, 5989)`形式で指定します。
-   `task-name` : 継続的データ検証タスクの名前。このパラメータは**必須**です。

## 実装 {#implementation}

DM における継続的なデータ検証 (バリデータ) のアーキテクチャは次のとおりです。

![validator summary](/media/dm/dm-validator-summary.jpeg)

継続的なデータ検証のライフサイクルは次のとおりです。

![validator lifecycle](/media/dm/dm-validator-lifecycle.jpeg)

継続的なデータ検証の詳細な実装は次のとおりです。

1.  バリデーターはアップストリームからbinlogイベントをプルし、変更された行を取得します。
    -   バリデータは、シンカーによって増分移行されたイベントのみをチェックします。イベントがシンカーによって処理されていない場合、バリデータは一時停止し、シンカーによる処理が完了するまで待機します。
    -   イベントがシンカーによって処理された場合、バリデーターは次の手順に進みます。
2.  バリデータはbinlogイベントを解析し、ブロックリストと許可リスト、テーブルフィルター、テーブルルーティングに基づいて行をフィルタリングします。その後、バリデータは変更された行をバックグラウンドで実行される検証ワーカーに送信します。
3.  検証ワーカーは、同じテーブルと同じ主キーに影響する変更された行をマージし、「期限切れ」データの検証を回避します。変更された行はメモリにキャッシュされます。
4.  検証ワーカーは、変更された行が一定数蓄積されるか、一定の時間間隔が経過すると、主キーを使用して下流のデータベースを照会し、現在のデータを取得して、変更された行と比較します。
5.  検証ワーカーはデータ検証を実行します。検証モードが`full`の場合、検証ワーカーは変更された行のデータを下流データベースのデータと比較します。検証モードが`fast`場合、検証ワーカーは変更された行の存在のみを確認します。
    -   変更された行が検証に合格した場合、変更された行はメモリから削除されます。
    -   変更された行が検証に失敗した場合、検証機能はすぐにエラーを報告せず、一定の時間間隔を待ってから行を再度検証します。
    -   変更された行が指定時間（ユーザーが指定）内に検証に合格できない場合、バリデータはその行をエラー行としてマークし、下流のメタデータデータベースに書き込みます。エラー行の情報は、移行タスクにクエリを実行することで確認できます。詳細は、 [検証ステータスをビュー](#view-the-validation-status)と[エラー行を処理する](#handle-error-rows)を参照してください。

## 制限事項 {#limitations}

-   検証するソース テーブルには、主キーまたは null 以外の一意のキーが必要です。
-   DM がアップストリーム データベースから DDL を移行する場合、次の制限が適用されます。
    -   DDL では、主キーを変更したり、列の順序を変更したり、既存の列を削除したりしてはなりません。
    -   テーブルを削除しないでください。
-   式を使用してイベントをフィルタリングするタスクはサポートされません。
-   TiDBとMySQLでは浮動小数点数の精度が異なります。10^-6未満の差は同等とみなされます。
-   次のデータ型はサポートされていません。
    -   JSON
    -   バイナリデータ
