---
title: TiDB 5.3.1 Release Notes
summary: TiDB 5.3.1 は 2022 年 3 月 3 日にリリースされました。このリリースには、TiDB、TiKV、PD、TiCDC、 TiFlash、バックアップと復元 (BR)、および TiDB データ移行 (DM) の互換性の変更、改善、バグ修正が含まれています。注目すべき変更点としては、ユーザー ログイン モード マッピングの最適化、TiCDC リカバリ時間の短縮、TiDB、TiKV、PD、 TiFlash、および TiCDC やTiDB Lightningなどのツールのさまざまなバグの修正などがあります。これらの修正により、データのインポート、ユーザー ログイン、ガベージコレクション、構成パラメータなどに関連する問題が解決されます。
---

# TiDB 5.3.1 リリースノート {#tidb-5-3-1-release-notes}

リリース日：2022年3月3日

TiDB バージョン: 5.3.1

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiDB Lightning

        -   データのインポート後に空の領域が多すぎるのを避けるため、デフォルト値`regionMaxKeyCount`を 1_440_000 から 1_280_000 に変更します[＃30018](https://github.com/pingcap/tidb/issues/30018)

## 改善点 {#improvements}

-   ティビ

    -   ユーザーログインモードのマッピングロジックを最適化して、ログ記録をよりMySQL互換にします[＃32648](https://github.com/pingcap/tidb/issues/32648)

-   ティクヴ

    -   解決ロックを必要とする領域の数を減らすことで、TiCDC の回復時間を短縮します (手順[＃11993](https://github.com/tikv/tikv/issues/11993)
    -   Raftログ[＃11404](https://github.com/tikv/tikv/issues/11404)へのガベージ コレクション (GC) を実行するときに書き込みバッチ サイズを増やすことで、GC プロセスを高速化します。
    -   procファイルシステム（procfs）をv0.12.0 [＃11702](https://github.com/tikv/tikv/issues/11702)に更新する

-   PD

    -   `DR_STATE`ファイル[＃4341](https://github.com/tikv/pd/issues/4341)のコンテンツフォーマットを最適化する

-   ツール

    -   ティCDC

        -   Kafka プロデューサーの設定パラメータを公開して、TiCDC [＃4385](https://github.com/pingcap/tiflow/issues/4385)で設定できるようにします。
        -   S3 をバックエンドstorageとして使用する場合、TiCDC 起動時に事前クリーンアッププロセスを追加します[＃3878](https://github.com/pingcap/tiflow/issues/3878)
        -   TiCDCクライアントは証明書名が指定されていない場合でも動作します[＃3627](https://github.com/pingcap/tiflow/issues/3627)
        -   チェックポイントのタイムスタンプが予期せず進むのを避けるために、テーブルごとにシンクのチェックポイントを管理する[＃3545](https://github.com/pingcap/tiflow/issues/3545)
        -   チェンジフィードを再開するための指数バックオフメカニズムを追加します[＃3329](https://github.com/pingcap/tiflow/issues/3329)
        -   TiCDC がメッセージを Kafka パーティション間でより均等に分散するように、Kafka シンクのデフォルト値を`partition-num`から 3 に変更します[＃3337](https://github.com/pingcap/tiflow/issues/3337)
        -   「EventFeed 再試行レート制限」ログの数を減らす[＃4006](https://github.com/pingcap/tiflow/issues/4006)
        -   デフォルト値`max-message-bytes`を10M [＃4041](https://github.com/pingcap/tiflow/issues/4041)に設定する
        -   `no owner alert` [＃4054](https://github.com/pingcap/tiflow/issues/4054)含む`buffer sink total row`と`table sink total row`の監視メトリックと[＃1606](https://github.com/pingcap/tiflow/issues/1606)を追加します`mounter row`
        -   TiKVストアがダウンしたときにKVクライアントが回復するまでの時間を短縮する[＃3191](https://github.com/pingcap/tiflow/issues/3191)

    -   TiDB Lightning

        -   ローカルディスク容量チェックが失敗した場合の事前チェックの出力メッセージを改良し、よりユーザーフレンドリーなものにします[＃30395](https://github.com/pingcap/tidb/issues/30395)

## バグの修正 {#bug-fixes}

-   ティビ

    -   TiDBの`date_format`が`'\n'`をMySQLと互換性のない方法で処理する問題を修正[＃32232](https://github.com/pingcap/tidb/issues/32232)
    -   `alter column set default`テーブルスキーマ[＃31074](https://github.com/pingcap/tidb/issues/31074)を誤って更新する問題を修正
    -   `tidb_restricted_read_only`有効になっているときに`tidb_super_read_only`が自動的に有効にならないバグを修正[＃31745](https://github.com/pingcap/tidb/issues/31745)
    -   照合順序を伴う`greatest`または`least`関数が間違った結果を返す問題を修正[＃31789](https://github.com/pingcap/tidb/issues/31789)
    -   クエリ[＃31636](https://github.com/pingcap/tidb/issues/31636)を実行するときに MPP タスク リストが空になるエラーを修正
    -   innerWorkerpanicによって発生するインデックス結合の誤った結果を修正[＃31494](https://github.com/pingcap/tidb/issues/31494)
    -   列タイプを`FLOAT`から`DOUBLE` [＃31372](https://github.com/pingcap/tidb/issues/31372)に変更した後の間違ったクエリ結果を修正
    -   インデックスルックアップ結合[＃30468](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときに発生する`invalid transaction`エラーを修正
    -   `Order By` [＃30271](https://github.com/pingcap/tidb/issues/30271)の最適化による誤ったクエリ結果を修正
    -   `MaxDays`と`MaxBackups`の設定がスローログ[＃25716](https://github.com/pingcap/tidb/issues/25716)に反映されない問題を修正
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`文を実行するとpanic[＃28078](https://github.com/pingcap/tidb/issues/28078)発生する問題を修正

-   ティクヴ

    -   ピアステータスが`Applying` [＃11746](https://github.com/tikv/tikv/issues/11746)のときにスナップショットファイルを削除すると発生するpanic問題を修正しました。
    -   フロー制御が有効で、 `level0_slowdown_trigger`明示的に設定されている場合に QPS が低下する問題を修正[＃11424](https://github.com/tikv/tikv/issues/11424)
    -   cgroup コントローラがマウントされていない場合に発生するpanic問題を修正[＃11569](https://github.com/tikv/tikv/issues/11569)
    -   TiKVの動作が停止した後にResolved TSのレイテンシーが増加する問題を修正[＃11351](https://github.com/tikv/tikv/issues/11351)
    -   GCワーカーがビジー状態のときにTiKVがデータの範囲を削除できない（ `unsafe_destroy_range`実行できない）というバグを修正[＃11903](https://github.com/tikv/tikv/issues/11903)
    -   ピアを破棄するとレイテンシーが大きくなる可能性がある問題を修正[＃10210](https://github.com/tikv/tikv/issues/10210)
    -   領域が空の場合に関数`any_value`誤った結果を返すバグを修正[＃11735](https://github.com/tikv/tikv/issues/11735)
    -   初期化されていないレプリカを削除すると古いレプリカが再作成される可能性がある問題を修正[＃10533](https://github.com/tikv/tikv/issues/10533)
    -   新しい選出が終了した後に`Prepare Merge`トリガーされたが、分離されたピアに通知されない場合のメタデータ破損の問題を修正[＃11526](https://github.com/tikv/tikv/issues/11526)
    -   コルーチンの実行速度が速すぎる場合に時々発生するデッドロックの問題を修正[＃11549](https://github.com/tikv/tikv/issues/11549)
    -   TiKVノードがダウンすると解決されたタイムスタンプが[＃11351](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正
    -   Raftクライアント実装[＃9714](https://github.com/tikv/tikv/issues/9714)でバッチメッセージが大きすぎる問題を修正
    -   極端な状況でリージョンのマージ、ConfChange、スナップショットが同時に発生した場合に発生するpanicの問題を修正[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKVが逆テーブルスキャンを実行するときにメモリロックを検出できない問題を修正[＃11440](https://github.com/tikv/tikv/issues/11440)
    -   ディスク容量がいっぱいのときにRocksDBのフラッシュまたは圧縮によってpanicが発生する問題を修正[＃11224](https://github.com/tikv/tikv/issues/11224)
    -   tikv-ctl が正しい地域関連情報を返すことができないバグを修正[＃11393](https://github.com/tikv/tikv/issues/11393)
    -   TiKV メトリック[＃11299](https://github.com/tikv/tikv/issues/11299)でインスタンスごとの gRPC リクエストの平均レイテンシーが不正確になる問題を修正

-   PD

    -   特定のケースでスケジュール処理に不要な JointConsensus ステップが含まれるバグを修正[＃4362](https://github.com/tikv/pd/issues/4362)
    -   投票者を直接降格させるとスケジュールが実行できないバグを修正[＃4444](https://github.com/tikv/pd/issues/4444)
    -   レプリカ[＃4325](https://github.com/tikv/pd/issues/4325)のレプリケーション モードの構成を更新するときに発生するデータ競合の問題を修正しました。
    -   特定のケースで読み取りロックが解除されないバグを修正[＃4354](https://github.com/tikv/pd/issues/4354)
    -   ホットスポット統計からコールドホットスポットデータを削除できない問題を修正[＃4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   入力引数`arg` `decimal(x,y)`の範囲を超えた場合に`cast(arg as decimal(x,y))`間違った結果を返す問題を修正しました
    -   `max_memory_usage`と`max_memory_usage_for_all_queries`が有効になっているときに発生するTiFlashクラッシュの問題を修正
    -   `cast(string as real)`間違った結果を返す問題を修正
    -   `cast(string as decimal)`間違った結果を返す問題を修正
    -   主キー列をより大きな int データ型に変更した後に発生する可能性のあるデータの不整合を修正します。
    -   `in` `select (arg0, arg1) in (x,y)` 、 `in`ように複数の引数を持つ場合に間違った結果が返されるバグを修正しました。
    -   MPPクエリが停止したときにTiFlashがpanicになる可能性がある問題を修正
    -   入力引数の先頭にゼロがある場合に`str_to_date`間違った結果を返す問題を修正しました
    -   フィルターが`where <string>`形式の場合にクエリが間違った結果を返す問題を修正しました
    -   入力引数`string`が`%Y-%m-%d\n%H:%i:%s`形式の場合に`cast(string as datetime)`間違った結果を返す問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作が完了した後にリージョンが不均等に分散される可能性がある問題を修正[＃31034](https://github.com/pingcap/tidb/issues/31034)

    -   ティCDC

        -   長いvarcharがエラーを報告するバグを修正`Column length too big` [＃4637](https://github.com/pingcap/tiflow/issues/4637)
        -   PDリーダーが強制終了するとTiCDCノードが異常終了するバグを修正[＃4248](https://github.com/pingcap/tiflow/issues/4248)
        -   セーフモードでの更新ステートメントの実行エラーにより DM ワーカーがpanicになる可能性がある問題を修正しました[＃4317](https://github.com/pingcap/tiflow/issues/4317)
        -   TiKVクライアントのキャッシュされたリージョンメトリックが負になる可能性がある問題を修正[＃4300](https://github.com/pingcap/tiflow/issues/4300)
        -   必要なプロセッサ情報が存在しない場合にHTTP APIがパニックになるバグを修正[＃3840](https://github.com/pingcap/tiflow/issues/3840)
        -   一時停止された変更フィード[＃4740](https://github.com/pingcap/tiflow/issues/4740)を削除するときに、REDO ログがクリーンアップされないバグを修正しました。
        -   コンテナ環境の OOM を修正[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   読み込みタスクを停止するとタスク[＃3771](https://github.com/pingcap/tiflow/issues/3771)が予期せず転送されるバグを修正
        -   ローダー[＃3252](https://github.com/pingcap/tiflow/issues/3252)の`query-status`コマンドで間違った進行状況が返される問題を修正
        -   クラスター内に異なるバージョンの TiCDC ノードがある場合に HTTP API が動作しない問題を修正[＃3483](https://github.com/pingcap/tiflow/issues/3483)
        -   S3storageが TiCDC Redo Log [＃3523](https://github.com/pingcap/tiflow/issues/3523)で構成されている場合に TiCDC が異常終了する問題を修正しました。
        -   デフォルト値を複製できない問題を修正[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正[＃4501](https://github.com/pingcap/tiflow/issues/4501)
        -   ステータス[＃4281](https://github.com/pingcap/tiflow/issues/4281)を照会するときにのみ同期メトリックが更新される問題を修正しました。
        -   `mq sink write row`監視データがない問題を修正[＃3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `min.insync.replicas` `replication-factor`より小さい場合にレプリケーションを実行できない問題を修正しました[＃3994](https://github.com/pingcap/tiflow/issues/3994)
        -   `mq sink write row`監視データがない問題を修正[＃3431](https://github.com/pingcap/tiflow/issues/3431)
        -   レプリケーションタスクが削除されたときに発生する可能性のあるpanic問題を修正[＃3128](https://github.com/pingcap/tiflow/issues/3128)
        -   デッドロックによりレプリケーションタスクが停止する可能性がある問題を修正[＃4055](https://github.com/pingcap/tiflow/issues/4055)
        -   etcd [＃2980](https://github.com/pingcap/tiflow/issues/2980)でタスク ステータスを手動でクリーンアップするときに発生する TiCDCpanicの問題を修正しました。
        -   DDL ステートメント内の特別なコメントによってレプリケーション タスクが停止する問題を修正しました[＃3755](https://github.com/pingcap/tiflow/issues/3755)
        -   `config.Metadata.Timeout` [＃3352](https://github.com/pingcap/tiflow/issues/3352)の誤った構成によって発生するレプリケーション停止の問題を修正
        -   一部の RHEL リリース[＃3584](https://github.com/pingcap/tiflow/issues/3584)でタイムゾーンの問題によりサービスを開始できない問題を修正しました。
        -   クラスターのアップグレード後に`stopped`チェンジフィードが自動的に再開される問題を修正[＃3473](https://github.com/pingcap/tiflow/issues/3473)
        -   デフォルト値を複製できない問題を修正[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   MySQLシンクデッドロック[＃2706](https://github.com/pingcap/tiflow/issues/2706)による警告が頻繁に発生する問題を修正
        -   Canalプロトコル[＃3676](https://github.com/pingcap/tiflow/issues/3676)で設定項目`enable-old-value`が`true`に自動的に設定されないバグを修正
        -   AvroシンクがJSON型列[＃3624](https://github.com/pingcap/tiflow/issues/3624)の解析をサポートしていない問題を修正
        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/tiflow/issues/3010)負の値エラーを修正

    -   TiDB データ移行 (DM)

        -   DM マスターと DM ワーカーを特定の順序で再起動した後に DM マスターのリレー ステータスが間違っているというバグを修正[＃3478](https://github.com/pingcap/tiflow/issues/3478)
        -   DM-workerが再起動後に起動に失敗するバグを修正[＃3344](https://github.com/pingcap/tiflow/issues/3344)
        -   PARTITION DDLの実行に時間がかかりすぎるとDMタスクが失敗するバグを修正[＃3854](https://github.com/pingcap/tiflow/issues/3854)
        -   アップストリームがMySQL 8.0 [＃3847](https://github.com/pingcap/tiflow/issues/3847)の場合にDMが`invalid sequence`を報告することがあるバグを修正
        -   DM がより細かい粒度の再試行を行うときにデータが失われるバグを修正[＃3487](https://github.com/pingcap/tiflow/issues/3487)
        -   `CREATE VIEW`ステートメントがデータレプリケーション[＃4173](https://github.com/pingcap/tiflow/issues/4173)を中断する問題を修正
        -   DDL ステートメントをスキップした後にスキーマをリセットする必要がある問題を修正[＃4177](https://github.com/pingcap/tiflow/issues/4177)

    -   TiDB Lightning

        -   一部のインポートタスクにソースファイルが含まれていない場合に、 TiDB Lightning がメタデータスキーマを削除しない可能性があるバグを修正しました[＃28144](https://github.com/pingcap/tidb/issues/28144)
        -   storageURL プレフィックスが「gcs://xxx」ではなく「gs://xxx」の場合にTiDB Lightning がエラーを返すバグを修正[＃32742](https://github.com/pingcap/tidb/issues/32742)
        -   --log-file=&quot;-&quot; を設定しても stdout [＃29876](https://github.com/pingcap/tidb/issues/29876)にログが出力されない問題を修正しました
        -   S3storageパスが存在しない場合にTiDB Lightning がエラーを報告しない問題を修正[＃30709](https://github.com/pingcap/tidb/issues/30709)
