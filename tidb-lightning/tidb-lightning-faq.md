---
title: TiDB Lightning FAQs
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Lightning.
---

# TiDB LightningFAQ {#tidb-lightning-faqs}

## TiDB Lightningでサポートされている TiDB/TiKV/PD クラスタの最小バージョンは何ですか? {#what-is-the-minimum-tidb-tikv-pd-cluster-version-supported-by-tidb-lightning}

TiDB Lightningのバージョンは、クラスターと同じである必要があります。 Local-backend モードを使用する場合、利用可能な最も古いバージョンは 4.0.0 です。 Importer-backend モードまたは TiDB-backend モードを使用する場合、利用可能な最も古いバージョンは 2.0.9 ですが、3.0 安定バージョンを使用することをお勧めします。

## TiDB Lightningは複数のスキーマ (データベース) のインポートをサポートしていますか? {#does-tidb-lightning-support-importing-multiple-schemas-databases}

はい。

## ターゲット データベースの権限要件は何ですか? {#what-are-the-privilege-requirements-for-the-target-database}

権限の詳細については、 [TiDB Lightningを使用するための前提条件](/tidb-lightning/tidb-lightning-requirements.md)を参照してください。

## 1 つのテーブルをインポートするときに、 TiDB Lightningでエラーが発生しました。他のテーブルに影響しますか?プロセスは終了しますか? {#tidb-lightning-encountered-an-error-when-importing-one-table-will-it-affect-other-tables-will-the-process-be-terminated}

エラーが発生したテーブルが 1 つだけの場合でも、残りは正常に処理されます。

## TiDB Lightningを適切に再起動するには? {#how-to-properly-restart-tidb-lightning}

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
5.  `tidb-lightning`*を開始し、プログラムが CHECKSUM エラーで失敗するまで待ちます*。
    -   `tikv-importer`を再起動すると、まだ書き込まれているすべてのエンジン ファイルが破棄されますが、 `tidb-lightning`はそのことを知りませんでした。 v3.0 の時点で、最も簡単な方法は`tidb-lightning`を続けて再試行することです。
