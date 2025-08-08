---
title: Troubleshoot TiDB Lightning
summary: TiDB Lightning の使用時に発生する可能性のある一般的な問題とその解決策について説明します。
---

# TiDB Lightning のトラブルシューティング {#troubleshoot-tidb-lightning}

このドキュメントでは、 TiDB Lightningの使用時に発生する可能性のある一般的な問題とその解決策をまとめています。

## インポート速度が遅すぎる {#import-speed-is-too-slow}

通常、 TiDB Lightningは256MBのデータファイルをインポートするのに、スレッドごとに2分かかります。これよりも大幅に遅い場合は、エラーが発生しています。各データファイルの所要時間は、 `restore chunk … takes`言及されているログから確認できます。これはGrafanaのメトリクスからも確認できます。

TiDB Lightning が遅くなる理由はいくつかあります。

**原因 1** : `region-concurrency`設定が高すぎるため、スレッドの競合が発生し、パフォーマンスが低下します。

1.  設定は、ログの先頭から`region-concurrency`検索すると見つかります。
2.  TiDB Lightning が他のサービス (TiKV Importer など) と同じマシンを共有する場合、 `region-concurrency` CPU コアの合計数の 75% に**手動で**設定する必要があります。
3.  CPUクォータ（例えばKubernetesの設定による制限）がある場合、 TiDB Lightningはそれを読み取れない可能性があります。この場合も、 `region-concurrency`**手動で**減らす必要があります。

**原因 2** : テーブル スキーマが複雑すぎます。

インデックスを追加するたびに、各行に新しいKVペアが作成されます。インデックスがN個ある場合、実際にインポートされるサイズはDumpling出力のサイズの約(N+1)倍になります。インデックスが無視できるほど小さい場合は、まずスキーマからインデックスを削除し、インポート完了後に`CREATE INDEX`使用して再度追加することができます。

**原因 3** : 各ファイルが大きすぎます。

TiDB Lightningは、データソースを256MB程度の複数のファイルに分割し、並列処理することで最適に動作します。各ファイルのサイズが大きすぎると、 TiDB Lightningが応答しない場合があります。

データ ソースが CSV であり、すべての CSV ファイルに改行制御文字 (U+000A および U+000D) を含むフィールドがない場合は、「厳密な形式」をオンにして、 TiDB Lightning が大きなファイルを自動的に分割するようにすることができます。

```toml
[mydumper]
strict-format = true
```

**原因 4** : TiDB Lightning が古すぎます。

最新バージョンをお試しください。速度が改善されているかもしれません。

## <code>tidb-lightning</code>プロセスがバックグラウンドで実行中に突然終了する {#the-code-tidb-lightning-code-process-suddenly-quits-while-running-in-background}

これは、 `tidb-lightning`正しく起動されていないためにシステムが SIGHUP シグナルを送信し、 `tidb-lightning`プロセスを停止したことが原因である可能性があります。この場合、 `tidb-lightning.log`通常、次のログを出力します。

    [2018/08/10 07:29:08.310 +08:00] [INFO] [main.go:41] ["got signal to exit"] [signal=hangup]

