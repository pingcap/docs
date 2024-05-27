---
title: Migration Task Precheck
summary: 移行タスクを開始する前に DM が実行する事前チェックについて説明します。
---

# 移行タスクの事前チェック {#migration-task-precheck}

DM を使用してアップストリームからダウンストリームにデータを移行する前に、事前チェックを行うことでアップストリーム データベース構成のエラーを検出し、移行がスムーズに進むようにします。このドキュメントでは、DM 事前チェック機能について、その使用シナリオ、チェック項目、引数などを紹介します。

## 使用シナリオ {#usage-scenario}

データ移行タスクをスムーズに実行するために、DM はタスクの開始時に自動的に事前チェックをトリガーし、チェック結果を返します。DM は、事前チェックに合格した後にのみ移行を開始します。

事前チェックを手動でトリガーするには、 `check-task`コマンドを実行します。

例えば：

```bash
tiup dmctl check-task ./task.yaml
```

## チェック項目の説明 {#descriptions-of-check-items}

タスクの事前チェックがトリガーされると、DM は移行モードの構成に従って対応する項目をチェックします。

このセクションでは、すべての事前チェック項目をリストします。

> **注記：**
>
> このドキュメントでは、必ず合格しなければならないチェック項目には「(必須)」というラベルが付いています。

> -   必須チェック項目に合格しなかった場合、DM はチェック後にエラーを返し、移行タスクを続行しません。この場合、エラー メッセージに従って構成を変更し、事前チェックの要件を満たした後にタスクを再試行してください。
>
> -   必須ではないチェック項目に合格しなかった場合、DM はチェック後に警告を返します。チェック結果に警告のみが含まれ、エラーが含まれていない場合、DM は自動的に移行タスクを開始します。

### 共通チェック項目 {#common-check-items}

選択した移行モードに関係なく、事前チェックには常に次の共通チェック項目が含まれます。

-   データベースバージョン

    -   MySQL バージョン &gt; 5.5

    -   MariaDB バージョン &gt;= 10.1.2

    > **警告：**
    >
    > -   DM を使用して MySQL 8.0 から TiDB にデータを移行することは、実験的機能です (DM v2.0 以降で導入)。本番環境での使用は推奨されません。
    > -   DM を使用して MariaDB から TiDB にデータを移行することは実験的機能です。本番環境での使用はお勧めしません。

-   アップストリームMySQLテーブルスキーマの互換性

    -   アップストリーム テーブルに、TiDB でサポートされていない外部キーがあるかどうかを確認します。事前チェックで外部キーが見つかった場合は、警告が返されます。

    -   アップストリーム テーブルが TiDB と互換性のない文字セットを使用していないかどうかを確認します。詳細については、 [TiDB でサポートされる文字セット](/character-set-and-collation.md)参照してください。

    -   アップストリーム テーブルに主キー制約または一意キー制約 (v1.0.7 から導入) があるかどうかを確認します。

    > **警告：**
    >
    > -   アップストリームで互換性のない文字セットが使用されている場合でも、ダウンストリームで utf8mb4 文字セットを使用してテーブルを作成することで、レプリケーションを続行できます。ただし、この方法はお勧めしません。アップストリームで使用されている互換性のない文字セットを、ダウンストリームでサポートされている別の文字セットに置き換えることをお勧めします。
    > -   アップストリーム テーブルに主キー制約または一意キー制約がない場合、同じデータ行がダウンストリームに複数回レプリケートされる可能性があり、これもレプリケーションのパフォーマンスに影響する可能性があります。本番環境では、アップストリーム テーブルに主キー制約または一意キー制約を指定することをお勧めします。

### 完全なデータ移行のためのチェック項目 {#check-items-for-full-data-migration}

