---
title: Troubleshoot TiDB Lightning
summary: Learn the common problems you might encounter when you use TiDB Lightning and their solutions.
---

# TiDB Lightningのトラブルシューティング {#troubleshoot-tidb-lightning}

このドキュメントでは、 TiDB Lightning を使用するときに発生する可能性のある一般的な問題とその解決策を要約します。

## インポート速度が遅すぎる {#import-speed-is-too-slow}

通常、 TiDB Lightningが 256 MB データ ファイルをインポートするには、スレッドごとに 2 分かかります。速度がこれより大幅に遅い場合は、エラーが発生します。各データ ファイルにかかった時間は、 `restore chunk … takes`のログから確認できます。これは、Grafana のメトリクスからも観察できます。

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

最新バージョンをお試しください。もしかしたら新たな速度向上があるかもしれません。

## <code>tidb-lightning</code>プロセスがバックグラウンドで実行中に突然終了する {#the-code-tidb-lightning-code-process-suddenly-quits-while-running-in-background}

これは、 `tidb-lightning`間違って開始したことが原因である可能性があり、そのためシステムが SIGHUP シグナルを送信して`tidb-lightning`プロセスを停止させます。この状況では、通常、 `tidb-lightning.log`次のログを出力します。

    [2018/08/10 07:29:08.310 +08:00] [INFO] [main.go:41] ["got signal to exit"] [signal=hangup]