6.  [失敗したテーブルとチェックポイントを破棄する](#checkpoint-for--has-invalid-status-error-code)
7.  `tidb-lightning`をやり直してください。

Local-backend または TiDB-backend を使用している場合、操作は、 `tikv-importer`がまだ実行されているときに Importer-backend を使用する場合と同じです。

## インポートされたデータの整合性を確保するにはどうすればよいですか? {#how-to-ensure-the-integrity-of-the-imported-data}

デフォルトでは、 TiDB Lightningはローカル データ ソースとインポートされたテーブルでチェックサムを実行します。チェックサムの不一致がある場合、プロセスは中止されます。これらのチェックサム情報は、ログから読み取ることができます。

ターゲット テーブルで`ADMIN CHECKSUM TABLE` SQL コマンドを実行して、インポートされたデータのチェックサムを再計算することもできます。

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

TiDB Lightningは以下をサポートしています。

-   [Dumpling](/dumpling-overview.md) 、CSV ファイル、および[Amazon Auroraによって生成された Apache Parquet ファイル](/migrate-aurora-to-tidb.md)によってエクスポートされたファイルのインポート。
-   ローカル ディスクまたは Amazon S3 ストレージからのデータの読み取り。詳細については、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。

## TiDB Lightningはスキーマとテーブルの作成をスキップできますか? {#could-tidb-lightning-skip-creating-schema-and-tables}

v5.1 から、 TiDB Lightningはダウンストリームのスキーマとテーブルを自動的に認識できるようになりました。 v5.1 より前のTiDB Lightningを使用している場合は、 `tidb-lightning.toml`の`[mydumper]`セクションに`no-schema = true`を設定する必要があります。これにより、 TiDB Lightningは`CREATE TABLE`の呼び出しをスキップし、メタデータをターゲット データベースから直接フェッチします。テーブルが実際に欠落している場合、 TiDB Lightningはエラーで終了します。

## 厳密な SQL モードを無効にして、無効なデータをインポートできるようにすることはできますか? {#can-the-strict-sql-mode-be-disabled-to-allow-importing-invalid-data}

はい。デフォルトでは、 TiDB Lightningで使用される[`sql_mode`](https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html)は`"STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"`であり、日付`1970-00-00`などの無効なデータは許可されません。モードは、 `tidb-lightning.toml`の`[tidb]`セクションの`sql-mode`の設定を変更することで変更できます。

```toml
...
[tidb]
sql-mode = ""
...
```

## 1 つの<code>tikv-importer</code> importer で複数の<code>tidb-lightning</code>インスタンスを処理できますか? {#can-one-code-tikv-importer-code-serve-multiple-code-tidb-lightning-code-instances}

はい、すべてのインスタンスが異なるテーブルで`tidb-lightning`する限り。

## <code>tikv-importer</code>プロセスを停止するには? {#how-to-stop-the-code-tikv-importer-code-process}

`tikv-importer`のプロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動デプロイの場合: `tikv-importer`がフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tikv-importer`コマンドを使用してプロセス ID を取得し、 `kill ${PID}`コマンドを使用してプロセスを終了します。

## <code>tidb-lightning</code>プロセスを停止するには? {#how-to-stop-the-code-tidb-lightning-code-process}

`tidb-lightning`のプロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動デプロイの場合: `tidb-lightning`がフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tidb-lighting`コマンドを使用してプロセス ID を取得し、 `kill -2 ${PID}`コマンドを使用してプロセスを終了します。

## バックグラウンドで実行中に<code>tidb-lightning</code>プロセスが突然終了するのはなぜですか? {#why-the-code-tidb-lightning-code-process-suddenly-quits-while-running-in-background}

これは、 `tidb-lightning`を誤って開始したことが原因である可能性があり、システムが SIGHUP シグナルを送信して`tidb-lightning`プロセスを停止させます。この状況では、通常、 `tidb-lightning.log`は次のログを出力します。

```
[2018/08/10 07:29:08.310 +08:00] [INFO] [main.go:41] ["got signal to exit"] [signal=hangup]
```

コマンドラインで`nohup`を直接使用して`tidb-lightning`を開始することはお勧めしません。スクリプトを実行することで[`tidb-lightning`開始](/tidb-lightning/deploy-tidb-lightning.md#step-3-start-tidb-lightning)できます。

また、 TiDB Lightningの最後のログでエラーが「コンテキストがキャンセルされました」と表示された場合は、最初の「ERROR」レベルのログを検索する必要があります。通常、この「エラー」レベルのログの後には「終了するシグナルがありました」が続きます。これは、 TiDB Lightningが割り込みシグナルを受信して終了したことを示します。

## TiDB Lightningを使用した後、私の TiDB クラスターが大量の CPU リソースを使用し、実行速度が非常に遅いのはなぜですか? {#why-my-tidb-cluster-is-using-lots-of-cpu-resources-and-running-very-slowly-after-using-tidb-lightning}

`tidb-lightning`が異常終了した場合、クラスターは本番環境に適していない「インポート モード」でスタックしている可能性があります。現在のモードは、次のコマンドを使用して取得できます。

{{< copyable "" >}}

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

次のコマンドを使用して、クラスターを強制的に「通常モード」に戻すことができます。

{{< copyable "" >}}

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

## TiDB Lightningは 1 ギガビット ネットワーク カードで使用できますか? {#can-tidb-lightning-be-used-with-1-gigabit-network-card}

TiDB Lightningツールセットは、10 ギガビット ネットワーク カードでの使用に最適です。特に`tikv-importer`の場合、1 ギガビット ネットワーク カードは*推奨されません*。

1 ギガビット ネットワーク カードは、合計 120 MB/秒の帯域幅しか提供できず、これをすべてのターゲット TiKV ストアで共有する必要があります。 TiDB Lightningは、1 ギガビット ネットワークのすべての帯域幅を簡単に飽和させ、PD に接続できなくなるため、クラスターをダウンさせる可能性があります。

## TiDB Lightningが対象の TiKV クラスタに大量の空き容量を必要とするのはなぜですか? {#why-tidb-lightning-requires-so-much-free-space-in-the-target-tikv-cluster}

3 つのレプリカのデフォルト設定では、ターゲット TiKV クラスターのスペース要件は、データ ソースのサイズの 6 倍です。次の要因がデータ ソースに反映されていないため、余分な &quot;2&quot; の倍数は保守的な見積もりです。

-   インデックスが占めるスペース
-   RocksDB での空間増幅

## TiDB Lightningの実行中に TiKV Importer を再起動できますか? {#can-tikv-importer-be-restarted-while-tidb-lightning-is-running}

いいえ。TiKV Importer は、エンジンの一部の情報をメモリに保存します。 `tikv-importer`を再起動すると、 `tidb-lightning`は接続が失われたために停止します。この時点で、これらの TiKV Importer 固有の情報が失われるため、 [失敗したチェックポイントを破棄する](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)にする必要があります。TiDB Lightningを再起動できます。

正しい順序については、 [TiDB Lightningを適切に再起動するには?](#how-to-properly-restart-tidb-lightning)も参照してください。

## TiDB Lightningに関連するすべての中間データを完全に破棄するには? {#how-to-completely-destroy-all-intermediate-data-associated-with-tidb-lightning}

1.  チェックポイント ファイルを削除します。

    {{< copyable "" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-remove=all
    ```

    何らかの理由でこのコマンドを実行できない場合は、手動でファイルを削除してみてください`/tmp/tidb_lightning_checkpoint.pb` 。

2.  Local-backend を使用している場合は、構成で`sorted-kv-dir`のディレクトリを削除します。 Importer-backend を使用している場合は、 `tikv-importer`をホストしているマシンの`import`ディレクトリ全体を削除します。

3.  必要に応じて、TiDB クラスターで作成されたすべてのテーブルとデータベースを削除します。

4.  残りのメタデータをクリーンアップします。次のいずれかの条件が存在する場合は、メタデータ スキーマを手動でクリーンアップする必要があります。

    -   TiDB Lightning v5.1.x および v5.2.x バージョンの場合、 `tidb-lightning-ctl`コマンドはターゲット クラスターのメタデータ スキーマをクリーンアップしません。手動でクリーンアップする必要があります。
    -   チェックポイント ファイルを手動で削除した場合は、ダウンストリーム メタデータ スキーマを手動でクリーンアップする必要があります。そうしないと、後続のインポートの正確性が影響を受ける可能性があります。

    次のコマンドを使用して、メタデータをクリーンアップします。

    {{< copyable "" >}}

    ```sql
    DROP DATABASE IF EXISTS `lightning_metadata`;
    ```

## TiDB Lightningが「 <code>could not find first pair, this shouldn&#39;t happen</code> 」というエラーを報告するのはなぜですか? {#why-does-tidb-lightning-report-the-code-could-not-find-first-pair-this-shouldn-t-happen-code-error}

このエラーは、TiDB Lightning がソートされたローカル ファイルを読み取るときに、 TiDB Lightning TiDB Lightningによって開かれたファイルの数がシステムの制限を超えたために発生する可能性があります。 Linux システムでは、 `ulimit -n`コマンドを使用して、このシステム制限の値が小さすぎるかどうかを確認できます。インポート中にこの値を`1000000` ( `ulimit -n 1000000` ) に調整することをお勧めします。

## インポート速度が遅すぎる {#import-speed-is-too-slow}

通常、 TiDB Lightningが 256 MB のデータ ファイルをインポートするには、スレッドごとに 2 分かかります。速度がこれより大幅に遅い場合は、エラーがあります。 `restore chunk … takes`に言及しているログから、各データ ファイルにかかった時間を確認できます。これは、Grafana のメトリクスからも確認できます。

TiDB Lightningが遅くなる理由はいくつかあります。

**原因 1** : `region-concurrency`の設定が高すぎるため、スレッドの競合が発生し、パフォーマンスが低下します。

1.  設定は、ログの先頭から`region-concurrency`を検索して見つけることができます。
2.  TiDB Lightningが他のサービス (TiKV Importer など) と同じマシンを共有している場合、 `region-concurrency`を CPU コアの総数の 75% に**手動で**設定する必要があります。
3.  CPU にクォータがある場合 (たとえば、Kubernetes の設定によって制限されている場合)、 TiDB Lightningはこれを読み取ることができない場合があります。この場合、 `region-concurrency`も**手動で**減らす必要があります。

**原因 2** : テーブル スキーマが複雑すぎます。

インデックスを追加するたびに、行ごとに新しい KV ペアが導入されます。 N 個のインデックスがある場合、インポートされる実際のサイズはDumpling出力のサイズの約 (N+1) 倍になります。インデックスが無視できる場合は、最初にそれらをスキーマから削除し、インポートの完了後に`CREATE INDEX`を使用してそれらを追加し直すことができます。

**原因 3** : 各ファイルが大きすぎます。

TiDB Lightningは、データ ソースが約 256 MB のサイズの複数のファイルに分割され、データを並列処理できる場合に最適に機能します。各ファイルが大きすぎると、 TiDB Lightningが応答しない場合があります。

データ ソースが CSV で、すべての CSV ファイルに改行制御文字 (U+000A および U+000D) を含むフィールドがない場合は、「厳密な形式」をオンにして、 TiDB Lightningが大きなファイルを自動的に分割できるようにすることができます。

```toml
[mydumper]
strict-format = true
```

**原因 4** : TiDB Lightningが古すぎる。

最新バージョンをお試しください！たぶん、新しい速度の改善があります。

## <code>checksum failed: checksum mismatched remote vs local</code> {#code-checksum-failed-checksum-mismatched-remote-vs-local-code}

**原因**: ローカル データ ソースとリモート インポート データベースのテーブルのチェックサムが異なります。このエラーには、いくつかのより深い理由があります。 `checksum mismatched`を含むログを確認することで、理由をさらに突き止めることができます。

`checksum mismatched`を含む行は、情報`total_kvs: x vs y`を提供します。ここで、 `x`は、インポートの完了後にターゲット クラスターによって計算されたキーと値のペア (KV ペア) の数を示し、 `y`は、ローカル データによって生成されたキーと値のペアの数を示します。ソース。

-   `x`が大きい場合、ターゲット クラスタに KV ペアが多いことを意味します。
    -   インポート前にこのテーブルが空でない可能性があるため、データ チェックサムに影響します。 TiDB Lightningが以前に失敗してシャットダウンしたが、正しく再起動しなかった可能性もあります。
-   `y`が大きい場合、ローカル データ ソースに KV ペアが多いことを意味します。
    -   ターゲット データベースのチェックサムがすべて 0 の場合は、インポートが行われていないことを意味します。クラスタがビジー状態でデータを受信できない可能性があります。
    -   エクスポートされたデータに、値が重複する UNIQUE および PRIMARY KEY などの重複データが含まれている可能性や、データでは大文字と小文字が区別されているのに、下流のテーブル構造では大文字と小文字が区別されない可能性があります。
-   その他の考えられる理由
    -   データ ソースが機械で生成され、 Dumplingによってバックアップされていない場合は、データがテーブルの制限に準拠していることを確認してください。たとえば、AUTO_INCREMENT 列は 0 ではなく正である必要があります。

**ソリューション**:

1.  `tidb-lightning-ctl`を使用して破損したデータを削除し、テーブル構造とデータを確認してから、 TiDB Lightningを再起動して、影響を受けたテーブルを再度インポートします。

    {{< copyable "" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

2.  外部データベースを使用してチェックポイント (変更`[checkpoint] dsn` ) を格納し、ターゲット データベースの負荷を軽減することを検討してください。

3.  TiDB Lightningが不適切に再起動された場合は、 FAQの「 [TiDB Lightningを適切に再起動する方法](#how-to-properly-restart-tidb-lightning) 」セクションも参照してください。

## <code>Checkpoint for … has invalid status:</code> (エラー コード) {#code-checkpoint-for-has-invalid-status-code-error-code}

**原因**: [チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)が有効になっていて、 TiDB Lightningまたは TiKV Importer が以前に異常終了しました。偶発的なデータ破損を防ぐために、 TiDB Lightningはエラーが解決されるまで起動しません。

エラー コードは 25 より小さい整数で、可能な値は 0、3、6、9、12、14、15、17、18、20、および 21 です。整数は、インポートで予期しない終了が発生したステップを示します。処理する。整数が大きいほど、出口が発生する後のステップです。

**ソリューション**:

エラーの原因が無効なデータ ソースである場合は、 `tidb-lightning-ctl`を使用してインポートされたデータを削除し、Lightning を再起動します。

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

その他のオプションについては、セクション[チェックポイント制御](/tidb-lightning/tidb-lightning-checkpoints.md#checkpoints-control)を参照してください。

## <code>ResourceTemporarilyUnavailable("Too many open engines …: …")</code> {#code-resourcetemporarilyunavailable-too-many-open-engines-code}

**原因**: 同時実行エンジン ファイルの数が、 `tikv-importer`で指定された制限を超えています。これは、設定ミスが原因である可能性があります。さらに、 `tidb-lightning`が異常終了した場合、エンジン ファイルがダングリング オープン状態のままになる可能性があり、これもこのエラーを引き起こす可能性があります。

**ソリューション**:

1.  `tikv-importer.toml`の`max-open-engines`の設定値を大きくします。この値は通常、使用可能なメモリによって決まります。これは、次を使用して計算できます。

    最大メモリ使用量 ≈ `max-open-engines` × `write-buffer-size` × `max-write-buffer-number`

2.  `table-concurrency` + `index-concurrency`の値を減らして`max-open-engines`未満にします。

3.  `tikv-importer`を再起動して、すべてのエンジン ファイルを強制的に削除します (デフォルトは`./data.import/` )。これにより、部分的にインポートされたすべてのテーブルも削除されるため、 TiDB Lightningは古いチェックポイントをクリアする必要があります。

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

## <code>cannot guess encoding for input file, please convert to UTF-8 manually</code> {#code-cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually-code}

**原因**: TiDB Lightningは、テーブル スキーマの UTF-8 および GB-18030 エンコーディングのみを認識します。このエラーは、ファイルがこれらのエンコーディングのいずれでもない場合に発生します。過去`ALTER TABLE`の実行により、UTF-8 の文字列と GB-18030 の別の文字列が含まれているなど、ファイルにエンコーディングが混在している可能性もあります。

**ソリューション**:

1.  ファイル全体が UTF-8 または GB-18030 になるようにスキーマを修正します。

2.  ターゲット データベース内の影響を受けるテーブルを手動で`CREATE`します。

3.  チェックをスキップするには、 `[mydumper] character-set = "binary"`を設定します。これにより、対象データベースにモジバケが導入される可能性があることに注意してください。

## <code>[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 …}'</code> {#code-sql2kv-sql-encode-error-types-1292-invalid-time-format-1970-1-1-code}

**原因**: 表に`timestamp`型の列が含まれていますが、時間値自体が存在しません。これは、DST の変更が原因であるか、時間の値がサポートされている範囲 (1970 年 1 月 1 日から 2038 年 1 月 19 日) を超えたことが原因です。

**ソリューション**:

1.  TiDB Lightningとソース データベースが同じタイム ゾーンを使用していることを確認します。

    TiDB Lightningを直接実行する場合、 `$TZ`環境変数を使用してタイムゾーンを強制できます。

    ```sh
    # Manual deployment, and force Asia/Shanghai.
    TZ='Asia/Shanghai' bin/tidb-lightning -config tidb-lightning.toml
    ```

2.  Mydumper を使用してデータをエクスポートする場合は、必ず`--skip-tz-utc`フラグを含めてください。

3.  クラスター全体が同じ最新バージョンの`tzdata` (バージョン 2018i 以降) を使用していることを確認します。

    CentOS では、 `yum info tzdata`を実行して、インストールされているバージョンと更新があるかどうかを確認します。 `yum upgrade tzdata`を実行してパッケージをアップグレードします。

## <code>[Error 8025: entry too large, the max entry size is 6291456]</code> {#code-error-8025-entry-too-large-the-max-entry-size-is-6291456-code}

**原因**: TiDB Lightningによって生成されたキーと値のペアの単一行が、TiDB によって設定された制限を超えています。

**解決策**:

現在、TiDB の制限を回避することはできません。他のテーブルを正常にインポートするには、このテーブルのみを無視できます。

## <code>rpc error: code = Unimplemented ...</code> TiDB Lightningがモードを切り替えたとき {#encounter-code-rpc-error-code-unimplemented-code-when-tidb-lightning-switches-the-mode}

**原因**: クラスタ内の一部のノードが`switch-mode`をサポートしていません。たとえば、TiFlash のバージョンが`v4.0.0-rc.2`より前の場合、 [`switch-mode`はサポートされていません](https://github.com/pingcap/tidb-lightning/issues/273) .

**ソリューション**:

-   クラスターに TiFlash ノードがある場合は、クラスターを`v4.0.0-rc.2`以上のバージョンに更新できます。
-   クラスタをアップグレードしない場合は、TiFlash を一時的に無効にします。

## <code>tidb lightning encountered error: TiDB version too old, expected '>=4.0.0', found '3.0.18'</code> {#code-tidb-lightning-encountered-error-tidb-version-too-old-expected-4-0-0-found-3-0-18-code}

TiDB Lightning Local-backend は、v4.0.0 以降のバージョンの TiDB クラスターへのデータのインポートのみをサポートします。 Local-backend を使用して v2.x または v3.x クラスターにデータをインポートしようとすると、上記のエラーが報告されます。この時点で、データのインポートに Importer バックエンドまたは TiDB バックエンドを使用するように構成を変更できます。

一部の`nightly`バージョンは v4.0.0-beta.2 に類似している可能性があります。これら`nightly`のバージョンのTiDB Lightningは、実際には Local-backend をサポートしています。 `nightly`バージョンを使用しているときにこのエラーが発生した場合は、構成を`check-requirements = false`に設定してバージョン チェックをスキップできます。このパラメータを設定する前に、 TiDB Lightningの設定が対応するバージョンをサポートしていることを確認してください。そうしないと、インポートが失敗する可能性があります。

## <code>restore table test.district failed: unknown columns in header [...]</code> {#code-restore-table-test-district-failed-unknown-columns-in-header-code}

このエラーは通常、CSV データ ファイルにヘッダーが含まれていないために発生します (最初の行は列名ではなくデータです)。したがって、次の構成をTiDB Lightning構成ファイルに追加する必要があります。

```
[mydumper.csv]
header = false
```

## TiDB Lightningの実行時のゴルーチン情報を取得する方法 {#how-to-get-the-runtime-goroutine-information-of-tidb-lightning}

1.  TiDB Lightningの設定ファイルに[`status-port`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-configuration)が指定されている場合は、この手順をスキップしてください。それ以外の場合は、 USR1 シグナルをTiDB Lightningに送信して`status-port`を有効にする必要があります。

    `ps`などのコマンドを使用してTiDB Lightningのプロセス ID (PID) を取得し、次のコマンドを実行します。

    {{< copyable "" >}}

    ```sh
    kill -USR1 <lightning-pid>
    ```

    TiDB Lightningのログを確認してください。 `starting HTTP server`のログは、新しく有効になった`status-port`を示して`started HTTP server` `start HTTP server` 。

2.  `http://<lightning-ip>:<status-port>/debug/pprof/goroutine?debug=2`にアクセスして、ゴルーチン情報を取得します。
