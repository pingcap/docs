---
title: TiDB 5.2.2 Release Notes
---

# TiDB5.2.2リリースノート {#tidb-5-2-2-release-notes}

発売日：2021年10月29日

TiDBバージョン：5.2.2

## 改善 {#improvements}

-   TiDB

    -   コプロセッサーがロックに遭遇したときに、影響を受けるSQLステートメントをデバッグログに表示します。これは、問題の診断に役立ちます[＃27718](https://github.com/pingcap/tidb/issues/27718)
    -   SQL論理層[＃27247](https://github.com/pingcap/tidb/issues/27247)でデータをバックアップおよび復元するときに、バックアップおよび復元データのサイズを表示することをサポートします。

-   TiKV

    -   L0フロー制御のアルゴリズムを簡素化する[＃10879](https://github.com/tikv/tikv/issues/10879)
    -   ラフトクライアントモジュール[＃10983](https://github.com/tikv/tikv/pull/10983)のエラーログレポートを改善する
    -   ロギングスレッドを改善して、パフォーマンスのボトルネックにならないようにします[＃10841](https://github.com/tikv/tikv/issues/10841)
    -   書き込みクエリの統計タイプをさらに追加する[＃10507](https://github.com/tikv/tikv/issues/10507)

-   PD

    -   ホットスポットスケジューラのQPSディメンションにさらに多くの種類の書き込みクエリを追加する[＃3869](https://github.com/tikv/pd/issues/3869)
    -   スケジューラのパフォーマンスを向上させるために、バランス領域スケジューラの再試行制限を動的に調整することをサポートします[＃3744](https://github.com/tikv/pd/issues/3744)
    -   TiDBダッシュボードをv2021.10.08.1に更新します[＃4070](https://github.com/tikv/pd/pull/4070)
    -   エビクトリーダースケジューラが異常なピアのあるリージョンをスケジュールできることをサポートする[＃4093](https://github.com/tikv/pd/issues/4093)
    -   スケジューラーの終了プロセスを高速化する[＃4146](https://github.com/tikv/pd/issues/4146)

-   ツール

    -   TiCDC

        -   Kafkaシンク構成アイテム`MaxMessageBytes`のデフォルト値を64MBから1MBに減らして、大きなメッセージが[＃3104](https://github.com/pingcap/tiflow/pull/3104)によって拒否される問題を修正します。
        -   関係[＃2726](https://github.com/pingcap/tiflow/pull/2726) [＃3037](https://github.com/pingcap/tiflow/pull/3037)のメモリ使用量を削減する[＃2553](https://github.com/pingcap/tiflow/issues/2553)
        -   監視項目とアラートルールを最適化して、同期リンク、メモリGC、およびストックデータスキャンプロセスの可観測性を向上させます[＃2735](https://github.com/pingcap/tiflow/pull/2735) [＃1606](https://github.com/pingcap/tiflow/issues/1606) [＃3000](https://github.com/pingcap/tiflow/pull/3000) [＃2985](https://github.com/pingcap/tiflow/issues/2985) [＃2156](https://github.com/pingcap/tiflow/issues/2156)
        -   同期タスクのステータスが正常な場合、誤解を招くユーザーを避けるために、履歴エラーメッセージは表示されなくなります[＃2242](https://github.com/pingcap/tiflow/issues/2242)

## バグの修正 {#bug-fixes}

-   TiDB

    -   plan-cacheが符号なしフラグの変更を検出できない問題を修正します[＃28254](https://github.com/pingcap/tidb/issues/28254)
    -   パーティション関数が範囲[＃28233](https://github.com/pingcap/tidb/issues/28233)外にある場合の誤ったパーティションプルーニングを修正します
    -   プランナーが`join` 、場合によっては[＃28087](https://github.com/pingcap/tidb/issues/28087)の無効なプランをキャッシュする可能性がある問題を修正します
    -   ハッシュ列タイプが列挙型[＃27893](https://github.com/pingcap/tidb/issues/27893)の場合の誤ったインデックスハッシュ結合を修正
    -   まれに、アイドル状態の接続をリサイクルするとリクエストの送信がブロックされる可能性があるというバッチクライアントのバグを修正します[＃27688](https://github.com/pingcap/tidb/pull/27688)
    -   ターゲットクラスタでチェックサムを実行できない場合のTiDBLightningパニックの問題を修正します[＃27686](https://github.com/pingcap/tidb/pull/27686)
    -   場合によっては`date_add`と`date_sub`の関数の間違った結果を修正します[＃27232](https://github.com/pingcap/tidb/issues/27232)
    -   ベクトル化された式[＃28643](https://github.com/pingcap/tidb/issues/28643)の`hour`関数の誤った結果を修正します
    -   MySQL5.1または古いクライアントバージョン[＃27855](https://github.com/pingcap/tidb/issues/27855)に接続する際の認証の問題を修正します
    -   新しいインデックスが追加されたときに、指定された時間外に自動分析がトリガーされる可能性がある問題を修正します[＃28698](https://github.com/pingcap/tidb/issues/28698)
    -   セッション変数を設定すると`tidb_snapshot`が無効になるバグを修正し[＃28683](https://github.com/pingcap/tidb/pull/28683)
    -   ピア領域が多数欠落しているクラスターでBRが機能しないバグを修正します[＃27534](https://github.com/pingcap/tidb/issues/27534)
    -   サポートされていない`cast`がTiFlash5にプッシュダウンされたときの`tidb_cast to Int32 is not supported`などの予期しないエラーを修正し[＃23907](https://github.com/pingcap/tidb/issues/23907)
    -   `%s value is out of range in '%s'`エラーメッセージ[＃27964](https://github.com/pingcap/tidb/issues/27964)で`DECIMAL overflow`が欠落している問題を修正します。
    -   一部のコーナーケースでMPPノードの可用性検出が機能しないバグを修正します[＃3118](https://github.com/pingcap/tics/issues/3118)
    -   35を割り当てるときの`DATA RACE` [＃27952](https://github.com/pingcap/tidb/issues/27952)問題を修正し`MPP task ID`
    -   空の`dual table`を削除した後のMPPクエリの`INDEX OUT OF RANGE`エラーを修正します。 [＃28250](https://github.com/pingcap/tidb/issues/28250)
    -   MPPクエリ[＃1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラーログ`invalid cop task execution summaries length`の問題を修正します
    -   MPPクエリ[＃28149](https://github.com/pingcap/tidb/pull/28149)のエラーログ`cannot found column in Schema column`の問題を修正します
    -   TiFlashがシャットダウンしているときにTiDBがパニックになる可能性がある問題を修正します[＃28096](https://github.com/pingcap/tidb/issues/28096)
    -   安全でない3DES（トリプルデータ暗号化アルゴリズム）ベースのTLS暗号スイートのサポートを削除します[＃27859](https://github.com/pingcap/tidb/pull/27859)
    -   事前チェック中にLightningがオフラインのTiKVノードに接続し、インポートの失敗を引き起こす問題を修正します[＃27826](https://github.com/pingcap/tidb/pull/27826)
    -   多くのファイルをテーブルにインポートするときに事前チェックに時間がかかりすぎる問題を修正します[＃27605](https://github.com/pingcap/tidb/issues/27605)
    -   式を書き換えると、 `between`が間違った照合順序を推測する[＃27146](https://github.com/pingcap/tidb/issues/27146)という問題を修正します。
    -   `group_concat`の関数が照合順序[＃27429](https://github.com/pingcap/tidb/issues/27429)を考慮しなかった問題を修正します
    -   `extract`関数の引数が負の期間[＃27236](https://github.com/pingcap/tidb/issues/27236)である場合に発生する誤った結果を修正します
    -   `NO_UNSIGNED_SUBTRACTION`が設定されている場合にパーティションの作成が失敗する問題を修正します[＃26765](https://github.com/pingcap/tidb/issues/26765)
    -   列のプルーニングと集計のプッシュダウンで副作用のある式を避ける[＃27106](https://github.com/pingcap/tidb/issues/27106)
    -   不要なgRPCログを削除する[＃24190](https://github.com/pingcap/tidb/issues/24190)
    -   精度関連の問題を修正するには、有効な10進数の長さを制限してください[＃3091](https://github.com/pingcap/tics/issues/3091)
    -   `plus`式[＃26977](https://github.com/pingcap/tidb/issues/26977)のオーバーフローをチェックする間違った方法の問題を修正します
    -   `new collation`のデータを含むテーブルから統計をダンプするときの`data too long`のエラーの問題を修正します[＃27024](https://github.com/pingcap/tidb/issues/27024)
    -   再試行されたトランザクションのステートメントが[＃28670](https://github.com/pingcap/tidb/pull/28670)に含まれない問題を修正し`TIDB_TRX`

-   TiKV

    -   輻輳エラー[＃11082](https://github.com/tikv/tikv/issues/11082)が原因でCDCがスキャンの再試行を頻繁に追加する問題を修正します
    -   チャネルがいっぱいになるとラフト接続が切断される問題を修正します[＃11047](https://github.com/tikv/tikv/issues/11047)
    -   Raftクライアントの実装でバッチメッセージが大きすぎるという問題を修正します[＃9714](https://github.com/tikv/tikv/issues/9714)
    -   一部のコルーチンが[＃10965](https://github.com/tikv/tikv/issues/10965)でリークする問題を修正し`resolved_ts`
    -   応答のサイズが[＃9012](https://github.com/tikv/tikv/issues/9012)を超えたときにコプロセッサーに発生するパニックの問題を修正します。
    -   スナップショットファイルをガベージコレクションできない場合に、スナップショットガベージコレクション（GC）がGCスナップショットファイルを見逃す問題を修正します[＃10813](https://github.com/tikv/tikv/issues/10813)
    -   コプロセッサー要求を処理するときのタイムアウトによって引き起こされるパニックの問題を修正します[＃10852](https://github.com/tikv/tikv/issues/10852)

-   PD

    -   ピアの数が設定されたピアの数を超えているために、PDがデータを持ち保留状態のピアを誤って削除する問題を修正します[＃4045](https://github.com/tikv/pd/issues/4045)
    -   PDが時間内にピアを修正しないという問題を修正します[＃4077](https://github.com/tikv/pd/issues/4077)
    -   散布範囲スケジューラが空の領域をスケジュールできない問題を修正します[＃4118](https://github.com/tikv/pd/pull/4118)
    -   キーマネージャのCPUコストが高すぎるという問題を修正します[＃4071](https://github.com/tikv/pd/issues/4071)
    -   ホットリージョンスケジューラの構成を設定するときに発生する可能性のあるデータ競合の問題を修正します[＃4159](https://github.com/tikv/pd/issues/4159)
    -   スタックリージョンシンカー[＃3936](https://github.com/tikv/pd/issues/3936)によって引き起こされる遅いリーダー選出を修正

-   TiFlash

    -   ライブラリ`nsl`がないために、一部のプラットフォームでTiFlashが起動しない問題を修正します。

-   ツール

    -   TiCDC
        -   アップストリームTiDBインスタンスが予期せず終了したときにTiCDCレプリケーションタスクが終了する可能性がある問題を修正します[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKVが同じリージョン[＃2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDCプロセスがパニックになる可能性がある問題を修正します。
        -   ダウンストリームのTiDB/MySQLの可用性を確認する際の不要なCPU消費を修正[＃3073](https://github.com/pingcap/tiflow/issues/3073)
        -   TiCDCによって生成されるKafkaメッセージの量が[＃2962](https://github.com/pingcap/tiflow/issues/2962)によって制約されないという問題を修正し`max-message-size`
        -   Kafkaメッセージの書き込み中にエラーが発生したときにTiCDC同期タスクが一時停止する可能性がある問題を修正します[＃2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`が有効になっている場合、有効なインデックスのない一部のパーティションテーブルが無視される可能性がある問題を修正します[＃2834](https://github.com/pingcap/tiflow/issues/2834)
        -   ストックデータのスキャンに時間がかかりすぎると、TiKVがGCを実行するためにストックデータのスキャンが失敗する可能性がある問題を修正します[＃2470](https://github.com/pingcap/tiflow/issues/2470)
        -   一部のタイプの列をOpenProtocol形式にエンコードするときに発生する可能性のあるパニックの問題を修正します[＃2758](https://github.com/pingcap/tiflow/issues/2758)
        -   一部のタイプの列をAvro形式[＃2648](https://github.com/pingcap/tiflow/issues/2648)にエンコードするときに発生する可能性のあるパニックの問題を修正します

    -   TiDB Binlog

        -   ほとんどのテーブルが除外されると、特別な負荷がかかった状態でチェックポイントを更新できないという問題を修正します[＃1075](https://github.com/pingcap/tidb-binlog/pull/1075)