コマンドラインで`nohup`直接使用して`tidb-lightning`を開始することはお勧めできません。 [`tidb-lightning`を開始する](/tidb-lightning/deploy-tidb-lightning.md#step-3-start-tidb-lightning)スクリプトを実行することで実行できます。

さらに、 TiDB Lightningの最後のログでエラーが「コンテキストがキャンセルされました」であることが示されている場合は、最初の「ERROR」レベルのログを検索する必要があります。通常、この「ERROR」レベルのログの後には「終了する信号を取得しました」というメッセージが続きます。これは、 TiDB Lightning が割り込み信号を受信して​​終了したことを示します。

## TiDB クラスターは大量の CPU リソースを使用し、 TiDB Lightningを使用した後は動作が非常に遅くなります。 {#the-tidb-cluster-uses-lots-of-cpu-resources-and-runs-very-slowly-after-using-tidb-lightning}

`tidb-lightning`が異常終了した場合、クラスターは本番には適さない「インポート モード」でスタックする可能性があります。現在のモードは、次のコマンドを使用して取得できます。

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

次のコマンドを使用して、クラスターを強制的に「通常モード」に戻すことができます。

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

## TiDB Lightning がエラーを報告する {#tidb-lightning-reports-an-error}

### <code>could not find first pair, this shouldn't happen</code> {#code-could-not-find-first-pair-this-shouldn-t-happen-code}

このエラーは、 TiDB Lightningがソートされたローカル ファイルを読み取るときに、 TiDB Lightningによって開かれたファイルの数がシステム制限を超えたために発生する可能性があります。 Linux システムでは、 `ulimit -n`コマンドを使用して、このシステム制限の値が小さすぎるかどうかを確認できます。インポート中にこの値を`1000000` ( `ulimit -n 1000000` ) に調整することをお勧めします。

### <code>checksum failed: checksum mismatched remote vs local</code> {#code-checksum-failed-checksum-mismatched-remote-vs-local-code}

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

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

2.  ターゲット データベースの負荷を軽減するために、外部データベースを使用してチェックポイント (変更`[checkpoint] dsn` ) を保存することを検討してください。

3.  TiDB Lightning が不適切に再起動された場合は、 FAQの「 [TiDB Lightning を適切に再起動する方法](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning) 」セクションも参照してください。

### <code>Checkpoint for … has invalid status:</code> (エラー コード) {#code-checkpoint-for-has-invalid-status-code-error-code}

**原因**: [チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)が有効になっており、 TiDB Lightningまたは TiKV Importer が以前に異常終了しました。偶発的なデータ破損を防ぐため、エラーが解決されるまでTiDB Lightning は起動しません。

エラー コードは 25 より小さい整数で、取り得る値は 0、3、6、9、12、14、15、17、18、20、および 21 です。整数は、インポートで予期しない終了が発生したステップを示します。プロセス。整数が大きいほど、終了は後のステップで発生します。

**解決策**:

エラーの原因が無効なデータソースである場合は、 `tidb-lightning-ctl`使用してインポートされたデータを削除し、Lightning を再起動します。

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

他のオプションについては、 [チェックポイント制御](/tidb-lightning/tidb-lightning-checkpoints.md#checkpoints-control)セクションを参照してください。

### <code>cannot guess encoding for input file, please convert to UTF-8 manually</code> {#code-cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually-code}

**原因**: TiDB Lightning は、テーブル スキーマの UTF-8 および GB-18030 エンコーディングのみを認識します。このエラーは、ファイルがこれらのエンコーディングのいずれでもない場合に発生します。過去`ALTER TABLE`の実行により、ファイルに UTF-8 の文字列と GB-18030 の別の文字列が含まれるなど、エンコーディングが混在している可能性もあります。

**解決策**:

1.  ファイル全体が UTF-8 または GB-18030 になるようにスキーマを修正してください。

2.  ターゲット データベース内の影響を受けるテーブルを手動で`CREATE`ます。

3.  チェックをスキップするには`[mydumper] character-set = "binary"`を設定します。これにより、ターゲット データベースに mojibake が導入される可能性があることに注意してください。

### <code>[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 …}'</code> {#code-sql2kv-sql-encode-error-types-1292-invalid-time-format-1970-1-1-code}

**原因**: テーブルに`timestamp`タイプの列が含まれていますが、時刻値自体が存在しません。これは、DST の変更または時刻値がサポートされている範囲 (1970 年 1 月 1 日から 2038 年 1 月 19 日) を超えているためです。

**解決策**:

1.  TiDB Lightningとソース データベースが同じタイム ゾーンを使用していることを確認します。

    TiDB Lightningを直接実行する場合、 `$TZ`環境変数を使用してタイムゾーンを強制できます。

    ```sh
    # Manual deployment, and force Asia/Shanghai.
    TZ='Asia/Shanghai' bin/tidb-lightning -config tidb-lightning.toml
    ```

2.  クラスター全体が同じ最新バージョン`tzdata` (バージョン 2018i 以降) を使用していることを確認します。

    CentOS では、 `yum info tzdata`を実行して、インストールされているバージョンとアップデートがあるかどうかを確認します。 `yum upgrade tzdata`を実行してパッケージをアップグレードします。

### <code>[Error 8025: entry too large, the max entry size is 6291456]</code> {#code-error-8025-entry-too-large-the-max-entry-size-is-6291456-code}

**原因**: TiDB Lightningによって生成された 1 行のキーと値のペアが、TiDB によって設定された制限を超えています。

**解決**：

現時点では、TiDB の制限を回避することはできません。他のテーブルを正常にインポートするには、このテーブルを無視する必要があります。

### TiDB Lightning がモードを切り替えるときに<code>rpc error: code = Unimplemented ...</code> {#encounter-code-rpc-error-code-unimplemented-code-when-tidb-lightning-switches-the-mode}

**原因**: クラスター内の一部のノードは`switch-mode`をサポートしていません。たとえば、 TiFlash のバージョンが`v4.0.0-rc.2`より前の場合は、 [`switch-mode`サポートされていません](https://github.com/pingcap/tidb-lightning/issues/273) 。

**解決策**:

-   クラスター内にTiFlashノードがある場合は、クラスターを`v4.0.0-rc.2`以降のバージョンに更新できます。
-   クラスターをアップグレードしたくない場合は、 TiFlash を一時的に無効にします。

### <code>tidb lightning encountered error: TiDB version too old, expected '>=4.0.0', found '3.0.18'</code> {#code-tidb-lightning-encountered-error-tidb-version-too-old-expected-4-0-0-found-3-0-18-code}

TiDB Lightning Local バックエンドは、v4.0.0 以降のバージョンの TiDB クラスターへのデータのインポートのみをサポートします。 Local-backend を使用して v2.x または v3.x クラスターにデータをインポートしようとすると、上記のエラーが報告されます。現時点では、データのインポートにインポーター バックエンドまたは TiDB バックエンドを使用するように構成を変更できます。

一部の`nightly`バージョンは v4.0.0-beta.2 に似ている可能性があります。 TiDB Lightningのこれら`nightly`のバージョンは、実際にローカル バックエンドをサポートしています。バージョン`nightly`の使用時にこのエラーが発生した場合は、構成`check-requirements = false`を設定することでバージョン チェックをスキップできます。このパラメータを設定する前に、 TiDB Lightningの設定が対応するバージョンをサポートしていることを確認してください。そうしないと、インポートが失敗する可能性があります。

### <code>restore table test.district failed: unknown columns in header [...]</code> {#code-restore-table-test-district-failed-unknown-columns-in-header-code}

このエラーは通常、CSV データ ファイルにヘッダーが含まれていないために発生します (最初の行は列名ではなくデータです)。したがって、次の設定をTiDB Lightning設定ファイルに追加する必要があります。

    [mydumper.csv]
    header = false

### <code>Unknown character set</code> {#code-unknown-character-set-code}

TiDB は、すべての MySQL 文字セットをサポートしているわけではありません。したがって、インポート中にテーブル スキーマを作成するときにサポートされていない文字セットが使用された場合、 TiDB Lightning はこのエラーを報告します。このエラーを回避するには、特定のデータに応じて[TiDB がサポートする文字セット](/character-set-and-collation.md)使用してダウンストリームにテーブル スキーマを事前に作成します。

### <code>invalid compression type ...</code> {#code-invalid-compression-type-code}

-   TiDB Lightning v6.4.0 以降のバージョンは、圧縮データ ファイル`gzip` 、 `snappy` 、および`zstd`のみをサポートします。他の種類の圧縮ファイルではエラーが発生します。ソース データ ファイルが保存されているディレクトリにサポートされていない圧縮ファイルが存在する場合、タスクはエラーを報告します。このようなエラーを回避するには、サポートされていないファイルをインポート データ ディレクトリから移動します。詳細については、 [圧縮ファイル](/tidb-lightning/tidb-lightning-data-source.md#compressed-files)を参照してください。

> **注記：**
>
> Snappy 圧縮ファイルは[公式の Snappy フォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。
