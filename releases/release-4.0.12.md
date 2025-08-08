---
title: TiDB 4.0.12 Release Notes
summary: TiDB 4.0.12は2021年4月2日にリリースされました。新機能には、オンラインローリングアップデート用の「tiflashレプリカ」の状態を確認するツールが含まれています。TiDB、TiKV、PD、 TiFlash、および各種ツールの機能強化に加え、TiDB、TiKV、PD、 TiFlash、TiCDC、バックアップ＆リストア、 TiDB Lightningのバグ修正も実装されました。
---

# TiDB 4.0.12 リリースノート {#tidb-4-0-12-release-notes}

発売日：2021年4月2日

TiDB バージョン: 4.0.12

## 新機能 {#new-features}

-   TiFlash

    -   オンラインローリングアップデートの`tiflash replica`のステータスを確認するツールを追加します

## 改善点 {#improvements}

-   TiDB

    -   `batch cop`モード[＃23164](https://github.com/pingcap/tidb/pull/23164)の`EXPLAIN`文の出力情報を絞り込む
    -   `EXPLAIN`文[＃23020](https://github.com/pingcap/tidb/pull/23020)の出力に、storageレイヤーにプッシュできない式の警告情報を追加します。
    -   DDLパッケージコードの一部を`Execute` `ExecRestricted`安全なAPIに移行する（2） [＃22935](https://github.com/pingcap/tidb/pull/22935)
    -   DDLパッケージコードの一部を`Execute` `ExecRestricted`安全なAPIに移行する（1） [＃22929](https://github.com/pingcap/tidb/pull/22929)
    -   `optimization-time`と`wait-TS-time`スローログ[＃22918](https://github.com/pingcap/tidb/pull/22918)に加える
    -   `infoschema.partitions`テーブル[＃22489](https://github.com/pingcap/tidb/pull/22489)から`partition_id`クエリをサポート
    -   SQL文の実行プランがバインディング[＃21430](https://github.com/pingcap/tidb/pull/21430)ヒントと一致しているかどうかをユーザーが知ることができるように`last_plan_from_binding`追加します。
    -   `pre-split`オプション[＃22872](https://github.com/pingcap/tidb/pull/22872)なしで切り捨てられたテーブルを散布する
    -   `str_to_date`式[＃22812](https://github.com/pingcap/tidb/pull/22812)に 3 つの書式指定子を追加します
    -   メトリクスモニター[＃22672](https://github.com/pingcap/tidb/pull/22672)で`PREPARE`実行失敗を`Failed Query OPM`として記録する
    -   `tidb_snapshot` [＃22641](https://github.com/pingcap/tidb/pull/22641)設定されている場合、 `PREPARE`実行でエラーを報告しません

-   TiKV

    -   短時間に大量の再接続を防ぐ[＃9879](https://github.com/tikv/tikv/pull/9879)
    -   多数の墓石のシナリオで書き込み操作とバッチ取得を最適化します[＃9729](https://github.com/tikv/tikv/pull/9729)
    -   リーダー移行の成功率を上げるために、デフォルト値の`leader-transfer-max-log-lag`を`128`に変更します[＃9605](https://github.com/tikv/tikv/pull/9605)

-   PD

    -   `pending-peers`または`down-peers`変更された場合にのみリージョンキャッシュを更新し、ハートビート[＃3471](https://github.com/pingcap/pd/pull/3471)更新する負荷を軽減します。
    -   `split-cache`の領域がマージ[＃3459](https://github.com/pingcap/pd/pull/3459)対象にならないようにします。

-   TiFlash

    -   設定ファイルを最適化し、不要な項目を削除します
    -   TiFlashバイナリファイルのサイズを縮小する
    -   適応型アグレッシブGC戦略を使用してメモリ使用量を削減する

-   ツール

    -   TiCDC

        -   ユーザーが現在のタイムスタンプ[＃1497](https://github.com/pingcap/tiflow/pull/1497) `start-ts`日前または`checkpoint-ts`日前に変更フィードを作成または再開するときに、二重の確認を追加します。
        -   古い値機能[＃1571](https://github.com/pingcap/tiflow/pull/1571)用の Grafana パネルを追加する

    -   バックアップと復元 (BR)

        -   環境変数`HTTP_PROXY`と`HTTPS_PROXY`ログに記録する[＃827](https://github.com/pingcap/br/pull/827)
        -   テーブル数が多い場合のバックアップパフォーマンスの向上[＃745](https://github.com/pingcap/br/pull/745)
        -   サービスセーフポイントチェックが失敗した場合はエラーを報告する[＃826](https://github.com/pingcap/br/pull/826)
        -   `backupmeta` [＃803](https://github.com/pingcap/br/pull/803)の`cluster_version`と`br_version`情報を加算します
        -   バックアップ[＃851](https://github.com/pingcap/br/pull/851)の成功率を上げるために、外部storageエラーの再試行を追加します。
        -   バックアップ中のメモリ使用量を削減する[＃886](https://github.com/pingcap/br/pull/886)

    -   TiDB Lightning

        -   予期しないエラーを回避するために、 TiDB Lightningを実行する前に TiDB クラスターのバージョンを確認してください[＃787](https://github.com/pingcap/br/pull/787)
        -   TiDB Lightningが`cancel`エラー[＃867](https://github.com/pingcap/br/pull/867)に遭遇したら、すぐに失敗しましょう
        -   メモリ使用量とパフォーマンスのバランスをとるために、 `tikv-importer.engine-mem-cache-size`と`tikv-importer.local-writer-mem-cache-size`構成項目を追加します[＃866](https://github.com/pingcap/br/pull/866)
        -   インポート速度を上げるために、TiDB Lightningのローカルバックエンドで`batch split region`並列実行します[＃868](https://github.com/pingcap/br/pull/868)
        -   TiDB Lightningを使用してS3storageからデータをインポートする場合、 TiDB Lightningは`s3:ListBucket`権限[＃919](https://github.com/pingcap/br/pull/919)必要としなくなりました。
        -   チェックポイントから再開する場合、 TiDB Lightningは元のエンジン[＃924](https://github.com/pingcap/br/pull/924)を使用し続けます。

## バグ修正 {#bug-fixes}

-   TiDB

    -   セッション変数が16進リテラルの場合に`get`変数式がおかしくなる問題を修正[＃23372](https://github.com/pingcap/tidb/pull/23372)
    -   `Enum`または`Set`タイプの高速実行プランを作成するときに間違った照合順序が使用される問題を修正しました[＃23292](https://github.com/pingcap/tidb/pull/23292)
    -   `nullif`式を`is-null` [＃23279](https://github.com/pingcap/tidb/pull/23279)と併用した場合に誤った結果になる可能性を修正しました
    -   自動分析が時間範囲外で実行される問題を修正[＃23219](https://github.com/pingcap/tidb/pull/23219)
    -   `CAST`関数が`point get`プラン[＃23211](https://github.com/pingcap/tidb/pull/23211)のエラーを無視する可能性がある問題を修正しました
    -   `CurrentDB`が空の場合に SPM が有効にならないバグを修正[＃23209](https://github.com/pingcap/tidb/pull/23209)
    -   IndexMerge プラン[＃23165](https://github.com/pingcap/tidb/pull/23165)でテーブル フィルターが間違っている可能性がある問題を修正しました
    -   `NULL`定数[＃23135](https://github.com/pingcap/tidb/pull/23135)の戻り値の型で予期しない`NotNullFlag`が発生する問題を修正
    -   テキストタイプ[＃23092](https://github.com/pingcap/tidb/pull/23092)で照合順序が処理されない可能性があるバグを修正
    -   範囲パーティションが`IN`式[＃23074](https://github.com/pingcap/tidb/pull/23074)を誤って処理する可能性がある問題を修正しました
    -   TiKVストアをトゥームストーンとしてマークした後、同じIPアドレスとポートで異なるStoreIDを持つ新しいTiKVストアを開始すると、 `StoreNotMatch`エラー[＃23071](https://github.com/pingcap/tidb/pull/23071)が返され続ける問題を修正しました。
    -   `INT`型は`NULL`で`YEAR` [＃22844](https://github.com/pingcap/tidb/pull/22844)を比較すると調整しない
    -   `auto_random`列[＃22736](https://github.com/pingcap/tidb/pull/22736)列のテーブルにデータをロードする際に接続が失われる問題を修正しました
    -   DDL 操作がキャンセル パス[＃23297](https://github.com/pingcap/tidb/pull/23297)でpanicに遭遇した場合の DDL ハングオーバーの問題を修正しました。
    -   `YEAR`列目と`NULL` [＃23104](https://github.com/pingcap/tidb/pull/23104)を比較する際のインデックススキャンのキー範囲の誤りを修正しました。
    -   正常に作成されたビューが[＃23083](https://github.com/pingcap/tidb/pull/23083)使用できない問題を修正しました

-   TiKV

    -   `IN`式が符号なし/符号付き整数を適切に処理しない問題を修正[＃9850](https://github.com/tikv/tikv/pull/9850)
    -   取り込み操作が再入可能ではない問題を修正[＃9779](https://github.com/tikv/tikv/pull/9779)
    -   TiKVコプロセッサ[＃9666](https://github.com/tikv/tikv/pull/9666)でJSONを文字列に変換するときにスペースが失われる問題を修正

-   PD

    -   ストアにラベル[＃3474](https://github.com/pingcap/pd/pull/3474)がない場合に分離レベルが間違っているというバグを修正しました

-   TiFlash

    -   `binary`型列のデフォルト値に先頭または末尾にゼロバイトが含まれている場合に、実行結果が不正確になる問題を修正しました。
    -   データベース名に特殊文字が含まれている場合にTiFlashがスキーマの同期に失敗するバグを修正しました
    -   小数値を含む`IN`式を処理するときに誤った結果が発生する問題を修正しました
    -   Grafana に表示される開かれたファイル数のメトリックが高くなるバグを修正しました
    -   TiFlashが`Timestamp`リテラルをサポートしないバグを修正
    -   `FROM_UNIXTIME`式を処理中に応答しない可能性がある問題を修正しました
    -   文字列を整数としてキャストしたときに誤った結果が出る問題を修正しました
    -   `like`関数が間違った結果を返す可能性があるバグを修正しました

-   ツール

    -   TiCDC

        -   `resolved ts`イベント[＃1464](https://github.com/pingcap/tiflow/pull/1464)の障害問題を修正
        -   ネットワークの問題による誤ったテーブルスケジュールによって発生するデータ損失の問題を修正[＃1508](https://github.com/pingcap/tiflow/pull/1508)
        -   プロセッサが停止した後にリソースが不意に解放されるバグを修正[＃1547](https://github.com/pingcap/tiflow/pull/1547)
        -   トランザクションカウンタが正しく更新されず、データベース接続リークが発生する可能性があるバグを修正しました[＃1524](https://github.com/pingcap/tiflow/pull/1524)
        -   PD にジッターがある場合に複数の所有者が共存し、テーブルが[＃1540](https://github.com/pingcap/tiflow/pull/1540)失われる可能性がある問題を修正しました。

    -   バックアップと復元 (BR)

        -   ターゲットパスがバケット名[＃733](https://github.com/pingcap/br/pull/733)の場合、S3storageの`WalkDir` `nil`返すバグを修正しました
        -   `status`ポートがTLS [＃839](https://github.com/pingcap/br/pull/839)で提供されないバグを修正

    -   TiDB Lightning

        -   TiKVインポーターがファイルが既に存在することを無視する可能性があるエラーを修正しました[＃848](https://github.com/pingcap/br/pull/848)
        -   TiDB Lightningが間違ったタイムスタンプを使用して間違ったデータを読み取る可能性があるバグを修正しました[＃850](https://github.com/pingcap/br/pull/850)
        -   TiDB Lightning の予期しない終了によりチェックポイントファイル[＃889](https://github.com/pingcap/br/pull/889)が破損する可能性があるバグを修正しました。
        -   `cancel`エラーが無視されるために発生する可能性のあるデータエラーの問題を修正[＃874](https://github.com/pingcap/br/pull/874)
