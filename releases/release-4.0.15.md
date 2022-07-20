---
title: TiDB 4.0.15 Release Notes
---

# TiDB4.0.15リリースノート {#tidb-4-0-15-release-notes}

リリース日：2021年9月27日

TiDBバージョン：4.0.15

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   新しいセッションで`SHOW VARIABLES`を実行すると時間がかかる問題を修正します。この修正により、 [＃21045](https://github.com/pingcap/tidb/pull/21045)で行われたいくつかの変更が元に戻され、互換性の問題が発生する可能性があります。 [＃24326](https://github.com/pingcap/tidb/issues/24326)

    <!---->

    -   次のバグ修正により、実行結果が変更され、アップグレードの非互換性が発生する可能性があります。
        -   `greatest(datetime) union null`が空の文字列[＃26532](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正します
        -   `having`句が正しく機能しない可能性がある問題を修正します[＃26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の周りの照合が異なる場合に発生する誤った実行結果を修正します[＃27146](https://github.com/pingcap/tidb/issues/27146)
        -   `extract`関数の引数が負の期間[＃27236](https://github.com/pingcap/tidb/issues/27236)である場合に発生する誤った結果を修正します
        -   `group_concat`関数の列に非ビン照合順序が含まれている場合に発生する誤った実行結果を修正します[＃27429](https://github.com/pingcap/tidb/issues/27429)
        -   `Apply`演算子を[＃27233](https://github.com/pingcap/tidb/issues/27233)に変換するときに列情報が失われる問題を修正し`Join`
        -   無効な文字列を`DATE`にキャストしたときの[＃26762](https://github.com/pingcap/tidb/issues/26762)しない動作の問題を修正しました
        -   新しい照合順序を有効にすると、複数の列の`count distinct`の結果が間違っているというバグを修正します[＃27091](https://github.com/pingcap/tidb/issues/27091)

## 機能強化 {#feature-enhancement}

-   TiKV

    -   TiCDC構成の動的な変更をサポート[＃10645](https://github.com/tikv/tikv/issues/10645)

## 改善 {#improvements}

-   TiDB

    -   ヒストグラムの行数に基づいて自動分析をトリガーする[＃24237](https://github.com/pingcap/tidb/issues/24237)

-   TiKV

    -   読み取りの待ち時間を短縮するために、読み取り準備と書き込み準備を別々に処理します[＃10475](https://github.com/tikv/tikv/issues/10475)
    -   TiKVコプロセッサーの遅いログは、要求の処理に費やされた時間のみを考慮します。 [＃10841](https://github.com/tikv/tikv/issues/10841)
    -   sloggerスレッドが過負荷になり、キューがいっぱいになったときにスレッドをブロックする代わりにログをドロップする[＃10841](https://github.com/tikv/tikv/issues/10841)
    -   解決されたTSメッセージのサイズを減らして、ネットワーク帯域幅を節約します[＃2448](https://github.com/pingcap/tiflow/issues/2448)

-   PD

    -   PD間でリージョン情報を同期するパフォーマンスを向上させる[＃3932](https://github.com/tikv/pd/pull/3932)

-   ツール

    -   バックアップと復元（BR）

        -   リージョンを同時に分割および分散して、復元速度を向上させる[＃1363](https://github.com/pingcap/br/pull/1363)
        -   PD要求エラーまたはTiKVI/Oタイムアウトエラーが発生したときにBRタスクを再試行します[＃27787](https://github.com/pingcap/tidb/issues/27787)
        -   復元後のクラスタ操作に影響を与えないように、多数の小さなテーブルを復元するときに空のリージョンを減らします[＃1374](https://github.com/pingcap/br/issues/1374)
        -   テーブルの作成中に`rebase auto id`の操作を実行すると、個別の`rebase auto id`のDDL操作が保存され、復元[＃1424](https://github.com/pingcap/br/pull/1424)が高速化されます。

    -   Dumpling

        -   `SHOW TABLE STATUS` [＃337](https://github.com/pingcap/dumpling/pull/337)のフィルタリング効率を向上させるために、テーブル情報を取得する前にスキップされたデータベースをフィルタリングします。
        -   一部のMySQLバージョン[＃322](https://github.com/pingcap/dumpling/issues/322)では`SHOW TABLE STATUS`が正しく機能しないため、 `SHOW FULL TABLES`を使用してエクスポートするテーブルのテーブル情報を取得します。
        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`構文をサポートしないMySQL互換データベースのバックアップをサポートする[＃309](https://github.com/pingcap/dumpling/issues/309)
        -   ダンプが失敗するという誤解を招く情報を回避するために、Dumpling警告ログを調整します[＃340](https://github.com/pingcap/dumpling/pull/340)

    -   TiDB Lightning

        -   式インデックスまたは仮想生成列に依存するインデックスを持つテーブルへのデータのインポートをサポート[＃1404](https://github.com/pingcap/br/issues/1404)

    -   TiCDC

        -   使いやすさを向上させるために、常に内部でTiKVから古い値を取得します[＃2397](https://github.com/pingcap/tiflow/pull/2397)
        -   テーブルのリージョンがすべてTiKVノードから転送される場合のゴルーチンの使用量を減らします[＃2284](https://github.com/pingcap/tiflow/issues/2284)
        -   同時実行性が高い場合に、ワーカープールを最適化してゴルーチンを減らします[＃2211](https://github.com/pingcap/tiflow/issues/2211)
        -   他のチェンジフィードに影響を与えないように、DDLステートメントを非同期で実行します[＃2295](https://github.com/pingcap/tiflow/issues/2295)
        -   グローバルgRPC接続プールを追加し、KVクライアント間でgRPC接続を共有します[＃2531](https://github.com/pingcap/tiflow/pull/2531)
        -   回復不能なDMLエラーで迅速に失敗する[＃1724](https://github.com/pingcap/tiflow/issues/1724)
        -   ユニファイドソーターがメモリを使用してデータを並べ替えるときにメモリ管理を最適化する[＃2553](https://github.com/pingcap/tiflow/issues/2553)
        -   DDL実行の[＃2669](https://github.com/pingcap/tiflow/issues/2669)メトリックを追加する[＃2595](https://github.com/pingcap/tiflow/issues/2595)
        -   メジャーバージョンまたはマイナーバージョン間でのTiCDCクラスターの運用を禁止する[＃2601](https://github.com/pingcap/tiflow/pull/2601)
        -   [＃2325](https://github.com/pingcap/tiflow/pull/2325)を削除し`file sorter`
        -   チェンジフィードが削除されたときにチェンジフィードメトリックをクリーンアップし、プロセッサが終了したときにプロセッサメトリックをクリーンアップします[＃2156](https://github.com/pingcap/tiflow/issues/2156)
        -   リージョンが初期化された後、ロック解決アルゴリズムを最適化する[＃2188](https://github.com/pingcap/tiflow/issues/2188)

## バグの修正 {#bug-fixes}

-   TiDB

    -   範囲[＃23672](https://github.com/pingcap/tidb/issues/23672)を構築するときに、バイナリリテラルに対して照合順序が正しく設定されないバグを修正します。

    -   クエリに`GROUP BY`と[＃26553](https://github.com/pingcap/tidb/pull/26553)の両方が含まれている場合に発生する「インデックスが範囲外」エラーを修正し`UNION`

    -   TiKVにトゥームストーンストアがある場合、TiDBがリクエストを送信できない可能性がある問題を修正します[＃23676](https://github.com/pingcap/tidb/issues/23676) [＃24648](https://github.com/pingcap/tidb/issues/24648)

    -   文書化されていない`/debug/sub-optimal-plan`を削除し[＃27264](https://github.com/pingcap/tidb/pull/27264)

    -   `case when`式[＃26662](https://github.com/pingcap/tidb/issues/26662)の間違った文字セットと照合順序の問題を修正しました

-   TiKV

    -   データの復元中にTDEが有効になっている場合に、BRが「ファイルはすでに存在します」というエラーを報告する問題を修正します[＃1179](https://github.com/pingcap/br/issues/1179)
    -   破損したスナップショットファイルによって引き起こされる潜在的なディスクフルの問題を修正する[＃10813](https://github.com/tikv/tikv/issues/10813)
    -   TiKVが古いリージョンを頻繁に削除する問題を修正します[＃10680](https://github.com/tikv/tikv/issues/10680)
    -   TiKVがPDクライアントを頻繁に再接続する問題を修正します[＃9690](https://github.com/tikv/tikv/issues/9690)
    -   暗号化ファイル辞書から古いファイル情報を確認する[＃9115](https://github.com/tikv/tikv/issues/9115)

-   PD

    -   PDが時間内にダウンピアを修正しないという問題を修正します[＃4077](https://github.com/tikv/pd/issues/4077)
    -   TiKV1をスケールアウトするときにPDがpanicになる可能性があるバグを修正し[＃3868](https://github.com/tikv/pd/issues/3868)

-   TiFlash

    -   TiFlashが複数のディスクに展開されているときに発生するデータの不整合の潜在的な問題を修正します
    -   `<=`に`CONSTANT`などの`>`が含まれている場合に発生する`COLUMN`た結果の`>=`を修正し`<`
    -   大量の書き込みの下でメトリックのストアサイズが不正確になる問題を修正します
    -   複数のディスクにデプロイしたときにTiFlashがデータを復元できない潜在的なバグを修正します
    -   TiFlashが長時間実行した後にデルタデータをガベージコレクションできないという潜在的な問題を修正します

-   ツール

    -   バックアップと復元（BR）

        -   バックアップと復元の平均速度が不正確に計算されるバグを修正します[＃1405](https://github.com/pingcap/br/issues/1405)

    -   TiCDC

        -   統合テスト[＃2422](https://github.com/pingcap/tiflow/issues/2422)でDDLジョブの重複が発生したときに発生する`ErrSchemaStorageTableMiss`のエラーを修正します。
        -   `ErrGCTTLExceeded`エラーが発生した場合にチェンジフィードを削除できないバグを修正します[＃2391](https://github.com/pingcap/tiflow/issues/2391)
        -   `capture list`コマンドの出力に古いキャプチャが表示される可能性がある問題を修正します[＃2388](https://github.com/pingcap/tiflow/issues/2388)
        -   TiCDCプロセッサ[＃2017](https://github.com/pingcap/tiflow/pull/2017)のデッドロックの問題を修正します
        -   このテーブルが再スケジュールされているときに複数のプロセッサが同じテーブルにデータを書き込む可能性があるために発生するデータの不整合の問題を修正します[＃2230](https://github.com/pingcap/tiflow/issues/2230)
        -   メタデータ管理[＃2557](https://github.com/pingcap/tiflow/pull/2557)で`EtcdWorker`スナップショットアイソレーションに違反するバグを修正します
        -   DDLシンクエラー[＃2552](https://github.com/pingcap/tiflow/issues/2552)が原因でチェンジフィードを停止できない問題を修正します
        -   TiCDCオープンプロトコルの問題を修正します。トランザクション[＃2612](https://github.com/pingcap/tiflow/issues/2612)に変更がない場合、TiCDCは空の値を出力します。
        -   符号なし`TINYINT`タイプ[＃2648](https://github.com/pingcap/tiflow/issues/2648)でTiCDCがpanicになるバグを修正します
        -   TiCDCがあまりにも多くのリージョンをキャプチャするときに発生するOOMを回避するために、gRPCウィンドウサイズを小さくします[＃2202](https://github.com/pingcap/tiflow/issues/2202)
        -   TiCDCがキャプチャするリージョンが多すぎる場合に発生するOOMの問題を修正します[＃2673](https://github.com/pingcap/tiflow/issues/2673)
        -   `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar`などのデータ型をJSON3にエンコードするときに発生するプロセスpanicの問題を修正し[＃2758](https://github.com/pingcap/tiflow/issues/2758)
        -   新しいチェンジフィードを作成するときに発生する可能性のあるメモリリークの問題を修正します[＃2389](https://github.com/pingcap/tiflow/issues/2389)
        -   スキーマ変更の終了TSで変更フィードが開始されたときにDDL処理が失敗するバグを修正します[＃2603](https://github.com/pingcap/tiflow/issues/2603)
        -   DDLステートメントの実行時に所有者がクラッシュした場合の潜在的なDDL損失の問題を修正します[＃1260](https://github.com/pingcap/tiflow/issues/1260)
        -   [＃2298](https://github.com/pingcap/tiflow/pull/2298)のマップへの安全でない同時アクセスの問題を修正し`SinkManager`
