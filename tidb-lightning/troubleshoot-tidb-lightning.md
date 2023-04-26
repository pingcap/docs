---
title: Troubleshoot TiDB Lightning
summary: Learn the common problems you might encounter when you use TiDB Lightning and their solutions.
---

# TiDB Lightningのトラブルシューティング {#troubleshoot-tidb-lightning}

このドキュメントでは、 TiDB Lightning を使用する際に遭遇する可能性のある一般的な問題とその解決策をまとめています。

## インポート速度が遅すぎる {#import-speed-is-too-slow}

通常、 TiDB Lightningが 256 MB のデータ ファイルをインポートするには、スレッドごとに 2 分かかります。速度がこれより大幅に遅い場合は、エラーがあります。 `restore chunk … takes`に言及しているログから、各データ ファイルにかかった時間を確認できます。これは、Grafana のメトリクスからも確認できます。

TiDB Lightning が遅くなる理由はいくつかあります。

**原因 1** : `region-concurrency`の設定が高すぎるため、スレッドの競合が発生し、パフォーマンスが低下します。

1.  設定は、ログの先頭から`region-concurrency`を検索して見つけることができます。
2.  TiDB Lightning が他のサービス (TiKV Importer など) と同じマシンを共有している場合、 `region-concurrency` CPU コアの総数の 75% に**手動で**設定する必要があります。
3.  CPU にクォータがある場合 (たとえば、Kubernetes の設定によって制限されている場合)、 TiDB Lightning はこれを読み取ることができない場合があります。この場合、 `region-concurrency`も**手動で**減らす必要があります。

**原因 2** : テーブル スキーマが複雑すぎます。

インデックスを追加するたびに、行ごとに新しい KV ペアが導入されます。 N 個のインデックスがある場合、インポートされる実際のサイズはDumpling出力のサイズの約 (N+1) 倍になります。インデックスが無視できる場合は、最初にそれらをスキーマから削除し、インポートの完了後に`CREATE INDEX`使用してそれらを追加し直すことができます。

**原因 3** : 各ファイルが大きすぎます。

TiDB Lightning は、データ ソースが約 256 MB のサイズの複数のファイルに分割され、データを並列処理できる場合に最適に機能します。各ファイルが大きすぎると、 TiDB Lightning が応答しない場合があります。

データ ソースが CSV で、すべての CSV ファイルに改行制御文字 (U+000A および U+000D) を含むフィールドがない場合は、「厳密な形式」をオンにして、 TiDB Lightning が大きなファイルを自動的に分割できるようにすることができます。

```toml
[mydumper]
strict-format = true
```

**原因 4** : TiDB Lightningが古すぎる。

最新バージョンをお試しください。たぶん、新しい速度の改善があります。

## バックグラウンドで実行中に<code>tidb-lightning</code>プロセスが突然終了する {#the-code-tidb-lightning-code-process-suddenly-quits-while-running-in-background}

これは、 `tidb-lightning`誤って開始したことが原因である可能性があり、システムが SIGHUP シグナルを送信して`tidb-lightning`プロセスを停止させます。この状況では、通常、 `tidb-lightning.log`次のログを出力します。

```
[2018/08/10 07:29:08.310 +08:00] [INFO] [main.go:41] ["got signal to exit"] [signal=hangup]
```

