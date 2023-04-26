---
title: TiDB Lightning FAQs
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Lightning.
---

# TiDB LightningFAQ {#tidb-lightning-faqs}

このドキュメントには、 TiDB Lightningに関するよくある質問 (FAQ) と回答が記載されています。

## TiDB Lightningでサポートされている TiDB/TiKV/PD クラスタの最小バージョンは何ですか? {#what-is-the-minimum-tidb-tikv-pd-cluster-version-supported-by-tidb-lightning}

TiDB Lightningのバージョンは、クラスターと同じである必要があります。 Local-backend モードを使用する場合、利用可能な最も古いバージョンは 4.0.0 です。 Importer-backend モードまたは TiDB-backend モードを使用する場合、利用可能な最も古いバージョンは 2.0.9 ですが、3.0 安定バージョンを使用することをお勧めします。

## TiDB Lightning は複数のスキーマ (データベース) のインポートをサポートしていますか? {#does-tidb-lightning-support-importing-multiple-schemas-databases}

はい。

## ターゲット データベースの権限要件は何ですか? {#what-are-the-privilege-requirements-for-the-target-database}

権限の詳細については、 [TiDB Lightning を使用するための前提条件](/tidb-lightning/tidb-lightning-requirements.md)を参照してください。

## 1 つのテーブルをインポートするときに、 TiDB Lightning でエラーが発生しました。他のテーブルに影響しますか?プロセスは終了しますか? {#tidb-lightning-encountered-an-error-when-importing-one-table-will-it-affect-other-tables-will-the-process-be-terminated}

エラーが発生したテーブルが 1 つだけの場合でも、残りは正常に処理されます。

## TiDB Lightning を適切に再起動するには? {#how-to-properly-restart-tidb-lightning}

Importer-backend を使用している場合、 `tikv-importer`のステータスに応じて、 TiDB Lightningを再起動する基本的なシーケンスは次のようになります。

`tikv-importer`がまだ実行中の場合:

