---
title: TiDB 5.3.1 Release Notes
---

# TiDB 5.3.1 リリースノート {#tidb-5-3-1-release-notes}

リリース日：2022年3月3日

TiDB バージョン: 5.3.1

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiDB Lightning

        -   データ インポート[<a href="https://github.com/pingcap/tidb/issues/30018">#30018</a>](https://github.com/pingcap/tidb/issues/30018)後に空のリージョンが多すぎるのを避けるために、デフォルト値`regionMaxKeyCount`を 1_440_000 から 1_280_000 に変更します。

## 改善点 {#improvements}

-   TiDB

    -   ユーザー ログイン モードのマッピング ロジックを最適化して、ログの MySQL 互換性を高めます[<a href="https://github.com/pingcap/tidb/issues/32648">#30450</a>](https://github.com/pingcap/tidb/issues/32648)

-   TiKV

    -   ロックの解決ステップ[<a href="https://github.com/tikv/tikv/issues/11993">#11993</a>](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   Raftログへの GC を実行するときに書き込みバッチ サイズを増やすことで、ガベージ コレクション (GC) プロセスを高速化します[<a href="https://github.com/tikv/tikv/issues/11404">#11404</a>](https://github.com/tikv/tikv/issues/11404)
    -   proc ファイルシステム (procfs) を v0.12.0 に更新します[<a href="https://github.com/tikv/tikv/issues/11702">#11702</a>](https://github.com/tikv/tikv/issues/11702)

-   PD

    -   `DR_STATE`ファイルのコンテンツ形式を最適化する[<a href="https://github.com/tikv/pd/issues/4341">#4341</a>](https://github.com/tikv/pd/issues/4341)

-   ツール

    -   TiCDC

        -   Kafka プロデューサの構成パラメータを公開して、TiCDC [<a href="https://github.com/pingcap/tiflow/issues/4385">#4385</a>](https://github.com/pingcap/tiflow/issues/4385)で構成できるようにします。
        -   S3 がバックstorage[<a href="https://github.com/pingcap/tiflow/issues/3878">#3878</a>](https://github.com/pingcap/tiflow/issues/3878)として使用されている場合、TiCDC 起動時にプレクリーンアップ プロセスを追加します。
        -   TiCDC クライアントは、証明書名が指定されていない場合でも機能します[<a href="https://github.com/pingcap/tiflow/issues/3627">#3627</a>](https://github.com/pingcap/tiflow/issues/3627)
        -   テーブルごとにシンク チェックポイントを管理して、チェックポイントのタイムスタンプが予期せず進むことを回避します[<a href="https://github.com/pingcap/tiflow/issues/3545">#3545</a>](https://github.com/pingcap/tiflow/issues/3545)
        -   変更フィードを再開するための指数バックオフ メカニズムを追加します。 [<a href="https://github.com/pingcap/tiflow/issues/3329">#3329</a>](https://github.com/pingcap/tiflow/issues/3329)
        -   TiCDC が Kafka パーティション間でメッセージをより均等に分散できるように、Kafka Sink のデフォルト値`partition-num`を[<a href="https://github.com/pingcap/tiflow/issues/3337">#3337</a>](https://github.com/pingcap/tiflow/issues/3337)に変更します。
        -   「EventFeed 再試行速度制限」ログの数を減らす[<a href="https://github.com/pingcap/tiflow/issues/4006">#4006</a>](https://github.com/pingcap/tiflow/issues/4006)
        -   デフォルト値の`max-message-bytes`を 10M [<a href="https://github.com/pingcap/tiflow/issues/4041">#4041</a>](https://github.com/pingcap/tiflow/issues/4041)に設定します。
        -   `no owner alert` 、 `mounter row` 、 `table sink total row` 、 `buffer sink total row`などの Prometheus および Grafana モニタリング メトリックとアラートを追加します[<a href="https://github.com/pingcap/tiflow/issues/4054">#4054</a>](https://github.com/pingcap/tiflow/issues/4054) [<a href="https://github.com/pingcap/tiflow/issues/1606">#1606</a>](https://github.com/pingcap/tiflow/issues/1606)
        -   TiKV ストアがダウンした場合に KV クライアントが回復するまでの時間を短縮します[<a href="https://github.com/pingcap/tiflow/issues/3191">#3191</a>](https://github.com/pingcap/tiflow/issues/3191)

    -   TiDB Lightning

        -   ローカル ディスク領域チェックが失敗した場合の事前チェックの出力メッセージをより使いやすく改良しました[<a href="https://github.com/pingcap/tidb/issues/30395">#30395</a>](https://github.com/pingcap/tidb/issues/30395)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDB の`date_format`が MySQL と互換性のない方法で`'\n'`処理する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/32232">#32232</a>](https://github.com/pingcap/tidb/issues/32232)
    -   `alter column set default`テーブル スキーマが誤って更新される問題を修正[<a href="https://github.com/pingcap/tidb/issues/31074">#31074</a>](https://github.com/pingcap/tidb/issues/31074)
    -   `tidb_restricted_read_only`を有効にすると`tidb_super_read_only`が自動的に有効にならないバグを修正[<a href="https://github.com/pingcap/tidb/issues/31745">#31745</a>](https://github.com/pingcap/tidb/issues/31745)
    -   照合順序のある`greatest`または`least`関数が間違った結果を取得する問題を修正[<a href="https://github.com/pingcap/tidb/issues/31789">#31789</a>](https://github.com/pingcap/tidb/issues/31789)
    -   クエリ[<a href="https://github.com/pingcap/tidb/issues/31636">#31636</a>](https://github.com/pingcap/tidb/issues/31636)を実行するときの MPP タスク リストが空のエラーを修正しました。
    -   innerWorkerpanic[<a href="https://github.com/pingcap/tidb/issues/31494">#31494</a>](https://github.com/pingcap/tidb/issues/31494)によって引き起こされるインデックス結合の間違った結果を修正します。
    -   列タイプを`FLOAT`から`DOUBLE`に変更した後の誤ったクエリ結果を修正します[<a href="https://github.com/pingcap/tidb/issues/31372">#31372</a>](https://github.com/pingcap/tidb/issues/31372)
    -   インデックス検索結合[<a href="https://github.com/pingcap/tidb/issues/30468">#30468</a>](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`エラーを修正しました。
    -   `Order By` [<a href="https://github.com/pingcap/tidb/issues/30271">#30271</a>](https://github.com/pingcap/tidb/issues/30271)の最適化による間違ったクエリ結果を修正
    -   スローログ[<a href="https://github.com/pingcap/tidb/issues/25716">#25716</a>](https://github.com/pingcap/tidb/issues/25716)では`MaxDays`と`MaxBackups`の設定が反映されない問題を修正
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanic[<a href="https://github.com/pingcap/tidb/issues/28078">#28078</a>](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正

-   TiKV

    -   ピアのステータスが`Applying` [<a href="https://github.com/tikv/tikv/issues/11746">#11746</a>](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除することによって引き起こされるpanicの問題を修正します。
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定されている場合の QPS ドロップの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11424">#11424</a>](https://github.com/tikv/tikv/issues/11424)
    -   cgroup コントローラーがマウントされていないときに発生するpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11569">#11569</a>](https://github.com/tikv/tikv/issues/11569)
    -   TiKVの動作停止後にResolved TSのレイテンシーが増加する問題を修正[<a href="https://github.com/tikv/tikv/issues/11351">#11351</a>](https://github.com/tikv/tikv/issues/11351)
    -   GC ワーカーがビジー状態の場合、TiKV がデータ範囲を削除できない ( `unsafe_destroy_range`は実行できない) バグを修正[<a href="https://github.com/tikv/tikv/issues/11903">#11903</a>](https://github.com/tikv/tikv/issues/11903)
    -   ピアを破棄するとレイテンシーが長くなる可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/10210">#10210</a>](https://github.com/tikv/tikv/issues/10210)
    -   `any_value`領域が空の場合に関数が間違った結果を返すバグを修正[<a href="https://github.com/tikv/tikv/issues/11735">#11735</a>](https://github.com/tikv/tikv/issues/11735)
    -   初期化されていないレプリカを削除すると古いレプリカが再作成される可能性がある問題を修正します[<a href="https://github.com/tikv/tikv/issues/10533">#10533</a>](https://github.com/tikv/tikv/issues/10533)
    -   新しい選択が完了した後に`Prepare Merge`がトリガーされたが、分離されたピアに通知されなかった場合のメタデータ破損の問題を修正します[<a href="https://github.com/tikv/tikv/issues/11526">#11526</a>](https://github.com/tikv/tikv/issues/11526)
    -   コルーチンの実行が速すぎる場合に時折発生するデッドロックの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11549">#11549</a>](https://github.com/tikv/tikv/issues/11549)
    -   TiKV ノードがダウンすると解決されたタイムスタンプが[<a href="https://github.com/tikv/tikv/issues/11351">#11351</a>](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正
    -   Raftクライアント実装[<a href="https://github.com/tikv/tikv/issues/9714">#9714</a>](https://github.com/tikv/tikv/issues/9714)でバッチメッセージが大きすぎる問題を修正
    -   極端な条件でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11475">#11475</a>](https://github.com/tikv/tikv/issues/11475)
    -   TiKV が逆テーブル スキャンを実行するときに TiKV がメモリロックを検出できない問題を修正します[<a href="https://github.com/tikv/tikv/issues/11440">#11440</a>](https://github.com/tikv/tikv/issues/11440)
    -   ディスク容量がいっぱいの場合、RocksDB のフラッシュまたは圧縮によってpanicが発生する問題を修正します[<a href="https://github.com/tikv/tikv/issues/11224">#11224</a>](https://github.com/tikv/tikv/issues/11224)
    -   tikv-ctl が正しいリージョン関連情報を返せないバグを修正[<a href="https://github.com/tikv/tikv/issues/11393">#11393</a>](https://github.com/tikv/tikv/issues/11393)
    -   TiKV メトリクス[<a href="https://github.com/tikv/tikv/issues/11299">#11299</a>](https://github.com/tikv/tikv/issues/11299)でインスタンスごとの gRPC リクエストの平均レイテンシーが不正確である問題を修正します。

-   PD

    -   特定のケースでスケジューリングプロセスに不要な JointConsensus ステップが含まれるバグを修正[<a href="https://github.com/tikv/pd/issues/4362">#4362</a>](https://github.com/tikv/pd/issues/4362)
    -   投票者を直接降格するとスケジュールが実行できないバグを修正[<a href="https://github.com/tikv/pd/issues/4444">#4444</a>](https://github.com/tikv/pd/issues/4444)
    -   レプリカ[<a href="https://github.com/tikv/pd/issues/4325">#4325</a>](https://github.com/tikv/pd/issues/4325)のレプリケーション モードの構成を更新するときに発生するデータ競合の問題を修正します。
    -   特定の場合に読み取りロックが解除されないバグを修正[<a href="https://github.com/tikv/pd/issues/4354">#4354</a>](https://github.com/tikv/pd/issues/4354)
    -   コールド ホットスポット データがホットスポット統計[<a href="https://github.com/tikv/pd/issues/4390">#4390</a>](https://github.com/tikv/pd/issues/4390)から削除できない問題を修正します。

-   TiFlash

    -   入力引数`arg` `decimal(x,y)`の範囲をオーバーフローした場合、 `cast(arg as decimal(x,y))`が間違った結果を返す問題を修正
    -   `max_memory_usage`と`max_memory_usage_for_all_queries`が有効になっている場合に発生するTiFlashクラッシュの問題を修正
    -   `cast(string as real)`が間違った結果を返す問題を修正
    -   `cast(string as decimal)`が間違った結果を返す問題を修正
    -   主キー列をより大きな int データ型に変更した後の潜在的なデータの不整合を修正
    -   `select (arg0, arg1) in (x,y)` 、 `in`などのステートメントで`in`複数の引数がある場合に間違った結果が返されるバグを修正
    -   MPP クエリが停止するとTiFlash がpanicになる問題を修正
    -   入力引数の先頭にゼロがある場合に`str_to_date`が間違った結果を返す問題を修正
    -   フィルターが`where <string>`形式の場合、クエリが間違った結果を返す問題を修正します。
    -   入力引数`string` `%Y-%m-%d\n%H:%i:%s`形式の場合、 `cast(string as datetime)`が間違った結果を返す問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作の終了後にリージョンが不均一に分散される可能性がある潜在的な問題を修正します[<a href="https://github.com/pingcap/tidb/issues/31034">#31034</a>](https://github.com/pingcap/tidb/issues/31034)

    -   TiCDC

        -   long varchar がエラーを報告するバグを修正`Column length too big` [<a href="https://github.com/pingcap/tiflow/issues/4637">#4637</a>](https://github.com/pingcap/tiflow/issues/4637)
        -   PDリーダーがキルされた場合にTiCDCノードが異常終了するバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4248">#4248</a>](https://github.com/pingcap/tiflow/issues/4248)
        -   セーフモードでの更新ステートメントの実行エラーにより DM ワーカーpanic[<a href="https://github.com/pingcap/tiflow/issues/4317">#4317</a>](https://github.com/pingcap/tiflow/issues/4317)が発生する可能性がある問題を修正します。
        -   TiKV クライアントのキャッシュされたリージョン メトリックがマイナス[<a href="https://github.com/pingcap/tiflow/issues/4300">#4300</a>](https://github.com/pingcap/tiflow/issues/4300)になる可能性がある問題を修正
        -   必要なプロセッサ情報が存在しない場合にHTTP APIがパニックするバグを修正[<a href="https://github.com/pingcap/tiflow/issues/3840">#3840</a>](https://github.com/pingcap/tiflow/issues/3840)
        -   一時停止されたチェンジフィード[<a href="https://github.com/pingcap/tiflow/issues/4740">#4740</a>](https://github.com/pingcap/tiflow/issues/4740)を削除するときに REDO ログがクリーンアップされないバグを修正
        -   コンテナ環境での OOM の修正[<a href="https://github.com/pingcap/tiflow/issues/1798">#1798</a>](https://github.com/pingcap/tiflow/issues/1798)
        -   ロードタスクを停止するとタスク[<a href="https://github.com/pingcap/tiflow/issues/3771">#3771</a>](https://github.com/pingcap/tiflow/issues/3771)が予期せず転送されるバグを修正
        -   ローダー[<a href="https://github.com/pingcap/tiflow/issues/3252">#3252</a>](https://github.com/pingcap/tiflow/issues/3252)の`query-status`コマンドに対して間違った進行状況が返される問題を修正
        -   クラスター内に異なるバージョンの TiCDC ノードがある場合、HTTP API が機能しない問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3483">#3483</a>](https://github.com/pingcap/tiflow/issues/3483)
        -   S3storageがTiCDC Redo Log [<a href="https://github.com/pingcap/tiflow/issues/3523">#3523</a>](https://github.com/pingcap/tiflow/issues/3523)で構成されている場合に TiCDC が異常終了する問題を修正
        -   デフォルト値を複製できない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3793">#3793</a>](https://github.com/pingcap/tiflow/issues/3793)
        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4501">#4501</a>](https://github.com/pingcap/tiflow/issues/4501)
        -   ステータス[<a href="https://github.com/pingcap/tiflow/issues/4281">#4281</a>](https://github.com/pingcap/tiflow/issues/4281)をクエリする場合にのみ同期メトリクスが更新される問題を修正
        -   `mq sink write row`監視データがない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3431">#3431</a>](https://github.com/pingcap/tiflow/issues/3431)
        -   `min.insync.replicas`が`replication-factor` [<a href="https://github.com/pingcap/tiflow/issues/3994">#3994</a>](https://github.com/pingcap/tiflow/issues/3994)より小さい場合にレプリケーションが実行できない問題を修正
        -   `mq sink write row`監視データがない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3431">#3431</a>](https://github.com/pingcap/tiflow/issues/3431)
        -   レプリケーション タスクが削除されたときに発生する潜在的なpanicの問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3128">#3128</a>](https://github.com/pingcap/tiflow/issues/3128)
        -   デッドロックによりレプリケーション タスクが停止するという潜在的な問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4055">#4055</a>](https://github.com/pingcap/tiflow/issues/4055)
        -   etcd [<a href="https://github.com/pingcap/tiflow/issues/2980">#2980</a>](https://github.com/pingcap/tiflow/issues/2980)でタスクステータスを手動でクリーンアップするときに発生する TiCDCpanicの問題を修正します。
        -   DDL ステートメント内の特別なコメントによりレプリケーション タスクが停止する問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3755">#3755</a>](https://github.com/pingcap/tiflow/issues/3755)
        -   `config.Metadata.Timeout` [<a href="https://github.com/pingcap/tiflow/issues/3352">#3352</a>](https://github.com/pingcap/tiflow/issues/3352)の誤った構成によって引き起こされるレプリケーション停止の問題を修正します。
        -   一部の RHEL リリースでタイムゾーンの問題が原因でサービスを開始できない問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3584">#3584</a>](https://github.com/pingcap/tiflow/issues/3584)
        -   `stopped`クラスターのアップグレード後に変更フィードが自動的に再開される問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3473">#3473</a>](https://github.com/pingcap/tiflow/issues/3473)
        -   デフォルト値を複製できない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3793">#3793</a>](https://github.com/pingcap/tiflow/issues/3793)
        -   MySQL シンクのデッドロックによって引き起こされる過度に頻繁な警告の問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/2706">#2706</a>](https://github.com/pingcap/tiflow/issues/2706)
        -   Canal および Maxwell プロトコル[<a href="https://github.com/pingcap/tiflow/issues/3676">#3676</a>](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`設定項目が自動的に`true`に設定されないバグを修正
        -   Avro シンクが JSON 型列の解析をサポートしていない問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3624">#3624</a>](https://github.com/pingcap/tiflow/issues/3624)
        -   チェンジフィードチェックポイントラグ[<a href="https://github.com/pingcap/tiflow/issues/3010">#3010</a>](https://github.com/pingcap/tiflow/issues/3010)の負の値エラーを修正

    -   TiDB データ移行 (DM)

        -   DMマスターとDMワーカーを特定の順序で再起動するとDMマスターの中継ステータスがおかしくなるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/3478">#3478</a>](https://github.com/pingcap/tiflow/issues/3478)
        -   再起動後にDM-workerが起動しないバグを修正[<a href="https://github.com/pingcap/tiflow/issues/3344">#3344</a>](https://github.com/pingcap/tiflow/issues/3344)
        -   PARTITION DDL の実行に時間がかかりすぎると DM タスクが失敗するバグを修正[<a href="https://github.com/pingcap/tiflow/issues/3854">#3854</a>](https://github.com/pingcap/tiflow/issues/3854)
        -   アップストリームが MySQL 8.0 [<a href="https://github.com/pingcap/tiflow/issues/3847">#3847</a>](https://github.com/pingcap/tiflow/issues/3847)の場合、DM が`invalid sequence`を報告することがあるバグを修正
        -   DM がより詳細な再試行を行うときにデータが失われるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/3487">#3487</a>](https://github.com/pingcap/tiflow/issues/3487)
        -   `CREATE VIEW`ステートメントがデータ レプリケーション[<a href="https://github.com/pingcap/tiflow/issues/4173">#4173</a>](https://github.com/pingcap/tiflow/issues/4173)を中断する問題を修正します。
        -   DDL ステートメントがスキップされた後にスキーマをリセットする必要がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4177">#4177</a>](https://github.com/pingcap/tiflow/issues/4177)

    -   TiDB Lightning

        -   一部のインポートタスクにソースファイルが含まれていない場合、 TiDB Lightning がメタデータスキーマを削除できないことがあるバグを修正[<a href="https://github.com/pingcap/tidb/issues/28144">#28144</a>](https://github.com/pingcap/tidb/issues/28144)
        -   storageURL プレフィックスが「gcs://xxx」ではなく「gs://xxx」の場合、 TiDB Lightning がエラーを返すバグを修正します[<a href="https://github.com/pingcap/tidb/issues/32742">#32742</a>](https://github.com/pingcap/tidb/issues/32742)
        -   --log-file=&quot;-&quot; を設定しても stdout [<a href="https://github.com/pingcap/tidb/issues/29876">#29876</a>](https://github.com/pingcap/tidb/issues/29876)にログが出力されない問題を修正
        -   S3storageパスが存在しない場合にTiDB Lightning がエラーを報告しない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30709">#30709</a>](https://github.com/pingcap/tidb/issues/30709)
