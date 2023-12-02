---
title: Migration Task Precheck
summary: Learn the precheck that DM performs before starting a migration task.
---

# 移行タスクの事前チェック {#migration-task-precheck}

DM を使用してアップストリームからダウンストリームにデータを移行する前に、事前チェックによりアップストリームのデータベース構成のエラーを検出し、移行がスムーズに行われるようにします。本書では、DMの事前チェック機能について、利用シーン、チェック項目、引数などを含めて紹介します。

## 利用シーン {#usage-scenario}

データ移行タスクをスムーズに実行するために、DM はタスクの開始時に事前チェックを自動的にトリガーし、チェック結果を返します。 DM は、事前チェックに合格した後にのみ移行を開始します。

事前チェックを手動でトリガーするには、 `check-task`コマンドを実行します。

例えば：

```bash
tiup dmctl check-task ./task.yaml
```

## チェック項目の説明 {#descriptions-of-check-items}

タスクの事前チェックがトリガーされると、DM は移行モードの設定に従って対応する項目をチェックします。

このセクションでは、すべての事前チェック項目をリストします。

> **注記：**
>
> 本書では必ず通過しなければならないチェック項目を「(必須)」と表記しています。

> -   必須のチェック項目に合格しない場合、DM はチェック後にエラーを返し、移行タスクは続行されません。この場合、エラー メッセージに従って構成を変更し、事前チェック要件を満たした後でタスクを再試行します。
>
> -   必須ではないチェック項目が不合格の場合、DM はチェック後に警告を返します。チェック結果に警告のみが含まれ、エラーが含まれていない場合、DM は自動的に移行タスクを開始します。

### よくあるチェック項目 {#common-check-items}

選択した移行モードに関係なく、事前チェックには常に次の共通チェック項目が含まれます。

-   データベースのバージョン

    -   MySQL バージョン &gt; 5.5

    -   MariaDB バージョン &gt;= 10.1.2

    > **警告：**
    >
    > -   DM を使用した MySQL 8.0 から TiDB へのデータの移行は実験的機能です (DM v2.0 以降に導入されました)。本番環境で使用することはお勧めできません。
    > -   DM を使用した MariaDB から TiDB へのデータの移行は実験的機能です。本番環境で使用することはお勧めできません。

-   アップストリーム MySQL テーブル スキーマの互換性

    -   上流テーブルに TiDB でサポートされていない外部キーがあるかどうかを確認します。事前チェックで外部キーが見つかった場合は、警告が返されます。

    -   上流のテーブルで TiDB と互換性のない文字セットが使用されていないか確認してください。詳細については、 [TiDB でサポートされる文字セット](/character-set-and-collation.md)を参照してください。

    -   上流テーブルに主キー制約または一意キー制約 (v1.0.7 から導入) があるかどうかを確認します。

    > **警告：**
    >
    > -   アップストリームで互換性のない文字セットが使用されている場合でも、ダウンストリームで utf8mb4 文字セットを使用してテーブルを作成することでレプリケーションを続行できます。ただし、この方法はお勧めできません。アップストリームで使用されている互換性のない文字セットを、ダウンストリームでサポートされている別の文字セットに置き換えることをお勧めします。
    > -   アップストリームのテーブルに主キー制約や一意キー制約がない場合、同じデータ行がダウンストリームに複数回レプリケートされる可能性があり、レプリケーションのパフォーマンスにも影響を与える可能性があります。本番環境では、上流テーブルに主キー制約または一意キー制約を指定することをお勧めします。

### 完全データ移行のチェック項目 {#check-items-for-full-data-migration}

