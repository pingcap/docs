---
title: Migration Task Precheck
summary: Learn the precheck that DM performs before starting a migration task.
---

# 移行タスクの事前チェック {#migration-task-precheck}

DM を使用してアップストリームからダウンストリームにデータを移行する前に、事前チェックによりアップストリーム データベース構成のエラーを検出し、移行がスムーズに進むようにします。このドキュメントでは、DM 事前チェック機能について、その使用シナリオ、チェック項目、および引数を含めて紹介します。

## 利用シーン {#usage-scenario}

データ移行タスクをスムーズに実行するために、DM はタスクの開始時に事前チェックを自動的にトリガーし、チェック結果を返します。 DM は、事前チェックに合格した後にのみ移行を開始します。

事前チェックを手動でトリガーするには、 `check-task`コマンドを実行します。

例えば：

{{< copyable "" >}}

```bash
tiup dmctl check-task ./task.yaml
```

## チェック項目の説明 {#descriptions-of-check-items}

タスクの事前チェックがトリガーされた後、DM は、移行モードの構成に従って、対応するアイテムをチェックします。

このセクションには、すべての事前チェック項目がリストされています。

> **ノート：**
>
> 本書では、合格しなければならないチェック項目を「(必須)」と表記しています。

> -   必須のチェック項目に合格しない場合、DM はチェック後にエラーを返し、移行タスクを続行しません。この場合、エラー メッセージに従って構成を変更し、事前チェックの要件を満たしてからタスクを再試行してください。
>
> -   必須ではないチェック項目をパスしなかった場合、DM はチェック後に警告を返します。チェック結果に警告のみが含まれ、エラーが含まれていない場合、DM は移行タスクを自動的に開始します。

### 共通チェック項目 {#common-check-items}

選択した移行モードに関係なく、事前チェックには常に次の一般的なチェック項目が含まれます。

-   データベースのバージョン

    -   MySQL バージョン &gt; 5.5

    -   MariaDB バージョン &gt;= 10.1.2

    > **警告：**
    >
    > -   DM を使用した MySQL 8.0 から TiDB へのデータの移行は、実験的機能です (DM v2.0 以降に導入されました)。本番環境で使用することはお勧めしません。
    > -   DM を使用した MariaDB から TiDB へのデータの移行は、実験的機能です。本番環境で使用することはお勧めしません。

-   アップストリームの MySQL テーブル スキーマの互換性

    -   アップストリーム テーブルに、TiDB でサポートされていない外部キーがあるかどうかを確認します。事前チェックで外部キーが見つかった場合は、警告が返されます。

    -   アップストリーム テーブルが TiDB と互換性のない文字セットを使用しているかどうかを確認します。詳細については、 [TiDB がサポートする文字セット](/character-set-and-collation.md)を参照してください。

    -   上流のテーブルに主キー制約または一意キー制約 (v1.0.7 から導入) があるかどうかを確認します。

    > **警告：**
    >
    > -   アップストリームで互換性のない文字セットが使用されている場合でも、ダウンストリームで utf8mb4 文字セットを使用してテーブルを作成することにより、レプリケーションを続行できます。ただし、この方法はお勧めしません。アップストリームで使用されている互換性のない文字セットを、ダウンストリームでサポートされている別の文字セットに置き換えることをお勧めします。
    > -   アップストリーム テーブルに主キー制約または一意キー制約がない場合、同じデータ行がダウンストリームに複数回レプリケートされる可能性があり、これもレプリケーションのパフォーマンスに影響を与える可能性があります。本番環境では、上流のテーブルに主キー制約または一意キー制約を指定することをお勧めします。

### 完全データ移行のチェック項目 {#check-items-for-full-data-migration}

