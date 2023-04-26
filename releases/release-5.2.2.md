---
title: TiDB 5.2.2 Release Notes
---

# TiDB 5.2.2 リリースノート {#tidb-5-2-2-release-notes}

リリース日：2021年10月29日

TiDB バージョン: 5.2.2

## 改良点 {#improvements}

-   TiDB

    -   コプロセッサーがロックを検出したときに、影響を受ける SQL ステートメントをデバッグ・ログに表示します。これは、問題の診断に役立ちます[#27718](https://github.com/pingcap/tidb/issues/27718)
    -   SQL 論理レイヤー[#27247](https://github.com/pingcap/tidb/issues/27247)でデータをバックアップおよび復元する場合のバックアップおよび復元データのサイズの表示のサポート

-   TiKV

    -   L0 フロー制御[#10879](https://github.com/tikv/tikv/issues/10879)のアルゴリズムを簡素化する
    -   raft クライアント モジュール[#10983](https://github.com/tikv/tikv/pull/10983)のエラー ログ レポートを改善します。
    -   ログ スレッドを改善して、パフォーマンスのボトルネックにならないようにする[#10841](https://github.com/tikv/tikv/issues/10841)
    -   書き込みクエリの統計タイプを追加する[#10507](https://github.com/tikv/tikv/issues/10507)

-   PD

    -   ホットスポット スケジューラ[#3869](https://github.com/tikv/pd/issues/3869)の QPS ディメンションに書き込みクエリのタイプを追加する
    -   スケジューラーのパフォーマンスを向上させるために、バランス領域スケジューラーの再試行制限を動的に調整するサポート[#3744](https://github.com/tikv/pd/issues/3744)
    -   TiDB ダッシュボードを v2021.10.08.1 に更新する[#4070](https://github.com/tikv/pd/pull/4070)
    -   エビクト リーダー スケジューラが異常なピアを含むリージョンをスケジュールできるようにするサポート[#4093](https://github.com/tikv/pd/issues/4093)
    -   スケジューラーの終了プロセスを高速化する[#4146](https://github.com/tikv/pd/issues/4146)

-   ツール

    -   TiCDC

        -   Kafka シンク構成項目`MaxMessageBytes`のデフォルト値を 64 MB から 1 MB に減らして、大きなメッセージが Kafka Broker [#3104](https://github.com/pingcap/tiflow/pull/3104)によって拒否される問題を修正します。
        -   レプリケーション パイプラインのメモリ使用量を減らす[#2553](https://github.com/pingcap/tiflow/issues/2553) [#3037](https://github.com/pingcap/tiflow/pull/3037) [#2726](https://github.com/pingcap/tiflow/pull/2726)
        -   監視項目とアラートルールを最適化し、同期リンク、メモリGC、および株式データのスキャンプロセスの可観測性を向上させる[#2735](https://github.com/pingcap/tiflow/pull/2735) [#1606](https://github.com/pingcap/tiflow/issues/1606) [#3000](https://github.com/pingcap/tiflow/pull/3000) [#2985](https://github.com/pingcap/tiflow/issues/2985) [#2156](https://github.com/pingcap/tiflow/issues/2156)
        -   同期タスクのステータスが通常の場合、ユーザーの誤解を招くことを避けるために、過去のエラー メッセージは表示されません[#2242](https://github.com/pingcap/tiflow/issues/2242)

## バグの修正 {#bug-fixes}

-   TiDB

    -   plan-cache が署名されていないフラグの変更を検出できない問題を修正します[#28254](https://github.com/pingcap/tidb/issues/28254)
    -   パーティション関数が範囲[#28233](https://github.com/pingcap/tidb/issues/28233)の外にある場合の間違ったパーティションのプルーニングを修正します。
    -   Planner が`join`の無効なプランをキャッシュする場合がある問題を修正します[#28087](https://github.com/pingcap/tidb/issues/28087)
    -   ハッシュ列のタイプが列挙型[#27893](https://github.com/pingcap/tidb/issues/27893)の場合の間違ったインデックス ハッシュ結合を修正
    -   アイドル状態の接続をリサイクルすると、まれにリクエストの送信がブロックされる可能性があるというバッチ クライアントのバグを修正します[#27688](https://github.com/pingcap/tidb/pull/27688)
    -   ターゲット クラスタでチェックサムの実行に失敗した場合のTiDB Lightningpanicの問題を修正します[#27686](https://github.com/pingcap/tidb/pull/27686)
    -   場合によっては`date_add`と`date_sub`関数の誤った結果を修正します[#27232](https://github.com/pingcap/tidb/issues/27232)
    -   ベクトル化された式[#28643](https://github.com/pingcap/tidb/issues/28643)の`hour`関数の間違った結果を修正
    -   MySQL 5.1 またはそれ以前のクライアント バージョン[#27855](https://github.com/pingcap/tidb/issues/27855)に接続する際の認証の問題を修正します。
    -   新しいインデックスが追加されたときに、指定された時間外にauto analyzeがトリガーされる可能性がある問題を修正します[#28698](https://github.com/pingcap/tidb/issues/28698)
    -   セッション変数を設定すると無効になるバグを修正`tidb_snapshot` [#28683](https://github.com/pingcap/tidb/pull/28683)
    -   不足しているピア リージョンが多数あるクラスタでBRが機能しないバグを修正します[#27534](https://github.com/pingcap/tidb/issues/27534)
    -   サポートされていない`cast` TiFlash [#23907](https://github.com/pingcap/tidb/issues/23907)に押し下げると`tidb_cast to Int32 is not supported`のような予期しないエラーが発生する問題を修正
    -   `%s value is out of range in '%s'`エラー メッセージ[#27964](https://github.com/pingcap/tidb/issues/27964)で`DECIMAL overflow`が欠落している問題を修正します。
    -   一部のまれなケースで MPP ノードの可用性検出が機能しないバグを修正します[#3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)を割り当てる際の`DATA RACE`問題を修正
    -   空`dual table`削除した後の MPP クエリの`INDEX OUT OF RANGE`エラーを修正します。 [#28250](https://github.com/pingcap/tidb/issues/28250)
    -   MPP クエリ[#1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラー ログ`invalid cop task execution summaries length`の問題を修正します。
    -   MPP クエリ[#28149](https://github.com/pingcap/tidb/pull/28149)のエラー ログ`cannot found column in Schema column`の問題を修正します。
    -   TiFlashのシャットダウン時に TiDB がpanicになる問題を修正[#28096](https://github.com/pingcap/tidb/issues/28096)
    -   安全でない 3DES (Triple Data Encryption Algorithm) ベースの TLS 暗号スイートのサポートを削除します[#27859](https://github.com/pingcap/tidb/pull/27859)
    -   事前チェック中に Lightning がオフラインの TiKV ノードに接続し、インポートの失敗を引き起こす問題を修正します[#27826](https://github.com/pingcap/tidb/pull/27826)
    -   テーブルに多数のファイルをインポートする場合、事前チェックに時間がかかりすぎる問題を修正します[#27605](https://github.com/pingcap/tidb/issues/27605)
    -   式を書き換えると`between`間違った照合順序を推論する問題を修正[#27146](https://github.com/pingcap/tidb/issues/27146)
    -   `group_concat`関数が照合順序[#27429](https://github.com/pingcap/tidb/issues/27429)を考慮していなかった問題を修正
    -   `extract`関数の引数が負の期間[#27236](https://github.com/pingcap/tidb/issues/27236)の場合に発生する結果の誤りを修正します。
    -   `NO_UNSIGNED_SUBTRACTION`を[#26765](https://github.com/pingcap/tidb/issues/26765)に設定するとパーティションの作成に失敗する問題を修正
    -   列の刈り込みと集計のプッシュダウンで副作用のある式を避ける[#27106](https://github.com/pingcap/tidb/issues/27106)
    -   無駄な gRPC ログを削除する[#24190](https://github.com/pingcap/tidb/issues/24190)
    -   有効な 10 進数の長さを制限して、精度関連の問題を修正する[#3091](https://github.com/pingcap/tics/issues/3091)
    -   `plus`式[#26977](https://github.com/pingcap/tidb/issues/26977)のオーバーフローのチェック方法が間違っている問題を修正
    -   `new collation`データ[#27024](https://github.com/pingcap/tidb/issues/27024)のテーブルから統計をダンプするときに`data too long`エラーが発生する問題を修正
    -   リトライしたトランザクションの明細が`TIDB_TRX` [#28670](https://github.com/pingcap/tidb/pull/28670)に含まれない問題を修正

-   TiKV

    -   Congest エラー[#11082](https://github.com/tikv/tikv/issues/11082)により、CDC が頻繁にスキャンの再試行を追加する問題を修正します。
    -   チャンネルがいっぱいになるといかだ接続が切断される問題を修正します[#11047](https://github.com/tikv/tikv/issues/11047)
    -   Raftクライアント実装[#9714](https://github.com/tikv/tikv/issues/9714)でバッチ メッセージが大きすぎる問題を修正
    -   `resolved_ts` [#10965](https://github.com/tikv/tikv/issues/10965)で一部のコルーチンがリークする問題を修正
    -   応答のサイズが 4 GiB を超えるとコプロセッサーに発生するpanicの問題を修正します[#9012](https://github.com/tikv/tikv/issues/9012)
    -   スナップショット ファイルをガベージ コレクションできない場合に、スナップショット ガベージ コレクション (GC) で GC スナップショット ファイルが失われる問題を修正します[#10813](https://github.com/tikv/tikv/issues/10813)
    -   コプロセッサー要求を処理する際のタイムアウトによって引き起こされるpanicの問題を修正します[#10852](https://github.com/tikv/tikv/issues/10852)

-   PD

    -   ピアの数が構成済みのピアの数を超えているため、PD がデータを含むピアと保留中の状態のピアを誤って削除する問題を修正します[#4045](https://github.com/tikv/pd/issues/4045)
    -   PD が時間内にダウンしたピアを修正しない問題を修正します[#4077](https://github.com/tikv/pd/issues/4077)
    -   分散範囲スケジューラーが空の領域をスケジュールできない問題を修正します[#4118](https://github.com/tikv/pd/pull/4118)
    -   キー マネージャーが CPU [#4071](https://github.com/tikv/pd/issues/4071)のコストが高すぎる問題を修正します。
    -   ホット リージョン スケジューラ[#4159](https://github.com/tikv/pd/issues/4159)の構成を設定するときに発生する可能性があるデータ競合の問題を修正します。
    -   リージョン シンサー[#3936](https://github.com/tikv/pd/issues/3936)のスタックによるリーダー選出の遅さを修正

-   TiFlash

    -   ライブラリ`nsl`が存在しないため、一部のプラットフォームでTiFlash が起動しない問題を修正

-   ツール

    -   TiCDC
        -   アップストリームの TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正します[#3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[#2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDC プロセスがパニックになる可能panicがある問題を修正します。
        -   ダウンストリームの TiDB/MySQL の可用性を検証する際の不要な CPU 消費を修正します[#3073](https://github.com/pingcap/tiflow/issues/3073)
        -   TiCDC によって生成される Kafka メッセージの量が`max-message-size` [#2962](https://github.com/pingcap/tiflow/issues/2962)によって制限されないという問題を修正します
        -   Kafka メッセージの書き込み中にエラーが発生すると、TiCDC 同期タスクが一時停止することがある問題を修正します[#2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`が有効な場合、有効なインデックスのない一部のパーティション テーブルが無視される可能性があるという問題を修正します[#2834](https://github.com/pingcap/tiflow/issues/2834)
        -   株式データのスキャンに時間がかかりすぎると、TiKV が GC を実行するために株式データのスキャンが失敗する可能性がある問題を修正します[#2470](https://github.com/pingcap/tiflow/issues/2470)
        -   一部のタイプの列を Open Protocol フォーマット[#2758](https://github.com/pingcap/tiflow/issues/2758)にエンコードする際に発生する可能性があったpanicの問題を修正
        -   一部のタイプの列を Avro フォーマット[#2648](https://github.com/pingcap/tiflow/issues/2648)にエンコードする際に発生する可能性があったpanicの問題を修正

    -   TiDBBinlog

        -   ほとんどのテーブルが除外されている場合、特定の負荷がかかるとチェックポイントを更新できないという問題を修正します[#1075](https://github.com/pingcap/tidb-binlog/pull/1075)
