---
title: TiDB Lightning FAQs
summary: TiDB Lightningに関するよくある質問 (FAQ) と回答について説明します。
---

# TiDB Lightningに関するよくある質問 {#tidb-lightning-faqs}

このドキュメントには、 TiDB Lightningに関するよくある質問 (FAQ) と回答が記載されています。

## TiDB Lightningでサポートされる最小の TiDB/TiKV/PD クラスター バージョンは何ですか? {#what-is-the-minimum-tidb-tikv-pd-cluster-version-supported-by-tidb-lightning}

TiDB Lightningのバージョンはクラスターと同じである必要があります。Local-backendモードを使用する場合、利用可能な最新バージョンは4.0.0です。Importer-backendモードまたはTiDB-backendモードを使用する場合、利用可能な最新バージョンは2.0.9ですが、安定版の3.0を使用することをお勧めします。

## TiDB Lightning は複数のスキーマ (データベース) のインポートをサポートしていますか? {#does-tidb-lightning-support-importing-multiple-schemas-databases}

はい。

## ターゲット データベースの権限要件は何ですか? {#what-are-the-privilege-requirements-for-the-target-database}

権限の詳細については[TiDB Lightningを使用するための前提条件](/tidb-lightning/tidb-lightning-requirements.md)参照してください。

## TiDB Lightning で1 つのテーブルのインポート中にエラーが発生しました。他のテーブルにも影響しますか？プロセスは終了しますか？ {#tidb-lightning-encountered-an-error-when-importing-one-table-will-it-affect-other-tables-will-the-process-be-terminated}

1 つのテーブルのみにエラーが発生した場合でも、残りのテーブルは正常に処理されます。

## TiDB Lightningを適切に再起動するにはどうすればよいですか? {#how-to-properly-restart-tidb-lightning}

