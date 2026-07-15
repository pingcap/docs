---
title: TiDB 8.1.2 Release Notes
summary: TiDB 8.1.2 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 8.1.2 リリースノート {#tidb-8-1-2-release-notes}

発売日：2024年12月26日

TiDB バージョン: 8.1.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiKV設定項目[`server.snap-min-ingest-size`](/tikv-configuration-file.md#snap-min-ingest-size-new-in-v812)を追加します。これは、TiKVがスナップショットを処理する際にインジェスト方式を採用するかどうかの最小しきい値を指定します。デフォルト値は`2MiB`です。

    -   スナップショットのサイズがこのしきい値を超えると、TiKVはスナップショットからSSTファイルをRocksDBにインポートするインジェスト方式を採用します。この方式は、大きなファイルの場合、より高速です。
    -   スナップショットのサイズがこのしきい値を超えない場合、TiKVは直接書き込み方式を採用し、各データをRocksDBに個別に書き込みます。この方式は、小さなファイルの場合により効率的です。

## 改善点 {#improvements}

-   TiDB

    -   リクエストユニット（RU）設定に関するメトリックを追加します [＃8444](https://github.com/tikv/pd/issues/8444) @ [nolouch](https://github.com/nolouch)

-   TiKV

    -   空のテーブルと小さなリージョンのシナリオでのリージョン結合の速度を向上 [＃17376](https://github.com/tikv/tikv/issues/17376) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   TiKVの`DiskFull`検出を最適化してRaftEngineの`spill-dir`構成と互換性を持たせ、この機能が一貫して動作することを保証します。 [＃17356](https://github.com/tikv/tikv/issues/17356) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   RocksDB 圧縮のトリガー メカニズムを最適化し、多数の DELETE バージョンを処理するときにディスク領域の再利用を高速化します。 [＃17269](https://github.com/tikv/tikv/issues/17269) @ [AndreMouche](https://github.com/AndreMouche)
    -   `import.num-threads`構成項目を動的に変更するサポート[＃17807](https://github.com/tikv/tikv/issues/17807) @ [RidRisR](https://github.com/RidRisR)
    -   Rusoto ライブラリを AWS Rust SDK に置き換えて、バックアップと復元のために外部ストレージ(Amazon S3 など) にアクセスします。これにより、IMDSv2 や EKS Pod Identity などの AWS 機能との互換性が向上します。 [＃12371](https://github.com/tikv/tikv/issues/12371) @ [akoshchiy](https://github.com/akoshchiy)

-   TiFlash

    -   クラスター化インデックスを持つテーブルで、バックグラウンドでの古いデータのガベージコレクションの速度が向上しました。 [＃9529](https://github.com/pingcap/tiflash/issues/9529) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   TLS を有効にした後に証明書を更新することでTiFlash がpanic可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [windtalker](https://github.com/windtalker)
    -   分散ストレージとコンピューティング要求を処理するときにTiFlash が作成する必要があるスレッドの数を減らし、大量のそのような要求を処理するときにTiFlashコンピューティングノードのクラッシュを回避するのに役立ちます[＃9334](https://github.com/pingcap/tiflash/issues/9334) @ [JinheLin](https://github.com/JinheLin)
    -   JOIN演算子のキャンセルメカニズムを改善し、JOIN演算子がキャンセル要求にタイムリーに応答できるようにします[＃9430](https://github.com/pingcap/tiflash/issues/9430) @ [windtalker](https://github.com/windtalker)
    -   `LENGTH()`と`ASCII()`関数の実行効率を最適化 [＃9344](https://github.com/pingcap/tiflash/issues/9344) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   分散ストレージおよびコンピューティングアーキテクチャ内のTiFlashコンピューティングノードの再試行戦略を最適化して、Amazon S3 からファイルをダウンロードする際の例外を処理します。 [＃9695](https://github.com/pingcap/tiflash/issues/9695) @ [JinheLin](https://github.com/JinheLin)

-   ツール

    -   Backup & Restore (BR)

        -   バックアップ中の不要なログ出力を削減[＃55902](https://github.com/pingcap/tidb/issues/55902) @ [Leavrth](https://github.com/Leavrth)
        -   バックアップパフォーマンスを向上させるために、フルバックアップ中のテーブルレベルのチェックサム計算（ `--checksum=false` ）をデフォルトで無効にする[＃56373](https://github.com/pingcap/tidb/issues/56373) @ [Tristan1900](https://github.com/Tristan1900)

    -   TiCDC

        -   TiCDCは、 `SUPER`権限を付与された後に非同期で実行されたDDLタスクのステータスを照会することをサポートし、同じテーブルでDDLタスクを繰り返し実行することによって発生する実行エラーを防止します。 [＃11521](https://github.com/pingcap/tiflow/issues/11521) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   下流が`SUPER`権限が付与されたTiDBの場合、TiCDCは下流データベースから`ADD INDEX DDL`の実行ステータスを照会することをサポートします。これにより、DDL文の実行を再試行する際のタイムアウトによるデータ複製の失敗を回避できる場合があります。 [＃10682](https://github.com/pingcap/tiflow/issues/10682) @ [CharlesCheung96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   v6.5からv7.5以降にアップグレードされたクラスターで、既存のTTLタスクが予期せず頻繁に実行される問題を修正[＃56539](https://github.com/pingcap/tidb/issues/56539) @ [lcwangchao](https://github.com/lcwangchao)
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [zimulala](https://github.com/zimulala)
    -   グローバルソートが有効でリージョンサイズが96 MiB を超えると`IMPORT INTO`実行が停止する問題を修正 [＃55374](https://github.com/pingcap/tidb/issues/55374) @ [lance6716](https://github.com/lance6716)
    -   `DUMP STATS`統計を JSON に変換するときにヒストグラムの上限と下限が壊れる問題を修正 [＃56083](https://github.com/pingcap/tidb/issues/56083) @ [hawkingrei](https://github.com/hawkingrei)
    -   エイリアスを持つマルチテーブル`DELETE`ステートメントに対して実行プラン バインディングを作成できない問題を修正しました。 [＃56726](https://github.com/pingcap/tidb/issues/56726) @ [hawkingrei](https://github.com/hawkingrei)
    -   TTLテーブルのメモリリークの問題を修正 [＃56934](https://github.com/pingcap/tidb/issues/56934) @ [lcwangchao](https://github.com/lcwangchao)
    -   パーティション式が`EXTRACT(YEAR FROM col)` の場合にパーティションプルーニングが機能しない問題を修正しました [＃54210](https://github.com/pingcap/tidb/issues/54210) @ [mjonss](https://github.com/mjonss)
    -   配置ルールを含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。 [＃54961](https://github.com/pingcap/tidb/issues/54961) @ [hawkingrei](https://github.com/hawkingrei)
    -   メモリ使用量が`tidb_mem_quota_query` で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [yibin87](https://github.com/yibin87)
    -   copタスク構築中にTiDBクエリをキャンセルできない問題を修正 [＃55957](https://github.com/pingcap/tidb/issues/55957) @ [yibin87](https://github.com/yibin87)
    -   TTLジョブ実行中に値を`tidb_ttl_delete_worker_count`減らすとジョブが完了しなくなる問題を修正しました [＃55561](https://github.com/pingcap/tidb/issues/55561) @ [lcwangchao](https://github.com/lcwangchao)
    -   `CAST`関数が文字セットの明示的な設定をサポートしていない問題を修正しました [＃55677](https://github.com/pingcap/tidb/issues/55677) @ [Defined2014](https://github.com/Defined2014)
    -   書き込み競合が発生したときにTTLタスクをキャンセルできない問題を修正[＃56422](https://github.com/pingcap/tidb/issues/56422) @ [YangKeao](https://github.com/YangKeao)
    -   `IndexNestedLoopHashJoin` のデータ競合問題を修正 [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [solotzg](https://github.com/solotzg)
    -   `StreamAggExec`分の`groupOffset`空の場合に TiDB がpanicを起こす可能性がある問題を修正しました [＃53867](https://github.com/pingcap/tidb/issues/53867) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   相関サブクエリと CTE を含むクエリを実行すると、TiDB がハングしたり、誤った結果が返されたりする問題を修正しました。 [＃55551](https://github.com/pingcap/tidb/issues/55551) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   インデックス追加中の再試行によって発生するデータ インデックスの不整合の問題を修正しました [＃55808](https://github.com/pingcap/tidb/issues/55808) @ [lance6716](https://github.com/lance6716)
    -   整数型の列に小さい表示幅を指定すると`out of range`エラーが発生する可能性がある問題を修正しました。 [＃55837](https://github.com/pingcap/tidb/issues/55837) @ [windtalker](https://github.com/windtalker)
    -   `LOAD DATA ... REPLACE INTO`操作でデータの不整合が発生する問題を修正[＃56408](https://github.com/pingcap/tidb/issues/56408) @ [fzzf678](https://github.com/fzzf678)
    -   `columnEvaluator`入力チャンク内の列参照を識別できず、SQL 文を実行すると`runtime error: index out of range`が発生する問題を修正しました。 [＃53713](https://github.com/pingcap/tidb/issues/53713) @ [AilinKid](https://github.com/AilinKid)
    -   共通テーブル式 (CTE) に複数のデータ コンシューマーがあり、1 つのコンシューマーがデータを読み取らずに終了した場合に発生する可能性のある無効なメモリアクセスの問題を修正しました[＃55881](https://github.com/pingcap/tidb/issues/55881) @ [windtalker](https://github.com/windtalker)
    -   TTLタスクをキャンセルした際に、対応するSQLが強制終了されない問題を修正[＃56511](https://github.com/pingcap/tidb/issues/56511) @ [lcwangchao](https://github.com/lcwangchao)
    -   `IMPORT INTO`文を使用して一時テーブルをインポートするときに TiDB がパニックになる問題を修正しました [＃55970](https://github.com/pingcap/tidb/issues/55970) @ [D3Hunter](https://github.com/D3Hunter)
    -   クエリ条件`column IS NULL` で一意インデックスにアクセスするときに、オプティマイザが行数を誤って 1 と推定する問題を修正しました。 [＃56116](https://github.com/pingcap/tidb/issues/56116) @ [hawkingrei](https://github.com/hawkingrei)
    -   情報スキーマキャッシュミスにより、古い読み取りのクエリレイテンシーが増加する問題を修正しました。 [＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)
    -   `UPDATE`文が`ENUM`型の値を誤って更新する問題を修正しました [＃56832](https://github.com/pingcap/tidb/issues/56832) @ [xhebox](https://github.com/xhebox)
    -   外部キーを含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。 [＃56456](https://github.com/pingcap/tidb/issues/56456) @ [hawkingrei](https://github.com/hawkingrei)
    -   `tidb_ttl_job_enable`変数が無効になった後、TTL タスクがキャンセルされない問題を修正[＃57404](https://github.com/pingcap/tidb/issues/57404) @ [YangKeao](https://github.com/YangKeao)
    -   `UPDATE`または`DELETE`ステートメントに再帰 CTE が含まれている場合、ステートメントがエラーを報告したり、 が有効にならない可能性がある問題を修正しました。 [＃55666](https://github.com/pingcap/tidb/issues/55666) @ [time-and-fate](https://github.com/time-and-fate)
    -   `INFORMATION_SCHEMA.STATISTICS`テーブルの`SUB_PART`値が`NULL` になる問題を修正しました [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [Defined2014](https://github.com/Defined2014)
    -   TiFlashシステムテーブルを照会するためのデフォルトのタイムアウトが短すぎる問題を修正[＃57816](https://github.com/pingcap/tidb/issues/57816) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   `default_collation_for_utf8mb4`変数の値が`SET NAMES`ステートメントで機能しない問題を修正しました [＃56439](https://github.com/pingcap/tidb/issues/56439) @ [Defined2014](https://github.com/Defined2014)
    -   `mysql.tidb_timer`テーブルでタイマーを手動で削除すると、TTL 内部コルーチンがpanicになる可能性がある問題を修正しました。 [＃57112](https://github.com/pingcap/tidb/issues/57112) @ [lcwangchao](https://github.com/lcwangchao)
    -   `tidb_ddl_enable_fast_reorg`経由で`ADD INDEX`と`CREATE INDEX`の加速を有効にすると、 `Duplicate entry`エラーが発生する可能性がある問題を修正しました。 [＃49233](https://github.com/pingcap/tidb/issues/49233) @ [lance6716](https://github.com/lance6716)
    -   大規模なテーブルに非分散方式でインデックスを追加するときにインデックスのタイムスタンプが`0`に設定される問題を修正[＃57980](https://github.com/pingcap/tidb/issues/57980) @ [lance6716](https://github.com/lance6716)

-   TiKV

    -   構成`resolved-ts.advance-ts-interval`有効にならないため、TiKV が再起動すると、TiCDC のレプリケーションレイテンシーと Point-in-time Recovery (PITR) が大幅に増加する問題を修正しました。 [＃17107](https://github.com/tikv/tikv/issues/17107) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   リソース制御をトリガーするときに一部のタスクで高いテールレイテンシーが発生する問題を修正しました [＃17589](https://github.com/tikv/tikv/issues/17589) @ [glorv](https://github.com/glorv)
    -   リージョンをマージすると稀に TiKV がpanicを起こす可能性がある問題を修正[＃17840](https://github.com/tikv/tikv/issues/17840) @ [glorv](https://github.com/glorv)
    -   ディスクがスタックしているときに TiKV が PD にハートビートを報告できない問題を修正しました [＃17939](https://github.com/tikv/tikv/issues/17939) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   Raftと RocksDB が異なるディスクにデプロイされている場合、RocksDB が配置されているディスクでは低速ディスク検出が機能しない問題を修正[＃17884](https://github.com/tikv/tikv/issues/17884) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカの即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。 [＃17469](https://github.com/tikv/tikv/issues/17469) @ [hbisheng](https://github.com/hbisheng)
    -   `RADIANS()`または`DEGREES()`関数を含むクエリを実行するとTiKVがpanic可能性がある問題を修正しました[＃17852](https://github.com/tikv/tikv/issues/17852) @ [gengliqi](https://github.com/gengliqi)
    -   多数のトランザクションが同じキーのロック解除待ち行列に入っていて、キーが頻繁に更新される場合、デッドロック検出への過度の圧力によって TiKV OOM 問題が発生する可能性がある問題を修正しました [＃17394](https://github.com/tikv/tikv/issues/17394) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   リージョンを[＃17602](https://github.com/tikv/tikv/issues/17602) @ [LykxSassinator](https://github.com/LykxSassinator)に分割した後、リーダーをすぐに選出できない問題を修正しました
    -   読み取りスレッドがRaft EngineのMemTable内の古いインデックスにアクセスしたときに発生するpanic問題を修正しました。 [＃17383](https://github.com/tikv/tikv/issues/17383) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   大きなテーブルやパーティションを削除した後に発生する可能性のあるフロー制御の問題を修正しました [＃17304](https://github.com/tikv/tikv/issues/17304) @ [Connor1996](https://github.com/Connor1996)

-   PD

    -   PD HTTPクライアントの再試行ロジックが効果がない可能性がある問題を修正[＃8499](https://github.com/tikv/pd/issues/8499) @ [JmPotato](https://github.com/JmPotato)
    -   潜在的なセキュリティ脆弱性を修正するために、Gin Web Framework のバージョンを v1.9.1 から v1.10.0 にアップグレードしました[＃8643](https://github.com/tikv/pd/issues/8643) @ [JmPotato](https://github.com/JmPotato)
    -   etcdリーダー遷移中にPDがリーダーを素早く再選出できない問題を修正 [＃8823](https://github.com/tikv/pd/issues/8823) @ [rleungx](https://github.com/rleungx)
    -   `replication.strictly-match-label`から`true`に設定するとTiFlash が起動しなくなる問題を修正 [＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)
    -   同じストアID で繰り返し作成された場合に`evict-leader-scheduler`正常に動作しない問題を修正 [＃8756](https://github.com/tikv/pd/issues/8756) @ [okJiang](https://github.com/okJiang)
    -   乱数ジェネレータの頻繁な作成によって発生するパフォーマンスジッターの問題を修正しました [＃8674](https://github.com/tikv/pd/issues/8674) @ [rleungx](https://github.com/rleungx)
    -   ホットスポット キャッシュのメモリリーク問題を修正 [＃8698](https://github.com/tikv/pd/issues/8698) @ [lhy1024](https://github.com/lhy1024)
    -   ラベル統計のメモリリーク問題を修正 [＃8700](https://github.com/tikv/pd/issues/8700) @ [lhy1024](https://github.com/lhy1024)
    -   削除されたリソース グループが監視パネルに引き続き表示される問題を修正しました [＃8716](https://github.com/tikv/pd/issues/8716) @ [AndreMouche](https://github.com/AndreMouche)
    -   マイクロサービスモードでPDリーダーが切り替えられたときにスケジューリングサーバーでデータ競合が発生する可能性がある問題を修正しました [＃8538](https://github.com/tikv/pd/issues/8538) @ [lhy1024](https://github.com/lhy1024)
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが利用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   リソース グループ セレクターがどのパネルでも有効にならない問題を修正しました [＃56572](https://github.com/pingcap/tidb/issues/56572) @ [glorv](https://github.com/glorv)

-   TiFlash

    -   複数のリージョンがスナップショットを同時に適用しているときに発生する誤ったリージョン重複チェックの失敗によりTiFlash がpanicになる可能性がある問題を修正しました。 [＃9329](https://github.com/pingcap/tiflash/issues/9329) @ [CalvinNeo](https://github.com/CalvinNeo)
    -   2番目のパラメータが負のの場合に`SUBSTRING()`関数が誤った結果を返す問題を修正しました [＃9604](https://github.com/pingcap/tiflash/issues/9604) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   遅延マテリアライゼーションが有効になっている場合に一部のクエリでエラーが報告される可能性がある問題を修正[＃9472](https://github.com/pingcap/tiflash/issues/9472) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   テーブルに無効な文字を含むデフォルト値を持つビット型の列が含まれている場合、 TiFlash がテーブル スキーマを解析できない問題を修正しました。 [＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   TiFlashでサポートされていない一部の JSON関数がTiFlash にプッシュダウンされる問題を修正しました [＃9444](https://github.com/pingcap/tiflash/issues/9444) @ [windtalker](https://github.com/windtalker)
    -   特定のケースで関数`CAST AS DECIMAL`の結果の符号が正しくない問題を修正[＃9301](https://github.com/pingcap/tiflash/issues/9301) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   分散ストレージおよびコンピューティングアーキテクチャで、 TiFlash書き込みノードの読み取りスナップショットがタイムリーにリリースされない問題を修正しました。 [＃9298](https://github.com/pingcap/tiflash/issues/9298) @ [JinheLin](https://github.com/JinheLin)
    -   `SUBSTRING()`関数が特定の整数型に対して`pos`と`len`引数をサポートせず、クエリエラーが発生する問題を修正しました [＃9473](https://github.com/pingcap/tiflash/issues/9473) @ [gengliqi](https://github.com/gengliqi)
    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [solotzg](https://github.com/solotzg)
    -   `LPAD()`と`RPAD()`関数が、場合によっては誤った結果を返す問題を修正しました[＃9465](https://github.com/pingcap/tiflash/issues/9465) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   分散ストレージおよびコンピューティングアーキテクチャで新しい列をクエリすると誤った結果が返される可能性がある問題を修正しました [＃9665](https://github.com/pingcap/tiflash/issues/9665) @ [zimulala](https://github.com/zimulala)

-   ツール

    -   Backup & Restore (BR)

        -   ログに暗号化された情報が出力される問題を修正 [＃57585](https://github.com/pingcap/tidb/issues/57585) @ [kennytm](https://github.com/kennytm)
        -   AWS EBS に基づくスナップショットバックアップが準備フェーズで失敗し、バックアップが停止する可能性がある問題を修正しました。 [＃52049](https://github.com/pingcap/tidb/issues/52049) @ [YuJuncen](https://github.com/YuJuncen)
        -   バックアップと復元のチェックポイントパスが一部の外部ストレージと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [Leavrth](https://github.com/Leavrth)
        -   `k8s.io/api`ライブラリバージョンにアップグレードして潜在的なセキュリティ脆弱性を修正します [＃57790](https://github.com/pingcap/tidb/issues/57790) @ [BornChanger](https://github.com/BornChanger)
        -   クラスター内に多数のテーブルがあるが、実際のデータサイズが小さい場合に PITR タスクが`Information schema is out of date`エラーを返す可能性がある問題を修正しました[＃57743](https://github.com/pingcap/tidb/issues/57743) @ [Tristan1900](https://github.com/Tristan1900)

    -   TiCDC

        -   PullerモジュールのResolved TSレイテンシーモニタリングで誤った値が表示される問題を修正しました [＃11561](https://github.com/pingcap/tiflow/issues/11561) @ [wlwilliamx](https://github.com/wlwilliamx)
        -   `enable-table-across-nodes`有効にすると、リージョン分割中にテーブルの一部のスパン レプリケーション タスクが失われる可能性がある問題を修正しました。 [＃11675](https://github.com/pingcap/tiflow/issues/11675) @ [wk989898](https://github.com/wk989898)
        -   やり直しモジュールがエラーを正しく報告できない問題を修正しました [＃11744](https://github.com/pingcap/tiflow/issues/11744) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   TiDB DDL 所有者の変更中に DDL タスクのスキーマ バージョンが非増分になったときに、TiCDC が誤って DDL タスクを破棄する問題を修正[＃11714](https://github.com/pingcap/tiflow/issues/11714) @ [wlwilliamx](https://github.com/wlwilliamx)
        -   チェンジフィードチェックポイントの**barrier-ts**監視メトリックが不正確になる可能性がある問題を修正しました[＃11553](https://github.com/pingcap/tiflow/issues/11553) @ [3AceShowHand](https://github.com/3AceShowHand)

    -   TiDB Data Migration (DM)

        -   複数の DM マスターノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)
