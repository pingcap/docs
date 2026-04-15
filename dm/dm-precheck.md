---
title: Migration Task Precheck
summary: DMが移行タスクを開始する前に実行する事前チェックについて学びましょう。
---

# 移行タスクの事前チェック {#migration-task-precheck}

DMを使用してアップストリームからダウンストリームへデータを移行する前に、事前チェックを行うことで、アップストリームデータベースの設定エラーを検出し、移行がスムーズに行われることを確認できます。このドキュメントでは、DMの事前チェック機能について、使用シナリオ、チェック項目、引数を含めて説明します。

## 使用シナリオ {#usage-scenario}

データ移行タスクをスムーズに実行するために、DMはタスク開始時に自動的に事前チェックを実行し、その結果を返します。DMは事前チェックに合格した後にのみ移行を開始します。

手動で事前チェ​​ックをトリガーするには、 `check-task`コマンドを実行します。

例えば：

```bash
tiup dmctl check-task ./task.yaml
```

## チェック項目の説明 {#descriptions-of-check-items}

タスクの事前チェックがトリガーされると、DMは移行モードの設定に従って対応する項目をチェックします。

このセクションには、事前チェック項目がすべて記載されています。

> **注記：**
>
> この文書では、必ず合格しなければならないチェック項目には「（必須）」というラベルが付いています。

> -   必須チェック項目に合格しなかった場合、DM はチェック後にエラーを返し、移行タスクを続行しません。この場合、エラーメッセージに従って設定を変更し、事前チェック要件を満たした後にタスクを再試行してください。
>
> -   必須ではないチェック項目が合格しなかった場合、DM はチェック後に警告を返します。チェック結果に警告のみでエラーがない場合、DM は自動的に移行タスクを開始します。

### 一般的なチェック項目 {#common-check-items}

移行モードの選択に関わらず、事前チェックには必ず以下の共通チェック項目が含まれます。

-   データベースバージョン

    -   MySQLバージョン &gt; 5.5

    -   MariaDB バージョン &gt;= 10.1.2

    > **警告：**
    >
    > -   DMを使用してMySQL 8.0からTiDBへデータを移行する機能は、実験的機能です（DM v2.0以降で導入されました）。本番環境での使用は推奨されません。
    > -   MariaDBからTiDBへのデータ移行にDMを使用する機能は実験的機能です。本番環境での使用は推奨されません。

