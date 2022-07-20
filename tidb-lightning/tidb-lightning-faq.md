---
title: TiDB Lightning FAQs
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Lightning.
---

# TiDB Lightning {#tidb-lightning-faqs}

## TiDBLightningでサポートされているTiDB Lightning /TiKV / PDクラスタの最小バージョンは何ですか？ {#what-is-the-minimum-tidb-tikv-pd-cluster-version-supported-by-tidb-lightning}

TiDB Lightningのバージョンは、クラスタと同じである必要があります。ローカルバックエンドモードを使用する場合、使用可能な最も古いバージョンは4.0.0です。インポーターバックエンドモードまたはTiDBバックエンドモードを使用する場合、使用可能な最も古いバージョンは2.0.9ですが、3.0安定バージョンを使用することをお勧めします。

## TiDB Lightningは複数のスキーマ（データベース）のインポートをサポートしていますか？ {#does-tidb-lightning-support-importing-multiple-schemas-databases}

はい。

## ターゲットデータベースの特権要件は何ですか？ {#what-are-the-privilege-requirements-for-the-target-database}

権限の詳細については、 [TiDB Lightningを使用するための前提条件](/tidb-lightning/tidb-lightning-requirements.md)を参照してください。

## 1つのテーブルをインポートするときにTiDB Lightningでエラーが発生しました。他のテーブルに影響しますか？プロセスは終了しますか？ {#tidb-lightning-encountered-an-error-when-importing-one-table-will-it-affect-other-tables-will-the-process-be-terminated}

1つのテーブルでエラーが発生した場合でも、残りのテーブルは通常どおり処理されます。

## TiDB Lightningを正しく再起動する方法は？ {#how-to-properly-restart-tidb-lightning}

Importer-backendを使用している場合、ステータス`tikv-importer`に応じて、 TiDB Lightningを再起動する基本的なシーケンスは次のようになります。

`tikv-importer`がまだ実行されている場合：

