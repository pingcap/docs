---
title: TiDB 5.2.2 Release Notes
---

# TiDB 5.2.2 リリースノート {#tidb-5-2-2-release-notes}

リリース日：2021年10月29日

TiDB バージョン: 5.2.2

## 改善点 {#improvements}

-   TiDB

    -   コプロセッサーがロックを検出したときに、影響を受ける SQL ステートメントをデバッグ ログに表示します。これは、問題の診断に役立ちます[#27718](https://github.com/pingcap/tidb/issues/27718)
    -   SQL 論理レイヤー[#27247](https://github.com/pingcap/tidb/issues/27247)でデータをバックアップおよび復元する際のバックアップおよび復元データのサイズの表示のサポート

-   TiKV

    -   L0フロー制御のアルゴリズムを簡略化[#10879](https://github.com/tikv/tikv/issues/10879)
    -   raft クライアント モジュール[#10983](https://github.com/tikv/tikv/pull/10983)のエラー ログ レポートを改善しました。
    -   ロギング スレッドがパフォーマンスのボトルネックになるのを回避するために、スレッドを改善します[#10841](https://github.com/tikv/tikv/issues/10841)
    -   書き込みクエリの統計タイプをさらに追加[#10507](https://github.com/tikv/tikv/issues/10507)

-   PD

    -   ホットスポット スケジューラ[#3869](https://github.com/tikv/pd/issues/3869)の QPS ディメンションにさらに多くの種類の書き込みクエリを追加します。
    -   バランス領域スケジューラの再試行制限を動的に調整して、スケジューラのパフォーマンスを向上させるサポート[#3744](https://github.com/tikv/pd/issues/3744)
    -   TiDB ダッシュボードを v2021.10.08.1 に更新します[#4070](https://github.com/tikv/pd/pull/4070)
    -   エビクト リーダー スケジューラが異常なピアのあるリージョンをスケジュールできることのサポート[#4093](https://github.com/tikv/pd/issues/4093)
    -   スケジューラの終了プロセスを高速化[#4146](https://github.com/tikv/pd/issues/4146)

-   ツール

    -   TiCDC

        -   Kafka シンク構成項目`MaxMessageBytes`のデフォルト値を 64 MB から 1 MB に減らし、大きなメッセージが Kafka ブローカーによって拒否される問題を修正します[#3104](https://github.com/pingcap/tiflow/pull/3104)
        -   再複製パイプラインでのメモリ使用量を削減する[#2553](https://github.com/pingcap/tiflow/issues/2553) [#3037](https://github.com/pingcap/tiflow/pull/3037) [#2726](https://github.com/pingcap/tiflow/pull/2726)
        -   監視項目とアラートルールを最適化し、同期リンク、メモリGC、ストックデータスキャン処理の可観測性を向上[#2735](https://github.com/pingcap/tiflow/pull/2735) [#1606](https://github.com/pingcap/tiflow/issues/1606) [#3000](https://github.com/pingcap/tiflow/pull/3000) [#2985](https://github.com/pingcap/tiflow/issues/2985) [#2156](https://github.com/pingcap/tiflow/issues/2156)
        -   同期タスクのステータスが正常な場合、ユーザーの誤解を避けるために、履歴エラー メッセージは表示されません[#2242](https://github.com/pingcap/tiflow/issues/2242)

## バグの修正 {#bug-fixes}

-   TiDB

    -   plan-cache が未署名フラグの変更を検出できない問題を修正[#28254](https://github.com/pingcap/tidb/issues/28254)
    -   パーティション関数が範囲[#28233](https://github.com/pingcap/tidb/issues/28233)の外にある場合の間違ったパーティション プルーニングを修正しました。
    -   場合によってはプランナーが`join`の無効なプランをキャッシュする可能性がある問題を修正します[#28087](https://github.com/pingcap/tidb/issues/28087)
    -   ハッシュ列タイプが enum [#27893](https://github.com/pingcap/tidb/issues/27893)の場合の間違ったインデックス ハッシュ結合を修正
    -   アイドル状態の接続をリサイクルすると、まれにリクエストの送信がブロックされる可能性があるというバッチ クライアントのバグを修正しました[#27688](https://github.com/pingcap/tidb/pull/27688)
    -   ターゲット クラスターでのチェックサムの実行に失敗した場合のTiDB Lightningpanicの問題を修正します[#27686](https://github.com/pingcap/tidb/pull/27686)
    -   場合によっては`date_add`と`date_sub`関数の間違った結果を修正する[#27232](https://github.com/pingcap/tidb/issues/27232)
    -   ベクトル化された式[#28643](https://github.com/pingcap/tidb/issues/28643)の関数`hour`の誤った結果を修正しました。
    -   MySQL 5.1 または古いクライアント バージョン[#27855](https://github.com/pingcap/tidb/issues/27855)に接続するときの認証の問題を修正
    -   新しいインデックスが追加されると、auto analyzeが指定された時間外にトリガーされる場合がある問題を修正します[#28698](https://github.com/pingcap/tidb/issues/28698)
    -   セッション変数を設定すると`tidb_snapshot` [#28683](https://github.com/pingcap/tidb/pull/28683)が無効になるバグを修正
    -   ピア領域が多数欠落しているクラスターではBRが機能しないバグを修正[#27534](https://github.com/pingcap/tidb/issues/27534)
    -   サポートされていない`cast` TiFlash [#23907](https://github.com/pingcap/tidb/issues/23907)にプッシュダウンされた場合の`tidb_cast to Int32 is not supported`のような予期しないエラーを修正
    -   `%s value is out of range in '%s'`エラーメッセージ[#27964](https://github.com/pingcap/tidb/issues/27964)に`DECIMAL overflow`が欠落している問題を修正
    -   MPP ノードの可用性検出が一部の特殊なケースで機能しないバグを修正[#3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)を割り当てるときの`DATA RACE`問題を修正
    -   空`dual table`削除した後の MPP クエリの`INDEX OUT OF RANGE`エラーを修正します。 [#28250](https://github.com/pingcap/tidb/issues/28250)
    -   MPP クエリ[#1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラー ログ`invalid cop task execution summaries length`の問題を修正します。
    -   MPP クエリ[#28149](https://github.com/pingcap/tidb/pull/28149)のエラー ログ`cannot found column in Schema column`の問題を修正
    -   TiFlashのシャットダウン時に TiDB がpanicになる問題を修正[#28096](https://github.com/pingcap/tidb/issues/28096)
    -   安全でない 3DES (トリプル データ暗号化アルゴリズム) ベースの TLS 暗号スイートのサポートを削除します[#27859](https://github.com/pingcap/tidb/pull/27859)
    -   Lightning が事前チェック中にオフライン TiKV ノードに接続し、インポート失敗が発生する問題を修正します[#27826](https://github.com/pingcap/tidb/pull/27826)
    -   多数のファイルをテーブル[#27605](https://github.com/pingcap/tidb/issues/27605)にインポートする場合、事前チェックに時間がかかりすぎる問題を修正
    -   式を書き換えると`between`間違った照合順序が推測される[#27146](https://github.com/pingcap/tidb/issues/27146)という問題を修正します。
    -   `group_concat`関数が照合順序を考慮していない問題を修正[#27429](https://github.com/pingcap/tidb/issues/27429)
    -   `extract`関数の引数が負の持続時間の場合に発生する結果が間違っていたのを修正[#27236](https://github.com/pingcap/tidb/issues/27236)
    -   `NO_UNSIGNED_SUBTRACTION`を[#26765](https://github.com/pingcap/tidb/issues/26765)に設定するとパーティションの作成に失敗する問題を修正
    -   列のプルーニングと集計プッシュダウンで副作用のある式を回避する[#27106](https://github.com/pingcap/tidb/issues/27106)
    -   不要な gRPC ログを削除する[#24190](https://github.com/pingcap/tidb/issues/24190)
    -   有効な 10 進数の長さを制限して、精度関連の問題を修正します[#3091](https://github.com/pingcap/tics/issues/3091)
    -   `plus`式[#26977](https://github.com/pingcap/tidb/issues/26977)のオーバーフローをチェックする間違った方法の問題を修正
    -   `new collation`データ[#27024](https://github.com/pingcap/tidb/issues/27024)を持つテーブルから統計をダンプするときに`data too long`エラーが発生する問題を修正
    -   リトライしたトランザクションのステートメントが`TIDB_TRX` [#28670](https://github.com/pingcap/tidb/pull/28670)に含まれない問題を修正

-   TiKV

    -   輻輳エラー[#11082](https://github.com/tikv/tikv/issues/11082)が原因で CDC がスキャンの再試行を頻繁に追加する問題を修正します。
    -   チャンネルがいっぱいの場合、Raft 接続が切断される問題を修正[#11047](https://github.com/tikv/tikv/issues/11047)
    -   Raftクライアント実装[#9714](https://github.com/tikv/tikv/issues/9714)でバッチメッセージが大きすぎる問題を修正
    -   `resolved_ts` [#10965](https://github.com/tikv/tikv/issues/10965)で一部のコルーチンがリークする問題を修正
    -   応答のサイズが 4 GiB を超えるとコプロセッサに発生するpanicの問題を修正します[#9012](https://github.com/tikv/tikv/issues/9012)
    -   スナップショット ファイルをガベージ コレクションできない場合、スナップショット ガベージ コレクション (GC) で GC スナップショット ファイルが失われる問題を修正します[#10813](https://github.com/tikv/tikv/issues/10813)
    -   コプロセッサーリクエストの処理時にタイムアウトが原因で発生するpanicの問題を修正[#10852](https://github.com/tikv/tikv/issues/10852)

-   PD

    -   ピアの数が設定されたピアの数を超えているため、PD がデータを持ち保留ステータスのピアを誤って削除する問題を修正します[#4045](https://github.com/tikv/pd/issues/4045)
    -   PD がダウンしたピアを時間内に修正しない問題を修正します[#4077](https://github.com/tikv/pd/issues/4077)
    -   スキャッタ範囲スケジューラが空の領域をスケジュールできない問題を修正します[#4118](https://github.com/tikv/pd/pull/4118)
    -   キーマネージャーのCPU消費量が多すぎる問題を修正[#4071](https://github.com/tikv/pd/issues/4071)
    -   ホット リージョン スケジューラ[#4159](https://github.com/tikv/pd/issues/4159)の構成を設定するときに発生する可能性があるデータ競合の問題を修正します。
    -   リージョン同期装置[#3936](https://github.com/tikv/pd/issues/3936)のスタックによって引き起こされるリーダー選出の遅さを修正

-   TiFlash

    -   ライブラリ`nsl`がないため、一部のプラットフォームでTiFlash が起動できない問題を修正

-   ツール

    -   TiCDC
        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正します[#3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[#2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDC プロセスがパニックになる可能panicがある問題を修正
        -   ダウンストリーム TiDB/MySQL の可用性を確認する際の不要な CPU 消費を修正[#3073](https://github.com/pingcap/tiflow/issues/3073)
        -   TiCDC によって生成される Kafka メッセージの量が`max-message-size` [#2962](https://github.com/pingcap/tiflow/issues/2962)の制限を受けない問題を修正
        -   Kafka メッセージの書き込み中にエラーが発生すると、TiCDC 同期タスクが一時停止することがある問題を修正します[#2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`が有効な場合、有効なインデックスのない一部のパーティション テーブルが無視される可能性がある問題を修正します[#2834](https://github.com/pingcap/tiflow/issues/2834)
        -   ストック データのスキャンに時間がかかりすぎる場合、TiKV が GC を実行するためにストック データのスキャンが失敗する可能性がある問題を修正します[#2470](https://github.com/pingcap/tiflow/issues/2470)
        -   一部の種類の列をオープン プロトコル形式[#2758](https://github.com/pingcap/tiflow/issues/2758)にエンコードするときに発生する可能性のpanicの問題を修正しました。
        -   一部の種類の列を Avro 形式[#2648](https://github.com/pingcap/tiflow/issues/2648)にエンコードするときに発生する可能性のpanicの問題を修正

    -   TiDBBinlog

        -   ほとんどのテーブルがフィルターで除外されると、特別な負荷がかかるとチェックポイントを更新できない問題を修正します[#1075](https://github.com/pingcap/tidb-binlog/pull/1075)
