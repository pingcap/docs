---
title: TiDB Lightning FAQs
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Lightning.
---

# TiDB Lightningよくある質問 {#tidb-lightning-faqs}

このドキュメントには、 TiDB Lightningに関するよくある質問 (FAQ) とその回答が記載されています。

## TiDB Lightningでサポートされる TiDB/TiKV/PD クラスターの最小バージョンは何ですか? {#what-is-the-minimum-tidb-tikv-pd-cluster-version-supported-by-tidb-lightning}

TiDB Lightningのバージョンはクラスターと同じである必要があります。ローカル バックエンド モードを使用する場合、利用可能な最も古いバージョンは 4.0.0 です。インポーター バックエンド モードまたは TiDB バックエンド モードを使用する場合、利用可能な最も古いバージョンは 2.0.9 ですが、安定バージョン 3.0 を使用することをお勧めします。

## TiDB Lightning は複数のスキーマ (データベース) のインポートをサポートしていますか? {#does-tidb-lightning-support-importing-multiple-schemas-databases}

はい。

## ターゲットデータベースの権限要件は何ですか? {#what-are-the-privilege-requirements-for-the-target-database}

権限の詳細については、 [TiDB Lightning を使用するための前提条件](/tidb-lightning/tidb-lightning-requirements.md)を参照してください。

## TiDB Lightning で1 つのテーブルをインポート中にエラーが発生しました。他のテーブルに影響はありますか?プロセスは終了しますか? {#tidb-lightning-encountered-an-error-when-importing-one-table-will-it-affect-other-tables-will-the-process-be-terminated}

1 つのテーブルのみでエラーが発生した場合でも、残りのテーブルは通常どおり処理されます。

## TiDB Lightning を適切に再起動するにはどうすればよいですか? {#how-to-properly-restart-tidb-lightning}

Importer-backend を使用している場合、 `tikv-importer`のステータスに応じて、 TiDB Lightningを再起動する基本的なシーケンスは次のようになります。

`tikv-importer`がまだ実行中の場合:

