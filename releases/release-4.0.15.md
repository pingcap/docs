---
title: TiDB 4.0.15 Release Notes
---

# TiDB 4.0.15 リリースノート {#tidb-4-0-15-release-notes}

リリース日：2021年9月27日

TiDB バージョン: 4.0.15

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   新しいセッションで`SHOW VARIABLES`を実行すると遅いという問題を修正します。この修正により、 [<a href="https://github.com/pingcap/tidb/pull/21045">#21045</a>](https://github.com/pingcap/tidb/pull/21045)で行われた一部の変更が元に戻されるため、互換性の問題が発生する可能性があります。 [<a href="https://github.com/pingcap/tidb/issues/24326">#24326</a>](https://github.com/pingcap/tidb/issues/24326)

    <!---->

    -   次のバグ修正により実行結果が変更され、アップグレードの非互換性が発生する可能性があります。
        -   `greatest(datetime) union null`が空の文字列[<a href="https://github.com/pingcap/tidb/issues/26532">#26532</a>](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正
        -   `having`句が正しく動作しない場合がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/26496">#26496</a>](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の前後の照合順序が異なる場合に発生する間違った実行結果を修正します[<a href="https://github.com/pingcap/tidb/issues/27146">#27146</a>](https://github.com/pingcap/tidb/issues/27146)
        -   `extract`関数の引数が負の持続時間の場合に発生する結果が間違っていたのを修正[<a href="https://github.com/pingcap/tidb/issues/27236">#27236</a>](https://github.com/pingcap/tidb/issues/27236)
        -   `group_concat`関数の列に非ビン照合順序がある場合に発生する間違った実行結果を修正します[<a href="https://github.com/pingcap/tidb/issues/27429">#27429</a>](https://github.com/pingcap/tidb/issues/27429)
        -   `Apply`演算子を`Join` [<a href="https://github.com/pingcap/tidb/issues/27233">#27233</a>](https://github.com/pingcap/tidb/issues/27233)に変換するときに列情報が欠落する問題を修正
        -   無効な文字列を`DATE` [<a href="https://github.com/pingcap/tidb/issues/26762">#26762</a>](https://github.com/pingcap/tidb/issues/26762)にキャストするときに予期しない動作が発生する問題を修正
        -   新しい照合順序が有効になっている場合、複数の列の`count distinct`結果が間違っているバグを修正[<a href="https://github.com/pingcap/tidb/issues/27091">#27091</a>](https://github.com/pingcap/tidb/issues/27091)

## 機能強化 {#feature-enhancement}

-   TiKV

    -   TiCDC 構成の動的変更のサポート[<a href="https://github.com/tikv/tikv/issues/10645">#10645</a>](https://github.com/tikv/tikv/issues/10645)

## 改善点 {#improvements}

-   TiDB

    -   ヒストグラムの行数に基づいて自動分析をトリガーする[<a href="https://github.com/pingcap/tidb/issues/24237">#24237</a>](https://github.com/pingcap/tidb/issues/24237)

-   TiKV

    -   読み取りレイテンシー[<a href="https://github.com/tikv/tikv/issues/10475">#10475</a>](https://github.com/tikv/tikv/issues/10475)を短縮するために、読み取り準備完了と書き込み準備完了を個別に処理します。
    -   TiKV コプロセッサーの低速ログでは、要求の処理に費やされた時間のみが考慮されます。 [<a href="https://github.com/tikv/tikv/issues/10841">#10841</a>](https://github.com/tikv/tikv/issues/10841)
    -   スロガー スレッドが過負荷になってキューがいっぱいになった場合、スレッドをブロックする代わりにログを削除します[<a href="https://github.com/tikv/tikv/issues/10841">#10841</a>](https://github.com/tikv/tikv/issues/10841)
    -   解決済み TS メッセージのサイズを削減して、ネットワーク帯域幅を節約します[<a href="https://github.com/pingcap/tiflow/issues/2448">#2448</a>](https://github.com/pingcap/tiflow/issues/2448)

-   PD

    -   PD 間のリージョン情報の同期パフォーマンスを向上[<a href="https://github.com/tikv/pd/pull/3932">#3932</a>](https://github.com/tikv/pd/pull/3932)

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンの分割と分散を同時に行い、復元速度を向上させます[<a href="https://github.com/pingcap/br/pull/1363">#1363</a>](https://github.com/pingcap/br/pull/1363)
        -   PD リクエスト エラーまたは TiKV I/O タイムアウト エラー[<a href="https://github.com/pingcap/tidb/issues/27787">#27787</a>](https://github.com/pingcap/tidb/issues/27787)が発生した場合にBRタスクを再試行します。
        -   多数の小さなテーブルを復元する場合は、空のリージョンを減らして、復元後のクラスター操作への影響を回避します[<a href="https://github.com/pingcap/br/issues/1374">#1374</a>](https://github.com/pingcap/br/issues/1374)
        -   テーブルの作成中に`rebase auto id`操作を実行すると、別個の`rebase auto id` DDL 操作が保存され、復元が高速化されます[<a href="https://github.com/pingcap/br/pull/1424">#1424</a>](https://github.com/pingcap/br/pull/1424)

    -   Dumpling

        -   `SHOW TABLE STATUS` [<a href="https://github.com/pingcap/dumpling/pull/337">#337</a>](https://github.com/pingcap/dumpling/pull/337)のフィルタリング効率を向上させるために、テーブル情報を取得する前にスキップされたデータベースをフィルタリングします。
        -   [<a href="https://github.com/pingcap/dumpling/issues/322">#322</a>](https://github.com/pingcap/dumpling/issues/322)の MySQL バージョンでは`SHOW TABLE STATUS`が正しく動作しないため、エクスポートするテーブルのテーブル情報を取得するには`SHOW FULL TABLES`を使用します。
        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`構文をサポートしない MySQL 互換データベースのバックアップのサポート[<a href="https://github.com/pingcap/dumpling/issues/309">#309</a>](https://github.com/pingcap/dumpling/issues/309)
        -   Dumpling警告ログを調整して、ダンプが失敗したという誤解を招く情報を回避します[<a href="https://github.com/pingcap/dumpling/pull/340">#340</a>](https://github.com/pingcap/dumpling/pull/340)

    -   TiDB Lightning

        -   式インデックスまたは仮想生成列に依存するインデックスを持つテーブルへのデータのインポートをサポートします[<a href="https://github.com/pingcap/br/issues/1404">#1404</a>](https://github.com/pingcap/br/issues/1404)

    -   TiCDC

        -   使いやすさを向上させるために、内部的に常に TiKV から古い値を取得します[<a href="https://github.com/pingcap/tiflow/pull/2397">#2397</a>](https://github.com/pingcap/tiflow/pull/2397)
        -   テーブルのリージョンがすべて TiKV ノードから転送される場合の goroutine の使用量を削減します[<a href="https://github.com/pingcap/tiflow/issues/2284">#2284</a>](https://github.com/pingcap/tiflow/issues/2284)
        -   同時実行性が高い場合、ゴルーチンを減らすためにワーカープールを最適化する[<a href="https://github.com/pingcap/tiflow/issues/2211">#2211</a>](https://github.com/pingcap/tiflow/issues/2211)
        -   他の変更フィードへの影響を避けるために、DDL ステートメントを非同期で実行します[<a href="https://github.com/pingcap/tiflow/issues/2295">#2295</a>](https://github.com/pingcap/tiflow/issues/2295)
        -   グローバル gRPC 接続プールを追加し、KV クライアント間で gRPC 接続を共有する[<a href="https://github.com/pingcap/tiflow/pull/2531">#2531</a>](https://github.com/pingcap/tiflow/pull/2531)
        -   回復不可能な DML エラーに対するフェイルファスト[<a href="https://github.com/pingcap/tiflow/issues/1724">#1724</a>](https://github.com/pingcap/tiflow/issues/1724)
        -   統合ソーターがデータの並べ替えにメモリを使用している場合、メモリ管理を最適化します[<a href="https://github.com/pingcap/tiflow/issues/2553">#2553</a>](https://github.com/pingcap/tiflow/issues/2553)
        -   DDL 実行用の Prometheus メトリクスを追加[<a href="https://github.com/pingcap/tiflow/issues/2595">#2595</a>](https://github.com/pingcap/tiflow/issues/2595) [<a href="https://github.com/pingcap/tiflow/issues/2669">#2669</a>](https://github.com/pingcap/tiflow/issues/2669)
        -   メジャー バージョンまたはマイナー バージョンにまたがる TiCDC クラスターの操作を禁止する[<a href="https://github.com/pingcap/tiflow/pull/2601">#2601</a>](https://github.com/pingcap/tiflow/pull/2601)
        -   `file sorter` [<a href="https://github.com/pingcap/tiflow/pull/2325">#2325</a>](https://github.com/pingcap/tiflow/pull/2325)を削除
        -   チェンジフィードが削除されたときにチェンジフィード メトリクスをクリーンアップし、プロセッサが終了したときにプロセッサ メトリクスをクリーンアップします[<a href="https://github.com/pingcap/tiflow/issues/2156">#2156</a>](https://github.com/pingcap/tiflow/issues/2156)
        -   リージョンの初期化後のロック解決アルゴリズムを最適化する[<a href="https://github.com/pingcap/tiflow/issues/2188">#2188</a>](https://github.com/pingcap/tiflow/issues/2188)

## バグの修正 {#bug-fixes}

-   TiDB

    -   範囲[<a href="https://github.com/pingcap/tidb/issues/23672">#23672</a>](https://github.com/pingcap/tidb/issues/23672)を構築するときにバイナリ リテラルの照合順序が誤って設定されるバグを修正

    -   クエリに`GROUP BY`と`UNION`両方が含まれている場合に発生する「インデックスが範囲外です」エラーを修正[<a href="https://github.com/pingcap/tidb/pull/26553">#26553</a>](https://github.com/pingcap/tidb/pull/26553)

    -   TiKV にトゥームストーン ストアがある場合、TiDB がリクエストの送信に失敗する可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/23676">#23676</a>](https://github.com/pingcap/tidb/issues/23676) [<a href="https://github.com/pingcap/tidb/issues/24648">#24648</a>](https://github.com/pingcap/tidb/issues/24648)

    -   文書化されていない`/debug/sub-optimal-plan` HTTP API [<a href="https://github.com/pingcap/tidb/pull/27264">#27264</a>](https://github.com/pingcap/tidb/pull/27264)を削除します。

    -   `case when`式[<a href="https://github.com/pingcap/tidb/issues/26662">#26662</a>](https://github.com/pingcap/tidb/issues/26662)の間違った文字セットと照合順序の問題を修正します。

-   TiKV

    -   データの復元中に TDE が有効になっている場合、 BR が「ファイルはすでに存在します」エラーを報告する問題を修正します[<a href="https://github.com/pingcap/br/issues/1179">#1179</a>](https://github.com/pingcap/br/issues/1179)
    -   破損したスナップショット ファイルによって引き起こされる潜在的なディスク フルの問題を修正します[<a href="https://github.com/tikv/tikv/issues/10813">#10813</a>](https://github.com/tikv/tikv/issues/10813)
    -   TiKV が古いリージョンを頻繁に削除する問題を修正します[<a href="https://github.com/tikv/tikv/issues/10680">#10680</a>](https://github.com/tikv/tikv/issues/10680)
    -   TiKV が PD クライアント[<a href="https://github.com/tikv/tikv/issues/9690">#9690</a>](https://github.com/tikv/tikv/issues/9690)に頻繁に再接続する問題を修正します。
    -   暗号化ファイル辞書から古いファイル情報を確認する[<a href="https://github.com/tikv/tikv/issues/9115">#9115</a>](https://github.com/tikv/tikv/issues/9115)

-   PD

    -   PD がダウンしたピアを時間内に修復しない問題を修正します[<a href="https://github.com/tikv/pd/issues/4077">#4077</a>](https://github.com/tikv/pd/issues/4077)
    -   TiKV [<a href="https://github.com/tikv/pd/issues/3868">#3868</a>](https://github.com/tikv/pd/issues/3868)をスケールアウトするときに PD がpanicになる可能性があるバグを修正

-   TiFlash

    -   TiFlash が複数のディスクに展開されている場合に発生するデータの不整合の潜在的な問題を修正
    -   クエリに`CONSTANT` 、 `<` 、 `<=` 、 `>` 、 `>=` 、または`COLUMN`などのフィルターが含まれている場合に発生する誤った結果のバグを修正しました。
    -   大量の書き込み時にメトリクスのストア サイズが不正確になる問題を修正
    -   複数のディスクに展開されている場合にTiFlash がデータを復元できないという潜在的なバグを修正
    -   TiFlash が長時間実行した後にデルタ データをガベージ コレクションできないという潜在的な問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップおよびリストア[<a href="https://github.com/pingcap/br/issues/1405">#1405</a>](https://github.com/pingcap/br/issues/1405)の平均速度が不正確に計算されるバグを修正

    -   TiCDC

        -   統合テスト[<a href="https://github.com/pingcap/tiflow/issues/2422">#2422</a>](https://github.com/pingcap/tiflow/issues/2422)でDDLジョブの重複が発生した場合に発生するエラー`ErrSchemaStorageTableMiss`を修正
        -   `ErrGCTTLExceeded`エラーが発生するとチェンジフィードが削除できないバグを修正[<a href="https://github.com/pingcap/tiflow/issues/2391">#2391</a>](https://github.com/pingcap/tiflow/issues/2391)
        -   `capture list`コマンド[<a href="https://github.com/pingcap/tiflow/issues/2388">#2388</a>](https://github.com/pingcap/tiflow/issues/2388)の出力に古いキャプチャが表示されることがある問題を修正します。
        -   TiCDC プロセッサ[<a href="https://github.com/pingcap/tiflow/pull/2017">#2017</a>](https://github.com/pingcap/tiflow/pull/2017)のデッドロック問題を修正
        -   このテーブルが再スケジュールされているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるために発生するデータの不整合の問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/2230">#2230</a>](https://github.com/pingcap/tiflow/issues/2230)
        -   メタデータ管理[<a href="https://github.com/pingcap/tiflow/pull/2557">#2557</a>](https://github.com/pingcap/tiflow/pull/2557)で`EtcdWorker`スナップショット分離に違反するバグを修正
        -   DDLシンクエラー[<a href="https://github.com/pingcap/tiflow/issues/2552">#2552</a>](https://github.com/pingcap/tiflow/issues/2552)によりチェンジフィードを停止できない問題を修正
        -   TiCDC オープン プロトコルの問題を修正: トランザクションに変更がない場合、TiCDC は空の値を出力します[<a href="https://github.com/pingcap/tiflow/issues/2612">#2612</a>](https://github.com/pingcap/tiflow/issues/2612)
        -   TiCDC が unsigned `TINYINT` type [<a href="https://github.com/pingcap/tiflow/issues/2648">#2648</a>](https://github.com/pingcap/tiflow/issues/2648)でpanicを引き起こすバグを修正しました。
        -   TiCDC がキャプチャするリージョン[<a href="https://github.com/pingcap/tiflow/issues/2202">#2202</a>](https://github.com/pingcap/tiflow/issues/2202)が多すぎるときに発生する OOM を回避するには、gRPC ウィンドウ サイズを小さくします。
        -   TiCDC がキャプチャするリージョン[<a href="https://github.com/pingcap/tiflow/issues/2673">#2673</a>](https://github.com/pingcap/tiflow/issues/2673)が多すぎる場合に発生する OOM 問題を修正します。
        -   `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar`などのデータ型を JSON [<a href="https://github.com/pingcap/tiflow/issues/2758">#2758</a>](https://github.com/pingcap/tiflow/issues/2758)にエンコードするときに発生するプロセスpanicの問題を修正
        -   新しい変更フィード[<a href="https://github.com/pingcap/tiflow/issues/2389">#2389</a>](https://github.com/pingcap/tiflow/issues/2389)を作成するときに発生する可能性があるメモリリークの問題を修正します。
        -   スキーマ変更[<a href="https://github.com/pingcap/tiflow/issues/2603">#2603</a>](https://github.com/pingcap/tiflow/issues/2603)の終了TSでチェンジフィードが開始されるとDDL処理が失敗するバグを修正
        -   DDL ステートメントの実行時に所有者がクラッシュした場合に DDL が失われる可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/1260">#1260</a>](https://github.com/pingcap/tiflow/issues/1260)
        -   `SinkManager` [<a href="https://github.com/pingcap/tiflow/pull/2298">#2298</a>](https://github.com/pingcap/tiflow/pull/2298)のマップへの安全でない同時アクセスの問題を修正
