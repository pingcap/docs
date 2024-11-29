---
title: Troubleshoot TiDB Lightning
summary: TiDB Lightning を使用する際に発生する可能性のある一般的な問題とその解決策について説明します。
---

# TiDB Lightning のトラブルシューティング {#troubleshoot-tidb-lightning}

このドキュメントでは、 TiDB Lightning の使用時に発生する可能性のある一般的な問題とその解決策をまとめています。

## インポート速度が遅すぎる {#import-speed-is-too-slow}

通常、 TiDB Lightning が256 MB のデータ ファイルをインポートするには、スレッドごとに 2 分かかります。速度がこれより大幅に遅い場合は、エラーがあります`restore chunk … takes`に記載されているログから、各データ ファイルにかかった時間を確認できます。これは、Grafana のメトリックからも確認できます。

TiDB Lightning が遅くなる理由はいくつかあります。

**原因 1** : `region-concurrency`の設定が高すぎるため、スレッドの競合が発生し、パフォーマンスが低下します。

1.  設定は、ログの先頭から`region-concurrency`検索すると見つかります。
2.  TiDB Lightning が他のサービス (TiKV Importer など) と同じマシンを共有する場合は、 `region-concurrency` CPU コアの合計数の 75% に**手動で**設定する必要があります。
3.  CPU にクォータがある場合 (Kubernetes 設定による制限など)、 TiDB Lightning はこれを読み取れない可能性があります。この場合も`region-concurrency`**手動で**減らす必要があります。

**原因 2** : テーブル スキーマが複雑すぎます。

インデックスを追加するたびに、各行に新しい KV ペアが導入されます。インデックスが N 個ある場合、インポートされる実際のサイズは、 Dumpling出力のサイズの約 (N+1) 倍になります。インデックスが無視できるほど小さい場合は、最初にスキーマからインデックスを削除し、インポートが完了した後に`CREATE INDEX`使用して再度追加することができます。

**原因 3** : 各ファイルが大きすぎます。

TiDB Lightning は、データ ソースが 256 MB 程度のサイズの複数のファイルに分割され、データを並列処理できる場合に最適に機能します。各ファイルが大きすぎると、 TiDB Lightning が応答しない可能性があります。

データ ソースが CSV であり、すべての CSV ファイルに改行制御文字 (U+000A および U+000D) を含むフィールドがない場合は、「厳密な形式」をオンにして、 TiDB Lightning で大きなファイルを自動的に分割することができます。

```toml
[mydumper]
strict-format = true
```

**原因 4** : TiDB Lightningが古すぎます。

最新バージョンをお試しください。速度がさらに向上するかもしれません。

## <code>tidb-lightning</code>プロセスがバックグラウンドで実行中に突然終了する {#the-code-tidb-lightning-code-process-suddenly-quits-while-running-in-background}

これは、 `tidb-lightning`誤って起動し、システムが SIGHUP 信号を送信して`tidb-lightning`プロセスを停止することによって発生する可能性があります。この状況では、通常、 `tidb-lightning.log`次のログを出力します。

    [2018/08/10 07:29:08.310 +08:00] [INFO] [main.go:41] ["got signal to exit"] [signal=hangup]

