---
title: TiDB 4.0.12 Release Notes
---

# TiDB4.0.12リリースノート {#tidb-4-0-12-release-notes}

発売日：2021年4月2日

TiDBバージョン：4.0.12

## 新機能 {#new-features}

-   TiFlash

    -   オンラインローリングアップデートの`tiflash replica`のステータスを確認するツールを追加します

## 改善 {#improvements}

-   TiDB

    -   `batch cop`モード[＃23164](https://github.com/pingcap/tidb/pull/23164)の`EXPLAIN`ステートメントの出力情報を調整します。
    -   `EXPLAIN`ステートメント[＃23020](https://github.com/pingcap/tidb/pull/23020)の出力に、ストレージレイヤーにプッシュできない式の警告情報を追加します。
    -   DDLパッケージコードの一部を`Execute`から安全なAPIに移行し[＃22935](https://github.com/pingcap/tidb/pull/22935) （2） `ExecRestricted`
    -   DDLパッケージコードの一部を`Execute`から安全なAPIに移行し[＃22929](https://github.com/pingcap/tidb/pull/22929) （1） `ExecRestricted`
    -   遅いログ[＃22918](https://github.com/pingcap/tidb/pull/22918)に`optimization-time`と`wait-TS-time`を追加します
    -   `infoschema.partitions`の表[＃22489](https://github.com/pingcap/tidb/pull/22489)から`partition_id`のクエリをサポート
    -   `last_plan_from_binding`を追加して、SQLステートメントの実行プランがバインディング[＃21430](https://github.com/pingcap/tidb/pull/21430)のヒントと一致するかどうかをユーザーが認識できるようにします。
    -   `pre-split`オプションなしで切り捨てられたテーブルを分散する[＃22872](https://github.com/pingcap/tidb/pull/22872)
    -   `str_to_date`式[＃22812](https://github.com/pingcap/tidb/pull/22812)に3つのフォーマット指定子を追加します
    -   `PREPARE`の実行失敗をメトリックモニター[＃22672](https://github.com/pingcap/tidb/pull/22672)に`Failed Query OPM`として記録します。
    -   `tidb_snapshot`が設定されている場合は`PREPARE`の実行でエラーを報告しない[＃22641](https://github.com/pingcap/tidb/pull/22641)

-   TiKV

    -   短時間で大量の再接続を防ぐ[＃9879](https://github.com/tikv/tikv/pull/9879)
    -   多くのトゥームストーンのシナリオで書き込み操作とバッチ取得を最適化する[＃9729](https://github.com/tikv/tikv/pull/9729)
    -   リーダーの異動の成功率を上げるには、デフォルト値の`leader-transfer-max-log-lag`を`128`に変更します[＃9605](https://github.com/tikv/tikv/pull/9605)

-   PD

    -   `pending-peers`つまたは`down-peers`の変更があった場合にのみ、リージョンキャッシュを更新します。これにより、ハートビートを更新するプレッシャーが軽減されます[＃3471](https://github.com/pingcap/pd/pull/3471)
    -   `split-cache`のリージョンがマージ[＃3459](https://github.com/pingcap/pd/pull/3459)のターゲットにならないようにします

-   TiFlash

    -   構成ファイルを最適化し、不要なアイテムを削除します
    -   TiFlashバイナリファイルのサイズを縮小します
    -   アダプティブアグレッシブGC戦略を使用して、メモリ使用量を削減します

-   ツール

    -   TiCDC

        -   ユーザーが現在のタイムスタンプの`start-ts`日前または`checkpoint-ts`日前にチェンジフィードを作成または再開するときに、二重の確認を追加します[＃1497](https://github.com/pingcap/tiflow/pull/1497)
        -   OldValue機能のGrafanaパネルを追加する[＃1571](https://github.com/pingcap/tiflow/pull/1571)

    -   バックアップと復元（BR）

        -   `HTTP_PROXY`と`HTTPS_PROXY`の環境変数をログに記録します[＃827](https://github.com/pingcap/br/pull/827)
        -   テーブルが多い場合のバックアップパフォーマンスの向上[＃745](https://github.com/pingcap/br/pull/745)
        -   サービスセーフポイントチェックが失敗した場合にエラーを報告する[＃826](https://github.com/pingcap/br/pull/826)
        -   [＃803](https://github.com/pingcap/br/pull/803)に`cluster_version`と`br_version`の情報を追加し`backupmeta`
        -   バックアップの成功率を上げるために、外部ストレージエラーの再試行を追加します[＃851](https://github.com/pingcap/br/pull/851)
        -   バックアップ中のメモリ使用量を削減[＃886](https://github.com/pingcap/br/pull/886)

    -   TiDB Lightning

        -   予期しないエラーを回避するために、TiDBLightningを実行する前にTiDBクラスタのバージョンを確認してください[＃787](https://github.com/pingcap/br/pull/787)
        -   TiDB Lightningが`cancel`のエラー[＃867](https://github.com/pingcap/br/pull/867)に遭遇すると、すぐに失敗します
        -   `tikv-importer.engine-mem-cache-size`と`tikv-importer.local-writer-mem-cache-size`の構成項目を追加して、メモリ使用量とパフォーマンスのバランスを取ります[＃866](https://github.com/pingcap/br/pull/866)
        -   TiDB Lightningのローカルバックエンドに対して`batch split region`を並行して実行し、インポート速度を上げます[＃868](https://github.com/pingcap/br/pull/868)
        -   TiDB Lightningを使用してS3ストレージからデータをインポートする場合、TiDBLightningは`s3:ListBucket`パーミッション[＃919](https://github.com/pingcap/br/pull/919)を必要としなくなりました。
        -   チェックポイントから再開する場合、TiDBLightningは元のエンジンを使用し続けます[＃924](https://github.com/pingcap/br/pull/924)

## バグの修正 {#bug-fixes}

-   TiDB

    -   セッション変数が16進リテラルである場合に`get`変数式が間違ってしまう問題を修正します[＃23372](https://github.com/pingcap/tidb/pull/23372)
    -   `Enum`または`Set`タイプ[＃23292](https://github.com/pingcap/tidb/pull/23292)の高速実行プランを作成するときに間違った照合順序が使用される問題を修正します
    -   [＃23279](https://github.com/pingcap/tidb/pull/23279)で使用した場合に発生する可能性のある`nullif`式の誤った結果を修正し`is-null` 。
    -   自動分析が時間範囲外でトリガーされる問題を修正します[＃23219](https://github.com/pingcap/tidb/pull/23219)
    -   `CAST`関数が`point get`プラン[＃23211](https://github.com/pingcap/tidb/pull/23211)のエラーを無視する可能性がある問題を修正します
    -   `CurrentDB`が空のときにSPMが有効にならないバグを修正します[＃23209](https://github.com/pingcap/tidb/pull/23209)
    -   IndexMergeプラン[＃23165](https://github.com/pingcap/tidb/pull/23165)で発生する可能性のある誤ったテーブルフィルターの問題を修正します
    -   `NULL`定数[＃23135](https://github.com/pingcap/tidb/pull/23135)の戻り型で予期しない`NotNullFlag`の問題を修正します
    -   照合順序がテキストタイプ[＃23092](https://github.com/pingcap/tidb/pull/23092)で処理されない可能性があるバグを修正します
    -   範囲パーティションが`IN`式[＃23074](https://github.com/pingcap/tidb/pull/23074)を誤って処理する可能性がある問題を修正します
    -   TiKVストアをトゥームストーンとしてマークした後、同じIPアドレスとポートを持つ異なるStoreIDで新しいTiKVストアを開始すると、 `StoreNotMatch`エラー[＃23071](https://github.com/pingcap/tidb/pull/23071)が返される問題を修正します。
    -   `NULL`で`YEAR`と比較した場合は`INT`タイプを調整しないで[＃22844](https://github.com/pingcap/tidb/pull/22844)
    -   `auto_random`列[＃22736](https://github.com/pingcap/tidb/pull/22736)のテーブルにデータをロードするときに接続が失われる問題を修正します
    -   キャンセルパス[＃23297](https://github.com/pingcap/tidb/pull/23297)でDDL操作がパニックに遭遇した場合のDDLハングオーバーの問題を修正します。
    -   `YEAR`列を[＃23104](https://github.com/pingcap/tidb/pull/23104)と比較するときのインデックススキャンの間違ったキー範囲を修正し`NULL`
    -   正常に作成されたビューが使用に失敗する問題を修正します[＃23083](https://github.com/pingcap/tidb/pull/23083)

-   TiKV

    -   `IN`式が符号なし/符号付き整数を適切に処理しない問題を修正します[＃9850](https://github.com/tikv/tikv/pull/9850)
    -   取り込み操作が再入可能ではないという問題を修正します[＃9779](https://github.com/tikv/tikv/pull/9779)
    -   TiKVコプロセッサー[＃9666](https://github.com/tikv/tikv/pull/9666)でJSONを文字列に変換するときにスペースが失われる問題を修正します

-   PD

    -   ストアにラベルがない場合に分離レベルが間違っているというバグを修正します[＃3474](https://github.com/pingcap/pd/pull/3474)

-   TiFlash

    -   `binary`タイプの列のデフォルト値に先頭または末尾のゼロバイトが含まれている場合の誤った実行結果の問題を修正します
    -   データベースの名前に特殊文字が含まれている場合、TiFlashがスキーマの同期に失敗するバグを修正します
    -   10進値で`IN`式を処理するときの誤った結果の問題を修正します
    -   Grafanaに表示される開いているファイル数のメトリックが高いバグを修正します
    -   TiFlashが`Timestamp`リテラルをサポートしないバグを修正します
    -   `FROM_UNIXTIME`の式を処理しているときに潜在的な応答しない問題を修正します
    -   文字列を整数としてキャストするときの誤った結果の問題を修正します
    -   `like`関数が間違った結果を返す可能性があるバグを修正します

-   ツール

    -   TiCDC

        -   `resolved ts`イベント[＃1464](https://github.com/pingcap/tiflow/pull/1464)の障害の問題を修正します
        -   ネットワークの問題による誤ったテーブルスケジューリングによって引き起こされるデータ損失の問題を修正します[＃1508](https://github.com/pingcap/tiflow/pull/1508)
        -   プロセッサが停止した後のリソースのタイムリーでないリリースのバグを修正します[＃1547](https://github.com/pingcap/tiflow/pull/1547)
        -   トランザクションカウンターが正しく更新されないバグを修正します。これにより、データベース接続のリークが発生する可能性があります[＃1524](https://github.com/pingcap/tiflow/pull/1524)
        -   PDにジッターがある場合に複数の所有者が共存できる問題を修正します。これにより、テーブルが欠落する可能性があります[＃1540](https://github.com/pingcap/tiflow/pull/1540)

    -   バックアップと復元（BR）

        -   ターゲットパスがバケット名[＃733](https://github.com/pingcap/br/pull/733)の場合、s3ストレージの`WalkDir`が`nil`を返すバグを修正します
        -   `status`ポートがTLS3で提供されないバグを修正し[＃839](https://github.com/pingcap/br/pull/839)

    -   TiDB Lightning

        -   TiKVImporterがファイルがすでに存在していることを無視する可能性があるエラーを修正します[＃848](https://github.com/pingcap/br/pull/848)
        -   TiDBLightningが間違ったタイムスタンプを使用して間違ったデータを読み取る可能性があるバグを修正します[＃850](https://github.com/pingcap/br/pull/850)
        -   TiDBLightningの予期しない終了によりチェックポイントファイルが破損する可能性があるバグを修正します[＃889](https://github.com/pingcap/br/pull/889)
        -   `cancel`エラーが無視されるために発生する可能性のあるデータエラーの問題を修正します[＃874](https://github.com/pingcap/br/pull/874)