完全データ移行モード（ `task-mode: full` ）の場合、 [共通チェック項目](#common-check-items)に加えて、事前チェックには以下のチェック項目も含まれます。

-   (必須) アップストリームデータベースのダンプ権限

    -   INFORMATION_SCHEMA およびダンプ テーブルに対する SELECT 権限
    -   RELOAD権限が`consistency=flush`場合
    -   ダンプテーブルに対するLOCK TABLES権限`consistency=flush/lock`場合）

-   (必須) アップストリーム MySQL マルチインスタンス シャーディング テーブルの一貫性

    -   悲観的モードでは、すべてのシャード テーブルのテーブル スキーマが次の項目で一貫しているかどうかを確認します。

        -   列の数
        -   カラム名
        -   カラムの順序
        -   カラムタイプ
        -   主キー
        -   ユニークインデックス

    -   楽観的モードでは、すべてのシャード テーブルのスキーマが[楽観的互換性](https://github.com/pingcap/tiflow/blob/release-8.1/dm/docs/RFCS/20191209_optimistic_ddl.md#modifying-column-types)満たしているかどうかを確認します。

    -   移行タスクが`start-task`コマンドによって正常に開始された場合、このタスクの事前チェックでは整合性チェックがスキップされます。

-   シャードテーブル内の主キーの自動増分

    -   シャード テーブルに自動増分主キーがある場合、事前チェックは警告を返します。自動増分主キーに競合がある場合は、解決策については[自動増分主キーの競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照してください。

#### 物理的な輸入のためのアイテムを確認する {#check-items-for-physical-import}

タスク構成で`import-mode: "physical"`設定すると、 [物理的な輸入](/tidb-lightning/tidb-lightning-physical-import-mode.md)正常に実行されることを確認するために、次のチェック項目が追加されます。プロンプトに従った後、これらのチェック項目の要件を満たすのが難しい場合は、 [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)を使用してデータをインポートしてみてください。

-   下流データベースの空の領域

    -   空のリージョンの数が`max(1000, 3 * the number of tables)` (「1000」と「テーブル数の 3 倍」のうち大きい方) より大きい場合、事前チェックは警告を返します。関連する PD パラメータを調整して、空のリージョンのマージを高速化し、空のリージョンの数が減少するのを待つことができます。3 [PD スケジューリングのベスト プラクティス - 低速リージョンのマージ](/best-practices/pd-scheduling-best-practices.md#region-merge-is-slow)参照してください。

-   下流データベースにおけるリージョン分布

    -   異なる TiKV ノード上のリージョンの数をチェックします。リージョン数が最も少ない TiKV ノードには`a`リージョンがあり、リージョン数が最も多い TiKV ノードには`b`リージョンがあると仮定すると、 `a / b`が 0.75 未満の場合、事前チェックは警告を返します。関連する PD パラメータを調整してリージョンのスケジュールを高速化し、リージョン数が変化するのを待つことができます。7 [PD スケジューリングのベスト プラクティス -Leader/リージョンの配分がバランスが取れていない](/best-practices/pd-scheduling-best-practices.md#leadersregions-are-not-evenly-distributed)参照してください。

-   下流データベースのTiDB、PD、およびTiKVのバージョン

    -   物理インポートでは、TiDB、PD、および TiKV のインターフェースを呼び出す必要があります。バージョンに互換性がない場合、事前チェックでエラーが返されます。

-   下流データベースの空き容量

    -   アップストリーム データベースの許可リストにあるすべてのテーブルの合計サイズを推定します ( `source_size` )。ダウンストリーム データベースの空き容量が`source_size`未満の場合、事前チェックはエラーを返します。ダウンストリーム データベースの空き容量が TiKV レプリカの数 * `source_size` * 2 未満の場合、事前チェックは警告を返します。

-   下流データベースが物理インポートと互換性のないタスクを実行しているかどうか

    -   現在、物理インポートはタスク[ティCDC](/ticdc/ticdc-overview.md)および[ピトル](/br/br-pitr-guide.md)と互換性がありません。これらのタスクがダウンストリーム データベースで実行されている場合、事前チェックはエラーを返します。

### 増分データ移行のチェック項目 {#check-items-for-incremental-data-migration}

増分データ移行モード（ `task-mode: incremental` ）の場合、 [共通チェック項目](#common-check-items)に加えて、事前チェックには次のチェック項目も含まれます。

-   (必須) 上流データベースのレプリケーション権限

    -   レプリケーションクライアント権限
    -   REPLICATION SLAVE 権限

-   データベースのプライマリ/セカンダリ構成

    -   プライマリ - セカンダリ レプリケーションの失敗を回避するには、アップストリーム データベースにデータベース ID `server_id`を指定することをお勧めします (AWS Aurora以外の環境では GTID が推奨されます)。

-   (必須) MySQL binlog設定

    -   binlogが有効になっているかどうかを確認します (DM で必要)。
    -   `binlog_format=ROW`が構成されているかどうかを確認します (DM は ROW 形式のbinlogの移行のみをサポートします)。
    -   `binlog_row_image=FULL`設定されているかどうかを確認します (DM は`binlog_row_image=FULL`のみをサポートします)。
    -   `binlog_do_db`または`binlog_ignore_db`が設定されている場合は、移行するデータベース テーブルが`binlog_do_db`および`binlog_ignore_db`の条件を満たしているかどうかを確認します。

-   (必須) アップストリーム データベースが[オンラインDDL](/dm/feature-online-ddl.md)プロセス ( `ghost`テーブルは作成されているが、 `rename`フェーズはまだ実行されていない) にあるかどうかを確認します。アップストリームがオンライン DDL プロセスにある場合、事前チェックでエラーが返されます。この場合、DDL が完了するまで待ってから再試行してください。

### 完全データ移行と増分データ移行のチェック項目 {#check-items-for-full-and-incremental-data-migration}

完全および増分データ移行モード（ `task-mode: all` ）の場合、事前チェックには[共通チェック項目](#common-check-items)に加えて[完全なデータ移行チェック項目](#check-items-for-full-data-migration)と[増分データ移行チェック項目](#check-items-for-incremental-data-migration)含まれます。

### 無視できるチェック項目 {#ignorable-check-items}

事前チェックにより、環境内の潜在的なリスクを見つけることができます。チェック項目を無視することはお勧めしません。データ移行タスクに特別なニーズがある場合は、 [`ignore-checking-items`設定項目](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)使用して一部のチェック項目をスキップできます。

| チェック項目                      | 説明                                                            |
| :-------------------------- | :------------------------------------------------------------ |
| `dump_privilege`            | アップストリーム MySQL インスタンス内のユーザーのダンプ権限をチェックします。                    |
| `replication_privilege`     | アップストリーム MySQL インスタンス内のユーザーのレプリケーション権限をチェックします。               |
| `version`                   | アップストリーム データベースのバージョンを確認します。                                  |
| `server_id`                 | server_id がアップストリーム データベースで設定されているかどうかを確認します。                 |
| `binlog_enable`             | アップストリーム データベースでbinlog が有効になっているかどうかを確認します。                   |
| `table_schema`              | アップストリーム MySQL テーブル内のテーブル スキーマの互換性をチェックします。                   |
| `schema_of_shard_tables`    | アップストリーム MySQL マルチインスタンス シャード内のテーブル スキーマの一貫性をチェックします。         |
| `auto_increment_ID`         | アップストリームの MySQL マルチインスタンス シャードで自動インクリメント主キーが競合するかどうかを確認します。   |
| `online_ddl`                | アップストリームが[オンラインDDL](/dm/feature-online-ddl.md)の処理中かどうかを確認します。 |
| `empty_region`              | 物理インポートのダウンストリーム データベース内の空の領域の数を確認します。                        |
| `region_distribution`       | 物理インポートのダウンストリーム データベース内のリージョンの分布を確認します。                      |
| `downstream_version`        | ダウンストリーム データベース内の TiDB、PD、および TiKV のバージョンを確認します。              |
| `free_space`                | ダウンストリーム データベースの空き領域を確認します。                                   |
| `downstream_mutex_features` | ダウンストリーム データベースが物理インポートと互換性のないタスクを実行しているかどうかを確認します。           |

> **注記：**
>
> 6.0 より前のバージョンでは、より多くの無視可能なチェック項目がサポートされています。6.0 以降、DM では、データの安全性に関連する一部のチェック項目を無視することはできません。たとえば、 `binlog_row_image`パラメータを誤って構成すると、レプリケーション中にデータが失われる可能性があります。

## 事前チェック引数を設定する {#configure-precheck-arguments}

移行タスクの事前チェックは並列処理をサポートしています。シャード化されたテーブルの行数が 100 万レベルに達した場合でも、事前チェックは数分で完了します。

事前チェックのスレッド数を指定するには、移行タスク構成ファイルの`mydumpers`フィールドの`threads`引数を構成できます。

```yaml
mydumpers:                           # Configuration arguments of the dump processing unit
  global:                            # Configuration name
    threads: 4                       # The number of threads that access the upstream when the dump processing unit performs the precheck and exports data from the upstream database (4 by default)
    chunk-filesize: 64               # The size of the files generated by the dump processing unit (64 MB by default)
    extra-args: "--consistency none" # Other arguments of the dump processing unit. You do not need to manually configure table-list in `extra-args`, because it is automatically generated by DM.

```

> **注記：**
>
> 値`threads`は、アップストリーム データベースと DM 間の物理接続の数を決定します。値が`threads`に大きすぎると、アップストリームの負荷が増加する可能性があります。したがって、適切な値に`threads`を設定する必要があります。
