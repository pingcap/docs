---
title: TiDB 4.0.11 Release Notes
---

# TiDB 4.0.11 リリースノート {#tidb-4-0-11-release-notes}

発売日：2021年2月26日

TiDB バージョン: 4.0.11

## 新機能 {#new-features}

-   TiDB

    -   `utf8_unicode_ci`および`utf8mb4_unicode_ci`照合をサポート[#22558](https://github.com/pingcap/tidb/pull/22558)

-   TiKV

    -   `utf8mb4_unicode_ci`照合順序[#9577](https://github.com/tikv/tikv/pull/9577)をサポート
    -   `cast_year_as_time`照合順序[#9299](https://github.com/tikv/tikv/pull/9299)をサポート

-   TiFlash

    -   コプロセッサー・スレッド・プールを追加して、実行のためにコプロセッサー要求をキューに入れ、場合によってはメモリ不足 (OOM) を回避し、 `cop_pool_size`と`batch_cop_pool_size`構成項目をデフォルト値の`NumOfPhysicalCores * 2`で追加します。

## 改良点 {#improvements}

-   TiDB

    -   外部結合から単純化された内部結合を並べ替える[#22402](https://github.com/pingcap/tidb/pull/22402)
    -   Grafana ダッシュボードで複数のクラスターをサポートする[#22534](https://github.com/pingcap/tidb/pull/22534)
    -   複数のステートメントの問題に対する回避策を追加します[#22468](https://github.com/pingcap/tidb/pull/22468)
    -   スロークエリのメトリクスを`internal`と`general` [#22405](https://github.com/pingcap/tidb/pull/22405)に分ける
    -   `utf8_unicode_ci`および`utf8mb4_unicode_ci`照合用のインターフェイスを追加します[#22099](https://github.com/pingcap/tidb/pull/22099)

-   TiKV

    -   DBaaS [#9591](https://github.com/tikv/tikv/pull/9591)のサーバー情報のメトリクスを追加
    -   Grafana ダッシュボードで複数のクラスターをサポートする[#9572](https://github.com/tikv/tikv/pull/9572)
    -   RocksDB メトリクスを TiDB [#9316](https://github.com/tikv/tikv/pull/9316)に報告する
    -   コプロセッサー・タスクの中断時間を記録します[#9277](https://github.com/tikv/tikv/pull/9277)
    -   Load Base Split [#9354](https://github.com/tikv/tikv/pull/9354)のキー数とキー サイズのしきい値を追加します。
    -   データのインポート前にファイルが存在するかどうかを確認する[#9544](https://github.com/tikv/tikv/pull/9544)
    -   Fast Tune パネルの改善[#9180](https://github.com/tikv/tikv/pull/9180)

-   PD

    -   Grafana ダッシュボードで複数のクラスターをサポートする[#3398](https://github.com/pingcap/pd/pull/3398)

-   TiFlash

    -   `date_format`関数のパフォーマンスを最適化する
    -   取り込み SST 処理のメモリ消費を最適化する
    -   Batch コプロセッサーの再試行ロジックを最適化して、リージョンエラーの可能性を減らします

-   ツール

    -   TiCDC

        -   `capture`メタデータにバージョン情報を追加し、 `changefeed`メタデータ[#1342](https://github.com/pingcap/tiflow/pull/1342)に`changefeed`の CLI バージョンを追加します。

    -   TiDB Lightning

        -   インポートのパフォーマンスを向上させるためにテーブルを並行して作成する[#502](https://github.com/pingcap/tidb-lightning/pull/502)
        -   エンジンの合計サイズがリージョンサイズ[#524](https://github.com/pingcap/tidb-lightning/pull/524)より小さい場合、リージョンの分割をスキップしてインポートのパフォーマンスを向上させます
        -   インポート進行状況バーを追加し、復元進行状況の精度を最適化します[#506](https://github.com/pingcap/tidb-lightning/pull/506)

## バグの修正 {#bug-fixes}

-   TiDB

    -   異常な`unicode_ci`定数伝播の問題を修正[#22614](https://github.com/pingcap/tidb/pull/22614)
    -   間違った照合順序と強制性を引き起こす可能性がある問題を修正します[#22602](https://github.com/pingcap/tidb/pull/22602)
    -   間違った照合順序結果を引き起こす可能性がある問題を修正します[#22599](https://github.com/pingcap/tidb/pull/22599)
    -   異なる照合の定数置換の問題を修正します[#22582](https://github.com/pingcap/tidb/pull/22582)
    -   照合順序[#22531](https://github.com/pingcap/tidb/pull/22531)を使用すると`like`関数が間違った結果を返すことがあるというバグを修正
    -   `least`と`greatest`関数で間違った`duration`型の推論の問題を修正します[#22580](https://github.com/pingcap/tidb/pull/22580)
    -   `like`関数が単一文字のワイルドカード ( `_` ) の後に複数文字のワイルドカード ( `%` ) を処理するときに発生するバグを修正します[#22575](https://github.com/pingcap/tidb/pull/22575)
    -   TiDB の組み込み関数の型推論エラーを修正 ( `least`および`greatest` ) [#22562](https://github.com/pingcap/tidb/pull/22562)
    -   パターン文字列が Unicode 文字列の場合に`like`関数が間違った結果を取得するバグを修正します[#22529](https://github.com/pingcap/tidb/pull/22529)
    -   ポイント取得クエリで、 `@@tidb_snapshot`変数を[#22527](https://github.com/pingcap/tidb/pull/22527)に設定するとスナップショットデータが取得されない不具合を修正
    -   結合からヒントを生成するときに発生する可能性のあるpanicを修正します[#22518](https://github.com/pingcap/tidb/pull/22518)
    -   文字列が誤って`BIT`タイプ[#22420](https://github.com/pingcap/tidb/pull/22420)に変換される問題を修正
    -   `tidb_rowid`列[#22359](https://github.com/pingcap/tidb/pull/22359)に値を挿入するときに発生する`index out of range`エラーを修正します。
    -   キャッシュされたプランが誤って使用されるバグを修正[#22353](https://github.com/pingcap/tidb/pull/22353)
    -   バイナリ/文字列の長さが長すぎる場合の`WEIGHT_STRING`関数の実行時panicを修正します[#22332](https://github.com/pingcap/tidb/pull/22332)
    -   関数パラメータの数が無効な場合、生成された列の使用を禁止する[#22174](https://github.com/pingcap/tidb/pull/22174)
    -   実行計画を立てる前にプロセス情報を正しく設定する[#22148](https://github.com/pingcap/tidb/pull/22148)
    -   `IndexLookUp` [#22136](https://github.com/pingcap/tidb/pull/22136)の不正確なランタイム統計の問題を修正
    -   クラスターがコンテナーにデプロイされている場合のメモリ使用量情報のキャッシュを追加します[#22116](https://github.com/pingcap/tidb/pull/22116)
    -   デコード プラン エラーの問題を修正します[#22022](https://github.com/pingcap/tidb/pull/22022)
    -   無効なウィンドウ仕様の使用に関するエラーを報告する[#21976](https://github.com/pingcap/tidb/pull/21976)
    -   `PREPARE`ステートメントが`EXECUTE` 、 `DEALLOCATE`または`PREPARE`でネストされている場合にエラーを報告する[#21972](https://github.com/pingcap/tidb/pull/21972)
    -   存在しないパーティションで`INSERT IGNORE`ステートメントを使用するとエラーが報告されない問題を修正します[#21971](https://github.com/pingcap/tidb/pull/21971)
    -   `EXPLAIN`結果とスローログ[#21964](https://github.com/pingcap/tidb/pull/21964)のエンコーディングを統一する
    -   集計演算子[#21957](https://github.com/pingcap/tidb/pull/21957)を使用する場合の結合での不明な列の問題を修正します。
    -   `ceiling`関数[#21936](https://github.com/pingcap/tidb/pull/21936)の間違った型推論を修正
    -   `Double`型の列が 10 進数の[#21916](https://github.com/pingcap/tidb/pull/21916)を無視する問題を修正
    -   サブクエリ[#21877](https://github.com/pingcap/tidb/pull/21877)で相関集計が計算される問題を修正します。
    -   キーの長さ &gt;= 65536 [#21870](https://github.com/pingcap/tidb/pull/21870)の JSON オブジェクトのエラーを報告する
    -   `dyname`関数が MySQL [#21850](https://github.com/pingcap/tidb/pull/21850)と互換性がない問題を修正
    -   入力データが長すぎる場合に`to_base64`関数が`NULL`返す問題を修正[#21813](https://github.com/pingcap/tidb/pull/21813)
    -   サブクエリ[#21808](https://github.com/pingcap/tidb/pull/21808)で複数のフィールドを比較できない問題を修正
    -   JSON [#21785](https://github.com/pingcap/tidb/pull/21785)で float 型を比較するときに発生する問題を修正します。
    -   JSON オブジェクトのタイプを比較するときに発生する問題を修正します[#21718](https://github.com/pingcap/tidb/pull/21718)
    -   `cast`関数の強制力値が正しく設定されていない問題を修正[#21714](https://github.com/pingcap/tidb/pull/21714)
    -   `IF`機能使用時の予期せぬpanicを修正[#21711](https://github.com/pingcap/tidb/pull/21711)
    -   JSON 検索から返された`NULL`結果が MySQL [#21700](https://github.com/pingcap/tidb/pull/21700)と互換性がない問題を修正
    -   `ORDER BY`と`HAVING` [#21697](https://github.com/pingcap/tidb/pull/21697)を使用して`only_full_group_by`モードを確認するときに発生する問題を修正します。
    -   `Day`と`Time`の単位が MySQL [#21676](https://github.com/pingcap/tidb/pull/21676)と互換性がない問題を修正
    -   `LEAD`と`LAG`のデフォルト値がフィールド タイプ[#21665](https://github.com/pingcap/tidb/pull/21665)に適応できない問題を修正します。
    -   チェックを実行して、 `LOAD DATA`ステートメントがデータをベース テーブルにのみロードできることを確認します[#21638](https://github.com/pingcap/tidb/pull/21638)
    -   `addtime`と`subtime`関数が無効な引数を処理するときに発生する問題を修正します[#21635](https://github.com/pingcap/tidb/pull/21635)
    -   近似値の丸めルールを「最も近い偶数に丸める」に変更します[#21628](https://github.com/pingcap/tidb/pull/21628)
    -   明示的に読み取られるまで`WEEK()`が`@@GLOBAL.default_week_format`認識しないという問題を修正します[#21623](https://github.com/pingcap/tidb/pull/21623)

-   TiKV

    -   TiKV が`PROST=1` [#9604](https://github.com/tikv/tikv/pull/9604)でビルドに失敗する問題を修正
    -   一致しないメモリ診断を修正します[#9589](https://github.com/tikv/tikv/pull/9589)
    -   部分的な RawKV 復元範囲の終了キーが[#9583](https://github.com/tikv/tikv/pull/9583)を含む問題を修正します
    -   TiCDC のインクリメンタル スキャン中に、ロールバックされたトランザクションのキーの古い値をロードするときに発生する TiKVpanicの問題を修正します[#9569](https://github.com/tikv/tikv/pull/9569)
    -   異なる設定の変更フィードが 1 つのリージョン[#9565](https://github.com/tikv/tikv/pull/9565)に接続されている場合の古い値の構成の不具合を修正します。
    -   MAC アドレスのないネットワーク インターフェイスを持つマシンで TiKV クラスターを実行すると発生するクラッシュの問題を修正します (v4.0.9 で導入) [#9516](https://github.com/tikv/tikv/pull/9516)
    -   巨大なリージョン[#9448](https://github.com/tikv/tikv/pull/9448)をバックアップする際の TiKV OOM の問題を修正
    -   `region-split-check-diff`カスタマイズできない問題を修正[#9530](https://github.com/tikv/tikv/pull/9530)
    -   システム時刻が戻ると TiKVpanicが発生する問題を修正[#9542](https://github.com/tikv/tikv/pull/9542)

-   PD

    -   メンバーの健康指標が正しく表示されない問題を修正します[#3368](https://github.com/pingcap/pd/pull/3368)
    -   ピア[#3352](https://github.com/pingcap/pd/pull/3352)がまだ存在するトゥームストーン ストアの削除を禁止する
    -   ストア制限を保持できない問題を修正[#3403](https://github.com/pingcap/pd/pull/3403)
    -   散布範囲スケジューラ[#3401](https://github.com/pingcap/pd/pull/3401)の制限制限を修正

-   TiFlash

    -   10進数型で`min` `max`結果が間違っている不具合を修正
    -   データ読み込み時にTiFlashがクラッシュすることがある不具合を修正
    -   DDL 操作後に書き込まれた一部のデータが、データの圧縮後に失われる可能性がある問題を修正します
    -   コプロセッサーでTiFlash が10 進定数を正しく処理しない問題を修正します。
    -   学習者の読み取りプロセス中に発生する可能性のあるクラッシュを修正
    -   TiDB とTiFlashの間の`0`または`NULL`による除算の一貫性のない動作を修正します。

-   ツール

    -   TiCDC

        -   `ErrTaskStatusNotExists`と`capture`セッションのクローズが同時に発生した場合、TiCDC サービスが予期せず終了することがあるバグを修正[#1240](https://github.com/pingcap/tiflow/pull/1240)
        -   `changefeed`が別の`changefeed` [#1347](https://github.com/pingcap/tiflow/pull/1347)の影響を受ける可能性があるという古い値スイッチの問題を修正します。
        -   無効な`sort-engine`パラメータ[#1309](https://github.com/pingcap/tiflow/pull/1309)を使用して新しい`changefeed`を処理すると、TiCDC サービスがハングする可能性があるバグを修正します
        -   所有者以外のノードでデバッグ情報を取得するときに発生するpanicの問題を修正します[#1349](https://github.com/pingcap/tiflow/pull/1349)
        -   テーブルの追加または削除時に`ticdc_processor_num_of_tables`および`ticdc_processor_table_resolved_ts`メトリックが正しく更新されない問題を修正します[#1351](https://github.com/pingcap/tiflow/pull/1351)
        -   テーブルを追加するときにプロセッサがクラッシュした場合にデータが失われる可能性がある問題を修正します[#1363](https://github.com/pingcap/tiflow/pull/1363)
        -   テーブルの移行中に、所有者が TiCDCサーバーの異常終了につながる可能性があるバグを修正します[#1352](https://github.com/pingcap/tiflow/pull/1352)
        -   サービス GC セーフポイントが失われた後、TiCDC が時間内に終了しないというバグを修正します[#1367](https://github.com/pingcap/tiflow/pull/1367)
        -   KV クライアントがイベント フィードの作成をスキップする可能性があるバグを修正します[#1336](https://github.com/pingcap/tiflow/pull/1336)
        -   トランザクションがダウンストリームにレプリケートされると、トランザクションのアトミック性が壊れるバグを修正[#1375](https://github.com/pingcap/tiflow/pull/1375)

    -   バックアップと復元 (BR)

        -   BR がバックアップを復元した後、TiKV が大きなリージョンを生成する可能性がある問題を修正します[#702](https://github.com/pingcap/br/pull/702)
        -   テーブルに Auto ID がない場合でもBR がテーブルの Auto ID を復元する問題を修正します[#720](https://github.com/pingcap/br/pull/720)

    -   TiDB Lightning

        -   TiDB-backend の使用時に`column count mismatch`トリガーされる可能性があるバグを修正[#535](https://github.com/pingcap/tidb-lightning/pull/535)
        -   ソースファイルの列数とターゲットテーブルの列数が一致しない場合、TiDB バックエンドがパニックするバグを修正[#528](https://github.com/pingcap/tidb-lightning/pull/528)
        -   TiDB Lightning のデータインポート中に TiKV が予期せずpanicになることがあるバグを修正[#554](https://github.com/pingcap/tidb-lightning/pull/554)
