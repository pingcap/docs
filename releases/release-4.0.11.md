---
title: TiDB 4.0.11 Release Notes
---

# TiDB 4.0.11 リリースノート {#tidb-4-0-11-release-notes}

発売日：2021年2月26日

TiDB バージョン: 4.0.11

## 新機能 {#new-features}

-   TiDB

    -   `utf8_unicode_ci`と`utf8mb4_unicode_ci`照合順序をサポート[#22558](https://github.com/pingcap/tidb/pull/22558)

-   TiKV

    -   `utf8mb4_unicode_ci`照合順序[#9577](https://github.com/tikv/tikv/pull/9577)をサポート
    -   `cast_year_as_time`照合順序[#9299](https://github.com/tikv/tikv/pull/9299)をサポート

-   TiFlash

    -   コプロセッサーのスレッド プールを追加してコプロセッサーの実行要求をキューに追加します。これにより、場合によってはメモリ不足 (OOM) が回避され、デフォルト値の`NumOfPhysicalCores * 2`で`cop_pool_size`と`batch_cop_pool_size`構成項目が追加されます。

## 改善点 {#improvements}

-   TiDB

    -   外部結合から単純化された内部結合を並べ替える[#22402](https://github.com/pingcap/tidb/pull/22402)
    -   Grafana ダッシュボードでの複数のクラスターのサポート[#22534](https://github.com/pingcap/tidb/pull/22534)
    -   複数のステートメントの問題に対する回避策を追加[#22468](https://github.com/pingcap/tidb/pull/22468)
    -   遅いクエリのメトリクスを`internal`と`general`に分割する[#22405](https://github.com/pingcap/tidb/pull/22405)
    -   `utf8_unicode_ci`および`utf8mb4_unicode_ci`照合順序のインターフェイスを追加[#22099](https://github.com/pingcap/tidb/pull/22099)

-   TiKV

    -   DBaaS [#9591](https://github.com/tikv/tikv/pull/9591)のサーバー情報のメトリクスを追加
    -   Grafana ダッシュボードでの複数のクラスターのサポート[#9572](https://github.com/tikv/tikv/pull/9572)
    -   RocksDB メトリクスを TiDB [#9316](https://github.com/tikv/tikv/pull/9316)にレポートする
    -   コプロセッサータスク[#9277](https://github.com/tikv/tikv/pull/9277)の一時停止時間を記録します。
    -   ロード ベース分割[#9354](https://github.com/tikv/tikv/pull/9354)のキー数とキー サイズのしきい値を追加します。
    -   データインポート前にファイルが存在するか確認[#9544](https://github.com/tikv/tikv/pull/9544)
    -   Fast Tune パネルの改善[#9180](https://github.com/tikv/tikv/pull/9180)

-   PD

    -   Grafana ダッシュボードでの複数のクラスターのサポート[#3398](https://github.com/pingcap/pd/pull/3398)

-   TiFlash

    -   `date_format`機能のパフォーマンスを最適化する
    -   SST 取り込み処理のメモリ消費を最適化する
    -   バッチコプロセッサーの再試行ロジックを最適化して、リージョンエラーの確率を低減します。

-   ツール

    -   TiCDC

        -   `capture`メタデータにバージョン情報を追加し、 `changefeed`メタデータに`changefeed`の CLI バージョンを追加します[#1342](https://github.com/pingcap/tiflow/pull/1342)

    -   TiDB Lightning

        -   テーブルを並行して作成してインポートのパフォーマンスを向上させる[#502](https://github.com/pingcap/tidb-lightning/pull/502)
        -   エンジンの合計サイズがリージョンサイズ[#524](https://github.com/pingcap/tidb-lightning/pull/524)より小さい場合、インポート パフォーマンスを向上させるためにリージョンの分割をスキップします。
        -   インポートの進行状況バーを追加し、復元の進行状況の精度を最適化します[#506](https://github.com/pingcap/tidb-lightning/pull/506)

## バグの修正 {#bug-fixes}

-   TiDB

    -   異常な`unicode_ci`定数伝播[#22614](https://github.com/pingcap/tidb/pull/22614)の問題を修正
    -   間違った照合順序と強制性を引き起こす可能性がある問題を修正します[#22602](https://github.com/pingcap/tidb/pull/22602)
    -   不正な照合順序結果を引き起こす可能性がある問題を修正[#22599](https://github.com/pingcap/tidb/pull/22599)
    -   異なる照合順序の定数置換の問題を修正します[#22582](https://github.com/pingcap/tidb/pull/22582)
    -   照合順序[#22531](https://github.com/pingcap/tidb/pull/22531)を使用した場合、 `like`関数が間違った結果を返す場合があるバグを修正
    -   `least`および`greatest`関数における誤った`duration`型推論の問題を修正[#22580](https://github.com/pingcap/tidb/pull/22580)
    -   `like`関数が単一文字のワイルドカード ( `_` ) に続いて複数文字のワイルドカード ( `%` ) を処理するときに発生するバグを修正します[#22575](https://github.com/pingcap/tidb/pull/22575)
    -   TiDB の組み込み関数( `least`および`greatest` ) の型推論エラーを修正しました[#22562](https://github.com/pingcap/tidb/pull/22562)
    -   パターン文字列が Unicode 文字列[#22529](https://github.com/pingcap/tidb/pull/22529)の場合、 `like`関数が間違った結果を取得するバグを修正しました。
    -   `@@tidb_snapshot`変数を[#22527](https://github.com/pingcap/tidb/pull/22527)に設定した場合、ポイント取得クエリでスナップショットデータが取得されないバグを修正
    -   結合[#22518](https://github.com/pingcap/tidb/pull/22518)からヒントを生成するときに発生する潜在的なpanicを修正します。
    -   文字列が誤って`BIT`型[#22420](https://github.com/pingcap/tidb/pull/22420)型に変換されてしまう問題を修正
    -   `tidb_rowid`列[#22359](https://github.com/pingcap/tidb/pull/22359)に値を挿入する際に発生する`index out of range`エラーを修正
    -   キャッシュされたプランが誤って使用されるバグを修正[#22353](https://github.com/pingcap/tidb/pull/22353)
    -   バイナリ/文字列の長さが長すぎる場合の`WEIGHT_STRING`関数の実行時panicを修正しました[#22332](https://github.com/pingcap/tidb/pull/22332)
    -   関数パラメータの数が無効な場合、生成された列の使用を禁止します[#22174](https://github.com/pingcap/tidb/pull/22174)
    -   実行計画を構築する前にプロセス情報を正しく設定します[#22148](https://github.com/pingcap/tidb/pull/22148)
    -   `IndexLookUp` [#22136](https://github.com/pingcap/tidb/pull/22136)の不正確な実行時統計の問題を修正
    -   クラスターがコンテナーにデプロイされる場合のメモリ使用量情報のキャッシュを追加します[#22116](https://github.com/pingcap/tidb/pull/22116)
    -   デコード計画エラーの問題を修正[#22022](https://github.com/pingcap/tidb/pull/22022)
    -   無効なウィンドウ仕様を使用した場合のエラーを報告する[#21976](https://github.com/pingcap/tidb/pull/21976)
    -   `PREPARE`ステートメントが`EXECUTE` 、 `DEALLOCATE` 、または`PREPARE`とネストされている場合にエラーを報告します[#21972](https://github.com/pingcap/tidb/pull/21972)
    -   存在しないパーティション[#21971](https://github.com/pingcap/tidb/pull/21971)で`INSERT IGNORE`ステートメントが使用された場合にエラーが報告されない問題を修正します。
    -   `EXPLAIN`の結果と遅いログ[#21964](https://github.com/pingcap/tidb/pull/21964)のエンコードを統一する
    -   集計演算子[#21957](https://github.com/pingcap/tidb/pull/21957)を使用する場合の結合での不明な列の問題を修正します。
    -   `ceiling`関数[#21936](https://github.com/pingcap/tidb/pull/21936)の間違った型推論を修正しました。
    -   `Double`型の列が 10 進数の[#21916](https://github.com/pingcap/tidb/pull/21916)を無視する問題を修正
    -   サブクエリ[#21877](https://github.com/pingcap/tidb/pull/21877)で相関集計が計算される問題を修正
    -   キーの長さが 65536 以上の JSON オブジェクトのエラーを報告する[#21870](https://github.com/pingcap/tidb/pull/21870)
    -   `dyname`関数が MySQL [#21850](https://github.com/pingcap/tidb/pull/21850)と互換性がない問題を修正
    -   入力データが長すぎる場合に`to_base64`関数が`NULL`返す問題を修正[#21813](https://github.com/pingcap/tidb/pull/21813)
    -   サブクエリ[#21808](https://github.com/pingcap/tidb/pull/21808)での複数のフィールドの比較の失敗を修正
    -   JSON [#21785](https://github.com/pingcap/tidb/pull/21785)の float 型を比較す​​るときに発生する問題を修正
    -   JSON オブジェクトのタイプを比較するときに発生する問題を修正します[#21718](https://github.com/pingcap/tidb/pull/21718)
    -   `cast`関数の強制値が正しく設定されない問題を修正[#21714](https://github.com/pingcap/tidb/pull/21714)
    -   `IF`機能[#21711](https://github.com/pingcap/tidb/pull/21711)使用時の予期せぬpanicを修正しました。
    -   JSON 検索から返される`NULL`結果が MySQL [#21700](https://github.com/pingcap/tidb/pull/21700)と互換性がない問題を修正
    -   `ORDER BY`と`HAVING`使用して`only_full_group_by`モードをチェックするときに発生する問題を修正[#21697](https://github.com/pingcap/tidb/pull/21697)
    -   `Day`と`Time`のユニットがMySQL [#21676](https://github.com/pingcap/tidb/pull/21676)と互換性がない問題を修正
    -   デフォルト値の`LEAD`と`LAG`がフィールド タイプ[#21665](https://github.com/pingcap/tidb/pull/21665)に適応できない問題を修正
    -   チェックを実行して、 `LOAD DATA`ステートメントがデータをベース テーブル[#21638](https://github.com/pingcap/tidb/pull/21638)にのみロードできることを確認します。
    -   `addtime`および`subtime`関数が無効な引数を処理するときに発生する問題を修正します[#21635](https://github.com/pingcap/tidb/pull/21635)
    -   近似値の丸めルールを「最も近い偶数に丸める」に変更します[#21628](https://github.com/pingcap/tidb/pull/21628)
    -   `WEEK()`が明示的に読み取られるまで`@@GLOBAL.default_week_format`認識しない問題を修正[#21623](https://github.com/pingcap/tidb/pull/21623)

-   TiKV

    -   `PROST=1` [#9604](https://github.com/tikv/tikv/pull/9604)で TiKV のビルドに失敗する問題を修正
    -   不一致のメモリ診断を修正[#9589](https://github.com/tikv/tikv/pull/9589)
    -   部分的な RawKV 復元範囲の終了キーが[#9583](https://github.com/tikv/tikv/pull/9583)を含む問題を修正
    -   TiCDC の増分スキャン中にロールバックされたトランザクションのキーの古い値をロードするときに発生する TiKVpanicの問題を修正します[#9569](https://github.com/tikv/tikv/pull/9569)
    -   異なる設定の変更フィードが 1 つのリージョン[#9565](https://github.com/tikv/tikv/pull/9565)に接続する場合の古い値の構成の不具合を修正
    -   MAC アドレスがないネットワーク インターフェイスを備えたマシンで TiKV クラスターを実行すると発生するクラッシュの問題を修正します (v4.0.9 で導入) [#9516](https://github.com/tikv/tikv/pull/9516)
    -   巨大なリージョン[#9448](https://github.com/tikv/tikv/pull/9448)をバックアップする際の TiKV OOM の問題を修正
    -   `region-split-check-diff`カスタマイズできない問題を修正[#9530](https://github.com/tikv/tikv/pull/9530)
    -   システム時間が戻ったときの TiKVpanicの問題を修正[#9542](https://github.com/tikv/tikv/pull/9542)

-   PD

    -   メンバーのヘルスメトリクスが正しく表示されない問題を修正[#3368](https://github.com/pingcap/pd/pull/3368)
    -   ピア[#3352](https://github.com/pingcap/pd/pull/3352)がまだあるトゥームストーン ストアの削除を禁止します。
    -   ストア制限を維持できない問題を修正[#3403](https://github.com/pingcap/pd/pull/3403)
    -   スキャッタ範囲スケジューラ[#3401](https://github.com/pingcap/pd/pull/3401)の制限制限を修正

-   TiFlash

    -   10進数型に対して`min` `max`結果が間違っているバグを修正
    -   データ読み取り時にTiFlashがクラッシュする可能性があるバグを修正
    -   DDL 操作後に書き込まれた一部のデータがデータ圧縮後に失われる可能性がある問題を修正
    -   TiFlash がコプロセッサーで 10 進定数を誤って処理する問題を修正
    -   学習者の読み取りプロセス中に発生する可能性のあるクラッシュを修正しました。
    -   TiDB とTiFlashの間での`0`または`NULL`による除算の一貫性のない動作を修正しました。

-   ツール

    -   TiCDC

        -   `ErrTaskStatusNotExists`と`capture`セッション終了が同時に発生した場合、TiCDCサービスが予期せず終了する場合があるバグを修正[#1240](https://github.com/pingcap/tiflow/pull/1240)
        -   `changefeed`が別の`changefeed` [#1347](https://github.com/pingcap/tiflow/pull/1347)の影響を受ける可能性があるという古い値スイッチの問題を修正します。
        -   無効な`sort-engine`パラメータ[#1309](https://github.com/pingcap/tiflow/pull/1309)を使用して新しい`changefeed`を処理するときに TiCDC サービスがハングする可能性があるバグを修正
        -   非所有ノード[#1349](https://github.com/pingcap/tiflow/pull/1349)のデバッグ情報を取得するときに発生するpanicの問題を修正します。
        -   テーブル[#1351](https://github.com/pingcap/tiflow/pull/1351)を追加または削除するときに`ticdc_processor_num_of_tables`および`ticdc_processor_table_resolved_ts`メトリクスが適切に更新されない問題を修正します。
        -   テーブル[#1363](https://github.com/pingcap/tiflow/pull/1363)を追加するときにプロセッサがクラッシュした場合にデータが失われる可能性がある問題を修正します。
        -   テーブル移行中に所有者が異常な TiCDCサーバー終了を引き起こす可能性があるバグを修正[#1352](https://github.com/pingcap/tiflow/pull/1352)
        -   サービス GC セーフポイントが失われた後、TiCDC が時間内に終了しないバグを修正[#1367](https://github.com/pingcap/tiflow/pull/1367)
        -   KVクライアントがイベントフィード[#1336](https://github.com/pingcap/tiflow/pull/1336)の作成をスキップする場合があるバグを修正
        -   トランザクションを下流にレプリケートするときにトランザクションのアトミック性が崩れるバグを修正[#1375](https://github.com/pingcap/tiflow/pull/1375)

    -   バックアップと復元 (BR)

        -   BR がバックアップ[#702](https://github.com/pingcap/br/pull/702)を復元した後、TiKV によって大きなリージョンが生成される可能性がある問題を修正します。
        -   テーブルに自動 ID [#720](https://github.com/pingcap/br/pull/720)がない場合でも、 BR がテーブルの自動 ID を復元する問題を修正します。

    -   TiDB Lightning

        -   TiDB-backend [#535](https://github.com/pingcap/tidb-lightning/pull/535)使用時に`column count mismatch`発生する場合があるバグを修正
        -   ソースファイルのカラム数[#528](https://github.com/pingcap/tidb-lightning/pull/528)ターゲットテーブルのカラム数が一致しない場合にTiDBバックエンドがパニックするバグを修正
        -   TiDB Lightning のデータインポート中に TiKV が予期せずpanic可能性があるバグを修正[#554](https://github.com/pingcap/tidb-lightning/pull/554)