1.  [`tidb-lightning`停止します](#how-to-stop-the-tidb-lightning-process) 。
2.  ソースデータの修正、設定の変更、ハードウェアの交換など、目的の変更を実行します。
3.  以前に変更によってテーブルが変更された場合は、 [対応するチェックポイントを削除します](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-remove)も変更されます。
4.  `tidb-lightning`を開始します。

`tikv-importer`を再起動する必要がある場合：

1.  [`tidb-lightning`停止します](#how-to-stop-the-tidb-lightning-process) 。
2.  [`tikv-importer`停止します](#how-to-stop-the-tikv-importer-process) 。
3.  ソースデータの修正、設定の変更、ハードウェアの交換など、目的の変更を実行します。
4.  `tikv-importer`を開始します。
5.  `tidb-lightning`*を開始し、プログラムがCHECKSUMエラー（存在する場合）で失敗するまで待ちます*。
    -   `tikv-importer`を再起動すると、まだ書き込まれているすべてのエンジンファイルが破棄されますが、 `tidb-lightning`はそれを認識していませんでした。 v3.0以降、最も簡単な方法は`tidb-lightning`を続行して再試行することです。
6.  [失敗したテーブルとチェックポイントを破棄します](#checkpoint-for--has-invalid-status-error-code)
7.  もう一度`tidb-lightning`を開始します。

Local-backendまたはTiDB-backendを使用している場合、操作は、 `tikv-importer`がまだ実行されているときにImporter-backendを使用する場合と同じです。

## インポートされたデータの整合性を確保するにはどうすればよいですか？ {#how-to-ensure-the-integrity-of-the-imported-data}

TiDB Lightningは、デフォルトで、ローカルデータソースとインポートされたテーブルに対してチェックサムを実行します。チェックサムの不一致がある場合、プロセスは中止されます。これらのチェックサム情報は、ログから読み取ることができます。

ターゲットテーブルで`ADMIN CHECKSUM TABLE`コマンドを実行して、インポートされたデータのチェックサムを再計算することもできます。

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

## TiDB Lightningどのような種類のデータソース形式がサポートされていますか？ {#what-kinds-of-data-source-formats-are-supported-by-tidb-lightning}

TiDB Lightningは以下をサポートします。

-   [Dumpling](/dumpling-overview.md) 、CSVファイル、および[AmazonAuroraによって生成されたAuroraファイル](/migrate-aurora-to-tidb.md)でエクスポートされたファイルをインポートします。
-   ローカルディスクまたはAmazonS3ストレージからのデータの読み取り。詳細については、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。

## TiDB Lightningはスキーマとテーブルの作成をスキップできますか？ {#could-tidb-lightning-skip-creating-schema-and-tables}

v5.1以降、 TiDB Lightningはダウンストリームのスキーマとテーブルを自動的に認識できます。 v5.1より前のTiDB Lightningを使用する場合は、 `tidb-lightning.toml`の`[mydumper]`セクションで`no-schema = true`を設定する必要があります。これにより、 TiDB Lightningは`CREATE TABLE`の呼び出しをスキップし、ターゲットデータベースからメタデータを直接フェッチします。テーブルが実際に欠落している場合、 TiDB Lightningはエラーで終了します。

## 厳密なSQLモードを無効にして、無効なデータをインポートできるようにすることはできますか？ {#can-the-strict-sql-mode-be-disabled-to-allow-importing-invalid-data}

はい。デフォルトでは、 TiDB Lightningで使用される[`sql_mode`](https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html)は`"STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"`であり、日付`1970-00-00`などの無効なデータを許可しません。モードは、 `tidb-lightning.toml`の`[tidb]`セクションの`sql-mode`設定を変更することで変更できます。

```toml
...
[tidb]
sql-mode = ""
...
```

## 1つの<code>tikv-importer</code> importerで複数の<code>tidb-lightning</code>インスタンスを処理できますか？ {#can-one-code-tikv-importer-code-serve-multiple-code-tidb-lightning-code-instances}

はい、すべての`tidb-lightning`つのインスタンスが異なるテーブルで動作する限り。

## <code>tikv-importer</code>プロセスを停止する方法は？ {#how-to-stop-the-code-tikv-importer-code-process}

`tikv-importer`のプロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動展開の場合： `tikv-importer`がフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tikv-importer`コマンドを使用してプロセスIDを取得してから、 `kill ${PID}`コマンドを使用してプロセスを終了します。

## <code>tidb-lightning</code>プロセスを停止する方法は？ {#how-to-stop-the-code-tidb-lightning-code-process}

`tidb-lightning`のプロセスを停止するには、展開方法に応じて対応する操作を選択できます。

-   手動展開の場合： `tidb-lightning`がフォアグラウンドで実行されている場合は、 <kbd>Ctrl</kbd> + <kbd>C</kbd>を押して終了します。それ以外の場合は、 `ps aux | grep tidb-lighting`コマンドを使用してプロセスIDを取得してから、 `kill -2 ${PID}`コマンドを使用してプロセスを終了します。

## バックグラウンドで実行しているときに<code>tidb-lightning</code>プロセスが突然終了するのはなぜですか？ {#why-the-code-tidb-lightning-code-process-suddenly-quits-while-running-in-background}

これは、 `tidb-lightning`を誤って開始したことが原因である可能性があります。これにより、システムはSIGHUP信号を送信して`tidb-lightning`プロセスを停止します。この状況では、 `tidb-lightning.log`は通常次のログを出力します。

```
[2018/08/10 07:29:08.310 +08:00] [INFO] [main.go:41] ["got signal to exit"] [signal=hangup]
```

コマンドラインで`nohup`を直接使用して`tidb-lightning`を開始することはお勧めしません。スクリプトを実行することで[`tidb-lightning`開始します](/tidb-lightning/deploy-tidb-lightning.md#step-3-start-tidb-lightning)できます。

さらに、 TiDB Lightningの最後のログにエラーが「コンテキストキャンセル」であることが示されている場合は、最初の「エラー」レベルのログを検索する必要があります。この「エラー」レベルのログの後には通常、「終了する信号を取得」が続きます。これは、 TiDB Lightningが割り込み信号を受信して終了したことを示します。

## TiDBクラスタが大量のCPUリソースを使用していて、 TiDB Lightningを使用した後、実行速度が非常に遅いのはなぜですか？ {#why-my-tidb-cluster-is-using-lots-of-cpu-resources-and-running-very-slowly-after-using-tidb-lightning}

`tidb-lightning`が異常終了した場合、クラスタは「インポート・モード」でスタックしている可能性があり、これは実動には適していません。現在のモードは、次のコマンドを使用して取得できます。

{{< copyable "" >}}

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

次のコマンドを使用して、クラスタを強制的に「通常モード」に戻すことができます。

{{< copyable "" >}}

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

## TiDB Lightningは1ギガビットネットワークカードで使用できますか？ {#can-tidb-lightning-be-used-with-1-gigabit-network-card}

TiDB Lightningツールセットは、10ギガビットネットワークカードで使用するのが最適です。 1ギガビットネットワークカードは、特に`tikv-importer`の*場合はお勧めしません*。

1ギガビットネットワークカードは、合計120 MB / sの帯域幅しか提供できません。これは、すべてのターゲットTiKVストア間で共有する必要があります。 TiDB Lightningは、1ギガビットネットワークのすべての帯域幅を簡単に飽和させ、PDに接続できなくなるため、クラスタを停止させる可能性があります。これを回避するには、*アップロード速度の制限*を[インポーターの構成](/tidb-lightning/tidb-lightning-configuration.md#tikv-importer)に設定します。

```toml
[import]
# Restricts the total upload speed to TiKV to 100 MB/s or less
upload-speed-limit = "100MB"
```

## TiDB LightningがターゲットTiKVクラスタに非常に多くの空き領域を必要とするのはなぜですか？ {#why-tidb-lightning-requires-so-much-free-space-in-the-target-tikv-cluster}

デフォルト設定の3レプリカでは、ターゲットTiKVクラスタのスペース要件はデータソースのサイズの6倍です。次の要因がデータソースに反映されていないため、「2」の余分な倍数は控えめな見積もりです。

-   インデックスが占めるスペース
-   RocksDBでのスペース増幅

## TiDB Lightningの実行中にTiKVImporterを再起動できますか？ {#can-tikv-importer-be-restarted-while-tidb-lightning-is-running}

いいえ。TiKVインポーターはエンジンの情報をメモリに保存します。 `tikv-importer`を再起動すると、接続が失われたため`tidb-lightning`が停止します。この時点で、これらのTiKVインポーター固有の情報が失われるため、 [失敗したチェックポイントを破棄する](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)にする必要があります。その後、 TiDB Lightningを再起動できます。

正しいシーケンスについては、 [TiDB Lightningを正しく再起動する方法は？](#how-to-properly-restart-tidb-lightning)も参照してください。

## TiDB Lightningに関連するすべての中間データを完全に破棄するにはどうすればよいですか？ {#how-to-completely-destroy-all-intermediate-data-associated-with-tidb-lightning}

1.  チェックポイントファイルを削除します。

    {{< copyable "" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-remove=all
    ```

    何らかの理由でこのコマンドを実行できない場合は、ファイル`/tmp/tidb_lightning_checkpoint.pb`を手動で削除してみてください。

2.  ローカルバックエンドを使用している場合は、構成内の`sorted-kv-dir`のディレクトリを削除します。 Importer-backendを使用している場合は、 `tikv-importer`をホストしているマシンの`import`のディレクトリ全体を削除します。

3.  必要に応じて、TiDBクラスタで作成されたすべてのテーブルとデータベースを削除します。

4.  残りのメタデータをクリーンアップします。次のいずれかの条件が存在する場合は、メタデータスキーマを手動でクリーンアップする必要があります。

    -   TiDB Lightning v5.1.xおよびv5.2.xバージョンの場合、 `tidb-lightning-ctl`コマンドはターゲットクラスタのメタデータスキーマをクリーンアップしません。手動でクリーンアップする必要があります。
    -   チェックポイントファイルを手動で削除した場合は、ダウンストリームメタデータスキーマを手動でクリーンアップする必要があります。そうしないと、後続のインポートの正確性が影響を受ける可能性があります。

    次のコマンドを使用して、メタデータをクリーンアップします。

    {{< copyable "" >}}

    ```sql
    DROP DATABASE IF EXISTS `lightning_metadata`;
    ```

## TiDB Lightning <code>could not find first pair, this shouldn&#39;t happen</code>か？ {#why-does-tidb-lightning-report-the-code-could-not-find-first-pair-this-shouldn-t-happen-code-error}

このエラーは、 TiDB Lightning TiDB Lightningがソートされたローカルファイルを読み取るときに、TiDBLightningによって開かれたファイルの数がシステム制限を超えたために発生する可能性があります。 Linuxシステムでは、 `ulimit -n`コマンドを使用して、このシステム制限の値が小さすぎるかどうかを確認できます。インポート中にこの値を`1000000` （ `ulimit -n 1000000` ）に調整することをお勧めします。

## インポート速度が遅すぎる {#import-speed-is-too-slow}

通常、256MBのデータファイルをインポートするのにTiDB Lightningはスレッドごとに2分かかります。速度がこれよりはるかに遅い場合は、エラーが発生します。各データファイルにかかった時間は、 `restore chunk … takes`に記載されているログから確認できます。これは、Grafanaのメトリックからも確認できます。

TiDB Lightningが遅くなる理由はいくつかあります。

**原因1** ： `region-concurrency`の設定が高すぎるため、スレッドの競合が発生し、パフォーマンスが低下します。

1.  設定は、ログの先頭から`region-concurrency`を検索して見つけることができます。
2.  TiDB Lightningが他のサービス（TiKV Importerなど）と同じマシンを共有している場合、 `region-concurrency`をCPUコアの総数の75％に**手動で**設定する必要があります。
3.  CPUにクォータがある場合（たとえば、Kubernetes設定によって制限されている場合）、 TiDB Lightningはこれを読み取れない可能性があります。この場合、 `region-concurrency`も**手動で**減らす必要があります。

**原因2** ：テーブルスキーマが複雑すぎます。

インデックスを追加するたびに、行ごとに新しいKVペアが導入されます。 N個のインデックスがある場合、インポートされる実際のサイズは、 Dumpling出力のサイズの約（N + 1）倍になります。インデックスが無視できる場合は、最初にスキーマからインデックスを削除し、インポートの完了後に`CREATE INDEX`を使用してインデックスを追加し直すことができます。

**原因3** ：各ファイルが大きすぎます。

TiDB Lightningは、データソースを約256 MBのサイズの複数のファイルに分割して、データを並列処理できる場合に最適に機能します。各ファイルが大きすぎると、 TiDB Lightningが応答しない場合があります。

データソースがCSVであり、すべてのCSVファイルに改行制御文字（U+000AおよびU+000D）を含むフィールドがない場合は、「厳密な形式」をオンにして、 TiDB Lightningが大きなファイルを自動的に分割できるようにすることができます。

```toml
[mydumper]
strict-format = true
```

**原因4** ： TiDB Lightningが古すぎます。

最新バージョンをお試しください！たぶん、新しい速度の改善があります。

## <code>checksum failed: checksum mismatched remote vs local</code> {#code-checksum-failed-checksum-mismatched-remote-vs-local-code}

**原因**：ローカル・データ・ソースとリモートでインポートされたデータベースの表のチェックサムが異なります。このエラーには、いくつかのより深い理由があります。 `checksum mismatched`を含むログを確認することで、理由をさらに特定できます。

`checksum mismatched`を含む行は、情報`total_kvs: x vs y`を提供します。ここで、 `x`は、インポートの完了後にターゲットクラスタによって計算されたキーと値のペア（KVペア）の数を示し、 `y`は、ローカルデータによって生成されたキーと値のペアの数を示します。ソース。

-   `x`が大きい場合は、ターゲットクラスタにKVペアが多いことを意味します。
    -   インポート前にこのテーブルが空ではないため、データチェックサムに影響を与える可能性があります。 TiDB Lightningが以前に失敗してシャットダウンしたが、正しく再起動しなかった可能性もあります。
-   `y`が大きい場合は、ローカルデータソースにKVペアが多いことを意味します。
    -   ターゲットデータベースのチェックサムがすべて0の場合、インポートが発生していないことを意味します。クラスタがビジー状態でデータを受信できない可能性があります。
    -   エクスポートされたデータに、値が重複するUNIQUEキーやPRIMARY KEYなどの重複データが含まれている可能性があります。または、データが大文字と小文字を区別する一方で、ダウンストリームテーブル構造は大文字と小文字を区別しない可能性があります。
-   その他の考えられる理由
    -   データソースがマシンで生成され、 Dumplingによってバックアップされていない場合は、データがテーブルの制限に準拠していることを確認してください。たとえば、AUTO_INCREMENT列は、0ではなく正である必要があります。

**ソリューション**：

1.  `tidb-lightning-ctl`を使用して破損したデータを削除し、テーブル構造とデータを確認してから、 TiDB Lightningを再起動して、影響を受けるテーブルを再度インポートします。

    {{< copyable "" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

2.  ターゲットデータベースの負荷を軽減するために、外部データベースを使用してチェックポイントを格納することを検討してください（変更`[checkpoint] dsn` ）。

3.  TiDB Lightningが不適切に再起動された場合は、 FAQの「 [TiDB Lightningを正しく再起動する方法](#how-to-properly-restart-tidb-lightning) 」セクションも参照してください。

## <code>Checkpoint for … has invalid status:</code>エラーコード） {#code-checkpoint-for-has-invalid-status-code-error-code}

**原因**： [チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)が有効であり、 TiDB LightningまたはTiKVImporterが以前に異常終了しました。偶発的なデータ破損を防ぐために、エラーが解決されるまでTiDB Lightningは起動しません。

エラーコードは25より小さい整数であり、可能な値は0、3、6、9、12、14、15、17、18、20、および21です。整数は、インポートで予期しない終了が発生するステップを示します。処理する。整数が大きいほど、出口が発生する後のステップです。

**ソリューション**：

無効なデータソースが原因でエラーが発生した場合は、 `tidb-lightning-ctl`を使用してインポートしたデータを削除し、Lightningを再起動してください。

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

他のオプションについては、 [チェックポイント管理](/tidb-lightning/tidb-lightning-checkpoints.md#checkpoints-control)セクションを参照してください。

## <code>ResourceTemporarilyUnavailable("Too many open engines …: …")</code> {#code-resourcetemporarilyunavailable-too-many-open-engines-code}

**原因**：同時エンジンファイルの数が`tikv-importer`で指定された制限を超えています。これは、設定の誤りが原因である可能性があります。さらに、 `tidb-lightning`が異常終了した場合、エンジンファイルがぶら下がっているオープン状態のままになる可能性があり、これもこのエラーの原因となる可能性があります。

**ソリューション**：

1.  `tikv-importer.toml`の`max-open-engines`設定の値を増やします。この値は通常、使用可能なメモリによって決まります。これは、次を使用して計算できます。

    最大メモリ使用量`max-open-engines` × `write-buffer-size` × `max-write-buffer-number`

2.  `table-concurrency` + `index-concurrency`の値を減らして、 `max-open-engines`未満にします。

3.  `tikv-importer`を再起動して、すべてのエンジンファイルを強制的に削除します（デフォルトは`./data.import/` ）。これにより、部分的にインポートされたすべてのテーブルも削除されます。これには、 TiDB Lightningが古いチェックポイントをクリアする必要があります。

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

## <code>cannot guess encoding for input file, please convert to UTF-8 manually</code> {#code-cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually-code}

**原因**： TiDB Lightningは、テーブルスキーマのUTF-8およびGB-18030エンコーディングのみを認識します。このエラーは、ファイルがこれらのエンコーディングのいずれにも含まれていない場合に発生します。過去`ALTER TABLE`の実行により、ファイルにUTF-8の文字列とGB-18030の別の文字列が含まれるなど、エンコードが混在している可能性もあります。

**ソリューション**：

1.  ファイルが完全にUTF-8またはGB-18030になるようにスキーマを修正します。

2.  ターゲットデータベース内の影響を受けるテーブルを手動で`CREATE` 。

3.  チェックをスキップするには、 `[mydumper] character-set = "binary"`を設定します。これにより、ターゲットデータベースに文字化けが導入される可能性があることに注意してください。

## <code>[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 …}'</code> {#code-sql2kv-sql-encode-error-types-1292-invalid-time-format-1970-1-1-code}

**原因**：表に`timestamp`タイプの列が含まれていますが、時間値自体が存在しません。これは、DSTが変更されたか、時間値がサポートされている範囲（1970年1月1日から2038年1月19日）を超えたことが原因です。

**ソリューション**：

1.  TiDB Lightningとソースデータベースが同じタイムゾーンを使用していることを確認します。

    TiDB Lightningを直接実行する場合、 `$TZ`の環境変数を使用してタイムゾーンを強制できます。

    ```sh
    # Manual deployment, and force Asia/Shanghai.
    TZ='Asia/Shanghai' bin/tidb-lightning -config tidb-lightning.toml
    ```

2.  Mydumperを使用してデータをエクスポートする場合は、必ず`--skip-tz-utc`フラグを含めてください。

3.  クラスタ全体が同じ最新バージョンの`tzdata` （バージョン2018i以降）を使用していることを確認します。

    CentOSで、 `yum info tzdata`を実行して、インストールされているバージョンと更新があるかどうかを確認します。 `yum upgrade tzdata`を実行して、パッケージをアップグレードします。

## <code>[Error 8025: entry too large, the max entry size is 6291456]</code> {#code-error-8025-entry-too-large-the-max-entry-size-is-6291456-code}

**原因**： TiDB Lightningによって生成されたキーと値のペアの単一行が、TiDBによって設定された制限を超えています。

**解決策**：

現在、TiDBの制限を回避することはできません。このテーブルを無視して、他のテーブルを正常にインポートできるようにすることしかできません。

## Encounter <code>rpc error: code = Unimplemented ...</code> TiDB Lightningがモードを切り替えたとき {#encounter-code-rpc-error-code-unimplemented-code-when-tidb-lightning-switches-the-mode}

**原因**：クラスタの一部のノードが`switch-mode`をサポートしていません。たとえば、 [`switch-mode`はサポートされていません](https://github.com/pingcap/tidb-lightning/issues/273)のバージョンが`v4.0.0-rc.2`より前の場合。

**ソリューション**：

-   クラスタにTiFlashノードがある場合は、クラスタを`v4.0.0-rc.2`つ以上のバージョンに更新できます。
-   クラスタをアップグレードしない場合は、TiFlashを一時的に無効にします。

## <code>tidb lightning encountered error: TiDB version too old, expected '>=4.0.0', found '3.0.18'</code> {#code-tidb-lightning-encountered-error-tidb-version-too-old-expected-4-0-0-found-3-0-18-code}

TiDB Lightningバックエンドは、v4.0.0以降のバージョンのTiDBクラスターへのデータのインポートのみをサポートします。ローカルバックエンドを使用してデータをv2.xまたはv3.xクラスタにインポートしようとすると、上記のエラーが報告されます。このとき、データのインポートにImporter-backendまたはTiDB-backendを使用するように構成を変更できます。

一部の`nightly`バージョンは、v4.0.0-beta.2に類似している可能性があります。これらの`nightly`のバージョンのTiDB Lightningは、実際にはローカルバックエンドをサポートしています。 `nightly`バージョンを使用しているときにこのエラーが発生した場合は、構成`check-requirements = false`を設定することにより、バージョンチェックをスキップできます。このパラメータを設定する前に、 TiDB Lightningの設定が対応するバージョンをサポートしていることを確認してください。そうしないと、インポートが失敗する可能性があります。

## <code>restore table test.district failed: unknown columns in header [...]</code> {#code-restore-table-test-district-failed-unknown-columns-in-header-code}

このエラーは通常、CSVデータファイルにヘッダーが含まれていないために発生します（最初の行は列名ではなくデータです）。したがって、 TiDB Lightning構成ファイルに次の構成を追加する必要があります。

```
[mydumper.csv]
header = false
```

## TiDB Lightningのランタイムゴルーチン情報を取得する方法 {#how-to-get-the-runtime-goroutine-information-of-tidb-lightning}

1.  TiDB Lightningの設定ファイルで[`status-port`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-configuration)が指定されている場合は、この手順をスキップしてください。それ以外の場合は、USR1信号をTiDB Lightningに送信して`status-port`を有効にする必要があります。

    `ps`などのコマンドを使用してTiDB LightningのプロセスID（PID）を取得し、次のコマンドを実行します。

    {{< copyable "" >}}

    ```sh
    kill -USR1 <lightning-pid>
    ```

    TiDB Lightningのログを確認してください。 `starting HTTP server`のログには、新しく有効になった`started HTTP server`が`status-port`され`start HTTP server` 。

2.  `http://<lightning-ip>:<status-port>/debug/pprof/goroutine?debug=2`にアクセスして、ゴルーチン情報を取得します。