-   アップストリームのMySQLテーブルスキーマの互換性

    -   アップストリームテーブルに外部キーがあるかどうかを確認してください。TiDBは外部キーをサポートしています（v8.5.0以降でGA）。また、DMはv8.5.6以降、外部キー制約を持つテーブルのレプリケーションを実験的にサポートしています。事前チェック中に、外部キーが検出された場合、DMは警告を返します。サポートされているシナリオと制限事項については、 [DM互換性カタログ](/dm/dm-compatibility-catalog.md#foreign-key-cascade-operations)参照してください。 .

    -   上流のテーブルで TiDB と互換性のない文字セットが使用されていないか確認してください。詳細については、 [TiDBでサポートされている文字セット](/character-set-and-collation.md)参照してください。

    -   上流テーブルに主キー制約または一意キー制約（v1.0.7以降で導入）があるかどうかを確認します。

    > **警告：**
    >
    > -   アップストリームで互換性のない文字セットが使用されている場合でも、ダウンストリームでutf8mb4文字セットを使用してテーブルを作成することで、レプリケーションを続行できます。ただし、この方法は推奨されません。アップストリームで使用されている互換性のない文字セットを、ダウンストリームでサポートされている別の文字セットに置き換えることをお勧めします。
    > -   上流テーブルに主キー制約または一意キー制約がない場合、同じデータ行が下流テーブルに複数回複製される可能性があり、レプリケーションのパフォーマンスに影響を与える可能性があります。本番環境では、上流テーブルに主キー制約または一意キー制約を指定することをお勧めします。

### 完全なデータ移行のためのチェック項目 {#check-items-for-full-data-migration}

完全データ移行モード ( `task-mode: full` ) の場合、事前チェックには[一般的なチェック項目](#common-check-items)に加えて、次のチェック項目も含まれます。

-   上流データベースのダンプ権限（必須）

    -   INFORMATION_SCHEMAに対するSELECT権限とダンプテーブル
    -   `consistency=flush`の場合、再読み込みの権限が必要です。
    -   `consistency=flush/lock`の場合、ダンプ テーブルに対する LOCK TABLES 権限

-   （必須）上流のMySQLマルチインスタンスシャーディングテーブルの一貫性

    -   悲観的モードでは、シャーディングされたすべてのテーブルのテーブルスキーマが以下の項目で一貫しているかどうかを確認します。

        -   列数
        -   カラム名
        -   カラムの順序
        -   カラムタイプ
        -   主キー
        -   一意のインデックス

    -   楽観的モードでは、すべてのシャードテーブルのスキーマが[楽観的相性](https://github.com/pingcap/tiflow/blob/release-8.5/dm/docs/RFCS/20191209_optimistic_ddl.md#modifying-column-types)を満たしているかどうかを確認します。

    -   `start-task`コマンドによって移行タスクが正常に開始された場合、このタスクの事前チェックでは整合性チェックがスキップされます。

-   シャーディングされたテーブルで主キーを自動インクリメントする

    -   シャードテーブルに自動インクリメント主キーがある場合、事前チェックにより警告が返されます。自動インクリメント主キーに競合がある場合の解決策については、 [自動インクリメント主キーの競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)参照してください。

#### 物理的に輸入する品目を確認してください {#check-items-for-physical-import}

タスク設定で`import-mode: "physical"`を設定した場合、 [物理的な輸入](/tidb-lightning/tidb-lightning-physical-import-mode.md)が正常に実行されることを確認するための以下のチェック項目が追加されます。指示に従っても、これらのチェック項目の要件を満たすことが難しい場合は、 [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)を使用してデータをインポートしてみてください。

-   下流データベース内の空の領域

    -   空のリージョンの数が`max(1000, 3 * the number of tables)` (「1000」と「テーブル数の 3 倍」の大きい方) より大きい場合、事前チェックは警告を返します。関連する PD パラメータを調整して、空のリージョンの結合を高速化し、空のリージョンの数が減少するのを待つことができます。 [PDスケジューリングのベストプラクティス - 低速リージョンマージ](/best-practices/pd-scheduling-best-practices.md#region-merge-is-slow)を参照。

-   下流データベースにおけるリージョン分布

    -   さまざまな TiKV ノード上のリージョンの数を確認します。リージョン数が最も少ない TiKV ノードに`a`個のリージョンがあり、リージョン数が最も多い TiKV ノードに`b`個のリージョンがあると仮定すると、 `a / b` 0.75 未満の場合、事前チェックは警告を返します。関連する PD パラメータを調整して、リージョンのスケジュールを高速化し、リージョンの数が変更されるのを待つことができます。 [PDスケジューリングのベストプラクティス -Leader/リージョンの配分がバランスが取れていない](/best-practices/pd-scheduling-best-practices.md#leadersregions-are-not-evenly-distributed)参照。

-   下流データベースにおけるTiDB、PD、およびTiKVのバージョン

    -   物理インポートでは、TiDB、PD、およびTiKVのインターフェースを呼び出す必要があります。バージョンに互換性がない場合、事前チェックでエラーが返されます。

-   下流データベースの空き容量

    -   上流データベース ( `source_size` ) の許可リストにあるすべてのテーブルの合計サイズを推定します。下流データベースの空き容量が`source_size`より少ない場合、事前チェックはエラーを返します。下流データベースの空き容量が TiKV レプリカの数 * `source_size` * 2 より少ない場合、事前チェックは警告を返します。

-   下流のデータベースが物理インポートと互換性のないタスクを実行しているかどうか

    -   現在、物理インポートは[TiCDC](/ticdc/ticdc-overview.md)および[PITR](/br/br-pitr-guide.md)タスクと互換性がありません。これらのタスクが下流データベースで実行されている場合、事前チェックでエラーが発生します。

### 増分データ移行のチェック項目 {#check-items-for-incremental-data-migration}

増分データ移行モード ( `task-mode: incremental` ) の場合、事前チェックには[一般的なチェック項目](#common-check-items)に加えて、次のチェック項目も含まれます。

-   （必須）上流データベースのレプリケーション権限

    -   レプリケーションクライアントの権限
    -   レプリケーションスレーブのアクセス許可

-   データベースのプライマリ/セカンダリ構成

    -   プライマリ/セカンダリレプリケーションの障害を回避するため、アップストリームデータベースにデータベースID `server_id`を指定することをお勧めします（AWS Aurora以外の環境ではGTIDの使用をお勧めします）。

-   （必須）MySQLbinlogの設定

    -   binlogが有効になっているか確認してください（DMで必須）。
    -   `binlog_format=ROW`が設定されているかどうかを確認してください（DMはROW形式のbinlogの移行のみをサポートしています）。
    -   `binlog_row_image=FULL`が設定されているかどうかを確認してください (DM は`binlog_row_image=FULL`のみをサポートしています)。
    -   `binlog_transaction_compression=OFF`が設定されているかどうかを確認してください (DM はトランザクション圧縮をサポートしていません)。
    -   `binlog_do_db`または`binlog_ignore_db`が設定されている場合は、移行対象のデータベース テーブルが`binlog_do_db`および`binlog_ignore_db`の条件を満たしているかどうかを確認します。

-   （必須）上流データベースが[オンラインDDL](/dm/feature-online-ddl.md)プロセス中かどうかを確認します（ `ghost`テーブルは作成されていますが、 `rename`フェーズはまだ実行されていません）。上流データベースがオンラインDDLプロセス中の場合、事前チェックでエラーが返されます。この場合、DDLが完了するまで待ってから再試行してください。

### 完全データ移行および増分データ移行のチェック項目 {#check-items-for-full-and-incremental-data-migration}

完全および増分データ移行モード ( `task-mode: all` ) の場合、事前チェックには[一般的なチェック項目](#common-check-items)に加えて、[完全なデータ移行チェック項目](#check-items-for-full-data-migration)と[増分データ移行チェック項目](#check-items-for-incremental-data-migration)も含まれます。

### 無視できるチェック項目 {#ignorable-check-items}

事前チェックでは、環境内の潜在的なリスクを検出できます。チェック項目を無視することは推奨されません。データ移行タスクに特別な要件がある場合は、 [`ignore-checking-items`設定項目](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)を使用して一部のチェック項目をスキップできます。

| チェック項目                      | 説明                                                              |
| :-------------------------- | :-------------------------------------------------------------- |
| `dump_privilege`            | 上流のMySQLインスタンスにおけるユーザーのダンプ権限を確認します。                             |
| `replication_privilege`     | 上流のMySQLインスタンスにおけるユーザーのレプリケーション権限を確認します。                        |
| `version`                   | 上流データベースのバージョンを確認します。                                           |
| `server_id`                 | 上流データベースにserver_idが設定されているかどうかを確認します。                           |
| `binlog_enable`             | アップストリームデータベースでbinlogが有効になっているかどうかを確認します。                       |
| `table_schema`              | 上流のMySQLテーブルにおけるテーブルスキーマの互換性を確認します。                             |
| `schema_of_shard_tables`    | アップストリームのMySQLマルチインスタンスシャードにおけるテーブルスキーマの一貫性をチェックします。            |
| `auto_increment_ID`         | 上流のMySQLマルチインスタンスシャードにおいて、自動インクリメント主キーの競合が発生していないかを確認します。       |
| `online_ddl`                | アップストリームが[オンラインDDL](/dm/feature-online-ddl.md)のプロセス中かどうかを確認します。 |
| `empty_region`              | 物理インポート先のダウンストリームデータベースにおける空のリージョンの数をチェックします。                   |
| `region_distribution`       | 物理インポートのために、下流データベースにおけるリージョンの分布を確認します。                         |
| `downstream_version`        | 下流データベース内のTiDB、PD、およびTiKVのバージョンを確認します。                          |
| `free_space`                | 下流データベースの空き容量を確認します。                                            |
| `downstream_mutex_features` | 下流のデータベースで、物理インポートと互換性のないタスクが実行されていないかを確認します。                   |

> **注記：**
>
> バージョン6.0より前のバージョンでは、無視可能なチェック項目がより多くサポートされていました。しかし、バージョン6.0以降では、データセキュリティに関連する一部のチェック項目を無視することはDMでは許可されていません。例えば、 `binlog_row_image`パラメータを誤って設定すると、レプリケーション中にデータが失われる可能性があります。

## 事前チェック引数を設定する {#configure-precheck-arguments}

移行タスクの事前チェックは並列処理に対応しています。シャーディングされたテーブルの行数が100万行に達しても、事前チェックは数分で完了します。

事前チェックのスレッド数を指定するには、移行タスク構成ファイルの`threads`フィールドの`mydumpers`引数を設定します。

```yaml
mydumpers:                           # Configuration arguments of the dump processing unit
  global:                            # Configuration name
    threads: 4                       # The number of threads that access the upstream when the dump processing unit performs the precheck and exports data from the upstream database (4 by default)
    chunk-filesize: 64               # The size of the files generated by the dump processing unit (64 MB by default)
    extra-args: "--consistency auto" # Other arguments of the dump processing unit. You do not need to manually configure table-list in `extra-args`, because it is automatically generated by DM.

```

> **注記：**
>
> `threads`の値は、アップストリームデータベースと DM 間の物理接続数を決定します。 `threads`値が大きすぎると、アップストリームの負荷が増加する可能性があります。そのため、 `threads`適切な値に設定する必要があります。