1.  [`tidb-lightning`停止する](#how-to-stop-the-tidb-lightning-process) .
2.  ソースデータの修正、設定の変更、ハードウェアの交換など、意図した変更を実行します。
3.  変更によって以前にいずれかのテーブルが変更された場合は、 [対応するチェックポイントを削除します](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-remove)も変更されます。
4.  `tidb-lightning`を開始します。

`tikv-importer`を再起動する必要がある場合:

1.  [`tidb-lightning`停止する](#how-to-stop-the-tidb-lightning-process) .
2.  [`tikv-importer`停止する](#how-to-stop-the-tikv-importer-process) .
3.  ソースデータの修正、設定の変更、ハードウェアの交換など、意図した変更を実行します。
4.  `tikv-importer`を開始します。
5.  `tidb-lightning`を開始し*、プログラムが CHECKSUM エラーで失敗するまで待ちます*。
    -   `tikv-importer`を再起動すると、まだ書き込まれているすべてのエンジン ファイルが破棄されますが、 `tidb-lightning`そのことを知りませんでした。 v3.0 の時点で、最も簡単な方法は`tidb-lightning`を続けて再試行することです。
6.  [失敗したテーブルとチェックポイントを破棄する](/tidb-lightning/troubleshoot-tidb-lightning.md#checkpoint-for--has-invalid-status-error-code)
7.  `tidb-lightning`をやり直してください。

Local-backend または TiDB-backend を使用している場合、操作は、 `tikv-importer`がまだ実行されているときに Importer-backend を使用する場合と同じです。

## インポートされたデータの整合性を確保するにはどうすればよいですか? {#how-to-ensure-the-integrity-of-the-imported-data}

デフォルトでは、 TiDB Lightning はローカル データ ソースとインポートされたテーブルでチェックサムを実行します。チェックサムの不一致がある場合、プロセスは中止されます。これらのチェックサム情報は、ログから読み取ることができます。

ターゲット テーブルで[`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) SQL コマンドを実行して、インポートされたデータのチェックサムを再計算することもできます。

```sql
ADMIN CHECKSUM TABLE `schema`.`table`;
```

```
+---------+------------+---------------------+-----------+-------------+
| Db_name | Table_name | Checksum_crc64_xor  | Total_kvs | Total_bytes |
+---------+------------+---------------------+-----------+-------------+
| schema  | table      | 5505282386844578743 |         3 |          96 |
+---------+------------+---------------------+-----------+-------------+
1 row in set (0.01 sec)
```

## TiDB Lightningでサポートされているデータ ソース形式は何ですか? {#what-kinds-of-data-source-formats-are-supported-by-tidb-lightning}

TiDB Lightning は以下をサポートしています。

-   [Dumpling](/dumpling-overview.md) 、CSV ファイル、および[Amazon Auroraによって生成された Apache Parquet ファイル](/migrate-aurora-to-tidb.md)によってエクスポートされたファイルのインポート。
-   ローカル ディスクまたは Amazon S3storageからのデータの読み取り。

## TiDB Lightning はスキーマとテーブルの作成をスキップできますか? {#could-tidb-lightning-skip-creating-schema-and-tables}

v5.1 から、 TiDB Lightning はダウンストリームのスキーマとテーブルを自動的に認識できるようになりました。 v5.1 より前のTiDB Lightningを使用している場合は、 `tidb-lightning.toml`の`[mydumper]`セクションに`no-schema = true`を設定する必要があります。これにより、 TiDB Lightning は`CREATE TABLE`の呼び出しをスキップし、メタデータをターゲット データベースから直接フェッチします。テーブルが実際に欠落している場合、 TiDB Lightning はエラーで終了します。

## 厳密な SQL モードを無効にして、無効なデータをインポートできるようにすることはできますか? {#can-the-strict-sql-mode-be-disabled-to-allow-importing-invalid-data}

はい。デフォルトでは、 TiDB Lightningで使用される[`sql_mode`](https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html) `"STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"`であり、日付`1970-00-00`などの無効なデータは許可されません。モードは、 `tidb-lightning.toml`の`[tidb]`セクションの`sql-mode`設定を変更することで変更できます。

```toml
...
[tidb]
sql-mode = ""
...
```

## 1 つの<code>tikv-importer</code>複数の<code>tidb-lightning</code>インスタンスを処理できますか? {#can-one-code-tikv-importer-code-serve-multiple-code-tidb-lightning-code-instances}

はい、すべて`tidb-lightning`インスタンスが異なるテーブルで動作する限り。

## <code>tikv-importer</code>プロセスを停止するには? {#how-to-stop-the-code-tikv-importer-code-process}

`tikv-importer`プロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動デプロイの場合: `tikv-importer`がフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tikv-importer`コマンドを使用してプロセス ID を取得し、 `kill ${PID}`コマンドを使用してプロセスを終了します。

## <code>tidb-lightning</code>プロセスを停止するには? {#how-to-stop-the-code-tidb-lightning-code-process}

`tidb-lightning`プロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動デプロイの場合: `tidb-lightning`がフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tidb-lightning`コマンドを使用してプロセス ID を取得し、 `kill -2 ${PID}`コマンドを使用してプロセスを終了します。

## TiDB Lightning は1 ギガビット ネットワーク カードで使用できますか? {#can-tidb-lightning-be-used-with-1-gigabit-network-card}

TiDB Lightning は、 10 ギガビットのネットワーク カードで使用するのが最適です。

1 ギガビット ネットワーク カードは、合計 120 MB/秒の帯域幅しか提供できず、これをすべてのターゲット TiKV ストアで共有する必要があります。 TiDB Lightning は、物理インポート モードで 1 ギガビット ネットワークのすべての帯域幅を簡単に飽和させ、PD に接続できなくなるため、クラスターをダウンさせる可能性があります。

## TiDB Lightning が対象の TiKV クラスタに大量の空き容量を必要とするのはなぜですか? {#why-tidb-lightning-requires-so-much-free-space-in-the-target-tikv-cluster}

3 つのレプリカのデフォルト設定では、ターゲット TiKV クラスターのスペース要件は、データ ソースのサイズの 6 倍です。次の要因がデータ ソースに反映されていないため、余分な &quot;2&quot; の倍数は保守的な見積もりです。

-   インデックスが占めるスペース
-   RocksDB での空間増幅

## TiDB Lightningの実行中に TiKV Importer を再起動できますか? {#can-tikv-importer-be-restarted-while-tidb-lightning-is-running}

いいえ。TiKV Importer は、エンジンの一部の情報をメモリに保存します。 `tikv-importer`を再起動すると、 `tidb-lightning`接続が失われたために停止します。この時点で、これらの TiKV Importer 固有の情報が失われるため、 [失敗したチェックポイントを破棄する](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)にする必要があります。後でTiDB Lightningを再起動できます。

正しい順序については、 [TiDB Lightning を適切に再起動するには?](#how-to-properly-restart-tidb-lightning)も参照してください。

## TiDB Lightningに関連するすべての中間データを完全に破棄するには? {#how-to-completely-destroy-all-intermediate-data-associated-with-tidb-lightning}

1.  チェックポイント ファイルを削除します。

    {{< copyable "" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-remove=all
    ```

    何らかの理由でこのコマンドを実行できない場合は、手動でファイルを削除してみてください`/tmp/tidb_lightning_checkpoint.pb` 。

2.  Local-backend を使用している場合は、構成で`sorted-kv-dir`ディレクトリを削除します。 Importer-backend を使用している場合は、 `tikv-importer`ホストしているマシンの`import`ディレクトリ全体を削除します。

3.  必要に応じて、TiDB クラスターで作成されたすべてのテーブルとデータベースを削除します。

4.  残りのメタデータをクリーンアップします。次のいずれかの条件が存在する場合は、メタデータ スキーマを手動でクリーンアップする必要があります。

    -   TiDB Lightning v5.1.x および v5.2.x バージョンの場合、 `tidb-lightning-ctl`コマンドはターゲット クラスターのメタデータ スキーマをクリーンアップしません。手動でクリーンアップする必要があります。
    -   チェックポイント ファイルを手動で削除した場合は、ダウンストリーム メタデータ スキーマを手動でクリーンアップする必要があります。そうしないと、後続のインポートの正確性が影響を受ける可能性があります。

    次のコマンドを使用して、メタデータをクリーンアップします。

    {{< copyable "" >}}

    ```sql
    DROP DATABASE IF EXISTS `lightning_metadata`;
    ```

## TiDB Lightningの実行時のゴルーチン情報を取得する方法 {#how-to-get-the-runtime-goroutine-information-of-tidb-lightning}

1.  TiDB Lightningの設定ファイルに[`status-port`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-configuration)が指定されている場合は、この手順をスキップしてください。それ以外の場合は、 USR1 シグナルをTiDB Lightningに送信して`status-port`を有効にする必要があります。

    `ps`などのコマンドを使用してTiDB Lightningのプロセス ID (PID) を取得し、次のコマンドを実行します。

    {{< copyable "" >}}

    ```sh
    kill -USR1 <lightning-pid>
    ```

    TiDB Lightningのログを確認してください。 `starting HTTP server`のログは、新しく有効になった`status-port`を示し`started HTTP server` `start HTTP server`ます。

2.  `http://<lightning-ip>:<status-port>/debug/pprof/goroutine?debug=2`にアクセスして、ゴルーチン情報を取得します。

## TiDB Lightning がSQL の Placement Rules と互換性がないのはなぜですか? {#why-is-tidb-lightning-not-compatible-with-placement-rules-in-sql}

TiDB Lightning は[SQL の配置規則](/placement-rules-in-sql.md)と互換性がありません。 TiDB Lightning が配置ポリシーを含むデータをインポートすると、 TiDB Lightning はエラーを報告します。

その理由は次のように説明されています。

SQL での配置ルールの目的は、特定の TiKV ノードのデータの場所をテーブルまたはパーティション レベルで制御することです。 TiDB Lightning は、テキスト ファイル内のデータをターゲットの TiDB クラスターにインポートします。データ ファイルが配置ルールの定義とともにエクスポートされる場合、インポート プロセス中に、 TiDB Lightning は定義に基づいてターゲット クラスタに対応する配置ルール ポリシーを作成する必要があります。ソース クラスタとターゲット クラスタのトポロジが異なる場合、これが問題を引き起こす可能性があります。

ソース クラスタに次のトポロジがあるとします。

![TiDB Lightning FAQ - source cluster topology](/media/lightning-faq-source-cluster-topology.jpg)

ソース クラスタには、次の配置ポリシーがあります。

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east" REGIONS="us-east,us-west";
```

**状況 1:**ターゲット クラスターに 3 つのレプリカがあり、トポロジーがソース クラスターとは異なります。このような場合、 TiDB Lightning がターゲット クラスタに配置ポリシーを作成するときに、エラーは報告されません。ただし、ターゲット クラスタのセマンティクスは間違っています。

![TiDB Lightning FAQ - situation 1](/media/lightning-faq-situation-1.jpg)

**状況 2:**ターゲット クラスターは、リージョン「us-mid」の別の TiKV ノードにフォロワー レプリカを配置し、トポロジーにリージョン「us-west」を持っていません。このような場合、ターゲット クラスタで配置ポリシーを作成すると、 TiDB Lightning はエラーを報告します。

![TiDB Lightning FAQ - situation 2](/media/lightning-faq-situation-2.jpg)

**回避策:**

TiDB Lightningを使用して SQL で配置ルールを使用するには、データをターゲット テーブルにインポートする**前に、**関連するラベルとオブジェクトがターゲット TiDB クラスターに作成されていることを確認する必要があります。 SQL の配置ルールは PD および TiKVレイヤーで機能するため、 TiDB Lightning は、インポートされたデータを格納するためにどの TiKV を使用する必要があるかを見つけるために必要な情報を取得できます。このように、SQL のこの配置ルールはTiDB Lightningに対して透過的です。

手順は次のとおりです。

1.  データ分散トポロジを計画します。
2.  TiKV と PD に必要なラベルを構成します。
3.  配置ルール ポリシーを作成し、作成したポリシーをターゲット テーブルに適用します。
4.  TiDB Lightning を使用して、データをターゲット テーブルにインポートします。
