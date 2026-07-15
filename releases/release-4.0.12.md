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

    -   `batch cop`モードの`EXPLAIN`文の出力情報を絞り込む [＃23164](https://github.com/pingcap/tidb/pull/23164)
    -   `EXPLAIN`文の出力に、ストレージレイヤーにプッシュできない式の警告情報を追加します。 [＃23020](https://github.com/pingcap/tidb/pull/23020)
    -   DDLパッケージコードの一部を`Execute` `ExecRestricted`安全なAPIに移行する（2） [＃22935](https://github.com/pingcap/tidb/pull/22935)
    -   DDLパッケージコードの一部を`Execute` `ExecRestricted`安全なAPIに移行する（1） [＃22929](https://github.com/pingcap/tidb/pull/22929)
    -   `optimization-time`と`wait-TS-time`スローログに加える [＃22918](https://github.com/pingcap/tidb/pull/22918)
    -   `infoschema.partitions`テーブルから`partition_id`クエリをサポート [＃22489](https://github.com/pingcap/tidb/pull/22489)
    -   SQL文の実行プランがバインディングヒントと一致しているかどうかをユーザーが知ることができるように`last_plan_from_binding`追加します。 [＃21430](https://github.com/pingcap/tidb/pull/21430)
    -   `pre-split`オプションなしで切り捨てられたテーブルを散布する [＃22872](https://github.com/pingcap/tidb/pull/22872)
    -   `str_to_date`式に 3 つの書式指定子を追加します [＃22812](https://github.com/pingcap/tidb/pull/22812)
    -   メトリクスモニターで`PREPARE`実行失敗を`Failed Query OPM`として記録する [＃22672](https://github.com/pingcap/tidb/pull/22672)
    -   `tidb_snapshot` 設定されている場合、 `PREPARE`実行でエラーを報告しません [＃22641](https://github.com/pingcap/tidb/pull/22641)

-   TiKV

    -   短時間に大量の再接続を防ぐ[＃9879](https://github.com/tikv/tikv/pull/9879)
    -   多数のtombstoneのシナリオで書き込み操作とバッチ取得を最適化します[＃9729](https://github.com/tikv/tikv/pull/9729)
    -   リーダー移行の成功率を上げるために、デフォルト値の`leader-transfer-max-log-lag`を`128`に変更します[＃9605](https://github.com/tikv/tikv/pull/9605)

-   PD

    -   `pending-peers`または`down-peers`変更された場合にのみリージョンキャッシュを更新し、ハートビート更新する負荷を軽減します。 [＃3471](https://github.com/pingcap/pd/pull/3471)
    -   `split-cache`の領域がマージ対象にならないようにします。 [＃3459](https://github.com/pingcap/pd/pull/3459)

-   TiFlash

    -   設定ファイルを最適化し、不要な項目を削除します
    -   TiFlashバイナリファイルのサイズを縮小する
    -   適応型アグレッシブGC戦略を使用してメモリ使用量を削減する

-   ツール

    -   TiCDC

        -   ユーザーが現在のタイムスタンプ[＃1497](https://github.com/pingcap/tiflow/pull/1497) `start-ts`日前または`checkpoint-ts`日前に変更フィードを作成または再開するときに、二重の確認を追加します。
        -   古い値機能用の Grafana パネルを追加する [＃1571](https://github.com/pingcap/tiflow/pull/1571)

    -   Backup & Restore (BR)

        -   環境変数`HTTP_PROXY`と`HTTPS_PROXY`ログに記録する[＃827](https://github.com/pingcap/br/pull/827)
        -   テーブル数が多い場合のバックアップパフォーマンスの向上[＃745](https://github.com/pingcap/br/pull/745)
        -   サービスセーフポイントチェックが失敗した場合はエラーを報告する[＃826](https://github.com/pingcap/br/pull/826)
        -   `backupmeta` の`cluster_version`と`br_version`情報を加算します [＃803](https://github.com/pingcap/br/pull/803)
        -   バックアップの成功率を上げるために、外部ストレージエラーの再試行を追加します。 [＃851](https://github.com/pingcap/br/pull/851)
        -   バックアップ中のメモリ使用量を削減する[＃886](https://github.com/pingcap/br/pull/886)

    -   TiDB Lightning

        -   予期しないエラーを回避するために、 TiDB Lightningを実行する前に TiDB クラスターのバージョンを確認してください[＃787](https://github.com/pingcap/br/pull/787)
        -   TiDB Lightningが`cancel`エラーに遭遇したら、すぐに失敗しましょう [＃867](https://github.com/pingcap/br/pull/867)
        -   メモリ使用量とパフォーマンスのバランスをとるために、 `tikv-importer.engine-mem-cache-size`と`tikv-importer.local-writer-mem-cache-size`構成項目を追加します[＃866](https://github.com/pingcap/br/pull/866)
        -   インポート速度を上げるために、TiDB Lightningのローカルバックエンドで`batch split region`並列実行します[＃868](https://github.com/pingcap/br/pull/868)
        -   TiDB Lightningを使用してS3ストレージからデータをインポートする場合、 TiDB Lightningは`s3:ListBucket`権限必要としなくなりました。 [＃919](https://github.com/pingcap/br/pull/919)
        -   チェックポイントから再開する場合、 TiDB Lightningは元のエンジンを使用し続けます。 [＃924](https://github.com/pingcap/br/pull/924)

## バグ修正 {#bug-fixes}

-   TiDB

    -   セッション変数が16進リテラルの場合に`get`変数式がおかしくなる問題を修正[＃23372](https://github.com/pingcap/tidb/pull/23372)
    -   `Enum`または`Set`タイプの高速実行プランを作成するときに間違った照合順序が使用される問題を修正しました[＃23292](https://github.com/pingcap/tidb/pull/23292)
    -   `nullif`式を`is-null` と併用した場合に誤った結果になる可能性を修正しました [＃23279](https://github.com/pingcap/tidb/pull/23279)
    -   自動分析が時間範囲外で実行される問題を修正[＃23219](https://github.com/pingcap/tidb/pull/23219)
    -   `CAST`関数が`point get`プランのエラーを無視する可能性がある問題を修正しました [＃23211](https://github.com/pingcap/tidb/pull/23211)
    -   `CurrentDB`が空の場合に SPM が有効にならないバグを修正[＃23209](https://github.com/pingcap/tidb/pull/23209)
    -   IndexMerge プランでテーブル フィルターが間違っている可能性がある問題を修正しました [＃23165](https://github.com/pingcap/tidb/pull/23165)
    -   `NULL`定数の戻り値の型で予期しない`NotNullFlag`が発生する問題を修正 [＃23135](https://github.com/pingcap/tidb/pull/23135)
    -   テキストタイプで照合順序が処理されない可能性があるバグを修正 [＃23092](https://github.com/pingcap/tidb/pull/23092)
    -   範囲パーティションが`IN`式を誤って処理する可能性がある問題を修正しました [＃23074](https://github.com/pingcap/tidb/pull/23074)
    -   TiKVストアをtombstoneとしてマークした後、同じIPアドレスとポートで異なるStoreIDを持つ新しいTiKVストアを開始すると、 `StoreNotMatch`エラーが返され続ける問題を修正しました。 [＃23071](https://github.com/pingcap/tidb/pull/23071)
    -   `INT`型は`NULL`で`YEAR` を比較すると調整しない [＃22844](https://github.com/pingcap/tidb/pull/22844)
    -   `auto_random`列列のテーブルにデータをロードする際に接続が失われる問題を修正しました [＃22736](https://github.com/pingcap/tidb/pull/22736)
    -   DDL 操作がキャンセル パスでpanicに遭遇した場合の DDL ハングオーバーの問題を修正しました。 [＃23297](https://github.com/pingcap/tidb/pull/23297)
    -   `YEAR`列と`NULL` を比較する際のインデックススキャンのキー範囲の誤りを修正しました。 [＃23104](https://github.com/pingcap/tidb/pull/23104)
    -   正常に作成されたビューが使用できない問題を修正しました [＃23083](https://github.com/pingcap/tidb/pull/23083)

-   TiKV

    -   `IN`式が符号なし/符号付き整数を適切に処理しない問題を修正[＃9850](https://github.com/tikv/tikv/pull/9850)
    -   取り込み操作が再入可能ではない問題を修正[＃9779](https://github.com/tikv/tikv/pull/9779)
    -   TiKVコプロセッサでJSONを文字列に変換するときにスペースが失われる問題を修正 [＃9666](https://github.com/tikv/tikv/pull/9666)

-   PD

    -   ストアにラベルがない場合に分離レベルが間違っているというバグを修正しました [＃3474](https://github.com/pingcap/pd/pull/3474)

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

        -   `resolved ts`イベントの障害問題を修正 [＃1464](https://github.com/pingcap/tiflow/pull/1464)
        -   ネットワークの問題による誤ったテーブルスケジュールによって発生するデータ損失の問題を修正[＃1508](https://github.com/pingcap/tiflow/pull/1508)
        -   プロセッサが停止した後にリソースが不意に解放されるバグを修正[＃1547](https://github.com/pingcap/tiflow/pull/1547)
        -   トランザクションカウンタが正しく更新されず、データベース接続リークが発生する可能性があるバグを修正しました[＃1524](https://github.com/pingcap/tiflow/pull/1524)
        -   PD にジッターがある場合に複数の所有者が共存し、テーブルが失われる可能性がある問題を修正しました。 [＃1540](https://github.com/pingcap/tiflow/pull/1540)

    -   Backup & Restore (BR)

        -   ターゲットパスがバケット名の場合、S3ストレージの`WalkDir` `nil`返すバグを修正しました [＃733](https://github.com/pingcap/br/pull/733)
        -   `status`ポートがTLS で提供されないバグを修正 [＃839](https://github.com/pingcap/br/pull/839)

    -   TiDB Lightning

        -   TiKVインポーターがファイルが既に存在することを無視する可能性があるエラーを修正しました[＃848](https://github.com/pingcap/br/pull/848)
        -   TiDB Lightningが間違ったタイムスタンプを使用して間違ったデータを読み取る可能性があるバグを修正しました[＃850](https://github.com/pingcap/br/pull/850)
        -   TiDB Lightning の予期しない終了によりチェックポイントファイルが破損する可能性があるバグを修正しました。 [＃889](https://github.com/pingcap/br/pull/889)
        -   `cancel`エラーが無視されるために発生する可能性のあるデータエラーの問題を修正[＃874](https://github.com/pingcap/br/pull/874)
