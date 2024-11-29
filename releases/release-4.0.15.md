---
title: TiDB 4.0.15 Release Notes
summary: 「TiDB 4.0.15 リリース ノート: 互換性の変更には、アップグレードの非互換性を引き起こす可能性のあるバグ修正が含まれます。TiKV の機能強化により、構成の動的な変更がサポートされます。TiDB、TiKV、PD、およびツールが改善されました。TiDB、TiKV、PD、 TiFlash、バックアップと復元、および TiCDC のバグ修正。」
---

# TiDB 4.0.15 リリースノート {#tidb-4-0-15-release-notes}

リリース日：2021年9月27日

TiDB バージョン: 4.0.15

## 互換性の変更 {#compatibility-changes}

-   ティビ

    -   新しいセッションで`SHOW VARIABLES`実行すると遅くなる問題を修正しました。この修正により、 [＃21045](https://github.com/pingcap/tidb/pull/21045)で行われた変更の一部が元に戻り、互換性の問題が発生する可能性があります[＃24326](https://github.com/pingcap/tidb/issues/24326)

    <!---->

    -   次のバグ修正により実行結果が変わり、アップグレードの非互換性が発生する可能性があります。
        -   `greatest(datetime) union null`空の文字列[＃26532](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正
        -   `having`節が正しく動作しない可能性がある問題を修正[＃26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の前後の照合順序が異なる場合に発生する誤った実行結果を修正[＃27146](https://github.com/pingcap/tidb/issues/27146)
        -   `extract`関数の引数が負の期間[＃27236](https://github.com/pingcap/tidb/issues/27236)場合に発生する結果の誤りを修正
        -   `group_concat`関数の列に非ビン照合順序[＃27429](https://github.com/pingcap/tidb/issues/27429)がある場合に発生する誤った実行結果を修正
        -   `Apply`演算子を`Join` [＃27233](https://github.com/pingcap/tidb/issues/27233)に変換するときに列情報が失われる問題を修正
        -   無効な文字列を`DATE` [＃26762](https://github.com/pingcap/tidb/issues/26762)にキャストしたときに予期しない動作が発生する問題を修正
        -   新しい照合順序が有効な場合に、複数の列の`count distinct`結果が間違っているというバグを修正しました[＃27091](https://github.com/pingcap/tidb/issues/27091)

## 機能強化 {#feature-enhancement}

-   ティクヴ

    -   TiCDC 構成の動的な変更をサポート[＃10645](https://github.com/tikv/tikv/issues/10645)

## 改善点 {#improvements}

-   ティビ

    -   ヒストグラムの行数に基づいて自動分析をトリガーする[＃24237](https://github.com/pingcap/tidb/issues/24237)

-   ティクヴ

    -   読み取り準備と書き込み準備は別々に処理して読み取りレイテンシーを削減する[＃10475](https://github.com/tikv/tikv/issues/10475)
    -   TiKV コプロセッサのスロー ログは[＃10841](https://github.com/tikv/tikv/issues/10841)要求の処理に費やされた時間のみを考慮します。1
    -   スロガースレッドが過負荷になり、キューがいっぱいになったときに、スレッドをブロックする代わりにログをドロップします[＃10841](https://github.com/tikv/tikv/issues/10841)
    -   解決されたTSメッセージのサイズを縮小してネットワーク帯域幅を節約する[＃2448](https://github.com/pingcap/tiflow/issues/2448)

-   PD

    -   PD [＃3932](https://github.com/tikv/pd/pull/3932)間のリージョン情報の同期パフォーマンスを向上

-   ツール

    -   バックアップと復元 (BR)

        -   領域を同時に分割して分散させることで復元速度を向上[＃1363](https://github.com/pingcap/br/pull/1363)
        -   PD 要求エラーまたは TiKV I/O タイムアウト エラーが発生した場合は、 BRタスクを再試行します[＃27787](https://github.com/pingcap/tidb/issues/27787)
        -   多数の小さなテーブルを復元するときに空の領域を減らして、復元後のクラスター操作に影響を与えないようにします[＃1374](https://github.com/pingcap/br/issues/1374)
        -   テーブルの作成中に`rebase auto id`操作を実行すると、個別の`rebase auto id` DDL操作が節約され、復元が高速化されます[＃1424](https://github.com/pingcap/br/pull/1424)

    -   Dumpling

        -   テーブル情報を取得する前にスキップされたデータベースをフィルタリングして、 `SHOW TABLE STATUS` [＃337](https://github.com/pingcap/dumpling/pull/337)のフィルタリング効率を向上させます。
        -   エクスポートするテーブルのテーブル情報を取得するには`SHOW FULL TABLES`使用します。3 `SHOW TABLE STATUS`一部の MySQL バージョン[＃322](https://github.com/pingcap/dumpling/issues/322)では正しく動作しないためです。
        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`構文をサポートしていない MySQL 互換データベースのバックアップをサポート[＃309](https://github.com/pingcap/dumpling/issues/309)
        -   Dumpling の警告ログを改良し、ダンプが失敗したという誤解を招く情報を回避する[＃340](https://github.com/pingcap/dumpling/pull/340)

    -   TiDB Lightning

        -   式インデックスまたは仮想生成列に依存するインデックスを持つテーブルへのデータのインポートをサポート[＃1404](https://github.com/pingcap/br/issues/1404)

    -   ティCDC

        -   使いやすさを向上させるために、常に TiKV から古い値を内部的に取得します[＃2397](https://github.com/pingcap/tiflow/pull/2397)
        -   テーブルのリージョンがすべて TiKV ノードから転送されるときに、goroutine の使用を減らす[＃2284](https://github.com/pingcap/tiflow/issues/2284)
        -   同時実行性が高い場合に、ワーカープールを最適化して goroutine の数を減らす[＃2211](https://github.com/pingcap/tiflow/issues/2211)
        -   他の変更フィードに影響を与えないように、DDL ステートメントを非同期で実行します[＃2295](https://github.com/pingcap/tiflow/issues/2295)
        -   グローバル gRPC 接続プールを追加し、KV クライアント間で gRPC 接続を共有する[＃2531](https://github.com/pingcap/tiflow/pull/2531)
        -   回復不可能な DML エラーに対して迅速に対処[＃1724](https://github.com/pingcap/tiflow/issues/1724)
        -   Unified Sorter がメモリを使用してデータをソートする場合のメモリ管理を最適化します[＃2553](https://github.com/pingcap/tiflow/issues/2553)
        -   DDL実行のPrometheusメトリックを追加する[＃2595](https://github.com/pingcap/tiflow/issues/2595) [＃2669](https://github.com/pingcap/tiflow/issues/2669)
        -   メジャーバージョンまたはマイナーバージョン間での TiCDC クラスターの操作を禁止する[＃2601](https://github.com/pingcap/tiflow/pull/2601)
        -   削除`file sorter` [＃2325](https://github.com/pingcap/tiflow/pull/2325)
        -   変更フィードが削除されたときに変更フィード メトリックをクリーンアップし、プロセッサが終了したときにプロセッサ メトリックをクリーンアップします[＃2156](https://github.com/pingcap/tiflow/issues/2156)
        -   リージョンが初期化された後のロック解決アルゴリズムを最適化する[＃2188](https://github.com/pingcap/tiflow/issues/2188)

## バグ修正 {#bug-fixes}

-   ティビ

    -   範囲[＃23672](https://github.com/pingcap/tidb/issues/23672)を構築するときにバイナリリテラルの照合順序が誤って設定されるバグを修正しました

    -   クエリに`GROUP BY`と`UNION` [＃26553](https://github.com/pingcap/tidb/pull/26553)が含まれている場合に発生する「インデックスが範囲外です」というエラーを修正しました。

    -   TiKV にトゥームストーン ストアがある場合に TiDB がリクエストの送信に失敗する可能性がある問題を修正[＃23676](https://github.com/pingcap/tidb/issues/23676) [＃24648](https://github.com/pingcap/tidb/issues/24648)

    -   文書化されていない`/debug/sub-optimal-plan` HTTP API [＃27264](https://github.com/pingcap/tidb/pull/27264)を削除する

    -   `case when`式[＃26662](https://github.com/pingcap/tidb/issues/26662)の文字セットと照合順序が間違っている問題を修正

-   ティクヴ

    -   データ復元中に TDE が有効になっているとBR が「ファイルが既に存在します」というエラーを報告する問題を修正[＃1179](https://github.com/pingcap/br/issues/1179)
    -   破損したスナップショットファイルによって引き起こされる潜在的なディスクフル問題を修正[＃10813](https://github.com/tikv/tikv/issues/10813)
    -   TiKV が古いリージョンを頻繁に削除する問題を修正[＃10680](https://github.com/tikv/tikv/issues/10680)
    -   TiKVがPDクライアント[＃9690](https://github.com/tikv/tikv/issues/9690)に頻繁に再接続する問題を修正
    -   暗号化ファイル辞書[＃9115](https://github.com/tikv/tikv/issues/9115)から古いファイル情報を確認する

-   PD

    -   PDがダウンしたピアを時間内に修復しない問題を修正[＃4077](https://github.com/tikv/pd/issues/4077)
    -   TiKV [＃3868](https://github.com/tikv/pd/issues/3868)をスケールアウトするときに PD がpanicになる可能性があるバグを修正しました

-   TiFlash

    -   TiFlashが複数のディスクに展開されている場合に発生する可能性のあるデータの不整合の問題を修正しました。
    -   クエリに`CONSTANT` 、 `<` 、 `<=` 、 `>` 、 `>=` 、 `COLUMN`などのフィルターが含まれている場合に誤った結果が発生するバグを修正しました。
    -   書き込みが集中するとメトリクスのストアサイズが不正確になる問題を修正
    -   複数のディスクに展開されたときにTiFlash がデータを復元できない潜在的なバグを修正
    -   TiFlash が長時間実行した後にデルタデータをガベージコレクションできない潜在的な問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップとリストアの平均速度が不正確に計算されるバグを修正[＃1405](https://github.com/pingcap/br/issues/1405)

    -   ティCDC

        -   統合テスト[＃2422](https://github.com/pingcap/tiflow/issues/2422)でDDLジョブの重複が発生したときに発生する`ErrSchemaStorageTableMiss`エラーを修正します。
        -   `ErrGCTTLExceeded`エラーが発生した場合に changefeed を削除できないバグを修正[＃2391](https://github.com/pingcap/tiflow/issues/2391)
        -   `capture list`コマンド[＃2388](https://github.com/pingcap/tiflow/issues/2388)の出力に古いキャプチャが表示される問題を修正しました
        -   TiCDCプロセッサ[#2017](https://github.com/pingcap/tiflow/pull/2017)のデッドロック問題を修正
        -   このテーブルが再スケジュールされているときに複数のプロセッサが同じテーブルにデータを書き込む可能性があるために発生するデータの不整合の問題を修正しました[＃2230](https://github.com/pingcap/tiflow/issues/2230)
        -   メタデータ管理[＃2557](https://github.com/pingcap/tiflow/pull/2557)でスナップショット`EtcdWorker`分離が違反されるバグを修正
        -   DDLシンクエラー[＃2552](https://github.com/pingcap/tiflow/issues/2552)によりチェンジフィードを停止できない問題を修正
        -   TiCDC オープン プロトコルの問題を修正: トランザクション[＃2612](https://github.com/pingcap/tiflow/issues/2612)に変更がない場合、TiCDC は空の値を出力する
        -   符号なし`TINYINT`型[＃2648](https://github.com/pingcap/tiflow/issues/2648)でTiCDCがpanicを起こすバグを修正
        -   TiCDC があまりにも多くのリージョンをキャプチャしたときに発生する OOM を回避するために、gRPC ウィンドウ サイズを減らします[＃2202](https://github.com/pingcap/tiflow/issues/2202)
        -   TiCDC があまりにも多くのリージョンをキャプチャしたときに発生する OOM 問題を修正しました[＃2673](https://github.com/pingcap/tiflow/issues/2673)
        -   `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar`などのデータ型をJSON [＃2758](https://github.com/pingcap/tiflow/issues/2758)にエンコードするときに発生するプロセスpanicの問題を修正
        -   新しい変更フィード[＃2389](https://github.com/pingcap/tiflow/issues/2389)を作成するときに発生する可能性のあるメモリリークの問題を修正しました
        -   スキーマ変更[＃2603](https://github.com/pingcap/tiflow/issues/2603)の終了 TS で変更フィードが開始されると DDL 処理が失敗するバグを修正しました。
        -   DDL ステートメント[＃1260](https://github.com/pingcap/tiflow/issues/1260)の実行時にオーナーがクラッシュした場合の潜在的な DDL 損失の問題を修正しました。
        -   `SinkManager` [＃2298](https://github.com/pingcap/tiflow/pull/2298)のマップへの安全でない同時アクセスの問題を修正
