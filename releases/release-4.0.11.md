---
title: TiDB 4.0.11 Release Notes
summary: TiDB 4.0.11は2021年2月26日にリリースされました。新機能には、utf8_unicode_ci`および`utf8mb4_unicode_ci`照合順序のサポートが含まれます。内部結合、Grafanaダッシュボード、スロークエリメトリクスが改善されました。バグ修正では、照合順序、型推論、関数エラーに関する問題が修正されました。TiKVの改善には、Grafanaダッシュボードでの複数クラスターのサポート、メモリ診断とOOMエラーのバグ修正が含まれます。PDでは、メンバーのヘルスメトリクスとストア制限の永続性の問題が解決されました。TiFlashのバグ修正では、小数型の結果、データ損失、クラッシュの問題が修正されました。TiCDC、 BR、 TiDB Lightningなどのツールにもバグ修正と改善が行われました。
---

# TiDB 4.0.11 リリースノート {#tidb-4-0-11-release-notes}

発売日：2021年2月26日

TiDB バージョン: 4.0.11

## 新機能 {#new-features}

-   TiDB

    -   `utf8_unicode_ci`と`utf8mb4_unicode_ci`照合順序[＃22558](https://github.com/pingcap/tidb/pull/22558)サポート

-   TiKV

    -   `utf8mb4_unicode_ci`照合順序[＃9577](https://github.com/tikv/tikv/pull/9577)サポートする
    -   `cast_year_as_time`照合順序[＃9299](https://github.com/tikv/tikv/pull/9299)サポートする

-   TiFlash

    -   コプロセッサースレッドプールを追加して、コプロセッサー要求の実行キューに入れます。これにより、場合によってはメモリ不足（OOM）を回避できます。また、 `cop_pool_size`と`batch_cop_pool_size`設定項目をデフォルト値の`NumOfPhysicalCores * 2`で追加します。

## 改善点 {#improvements}

-   TiDB

    -   外部結合[＃22402](https://github.com/pingcap/tidb/pull/22402)から簡素化された内部結合を並べ替える
    -   Grafanaダッシュボードで複数のクラスターをサポート[＃22534](https://github.com/pingcap/tidb/pull/22534)
    -   複数のステートメントの問題に対する回避策を追加[＃22468](https://github.com/pingcap/tidb/pull/22468)
    -   遅いクエリの指標[＃22405](https://github.com/pingcap/tidb/pull/22405) `internal`と`general`に分ける
    -   `utf8_unicode_ci`と`utf8mb4_unicode_ci`照合順序[＃22099](https://github.com/pingcap/tidb/pull/22099)インターフェースを追加

-   TiKV

    -   DBaaS [＃9591](https://github.com/tikv/tikv/pull/9591)サーバー情報のメトリクスを追加
    -   Grafanaダッシュボードで複数のクラスターをサポート[＃9572](https://github.com/tikv/tikv/pull/9572)
    -   RocksDB メトリックを TiDB [＃9316](https://github.com/tikv/tikv/pull/9316)に報告する
    -   コプロセッサータスク[＃9277](https://github.com/tikv/tikv/pull/9277)の中断時間を記録する
    -   Load Base Split [＃9354](https://github.com/tikv/tikv/pull/9354)のキー数とキーサイズのしきい値を追加します。
    -   データのインポート前にファイルが存在するかどうかを確認する[＃9544](https://github.com/tikv/tikv/pull/9544)
    -   ファストチューンパネル[＃9180](https://github.com/tikv/tikv/pull/9180)改善

-   PD

    -   Grafanaダッシュボードで複数のクラスターをサポート[＃3398](https://github.com/pingcap/pd/pull/3398)

-   TiFlash

    -   `date_format`機能のパフォーマンスを最適化する
    -   取り込みSSTの処理におけるメモリ消費を最適化
    -   バッチココプロセッサーの再試行ロジックを最適化して、リージョンエラーの可能性を低減します。

-   ツール

    -   TiCDC

        -   `capture`メタデータにバージョン情報を追加し、 `changefeed`メタデータ[＃1342](https://github.com/pingcap/tiflow/pull/1342)に`changefeed`の CLI バージョンを追加します。

    -   TiDB Lightning

        -   インポートパフォーマンスを向上させるためにテーブルを並列に作成する[＃502](https://github.com/pingcap/tidb-lightning/pull/502)
        -   エンジンの合計サイズがリージョンサイズ[＃524](https://github.com/pingcap/tidb-lightning/pull/524)より小さい場合は、リージョンの分割をスキップしてインポート パフォーマンスを向上させます。
        -   インポート進行状況バーを追加し、復元進行状況の精度を最適化します[＃506](https://github.com/pingcap/tidb-lightning/pull/506)

## バグ修正 {#bug-fixes}

-   TiDB

    -   異常な`unicode_ci`定数伝播[＃22614](https://github.com/pingcap/tidb/pull/22614)の問題を修正
    -   誤った照合順序と強制可能性を引き起こす可能性のある問題を修正[＃22602](https://github.com/pingcap/tidb/pull/22602)
    -   照合順序結果が誤っている可能性がある問題を修正[＃22599](https://github.com/pingcap/tidb/pull/22599)
    -   異なる照合順序における定数置換の問題を修正[＃22582](https://github.com/pingcap/tidb/pull/22582)
    -   照合順序[＃22531](https://github.com/pingcap/tidb/pull/22531)使用すると関数`like`間違った結果を返す可能性があるバグを修正しました
    -   `least`と`greatest`関数[＃22580](https://github.com/pingcap/tidb/pull/22580)における誤った`duration`型推論の問題を修正
    -   `like`関数が単一文字のワイルドカード ( `_` ) に続いて複数文字のワイルドカード ( `%` ) を処理するときに発生するバグを修正しました[＃22575](https://github.com/pingcap/tidb/pull/22575)
    -   TiDBの組み込み関数の型推論エラーを修正（ `least`と`greatest` ） [＃22562](https://github.com/pingcap/tidb/pull/22562)
    -   パターン文字列がUnicode文字列[＃22529](https://github.com/pingcap/tidb/pull/22529)の場合に`like`関数が間違った結果を返すバグを修正しました
    -   `@@tidb_snapshot`変数が[＃22527](https://github.com/pingcap/tidb/pull/22527)設定されている場合にポイント取得クエリがスナップショットデータを取得できないバグを修正しました
    -   結合からヒントを生成するときに発生する可能性のあるpanicを修正[＃22518](https://github.com/pingcap/tidb/pull/22518)
    -   文字列が`BIT`型[＃22420](https://github.com/pingcap/tidb/pull/22420)に誤って変換される問題を修正
    -   `tidb_rowid`列目に値を挿入するときに発生する`index out of range`エラーを修正[＃22359](https://github.com/pingcap/tidb/pull/22359)
    -   キャッシュされたプランが誤って使用されるバグを修正[＃22353](https://github.com/pingcap/tidb/pull/22353)
    -   バイナリ/文字列の長さが大きすぎる場合に関数`WEIGHT_STRING`で発生するランタイムpanicを修正[＃22332](https://github.com/pingcap/tidb/pull/22332)
    -   関数パラメータの数が無効な場合、生成された列の使用を禁止する[＃22174](https://github.com/pingcap/tidb/pull/22174)
    -   実行プランを構築する前にプロセス情報を正しく設定する[＃22148](https://github.com/pingcap/tidb/pull/22148)
    -   `IndexLookUp` [＃22136](https://github.com/pingcap/tidb/pull/22136)の不正確な実行時統計の問題を修正
    -   コンテナ[＃22116](https://github.com/pingcap/tidb/pull/22116)にクラスタをデプロイするときにメモリ使用量情報のキャッシュを追加する
    -   デコードプランエラーの問題を修正[＃22022](https://github.com/pingcap/tidb/pull/22022)
    -   無効なウィンドウ仕様の使用によるエラーを報告[＃21976](https://github.com/pingcap/tidb/pull/21976)
    -   `PREPARE`文が`EXECUTE` 、 `DEALLOCATE` 、または`PREPARE` [＃21972](https://github.com/pingcap/tidb/pull/21972)とネストされている場合はエラーを報告します。
    -   存在しないパーティション[＃21971](https://github.com/pingcap/tidb/pull/21971)で`INSERT IGNORE`ステートメントが使用された場合にエラーが報告されない問題を修正しました
    -   `EXPLAIN`結果のエンコードを統一し、 [＃21964](https://github.com/pingcap/tidb/pull/21964)遅いログ
    -   集計演算子[＃21957](https://github.com/pingcap/tidb/pull/21957)使用するときに結合で不明な列が発生する問題を修正しました
    -   `ceiling`関数[＃21936](https://github.com/pingcap/tidb/pull/21936)の間違った型推論を修正
    -   `Double`型の列が小数点[＃21916](https://github.com/pingcap/tidb/pull/21916)無視する問題を修正しました
    -   相関集計がサブクエリ[＃21877](https://github.com/pingcap/tidb/pull/21877)で計算される問題を修正
    -   キーの長さが65536以上のJSONオブジェクトのエラーを報告します[＃21870](https://github.com/pingcap/tidb/pull/21870)
    -   `dyname`関数がMySQL [＃21850](https://github.com/pingcap/tidb/pull/21850)と互換性がない問題を修正
    -   入力データが長すぎる場合に`to_base64`関数が`NULL`返す問題を修正しました[＃21813](https://github.com/pingcap/tidb/pull/21813)
    -   サブクエリ[＃21808](https://github.com/pingcap/tidb/pull/21808)で複数のフィールドを比較できない問題を修正
    -   JSON [＃21785](https://github.com/pingcap/tidb/pull/21785)で float 型を比較する際に発生する問題を修正しました
    -   JSONオブジェクトの型を比較する際に発生する問題を修正[＃21718](https://github.com/pingcap/tidb/pull/21718)
    -   `cast`関数の強制値が正しく設定されていない問題を修正[＃21714](https://github.com/pingcap/tidb/pull/21714)
    -   `IF`関数[＃21711](https://github.com/pingcap/tidb/pull/21711)使用時に予期しないpanicが発生する問題を修正
    -   JSON検索から返される`NULL`結果がMySQL [＃21700](https://github.com/pingcap/tidb/pull/21700)と互換性がない問題を修正しました
    -   `ORDER BY`と`HAVING`使用して`only_full_group_by`モードをチェックするときに発生する問題を修正しました[＃21697](https://github.com/pingcap/tidb/pull/21697)
    -   `Day`と`Time`の単位がMySQL [＃21676](https://github.com/pingcap/tidb/pull/21676)と互換性がない問題を修正
    -   デフォルト値`LEAD`と`LAG`フィールドタイプ[＃21665](https://github.com/pingcap/tidb/pull/21665)に適応できない問題を修正
    -   `LOAD DATA`文がベーステーブル[＃21638](https://github.com/pingcap/tidb/pull/21638)にのみデータをロードできることを確認するためのチェックを実行します。
    -   `addtime`と`subtime`関数が無効な引数[＃21635](https://github.com/pingcap/tidb/pull/21635)処理するときに発生する問題を修正しました
    -   近似値の丸めルールを「最も近い偶数に丸める」に変更します[＃21628](https://github.com/pingcap/tidb/pull/21628)
    -   `WEEK()`明示的に読み込まれるまで`@@GLOBAL.default_week_format`認識しない問題を修正[＃21623](https://github.com/pingcap/tidb/pull/21623)

-   TiKV

    -   `PROST=1` [＃9604](https://github.com/tikv/tikv/pull/9604)でTiKVのビルドに失敗する問題を修正
    -   一致しないメモリ診断を修正[＃9589](https://github.com/tikv/tikv/pull/9589)
    -   部分的なRawKV復元範囲の終了キーが[＃9583](https://github.com/tikv/tikv/pull/9583)含む問題を修正
    -   TiCDC の増分スキャン中にロールバックされたトランザクションのキーの古い値をロードするときに発生する TiKVpanicの問題を修正しました[＃9569](https://github.com/tikv/tikv/pull/9569)
    -   異なる設定の変更フィードが 1 つのリージョン[＃9565](https://github.com/tikv/tikv/pull/9565)に接続したときに古い値の構成の不具合を修正しました。
    -   MAC アドレスのないネットワーク インターフェースを持つマシンで TiKV クラスターを実行すると発生するクラッシュの問題を修正しました (v4.0.9 で導入) [＃9516](https://github.com/tikv/tikv/pull/9516)
    -   巨大なリージョン[＃9448](https://github.com/tikv/tikv/pull/9448)をバックアップする際のTiKV OOMの問題を修正
    -   `region-split-check-diff`カスタマイズできない問題を修正[＃9530](https://github.com/tikv/tikv/pull/9530)
    -   システム時刻が[＃9542](https://github.com/tikv/tikv/pull/9542)に戻ったときにTiKVpanicが発生する問題を修正

-   PD

    -   メンバーの健康指標が正しく表示されない問題を修正[＃3368](https://github.com/pingcap/pd/pull/3368)
    -   ピア[＃3352](https://github.com/pingcap/pd/pull/3352)まだ残っているトゥームストーンストアの削除を禁止する
    -   ストア制限が維持できない問題を修正[＃3403](https://github.com/pingcap/pd/pull/3403)
    -   散布範囲スケジューラ[＃3401](https://github.com/pingcap/pd/pull/3401)の制限制限を修正

-   TiFlash

    -   小数型で`min` / `max`結果が間違っているというバグを修正しました
    -   TiFlashがデータ読み取り時にクラッシュする可能性があるバグを修正
    -   DDL操作後に書き込まれたデータの一部がデータ圧縮後に失われる可能性がある問題を修正しました
    -   TiFlashがコプロセッサー内の10進定数を正しく処理しない問題を修正
    -   学習者の読み取りプロセス中に発生する可能性のあるクラッシュを修正しました
    -   TiDBとTiFlash間の`0`または`NULL`による除算の不一致な動作を修正

-   ツール

    -   TiCDC

        -   `ErrTaskStatusNotExists`と`capture`セッションの終了が同時に発生した場合、TiCDCサービスが予期せず終了する可能性があるバグを修正[＃1240](https://github.com/pingcap/tiflow/pull/1240)
        -   `changefeed`が別の`changefeed` [＃1347](https://github.com/pingcap/tiflow/pull/1347)の影響を受ける可能性があるという古い値の切り替え問題を修正しました
        -   無効な`sort-engine`パラメータ[＃1309](https://github.com/pingcap/tiflow/pull/1309)を持つ新しい`changefeed`処理するときにTiCDCサービスがハングする可能性があるバグを修正しました
        -   非オーナーノードでデバッグ情報を取得する際に発生するpanicの問題を修正[＃1349](https://github.com/pingcap/tiflow/pull/1349)
        -   テーブル[＃1351](https://github.com/pingcap/tiflow/pull/1351)を追加または削除したときに、 `ticdc_processor_num_of_tables`と`ticdc_processor_table_resolved_ts`メトリックが正しく更新されない問題を修正しました。
        -   テーブル[＃1363](https://github.com/pingcap/tiflow/pull/1363)を追加するときにプロセッサがクラッシュした場合に潜在的なデータ損失が発生する問題を修正しました
        -   テーブル移行中に所有者が TiCDCサーバーの異常終了を引き起こす可能性があるバグを修正[＃1352](https://github.com/pingcap/tiflow/pull/1352)
        -   サービスGCセーフポイントが失われた後にTiCDCが時間内に終了しないバグを修正[＃1367](https://github.com/pingcap/tiflow/pull/1367)
        -   KVクライアントがイベントフィード[＃1336](https://github.com/pingcap/tiflow/pull/1336)作成をスキップする可能性があるバグを修正しました
        -   トランザクションが下流に複製されたときにトランザクションの原子性が壊れるバグを修正[＃1375](https://github.com/pingcap/tiflow/pull/1375)

    -   バックアップと復元 (BR)

        -   BRがバックアップ[＃702](https://github.com/pingcap/br/pull/702)を復元した後にTiKVが大きなリージョンを生成する可能性がある問題を修正しました
        -   テーブルに自動 ID [＃720](https://github.com/pingcap/br/pull/720)がない場合でもBR がテーブルの自動 ID を復元する問題を修正しました

    -   TiDB Lightning

        -   TiDBバックエンド[＃535](https://github.com/pingcap/tidb-lightning/pull/535)使用時に`column count mismatch`が発生する可能性があるバグを修正
        -   ソースファイルの列数とターゲットテーブルの列数が一致しない場合に TiDB バックエンドがパニックを起こすバグを修正[＃528](https://github.com/pingcap/tidb-lightning/pull/528)
        -   TiDB Lightning のデータインポート中に TiKV が予期せずpanic可能性があるバグを修正[＃554](https://github.com/pingcap/tidb-lightning/pull/554)
