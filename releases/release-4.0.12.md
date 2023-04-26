---
title: TiDB 4.0.12 Release Notes
---

# TiDB 4.0.12 リリースノート {#tidb-4-0-12-release-notes}

発売日：2021年4月2日

TiDB バージョン: 4.0.12

## 新機能 {#new-features}

-   TiFlash

    -   `tiflash replica`のオンライン ローリング アップデートのステータスをチェックするツールを追加する

## 改良点 {#improvements}

-   TiDB

    -   `batch cop`モード[#23164](https://github.com/pingcap/tidb/pull/23164)の`EXPLAIN`ステートメントの出力情報を絞り込む
    -   `EXPLAIN`文の出力にstorageレイヤーにプッシュできない式の警告情報を追加[#23020](https://github.com/pingcap/tidb/pull/23020)
    -   DDL パッケージコードの一部を`Execute` / `ExecRestricted`から安全な API に移行する (2) [#22935](https://github.com/pingcap/tidb/pull/22935)
    -   DDL パッケージコードの一部を`Execute` / `ExecRestricted`から安全な API に移行する (1) [#22929](https://github.com/pingcap/tidb/pull/22929)
    -   スローログ[#22918](https://github.com/pingcap/tidb/pull/22918)に`optimization-time`と`wait-TS-time`を追加します。
    -   `infoschema.partitions`テーブル[#22489](https://github.com/pingcap/tidb/pull/22489)からのクエリ`partition_id`をサポート
    -   `last_plan_from_binding`を追加して、SQL ステートメントの実行計画がバインディング[#21430](https://github.com/pingcap/tidb/pull/21430)のヒントと一致するかどうかをユーザーが認識できるようにします。
    -   `pre-split`オプション[#22872](https://github.com/pingcap/tidb/pull/22872)を使用せずに切り捨てられたテーブルを散布する
    -   `str_to_date`式[#22812](https://github.com/pingcap/tidb/pull/22812)に 3 つの書式指定子を追加します
    -   `PREPARE`の実行失敗をメトリクス モニターに`Failed Query OPM`として記録する[#22672](https://github.com/pingcap/tidb/pull/22672)
    -   `tidb_snapshot`が設定されている場合、 `PREPARE`実行のエラーを報告しない[#22641](https://github.com/pingcap/tidb/pull/22641)

-   TiKV

    -   短時間に大量の再接続を防ぐ[#9879](https://github.com/tikv/tikv/pull/9879)
    -   多くのトゥームストーンのシナリオで書き込み操作とバッチ取得を最適化する[#9729](https://github.com/tikv/tikv/pull/9729)
    -   デフォルト値の`leader-transfer-max-log-lag`を`128`に変更して、リーダー転送の成功率を[#9605](https://github.com/tikv/tikv/pull/9605)に上げます

-   PD

    -   `pending-peers`つまたは`down-peers`変更があった場合にのみリージョンキャッシュを更新します。これにより、ハートビートを更新するプレッシャーが軽減されます[#3471](https://github.com/pingcap/pd/pull/3471)
    -   `split-cache`の地域がマージの対象にならないようにする[#3459](https://github.com/pingcap/pd/pull/3459)

-   TiFlash

    -   構成ファイルを最適化し、不要な項目を削除する
    -   TiFlashバイナリ ファイルのサイズを縮小する
    -   アダプティブ アグレッシブ GC 戦略を使用してメモリ使用量を削減する

-   ツール

    -   TiCDC

        -   ユーザーが現在のタイムスタンプの`start-ts`または`checkpoint-ts`日前の変更フィードを作成または再開するときに、二重確認を追加します[#1497](https://github.com/pingcap/tiflow/pull/1497)
        -   Old Value 機能用の Grafana パネルを追加する[#1571](https://github.com/pingcap/tiflow/pull/1571)

    -   バックアップと復元 (BR)

        -   `HTTP_PROXY`と`HTTPS_PROXY`環境変数を記録する[#827](https://github.com/pingcap/br/pull/827)
        -   多くのテーブルがある場合のバックアップ パフォーマンスの向上[#745](https://github.com/pingcap/br/pull/745)
        -   サービスのセーフ ポイント チェックが失敗した場合にエラーを報告する[#826](https://github.com/pingcap/br/pull/826)
        -   `backupmeta` [#803](https://github.com/pingcap/br/pull/803)に`cluster_version`と`br_version`情報を追加します。
        -   外部storageエラーの再試行を追加して、バックアップの成功率を高めます[#851](https://github.com/pingcap/br/pull/851)
        -   バックアップ中のメモリ使用量を減らす[#886](https://github.com/pingcap/br/pull/886)

    -   TiDB Lightning

        -   予期しないエラーを回避するために、 TiDB Lightningを実行する前に TiDB クラスターのバージョンを確認してください[#787](https://github.com/pingcap/br/pull/787)
        -   TiDB Lightning が`cancel`エラー[#867](https://github.com/pingcap/br/pull/867)を満たすとすぐに失敗する
        -   `tikv-importer.engine-mem-cache-size`と`tikv-importer.local-writer-mem-cache-size`構成項目を追加して、メモリ使用量とパフォーマンスのバランスを取る[#866](https://github.com/pingcap/br/pull/866)
        -   TiDB Lightning の Local-backend に対して`batch split region`を並行して実行し、インポート速度を向上させます[#868](https://github.com/pingcap/br/pull/868)
        -   TiDB Lightningを使用して S3storageからデータをインポートする場合、 TiDB Lightning は`s3:ListBucket`パーミッション[#919](https://github.com/pingcap/br/pull/919)を必要としなくなりました
        -   チェックポイントから再開するとき、 TiDB Lightning は元のエンジンを使用し続けます[#924](https://github.com/pingcap/br/pull/924)

## バグの修正 {#bug-fixes}

-   TiDB

    -   セッション変数が 16 進数リテラルの場合、 `get`変数式がおかしくなる問題を修正[#23372](https://github.com/pingcap/tidb/pull/23372)
    -   `Enum`または`Set`タイプ[#23292](https://github.com/pingcap/tidb/pull/23292)の高速実行計画を作成するときに、間違った照合順序が使用される問題を修正します。
    -   `nullif`式を`is-null` [#23279](https://github.com/pingcap/tidb/pull/23279)と一緒に使用すると間違った結果になる可能性がある問題を修正
    -   自動分析が時間範囲外でトリガーされる問題を修正します[#23219](https://github.com/pingcap/tidb/pull/23219)
    -   `CAST`関数が`point get`プラン[#23211](https://github.com/pingcap/tidb/pull/23211)のエラーを無視する可能性がある問題を修正します。
    -   `CurrentDB`が空[#23209](https://github.com/pingcap/tidb/pull/23209)のときに SPM が有効にならないバグを修正
    -   IndexMerge プラン[#23165](https://github.com/pingcap/tidb/pull/23165)のテーブル フィルターが間違っている可能性がある問題を修正します。
    -   `NULL`定数[#23135](https://github.com/pingcap/tidb/pull/23135)の戻り型で予期しない`NotNullFlag`が返される問題を修正
    -   テキスト型[#23092](https://github.com/pingcap/tidb/pull/23092)で照合順序できない場合がある不具合を修正
    -   範囲パーティションが`IN`式[#23074](https://github.com/pingcap/tidb/pull/23074)を誤って処理する可能性がある問題を修正します
    -   TiKV ストアをトゥームストーンとしてマークした後、同じ IP アドレスとポートを持つ別の StoreID で新しい TiKV ストアを開始すると、 `StoreNotMatch`エラー[#23071](https://github.com/pingcap/tidb/pull/23071)が返される問題を修正します。
    -   `YEAR` [#22844](https://github.com/pingcap/tidb/pull/22844)と比較して`NULL`の場合は`INT`タイプを調整しないでください
    -   `auto_random`列[#22736](https://github.com/pingcap/tidb/pull/22736)のテーブルにデータをロードするときに接続が失われる問題を修正
    -   DDL 操作がキャンセル パスでパニックにpanicしたときの DDL ハングオーバーの問題を修正します[#23297](https://github.com/pingcap/tidb/pull/23297)
    -   `YEAR`列を`NULL` [#23104](https://github.com/pingcap/tidb/pull/23104)と比較するときのインデックス スキャンの間違ったキー範囲を修正します。
    -   正常に作成されたビューが使用に失敗する問題を修正します[#23083](https://github.com/pingcap/tidb/pull/23083)

-   TiKV

    -   `IN`式が符号なし/符号付き整数を適切に処理しない問題を修正します[#9850](https://github.com/tikv/tikv/pull/9850)
    -   取り込み操作が再入可能でない問題を修正します[#9779](https://github.com/tikv/tikv/pull/9779)
    -   TiKV コプロセッサ[#9666](https://github.com/tikv/tikv/pull/9666)で JSON を文字列に変換するとスペースがなくなる問題を修正

-   PD

    -   ストアにラベル[#3474](https://github.com/pingcap/pd/pull/3474)がない場合、分離レベルが間違っているというバグを修正します

-   TiFlash

    -   `binary`型の列のデフォルト値に先頭または末尾のゼロ バイトが含まれている場合に、誤った実行結果になる問題を修正します。
    -   データベースの名前に特殊文字が含まれていると、 TiFlash がスキーマの同期に失敗するバグを修正
    -   `IN`進数値で 1 式を処理するときに誤った結果が得られる問題を修正します。
    -   Grafana で表示される開いているファイル数のメトリックが高いというバグを修正します
    -   TiFlashが`Timestamp`リテラルをサポートしていないバグを修正
    -   `FROM_UNIXTIME`式の処理中に応答しない可能性がある問題を修正します
    -   文字列を整数としてキャストしたときに誤った結果が返される問題を修正
    -   `like`関数が間違った結果を返すことがあるバグを修正

-   ツール

    -   TiCDC

        -   `resolved ts`イベント[#1464](https://github.com/pingcap/tiflow/pull/1464)の乱れ問題を修正
        -   ネットワークの問題による誤ったテーブル スケジューリングによるデータ損失の問題を修正する[#1508](https://github.com/pingcap/tiflow/pull/1508)
        -   プロセッサが停止した後、リソースがタイミングよく解放されないバグを修正します[#1547](https://github.com/pingcap/tiflow/pull/1547)
        -   トランザクション カウンターが正しく更新されず、データベース接続リークが発生する可能性があるバグを修正します[#1524](https://github.com/pingcap/tiflow/pull/1524)
        -   PD にジッターがある場合に複数の所有者が共存でき、テーブルが失われる可能性があるという問題を修正します[#1540](https://github.com/pingcap/tiflow/pull/1540)

    -   バックアップと復元 (BR)

        -   対象のパスがバケット名[#733](https://github.com/pingcap/br/pull/733)の場合、s3storageの`WalkDir` `nil`返すバグを修正
        -   `status`ポートが TLS [#839](https://github.com/pingcap/br/pull/839)で提供されないバグを修正

    -   TiDB Lightning

        -   ファイルが既に存在することを TiKV Importer が無視する可能性があるエラーを修正します[#848](https://github.com/pingcap/br/pull/848)
        -   TiDB Lightning が間違ったタイムスタンプを使用して間違ったデータを読み取る可能性があるバグを修正します[#850](https://github.com/pingcap/br/pull/850)
        -   TiDB Lightning の予期しない終了により、チェックポイント ファイル[#889](https://github.com/pingcap/br/pull/889)が破損する可能性があるバグを修正
        -   `cancel`エラーが無視されるために発生する可能性のあるデータ エラーの問題を修正します[#874](https://github.com/pingcap/br/pull/874)