コマンドラインで直接`nohup`使用して`tidb-lightning`起動することは推奨されません。スクリプトを実行することで[`tidb-lightning`を起動する](/get-started-with-tidb-lightning.md#step-4-start-tidb-lightning)起動できます。

また、 TiDB Lightningの最後のログに「Context cancellation」というエラーが表示されている場合は、最初の「ERROR」レベルのログを探す必要があります。この「ERROR」レベルのログには通常、「got signal to exit」が続きます。これは、 TiDB Lightningが割り込み信号を受信して終了したことを示しています。

## TiDB クラスターは多くの CPU リソースを消費し、 TiDB Lightningを使用すると非常に遅くなります。 {#the-tidb-cluster-uses-lots-of-cpu-resources-and-runs-very-slowly-after-using-tidb-lightning}

`tidb-lightning`異常終了した場合、クラスターは本番には適さない「インポートモード」で停止している可能性があります。現在のモードは次のコマンドで取得できます。

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

次のコマンドを使用して、クラスターを強制的に「通常モード」に戻すことができます。

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

## TiDB Lightningがエラーを報告 {#tidb-lightning-reports-an-error}

### <code>could not find first pair, this shouldn't happen</code> {#code-could-not-find-first-pair-this-shouldn-t-happen-code}

このエラーは、 TiDB Lightningがソート済みのローカルファイルを読み取る際に、開いているファイル数がシステム制限を超えたために発生する可能性があります。Linuxシステムでは、 `ulimit -n`コマンドを使用して、このシステム制限の値が小さすぎないかどうかを確認できます。インポート中にこの値を`1000000` （ `ulimit -n 1000000` ）に調整することをお勧めします。

### <code>checksum failed: checksum mismatched remote vs local</code> {#code-checksum-failed-checksum-mismatched-remote-vs-local-code}

**原因**: ローカルデータソースとリモートインポートデータベースのテーブルのチェックサムが異なります。このエラーには、より深刻な理由がいくつか考えられます。2 `checksum mismatched`含むログを確認することで、原因をさらに特定できます。

`checksum mismatched`を含む行は情報`total_kvs: x vs y`提供します。ここで、 `x`インポートの完了後にターゲット クラスターによって計算されたキーと値のペア (KV ペア) の数を示し、 `y`ローカル データ ソースによって生成されたキーと値のペアの数を示します。

-   `x`が大きい場合は、ターゲット クラスター内にさらに多くの KV ペアが存在することを意味します。
    -   インポート前にこのテーブルが空でなかったために、データのチェックサムに影響が出ている可能性があります。また、 TiDB Lightning が以前に障害を起こしてシャットダウンしたものの、正常に再起動しなかった可能性もあります。
-   `y`が大きい場合は、ローカル データ ソースにさらに多くの KV ペアが存在することを意味します。
    -   ターゲットデータベースのチェックサムがすべて0の場合、インポートが実行されていないことを意味します。クラスターがビジー状態のため、データを受信できない可能性があります。
    -   エクスポートされたデータに、重複した値を持つ UNIQUE KEY や PRIMARY KEY などの重複データが含まれている可能性があります。また、下流のテーブル構造では大文字と小文字が区別されないのに対し、データは大文字と小文字が区別される可能性があります。
-   その他の考えられる理由
    -   データソースが機械生成で、 Dumplingによってバックアップされていない場合は、データがテーブルの制限に準拠していることを確認してください。例えば、AUTO_INCREMENT 列は 0 ではなく正の値である必要があります。

**ソリューション**：

1.  `tidb-lightning-ctl`使用して破損したデータを削除し、テーブル構造とデータを確認して、 TiDB Lightningを再起動して、影響を受けるテーブルを再度インポートします。

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

2.  ターゲット データベースの負荷を軽減するために、チェックポイント (変更`[checkpoint] dsn` ) を保存するために外部データベースの使用を検討してください。

3.  TiDB Lightningが不適切に再起動された場合は、 FAQの「 [TiDB Lightningを適切に再起動する方法](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning) 」セクションも参照してください。

### <code>Checkpoint for … has invalid status:</code> (エラー コード) {#code-checkpoint-for-has-invalid-status-code-error-code}

**原因**: [チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)が有効になっており、 TiDB Lightningまたは TiKV Importer が以前に異常終了しています。偶発的なデータ破損を防ぐため、エラーが解決されるまでTiDB Lightning は起動しません。

エラーコードは25未満の整数で、0、3、6、9、12、14、15、17、18、20、21のいずれかの値を取ります。この整数は、インポートプロセスにおいて予期せぬ終了が発生したステップを示します。整数が大きいほど、終了が発生したステップが遅くなります。

**ソリューション**：

無効なデータ ソースによってエラーが発生した場合は、 `tidb-lightning-ctl`を使用してインポートされたデータを削除し、Lightning を再起動します。

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

その他のオプションについては、セクション[チェックポイント制御](/tidb-lightning/tidb-lightning-checkpoints.md#checkpoints-control)参照してください。

### <code>cannot guess encoding for input file, please convert to UTF-8 manually</code> {#code-cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually-code}

**原因**: TiDB Lightning は、テーブルスキーマのエンコーディングとして UTF-8 と GB-18030 のみを認識します。ファイルがこれらのいずれのエンコーディングでもない場合、このエラーが発生します。また、過去の`ALTER TABLE`の実行により、ファイルに UTF-8 の文字列と GB-18030 の文字列が混在しているなど、エンコーディングが混在している可能性もあります。

**ソリューション**：

1.  ファイル全体が UTF-8 または GB-18030 になるようにスキーマを修正します。

2.  ターゲット データベース内の影響を受けるテーブルを手動で`CREATE` 。

3.  `[mydumper] character-set = "binary"`設定するとチェックをスキップします。ただし、これにより対象データベースに文字化けが発生する可能性があります。

### <code>[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 …}'</code> {#code-sql2kv-sql-encode-error-types-1292-invalid-time-format-1970-1-1-code}

**原因**: テーブルに`timestamp`型の列が含まれていますが、時刻値自体が存在しません。これは、夏時間の変更、または時刻値がサポート範囲（1970年1月1日から2038年1月19日）を超えていることが原因です。

**ソリューション**：

1.  TiDB Lightningとソース データベースが同じタイム ゾーンを使用していることを確認します。

    TiDB Lightning を直接実行する場合、 `$TZ`環境変数を使用してタイムゾーンを強制できます。

    ```sh
    # Manual deployment, and force Asia/Shanghai.
    TZ='Asia/Shanghai' bin/tidb-lightning -config tidb-lightning.toml
    ```

2.  クラスター全体で同じ最新バージョン`tzdata` (バージョン 2018i 以上) が使用されていることを確認します。

    CentOS では、 `yum info tzdata`実行してインストールされているバージョンとアップデートの有無を確認します。3 `yum upgrade tzdata`実行してパッケージをアップグレードします。

### <code>[Error 8025: entry too large, the max entry size is 6291456]</code> {#code-error-8025-entry-too-large-the-max-entry-size-is-6291456-code}

**原因**: TiDB Lightningによって生成されたキーと値のペアの 1 行が、TiDB によって設定された制限を超えています。

**解決**：

-   制限を動的に増やすには、 [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)システム変数を使用します。
-   TiKVにも同様の制限があることに注意してください。1回の書き込みリクエストのデータサイズが[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size) （デフォルトでは`8MiB` ）を超えると、TiKVはこのリクエストの処理を拒否します。テーブルに大きなサイズの行がある場合は、両方の設定を変更する必要があります。

### TiDB Lightningがモードを切り替えるときに、 <code>rpc error: code = Unimplemented ...</code> {#encounter-code-rpc-error-code-unimplemented-code-when-tidb-lightning-switches-the-mode}

**原因**: クラスタ内の一部のノードが`switch-mode`サポートしていません。例えば、 TiFlash のバージョンが`v4.0.0-rc.2` 、 [`switch-mode`はサポートされていません](https://github.com/pingcap/tidb-lightning/issues/273)より前の場合などです。

**ソリューション**：

-   クラスター内にTiFlashノードがある場合は、クラスターを`v4.0.0-rc.2`以上のバージョンに更新できます。
-   クラスターをアップグレードしない場合は、 TiFlash を一時的に無効にします。

### <code>tidb lightning encountered error: TiDB version too old, expected '>=4.0.0', found '3.0.18'</code> {#code-tidb-lightning-encountered-error-tidb-version-too-old-expected-4-0-0-found-3-0-18-code}

TiDB Lightning Local-backend は、v4.0.0 以降のバージョンの TiDB クラスターへのデータインポートのみをサポートしています。Local-backend を使用して v2.x または v3.x クラスターにデータをインポートしようとすると、上記のエラーが報告されます。その場合は、設定を変更して、データのインポートに Importer-backend または TiDB-backend を使用するように設定できます。

`nightly`バージョンの中には、v4.0.0-beta.2 に類似しているものもあります。これらの`nightly`バージョンのTiDB Lightning は、実際にはローカルバックエンドをサポートしています。5 バージョン`nightly`使用時にこのエラーが発生した場合は、設定`check-requirements = false`設定することでバージョンチェックを省略できます。このパラメータを設定する前に、 TiDB Lightningの設定が対応するバージョンをサポートしていることを確認してください。そうでない場合、インポートが失敗する可能性があります。

### <code>restore table test.district failed: unknown columns in header [...]</code> {#code-restore-table-test-district-failed-unknown-columns-in-header-code}

このエラーは通常、CSVデータファイルにヘッダーが含まれていないこと（最初の行が列名ではなくデータである）が原因で発生します。そのため、 TiDB Lightning設定ファイルに以下の設定を追加する必要があります。

    [mydumper.csv]
    header = false

### <code>Unknown character set</code> {#code-unknown-character-set-code}

TiDBはMySQLのすべての文字セットをサポートしていません。そのため、インポート中にテーブルスキーマを作成する際にサポートされていない文字セットが使用されると、 TiDB Lightningはこのエラーを報告します。このエラーを回避するには、特定のデータに応じて、 [TiDBでサポートされている文字セット](/character-set-and-collation.md)使用して下流で事前にテーブルスキーマを作成してください。

### <code>invalid compression type ...</code> {#code-invalid-compression-type-code}

-   TiDB Lightning v6.4.0以降のバージョンでは、 `gzip` `snappy`圧縮データファイルのみがサポートされています。その他の種類の圧縮ファイルを使用するとエラーが発生します。ソースデータファイルが保存されているディレクトリにサポートされていない圧縮ファイルが存在する場合、タスク`zstd`エラーを報告します。このようなエラーを回避するには、サポートされていないファイルをインポートデータディレクトリから移動してください。詳細については、 [圧縮ファイル](/tidb-lightning/tidb-lightning-data-source.md#compressed-files)参照してください。

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。