1.  [`tidb-lightning`プロセスを停止する](#how-to-stop-the-tidb-lightning-process) 。
2.  新しい`tidb-lightning`タスクを開始します。3 `nohup tiup tidb-lightning -config tidb-lightning.toml`の前の開始コマンドを実行します。

## インポートされたデータの整合性を確保するにはどうすればよいですか? {#how-to-ensure-the-integrity-of-the-imported-data}

TiDB Lightningはデフォルトで、ローカルデータソースとインポートされたテーブルのチェックサムを実行します。チェックサムが一致しない場合、プロセスは中止されます。このチェックサム情報はログから読み取ることができます。

ターゲット テーブルで[`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) SQL コマンドを実行して、インポートされたデータのチェックサムを再計算することもできます。

```sql
ADMIN CHECKSUM TABLE `schema`.`table`;
```

    +---------+------------+---------------------+-----------+-------------+
    | Db_name | Table_name | Checksum_crc64_xor  | Total_kvs | Total_bytes |
    +---------+------------+---------------------+-----------+-------------+
    | schema  | table      | 5505282386844578743 |         3 |          96 |
    +---------+------------+---------------------+-----------+-------------+
    1 row in set (0.01 sec)

## TiDB Lightningではどのようなデータ ソース形式がサポートされていますか? {#what-kinds-of-data-source-formats-are-supported-by-tidb-lightning}

TiDB Lightning は以下をサポートします:

-   [Dumpling](/dumpling-overview.md) 、CSV ファイル、および[Amazon Auroraによって生成された Apache Parquet ファイル](/migrate-aurora-to-tidb.md) 、Apache Hive、Snowflake によってエクスポートされたファイルをインポートします。
-   ローカルディスクまたは Amazon S3storageからデータを読み取ります。

## TiDB Lightning はスキーマとテーブルの作成をスキップできますか? {#could-tidb-lightning-skip-creating-schema-and-tables}

v5.1以降、 TiDB Lightningは下流のスキーマとテーブルを自動的に認識できるようになりました。v5.1より前のTiDB Lightningをご利用の場合は、 `tidb-lightning.toml`の`[mydumper]`セクションに`no-schema = true`設定する必要があります。これにより、 TiDB Lightningは`CREATE TABLE`呼び出しをスキップし、ターゲットデータベースからメタデータを直接取得します。テーブルが実際に存在しない場合、 TiDB Lightningはエラーで終了します。

## 無効なデータのインポートを禁止するにはどうすればよいですか? {#how-to-prohibit-importing-invalid-data}

厳密な SQL モードを有効にすると、無効なデータのインポートを禁止できます。

デフォルトでは、 TiDB Lightningで使用される[`sql_mode`](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html) `"ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER"`であり、日付`1970-00-00`などの無効なデータが許可されます。

無効なデータのインポートを禁止するには、 `tidb-lightning.toml`の`[tidb]`セクションで`sql-mode`設定を`"STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"`に変更する必要があります。

```toml
...
[tidb]
sql-mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"
...
```

## <code>tidb-lightning</code>プロセスを停止するにはどうすればいいですか? {#how-to-stop-the-code-tidb-lightning-code-process}

`tidb-lightning`プロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動デプロイの場合： `tidb-lightning`フォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tidb-lightning`コマンドを使用してプロセス ID を取得し、 `kill -2 ${PID}`コマンドを使用してプロセスを終了します。

## TiDB Lightning は1 ギガビット ネットワーク カードで使用できますか? {#can-tidb-lightning-be-used-with-1-gigabit-network-card}

TiDB Lightning は、10 ギガビット ネットワーク カードで使用するのが最適です。

1ギガビットネットワークカードは合計120MB/秒の帯域幅しか提供できず、これをすべてのターゲットTiKVストアで共有する必要があります。TiDB TiDB Lightningは、物理インポートモードで1ギガビットネットワークの全帯域幅を簡単に飽和させ、PDに接続できなくなるため、クラスタを停止させる可能性があります。

## TiDB Lightning がターゲット TiKV クラスターにこれほど多くの空き領域を必要とするのはなぜですか? {#why-tidb-lightning-requires-so-much-free-space-in-the-target-tikv-cluster}

デフォルト設定のレプリカ数3の場合、ターゲットTiKVクラスターに必要な容量はデータソースの6倍になります。「2」という倍数は、以下の要素がデータソースに反映されていないため、控えめな見積もりです。

-   インデックスが占めるスペース
-   RocksDBにおける空間増幅

## TiDB Lightningに関連付けられたすべての中間データを完全に破棄するにはどうすればよいですか? {#how-to-completely-destroy-all-intermediate-data-associated-with-tidb-lightning}

1.  チェックポイント ファイルを削除します。

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-remove=all
    ```

    何らかの理由でこのコマンドを実行できない場合は、ファイル`/tmp/tidb_lightning_checkpoint.pb`手動で削除してみてください。

2.  Local-backend を使用している場合は、構成内の`sorted-kv-dir`ディレクトリを削除します。

3.  必要に応じて、TiDB クラスター上に作成されたすべてのテーブルとデータベースを削除します。

4.  残留メタデータをクリーンアップします。以下のいずれかの条件に該当する場合は、メタデータスキーマを手動でクリーンアップする必要があります。

    -   TiDB Lightning v5.1.xおよびv5.2.xバージョンの場合、 `tidb-lightning-ctl`コマンドではターゲットクラスタ内のメタデータスキーマがクリーンアップされません。手動でクリーンアップする必要があります。
    -   チェックポイント ファイルを手動で削除した場合は、ダウンストリーム メタデータ スキーマを手動でクリーンアップする必要があります。そうしないと、後続のインポートの正確性が影響を受ける可能性があります。

    メタデータをクリーンアップするには、次のコマンドを使用します。

    ```sql
    DROP DATABASE IF EXISTS `lightning_metadata`;
    ```

## TiDB Lightningのランタイムgoroutine情報を取得する方法 {#how-to-get-the-runtime-goroutine-information-of-tidb-lightning}

1.  TiDB Lightningの設定ファイルで[`status-port`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-configuration)指定されている場合は、この手順をスキップしてください。それ以外の場合は、 `status-port`有効にするためにTiDB Lightningに USR1 信号を送信する必要があります。

    `ps`などのコマンドを使用してTiDB Lightningのプロセス ID (PID) を取得し、次のコマンドを実行します。

    ```sh
    kill -USR1 <lightning-pid>
    ```

    TiDB Lightningのログを確認します。1/ `starting HTTP server` / `started HTTP server`のログに`start HTTP server`新たに有効化された`status-port`表示されます。

2.  `http://<lightning-ip>:<status-port>/debug/pprof/goroutine?debug=2`アクセスして、goroutine 情報を取得します。

## TiDB Lightning がSQL の配置ルールと互換性がないのはなぜですか? {#why-is-tidb-lightning-not-compatible-with-placement-rules-in-sql}

TiDB Lightning は[SQLの配置ルール](/placement-rules-in-sql.md)と互換性がありません。配置ポリシーを含むデータをTiDB Lightningにインポートすると、エラーが報告されます。

その理由は次のように説明されます。

SQLにおける配置ルールの目的は、特定のTiKVノードのデータ配置をテーブルレベルまたはパーティションレベルで制御することです。TiDB TiDB Lightningは、テキストファイル形式のデータをターゲットのTiDBクラスターにインポートします。データファイルが配置ルールの定義と共にエクスポートされた場合、インポートプロセス中に、 TiDB Lightningは定義に基づいてターゲットクラスター内に対応する配置ルールポリシーを作成する必要があります。ソースクラスターとターゲットクラスターのトポロジが異なる場合、これが問題を引き起こす可能性があります。

Suppose the source cluster has the following topology:

![TiDB Lightning FAQ - source cluster topology](/media/lightning-faq-source-cluster-topology.jpg)

ソース クラスターには次の配置ポリシーがあります。

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east" REGIONS="us-east,us-west";
```

**状況1：**ターゲットクラスタに3つのレプリカがあり、トポロジがソースクラスタと異なります。このような場合、 TiDB Lightningがターゲットクラスタに配置ポリシーを作成する際にエラーは報告されませんが、ターゲットクラスタのセマンティクスが誤っています。

![TiDB Lightning FAQ - situation 1](/media/lightning-faq-situation-1.jpg)

**状況2：**ターゲットクラスタがフォロワーレプリカを「us-mid」リージョン内の別のTiKVノードに配置しており、トポロジ内に「us-west」リージョンが含まれていない場合。このような場合、ターゲットクラスタで配置ポリシーを作成すると、 TiDB Lightningはエラーを報告します。

![TiDB Lightning FAQ - situation 2](/media/lightning-faq-situation-2.jpg)

**回避策:**

TiDB LightningでSQLの配置ルールを使用するには、データをターゲットテーブルにインポートする**前に、**関連するラベルとオブジェクトがターゲットTiDBクラスター内に作成されていることを確認する必要があります。SQLの配置ルールはPDおよびTiKVレイヤーで機能するため、 TiDB Lightning はインポートされたデータの保存にどのTiKVを使用するかを判断するために必要な情報を取得できます。このように、SQLの配置ルールはTiDB Lightningに対して透過的です。

手順は次のとおりです。

1.  データ分散トポロジを計画します。
2.  TiKV および PD に必要なラベルを構成します。
3.  配置ルール ポリシーを作成し、作成したポリシーをターゲット テーブルに適用します。
4.  TiDB Lightningを使用して、データをターゲット テーブルにインポートします。

## TiDB LightningとDumplingを使用してスキーマをコピーするにはどうすればよいですか? {#how-can-i-use-tidb-lightning-and-dumpling-to-copy-a-schema}

あるスキーマから新しいスキーマにスキーマ定義とテーブルデータの両方をコピーしたい場合は、このセクションの手順に従ってください。この例では、スキーマ`test`のコピーを`test2`という新しいスキーマに作成する方法を説明します。

1.  必要なスキーマのみを選択するには、 `-B test`を使用して元のスキーマのバックアップを作成します。

        tiup dumpling -B test -o /tmp/bck1

2.  次の内容のファイルを`/tmp/tidb-lightning.toml`作成します。

    ```toml
    [tidb]
    host = "127.0.0.1"
    port = 4000
    user = "root"

    [tikv-importer]
    backend = "tidb"

    [mydumper]
    data-source-dir = "/tmp/bck1"

    [[mydumper.files]]
    pattern = '^[a-z]*\.(.*)\.[0-9]*\.sql$'
    schema = 'test2'
    table = '$1'
    type = 'sql'

    [[mydumper.files]]
    pattern = '^[a-z]*\.(.*)\-schema\.sql$'
    schema = 'test2'
    table = '$1'
    type = 'table-schema'
    ```

    この設定ファイルでは、元のダンプで使用されたスキーマ名とは異なるスキーマ名を使用するため、 `schema = 'test2'`設定します。ファイル名はテーブル名を決定するために使用されます。

3.  この構成ファイルを使用してインポートを実行します。

        tiup tidb-lightning -config /tmp/tidb-lightning.toml
