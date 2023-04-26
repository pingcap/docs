---
title: TiDB 5.3.1 Release Notes
---

# TiDB 5.3.1 リリースノート {#tidb-5-3-1-release-notes}

リリース日：2022年3月3日

TiDB バージョン: 5.3.1

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiDB Lightning

        -   デフォルト値の`regionMaxKeyCount` 1_440_000 から 1_280_000 に変更して、データのインポート後に空のリージョンが多くなりすぎないようにします[#30018](https://github.com/pingcap/tidb/issues/30018)

## 改良点 {#improvements}

-   TiDB

    -   ユーザー ログイン モードのマッピング ロジックを最適化して、ロギングをより MySQL 互換にする[#30450](https://github.com/pingcap/tidb/issues/32648)

-   TiKV

    -   ロックの解決ステップ[#11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   ガベージ コレクション (GC) プロセスを高速化するには、GC をRaftログに実行するときに書き込みバッチ サイズを増やします[#11404](https://github.com/tikv/tikv/issues/11404)
    -   proc ファイルシステム (procfs) を v0.12.0 に更新します[#11702](https://github.com/tikv/tikv/issues/11702)

-   PD

    -   `DR_STATE`ファイルのコンテンツ形式を最適化する[#4341](https://github.com/tikv/pd/issues/4341)

-   ツール

    -   TiCDC

        -   Kafka プロデューサーの構成パラメーターを公開して、TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)で構成可能にする
        -   S3 がバックstorageとして使用されている場合、TiCDC の起動時に事前クリーンアップ プロセスを追加します[#3878](https://github.com/pingcap/tiflow/issues/3878)
        -   TiCDC クライアントは、証明書名が指定されていない場合に機能します[#3627](https://github.com/pingcap/tiflow/issues/3627)
        -   テーブルごとにシンク チェックポイントを管理して、予期しないチェックポイント タイムスタンプの進行を回避する[#3545](https://github.com/pingcap/tiflow/issues/3545)
        -   変更フィードを再開するための指数バックオフ メカニズムを追加します。 [#3329](https://github.com/pingcap/tiflow/issues/3329)
        -   Kafka Sink `partition-num`のデフォルト値を 3 に変更して、TiCDC が Kafka パーティション間でメッセージをより均等に分散するようにします[#3337](https://github.com/pingcap/tiflow/issues/3337)
        -   「EventFeed retry rate limited」ログのカウントを減らします[#4006](https://github.com/pingcap/tiflow/issues/4006)
        -   デフォルト値の`max-message-bytes`を 10M に設定[#4041](https://github.com/pingcap/tiflow/issues/4041)
        -   `no owner alert` 、 `mounter row` 、 `table sink total row` 、および`buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)を含む、Prometheus および Grafana のモニタリング メトリックとアラートをさらに追加します。
        -   TiKV ストアがダウンしたときに KV クライアントが回復するまでの時間を短縮する[#3191](https://github.com/pingcap/tiflow/issues/3191)

    -   TiDB Lightning

        -   ローカル ディスク容量チェックが失敗した場合に、事前チェックの出力メッセージをより使いやすいものに調整します[#30395](https://github.com/pingcap/tidb/issues/30395)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDB の`date_format`が MySQL と互換性のない方法で`'\n'`処理する問題を修正します[#32232](https://github.com/pingcap/tidb/issues/32232)
    -   `alter column set default`テーブル スキーマを誤って更新する問題を修正します[#31074](https://github.com/pingcap/tidb/issues/31074)
    -   `tidb_restricted_read_only`を有効にすると`tidb_super_read_only`が自動的に有効にならない不具合を修正[#31745](https://github.com/pingcap/tidb/issues/31745)
    -   照合順序を伴う`greatest`または`least`関数が間違った結果を取得する問題を修正します[#31789](https://github.com/pingcap/tidb/issues/31789)
    -   クエリ実行時の MPP タスク リストの空エラーを修正します[#31636](https://github.com/pingcap/tidb/issues/31636)
    -   innerWorkerpanic[#31494](https://github.com/pingcap/tidb/issues/31494)によって引き起こされたインデックス結合の誤った結果を修正
    -   列の種類を`FLOAT`から`DOUBLE`に変更した後の誤ったクエリ結果を修正する[#31372](https://github.com/pingcap/tidb/issues/31372)
    -   インデックス ルックアップ ジョイン[#30468](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`エラーを修正します。
    -   `Order By` [#30271](https://github.com/pingcap/tidb/issues/30271)の最適化による間違ったクエリ結果を修正
    -   `MaxDays`と`MaxBackups`の設定がスローログ[#25716](https://github.com/pingcap/tidb/issues/25716)に反映されない問題を修正
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanic[#28078](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正します。

-   TiKV

    -   ピア ステータスが`Applying` [#11746](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除すると発生するpanicの問題を修正します。
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定され[#11424](https://github.com/tikv/tikv/issues/11424)いる場合の QPS ドロップの問題を修正します。
    -   cgroup コントローラーがマウントされていない場合に発生するpanicの問題を修正します[#11569](https://github.com/tikv/tikv/issues/11569)
    -   TiKVの動作停止後、Resolved TSのレイテンシーが増加する問題を修正[#11351](https://github.com/tikv/tikv/issues/11351)
    -   TiKV が GC ワーカがビジー状態の場合、データの範囲を削除できない ( `unsafe_destroy_range`を実行できない) バグを修正[#11903](https://github.com/tikv/tikv/issues/11903)
    -   ピアを破棄すると高レイテンシーが発生する可能性がある問題を修正します[#10210](https://github.com/tikv/tikv/issues/10210)
    -   領域が空の場合に`any_value`関数が間違った結果を返すバグを修正[#11735](https://github.com/tikv/tikv/issues/11735)
    -   初期化されていないレプリカを削除すると、古いレプリカが再作成される可能性があるという問題を修正します[#10533](https://github.com/tikv/tikv/issues/10533)
    -   新しい選択が終了した後に`Prepare Merge`がトリガーされたが、隔離されたピアに通知されていない場合のメタデータの破損の問題を修正します[#11526](https://github.com/tikv/tikv/issues/11526)
    -   コルーチンの実行速度が速すぎる場合に時々発生するデッドロックの問題を修正します[#11549](https://github.com/tikv/tikv/issues/11549)
    -   TiKV ノードがダウンしていると、解決されたタイムスタンプが[#11351](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正します。
    -   Raftクライアント実装[#9714](https://github.com/tikv/tikv/issues/9714)でバッチ メッセージが大きすぎる問題を修正
    -   極端な状況でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[#11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKV がリバース テーブル スキャンを実行すると、TiKV がメモリロックを検出できない問題を修正します[#11440](https://github.com/tikv/tikv/issues/11440)
    -   ディスク容量がいっぱいになると、RocksDB のフラッシュまたは圧縮によってpanicが発生する問題を修正します[#11224](https://github.com/tikv/tikv/issues/11224)
    -   tikv-ctl が正しいリージョン関連の情報を返せないバグを修正[#11393](https://github.com/tikv/tikv/issues/11393)
    -   インスタンスごとの gRPC リクエストの平均レイテンシーが TiKV メトリクスで不正確である問題を修正します[#11299](https://github.com/tikv/tikv/issues/11299)

-   PD

    -   特定のケースで、スケジューリング プロセスに不要な JointConsensus ステップが含まれるバグを修正します[#4362](https://github.com/tikv/pd/issues/4362)
    -   投票者を直接降格させるとスケジューリングが実行できないバグを修正[#4444](https://github.com/tikv/pd/issues/4444)
    -   レプリカ[#4325](https://github.com/tikv/pd/issues/4325)のレプリケーション モードの構成を更新するときに発生するデータ競合の問題を修正します。
    -   特定の場合に読み取りロックが解除されない不具合を修正[#4354](https://github.com/tikv/pd/issues/4354)
    -   コールド ホットスポット データがホットスポット統計から削除できない問題を修正します[#4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   入力引数`arg` `decimal(x,y)`の範囲を超えると`cast(arg as decimal(x,y))`間違った結果を返す問題を修正
    -   `max_memory_usage`と`max_memory_usage_for_all_queries`が有効になっているときに発生するTiFlashクラッシュの問題を修正します。
    -   `cast(string as real)`が間違った結果を返す問題を修正
    -   `cast(string as decimal)`が間違った結果を返す問題を修正
    -   主キー列をより大きな int データ型に変更した後の潜在的なデータ不整合を修正
    -   `in` `select (arg0, arg1) in (x,y)`のようなステートメントで複数の引数を持っている場合、 `in`間違った結果を返すというバグを修正します
    -   MPP クエリが停止したときにTiFlash がpanicになる問題を修正
    -   入力引数の先頭にゼロがある場合に`str_to_date`が間違った結果を返す問題を修正
    -   フィルターが`where <string>`形式の場合、クエリが間違った結果を返す問題を修正します。
    -   入力引数`string` `%Y-%m-%d\n%H:%i:%s`形式の場合、 `cast(string as datetime)`が間違った結果を返す問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作の完了後にリージョンが不均一に分散される可能性があるという潜在的な問題を修正します[#31034](https://github.com/pingcap/tidb/issues/31034)

    -   TiCDC

        -   長い varchar がエラーを報告するバグを修正`Column length too big` [#4637](https://github.com/pingcap/tiflow/issues/4637)
        -   PD リーダーが強制終了されたときに TiCDC ノードが異常終了するバグを修正します[#4248](https://github.com/pingcap/tiflow/issues/4248)
        -   セーフモードで update ステートメントの実行エラーが発生すると、DM-workerpanic[#4317](https://github.com/pingcap/tiflow/issues/4317)が発生する可能性がある問題を修正します。
        -   TiKV クライアントのキャッシュされたリージョン メトリックがマイナス[#4300](https://github.com/pingcap/tiflow/issues/4300)になる可能性がある問題を修正します
        -   必要なプロセッサ情報が存在しない場合に HTTP API がパニックするバグを修正[#3840](https://github.com/pingcap/tiflow/issues/3840)
        -   一時停止中の変更フィードを削除すると、REDO ログがクリーンアップされないバグを修正します[#4740](https://github.com/pingcap/tiflow/issues/4740)
        -   コンテナ環境で OOM を修正する[#1798](https://github.com/pingcap/tiflow/issues/1798)
        -   ローディングタスクを停止するとタスクが予期せず転送されるバグを修正[#3771](https://github.com/pingcap/tiflow/issues/3771)
        -   ローダー[#3252](https://github.com/pingcap/tiflow/issues/3252)の`query-status`コマンドに対して間違った進行状況が返される問題を修正します。
        -   クラスタ内に異なるバージョンの TiCDC ノードがある場合、HTTP API が機能しない問題を修正します[#3483](https://github.com/pingcap/tiflow/issues/3483)
        -   S3storageがTiCDC Redo Log [#3523](https://github.com/pingcap/tiflow/issues/3523)で構成されている場合、TiCDC が異常終了する問題を修正します。
        -   デフォルト値をレプリケートできない問題を修正[#3793](https://github.com/pingcap/tiflow/issues/3793)
        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正します[#4501](https://github.com/pingcap/tiflow/issues/4501)
        -   ステータス[#4281](https://github.com/pingcap/tiflow/issues/4281)を照会した場合にのみ syncer メトリクスが更新される問題を修正します。
        -   `mq sink write row`監視データがない問題を修正[#3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `min.insync.replicas`が`replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)より小さい場合にレプリケーションが実行できない問題を修正
        -   `mq sink write row`監視データがない問題を修正[#3431](https://github.com/pingcap/tiflow/issues/3431)
        -   レプリケーション タスクが削除されたときに発生する潜在的なpanicの問題を修正します[#3128](https://github.com/pingcap/tiflow/issues/3128)
        -   デッドロックが原因でレプリケーション タスクがスタックする潜在的な問題を修正します[#4055](https://github.com/pingcap/tiflow/issues/4055)
        -   etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)でタスク ステータスを手動でクリーニングするときに発生する TiCDCpanicの問題を修正します。
        -   DDL ステートメントの特殊なコメントによってレプリケーション タスクが停止する問題を修正します[#3755](https://github.com/pingcap/tiflow/issues/3755)
        -   `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)の構成が正しくないために発生するレプリケーション停止の問題を修正します。
        -   一部の RHEL リリースでタイムゾーンの問題が原因でサービスを開始できない問題を修正します[#3584](https://github.com/pingcap/tiflow/issues/3584)
        -   `stopped`クラスターのアップグレード後に変更フィードが自動的に再開される問題を修正します[#3473](https://github.com/pingcap/tiflow/issues/3473)
        -   デフォルト値をレプリケートできない問題を修正[#3793](https://github.com/pingcap/tiflow/issues/3793)
        -   MySQL シンクのデッドロック[#2706](https://github.com/pingcap/tiflow/issues/2706)が原因で頻繁に警告が表示される問題を修正
        -   Canal および Maxwell プロトコル[#3676](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`構成項目が自動的に`true`に設定されないバグを修正
        -   Avro シンクが JSON 型の列の解析をサポートしていない問題を修正します[#3624](https://github.com/pingcap/tiflow/issues/3624)
        -   changefeed チェックポイントラグ[#3010](https://github.com/pingcap/tiflow/issues/3010)の負の値のエラーを修正します。

    -   TiDB データ移行 (DM)

        -   DM-master と DM-worker を特定の順序で再起動した後、DM-master のリレー ステータスが間違っているというバグを修正します[#3478](https://github.com/pingcap/tiflow/issues/3478)
        -   再起動後に DM-worker が起動しないバグを修正[#3344](https://github.com/pingcap/tiflow/issues/3344)
        -   PARTITION DDL の実行に時間がかかりすぎると DM タスクが失敗するバグを修正します[#3854](https://github.com/pingcap/tiflow/issues/3854)
        -   アップストリームが MySQL 8.0 [#3847](https://github.com/pingcap/tiflow/issues/3847)の場合に DM が`invalid sequence`を報告することがあるバグを修正
        -   DM がよりきめ細かい再試行を行うと、データが失われるバグを修正します[#3487](https://github.com/pingcap/tiflow/issues/3487)
        -   `CREATE VIEW`ステートメントがデータ レプリケーションを中断する問題を修正します[#4173](https://github.com/pingcap/tiflow/issues/4173)
        -   DDL ステートメントがスキップされた後にスキーマをリセットする必要がある問題を修正します[#4177](https://github.com/pingcap/tiflow/issues/4177)

    -   TiDB Lightning

        -   一部のインポート タスクにソース ファイルが含まれていない場合、 TiDB Lightning がメタデータ スキーマを削除しないことがあるというバグを修正します[#28144](https://github.com/pingcap/tidb/issues/28144)
        -   storageURL のプレフィックスが「gcs://xxx」ではなく「gs://xxx」の場合、 TiDB Lightning がエラーを返すバグを修正[#32742](https://github.com/pingcap/tidb/issues/32742)
        -   --log-file=&quot;-&quot; を設定してもログが stdout [#29876](https://github.com/pingcap/tidb/issues/29876)に出力されない問題を修正します。
        -   S3storageパスが存在しない場合にTiDB Lightning がエラーを報告しない問題を修正します[#30709](https://github.com/pingcap/tidb/issues/30709)
