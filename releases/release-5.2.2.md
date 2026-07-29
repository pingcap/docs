---
title: TiDB 5.2.2 Release Notes
summary: TiDB 5.2.2は2021年10月29日にリリースされました。このリリースには、TiDB、TiKV、PD、TiCDC、 TiFlash、TiDB Binlogのさまざまな改善とバグ修正が含まれています。改善点には、影響を受けるSQL文をデバッグログに表示すること、バックアップと復元のデータサイズの表示のサポートなどが含まれます。バグ修正では、プランキャッシュの検出、誤ったパーティション関数、クエリ関数、クライアント接続、データレプリケーションに関連するその他のさまざまな問題に対処しています。
---

# TiDB 5.2.2 リリースノート {#tidb-5-2-2-release-notes}

リリース日：2021年10月29日

TiDB バージョン: 5.2.2

## 改善点 {#improvements}

-   TiDB

    -   コプロセッサがロックに遭遇したときに影響を受けるSQL文をデバッグログに表示します。これは問題の診断に役立ちます[＃27718](https://github.com/pingcap/tidb/issues/27718)
    -   SQL論理レイヤーでデータをバックアップおよび復元するときに、バックアップおよび復元データのサイズを表示する機能をサポート [＃27247](https://github.com/pingcap/tidb/issues/27247)

-   TiKV

    -   L0フロー制御のアルゴリズムを簡素化する [＃10879](https://github.com/tikv/tikv/issues/10879)
    -   ラフトクライアントモジュールのエラーログレポートを改善 [＃10983](https://github.com/tikv/tikv/pull/10983)
    -   パフォーマンスのボトルネックにならないようにログスレッドを改善する[＃10841](https://github.com/tikv/tikv/issues/10841)
    -   書き込みクエリの統計タイプを追加する[＃10507](https://github.com/tikv/tikv/issues/10507)

-   PD

    -   ホットスポット スケジューラの QPS ディメンションに書き込みクエリの種類を追加する [＃3869](https://github.com/tikv/pd/issues/3869)
    -   バランスリージョンスケジューラの再試行制限を動的に調整して、スケジューラのパフォーマンスを向上させることをサポートしました。 [＃3744](https://github.com/tikv/pd/issues/3744)
    -   TiDB Dashboardをv2021.10.08.1 に更新 [＃4070](https://github.com/tikv/pd/pull/4070)
    -   退去リーダースケジューラが不健全なピアを持つリージョンをスケジュールできるようにサポート[＃4093](https://github.com/tikv/pd/issues/4093)
    -   スケジューラの終了プロセスを高速化 [＃4146](https://github.com/tikv/pd/issues/4146)

-   ツール

    -   TiCDC

        -   Kafka シンク構成項目`MaxMessageBytes`のデフォルト値を 64 MB から 1 MB に減らし、大きなメッセージが Kafka ブローカーによって拒否される問題を修正しました。 [＃3104](https://github.com/pingcap/tiflow/pull/3104)
        -   レプリケーションパイプラインのメモリ使用量を削減する[＃2553](https://github.com/pingcap/tiflow/issues/2553) [＃3037](https://github.com/pingcap/tiflow/pull/3037) [＃2726](https://github.com/pingcap/tiflow/pull/2726)
        -   監視項目とアラートルールを最適化して、同期リンク、メモリGC、在庫データスキャンプロセスの可観測性を向上させる[＃2735](https://github.com/pingcap/tiflow/pull/2735) [＃1606](https://github.com/pingcap/tiflow/issues/1606) [＃3000](https://github.com/pingcap/tiflow/pull/3000) [＃2985](https://github.com/pingcap/tiflow/issues/2985) [＃2156](https://github.com/pingcap/tiflow/issues/2156)
        -   同期タスクのステータスが正常であれば、ユーザーの誤解を避けるために過去のエラーメッセージは表示されなくなります[＃2242](https://github.com/pingcap/tiflow/issues/2242)

## バグ修正 {#bug-fixes}

-   TiDB

    -   プランキャッシュが未署名フラグの変更を検出できない問題を修正[＃28254](https://github.com/pingcap/tidb/issues/28254)
    -   パーティション関数が範囲外の場合の誤ったパーティションプルーニングを修正[＃28233](https://github.com/pingcap/tidb/issues/28233)
    -   プランナーが`join`の無効なプランをキャッシュする可能性がある問題を修正しました[＃28087](https://github.com/pingcap/tidb/issues/28087)
    -   ハッシュ列の型が列挙型場合の間違ったインデックス ハッシュ結合を修正しました [＃27893](https://github.com/pingcap/tidb/issues/27893)
    -   アイドル接続をリサイクルすると、まれにリクエストの送信がブロックされる可能性があるバッチクライアントのバグを修正しました[＃27688](https://github.com/pingcap/tidb/pull/27688)
    -   ターゲット クラスタでチェックサムの実行に失敗した場合のTiDB Lightning panic問題を修正しました。 [＃27686](https://github.com/pingcap/tidb/pull/27686)
    -   いくつかのケースで`date_add`と`date_sub`関数の誤った結果を修正[＃27232](https://github.com/pingcap/tidb/issues/27232)
    -   ベクトル化された式の関数`hour`の誤った結果を修正します [＃28643](https://github.com/pingcap/tidb/issues/28643)
    -   MySQL 5.1またはそれ以前のクライアントバージョンに接続する際の認証問題を修正 [＃27855](https://github.com/pingcap/tidb/issues/27855)
    -   新しいインデックスが追加されたときに、指定された時間外にauto analyzeがトリガーされる可能性がある問題を修正しました[＃28698](https://github.com/pingcap/tidb/issues/28698)
    -   セッション変数を設定すると`tidb_snapshot` が無効になるバグを修正 [＃28683](https://github.com/pingcap/tidb/pull/28683)
    -   ピアが見つからないリージョンが多数あるクラスタでBRが機能しないバグを修正[＃27534](https://github.com/pingcap/tidb/issues/27534)
    -   サポートされていない`cast` TiFlash にプッシュダウンされたときに発生する`tidb_cast to Int32 is not supported`ような予期しないエラーを修正しました [＃23907](https://github.com/pingcap/tidb/issues/23907)
    -   `%s value is out of range in '%s'`エラーメッセージに`DECIMAL overflow`が欠落している問題を修正 [＃27964](https://github.com/pingcap/tidb/issues/27964)
    -   MPPノードの可用性検出が一部のコーナーケースで機能しないバグを修正[＃3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` を割り当てる際の`DATA RACE`問題を修正 [＃27952](https://github.com/pingcap/tidb/issues/27952)
    -   空の`dual table`を削除した後の MPP クエリの`INDEX OUT OF RANGE`エラーを修正します[＃28250](https://github.com/pingcap/tidb/issues/28250)
    -   MPPクエリの誤検知エラーログ`invalid cop task execution summaries length`の問題を修正 [＃1791](https://github.com/pingcap/tics/issues/1791)
    -   MPPクエリのエラーログ`cannot found column in Schema column`の問題を修正 [＃28149](https://github.com/pingcap/tidb/pull/28149)
    -   TiFlashがシャットダウンするときに TiDB がpanicする可能性がある問題を修正[＃28096](https://github.com/pingcap/tidb/issues/28096)
    -   安全でない3DES（トリプルデータ暗号化アルゴリズム）ベースのTLS暗号スイートサポートを削除します [＃27859](https://github.com/pingcap/tidb/pull/27859)
    -   Lightning が事前チェック中にオフラインの TiKV ノードに接続し、インポートが失敗する問題を修正しました[＃27826](https://github.com/pingcap/tidb/pull/27826)
    -   多数のファイルをテーブルにインポートするときに事前チェックに時間がかかりすぎる問題を修正しました [＃27605](https://github.com/pingcap/tidb/issues/27605)
    -   式を書き換えると間違った照合順序が推測される問題を修正`between` [＃27146](https://github.com/pingcap/tidb/issues/27146)
    -   `group_concat`関数が照合順序を考慮していなかった問題を修正[＃27429](https://github.com/pingcap/tidb/issues/27429)
    -   `extract`関数の引数が負の期間場合に発生する結果の誤りを修正 [＃27236](https://github.com/pingcap/tidb/issues/27236)
    -   `NO_UNSIGNED_SUBTRACTION` 設定されている場合にパーティションの作成が失敗する問題を修正 [＃26765](https://github.com/pingcap/tidb/issues/26765)
    -   列プルーニングと集計プッシュダウンで副作用のある式を避ける [＃27106](https://github.com/pingcap/tidb/issues/27106)
    -   不要なgRPCログを削除する[＃24190](https://github.com/pingcap/tidb/issues/24190)
    -   有効な小数点以下の桁数を制限することで精度関連の問題を修正する[＃3091](https://github.com/pingcap/tics/issues/3091)
    -   `plus`式のオーバーフローをチェックする間違った方法の問題を修正 [＃26977](https://github.com/pingcap/tidb/issues/26977)
    -   `new collation`データをテーブルから統計をダンプするときに`data too long`のエラーが発生する問題を修正しました。 [＃27024](https://github.com/pingcap/tidb/issues/27024)
    -   再試行されたトランザクションのステートメントが`TIDB_TRX` に含まれない問題を修正 [＃28670](https://github.com/pingcap/tidb/pull/28670)

-   TiKV

    -   輻輳エラーによりCDCがスキャン再試行を頻繁に追加する問題を修正 [＃11082](https://github.com/tikv/tikv/issues/11082)
    -   チャネルがいっぱいになるとラフト接続が切断される問題を修正[＃11047](https://github.com/tikv/tikv/issues/11047)
    -   Raftクライアント実装でバッチメッセージが大きすぎる問題を修正 [＃9714](https://github.com/tikv/tikv/issues/9714)
    -   `resolved_ts` で一部のコルーチンがリークする問題を修正 [＃10965](https://github.com/tikv/tikv/issues/10965)
    -   応答サイズが4GiBを超えるとコプロセッサに発生するpanic問題を修正[＃9012](https://github.com/tikv/tikv/issues/9012)
    -   スナップショット ファイルがガベージ コレクションできない場合に、スナップショット ガベージ コレクション (GC) で GC スナップショット ファイルが失われる問題を修正しました[＃10813](https://github.com/tikv/tikv/issues/10813)
    -   コプロセッサー要求の処理中にタイムアウトによって発生するpanic問題を修正[＃10852](https://github.com/tikv/tikv/issues/10852)

-   PD

    -   ピア数が設定されたピア数を超えたために、PD がデータがあり保留中の状態のピアを誤って削除する問題を修正しました。 [＃4045](https://github.com/tikv/pd/issues/4045)
    -   PDが時間内にピアを修正しない問題を修正[＃4077](https://github.com/tikv/pd/issues/4077)
    -   散布範囲スケジューラが空のリージョンをスケジュールできない問題を修正[＃4118](https://github.com/tikv/pd/pull/4118)
    -   キーマネージャのCPU使用率が高すぎる問題を修正[＃4071](https://github.com/tikv/pd/issues/4071)
    -   ホットリージョンスケジューラの設定時に発生する可能性のあるデータ競合の問題を修正しました。 [＃4159](https://github.com/tikv/pd/issues/4159)
    -   リージョン同期が停止したことによるリーダー選出の遅延を修正[＃3936](https://github.com/tikv/pd/issues/3936)

-   TiFlash

    -   ライブラリ`nsl`がないため、一部のプラットフォームでTiFlashが起動に失敗する問題を修正しました。

-   ツール

    -   TiCDC
        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正しました[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKVが同じリージョンに重複したリクエストを送信した場合にTiCDCプロセスがpanicする可能性がある問題を修正しました [＃2386](https://github.com/pingcap/tiflow/issues/2386)
        -   下流の TiDB/MySQL の可用性を検証する際の不要な CPU 消費を修正[＃3073](https://github.com/pingcap/tiflow/issues/3073)
        -   TiCDCによって生成されるKafkaメッセージの量が`max-message-size` に制限されない問題を修正 [＃2962](https://github.com/pingcap/tiflow/issues/2962)
        -   Kafka メッセージの書き込み中にエラーが発生すると TiCDC 同期タスクが一時停止する可能性がある問題を修正[＃2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`有効になっているときに、有効なインデックスのない一部のパーティションテーブルが無視される可能性がある問題を修正[＃2834](https://github.com/pingcap/tiflow/issues/2834)
        -   株価データのスキャンに時間がかかりすぎると、TiKV が GC を実行するため株価データのスキャンが失敗する可能性がある問題を修正しました[＃2470](https://github.com/pingcap/tiflow/issues/2470)
        -   一部のタイプの列を Open Protocol 形式にエンコードするときに発生する可能性のあるpanic問題を修正しました。 [＃2758](https://github.com/pingcap/tiflow/issues/2758)
        -   一部のタイプの列をAvro形式にエンコードする際に発生する可能性のあるpanic問題を修正しました [＃2648](https://github.com/pingcap/tiflow/issues/2648)

    -   TiDB Binlog

        -   ほとんどのテーブルがフィルタリングされると、特定の負荷でチェックポイントを更新できない問題を修正しました。 [＃1075](https://github.com/pingcap/tidb-binlog/pull/1075)