`tidb-lightning`起動するためにコマンドラインで`nohup`直接使用することは推奨されません。 [`tidb-lightning`起動する](/get-started-with-tidb-lightning.md#step-4-start-tidb-lightning)スクリプトを実行することで起動できます。

また、 TiDB Lightningの最後のログに「コンテキストがキャンセルされました」というエラーが表示されている場合は、最初の「ERROR」レベルのログを検索する必要があります。この「ERROR」レベルのログの後には通常、「終了するための信号を受け取りました」が続きます。これは、 TiDB Lightning が割り込み信号を受信して​​終了したことを示しています。

## TiDBクラスターはCPUリソースを大量に消費し、 TiDB Lightningの使用後は非常に遅くなります。 {#the-tidb-cluster-uses-lots-of-cpu-resources-and-runs-very-slowly-after-using-tidb-lightning}

`tidb-lightning`異常終了した場合、クラスターは「インポート モード」のままになっている可能性がありますが、これは本番に適していません。現在のモードは、次のコマンドを使用して取得できます。

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

次のコマンドを使用して、クラスターを強制的に「通常モード」に戻すことができます。

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

## TiDB Lightningがエラーを報告 {#tidb-lightning-reports-an-error}

### <code>could not find first pair, this shouldn't happen</code> {#code-could-not-find-first-pair-this-shouldn-t-happen-code}

このエラーは、 TiDB Lightning がソートされたローカル ファイルを読み取るときに、 TiDB Lightningによって開かれるファイル数がシステム制限を超えたために発生する可能性があります。Linux システムでは、 `ulimit -n`コマンドを使用して、このシステム制限の値が小さすぎるかどうかを確認できます。インポート中にこの値を`1000000` ( `ulimit -n 1000000` ) に調整することをお勧めします。

### <code>checksum failed: checksum mismatched remote vs local</code> {#code-checksum-failed-checksum-mismatched-remote-vs-local-code}

**原因**: ローカル データ ソースとリモート インポート データベースのテーブルのチェックサムが異なります。このエラーには、いくつかのより深い理由があります`checksum mismatched`を含むログを確認することで、さらに理由を突き止めることができます。

`checksum mismatched`含む行は情報`total_kvs: x vs y`を提供します。ここで、 `x`インポートの完了後にターゲット クラスターによって計算されたキーと値のペア (KV ペア) の数を示し、 `y`ローカル データ ソースによって生成されたキーと値のペアの数を示します。

-   `x`が大きい場合は、ターゲット クラスター内に KV ペアがさらに存在することを意味します。
    -   このテーブルはインポート前に空でなかった可能性があり、そのためデータ チェックサムに影響します。また、 TiDB Lightning が以前に失敗してシャットダウンしたが、正しく再起動されなかった可能性もあります。
-   `y`が大きい場合は、ローカル データ ソースに KV ペアがさらに存在することを意味します。
    -   ターゲット データベースのチェックサムがすべて 0 の場合、インポートは行われていないことを意味します。クラスターがビジー状態のため、データを受信できない可能性があります。
    -   エクスポートされたデータに、重複した値を持つ UNIQUE KEY や PRIMARY KEY などの重複データが含まれている可能性があります。また、下流のテーブル構造では大文字と小文字が区別されるのに、データでは大文字と小文字が区別されない可能性もあります。
-   その他の考えられる理由
    -   データ ソースがマシンによって生成され、 Dumplingによってバックアップされていない場合は、データがテーブル制限に準拠していることを確認してください。たとえば、AUTO_INCREMENT 列は 0 ではなく正の値である必要があります。

**ソリューション**:

1.  `tidb-lightning-ctl`使用して破損したデータを削除し、テーブル構造とデータを確認して、 TiDB Lightning を再起動し、影響を受けるテーブルを再度インポートします。

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

2.  ターゲット データベースの負荷を軽減するために、チェックポイント (変更`[checkpoint] dsn` ) を保存するために外部データベースを使用することを検討してください。

3.  TiDB Lightningが不適切に再起動された場合は、 FAQの「 [TiDB Lightningを適切に再起動する方法](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning) 」セクションも参照してください。

### <code>Checkpoint for … has invalid status:</code> (エラー コード) {#code-checkpoint-for-has-invalid-status-code-error-code}

**原因**: [チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)が有効になっており、 TiDB Lightningまたは TiKV Importer が以前に異常終了しました。偶発的なデータ破損を防ぐため、エラーが解決されるまでTiDB Lightning は起動しません。

エラー コードは 25 未満の整数で、0、3、6、9、12、14、15、17、18、20、21 の値を取ります。整数は、インポート プロセスで予期しない終了が発生したステップを示します。整数が大きいほど、終了が発生するステップが遅くなります。

**ソリューション**:

無効なデータ ソースによってエラーが発生した場合は、 `tidb-lightning-ctl`使用してインポートされたデータを削除し、Lightning を再起動します。

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

その他のオプションについては、セクション[チェックポイント制御](/tidb-lightning/tidb-lightning-checkpoints.md#checkpoints-control)を参照してください。

### <code>cannot guess encoding for input file, please convert to UTF-8 manually</code> {#code-cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually-code}

**原因**: TiDB Lightning は、テーブル スキーマの UTF-8 および GB-18030 エンコーディングのみを認識します。ファイルがこれらのいずれのエンコーディングでもない場合、このエラーが発生します。また、過去の`ALTER TABLE`の実行により、UTF-8 の文字列と GB-18030 の別の文字列を含むなど、ファイルにエンコーディングが混在している可能性もあります。

**ソリューション**:

1.  ファイル全体が UTF-8 または GB-18030 になるようにスキーマを修正します。

2.  ターゲット データベース内の影響を受けるテーブルを手動で`CREATE` 。

3.  チェックをスキップするには`[mydumper] character-set = "binary"`設定します。これにより、ターゲット データベースに mojibake が導入される可能性があることに注意してください。

### <code>[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 …}'</code> {#code-sql2kv-sql-encode-error-types-1292-invalid-time-format-1970-1-1-code}

**原因**: テーブルに`timestamp`型の列が含まれていますが、時間値自体が存在しません。これは、DST の変更によるか、時間値がサポートされている範囲 (1970 年 1 月 1 日から 2038 年 1 月 19 日) を超えたことが原因です。

**ソリューション**:

1.  TiDB Lightningとソース データベースが同じタイム ゾーンを使用していることを確認します。

    TiDB Lightning を直接実行する場合、 `$TZ`環境変数を使用してタイムゾーンを強制することができます。

    ```sh
    # Manual deployment, and force Asia/Shanghai.
    TZ='Asia/Shanghai' bin/tidb-lightning -config tidb-lightning.toml
    ```

2.  クラスター全体で同じ最新バージョン`tzdata` (バージョン 2018i 以上) が使用されていることを確認します。

    CentOS では、 `yum info tzdata`実行してインストールされているバージョンと更新があるかどうかを確認します`yum upgrade tzdata`実行してパッケージをアップグレードします。

### <code>[Error 8025: entry too large, the max entry size is 6291456]</code> {#code-error-8025-entry-too-large-the-max-entry-size-is-6291456-code}

**原因**: TiDB Lightningによって生成されたキーと値のペアの 1 行が、TiDB によって設定された制限を超えています。

**解決**：

-   制限を動的に増やすには、 [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760)システム変数を使用します。
-   TiKV にも同様の制限があることに注意してください。単一の書き込み要求のデータ サイズが[`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size) (デフォルトでは`8MiB` ) を超えると、TiKV はこの要求の処理を拒否します。テーブルに大きなサイズの行がある場合は、両方の設定を変更する必要があります。

### TiDB Lightningがモードを切り替えると、 <code>rpc error: code = Unimplemented ...</code> {#encounter-code-rpc-error-code-unimplemented-code-when-tidb-lightning-switches-the-mode}

**原因**: クラスター内の一部のノードは`switch-mode`サポートしていません。たとえば、 TiFlash のバージョンが`v4.0.0-rc.2` 、 [`switch-mode`サポートされていません](https://github.com/pingcap/tidb-lightning/issues/273)より前の場合などです。

**ソリューション**:

-   クラスター内にTiFlashノードがある場合は、クラスターを`v4.0.0-rc.2`以上のバージョンに更新できます。
-   クラスターをアップグレードしない場合は、 TiFlash を一時的に無効にします。

### <code>tidb lightning encountered error: TiDB version too old, expected '>=4.0.0', found '3.0.18'</code> {#code-tidb-lightning-encountered-error-tidb-version-too-old-expected-4-0-0-found-3-0-18-code}

TiDB Lightningローカル バックエンドは、v4.0.0 以降のバージョンの TiDB クラスターへのデータのインポートのみをサポートします。ローカル バックエンドを使用して v2.x または v3.x クラスターにデータをインポートしようとすると、上記のエラーが報告されます。この時点で、データのインポートに Importer バックエンドまたは TiDB バックエンドを使用するように設定を変更できます。

いくつかの`nightly`バージョンは、v4.0.0-beta.2 に似ている可能性があります。これらの`nightly`バージョンのTiDB Lightning は、実際には Local-backend をサポートしています`nightly`バージョンの使用時にこのエラーが発生した場合は、構成`check-requirements = false`を設定することでバージョン チェックをスキップできます。このパラメータを設定する前に、 TiDB Lightningの構成が対応するバージョンをサポートしていることを確認してください。そうでない場合、インポートが失敗する可能性があります。

### <code>restore table test.district failed: unknown columns in header [...]</code> {#code-restore-table-test-district-failed-unknown-columns-in-header-code}

このエラーは通常、CSV データ ファイルにヘッダーが含まれていないために発生します (最初の行は列名ではなくデータです)。そのため、 TiDB Lightning構成ファイルに次の構成を追加する必要があります。

    [mydumper.csv]
    header = false

### <code>Unknown character set</code> {#code-unknown-character-set-code}

TiDB はすべての MySQL 文字セットをサポートしていません。そのため、インポート中にテーブル スキーマを作成するときにサポートされていない文字セットが使用されると、 TiDB Lightning はこのエラーを報告します。このエラーを回避するには、特定のデータに応じて[TiDB でサポートされている文字セット](/character-set-and-collation.md)使用してダウンストリームで事前にテーブル スキーマを作成します。

### <code>invalid compression type ...</code> {#code-invalid-compression-type-code}

-   TiDB Lightning v6.4.0 以降のバージョンでは、次の圧縮データ ファイルのみがサポートされています: `gzip` 、 `snappy` 、および`zstd` 。その他の種類の圧縮ファイルではエラーが発生します。ソース データ ファイルが格納されているディレクトリにサポートされていない圧縮ファイルが存在する場合、タスクによってエラーが報告されます。このようなエラーを回避するには、サポートされていないファイルをインポート データ ディレクトリから移動します。詳細については、 [圧縮ファイル](/tidb-lightning/tidb-lightning-data-source.md#compressed-files)参照してください。

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。Snappy 圧縮の他のバリエーションはサポートされていません。
