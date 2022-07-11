---
title: TiDB 5.3.1 Release Notes
---

# TiDB5.3.1リリースノート {#tidb-5-3-1-release-notes}

リリース日：2022年3月3日

TiDBバージョン：5.3.1

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiDB Lightning

        -   データのインポート後に空のリージョンが多すぎないように、デフォルト値の`regionMaxKeyCount`を1_440_000から1_280_000に変更します[＃30018](https://github.com/pingcap/tidb/issues/30018)

## 改善 {#improvements}

-   TiDB

    -   ユーザーログインモードのマッピングロジックを最適化して、ロギングをよりMySQL互換にします[＃30450](https://github.com/pingcap/tidb/issues/32648)

-   TiKV

    -   ロックの解決ステップ[＃11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことにより、TiCDCの回復時間を短縮します。
    -   GC to Raftログを実行するときに書き込みバッチサイズを増やすことにより、ガベージコレクション（GC）プロセスを高速化します[＃11404](https://github.com/tikv/tikv/issues/11404)
    -   procファイルシステム（procfs）をv0.12.0に更新します[＃11702](https://github.com/tikv/tikv/issues/11702)

-   PD

    -   `DR_STATE`ファイルのコンテンツフォーマットを最適化する[＃4341](https://github.com/tikv/pd/issues/4341)

-   ツール

    -   TiCDC

        -   Kafkaプロデューサーの構成パラメーターを公開して、 [＃4385](https://github.com/pingcap/tiflow/issues/4385)で構成可能にします。
        -   S3がバックエンドストレージとして使用されている場合は、TiCDCの起動時に事前クリーンアッププロセスを追加します[＃3878](https://github.com/pingcap/tiflow/issues/3878)
        -   TiCDCクライアントは、証明書名が指定されていない場合に機能します[＃3627](https://github.com/pingcap/tiflow/issues/3627)
        -   テーブルごとにシンクチェックポイントを管理して、チェックポイントタイムスタンプの予期しない前進を回避します[＃3545](https://github.com/pingcap/tiflow/issues/3545)
        -   チェンジフィードを再開するための指数バックオフメカニズムを追加します。 [＃3329](https://github.com/pingcap/tiflow/issues/3329)
        -   Kafka Sink `partition-num`のデフォルト値を3に変更して、TiCDCがKafkaパーティション間でメッセージをより均等に分散するようにします[＃3337](https://github.com/pingcap/tiflow/issues/3337)
        -   「EventFeed再試行レート制限」ログの数を減らす[＃4006](https://github.com/pingcap/tiflow/issues/4006)
        -   デフォルト値の`max-message-bytes`を設定します[＃4041](https://github.com/pingcap/tiflow/issues/4041)
        -   `no owner alert` `buffer sink total row` [＃4054](https://github.com/pingcap/tiflow/issues/4054)など、 [＃1606](https://github.com/pingcap/tiflow/issues/1606)と`mounter row`の監視メトリックとアラートをさらに追加し`table sink total row`
        -   TiKVストアがダウンしたときにKVクライアントが回復する時間を短縮する[＃3191](https://github.com/pingcap/tiflow/issues/3191)

    -   TiDB Lightning

        -   事前チェックの出力メッセージを調整して、ローカルディスクスペースチェックが失敗したときにユーザーフレンドリーにする[＃30395](https://github.com/pingcap/tidb/issues/30395)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDBの`date_format`がMySQLと互換性のない方法で`'\n'`を処理する問題を修正します[＃32232](https://github.com/pingcap/tidb/issues/32232)
    -   `alter column set default`がテーブルスキーマ[＃31074](https://github.com/pingcap/tidb/issues/31074)を誤って更新する問題を修正します
    -   `tidb_restricted_read_only`が有効になっているときに`tidb_super_read_only`が自動的に有効にならないバグを修正します[＃31745](https://github.com/pingcap/tidb/issues/31745)
    -   照合順序を伴う`greatest`または`least`関数が間違った結果を取得する問題を修正します[＃31789](https://github.com/pingcap/tidb/issues/31789)
    -   クエリ実行時のMPPタスクリストの空のエラーを修正[＃31636](https://github.com/pingcap/tidb/issues/31636)
    -   innerWorkerpanicによって引き起こされるインデックス結合の誤った結果を修正します[＃31494](https://github.com/pingcap/tidb/issues/31494)
    -   列タイプを`FLOAT`から`DOUBLE`に変更した後の誤ったクエリ結果を[＃31372](https://github.com/pingcap/tidb/issues/31372)する
    -   インデックスルックアップ結合[＃30468](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`のエラーを修正しました
    -   `Order By`の最適化による誤ったクエリ結果を[＃30271](https://github.com/pingcap/tidb/issues/30271)
    -   `MaxDays`と`MaxBackups`の構成が遅いログ[＃25716](https://github.com/pingcap/tidb/issues/25716)で有効にならない問題を修正します
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanicになる問題を修正します[＃28078](https://github.com/pingcap/tidb/issues/28078)

-   TiKV

    -   ピアステータスが`Applying`のときにスナップショットファイルを削除することによって引き起こされるpanicの問題を修正し[＃11746](https://github.com/tikv/tikv/issues/11746)
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定されている場合のQPSドロップの問題を修正します[＃11424](https://github.com/tikv/tikv/issues/11424)
    -   cgroupコントローラーがマウントされていないときに発生するpanicの問題を修正します[＃11569](https://github.com/tikv/tikv/issues/11569)
    -   TiKVの動作が停止した後、解決されたTSの遅延が増加する問題を修正します[＃11351](https://github.com/tikv/tikv/issues/11351)
    -   GCワーカーがビジー状態のときにTiKVがデータの範囲を削除できない（ `unsafe_destroy_range`は実行できない）バグを修正します[＃11903](https://github.com/tikv/tikv/issues/11903)
    -   ピアを破棄すると待ち時間が長くなる可能性があるという問題を修正します[＃10210](https://github.com/tikv/tikv/issues/10210)
    -   領域が空の場合に`any_value`関数が間違った結果を返すバグを修正します[＃11735](https://github.com/tikv/tikv/issues/11735)
    -   初期化されていないレプリカを削除すると、古いレプリカが再作成される可能性がある問題を修正します[＃10533](https://github.com/tikv/tikv/issues/10533)
    -   新しい選択が終了した後に`Prepare Merge`がトリガーされたが、分離されたピアに通知されない場合のメタデータ破損の問題を修正します[＃11526](https://github.com/tikv/tikv/issues/11526)
    -   コルーチンの実行速度が速すぎる場合に時々発生するデッドロックの問題を修正します[＃11549](https://github.com/tikv/tikv/issues/11549)
    -   TiKVノードがダウンすると、解決されたタイムスタンプが[＃11351](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正します。
    -   Raftクライアントの実装でバッチメッセージが大きすぎるという問題を修正します[＃9714](https://github.com/tikv/tikv/issues/9714)
    -   リージョンマージ、ConfChange、およびスナップショットが極端な条件で同時に発生するときに発生するpanicの問題を修正します[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKVが逆テーブルスキャンを実行すると、TiKVがメモリロックを検出できない問題を修正します[＃11440](https://github.com/tikv/tikv/issues/11440)
    -   ディスク容量がいっぱいになると、RocksDBのフラッシュまたは圧縮によってpanicが発生する問題を修正します[＃11224](https://github.com/tikv/tikv/issues/11224)
    -   tikv-ctlが正しいリージョン関連情報を返さないバグを修正します[＃11393](https://github.com/tikv/tikv/issues/11393)
    -   インスタンスごとのgRPCリクエストの平均レイテンシがTiKVメトリクス[＃11299](https://github.com/tikv/tikv/issues/11299)で不正確であるという問題を修正します

-   PD

    -   特定の場合にスケジューリングプロセスに不要なJointConsensusステップがあるバグを修正します[＃4362](https://github.com/tikv/pd/issues/4362)
    -   投票者を直接降格するときにスケジュールを実行できないバグを修正します[＃4444](https://github.com/tikv/pd/issues/4444)
    -   レプリカのレプリケーションモードの構成を更新するときに発生するデータ競合の問題を修正します[＃4325](https://github.com/tikv/pd/issues/4325)
    -   特定の場合に読み取りロックが解放されないバグを修正します[＃4354](https://github.com/tikv/pd/issues/4354)
    -   コールドホットスポットデータをホットスポット統計から削除できない問題を修正します[＃4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   入力引数`arg`が`decimal(x,y)`の範囲をオーバーフローすると、 `cast(arg as decimal(x,y))`が間違った結果を返す問題を修正します。
    -   `max_memory_usage`と`max_memory_usage_for_all_queries`が有効になっているときに発生するTiFlashクラッシュの問題を修正します
    -   `cast(string as real)`が間違った結果を返す問題を修正します
    -   `cast(string as decimal)`が間違った結果を返す問題を修正します
    -   主キー列をより大きなintデータ型に変更した後の潜在的なデータの不整合を修正
    -   `in`が`select (arg0, arg1) in (x,y)`のようなステートメントに複数の引数を持っている場合、 `in`が間違った結果を返すというバグを修正します
    -   MPPクエリが停止したときにTiFlashがpanicになる可能性がある問題を修正します
    -   入力引数に先行ゼロがある場合に`str_to_date`が間違った結果を返す問題を修正します
    -   フィルタが`where <string>`形式の場合、クエリが間違った結果を返す問題を修正します
    -   入力引数`string`が`%Y-%m-%d\n%H:%i:%s`形式の場合に`cast(string as datetime)`が間違った結果を返す問題を修正します

-   ツール

    -   バックアップと復元（BR）

        -   復元操作の終了後にリージョンが不均一に分散される可能性があるという潜在的な問題を修正します[＃31034](https://github.com/pingcap/tidb/issues/31034)

    -   TiCDC

        -   [＃4637](https://github.com/pingcap/tiflow/issues/4637)がエラーを報告するバグを修正します`Column length too big`
        -   PDリーダーが殺されたときにTiCDCノードが異常終了するバグを修正します[＃4248](https://github.com/pingcap/tiflow/issues/4248)
        -   セーフモードでの更新ステートメントの実行エラーがDMワーカーのpanicを引き起こす可能性がある問題を修正します[＃4317](https://github.com/pingcap/tiflow/issues/4317)
        -   TiKVクライアントのキャッシュ領域メトリックが負になる可能性がある問題を修正します[＃4300](https://github.com/pingcap/tiflow/issues/4300)
        -   必要なプロセッサ情報が存在しない場合にHTTPAPIがパニックになるバグを修正します[＃3840](https://github.com/pingcap/tiflow/issues/3840)
        -   DM-masterとDM-workerを特定の順序で再起動した後、DM-masterのリレーステータスが間違っているバグを修正します[＃3478](https://github.com/pingcap/tiflow/issues/3478)
        -   再起動後にDMワーカーが起動に失敗するバグを修正します[＃3344](https://github.com/pingcap/tiflow/issues/3344)
        -   PARTITIONDDLの実行に時間がかかりすぎるとDMタスクが失敗するバグを修正します[＃3854](https://github.com/pingcap/tiflow/issues/3854)
        -   アップストリームがMySQL8.03の場合にDMが`invalid sequence`を報告する可能性があるバグを修正し[＃3847](https://github.com/pingcap/tiflow/issues/3847)
        -   一時停止したチェンジフィードを削除すると、REDOログがクリーンアップされないバグを修正します[＃4740](https://github.com/pingcap/tiflow/issues/4740)
        -   DMがよりきめ細かい再試行を行う場合のデータ損失のバグを修正[＃3487](https://github.com/pingcap/tiflow/issues/3487)
        -   コンテナ環境でのOOMの修正[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   読み込み中のタスクを停止すると、予期しないタスクの転送が発生するバグを修正します[＃3771](https://github.com/pingcap/tiflow/issues/3771)
        -   ローダー[＃3252](https://github.com/pingcap/tiflow/issues/3252)の`query-status`コマンドで間違った進行状況が返される問題を修正します
        -   クラスタ[＃3483](https://github.com/pingcap/tiflow/issues/3483)に異なるバージョンのTiCDCノードがある場合にHTTPAPIが機能しない問題を修正します
        -   S3ストレージがTiCDCRedoLog1で設定されている場合にTiCDCが異常終了する問題を修正し[＃3523](https://github.com/pingcap/tiflow/issues/3523)
        -   デフォルト値を複製できない問題を修正します[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   `batch-replace-enable`が無効になっている場合にMySQLシンクが重複した`replace`のSQLステートメントを生成するバグを修正します[＃4501](https://github.com/pingcap/tiflow/issues/4501)
        -   シンカーメトリックがステータス[＃4281](https://github.com/pingcap/tiflow/issues/4281)をクエリするときにのみ更新される問題を修正します
        -   `mq sink write row`に監視データがないという問題を修正します[＃3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `min.insync.replicas`が[＃3994](https://github.com/pingcap/tiflow/issues/3994)より小さい場合、レプリケーションを実行できない問題を修正し`replication-factor` 。
        -   `CREATE VIEW`ステートメントがデータレプリケーションを中断する問題を修正します[＃4173](https://github.com/pingcap/tiflow/issues/4173)
        -   DDLステートメントがスキップされた後にスキーマをリセットする必要がある問題を修正します[＃4177](https://github.com/pingcap/tiflow/issues/4177)
        -   `mq sink write row`に監視データがないという問題を修正します[＃3431](https://github.com/pingcap/tiflow/issues/3431)
        -   レプリケーションタスクが削除されたときに発生する可能性のあるpanicの問題を修正する[＃3128](https://github.com/pingcap/tiflow/issues/3128)
        -   デッドロックによってレプリケーションタスクがスタックするという潜在的な問題を修正します[＃4055](https://github.com/pingcap/tiflow/issues/4055)
        -   etcd1のタスクステータスを手動でクリーニングするときに発生するTiCDCpanicの問題を修正し[＃2980](https://github.com/pingcap/tiflow/issues/2980)
        -   DDLステートメントの特別なコメントによってレプリケーションタスクが停止する問題を修正します[＃3755](https://github.com/pingcap/tiflow/issues/3755)
        -   `config.Metadata.Timeout`の誤った構成によって引き起こされるレプリケーション停止の問題を修正し[＃3352](https://github.com/pingcap/tiflow/issues/3352) 。
        -   一部のRHELリリース[＃3584](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題が原因でサービスを開始できない問題を修正します
        -   クラスタのアップグレード後に`stopped`つのチェンジフィードが自動的に再開する問題を修正します[＃3473](https://github.com/pingcap/tiflow/issues/3473)
        -   デフォルト値を複製できない問題を修正します[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   MySQLシンクデッドロック[＃2706](https://github.com/pingcap/tiflow/issues/2706)によって引き起こされる過度に頻繁な警告の問題を修正します
        -   CanalおよびMaxwellプロトコル[＃3676](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`の構成アイテムが自動的に`true`に設定されないバグを修正します。
        -   AvroシンクがJSONタイプの列の解析をサポートしていない問題を修正します[＃3624](https://github.com/pingcap/tiflow/issues/3624)
        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/tiflow/issues/3010)の負の値エラーを修正しました

    -   TiDB Lightning

        -   一部のインポートタスクにソースファイルが含まれていない場合にTiDB Lightningがメタデータスキーマを削除しない可能性があるバグを修正します[＃28144](https://github.com/pingcap/tidb/issues/28144)
        -   ストレージURLプレフィックスが「gcs：// xxx」ではなく「gs：// xxx」の場合、 TiDB Lightningがエラーを返すバグを修正します[＃32742](https://github.com/pingcap/tidb/issues/32742)
        -   --log-file=&quot;-&quot;を設定してもログがstdout1に[＃29876](https://github.com/pingcap/tidb/issues/29876)されない問題を修正します
        -   S3ストレージパスが存在しない場合にTiDB Lightningがエラーを報告しない問題を修正します[＃30709](https://github.com/pingcap/tidb/issues/30709)