完全データ移行モード ( `task-mode: full` ) の場合、事前チェックには[よくあるチェック項目](#common-check-items)に加えて、次のチェック項目も含まれます。

-   上流データベースのダンプ権限 (必須)

    -   INFORMATION_SCHEMA およびダンプ テーブルに対する SELECT 権限
    -   RELOAD 許可 ( `consistency=flush`の場合)
    -   ダンプ テーブルに対する LOCK TABLES 権限 ( `consistency=flush/lock`の場合)

-   (必須) アップストリーム MySQL マルチインスタンス シャーディング テーブルの一貫性

    -   悲観的モードでは、すべてのシャードテーブルのテーブルスキーマが次の項目で一貫しているかどうかを確認します。

        -   列の数
        -   カラム名
        -   カラムの順序
        -   カラムの種類
        -   主キー
        -   一意のインデックス

    -   楽観的モードでは、すべてのシャード テーブルのスキーマが[楽観的互換性](https://github.com/pingcap/tiflow/blob/release-7.5/dm/docs/RFCS/20191209_optimistic_ddl.md#modifying-column-types)を満たすかどうかを確認します。

    -   移行タスクが`start-task`コマンドによって正常に開始された場合、このタスクの事前チェックでは整合性チェックがスキップされます。

-   シャードテーブルの主キーの自動インクリメント

    -   シャードテーブルに自動インクリメント主キーがある場合、事前チェックにより警告が返されます。自動インクリメント主キーに競合がある場合、解決策については[自動インクリメント主キーの競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照してください。

#### 現物輸入のチェック項目 {#check-items-for-physical-import}

タスク構成で`import-mode: "physical"`を設定した場合、 [物理的なインポート](/tidb-lightning/tidb-lightning-physical-import-mode.md)正常に動作することを確認するために以下のチェック項目が追加されます。指示に従っても、これらのチェック項目の要件を満たすことが難しい場合は、 [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)を使用してデータをインポートしてみてください。

-   ダウンストリーム データベース内の空の領域

    -   空のリージョンの数が`max(1000, 3 * the number of tables)` (「1000」と「テーブル数の 3 倍」の大きい方) より大きい場合、事前チェックは警告を返します。関連する PD パラメータを調整して、空のリージョンの結合を高速化し、空のリージョンの数が減少するのを待つことができます。 [PD スケジュールのベスト プラクティス - 低速なリージョンマージ](/best-practices/pd-scheduling-best-practices.md#region-merge-is-slow)を参照してください。

-   ダウンストリームデータベースのリージョン分布

    -   さまざまな TiKV ノード上のリージョンの数を確認します。リージョン数が最も低い TiKV ノードにリージョンが`a`つあり、リージョン数が最も高い TiKV ノードに`b`のリージョンがあると仮定すると、 `a / b`が 0.75 未満の場合、事前チェックは警告を返します。関連する PD パラメータを調整して、リージョンのスケジュールを高速化し、リージョンの数が変更されるのを待つことができます。 [PD スケジュールのベスト プラクティス -Leader/リージョンの分散のバランスが取れていません](/best-practices/pd-scheduling-best-practices.md#leadersregions-are-not-evenly-distributed)を参照してください。

-   ダウンストリーム データベース内の TiDB、PD、および TiKV のバージョン

    -   物理インポートでは、TiDB、PD、および TiKV のインターフェイスを呼び出す必要があります。バージョンに互換性がない場合、事前チェックはエラーを返します。

-   ダウンストリームデータベースの空き容量

    -   アップストリーム データベースの許可リスト内のすべてのテーブルの合計サイズを推定します ( `source_size` )。ダウンストリーム データベースの空き領域が`source_size`未満の場合、事前チェックはエラーを返します。ダウンストリーム データベースの空き領域が TiKV レプリカの数 * `source_size` * 2 未満の場合、事前チェックにより警告が返されます。

-   ダウンストリーム データベースが物理インポートと互換性のないタスクを実行しているかどうか

    -   現在、物理インポートは[TiCDC](/ticdc/ticdc-overview.md)および[PITR](/br/br-pitr-guide.md)タスクと互換性がありません。これらのタスクがダウンストリーム データベースで実行されている場合、事前チェックはエラーを返します。

### 増分データ移行のチェック項目 {#check-items-for-incremental-data-migration}

増分データ移行モード ( `task-mode: incremental` ) の場合、事前チェックには[よくあるチェック項目](#common-check-items)に加えて、次のチェック項目も含まれます。

-   (必須) アップストリーム データベース REPLICATION 権限

    -   レプリケーションクライアント権限
    -   レプリケーションスレーブ権限

-   データベースのプライマリ-セカンダリ構成

    -   プライマリとセカンダリのレプリケーションの失敗を回避するには、アップストリーム データベースにデータベース ID `server_id`を指定することをお勧めします (非 AWS Aurora環境には GTID が推奨されます)。

-   (必須) MySQLbinlog設定

    -   binlogが有効になっているかどうかを確認します (DM で必要)。
    -   `binlog_format=ROW`が設定されているかどうかを確認します (DM は ROW 形式のbinlogの移行のみをサポートします)。
    -   `binlog_row_image=FULL`が構成されているかどうかを確認します (DM は`binlog_row_image=FULL`のみをサポートします)。
    -   `binlog_do_db`または`binlog_ignore_db`が設定されている場合、移行するデータベーステーブルが`binlog_do_db`および`binlog_ignore_db`の条件を満たしているか確認してください。

-   (必須) 上流データベースが[オンライン DDL](/dm/feature-online-ddl.md)プロセス ( `ghost`テーブルは作成されているが、 `rename`フェーズがまだ実行されていないプロセス) にあるかどうかを確認します。アップストリームがオンライン DDL プロセスにある場合、事前チェックはエラーを返します。この場合、DDL が完了するまで待ってから再試行してください。

### 完全データ移行および増分データ移行のチェック項目 {#check-items-for-full-and-incremental-data-migration}

完全および増分データ移行モード ( `task-mode: all` ) の場合、事前チェックには[よくあるチェック項目](#common-check-items)に加えて[完全なデータ移行チェック項目](#check-items-for-full-data-migration)および[増分データ移行のチェック項目](#check-items-for-incremental-data-migration)も含まれます。

### 無視できるチェック項目 {#ignorable-check-items}

事前チェックにより、環境内の潜在的なリスクを見つけることができます。チェック項目を無視することはお勧めできません。データ移行タスクに特別なニーズがある場合は、「 [`ignore-checking-items`設定項目](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)を使用して一部のチェック項目をスキップできます。

| チェック項目                      | 説明                                                          |
| :-------------------------- | :---------------------------------------------------------- |
| `dump_privilege`            | 上流の MySQL インスタンスのユーザーのダンプ権限を確認します。                          |
| `replication_privilege`     | 上流の MySQL インスタンスのユーザーのレプリケーション権限を確認します。                     |
| `version`                   | 上流データベースのバージョンを確認します。                                       |
| `server_id`                 | server_id がアップストリーム データベースで構成されているかどうかを確認します。               |
| `binlog_enable`             | アップストリーム データベースでbinlogが有効になっているかどうかを確認します。                  |
| `table_schema`              | アップストリームの MySQL テーブル内のテーブル スキーマの互換性をチェックします。                |
| `schema_of_shard_tables`    | アップストリームの MySQL マルチインスタンス シャード内のテーブル スキーマの一貫性をチェックします。      |
| `auto_increment_ID`         | 自動インクリメント主キーがアップストリームの MySQL マルチインスタンス シャードで競合するかどうかを確認します。 |
| `online_ddl`                | 上流が[オンライン DDL](/dm/feature-online-ddl.md)のプロセス中かどうかを確認します。  |
| `empty_region`              | 物理インポート用にダウンストリーム データベース内の空のリージョンの数を確認します。                  |
| `region_distribution`       | 物理インポートのダウンストリーム データベース内のリージョンの分布を確認します。                    |
| `downstream_version`        | ダウンストリーム データベース内の TiDB、PD、および TiKV のバージョンを確認します。            |
| `free_space`                | ダウンストリームデータベースの空き容量を確認します。                                  |
| `downstream_mutex_features` | ダウンストリーム データベースが物理インポートと互換性のないタスクを実行していないかどうかを確認します。        |

> **注記：**
>
> v6.0 より前のバージョンでは、さらに無視できるチェック項目がサポートされています。 v6.0 以降、DM ではデータの安全性に関連する一部のチェック項目を無視することができません。たとえば、 `binlog_row_image`パラメータを誤って構成すると、レプリケーション中にデータが失われる可能性があります。

## 事前チェック引数を構成する {#configure-precheck-arguments}

移行タスクの事前チェックは、並列処理をサポートします。シャードテーブルの行数が 100 万レベルに達した場合でも、事前チェックは数分で完了できます。

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
> 値`threads`により、アップストリーム データベースと DM の間の物理接続の数が決まります。 `threads`値が大きすぎると、上流の負荷が増加する可能性があります。したがって、 `threads`適切な値に設定する必要があります。