コマンドラインで`nohup`直接使用して`tidb-lightning`を開始することはお勧めしません。スクリプトを実行することで[`tidb-lightning`を開始](/tidb-lightning/deploy-tidb-lightning.md#step-3-start-tidb-lightning)できます。

また、 TiDB Lightningの最後のログでエラーが「コンテキストがキャンセルされました」と表示された場合は、最初の「ERROR」レベルのログを検索する必要があります。通常、この「エラー」レベルのログの後には「終了するシグナルがありました」が続きます。これは、 TiDB Lightning が割り込みシグナルを受信して終了したことを示します。

## TiDB クラスターは大量の CPU リソースを使用し、 TiDB Lightningを使用した後は非常に遅くなります {#the-tidb-cluster-uses-lots-of-cpu-resources-and-runs-very-slowly-after-using-tidb-lightning}

`tidb-lightning`が異常終了した場合、クラスターは本番に適していない「インポート モード」でスタックしている可能性があります。現在のモードは、次のコマンドを使用して取得できます。

{{< copyable "" >}}

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

次のコマンドを使用して、クラスターを強制的に「通常モード」に戻すことができます。

{{< copyable "" >}}

```sh
tidb-lightning-ctl --config tidb-lightning.toml --fetch-mode
```

## TiDB Lightning がエラーを報告する {#tidb-lightning-reports-an-error}

### <code>could not find first pair, this shouldn't happen</code> {#code-could-not-find-first-pair-this-shouldn-t-happen-code}

このエラーは、 TiDB Lightningがソートされたローカル ファイルを読み取るときに、 TiDB Lightningによって開かれたファイルの数がシステムの制限を超えたために発生する可能性があります。 Linux システムでは、 `ulimit -n`コマンドを使用して、このシステム制限の値が小さすぎるかどうかを確認できます。インポート中にこの値を`1000000` ( `ulimit -n 1000000` ) に調整することをお勧めします。

### <code>checksum failed: checksum mismatched remote vs local</code> {#code-checksum-failed-checksum-mismatched-remote-vs-local-code}

**原因**: ローカル データ ソースとリモート インポート データベースのテーブルのチェックサムが異なります。このエラーには、いくつかのより深い理由があります。 `checksum mismatched`を含むログを確認することで、理由をさらに突き止めることができます。

`checksum mismatched`を含む行は、情報`total_kvs: x vs y`提供します。ここで、 `x` 、インポートの完了後にターゲット クラスターによって計算されたキーと値のペア (KV ペア) の数を示し、 `y` 、ローカル データによって生成されたキーと値のペアの数を示します。ソース。

-   `x`が大きい場合、ターゲット クラスタに KV ペアが多いことを意味します。
    -   インポート前にこのテーブルが空でない可能性があるため、データ チェックサムに影響します。 TiDB Lightning が以前に失敗してシャットダウンしたが、正しく再起動しなかった可能性もあります。
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

3.  TiDB Lightning が不適切に再起動された場合は、 FAQの「 [TiDB Lightning を適切に再起動する方法](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning) 」セクションも参照してください。

### <code>Checkpoint for … has invalid status:</code> (エラー コード) {#code-checkpoint-for-has-invalid-status-code-error-code}

**原因**: [チェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)が有効になっていて、 TiDB Lightningまたは TiKV Importer が以前に異常終了しました。偶発的なデータ破損を防ぐために、 TiDB Lightning はエラーが解決されるまで起動しません。

エラー コードは 25 より小さい整数で、可能な値は 0、3、6、9、12、14、15、17、18、20、および 21 です。整数は、インポートで予期しない終了が発生したステップを示します。プロセス。整数が大きいほど、出口が発生する後のステップです。

**ソリューション**:

エラーの原因が無効なデータ ソースである場合は、 `tidb-lightning-ctl`使用してインポートされたデータを削除し、Lightning を再起動します。

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

その他のオプションについては、セクション[チェックポイント制御](/tidb-lightning/tidb-lightning-checkpoints.md#checkpoints-control)を参照してください。

### <code>ResourceTemporarilyUnavailable("Too many open engines …: …")</code> {#code-resourcetemporarilyunavailable-too-many-open-engines-code}

**原因**: 同時実行エンジン ファイルの数が、 `tikv-importer`で指定された制限を超えています。これは、設定ミスが原因である可能性があります。さらに、 `tidb-lightning`異常終了した場合、エンジン ファイルがダングリング オープン状態のままになる可能性があり、これもこのエラーを引き起こす可能性があります。

**ソリューション**:

1.  `tikv-importer.toml`の`max-open-engines`の設定値を大きくします。この値は通常、使用可能なメモリによって決定されます。これは、次を使用して計算できます。

    最大メモリ使用量 ≈ `max-open-engines` × `write-buffer-size` × `max-write-buffer-number`

2.  `table-concurrency` + `index-concurrency`の値を減らして`max-open-engines`未満にします。

3.  `tikv-importer`を再起動して、すべてのエンジン ファイルを強制的に削除します (デフォルトは`./data.import/` )。これにより、部分的にインポートされたすべてのテーブルも削除されるため、 TiDB Lightning は古いチェックポイントをクリアする必要があります。

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

### <code>cannot guess encoding for input file, please convert to UTF-8 manually</code> {#code-cannot-guess-encoding-for-input-file-please-convert-to-utf-8-manually-code}

**原因**: TiDB Lightning は、テーブル スキーマの UTF-8 および GB-18030 エンコーディングのみを認識します。このエラーは、ファイルがこれらのエンコーディングのいずれでもない場合に発生します。履歴`ALTER TABLE`の実行により、UTF-8 の文字列と GB-18030 の別の文字列が含まれているなど、ファイルにエンコーディングが混在している可能性もあります。

**ソリューション**:

1.  ファイル全体が UTF-8 または GB-18030 になるようにスキーマを修正します。

2.  ターゲット データベース内の影響を受けるテーブルを手動で`CREATE`ます。

3.  チェックをスキップするには、 `[mydumper] character-set = "binary"`を設定します。これにより、対象データベースにモジバケが導入される可能性があることに注意してください。

### <code>[sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 …}'</code> {#code-sql2kv-sql-encode-error-types-1292-invalid-time-format-1970-1-1-code}

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

### <code>[Error 8025: entry too large, the max entry size is 6291456]</code> {#code-error-8025-entry-too-large-the-max-entry-size-is-6291456-code}

**原因**: TiDB Lightningによって生成されたキーと値のペアの単一行が、TiDB によって設定された制限を超えています。

**解決策**:

現在、TiDB の制限を回避することはできません。他のテーブルを正常にインポートするには、このテーブルのみを無視できます。

### <code>rpc error: code = Unimplemented ...</code> TiDB Lightning がモードを切り替えたとき {#encounter-code-rpc-error-code-unimplemented-code-when-tidb-lightning-switches-the-mode}

**原因**: クラスタ内の一部のノードが`switch-mode`をサポートしていません。たとえば、 TiFlash のバージョンが`v4.0.0-rc.2`より前の場合、 [`switch-mode`サポートされていません](https://github.com/pingcap/tidb-lightning/issues/273) .

**ソリューション**:

-   クラスターにTiFlashノードがある場合は、クラスターを`v4.0.0-rc.2`以上のバージョンに更新できます。
-   クラスタをアップグレードしない場合は、 TiFlash を一時的に無効にします。

### <code>tidb lightning encountered error: TiDB version too old, expected '>=4.0.0', found '3.0.18'</code> {#code-tidb-lightning-encountered-error-tidb-version-too-old-expected-4-0-0-found-3-0-18-code}

TiDB Lightning Local-backend は、v4.0.0 以降のバージョンの TiDB クラスターへのデータのインポートのみをサポートします。 Local-backend を使用して v2.x または v3.x クラスターにデータをインポートしようとすると、上記のエラーが報告されます。この時点で、データのインポートに Importer バックエンドまたは TiDB バックエンドを使用するように構成を変更できます。

一部の`nightly`バージョンは v4.0.0-beta.2 に類似している可能性があります。これら`nightly`のバージョンのTiDB Lightning は、実際には Local-backend をサポートしています。 `nightly`バージョンを使用しているときにこのエラーが発生した場合は、構成を`check-requirements = false`に設定してバージョン チェックをスキップできます。このパラメータを設定する前に、 TiDB Lightningの設定が対応するバージョンをサポートしていることを確認してください。そうしないと、インポートが失敗する可能性があります。

### <code>restore table test.district failed: unknown columns in header [...]</code> {#code-restore-table-test-district-failed-unknown-columns-in-header-code}

このエラーは通常、CSV データ ファイルにヘッダーが含まれていないために発生します (最初の行は列名ではなくデータです)。したがって、次の構成をTiDB Lightning構成ファイルに追加する必要があります。

```
[mydumper.csv]
header = false
```

### <code>Unknown character set</code> {#code-unknown-character-set-code}

TiDB はすべての MySQL 文字セットをサポートしているわけではありません。したがって、インポート中にテーブル スキーマを作成するときに、サポートされていない文字セットが使用されている場合、 TiDB Lightning はこのエラーを報告します。このエラーを回避するには、特定のデータに従って[TiDB がサポートする文字セット](/character-set-and-collation.md)を使用して、事前にダウンストリームでテーブル スキーマを作成できます。

### <code>invalid compression type ...</code> {#code-invalid-compression-type-code}

-   TiDB Lightning v6.4.0 以降のバージョンでは、 `.bak`ファイルと次の圧縮データ ファイルのみがサポートされます: `gzip` 、 `snappy` 、および`zstd` 。他のタイプのファイルはエラーの原因になります。サポートされていないファイルについては、事前にファイル名を変更するか、これらのファイルをインポート データ ディレクトリから移動して、このようなエラーを回避する必要があります。詳細については、 [圧縮ファイル](/tidb-lightning/tidb-lightning-data-source.md#compressed-files)を参照してください。
