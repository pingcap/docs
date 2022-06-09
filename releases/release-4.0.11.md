---
title: TiDB 4.0.11 Release Notes
---

# TiDB4.0.11リリースノート {#tidb-4-0-11-release-notes}

発売日：2021年2月26日

TiDBバージョン：4.0.11

## 新機能 {#new-features}

-   TiDB

    -   `utf8_unicode_ci`と`utf8mb4_unicode_ci`の照合をサポートする[＃22558](https://github.com/pingcap/tidb/pull/22558)

-   TiKV

    -   `utf8mb4_unicode_ci`の照合順序をサポートする[＃9577](https://github.com/tikv/tikv/pull/9577)
    -   `cast_year_as_time`の照合順序をサポートする[＃9299](https://github.com/tikv/tikv/pull/9299)

-   TiFlash

    -   コプロセッサースレッドプールを追加して、実行のためのコプロセッサー要求をキューに入れます。これにより、場合によってはメモリー不足（OOM）が回避され、デフォルト値`NumOfPhysicalCores * 2`で`cop_pool_size`および`batch_cop_pool_size`構成項目が追加されます。

## 改善 {#improvements}

-   TiDB

    -   外部結合から簡略化された内部結合を並べ替える[＃22402](https://github.com/pingcap/tidb/pull/22402)
    -   Grafanaダッシュボードで複数のクラスターをサポートする[＃22534](https://github.com/pingcap/tidb/pull/22534)
    -   複数のステートメントの問題の回避策を追加する[＃22468](https://github.com/pingcap/tidb/pull/22468)
    -   遅いクエリのメトリックを`internal`と[＃22405](https://github.com/pingcap/tidb/pull/22405)に分割し`general`
    -   `utf8_unicode_ci`と`utf8mb4_unicode_ci`の照合用のインターフェースを追加する[＃22099](https://github.com/pingcap/tidb/pull/22099)

-   TiKV

    -   DBaaS1のサーバー情報のメトリックを追加し[＃9591](https://github.com/tikv/tikv/pull/9591)
    -   Grafanaダッシュボードで複数のクラスターをサポートする[＃9572](https://github.com/tikv/tikv/pull/9572)
    -   RocksDBメトリックを[＃9316](https://github.com/tikv/tikv/pull/9316)に報告する
    -   コプロセッサー・タスクの中断時間を記録する[＃9277](https://github.com/tikv/tikv/pull/9277)
    -   Load BaseSplit1のキーカウントとキーサイズのしきい値を追加し[＃9354](https://github.com/tikv/tikv/pull/9354)
    -   データをインポートする前にファイルが存在するかどうかを確認してください[＃9544](https://github.com/tikv/tikv/pull/9544)
    -   FastTuneパネルを改善する[＃9180](https://github.com/tikv/tikv/pull/9180)

-   PD

    -   Grafanaダッシュボードで複数のクラスターをサポートする[＃3398](https://github.com/pingcap/pd/pull/3398)

-   TiFlash

    -   `date_format`の機能のパフォーマンスを最適化する
    -   取り込みSSTの処理のメモリ消費を最適化する
    -   リージョンエラーの可能性を減らすために、バッチコプロセッサーの再試行ロジックを最適化します

-   ツール

    -   TiCDC

        -   `capture`メタデータにバージョン情報を追加し、 `changefeed`メタデータに`changefeed`のCLIバージョンを追加します[＃1342](https://github.com/pingcap/tiflow/pull/1342)

    -   TiDB Lightning

        -   インポートパフォーマンスを向上させるためにテーブルを並列に作成する[＃502](https://github.com/pingcap/tidb-lightning/pull/502)
        -   エンジンの合計サイズがリージョンサイズ[＃524](https://github.com/pingcap/tidb-lightning/pull/524)より小さい場合は、リージョンの分割をスキップしてインポートパフォーマンスを向上させます
        -   インポートの進行状況バーを追加し、復元の進行状況の精度を最適化します[＃506](https://github.com/pingcap/tidb-lightning/pull/506)

## バグの修正 {#bug-fixes}

-   TiDB

    -   異常な`unicode_ci`定数伝播[＃22614](https://github.com/pingcap/tidb/pull/22614)の問題を修正します
    -   間違った照合順序と強制性を引き起こす可能性のある問題を修正します[＃22602](https://github.com/pingcap/tidb/pull/22602)
    -   間違った照合順序結果を引き起こす可能性のある問題を修正します[＃22599](https://github.com/pingcap/tidb/pull/22599)
    -   さまざまな照合の定数置換の問題を修正します[＃22582](https://github.com/pingcap/tidb/pull/22582)
    -   照合順序[＃22531](https://github.com/pingcap/tidb/pull/22531)を使用すると、 `like`関数が間違った結果を返す可能性があるバグを修正します。
    -   `least`および`greatest`関数での誤った`duration`型推論の問題を修正します[＃22580](https://github.com/pingcap/tidb/pull/22580)
    -   `like`関数が単一文字のワイルドカード（ `_` ）とそれに続く複数文字のワイルドカード（ `%` ）を処理するときに発生するバグを修正します[＃22575](https://github.com/pingcap/tidb/pull/22575)
    -   TiDBの組み込み関数（ `least`および`greatest` ）の型推論エラーを修正します[＃22562](https://github.com/pingcap/tidb/pull/22562)
    -   パターン文字列がUnicode文字列[＃22529](https://github.com/pingcap/tidb/pull/22529)の場合、 `like`関数が間違った結果を取得するバグを修正します。
    -   `@@tidb_snapshot`変数が[＃22527](https://github.com/pingcap/tidb/pull/22527)に設定されている場合、ポイント取得クエリがスナップショットデータを取得しないバグを修正します。
    -   結合からヒントを生成するときに発生する可能性のあるパニックを修正する[＃22518](https://github.com/pingcap/tidb/pull/22518)
    -   文字列が誤って`BIT`タイプ[＃22420](https://github.com/pingcap/tidb/pull/22420)に変換される問題を修正します
    -   `tidb_rowid`列に値を挿入するときに発生する`index out of range`エラーを修正します[＃22359](https://github.com/pingcap/tidb/pull/22359)
    -   キャッシュされたプランが誤って使用されるバグを修正します[＃22353](https://github.com/pingcap/tidb/pull/22353)
    -   バイナリ/文字列の長さが長すぎる場合の`WEIGHT_STRING`関数の実行時のパニックを修正します[＃22332](https://github.com/pingcap/tidb/pull/22332)
    -   関数パラメーターの数が無効な場合に生成された列の使用を禁止する[＃22174](https://github.com/pingcap/tidb/pull/22174)
    -   実行計画を作成する前に、プロセス情報を正しく設定する[＃22148](https://github.com/pingcap/tidb/pull/22148)
    -   [＃22136](https://github.com/pingcap/tidb/pull/22136)の不正確な実行時統計の問題を修正し`IndexLookUp`
    -   クラスタがコンテナにデプロイされている場合のメモリ使用量情報のキャッシュを追加する[＃22116](https://github.com/pingcap/tidb/pull/22116)
    -   デコードプランエラーの問題を修正します[＃22022](https://github.com/pingcap/tidb/pull/22022)
    -   無効なウィンドウ仕様を使用した場合のエラーを報告する[＃21976](https://github.com/pingcap/tidb/pull/21976)
    -   `PREPARE` [＃21972](https://github.com/pingcap/tidb/pull/21972)が`EXECUTE` 、または`DEALLOCATE`で`PREPARE`されている場合にエラーを報告する
    -   存在しないパーティション[＃21971](https://github.com/pingcap/tidb/pull/21971)で`INSERT IGNORE`ステートメントが使用されたときにエラーが報告されない問題を修正します。
    -   `EXPLAIN`の結果のエンコーディングを統一し、ログ[＃21964](https://github.com/pingcap/tidb/pull/21964)を遅くします
    -   集計演算子[＃21957](https://github.com/pingcap/tidb/pull/21957)を使用する場合の結合での不明な列の問題を修正します
    -   `ceiling`関数[＃21936](https://github.com/pingcap/tidb/pull/21936)の間違った型推論を修正します
    -   `Double`タイプの列が10進数の[＃21916](https://github.com/pingcap/tidb/pull/21916)を無視する問題を修正します
    -   相関集計がサブクエリ[＃21877](https://github.com/pingcap/tidb/pull/21877)で計算される問題を修正します
    -   キーの長さが65536以上のJSONオブジェクトのエラーを報告する[＃21870](https://github.com/pingcap/tidb/pull/21870)
    -   `dyname`関数がMySQL3と互換性がないという問題を修正し[＃21850](https://github.com/pingcap/tidb/pull/21850)
    -   入力データが長すぎる場合に`to_base64`関数が`NULL`を返す問題を修正します[＃21813](https://github.com/pingcap/tidb/pull/21813)
    -   サブクエリ[＃21808](https://github.com/pingcap/tidb/pull/21808)の複数のフィールドを比較できない問題を修正しました
    -   JSON1でfloat型を比較するときに発生する問題を修正し[＃21785](https://github.com/pingcap/tidb/pull/21785)
    -   JSONオブジェクトのタイプを比較するときに発生する問題を修正します[＃21718](https://github.com/pingcap/tidb/pull/21718)
    -   `cast`関数の強制力の値が誤って設定されている問題を修正します[＃21714](https://github.com/pingcap/tidb/pull/21714)
    -   `IF`関数[＃21711](https://github.com/pingcap/tidb/pull/21711)を使用するときの予期しないパニックを修正します
    -   JSON検索から返される`NULL`の結果がMySQL3と互換性がないという問題を修正し[＃21700](https://github.com/pingcap/tidb/pull/21700)
    -   `ORDER BY`と[＃21697](https://github.com/pingcap/tidb/pull/21697)を使用して`only_full_group_by`モードをチェックするときに発生する問題を修正し`HAVING`
    -   `Day`と`Time`のユニットが[＃21676](https://github.com/pingcap/tidb/pull/21676)と互換性がないという問題を修正します
    -   デフォルト値の`LEAD`と`LAG`がフィールドタイプ[＃21665](https://github.com/pingcap/tidb/pull/21665)に適応できない問題を修正します。
    -   チェックを実行して、 `LOAD DATA`ステートメントがデータをベーステーブル[＃21638](https://github.com/pingcap/tidb/pull/21638)にのみロードできることを確認します。
    -   `addtime`と`subtime`の関数が無効な引数を処理するときに発生する問題を修正します[＃21635](https://github.com/pingcap/tidb/pull/21635)
    -   概算値の丸め規則を「最も近い偶数に丸める」に変更します[＃21628](https://github.com/pingcap/tidb/pull/21628)
    -   明示的に読み取られるまで`WEEK()`が`@@GLOBAL.default_week_format`を認識しないという問題を修正します[＃21623](https://github.com/pingcap/tidb/pull/21623)

-   TiKV

    -   TiKVが[＃9604](https://github.com/tikv/tikv/pull/9604)でビルドに失敗する問題を修正し`PROST=1`
    -   一致しないメモリ診断を修正する[＃9589](https://github.com/tikv/tikv/pull/9589)
    -   部分的なRawKV復元範囲のエンドキーが包括的であるという問題を修正します[＃9583](https://github.com/tikv/tikv/pull/9583)
    -   TiCDCのインクリメンタルスキャン中にロールバックされたトランザクションのキーの古い値をロードするときに発生するTiKVパニックの問題を修正します[＃9569](https://github.com/tikv/tikv/pull/9569)
    -   異なる設定のチェンジフィードが1つのリージョン[＃9565](https://github.com/tikv/tikv/pull/9565)に接続するときの古い値の構成グリッチを修正します
    -   MACアドレスがないネットワークインターフェイスを備えたマシンでTiKVクラスタを実行するときに発生するクラッシュの問題を修正します（v4.0.9で導入） [＃9516](https://github.com/tikv/tikv/pull/9516)
    -   巨大なリージョン[＃9448](https://github.com/tikv/tikv/pull/9448)をバックアップするときのTiKVOOMの問題を修正します
    -   `region-split-check-diff`はカスタマイズできないという問題を修正します[＃9530](https://github.com/tikv/tikv/pull/9530)
    -   システム時刻が戻ったときのTiKVパニックの問題を修正します[＃9542](https://github.com/tikv/tikv/pull/9542)

-   PD

    -   メンバーのヘルスメトリックが正しく表示されない問題を修正します[＃3368](https://github.com/pingcap/pd/pull/3368)
    -   まだピアがいるトゥームストーンストアの削除を禁止する[＃3352](https://github.com/pingcap/pd/pull/3352)
    -   ストア制限を維持できない問題を修正します[＃3403](https://github.com/pingcap/pd/pull/3403)
    -   スキャッターレンジスケジューラの制限制限を修正[＃3401](https://github.com/pingcap/pd/pull/3401)

-   TiFlash

    -   `min`の結果が10進`max`で間違っているバグを修正します
    -   データの読み取り時にTiFlashがクラッシュする可能性があるバグを修正
    -   DDL操作後に書き込まれた一部のデータがデータ圧縮後に失われる可能性がある問題を修正します
    -   TiFlashがコプロセッサーで10進定数を誤って処理する問題を修正します
    -   学習者の読み取りプロセス中に発生する可能性のあるクラッシュを修正
    -   TiDBとTiFlashの間で`0`または`NULL`で除算する際の一貫性のない動作を修正します

-   ツール

    -   TiCDC

        -   `ErrTaskStatusNotExists`と`capture`のセッションの終了が同時に発生したときにTiCDCサービスが予期せず終了する可能性があるバグを修正します[＃1240](https://github.com/pingcap/tiflow/pull/1240)
        -   `changefeed`が別の[＃1347](https://github.com/pingcap/tiflow/pull/1347)の影響を受ける可能性があるという古い値スイッチの問題を修正し`changefeed`
        -   無効な`sort-engine`パラメータ[＃1309](https://github.com/pingcap/tiflow/pull/1309)を使用して新しい`changefeed`を処理するときにTiCDCサービスがハングする可能性があるバグを修正します。
        -   非所有者ノードでデバッグ情報を取得するときに発生するパニックの問題を修正します[＃1349](https://github.com/pingcap/tiflow/pull/1349)
        -   テーブルを追加または削除するときに`ticdc_processor_num_of_tables`と`ticdc_processor_table_resolved_ts`のメトリックが適切に更新されない問題を修正します[＃1351](https://github.com/pingcap/tiflow/pull/1351)
        -   テーブルの追加時にプロセッサがクラッシュした場合の潜在的なデータ損失の問題を修正します[＃1363](https://github.com/pingcap/tiflow/pull/1363)
        -   テーブルの移行中に所有者が異常なTiCDCサーバーの終了につながる可能性があるバグを修正します[＃1352](https://github.com/pingcap/tiflow/pull/1352)
        -   サービスGCセーフポイントが失われた後、TiCDCが時間内に終了しないバグを修正します[＃1367](https://github.com/pingcap/tiflow/pull/1367)
        -   KVクライアントがイベントフィードの作成をスキップする可能性があるバグを修正します[＃1336](https://github.com/pingcap/tiflow/pull/1336)
        -   トランザクションがダウンストリームに複製されるときにトランザクションのアトミック性が壊れるバグを修正します[＃1375](https://github.com/pingcap/tiflow/pull/1375)

    -   バックアップと復元（BR）

        -   BRがバックアップを復元した後にTiKVが大きなリージョンを生成する可能性があるという問題を修正します[＃702](https://github.com/pingcap/br/pull/702)
        -   テーブルに自動[＃720](https://github.com/pingcap/br/pull/720)がない場合でも、BRがテーブルの自動IDを復元する問題を修正します。

    -   TiDB Lightning

        -   TiDBバックエンド[＃535](https://github.com/pingcap/tidb-lightning/pull/535)の使用時に`column count mismatch`がトリガーされる可能性があるバグを修正します
        -   ソースファイルの列数とターゲットテーブルの列数が一致しない場合にTiDBバックエンドがパニックになるバグを修正します[＃528](https://github.com/pingcap/tidb-lightning/pull/528)
        -   TiDBLightningのデータインポート中にTiKVが予期せずパニックになる可能性があるバグを修正します[＃554](https://github.com/pingcap/tidb-lightning/pull/554)
