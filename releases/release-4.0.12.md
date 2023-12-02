---
title: TiDB 4.0.12 Release Notes
---

# TiDB 4.0.12 リリースノート {#tidb-4-0-12-release-notes}

発売日：2021年4月2日

TiDB バージョン: 4.0.12

## 新機能 {#new-features}

-   TiFlash

    -   オンライン ローリング アップデートの`tiflash replica`のステータスを確認するツールを追加します。

## 改善点 {#improvements}

-   TiDB

    -   `EXPLAIN`ステートメントの出力情報を`batch cop`モード[#23164](https://github.com/pingcap/tidb/pull/23164)に絞り込む
    -   `EXPLAIN`ステートメント[#23020](https://github.com/pingcap/tidb/pull/23020)の出力に、storageレイヤーにプッシュできない式に関する警告情報を追加します。
    -   `Execute` / `ExecRestricted`のDDLパッケージコードの一部を安全なAPIに移行する(2) [#22935](https://github.com/pingcap/tidb/pull/22935)
    -   DDLパッケージコードの一部`ExecRestricted` `Execute`から安全なAPIに移行(1) [#22929](https://github.com/pingcap/tidb/pull/22929)
    -   スローログ[#22918](https://github.com/pingcap/tidb/pull/22918)に`optimization-time`と`wait-TS-time`を追加します。
    -   `infoschema.partitions`テーブル[#22489](https://github.com/pingcap/tidb/pull/22489)からの`partition_id`クエリのサポート
    -   `last_plan_from_binding`を追加すると、SQL ステートメントの実行計画がバインディング[#21430](https://github.com/pingcap/tidb/pull/21430)のヒントと一致するかどうかをユーザーが知ることができます。
    -   `pre-split`オプション[#22872](https://github.com/pingcap/tidb/pull/22872)を使用せずに切り捨てられたテーブルを分散する
    -   `str_to_date`式[#22812](https://github.com/pingcap/tidb/pull/22812)に 3 つの書式指定子を追加します。
    -   `PREPARE`実行失敗をメトリック モニター[#22672](https://github.com/pingcap/tidb/pull/22672)に`Failed Query OPM`として記録します。
    -   `tidb_snapshot`が[#22641](https://github.com/pingcap/tidb/pull/22641)に設定されている場合、 `PREPARE`の実行でエラーを報告しません。

-   TiKV

    -   短期間に大量の再接続を防止する[#9879](https://github.com/tikv/tikv/pull/9879)
    -   多数のトゥームストーン[#9729](https://github.com/tikv/tikv/pull/9729)のシナリオにおける書き込み操作とバッチ取得を最適化します。
    -   デフォルト値の`leader-transfer-max-log-lag`を`128`に変更して、リーダー転送の成功率を高めます[#9605](https://github.com/tikv/tikv/pull/9605)

-   PD

    -   `pending-peers`または`down-peers`変更された場合にのみリージョンキャッシュを更新します。これにより、ハートビートの更新のプレッシャーが軽減されます[#3471](https://github.com/pingcap/pd/pull/3471)
    -   `split-cache`のリージョンがマージ[#3459](https://github.com/pingcap/pd/pull/3459)のターゲットにならないようにする

-   TiFlash

    -   設定ファイルを最適化し、不要な項目を削除する
    -   TiFlashバイナリ ファイルのサイズを削減します。
    -   アダプティブ アグレッシブ GC 戦略を使用してメモリ使用量を削減する

-   ツール

    -   TiCDC

        -   ユーザーが変更フィードを作成または再開するときに、現在のタイムスタンプの 1 日前に`start-ts`または`checkpoint-ts`使用して二重確認を追加します[#1497](https://github.com/pingcap/tiflow/pull/1497)
        -   Old Value 機能[#1571](https://github.com/pingcap/tiflow/pull/1571)用の Grafana パネルを追加します。

    -   バックアップと復元 (BR)

        -   `HTTP_PROXY`および`HTTPS_PROXY`環境変数をログに記録します[#827](https://github.com/pingcap/br/pull/827)
        -   多数のテーブルがある場合のバックアップ パフォーマンスを向上させる[#745](https://github.com/pingcap/br/pull/745)
        -   サービス セーフ ポイント チェックが失敗した場合にエラーを報告する[#826](https://github.com/pingcap/br/pull/826)
        -   `backupmeta` [#803](https://github.com/pingcap/br/pull/803)に`cluster_version`と`br_version`情報を追加します。
        -   バックアップ[#851](https://github.com/pingcap/br/pull/851)の成功率を高めるために、外部storageエラーに対する再試行を追加します。
        -   バックアップ時のメモリ使用量を削減[#886](https://github.com/pingcap/br/pull/886)

    -   TiDB Lightning

        -   予期しないエラーを避けるために、 TiDB Lightningを実行する前に TiDB クラスターのバージョンを確認してください[#787](https://github.com/pingcap/br/pull/787)
        -   TiDB Lightning が`cancel`エラー[#867](https://github.com/pingcap/br/pull/867)に該当すると高速に失敗します
        -   `tikv-importer.engine-mem-cache-size`と`tikv-importer.local-writer-mem-cache-size`構成項目を追加して、メモリ使用量とパフォーマンスのバランスをとります[#866](https://github.com/pingcap/br/pull/866)
        -   TiDB Lightning のローカル バックエンドに対して`batch split region`を並行して実行して、インポート速度を向上させます[#868](https://github.com/pingcap/br/pull/868)
        -   TiDB Lightningを使用して S3storageからデータをインポートする場合、 TiDB Lightning は`s3:ListBucket`権限[#919](https://github.com/pingcap/br/pull/919)を必要としなくなりました。
        -   チェックポイントから再開する場合、 TiDB Lightning は元のエンジン[#924](https://github.com/pingcap/br/pull/924)を使用し続けます。

## バグの修正 {#bug-fixes}

-   TiDB

    -   セッション変数が16進リテラル[#23372](https://github.com/pingcap/tidb/pull/23372)の場合、 `get`変数式が誤る問題を修正
    -   `Enum`または`Set`タイプ[#23292](https://github.com/pingcap/tidb/pull/23292)の高速実行プランを作成するときに間違った照合順序が使用される問題を修正
    -   `nullif`式を`is-null` [#23279](https://github.com/pingcap/tidb/pull/23279)と一緒に使用した場合に発生する可能性のある間違った結果を修正しました。
    -   自動分析が時間範囲外でトリガーされる問題を修正します[#23219](https://github.com/pingcap/tidb/pull/23219)
    -   `CAST`関数が`point get`プラン[#23211](https://github.com/pingcap/tidb/pull/23211)のエラーを無視する可能性がある問題を修正
    -   `CurrentDB`が空の場合に SPM が有効にならないバグを修正[#23209](https://github.com/pingcap/tidb/pull/23209)
    -   IndexMerge プラン[#23165](https://github.com/pingcap/tidb/pull/23165)の間違ったテーブル フィルターが存在する可能性がある問題を修正します。
    -   定数`NULL` [#23135](https://github.com/pingcap/tidb/pull/23135)値の型で予期しない`NotNullFlag`が発生する問題を修正
    -   テキストタイプ[#23092](https://github.com/pingcap/tidb/pull/23092)で照合順序処理ができない場合があるバグを修正
    -   範囲パーティションが`IN`式[#23074](https://github.com/pingcap/tidb/pull/23074)を誤って処理する可能性がある問題を修正します。
    -   TiKV ストアを廃棄済みとしてマークした後、同じ IP アドレスとポートを持つ異なる StoreID で新しい TiKV ストアを開始すると、 `StoreNotMatch`エラー[#23071](https://github.com/pingcap/tidb/pull/23071)が返され続ける問題を修正します。
    -   `INT`タイプが`NULL`の場合、 `YEAR` [#22844](https://github.com/pingcap/tidb/pull/22844)と比較して調整しないでください。
    -   `auto_random`列[#22736](https://github.com/pingcap/tidb/pull/22736)のテーブルにデータをロードするときに接続が失われる問題を修正
    -   DDL 操作がキャンセル パス[#23297](https://github.com/pingcap/tidb/pull/23297)でパニックにpanicした場合の DDL ハングオーバーの問題を修正します。
    -   `YEAR`列と`NULL` [#23104](https://github.com/pingcap/tidb/pull/23104)を比較するときのインデックス スキャンの間違ったキー範囲を修正しました。
    -   正常に作成されたビューが使用できない問題を修正[#23083](https://github.com/pingcap/tidb/pull/23083)

-   TiKV

    -   `IN`式が符号なし/符号付き整数を適切に処理しない問題を修正します[#9850](https://github.com/tikv/tikv/pull/9850)
    -   取り込み操作が再入可能ではない問題を修正[#9779](https://github.com/tikv/tikv/pull/9779)
    -   TiKV コプロセッサ[#9666](https://github.com/tikv/tikv/pull/9666)で JSON を文字列に変換するときにスペースが失われる問題を修正

-   PD

    -   ストアにラベル[#3474](https://github.com/pingcap/pd/pull/3474)がない場合、分離レベルが間違っているバグを修正

-   TiFlash

    -   `binary` type カラムのデフォルト値に先頭または末尾のゼロバイトが含まれている場合に、実行結果が正しくなくなる問題を修正
    -   データベース名に特殊文字が含まれている場合、 TiFlash がスキーマの同期に失敗するバグを修正
    -   10 進数値を含む`IN`式を処理するときに誤った結果が発生する問題を修正
    -   Grafanaで表示される開かれたファイル数のメトリクスが高くなるバグを修正
    -   TiFlashが`Timestamp`リテラルをサポートしていないバグを修正
    -   `FROM_UNIXTIME`式の処理中に応答しない可能性がある問題を修正
    -   文字列を整数としてキャストするときに誤った結果が表示される問題を修正
    -   `like`関数が間違った結果を返す可能性があるバグを修正

-   ツール

    -   TiCDC

        -   `resolved ts`イベント[#1464](https://github.com/pingcap/tiflow/pull/1464)の障害問題を修正
        -   ネットワークの問題による間違ったテーブルのスケジューリングによって引き起こされるデータ損失の問題を修正します[#1508](https://github.com/pingcap/tiflow/pull/1508)
        -   プロセッサ停止後のリソースの早期解放のバグを修正[#1547](https://github.com/pingcap/tiflow/pull/1547)
        -   トランザクションカウンターが正しく更新されず、データベース接続リーク[#1524](https://github.com/pingcap/tiflow/pull/1524)が発生する可能性があるバグを修正
        -   PD にジッターがある場合に複数の所有者が共存でき、テーブルが[#1540](https://github.com/pingcap/tiflow/pull/1540)欠落する可能性がある問題を修正します。

    -   バックアップと復元 (BR)

        -   ターゲットパスがバケット名[#733](https://github.com/pingcap/br/pull/733)の場合、s3storageの`WalkDir` `nil`を返すバグを修正
        -   `status`ポートが TLS [#839](https://github.com/pingcap/br/pull/839)で提供されないバグを修正

    -   TiDB Lightning

        -   TiKV インポーターがファイルが既に存在していることを無視する可能性があるエラーを修正します[#848](https://github.com/pingcap/br/pull/848)
        -   TiDB Lightning が間違ったタイムスタンプを使用し、間違ったデータを読み取る可能性があるバグを修正しました[#850](https://github.com/pingcap/br/pull/850)
        -   TiDB Lightning の予期しない終了によりチェックポイント ファイル[#889](https://github.com/pingcap/br/pull/889)が破損する可能性があるバグを修正
        -   `cancel`エラーが無視されるためにデータ エラーが発生する可能性がある問題を修正します[#874](https://github.com/pingcap/br/pull/874)
