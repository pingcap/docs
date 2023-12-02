---
title: TiDB 4.0.15 Release Notes
---

# TiDB 4.0.15 リリースノート {#tidb-4-0-15-release-notes}

リリース日：2021年9月27日

TiDB バージョン: 4.0.15

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   新しいセッションで`SHOW VARIABLES`を実行すると遅いという問題を修正します。この修正により、 [#21045](https://github.com/pingcap/tidb/pull/21045)で行われた一部の変更が元に戻されるため、互換性の問題が発生する可能性があります。 [#24326](https://github.com/pingcap/tidb/issues/24326)

    <!---->

    -   次のバグ修正により実行結果が変更され、アップグレードの非互換性が発生する可能性があります。
        -   `greatest(datetime) union null`が空の文字列[#26532](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正
        -   `having`句が正しく動作しない場合がある問題を修正[#26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の前後の照合順序が異なる場合に発生する間違った実行結果を修正します[#27146](https://github.com/pingcap/tidb/issues/27146)
        -   `extract`関数の引数が負の持続時間の場合に発生する結果が間違っていたのを修正[#27236](https://github.com/pingcap/tidb/issues/27236)
        -   `group_concat`関数の列に非ビン照合順序がある場合に発生する間違った実行結果を修正します[#27429](https://github.com/pingcap/tidb/issues/27429)
        -   `Apply`演算子を`Join` [#27233](https://github.com/pingcap/tidb/issues/27233)に変換するときに列情報が欠落する問題を修正
        -   無効な文字列を`DATE` [#26762](https://github.com/pingcap/tidb/issues/26762)にキャストするときに予期しない動作が発生する問題を修正
        -   新しい照合順序が有効になっている場合、複数の列の`count distinct`結果が間違っているバグを修正[#27091](https://github.com/pingcap/tidb/issues/27091)

## 機能強化 {#feature-enhancement}

-   TiKV

    -   TiCDC 構成の動的変更のサポート[#10645](https://github.com/tikv/tikv/issues/10645)

## 改善点 {#improvements}

-   TiDB

    -   ヒストグラムの行数に基づいて自動分析をトリガーする[#24237](https://github.com/pingcap/tidb/issues/24237)

-   TiKV

    -   読み取りレイテンシー[#10475](https://github.com/tikv/tikv/issues/10475)を短縮するために、読み取り準備完了と書き込み準備完了を個別に処理します。
    -   TiKV コプロセッサーの低速ログでは、要求の処理に費やされた時間のみが考慮されます。 [#10841](https://github.com/tikv/tikv/issues/10841)
    -   スロガー スレッドが過負荷になってキューがいっぱいになった場合、スレッドをブロックする代わりにログを削除します[#10841](https://github.com/tikv/tikv/issues/10841)
    -   解決済み TS メッセージのサイズを削減して、ネットワーク帯域幅を節約します[#2448](https://github.com/pingcap/tiflow/issues/2448)

-   PD

    -   PD 間のリージョン情報の同期パフォーマンスを向上[#3932](https://github.com/tikv/pd/pull/3932)

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンの分割と分散を同時に行い、復元速度を向上させます[#1363](https://github.com/pingcap/br/pull/1363)
        -   PD リクエスト エラーまたは TiKV I/O タイムアウト エラー[#27787](https://github.com/pingcap/tidb/issues/27787)が発生した場合にBRタスクを再試行します。
        -   多数の小さなテーブルを復元する場合は、空のリージョンを減らして、復元後のクラスター操作への影響を回避します[#1374](https://github.com/pingcap/br/issues/1374)
        -   テーブルの作成中に`rebase auto id`操作を実行すると、別個の`rebase auto id` DDL 操作が保存され、復元が高速化されます[#1424](https://github.com/pingcap/br/pull/1424)

    -   Dumpling

        -   `SHOW TABLE STATUS` [#337](https://github.com/pingcap/dumpling/pull/337)のフィルタリング効率を向上させるために、テーブル情報を取得する前にスキップされたデータベースをフィルタリングします。
        -   [#322](https://github.com/pingcap/dumpling/issues/322)の MySQL バージョンでは`SHOW TABLE STATUS`が正しく動作しないため、エクスポートするテーブルのテーブル情報を取得するには`SHOW FULL TABLES`を使用します。
        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`構文をサポートしない MySQL 互換データベースのバックアップのサポート[#309](https://github.com/pingcap/dumpling/issues/309)
        -   Dumpling警告ログを調整して、ダンプが失敗したという誤解を招く情報を回避します[#340](https://github.com/pingcap/dumpling/pull/340)

    -   TiDB Lightning

        -   式インデックスまたは仮想生成列に依存するインデックスを持つテーブルへのデータのインポートをサポートします[#1404](https://github.com/pingcap/br/issues/1404)

    -   TiCDC

        -   使いやすさを向上させるために、内部的に常に TiKV から古い値を取得します[#2397](https://github.com/pingcap/tiflow/pull/2397)
        -   テーブルのリージョンがすべて TiKV ノードから転送される場合の goroutine の使用量を削減します[#2284](https://github.com/pingcap/tiflow/issues/2284)
        -   同時実行性が高い場合、ゴルーチンを減らすためにワーカープールを最適化する[#2211](https://github.com/pingcap/tiflow/issues/2211)
        -   他の変更フィードへの影響を避けるために、DDL ステートメントを非同期で実行します[#2295](https://github.com/pingcap/tiflow/issues/2295)
        -   グローバル gRPC 接続プールを追加し、KV クライアント間で gRPC 接続を共有する[#2531](https://github.com/pingcap/tiflow/pull/2531)
        -   回復不可能な DML エラーに対するフェイルファスト[#1724](https://github.com/pingcap/tiflow/issues/1724)
        -   統合ソーターがデータの並べ替えにメモリを使用している場合、メモリ管理を最適化します[#2553](https://github.com/pingcap/tiflow/issues/2553)
        -   DDL 実行用の Prometheus メトリクスを追加[#2595](https://github.com/pingcap/tiflow/issues/2595) [#2669](https://github.com/pingcap/tiflow/issues/2669)
        -   メジャー バージョンまたはマイナー バージョンにまたがる TiCDC クラスターの操作を禁止する[#2601](https://github.com/pingcap/tiflow/pull/2601)
        -   `file sorter` [#2325](https://github.com/pingcap/tiflow/pull/2325)を削除
        -   チェンジフィードが削除されたときにチェンジフィード メトリクスをクリーンアップし、プロセッサが終了したときにプロセッサ メトリクスをクリーンアップします[#2156](https://github.com/pingcap/tiflow/issues/2156)
        -   リージョンの初期化後のロック解決アルゴリズムを最適化する[#2188](https://github.com/pingcap/tiflow/issues/2188)

## バグの修正 {#bug-fixes}

-   TiDB

    -   範囲[#23672](https://github.com/pingcap/tidb/issues/23672)を構築するときにバイナリ リテラルの照合順序が誤って設定されるバグを修正

    -   クエリに`GROUP BY`と`UNION`両方が含まれている場合に発生する「インデックスが範囲外です」エラーを修正[#26553](https://github.com/pingcap/tidb/pull/26553)

    -   TiKV にトゥームストーン ストアがある場合、TiDB がリクエストの送信に失敗する可能性がある問題を修正[#23676](https://github.com/pingcap/tidb/issues/23676) [#24648](https://github.com/pingcap/tidb/issues/24648)

    -   文書化されていない`/debug/sub-optimal-plan` HTTP API [#27264](https://github.com/pingcap/tidb/pull/27264)を削除します。

    -   `case when`式[#26662](https://github.com/pingcap/tidb/issues/26662)の間違った文字セットと照合順序の問題を修正します。

-   TiKV

    -   データの復元中に TDE が有効になっている場合、 BR が「ファイルはすでに存在します」エラーを報告する問題を修正します[#1179](https://github.com/pingcap/br/issues/1179)
    -   破損したスナップショット ファイルによって引き起こされる潜在的なディスク フルの問題を修正します[#10813](https://github.com/tikv/tikv/issues/10813)
    -   TiKV が古いリージョンを頻繁に削除する問題を修正します[#10680](https://github.com/tikv/tikv/issues/10680)
    -   TiKV が PD クライアント[#9690](https://github.com/tikv/tikv/issues/9690)に頻繁に再接続する問題を修正します。
    -   暗号化ファイル辞書から古いファイル情報を確認する[#9115](https://github.com/tikv/tikv/issues/9115)

-   PD

    -   PD がダウンしたピアを時間内に修復しない問題を修正します[#4077](https://github.com/tikv/pd/issues/4077)
    -   TiKV [#3868](https://github.com/tikv/pd/issues/3868)をスケールアウトするときに PD がpanicになる可能性があるバグを修正

-   TiFlash

    -   TiFlash が複数のディスクに展開されている場合に発生するデータの不整合の潜在的な問題を修正
    -   クエリに`CONSTANT` 、 `<` 、 `<=` 、 `>` 、 `>=` 、または`COLUMN`などのフィルターが含まれている場合に発生する誤った結果のバグを修正しました。
    -   大量の書き込み時にメトリクスのストア サイズが不正確になる問題を修正
    -   複数のディスクに展開されている場合にTiFlash がデータを復元できないという潜在的なバグを修正
    -   TiFlash が長時間実行した後にデルタ データをガベージ コレクションできないという潜在的な問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップおよびリストア[#1405](https://github.com/pingcap/br/issues/1405)の平均速度が不正確に計算されるバグを修正

    -   TiCDC

        -   統合テスト[#2422](https://github.com/pingcap/tiflow/issues/2422)でDDLジョブの重複が発生した場合に発生するエラー`ErrSchemaStorageTableMiss`を修正
        -   `ErrGCTTLExceeded`エラーが発生するとチェンジフィードが削除できないバグを修正[#2391](https://github.com/pingcap/tiflow/issues/2391)
        -   `capture list`コマンド[#2388](https://github.com/pingcap/tiflow/issues/2388)の出力に古いキャプチャが表示されることがある問題を修正します。
        -   TiCDC プロセッサ[#2017](https://github.com/pingcap/tiflow/pull/2017)のデッドロック問題を修正
        -   このテーブルが再スケジュールされているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるために発生するデータの不整合の問題を修正します[#2230](https://github.com/pingcap/tiflow/issues/2230)
        -   メタデータ管理[#2557](https://github.com/pingcap/tiflow/pull/2557)で`EtcdWorker`スナップショット分離に違反するバグを修正
        -   DDLシンクエラー[#2552](https://github.com/pingcap/tiflow/issues/2552)によりチェンジフィードを停止できない問題を修正
        -   TiCDC オープン プロトコルの問題を修正: トランザクションに変更がない場合、TiCDC は空の値を出力します[#2612](https://github.com/pingcap/tiflow/issues/2612)
        -   TiCDC が unsigned `TINYINT` type [#2648](https://github.com/pingcap/tiflow/issues/2648)でpanicを引き起こすバグを修正しました。
        -   TiCDC がキャプチャするリージョン[#2202](https://github.com/pingcap/tiflow/issues/2202)が多すぎるときに発生する OOM を回避するには、gRPC ウィンドウ サイズを小さくします。
        -   TiCDC がキャプチャするリージョン[#2673](https://github.com/pingcap/tiflow/issues/2673)が多すぎる場合に発生する OOM 問題を修正します。
        -   `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar`などのデータ型を JSON [#2758](https://github.com/pingcap/tiflow/issues/2758)にエンコードするときに発生するプロセスpanicの問題を修正
        -   新しい変更フィード[#2389](https://github.com/pingcap/tiflow/issues/2389)を作成するときに発生する可能性があるメモリリークの問題を修正します。
        -   スキーマ変更[#2603](https://github.com/pingcap/tiflow/issues/2603)の終了TSでチェンジフィードが開始されるとDDL処理が失敗するバグを修正
        -   DDL ステートメントの実行時に所有者がクラッシュした場合に DDL が失われる可能性がある問題を修正します[#1260](https://github.com/pingcap/tiflow/issues/1260)
        -   `SinkManager` [#2298](https://github.com/pingcap/tiflow/pull/2298)のマップへの安全でない同時アクセスの問題を修正