1.  [`tidb-lightning`やめる](#how-to-stop-the-tidb-lightning-process) 。
2.  ソースデータの修正、設定の変更、ハードウェアの交換など、意図した変更を実行します。
3.  以前の変更によってテーブルが変更されている場合は、 [対応するチェックポイントを削除します](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-remove)も追加されます。
4.  `tidb-lightning`を開始します。

`tikv-importer`を再起動する必要がある場合:

1.  [`tidb-lightning`やめる](#how-to-stop-the-tidb-lightning-process) 。
2.  [`tikv-importer`停止する](#how-to-stop-the-tikv-importer-process) 。
3.  ソースデータの修正、設定の変更、ハードウェアの交換など、意図した変更を実行します。
4.  `tikv-importer`を開始します。
5.  `tidb-lightning`を開始し*、CHECKSUM エラー (存在する場合) でプログラムが失敗するまで待ちます*。
    -   `tikv-importer`を再起動すると、まだ書き込まれているすべてのエンジン ファイルが破壊されますが、 `tidb-lightning`それを知りませんでした。 v3.0 では、最も簡単な方法は`tidb-lightning`を続行して再試行することです。
6.  [失敗したテーブルとチェックポイントを破棄します](/tidb-lightning/troubleshoot-tidb-lightning.md#checkpoint-for--has-invalid-status-error-code)
7.  もう一度`tidb-lightning`から始めます。

Local-backend または TiDB-backend を使用している場合、操作は`tikv-importer`がまだ実行中の場合に Importer-backend を使用する場合と同じです。

## インポートされたデータの整合性を確保するにはどうすればよいですか? {#how-to-ensure-the-integrity-of-the-imported-data}

TiDB Lightning はデフォルトで、ローカル データ ソースとインポートされたテーブルに対してチェックサムを実行します。チェックサムが一致しない場合、プロセスは中止されます。これらのチェックサム情報はログから読み取ることができます。

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

## TiDB Lightningではどのような種類のデータ ソース形式がサポートされていますか? {#what-kinds-of-data-source-formats-are-supported-by-tidb-lightning}

TiDB Lightningは以下をサポートします。

-   [Dumpling](/dumpling-overview.md) 、CSVファイル、 [Amazon Auroraによって生成された Apache Parquet ファイル](/migrate-aurora-to-tidb.md)でエクスポートしたファイルをインポートします。
-   ローカル ディスクまたは Amazon S3storageからのデータの読み取り。

## TiDB Lightning はスキーマとテーブルの作成をスキップできますか? {#could-tidb-lightning-skip-creating-schema-and-tables}

v5.1 以降、 TiDB Lightning はダウンストリームのスキーマとテーブルを自動的に認識できるようになりました。 TiDB Lightning v5.1 より前のバージョンを使用している場合は、 `tidb-lightning.toml`の`[mydumper]`セクションに`no-schema = true`を設定する必要があります。これにより、 TiDB Lightning は`CREATE TABLE`の呼び出しをスキップし、ターゲット データベースから直接メタデータをフェッチします。実際にテーブルが欠落している場合、 TiDB Lightning はエラーで終了します。

## 無効なデータのインポートを禁止するにはどうすればよいですか? {#how-to-prohibit-importing-invalid-data}

厳密 SQL モードを有効にすることで、無効なデータのインポートを禁止できます。

デフォルトでは、 TiDB Lightningで使用される[`sql_mode`](https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html) `"ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER"`で、日付`1970-00-00`などの無効なデータが許可されます。

不正なデータのインポートを禁止するには、 `tidb-lightning.toml`の`[tidb]`の設定を`sql-mode`から`"STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"`に変更する必要があります。

```toml
...
[tidb]
sql-mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"
...
```

## 1 つの<code>tikv-importer</code>複数の<code>tidb-lightning</code>インスタンスに対応できますか? {#can-one-code-tikv-importer-code-serve-multiple-code-tidb-lightning-code-instances}

はい、 `tidb-lightning`のインスタンスごとに異なるテーブルで動作する限り、可能です。

## <code>tikv-importer</code>プロセスを停止するにはどうすればよいですか? {#how-to-stop-the-code-tikv-importer-code-process}

`tikv-importer`プロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動デプロイメントの場合: `tikv-importer`がフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tikv-importer`コマンドを使用してプロセス ID を取得し、 `kill ${PID}`コマンドを使用してプロセスを終了します。

## <code>tidb-lightning</code>プロセスを停止するにはどうすればよいですか? {#how-to-stop-the-code-tidb-lightning-code-process}

`tidb-lightning`プロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動デプロイメントの場合: `tidb-lightning`がフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tidb-lightning`コマンドを使用してプロセス ID を取得し、 `kill -2 ${PID}`コマンドを使用してプロセスを終了します。

## TiDB Lightning は1 ギガビット ネットワーク カードで使用できますか? {#can-tidb-lightning-be-used-with-1-gigabit-network-card}

TiDB Lightning は、 10 ギガビット ネットワーク カードと併用するのが最適です。

1 ギガビット ネットワーク カードは合計 120 MB/秒の帯域幅しか提供できず、これをすべてのターゲット TiKV ストアで共有する必要があります。 TiDB Lightning は、物理インポート モードで 1 ギガビット ネットワークのすべての帯域幅を簡単に飽和させ、PD に接続できなくなるため、クラスターをダウンさせる可能性があります。

## TiDB Lightning がターゲット TiKV クラスターにこれほど多くの空き領域を必要とするのはなぜですか? {#why-tidb-lightning-requires-so-much-free-space-in-the-target-tikv-cluster}

デフォルト設定の 3 つのレプリカでは、ターゲット TiKV クラスターのスペース要件はデータ ソースのサイズの 6 倍になります。次の要素がデータ ソースに反映されていないため、「2」の追加倍数は控えめな推定値です。

-   インデックスが占めるスペース
-   RocksDB の空間増幅

## TiDB Lightningの実行中に TiKV Importer を再起動できますか? {#can-tikv-importer-be-restarted-while-tidb-lightning-is-running}

いいえ。TiKV インポーターはエンジンの一部の情報をメモリに保存します。 `tikv-importer`を再起動すると、 `tidb-lightning`接続が失われたため停止します。この時点で、TiKV Importer 固有の情報が失われるため、 [失敗したチェックポイントを破棄する](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)を行う必要があります。後でTiDB Lightningを再起動できます。

正しい順序については[TiDB Lightning を適切に再起動するにはどうすればよいですか?](#how-to-properly-restart-tidb-lightning)も参照してください。

## TiDB Lightningに関連付けられたすべての中間データを完全に破棄するにはどうすればよいですか? {#how-to-completely-destroy-all-intermediate-data-associated-with-tidb-lightning}

1.  チェックポイントファイルを削除します。

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-remove=all
    ```

    何らかの理由でこのコマンドを実行できない場合は、ファイル`/tmp/tidb_lightning_checkpoint.pb`を手動で削除してみてください。

2.  Local-backend を使用している場合は、構成内の`sorted-kv-dir`ディレクトリを削除します。 Importer-backend を使用している場合は、 `tikv-importer`ホストしているマシン上の`import`ディレクトリ全体を削除します。

3.  必要に応じて、TiDB クラスター上に作成されたすべてのテーブルとデータベースを削除します。

4.  残ったメタデータをクリーンアップします。次のいずれかの条件が存在する場合は、メタデータ スキーマを手動でクリーンアップする必要があります。

    -   TiDB Lightning v5.1.x および v5.2.x バージョンの場合、 `tidb-lightning-ctl`コマンドはターゲット クラスター内のメタデータ スキーマをクリーンアップしません。手動でクリーンアップする必要があります。
    -   チェックポイント ファイルを手動で削除した場合は、ダウンストリーム メタデータ スキーマを手動でクリーンアップする必要があります。そうしないと、後続のインポートの正確さに影響が出る可能性があります。

    次のコマンドを使用してメタデータをクリーンアップします。

    ```sql
    DROP DATABASE IF EXISTS `lightning_metadata`;
    ```

## TiDB Lightningのランタイムゴルーチン情報を取得する方法 {#how-to-get-the-runtime-goroutine-information-of-tidb-lightning}

1.  TiDB Lightningの設定ファイルで[`status-port`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-configuration)が指定されている場合は、この手順をスキップしてください。それ以外の場合は、USR1 信号をTiDB Lightningに送信して`status-port`を有効にする必要があります。

    `ps`などのコマンドを使用してTiDB Lightningのプロセス ID (PID) を取得し、次のコマンドを実行します。

    ```sh
    kill -USR1 <lightning-pid>
    ```

    TiDB Lightningのログを確認してください。 `starting HTTP server` / `start HTTP server` / `started HTTP server`のログには、新しく有効になった`status-port`が表示されます。

2.  `http://<lightning-ip>:<status-port>/debug/pprof/goroutine?debug=2`にアクセスして goroutine 情報を取得します。

## TiDB Lightning がSQL の配置ルールと互換性がないのはなぜですか? {#why-is-tidb-lightning-not-compatible-with-placement-rules-in-sql}

TiDB Lightning は[SQL の配置ルール](/placement-rules-in-sql.md)と互換性がありません。 TiDB Lightning が配置ポリシーを含むデータをインポートすると、 TiDB Lightning はエラーを報告します。

その理由は次のように説明されています。

SQL の配置ルールの目的は、テーブルまたはパーティション レベルで特定の TiKV ノードのデータの場所を制御することです。 TiDB Lightning は、テキスト ファイル内のデータをターゲット TiDB クラスターにインポートします。データ ファイルが配置ルールの定義とともにエクスポートされる場合、インポート プロセス中に、 TiDB Lightning は定義に基づいてターゲット クラスターに対応する配置ルール ポリシーを作成する必要があります。ソース クラスターとターゲット クラスターのトポロジが異なる場合、問題が発生する可能性があります。

ソース クラスターに次のトポロジがあるとします。

![TiDB Lightning FAQ - source cluster topology](/media/lightning-faq-source-cluster-topology.jpg)

ソースクラスターには次の配置ポリシーがあります。

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east" REGIONS="us-east,us-west";
```

**状況 1:**ターゲット クラスターには 3 つのレプリカがあり、トポロジはソース クラスターとは異なります。このような場合、 TiDB Lightning がターゲット クラスターに配置ポリシーを作成するときに、エラーは報告されません。ただし、ターゲット クラスターのセマンティクスが間違っています。

![TiDB Lightning FAQ - situation 1](/media/lightning-faq-situation-1.jpg)

**状況 2:**ターゲット クラスターは、リージョン「us-mid」の別の TiKV ノードにフォロワー レプリカを配置しますが、トポロジにリージョン「us-west」がありません。このような場合、ターゲット クラスターで配置ポリシーを作成すると、 TiDB Lightning はエラーを報告します。

![TiDB Lightning FAQ - situation 2](/media/lightning-faq-situation-2.jpg)

**回避策:**

TiDB Lightningを使用して SQL で配置ルールを使用するには、ターゲット テーブルにデータをインポートする**前に、**関連するラベルとオブジェクトがターゲット TiDB クラスターに作成されていることを確認する必要があります。 SQL の配置ルールは PD および TiKVレイヤーで機能するため、 TiDB Lightning は、インポートされたデータを保存するためにどの TiKV を使用する必要があるかを判断するために必要な情報を取得できます。このように、SQL のこの配置ルールはTiDB Lightningに対して透過的です。

手順は次のとおりです。

1.  データ分散トポロジを計画します。
2.  TiKV と PD に必要なラベルを構成します。
3.  配置ルールポリシーを作成し、作成したポリシーを対象テーブルに適用します。
4.  TiDB Lightning を使用して、データをターゲットテーブルにインポートします。

## TiDB LightningとDumpling を使用してスキーマをコピーするにはどうすればよいですか? {#how-can-i-use-tidb-lightning-and-dumpling-to-copy-a-schema}

スキーマ定義とテーブル データの両方を 1 つのスキーマから新しいスキーマにコピーする場合は、このセクションの手順に従います。この例では、 `test`スキーマのコピーを`test2`という新しいスキーマに作成する方法を学びます。

1.  `-B test`を使用して元のスキーマのバックアップを作成し、必要なスキーマのみを選択します。

        tiup dumpling -B test -o /tmp/bck1

2.  次の内容を含む`/tmp/tidb-lightning.toml`ファイルを作成します。

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

    この構成ファイルでは、元のダンプで使用されたものとは異なるスキーマ名を使用するため、 `schema = 'test2'`を設定します。ファイル名はテーブルの名前を決定するために使用されます。

3.  この構成ファイルを使用してインポートを実行します。

        tiup tidb-lightning -config /tmp/tidb-lightning.toml
