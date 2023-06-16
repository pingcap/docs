---
title: TiDB Lightning FAQs
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Lightning.
---

# TiDB Lightningよくある質問 {#tidb-lightning-faqs}

## TiDB Lightningでサポートされる TiDB/TiKV/PD クラスターの最小バージョンは何ですか? {#what-is-the-minimum-tidb-tikv-pd-cluster-version-supported-by-tidb-lightning}

TiDB Lightningのバージョンはクラスターと同じである必要があります。ローカル バックエンド モードを使用する場合、利用可能な最も古いバージョンは 4.0.0 です。インポーター バックエンド モードまたは TiDB バックエンド モードを使用する場合、利用可能な最も古いバージョンは 2.0.9 ですが、安定バージョン 3.0 を使用することをお勧めします。

## TiDB Lightning は複数のスキーマ (データベース) のインポートをサポートしていますか? {#does-tidb-lightning-support-importing-multiple-schemas-databases}

はい。

## ターゲットデータベースの権限要件は何ですか? {#what-are-the-privilege-requirements-for-the-target-database}

TiDB Lightning には次の権限が必要です。

-   選択する
-   アップデート
-   変更
-   作成
-   落とす

[<a href="/tidb-lightning/tidb-lightning-backends.md#tidb-lightning-tidb-backend">TiDB バックエンド</a>](/tidb-lightning/tidb-lightning-backends.md#tidb-lightning-tidb-backend)が選択されている場合、またはターゲット データベースがチェックポイントの保存に使用されている場合は、さらに次の権限が必要です。

-   入れる
-   消去

データは TiKV に直接取り込まれ、TiDB 権限システム全体がバイパスされるため、ローカル バックエンドとインポーター バックエンドにはこれら 2 つの権限は必要ありません。 TiKV、TiKV Importer、およびTiDB Lightningのポートがクラスターの外部に到達できない限り、これは安全です。

TiDB Lightningの`checksum`構成が`true`に設定されている場合、ダウンストリーム TiDB の管理者ユーザー権限をTiDB Lightningに付与する必要があります。

## TiDB Lightning で1 つのテーブルをインポート中にエラーが発生しました。他のテーブルに影響はありますか?プロセスは終了しますか? {#tidb-lightning-encountered-an-error-when-importing-one-table-will-it-affect-other-tables-will-the-process-be-terminated}

1 つのテーブルのみでエラーが発生した場合でも、残りのテーブルは通常どおり処理されます。

## TiDB Lightning を適切に再起動するにはどうすればよいですか? {#how-to-properly-restart-tidb-lightning}

Importer-backend を使用している場合、 `tikv-importer`のステータスに応じて、 TiDB Lightningを再起動する基本的なシーケンスは次のようになります。

`tikv-importer`がまだ実行中の場合:

1.  [<a href="#how-to-stop-the-tidb-lightning-process">`tidb-lightning`やめる</a>](#how-to-stop-the-tidb-lightning-process) 。
2.  ソースデータの修正、設定の変更、ハードウェアの交換など、意図した変更を実行します。
3.  以前の変更によってテーブルが変更されている場合は、 [<a href="/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-remove">対応するチェックポイントを削除します</a>](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-remove)も追加されます。
4.  `tidb-lightning`を開始します。

`tikv-importer`を再起動する必要がある場合:

1.  [<a href="#how-to-stop-the-tidb-lightning-process">`tidb-lightning`やめる</a>](#how-to-stop-the-tidb-lightning-process) 。
2.  [<a href="#how-to-stop-the-tikv-importer-process">`tikv-importer`停止する</a>](#how-to-stop-the-tikv-importer-process) 。
3.  ソースデータの修正、設定の変更、ハードウェアの交換など、意図した変更を実行します。
4.  `tikv-importer`を開始します。
5.  `tidb-lightning`を開始し*、CHECKSUM エラー (存在する場合) でプログラムが失敗するまで待ちます*。
    -   `tikv-importer`を再起動すると、まだ書き込まれているすべてのエンジン ファイルが破壊されますが、 `tidb-lightning`それを知りませんでした。 v3.0 では、最も簡単な方法は`tidb-lightning`を続行して再試行することです。
6.  [<a href="#checkpoint-for--has-invalid-status-error-code">失敗したテーブルとチェックポイントを破棄します</a>](#checkpoint-for--has-invalid-status-error-code)
7.  もう一度`tidb-lightning`から始めます。

Local-backend または TiDB-backend を使用している場合、操作は`tikv-importer`がまだ実行中の場合に Importer-backend を使用する場合と同じです。

## インポートされたデータの整合性を確保するにはどうすればよいですか? {#how-to-ensure-the-integrity-of-the-imported-data}

TiDB Lightning はデフォルトで、ローカル データ ソースとインポートされたテーブルに対してチェックサムを実行します。チェックサムが一致しない場合、プロセスは中止されます。これらのチェックサム情報はログから読み取ることができます。

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

## TiDB Lightningではどのような種類のデータ ソース形式がサポートされていますか? {#what-kinds-of-data-source-formats-are-supported-by-tidb-lightning}

TiDB Lightningは以下をサポートします。

-   [<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md) 、CSVファイル、 [<a href="/migrate-aurora-to-tidb.md">Amazon Auroraによって生成された Apache Parquet ファイル</a>](/migrate-aurora-to-tidb.md)でエクスポートしたファイルをインポートします。
-   ローカル ディスクまたは Amazon S3storageからのデータの読み取り。詳細は[<a href="/br/backup-and-restore-storages.md">外部ストレージ</a>](/br/backup-and-restore-storages.md)を参照してください。

## TiDB Lightning はスキーマとテーブルの作成をスキップできますか? {#could-tidb-lightning-skip-creating-schema-and-tables}

はい。ターゲット データベースにテーブルをすでに作成している場合は、 `tidb-lightning.toml`の`[mydumper]`セクションに`no-schema = true`を設定できます。これにより、 TiDB Lightning は`CREATE TABLE`の呼び出しをスキップし、ターゲット データベースから直接メタデータをフェッチします。実際にテーブルが欠落している場合、 TiDB Lightning はエラーで終了します。

## 厳密 SQL モードを無効にして、無効なデータをインポートできるようにすることはできますか? {#can-the-strict-sql-mode-be-disabled-to-allow-importing-invalid-data}

はい。デフォルトでは、 TiDB Lightningで使用される[<a href="https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html">`sql_mode`</a>](https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html) `"STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"`で、日付`1970-00-00`などの無効なデータは許可されません。モードは、 `tidb-lightning.toml`の`[tidb]`セクションの`sql-mode`設定を変更することで変更できます。

```toml
...
[tidb]
sql-mode = ""
...
```

## 1 つの<code>tikv-importer</code>複数の<code>tidb-lightning</code>インスタンスに対応できますか? {#can-one-code-tikv-importer-code-serve-multiple-code-tidb-lightning-code-instances}

はい、 `tidb-lightning`のインスタンスごとに異なるテーブルで動作する限り、可能です。

## <code>tikv-importer</code>プロセスを停止するにはどうすればよいですか? {#how-to-stop-the-code-tikv-importer-code-process}

`tikv-importer`プロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動デプロイメントの場合: `tikv-importer`がフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tikv-importer`コマンドを使用してプロセス ID を取得し、 `kill ${PID}`コマンドを使用してプロセスを終了します。

## <code>tidb-lightning</code>プロセスを停止するにはどうすればよいですか? {#how-to-stop-the-code-tidb-lightning-code-process}

`tidb-lightning`プロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動デプロイメントの場合: `tidb-lightning`がフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tidb-lighting`コマンドを使用してプロセス ID を取得し、 `kill -2 ${PID}`コマンドを使用してプロセスを終了します。

## <code>tidb-lightning</code>プロセスがバックグラウンドで実行中に突然終了するのはなぜですか? {#why-the-code-tidb-lightning-code-process-suddenly-quits-while-running-in-background}

これは、 `tidb-lightning`間違って開始したことが原因である可能性があり、そのためシステムが SIGHUP シグナルを送信して`tidb-lightning`プロセスを停止させます。この状況では、通常、 `tidb-lightning.log`次のログを出力します。

```
[2018/08/10 07:29:08.310 +08:00] [INFO] [main.go:41] ["got signal to exit"] [signal=hangup]
```

コマンドラインで`nohup`直接使用して`tidb-lightning`を開始することはお勧めできません。 [<a href="/tidb-lightning/deploy-tidb-lightning.md#step-3-start-tidb-lightning">`tidb-lightning`を開始する</a>](/tidb-lightning/deploy-tidb-lightning.md#step-3-start-tidb-lightning)スクリプトを実行することで実行できます。

さらに、 TiDB Lightningの最後のログでエラーが「コンテキストがキャンセルされました」であることが示されている場合は、最初の「ERROR」レベルのログを検索する必要があります。通常、この「ERROR」レベルのログの後には「終了する信号を取得しました」というメッセージが続きます。これは、 TiDB Lightning が割り込み信号を受信して​​終了したことを示します。

## TiDB Lightning を使用した後、TiDB クラスターが大量の CPU リソースを使用し、動作が非常に遅くなるのはなぜですか? {#why-my-tidb-cluster-is-using-lots-of-cpu-resources-and-running-very-slowly-after-using-tidb-lightning}

`tidb-lightning`が異常終了した場合、クラスターは本番には適さない「インポート モード」でスタックする可能性があります。現在のモードは、次のコマンドを使用して取得できます。

{{< copyable "" >}}

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

次のコマンドを使用して、クラスターを強制的に「通常モード」に戻すことができます。

{{< copyable "" >}}

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

## TiDB Lightning は1 ギガビット ネットワーク カードで使用できますか? {#can-tidb-lightning-be-used-with-1-gigabit-network-card}

TiDB Lightningツールセットは、10 ギガビット ネットワーク カードと併用するのが最適です。 1 ギガビット ネットワーク カードは、特に`tikv-importer`では*推奨されません*。

1 ギガビット ネットワーク カードは合計 120 MB/秒の帯域幅しか提供できず、これをすべてのターゲット TiKV ストアで共有する必要があります。 TiDB Lightning は、 1 ギガビット ネットワークのすべての帯域幅を簡単に飽和させ、PD に接続できなくなるため、クラスターをダウンさせる可能性があります。これを回避するには、 [<a href="/tidb-lightning/tidb-lightning-configuration.md#tikv-importer">インポーターの設定</a>](/tidb-lightning/tidb-lightning-configuration.md#tikv-importer)で*アップロード速度制限*を設定します。

```toml
[import]
# Restricts the total upload speed to TiKV to 100 MB/s or less
upload-speed-limit = "100MB"
```

## TiDB Lightning がターゲット TiKV クラスターにこれほど多くの空き領域を必要とするのはなぜですか? {#why-tidb-lightning-requires-so-much-free-space-in-the-target-tikv-cluster}

デフォルト設定の 3 つのレプリカでは、ターゲット TiKV クラスターのスペース要件はデータ ソースのサイズの 6 倍になります。次の要素がデータ ソースに反映されていないため、「2」の余分な倍数は控えめな推定値です。

-   インデックスが占めるスペース
-   RocksDB の空間増幅

## TiDB Lightningの実行中に TiKV Importer を再起動できますか? {#can-tikv-importer-be-restarted-while-tidb-lightning-is-running}

いいえ。TiKV インポーターはエンジンの一部の情報をメモリに保存します。 `tikv-importer`を再起動すると、 `tidb-lightning`接続が失われたため停止します。この時点で、TiKV Importer 固有の情報が失われるため、 [<a href="/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy">失敗したチェックポイントを破棄する</a>](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)を行う必要があります。後でTiDB Lightningを再起動できます。

正しい順序については[<a href="#how-to-properly-restart-tidb-lightning">TiDB Lightning を適切に再起動するにはどうすればよいですか?</a>](#how-to-properly-restart-tidb-lightning)も参照してください。

## TiDB Lightningに関連付けられたすべての中間データを完全に破棄するにはどうすればよいですか? {#how-to-completely-destroy-all-intermediate-data-associated-with-tidb-lightning}

1.  チェックポイントファイルを削除します。

    {{< copyable "" >}}

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

    {{< copyable "" >}}

    ```sql
    DROP DATABASE IF EXISTS `lightning_metadata`;
    ```

## TiDB Lightning が<code>could not find first pair, this shouldn&#39;t happen</code> 」というエラーを報告するのはなぜですか? {#why-does-tidb-lightning-report-the-code-could-not-find-first-pair-this-shouldn-t-happen-code-error}

このエラーは、 TiDB Lightningがソートされたローカル ファイルを読み取るときに、 TiDB Lightningによって開かれたファイルの数がシステム制限を超えたために発生する可能性があります。 Linux システムでは、 `ulimit -n`コマンドを使用して、このシステム制限の値が小さすぎるかどうかを確認できます。インポート中にこの値を`1000000` ( `ulimit -n 1000000` ) に調整することをお勧めします。

## インポート速度が遅すぎる {#import-speed-is-too-slow}

通常、 TiDB Lightning で256 MB データ ファイルをインポートするには、スレッドごとに 2 分かかります。速度がこれより大幅に遅い場合は、エラーが発生します。各データ ファイルにかかった時間は、 `restore chunk … takes`のログから確認できます。これは、Grafana のメトリクスからも観察できます。

TiDB Lightning が遅くなる理由はいくつかあります。

**原因 1** : `region-concurrency`の設定が高すぎるため、スレッドの競合が発生し、パフォーマンスが低下します。

1.  設定は、ログの先頭から検索`region-concurrency`で見つけることができます。
2.  TiDB Lightning が他のサービス (TiKV Importer など) と同じマシンを共有する場合、CPU コアの総数の 75% に`region-concurrency`を**手動で**設定する必要があります。
3.  CPU にクォータがある場合 (たとえば、Kubernetes 設定によって制限されている場合)、 TiDB Lightning はこれを読み取れない可能性があります。この場合、**手動で**`region-concurrency`を減らす必要もあります。

**原因 2** : テーブル スキーマが複雑すぎます。

インデックスを追加するたびに、行ごとに新しい KV ペアが導入されます。 N 個のインデックスがある場合、インポートされる実際のサイズは、 Dumpling出力のサイズの約 (N+1) 倍になります。インデックスが無視できる場合は、まずスキーマからインデックスを削除し、インポートが完了した後に`CREATE INDEX`を使用して追加し直すことができます。

**原因3** ：各ファイルが大きすぎます。

TiDB Lightning は、データを並行して処理できるように、データ ソースがサイズ約 256 MB の複数のファイルに分割されている場合に最適に機能します。各ファイルが大きすぎる場合、 TiDB Lightning が応答しない可能性があります。

データ ソースが CSV で、すべての CSV ファイルに改行制御文字 (U+000A および U+000D) を含むフィールドがない場合、「厳密な形式」をオンにして、 TiDB Lightning が大きなファイルを自動的に分割できるようにすることができます。

```toml
[mydumper]
strict-format = true
```

**原因 4** : TiDB Lightning が古すぎます。

最新バージョンをお試しください!もしかしたら新たな速度向上があるかもしれません。

## <code>checksum failed: checksum mismatched remote vs local</code> {#code-checksum-failed-checksum-mismatched-remote-vs-local-code}

**原因**: ローカル データ ソースとリモート インポートされたデータベースのテーブルのチェックサムが異なります。このエラーにはいくつかの深い理由があります。 `checksum mismatched`を含むログを確認すると、さらに原因を特定できます。

`checksum mismatched`を含む行は情報`total_kvs: x vs y`提供します。ここで、 `x`インポート完了後にターゲット クラスターによって計算されたキーと値のペア (KV ペア) の数を示し、 `y`ローカル データによって生成されたキーと値のペアの数を示します。ソース。

-   `x`が大きい場合は、ターゲット クラスター内により多くの KV ペアが存在することを意味します。
    -   インポート前にこのテーブルが空ではない可能性があり、そのためデータのチェックサムに影響を与えます。 TiDB Lightning が以前に失敗してシャットダウンしたが、正しく再起動されなかった可能性もあります。
-   `y`が大きい場合は、ローカル データ ソースに多くの KV ペアがあることを意味します。
    -   ターゲット データベースのチェックサムがすべて 0 の場合は、インポートが行われていないことを意味します。クラスターがビジー状態でデータを受信できない可能性があります。
    -   エクスポートされたデータには、重複した値を持つ UNIQUE キーと PRIMARY KEY などの重複データが含まれているか、データは大文字と小文字が区別されるが、ダウンストリーム テーブル構造では大文字と小文字が区別されない可能性があります。
-   その他考えられる理由
    -   データ ソースが機械生成され、 Dumplingによってバックアップされていない場合は、データがテーブルの制限に準拠していることを確認してください。たとえば、AUTO_INCREMENT 列は 0 ではなく、正の値である必要があります。

**解決策**:

1.  `tidb-lightning-ctl`を使用して破損したデータを削除し、テーブル構造とデータを確認して、 TiDB Lightningを再起動して影響を受けるテーブルを再度インポートします。

    {{< copyable "" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

2.  ターゲット データベースの負荷を軽減するために、外部データベースを使用してチェックポイント (変更`[checkpoint] dsn` ) を保存することを検討してください。

3.  TiDB Lightning が不適切に再起動された場合は、 FAQの「 [<a href="#how-to-properly-restart-tidb-lightning">TiDB Lightning を適切に再起動する方法</a>](#how-to-properly-restart-tidb-lightning) 」セクションも参照してください。

## <code>Checkpoint for … has invalid status:</code> (エラー コード) {#code-checkpoint-for-has-invalid-status-code-error-code}

**原因**: [<a href="/tidb-lightning/tidb-lightning-checkpoints.md">チェックポイント</a>](/tidb-lightning/tidb-lightning-checkpoints.md)が有効になっており、 TiDB Lightningまたは TiKV Importer が以前に異常終了しました。偶発的なデータ破損を防ぐため、エラーが解決されるまでTiDB Lightning は起動しません。

エラー コードは 25 より小さい整数で、取り得る値は 0、3、6、9、12、14、15、17、18、20、および 21 です。整数は、インポートで予期しない終了が発生したステップを示します。プロセス。整数が大きいほど、終了は後のステップで発生します。

**解決策**:

エラーの原因が無効なデータソースである場合は、 `tidb-lightning-ctl`使用してインポートされたデータを削除し、Lightning を再起動します。

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

他のオプションについては、 [<a href="/tidb-lightning/tidb-lightning-checkpoints.md#checkpoints-control">チェックポイント制御</a>](/tidb-lightning/tidb-lightning-checkpoints.md#checkpoints-control)セクションを参照してください。

## <code>ResourceTemporarilyUnavailable("Too many open engines …: …")</code> {#code-resourcetemporarilyunavailable-too-many-open-engines-code}

**原因**: 同時エンジン ファイルの数が`tikv-importer`で指定された制限を超えています。これは構成ミスが原因である可能性があります。さらに、 `tidb-lightning`異常終了した場合、エンジン ファイルがダングリング オープン状態のままになる可能性があり、これもこのエラーの原因となる可能性があります。

**解決策**:

1.  `tikv-importer.toml`の`max-open-engines`設定の値を増やします。通常、この値は使用可能なメモリによって決まります。これは次を使用して計算できます。

    最大メモリ使用量 ≈ `max-open-engines` × `write-buffer-size` × `max-write-buffer-number`

2.  `table-concurrency` + `index-concurrency`の値を`max-open-engines`未満になるように減らします。

3.  すべてのエンジン ファイルを強制的に削除するには、 `tikv-importer`を再起動します (デフォルトは`./data.import/` )。これにより、部分的にインポートされたテーブルもすべて削除されるため、 TiDB Lightning で古いチェックポイントをクリアする必要があります。

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

## <code>cannot guess encoding for input file, please convert to UTF-8 manually</code> {#code-cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually-code}

**原因**: TiDB Lightning は、テーブル スキーマの UTF-8 および GB-18030 エンコーディングのみを認識します。このエラーは、ファイルがこれらのエンコーディングのいずれでもない場合に発生します。過去`ALTER TABLE`の実行により、ファイルに UTF-8 の文字列と GB-18030 の別の文字列が含まれるなど、エンコーディングが混在している可能性もあります。

**解決策**:

1.  ファイル全体が UTF-8 または GB-18030 になるようにスキーマを修正してください。

2.  ターゲット データベース内の影響を受けるテーブルを手動で`CREATE`設定し、自動テーブル作成をスキップするには`[mydumper] no-schema = true`を設定します。

3.  チェックをスキップするには`[mydumper] character-set = "binary"`を設定します。これにより、ターゲット データベースに mojibake が導入される可能性があることに注意してください。

## <code>[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 …}'</code> {#code-sql2kv-sql-encode-error-types-1292-invalid-time-format-1970-1-1-code}

**原因**: テーブルに`timestamp`タイプの列が含まれていますが、時刻値自体が存在しません。これは、DST の変更または時刻値がサポートされている範囲 (1970 年 1 月 1 日から 2038 年 1 月 19 日) を超えているためです。

**解決策**:

1.  TiDB Lightningとソース データベースが同じタイム ゾーンを使用していることを確認します。

    TiDB Lightningを直接実行する場合、 `$TZ`環境変数を使用してタイムゾーンを強制できます。

    ```sh
    # Manual deployment, and force Asia/Shanghai.
    TZ='Asia/Shanghai' bin/tidb-lightning -config tidb-lightning.toml
    ```

2.  Mydumper を使用してデータをエクスポートする場合は、必ず`--skip-tz-utc`フラグを含めてください。

3.  クラスター全体が同じ最新バージョン`tzdata` (バージョン 2018i 以降) を使用していることを確認します。

    CentOS では、 `yum info tzdata`を実行して、インストールされているバージョンとアップデートがあるかどうかを確認します。 `yum upgrade tzdata`を実行してパッケージをアップグレードします。

## <code>[Error 8025: entry too large, the max entry size is 6291456]</code> {#code-error-8025-entry-too-large-the-max-entry-size-is-6291456-code}

**原因**: TiDB Lightningによって生成された 1 行のキーと値のペアが、TiDB によって設定された制限を超えています。

**解決策**:

この制限を回避するには、TiDB 構成項目[<a href="/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50">`txn-entry-size-limit`</a>](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)と TiKV 構成項目[<a href="/tikv-configuration-file.md#raft-entry-max-size">`raft-entry-max-size`</a>](/tikv-configuration-file.md#raft-entry-max-size)を、インポートするデータよりも大きい値に変更して、再試行します。

## TiDB Lightning がモードを切り替えるときに<code>rpc error: code = Unimplemented ...</code> {#encounter-code-rpc-error-code-unimplemented-code-when-tidb-lightning-switches-the-mode}

**原因**: クラスター内の一部のノードは`switch-mode`をサポートしていません。たとえば、 TiFlash のバージョンが`v4.0.0-rc.2`より前の場合は、 [<a href="https://github.com/pingcap/tidb-lightning/issues/273">`switch-mode`サポートされていません</a>](https://github.com/pingcap/tidb-lightning/issues/273) 。

**解決策**:

-   クラスター内にTiFlashノードがある場合は、クラスターを`v4.0.0-rc.2`以降のバージョンに更新できます。
-   クラスターをアップグレードしたくない場合は、 TiFlash を一時的に無効にします。

## <code>tidb lightning encountered error: TiDB version too old, expected '>=4.0.0', found '3.0.18'</code> {#code-tidb-lightning-encountered-error-tidb-version-too-old-expected-4-0-0-found-3-0-18-code}

TiDB Lightning Local バックエンドは、v4.0.0 以降のバージョンの TiDB クラスターへのデータのインポートのみをサポートします。 Local-backend を使用して v2.x または v3.x クラスターにデータをインポートしようとすると、上記のエラーが報告されます。現時点では、データのインポートにインポーター バックエンドまたは TiDB バックエンドを使用するように構成を変更できます。

一部の`nightly`バージョンは v4.0.0-beta.2 に似ている可能性があります。 TiDB Lightningのこれら`nightly`のバージョンは、実際にローカル バックエンドをサポートしています。バージョン`nightly`の使用時にこのエラーが発生した場合は、構成`check-requirements = false`を設定することでバージョン チェックをスキップできます。このパラメータを設定する前に、 TiDB Lightningの設定が対応するバージョンをサポートしていることを確認してください。そうしないと、インポートが失敗する可能性があります。

## <code>restore table test.district failed: unknown columns in header [...]</code> {#code-restore-table-test-district-failed-unknown-columns-in-header-code}

このエラーは通常、CSV データ ファイルにヘッダーが含まれていないために発生します (最初の行は列名ではなくデータです)。したがって、次の設定をTiDB Lightning設定ファイルに追加する必要があります。

```
[mydumper.csv]
header = false
```

## TiDB Lightningのランタイムゴルーチン情報を取得する方法 {#how-to-get-the-runtime-goroutine-information-of-tidb-lightning}

1.  TiDB Lightningの設定ファイルで[<a href="/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-configuration">`status-port`</a>](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-configuration)が指定されている場合は、この手順をスキップしてください。それ以外の場合は、USR1 信号をTiDB Lightningに送信して`status-port`を有効にする必要があります。

    `ps`などのコマンドを使用してTiDB Lightningのプロセス ID (PID) を取得し、次のコマンドを実行します。

    {{< copyable "" >}}

    ```sh
    kill -USR1 <lightning-pid>
    ```

    TiDB Lightningのログを確認してください。 `starting HTTP server` / `start HTTP server` / `started HTTP server`のログには、新しく有効になった`status-port`が表示されます。

2.  `http://<lightning-ip>:<status-port>/debug/pprof/goroutine?debug=2`にアクセスして goroutine 情報を取得します。
