---
title: TiDB 4.0.15 Release Notes
---

# TiDB 4.0.15 リリースノート {#tidb-4-0-15-release-notes}

リリース日：2021年9月27日

TiDB バージョン: 4.0.15

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   新しいセッションで`SHOW VARIABLES`を実行すると遅い問題を修正します。この修正により、 [#21045](https://github.com/pingcap/tidb/pull/21045)で行われた一部の変更が元に戻り、互換性の問題が発生する可能性があります。 [#24326](https://github.com/pingcap/tidb/issues/24326)

    <!---->

    -   次のバグ修正により実行結果が変更され、アップグレードの非互換性が生じる可能性があります。
        -   `greatest(datetime) union null`が空の文字列[#26532](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正
        -   `having`節が正しく動作しない場合がある問題を修正[#26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の前後の照合が異なる場合に発生する誤った実行結果を修正します[#27146](https://github.com/pingcap/tidb/issues/27146)
        -   `extract`関数の引数が負の期間[#27236](https://github.com/pingcap/tidb/issues/27236)の場合に発生する結果の誤りを修正します。
        -   `group_concat`関数の列に非ビン照合順序がある場合に発生する誤った実行結果を修正します[#27429](https://github.com/pingcap/tidb/issues/27429)
        -   `Apply`演算子を`Join` [#27233](https://github.com/pingcap/tidb/issues/27233)に変換すると列情報が欠落する問題を修正
        -   無効な文字列を`DATE` [#26762](https://github.com/pingcap/tidb/issues/26762)にキャストすると予期しない動作が発生する問題を修正
        -   新しい照合順序が有効になっている場合、複数の列の`count distinct`結果が間違っているというバグを修正します[#27091](https://github.com/pingcap/tidb/issues/27091)

## 機能強化 {#feature-enhancement}

-   TiKV

    -   TiCDC 構成の動的変更をサポート[#10645](https://github.com/tikv/tikv/issues/10645)

## 改良点 {#improvements}

-   TiDB

    -   ヒストグラムの行数に基づいて自動分析をトリガーする[#24237](https://github.com/pingcap/tidb/issues/24237)

-   TiKV

    -   読み取りレイテンシーを短縮するために、読み取り準備完了と書き込み準備完了を別々に処理する[#10475](https://github.com/tikv/tikv/issues/10475)
    -   TiKV コプロセッサーのスローログでは、リクエストの処理に費やされた時間のみが考慮されます。 [#10841](https://github.com/tikv/tikv/issues/10841)
    -   slogger スレッドが過負荷になり、キューがいっぱいになったときに、スレッドをブロックする代わりにログを削除します[#10841](https://github.com/tikv/tikv/issues/10841)
    -   解決済み TS メッセージのサイズを縮小してネットワーク帯域幅を節約する[#2448](https://github.com/pingcap/tiflow/issues/2448)

-   PD

    -   PD 間のリージョン情報の同期のパフォーマンスを向上させます[#3932](https://github.com/tikv/pd/pull/3932)

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンを同時に分割および分散して復元速度を向上させる[#1363](https://github.com/pingcap/br/pull/1363)
        -   PD 要求エラーまたは TiKV I/O タイムアウト エラー[#27787](https://github.com/pingcap/tidb/issues/27787)が発生したときにBRタスクを再試行します
        -   復元後のクラスター操作への影響を避けるために、多数の小さなテーブルを復元する場合は空のリージョンを減らします[#1374](https://github.com/pingcap/br/issues/1374)
        -   テーブルの作成中に`rebase auto id`操作を実行します。これにより、別個の`rebase auto id` DDL 操作が節約され、復元が高速化されます[#1424](https://github.com/pingcap/br/pull/1424)

    -   Dumpling

        -   `SHOW TABLE STATUS` [#337](https://github.com/pingcap/dumpling/pull/337)のフィルタリング効率を向上させるために、テーブル情報を取得する前に、スキップされたデータベースをフィルタリングします。
        -   一部の MySQL バージョンでは`SHOW TABLE STATUS`が正しく機能しないため、エクスポートするテーブルのテーブル情報を取得するには`SHOW FULL TABLES`を使用します[#322](https://github.com/pingcap/dumpling/issues/322)
        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`構文をサポートしていない MySQL 互換データベースのバックアップのサポート[#309](https://github.com/pingcap/dumpling/issues/309)
        -   Dumpling警告ログを改良して、ダンプが失敗したという誤解を招く情報を回避します[#340](https://github.com/pingcap/dumpling/pull/340)

    -   TiDB Lightning

        -   式インデックスまたは仮想生成列に依存するインデックスを持つテーブルへのデータのインポートをサポート[#1404](https://github.com/pingcap/br/issues/1404)

    -   TiCDC

        -   使いやすさを向上させるために、常に内部で TiKV から古い値を取得します[#2397](https://github.com/pingcap/tiflow/pull/2397)
        -   テーブルのリージョンがすべて TiKV ノードから転送されるときのゴルーチンの使用量を減らします[#2284](https://github.com/pingcap/tiflow/issues/2284)
        -   同時実行性が高い場合、より少ないゴルーチンのためにワーカープールを最適化します[#2211](https://github.com/pingcap/tiflow/issues/2211)
        -   DDL ステートメントを非同期的に実行して、他の変更フィードに影響を与えないようにする[#2295](https://github.com/pingcap/tiflow/issues/2295)
        -   グローバル gRPC 接続プールを追加し、KV クライアント間で gRPC 接続を共有する[#2531](https://github.com/pingcap/tiflow/pull/2531)
        -   回復不能な DML エラーのフェイル ファスト[#1724](https://github.com/pingcap/tiflow/issues/1724)
        -   ユニファイド ソーターがデータの並べ替えにメモリを使用している場合のメモリ管理を最適化する[#2553](https://github.com/pingcap/tiflow/issues/2553)
        -   DDL 実行用の Prometheus メトリックを追加する[#2595](https://github.com/pingcap/tiflow/issues/2595) [#2669](https://github.com/pingcap/tiflow/issues/2669)
        -   メジャーまたはマイナー バージョン間での TiCDC クラスターの動作を禁止する[#2601](https://github.com/pingcap/tiflow/pull/2601)
        -   削除`file sorter` [#2325](https://github.com/pingcap/tiflow/pull/2325)
        -   changefeed が削除されたときに changefeed メトリックをクリーンアップし、プロセッサが終了したときにプロセッサ メトリックをクリーンアップします[#2156](https://github.com/pingcap/tiflow/issues/2156)
        -   リージョンが初期化された後にロック解決アルゴリズムを最適化する[#2188](https://github.com/pingcap/tiflow/issues/2188)

## バグの修正 {#bug-fixes}

-   TiDB

    -   範囲を構築するときに、バイナリ リテラルに対して照合順序が正しく設定されないバグを修正します[#23672](https://github.com/pingcap/tidb/issues/23672)

    -   クエリに`GROUP BY`と`UNION` [#26553](https://github.com/pingcap/tidb/pull/26553)両方が含まれている場合に発生する「範囲外のインデックス」エラーを修正します。

    -   TiKV にトゥームストーン ストアがある場合、TiDB がリクエストの送信に失敗する可能性がある問題を修正します[#23676](https://github.com/pingcap/tidb/issues/23676) [#24648](https://github.com/pingcap/tidb/issues/24648)

    -   文書化されていない`/debug/sub-optimal-plan` HTTP API [#27264](https://github.com/pingcap/tidb/pull/27264)を削除します

    -   式`case when`の間違った文字セットと照合順序の問題を修正します[#26662](https://github.com/pingcap/tidb/issues/26662)

-   TiKV

    -   データの復元中に TDE が有効になっていると、 BR が「ファイルが既に存在します」というエラーを報告する問題を修正します[#1179](https://github.com/pingcap/br/issues/1179)
    -   破損したスナップショット ファイルが原因で発生する可能性のあるディスクがいっぱいになる問題を修正します[#10813](https://github.com/tikv/tikv/issues/10813)
    -   TiKV が古いリージョンを頻繁に削除する問題を修正[#10680](https://github.com/tikv/tikv/issues/10680)
    -   TiKV が頻繁に PD クライアントに再接続する問題を修正[#9690](https://github.com/tikv/tikv/issues/9690)
    -   暗号化ファイル辞書から古いファイル情報を確認する[#9115](https://github.com/tikv/tikv/issues/9115)

-   PD

    -   PD が時間[#4077](https://github.com/tikv/pd/issues/4077)でダウンしたピアを修正しない問題を修正します。
    -   TiKV [#3868](https://github.com/tikv/pd/issues/3868)をスケールアウトすると PD がpanicになることがあるバグを修正

-   TiFlash

    -   TiFlash が複数のディスクに展開されている場合に発生する可能性のあるデータの不整合の問題を修正します。
    -   クエリに`CONSTANT` 、 `<` 、 `<=` 、 `>` 、 `>=` 、または`COLUMN`などのフィルターが含まれている場合に発生する誤った結果のバグを修正します
    -   負荷の高い書き込みでメトリクスのストア サイズが不正確になる問題を修正
    -   複数のディスクに展開されたときにTiFlash がデータを復元できないという潜在的なバグを修正します
    -   長時間実行した後、 TiFlash がデルタ データをガベージ コレクションできないという潜在的な問題を修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップとリストアの平均速度が不正確に計算されるバグを修正[#1405](https://github.com/pingcap/br/issues/1405)

    -   TiCDC

        -   統合テスト[#2422](https://github.com/pingcap/tiflow/issues/2422)で DDL ジョブの重複が発生した場合に発生する`ErrSchemaStorageTableMiss`エラーを修正します。
        -   `ErrGCTTLExceeded`エラーが発生するとチェンジフィードを削除できない不具合を修正[#2391](https://github.com/pingcap/tiflow/issues/2391)
        -   `capture list`コマンド[#2388](https://github.com/pingcap/tiflow/issues/2388)の出力に古いキャプチャが表示されることがある問題を修正します。
        -   TiCDC プロセッサ[#2017](https://github.com/pingcap/tiflow/pull/2017)のデッドロックの問題を修正します。
        -   このテーブルが再スケジュールされているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるために発生するデータの不整合の問題を修正します[#2230](https://github.com/pingcap/tiflow/issues/2230)
        -   メタデータ管理で`EtcdWorker`スナップショット分離に違反するバグを修正[#2557](https://github.com/pingcap/tiflow/pull/2557)
        -   DDL シンク エラー[#2552](https://github.com/pingcap/tiflow/issues/2552)により、変更フィードを停止できない問題を修正します。
        -   TiCDC Open Protocol の問題を修正: トランザクションに変更がない場合、TiCDC が空の値を出力する[#2612](https://github.com/pingcap/tiflow/issues/2612)
        -   unsigned `TINYINT` type [#2648](https://github.com/pingcap/tiflow/issues/2648)で TiCDC がpanicになるバグを修正
        -   TiCDC がキャプチャするリージョンが多すぎる場合に発生する OOM を回避するために、gRPC ウィンドウ サイズを小さくします[#2202](https://github.com/pingcap/tiflow/issues/2202)
        -   TiCDC がキャプチャするリージョンが多すぎる場合に発生する OOM の問題を修正します[#2673](https://github.com/pingcap/tiflow/issues/2673)
        -   `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar`などのデータ型を JSON にエンコードする際にプロセスpanicが発生する問題を修正[#2758](https://github.com/pingcap/tiflow/issues/2758)
        -   新しい変更フィード[#2389](https://github.com/pingcap/tiflow/issues/2389)を作成するときに発生する可能性があるメモリリークの問題を修正します。
        -   スキーマ変更[#2603](https://github.com/pingcap/tiflow/issues/2603)の終了 TS で変更フィードが開始されると、DDL 処理が失敗するバグを修正します。
        -   DDL ステートメントの実行時に所有者がクラッシュすると、DDL が失われる可能性がある問題を修正します[#1260](https://github.com/pingcap/tiflow/issues/1260)
        -   `SinkManager` [#2298](https://github.com/pingcap/tiflow/pull/2298)でマップへの安全でない同時アクセスの問題を修正