完全データ移行モード ( `task-mode: full` ) の場合、 [共通チェック項目](#common-check-items)に加えて、事前チェックには次のチェック項目も含まれます。

-   (必須) アップストリーム データベースのダンプ権限

    -   INFORMATION_SCHEMA およびダンプ テーブルに対する SELECT 権限
    -   `consistency=flush`の場合は RELOAD パーミッション
    -   `consistency=flush/lock`の場合、ダンプ テーブルに対する LOCK TABLES 権限

-   (必須) アップストリームの MySQL マルチインスタンス シャーディング テーブルの一貫性

    -   悲観的モードでは、すべてのシャード テーブルのテーブル スキーマが次の項目で一致しているかどうかを確認します。

        -   列の数
        -   カラム名
        -   カラムの順序
        -   カラムの種類
        -   主キー
        -   一意のインデックス

    -   楽観的モードで、すべてのシャード テーブルのスキーマが[楽観的互換性](https://github.com/pingcap/tiflow/blob/master/dm/docs/RFCS/20191209_optimistic_ddl.md#modifying-column-types)を満たすかどうかを確認します。

    -   移行タスクが`start-task`コマンドで正常に開始された場合、このタスクの事前チェックは整合性チェックをスキップします。

-   シャード テーブルの主キーの自動インクリメント

    -   シャード テーブルに自動インクリメント主キーがある場合、事前チェックは警告を返します。自動インクリメントの主キーに競合がある場合は、解決策について[自動インクリメント主キーの競合を処理する](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照してください。

### 増分データ移行のチェック項目 {#check-items-for-incremental-data-migration}

増分データ移行モード ( `task-mode: incremental` ) の場合、 [共通チェック項目](#common-check-items)に加えて、事前チェックには次のチェック項目も含まれます。

-   (必須) アップストリーム データベースの REPLICATION 権限

    -   レプリケーション クライアントの権限
    -   REPLICATION SLAVE パーミッション

-   データベースのプライマリ - セカンダリ構成

    -   プライマリとセカンダリのレプリケーションの失敗を回避するために、アップストリーム データベースにデータベース ID `server_id`を指定することをお勧めします (AWS Aurora以外の環境では GTID をお勧めします)。

-   (必須) MySQLbinlog構成

    -   binlogが有効になっているかどうかを確認します (DM で必要)。
    -   `binlog_format=ROW`が構成されているかどうかを確認します (DM は ROW 形式のbinlogの移行のみをサポートします)。
    -   `binlog_row_image=FULL`が構成されているかどうかを確認します (DM は`binlog_row_image=FULL`のみをサポートします)。
    -   `binlog_do_db`または`binlog_ignore_db`が設定されている場合、移行するデータベーステーブルが`binlog_do_db`および`binlog_ignore_db`の条件を満たしているかどうかを確認します。

-   (必須) 上流のデータベースが[オンライン DDL](/dm/feature-online-ddl.md)プロセス ( `ghost`テーブルは作成されているが、 `rename`フェーズはまだ実行されていないプロセス) にあるかどうかを確認します。アップストリームがオンライン DDL プロセスにある場合、事前チェックはエラーを返します。この場合、DDL が完了するまで待ってから再試行してください。

### 完全および増分データ移行のチェック項目 {#check-items-for-full-and-incremental-data-migration}

完全および増分データ移行モード ( `task-mode: all` ) の場合、 [共通チェック項目](#common-check-items)に加えて、事前チェックには[フルデータ移行チェック項目](#check-items-for-full-data-migration)と[増分データ移行チェック項目](#check-items-for-incremental-data-migration)も含まれます。

### 無視できるチェック項目 {#ignorable-check-items}

事前チェックにより、環境内の潜在的なリスクを見つけることができます。チェック項目を無視することはお勧めできません。データ移行タスクに特別なニーズがある場合は、 [`ignore-checking-items`構成アイテム](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)を使用して一部のチェック項目をスキップできます。

| チェック項目                   | 説明                                                                 |
| :----------------------- | :----------------------------------------------------------------- |
| `dump_privilege`         | 上流の MySQL インスタンスでユーザーのダンプ権限を確認します。                                 |
| `replication_privilege`  | 上流の MySQL インスタンスでユーザーのレプリケーション権限を確認します。                            |
| `version`                | アップストリーム データベースのバージョンを確認します。                                       |
| `server_id`              | アップストリーム データベースで server_id が設定されているかどうかを確認します。                     |
| `binlog_enable`          | アップストリーム データベースでbinlogが有効になっているかどうかを確認します。                         |
| `table_schema`           | アップストリーム MySQL テーブルのテーブル スキーマの互換性をチェックします。                         |
| `schema_of_shard_tables` | アップストリームの MySQL マルチインスタンス シャード内のテーブル スキーマの一貫性をチェックします。             |
| `auto_increment_ID`      | 上流の MySQL マルチインスタンス シャードで自動インクリメント主キーが競合するかどうかを確認します。              |
| `online_ddl`             | アップストリームが[オンライン DDL](/dm/feature-online-ddl.md)のプロセスにあるかどうかを確認します。 |

> **ノート：**
>
> v6.0 より前のバージョンでは、より多くの無視可能なチェック項目がサポートされています。 v6.0 以降、DM はデータの安全性に関するいくつかのチェック項目を無視することを許可しません。たとえば、 `binlog_row_image`パラメーターを正しく構成しないと、レプリケーション中にデータが失われる可能性があります。

## 事前チェック引数の構成 {#configure-precheck-arguments}

移行タスクの事前チェックでは、並列処理がサポートされています。シャード テーブルの行数が 100 万レベルに達した場合でも、数分で事前チェックを完了できます。

事前チェックのスレッド数を指定するには、移行タスク構成ファイルの`mydumpers`フィールドの`threads`引数を構成します。

```yaml
mydumpers:                           # Configuration arguments of the dump processing unit
  global:                            # Configuration name
    threads: 4                       # The number of threads that access the upstream when the dump processing unit performs the precheck and exports data from the upstream database (4 by default)
    chunk-filesize: 64               # The size of the files generated by the dump processing unit (64 MB by default)
    extra-args: "--consistency none" # Other arguments of the dump processing unit. You do not need to manually configure table-list in `extra-args`, because it is automatically generated by DM.

```

> **ノート：**
>
> 値`threads`は、アップストリーム データベースと DM 間の物理接続の数を決定します。 `threads`値が大きすぎると、アップストリームの負荷が増加する可能性があります。したがって、 `threads`適切な値に設定する必要があります。
