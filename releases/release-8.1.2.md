---
title: TiDB 8.1.2 Release Notes
summary: TiDB 8.1.2 の改善点とバグ修正について説明します。
---

# TiDB 8.1.2 リリースノート {#tidb-8-1-2-release-notes}

発売日: 2024年12月26日

TiDB バージョン: 8.1.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

## 改善点 {#improvements}

-   ティビ

    -   リクエストユニット (RU) 設定に関するメトリックを追加[＃8444](https://github.com/tikv/pd/issues/8444) @ [ノルーシュ](https://github.com/nolouch)

-   ティクヴ

    -   空のテーブルと小さなリージョン[＃17376](https://github.com/tikv/tikv/issues/17376) @ [リクササシネーター](https://github.com/LykxSassinator)シナリオでのリージョンマージの速度を向上
    -   TiKV の`DiskFull`検出を最適化して RaftEngine の`spill-dir`構成と互換性を持たせ、この機能が[＃17356](https://github.com/tikv/tikv/issues/17356) @ [リクササシネーター](https://github.com/LykxSassinator)で一貫して動作するようにしました。
    -   RocksDB 圧縮のトリガー メカニズムを最適化し、多数の DELETE バージョン[＃17269](https://github.com/tikv/tikv/issues/17269) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)を処理するときにディスク領域の再利用を高速化します。
    -   `import.num-threads`構成項目を動的に変更するサポート[＃17807](https://github.com/tikv/tikv/issues/17807) @ [リドリス](https://github.com/RidRisR)
    -   Rusoto ライブラリを AWS Rust SDK に置き換えて、バックアップと復元のために外部storage(Amazon S3 など) にアクセスします。これにより、IMDSv2 や EKS Pod Identity [＃12371](https://github.com/tikv/tikv/issues/12371) @ [アコシチ](https://github.com/akoshchiy)などの AWS 機能との互換性が向上します。

-   TiFlash

    -   クラスター化インデックス[＃9529](https://github.com/pingcap/tiflash/issues/9529) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を持つテーブルで、バックグラウンドでの古いデータのガベージコレクションの速度が向上しました。
    -   TLS を有効にした後に証明書を更新することでTiFlash がpanicになる可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [風の話し手](https://github.com/windtalker)
    -   分散storageとコンピューティング要求を処理するときにTiFlash が作成する必要があるスレッドの数を減らし、大量のそのような要求を処理するときにTiFlashコンピューティングノードのクラッシュを回避するのに役立ちます[＃9334](https://github.com/pingcap/tiflash/issues/9334) @ [ジンヘリン](https://github.com/JinheLin)
    -   JOIN 演算子のキャンセル メカニズムを改善し、JOIN 演算子がキャンセル要求にタイムリーに応答できるようにします[＃9430](https://github.com/pingcap/tiflash/issues/9430) @ [風の話し手](https://github.com/windtalker)
    -   `LENGTH()`と`ASCII()`関数の実行効率を最適化[＃9344](https://github.com/pingcap/tiflash/issues/9344) @ [翻訳者](https://github.com/xzhangxian1008)
    -   分散storageおよびコンピューティングアーキテクチャ内のTiFlashコンピューティングノードの再試行戦略を最適化して、Amazon S3 [＃9695](https://github.com/pingcap/tiflash/issues/9695) @ [ジンヘリン](https://github.com/JinheLin)からファイルをダウンロードする際の例外を処理します。

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ中の不要なログ出力を削減[＃55902](https://github.com/pingcap/tidb/issues/55902) @ [リーヴルス](https://github.com/Leavrth)

    -   ティCDC

        -   TiCDC は、 `SUPER`権限を付与された後に非同期で実行された DDL タスクのステータスを照会することをサポートし、同じテーブル[＃11521](https://github.com/pingcap/tiflow/issues/11521) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)で DDL タスクを繰り返し実行することによって発生する実行エラーを防止します。
        -   ダウンストリームが`SUPER`権限が付与された TiDB の場合、TiCDC は、場合によっては DDL ステートメントの実行を再試行する際のタイムアウトによるデータ複製の失敗を回避するために、ダウンストリーム データベースから`ADD INDEX DDL`の実行ステータスを照会することをサポートします[＃10682](https://github.com/pingcap/tiflow/issues/10682) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   ティビ

    -   v6.5 から v7.5 以降にアップグレードされたクラスターで、既存の TTL タスクが予期せず頻繁に実行される問題を修正[＃56539](https://github.com/pingcap/tidb/issues/56539) @ [lcwangchao](https://github.com/lcwangchao)
    -   特定の状況下でプラン キャッシュを使用する際に、メタデータ ロックを不適切に使用すると異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [ジムララ](https://github.com/zimulala)
    -   グローバルソートが有効でリージョンサイズが96 MiB [＃55374](https://github.com/pingcap/tidb/issues/55374) @ [ランス6716](https://github.com/lance6716)を超えると`IMPORT INTO`実行が停止する問題を修正
    -   `DUMP STATS`統計を JSON [＃56083](https://github.com/pingcap/tidb/issues/56083) @ [ホーキングレイ](https://github.com/hawkingrei)に変換するときにヒストグラムの上限と下限が壊れる問題を修正
    -   エイリアス[＃56726](https://github.com/pingcap/tidb/issues/56726) @ [ホーキングレイ](https://github.com/hawkingrei)を持つマルチテーブル`DELETE`ステートメントに対して実行プラン バインディングを作成できない問題を修正しました。
    -   TTL テーブル[＃56934](https://github.com/pingcap/tidb/issues/56934) @ [lcwangchao](https://github.com/lcwangchao)のメモリリークの問題を修正
    -   パーティション式が`EXTRACT(YEAR FROM col)` [＃54210](https://github.com/pingcap/tidb/issues/54210) @ [ミョンス](https://github.com/mjonss)の場合にパーティションプルーニングが機能しない問題を修正しました
    -   配置ルール[＃54961](https://github.com/pingcap/tidb/issues/54961) @ [ホーキングレイ](https://github.com/hawkingrei)を含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。
    -   メモリ使用量が`tidb_mem_quota_query` [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [いびん87](https://github.com/yibin87)で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました
    -   copタスク構築中にTiDBクエリをキャンセルできない問題を修正[＃55957](https://github.com/pingcap/tidb/issues/55957) @ [いびん87](https://github.com/yibin87)
    -   TTLジョブ実行中に`tidb_ttl_delete_worker_count`の値を減らすとジョブが[＃55561](https://github.com/pingcap/tidb/issues/55561) @ [lcwangchao](https://github.com/lcwangchao)で完了しなくなる問題を修正
    -   `CAST`関数が文字セット[＃55677](https://github.com/pingcap/tidb/issues/55677) @ [定義2014](https://github.com/Defined2014)の明示的な設定をサポートしていない問題を修正
    -   書き込み競合が発生したときに TTL タスクをキャンセルできない問題を修正[＃56422](https://github.com/pingcap/tidb/issues/56422) @ [ヤンケオ](https://github.com/YangKeao)
    -   `IndexNestedLoopHashJoin` [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [ソロッツ](https://github.com/solotzg)のデータ競合問題を修正
    -   `StreamAggExec`分の`groupOffset`空の場合に TiDB がpanicを起こす可能性がある問題を修正しました[＃53867](https://github.com/pingcap/tidb/issues/53867) @ [翻訳者](https://github.com/xzhangxian1008)
    -   相関サブクエリと CTE [＃55551](https://github.com/pingcap/tidb/issues/55551) @ [グオシャオゲ](https://github.com/guo-shaoge)含むクエリを実行すると、TiDB がハングしたり、誤った結果が返されたりする問題を修正しました。
    -   インデックス追加[＃55808](https://github.com/pingcap/tidb/issues/55808) @ [ランス6716](https://github.com/lance6716)中の再試行によって発生するデータ インデックスの不整合の問題を修正
    -   整数型[＃55837](https://github.com/pingcap/tidb/issues/55837) @ [風の話し手](https://github.com/windtalker)の列に小さい表示幅が指定された場合、 `out of range`エラーが発生する可能性がある問題を修正しました。
    -   `LOAD DATA ... REPLACE INTO`操作でデータの不整合が発生する問題を修正[＃56408](https://github.com/pingcap/tidb/issues/56408) @ [ふーふー](https://github.com/fzzf678)
    -   `columnEvaluator`入力チャンク内の列参照を識別できず、SQL ステートメント[＃53713](https://github.com/pingcap/tidb/issues/53713) @ [アイリンキッド](https://github.com/AilinKid)を実行すると`runtime error: index out of range`発生する問題を修正しました。
    -   共通テーブル式 (CTE) に複数のデータ コンシューマーがあり、1 つのコンシューマーがデータを読み取らずに終了した場合に発生する可能性のある不正なメモリアクセスの問題を修正しました[＃55881](https://github.com/pingcap/tidb/issues/55881) @ [風の話し手](https://github.com/windtalker)
    -   TTLタスクをキャンセルした際に、対応するSQLが強制終了されない問題を修正[＃56511](https://github.com/pingcap/tidb/issues/56511) @ [lcwangchao](https://github.com/lcwangchao)
    -   `IMPORT INTO`ステートメント[＃55970](https://github.com/pingcap/tidb/issues/55970) @ [D3ハンター](https://github.com/D3Hunter)を使用して一時テーブルをインポートするときに TiDB がパニックになる問題を修正しました。
    -   クエリ条件`column IS NULL` [＃56116](https://github.com/pingcap/tidb/issues/56116) @ [ホーキングレイ](https://github.com/hawkingrei)で一意のインデックスにアクセスするときに、オプティマイザが行数を誤って 1 と見積もる問題を修正しました。
    -   情報スキーマキャッシュミス[＃53428](https://github.com/pingcap/tidb/issues/53428) @ [クレイジーcs520](https://github.com/crazycs520)により、古い読み取りのクエリレイテンシーが増加する問題を修正しました。
    -   `UPDATE`文が`ENUM`型[＃56832](https://github.com/pingcap/tidb/issues/56832) @ [xhebox](https://github.com/xhebox)の値を誤って更新する問題を修正しました。
    -   外部キー[＃56456](https://github.com/pingcap/tidb/issues/56456) @ [ホーキングレイ](https://github.com/hawkingrei)を含むテーブル構造をインポートするときに Plan Replayer がエラーを報告する可能性がある問題を修正しました。
    -   `tidb_ttl_job_enable`変数が無効になった後、TTL タスクがキャンセルされない問題を修正[＃57404](https://github.com/pingcap/tidb/issues/57404) @ [ヤンケオ](https://github.com/YangKeao)
    -   `UPDATE`または`DELETE`ステートメントに再帰 CTE が含まれている場合、ステートメントがエラーを報告したり、 [＃55666](https://github.com/pingcap/tidb/issues/55666) @ [時間と運命](https://github.com/time-and-fate)有効にならない可能性がある問題を修正しました。
    -   `INFORMATION_SCHEMA.STATISTICS`テーブルの`SUB_PART`値が`NULL` [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [定義2014](https://github.com/Defined2014)になる問題を修正しました
    -   TiFlashシステム テーブルを照会する際のデフォルトのタイムアウトが短すぎる問題を修正[＃57816](https://github.com/pingcap/tidb/issues/57816) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   `default_collation_for_utf8mb4`変数の値が`SET NAMES`ステートメント[＃56439](https://github.com/pingcap/tidb/issues/56439) @ [定義2014](https://github.com/Defined2014)で機能しない問題を修正しました
    -   `mysql.tidb_timer`テーブル[＃57112](https://github.com/pingcap/tidb/issues/57112) @ [lcwangchao](https://github.com/lcwangchao)でタイマーを手動で削除すると、TTL 内部コルーチンがpanicになる可能性がある問題を修正しました。
    -   `tidb_ddl_enable_fast_reorg`経由で`ADD INDEX`と`CREATE INDEX`の加速を有効にすると`Duplicate entry`エラー[＃49233](https://github.com/pingcap/tidb/issues/49233) @ [ランス6716](https://github.com/lance6716)が発生する可能性がある問題を修正しました
    -   大規模なテーブルに非分散方式でインデックスを追加すると、インデックスのタイムスタンプが`0`に設定される問題を修正[＃57980](https://github.com/pingcap/tidb/issues/57980) @ [ランス6716](https://github.com/lance6716)

-   ティクヴ

    -   構成`resolved-ts.advance-ts-interval`有効にならず、TiKV が[＃17107](https://github.com/tikv/tikv/issues/17107) @ [ミョンケミンタ](https://github.com/MyonKeminta)で再起動すると TiCDC とポイントインタイムリカバリ (PITR) のレプリケーションレイテンシーが大幅に増加する問題を修正しました。
    -   リソース制御[＃17589](https://github.com/tikv/tikv/issues/17589) @ [栄光](https://github.com/glorv)をトリガーするときに一部のタスクで高いテールレイテンシーが発生する問題を修正しました。
    -   リージョンをマージすると稀に TiKV がpanicを起こす可能性がある問題を修正[＃17840](https://github.com/tikv/tikv/issues/17840) @ [栄光](https://github.com/glorv)
    -   ディスクがスタックしているときに TiKV が PD にハートビートを報告できない問題を修正[＃17939](https://github.com/tikv/tikv/issues/17939) @ [リクササシネーター](https://github.com/LykxSassinator)
    -   Raftと RocksDB が異なるディスクにデプロイされている場合、RocksDB が配置されているディスクに対して低速ディスク検出が機能しない問題を修正[＃17884](https://github.com/tikv/tikv/issues/17884) @ [リクササシネーター](https://github.com/LykxSassinator)
    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカ[＃17469](https://github.com/tikv/tikv/issues/17469) @ [ビシェン](https://github.com/hbisheng)の即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。
    -   `RADIANS()`または`DEGREES()`関数を含むクエリを実行するときに TiKV がpanicになる可能性がある問題を修正[＃17852](https://github.com/tikv/tikv/issues/17852) @ [ゲンリキ](https://github.com/gengliqi)
    -   多数のトランザクションが同じキーのロック解除待ち行列に入っていて、キーが頻繁に更新される場合、デッドロック検出に過度の負荷がかかり、TiKV OOM 問題[＃17394](https://github.com/tikv/tikv/issues/17394) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。
    -   リージョンを[＃17602](https://github.com/tikv/tikv/issues/17602)対[リクササシネーター](https://github.com/LykxSassinator)に分割した後、リーダーをすぐに選出できない問題を修正しました。
    -   読み取りスレッドがRaft Engine[＃17383](https://github.com/tikv/tikv/issues/17383) @ [リクササシネーター](https://github.com/LykxSassinator)のMemTable内の古いインデックスにアクセスしたときに発生するpanic問題を修正しました。
    -   大きなテーブルやパーティションを削除した後に発生する可能性のあるフロー制御の問題を修正[＃17304](https://github.com/tikv/tikv/issues/17304) @ [コナー1996](https://github.com/Connor1996)

-   PD

    -   PD HTTP クライアントの再試行ロジックが無効になる可能性がある問題を修正[＃8499](https://github.com/tikv/pd/issues/8499) @ [じゃがいも](https://github.com/JmPotato)
    -   潜在的なセキュリティ脆弱性を修正するため、Gin Web Framework のバージョンを v1.9.1 から v1.10.0 にアップグレードします[＃8643](https://github.com/tikv/pd/issues/8643) @ [じゃがいも](https://github.com/JmPotato)
    -   etcd リーダー遷移[＃8823](https://github.com/tikv/pd/issues/8823) @ [rleungx](https://github.com/rleungx)中に PD がリーダーを迅速に再選出できない問題を修正
    -   `replication.strictly-match-label`から`true`に設定するとTiFlash が[＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)で起動しなくなる問題を修正
    -   同じストアID [＃8756](https://github.com/tikv/pd/issues/8756) @ [ok江](https://github.com/okJiang)で繰り返し作成された場合に`evict-leader-scheduler`正常に動作しない問題を修正
    -   乱数ジェネレータ[＃8674](https://github.com/tikv/pd/issues/8674) @ [rleungx](https://github.com/rleungx)の頻繁な作成によって発生するパフォーマンスジッターの問題を修正しました
    -   ホットスポット キャッシュ[＃8698](https://github.com/tikv/pd/issues/8698) @ [翻訳者](https://github.com/lhy1024)のメモリリーク問題を修正
    -   ラベル統計[＃8700](https://github.com/tikv/pd/issues/8700) @ [翻訳者](https://github.com/lhy1024)のメモリリーク問題を修正
    -   削除されたリソース グループが監視パネル[＃8716](https://github.com/tikv/pd/issues/8716) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)に引き続き表示される問題を修正しました
    -   マイクロサービスモード[＃8538](https://github.com/tikv/pd/issues/8538) @ [翻訳者](https://github.com/lhy1024)でPDリーダーが切り替えられたときにスケジューリングサーバーでデータ競合が発生する可能性がある問題を修正
    -   `evict-leader-scheduler`で間違ったパラメータを使用すると、PD がエラーを正しく報告せず、一部のスケジューラが使用できなくなる問題を修正しました[＃8619](https://github.com/tikv/pd/issues/8619) @ [rleungx](https://github.com/rleungx)
    -   リソース グループ セレクターがどのパネルでも有効にならない問題を修正[＃56572](https://github.com/pingcap/tidb/issues/56572) @ [栄光](https://github.com/glorv)

-   TiFlash

    -   複数のリージョンがスナップショット[＃9329](https://github.com/pingcap/tiflash/issues/9329) @ [カルビンネオ](https://github.com/CalvinNeo)を同時に適用しているときに発生する誤ったリージョン重複チェックの失敗によりTiFlash がpanicになる可能性がある問題を修正しました。
    -   2 番目のパラメータが負の[＃9604](https://github.com/pingcap/tiflash/issues/9604) @ [グオシャオゲ](https://github.com/guo-shaoge)の場合に`SUBSTRING()`関数が誤った結果を返す問題を修正しました
    -   遅延マテリアライゼーションが有効になっている場合に一部のクエリでエラーが報告される問題を修正[＃9472](https://github.com/pingcap/tiflash/issues/9472) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   テーブルに無効な文字[＃9461](https://github.com/pingcap/tiflash/issues/9461) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を含むデフォルト値を持つビット型列が含まれている場合に、 TiFlash がテーブル スキーマを解析できない問題を修正しました。
    -   TiFlashでサポートされていない一部の JSON関数がTiFlash [＃9444](https://github.com/pingcap/tiflash/issues/9444) @ [風の話し手](https://github.com/windtalker)にプッシュダウンされる問題を修正しました
    -   特定のケースで`CAST AS DECIMAL`関数の結果の符号が正しくない問題を修正[＃9301](https://github.com/pingcap/tiflash/issues/9301) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   分散storageおよびコンピューティングアーキテクチャ[＃9298](https://github.com/pingcap/tiflash/issues/9298) @ [ジンヘリン](https://github.com/JinheLin)で、 TiFlash書き込みノードの読み取りスナップショットがタイムリーにリリースされない問題を修正しました。
    -   `SUBSTRING()`関数が特定の整数型の`pos`番目と`len`引数をサポートせず、クエリ エラー[＃9473](https://github.com/pingcap/tiflash/issues/9473) @ [ゲンリキ](https://github.com/gengliqi)が発生する問題を修正しました。
    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [ソロッツ](https://github.com/solotzg)
    -   `LPAD()`と`RPAD()`関数が場合によっては誤った結果を返す問題を修正[＃9465](https://github.com/pingcap/tiflash/issues/9465) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   分散storageおよびコンピューティングアーキテクチャ[＃9665](https://github.com/pingcap/tiflash/issues/9665) @ [ジムララ](https://github.com/zimulala)で新しい列をクエリすると誤った結果が返される可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   ログに暗号化された情報が出力される問題を修正[＃57585](https://github.com/pingcap/tidb/issues/57585) @ [ケニー](https://github.com/kennytm)
        -   AWS EBS に基づくスナップショット バックアップが準備フェーズで失敗し、バックアップが停止する問題を修正しました[＃52049](https://github.com/pingcap/tidb/issues/52049) @ [ユジュンセン](https://github.com/YuJuncen)
        -   バックアップと復元のチェックポイントパスが一部の外部storageと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [リーヴルス](https://github.com/Leavrth)
        -   `k8s.io/api`ライブラリ バージョン[＃57790](https://github.com/pingcap/tidb/issues/57790) @ [ボーンチェンジャー](https://github.com/BornChanger)にアップグレードして潜在的なセキュリティ脆弱性を修正します
        -   クラスター内に多数のテーブルがあるが、実際のデータ サイズが小さい場合に PITR タスクが`Information schema is out of date`エラーを返す可能性がある問題を修正しました[＃57743](https://github.com/pingcap/tidb/issues/57743) @ [トリスタン1900](https://github.com/Tristan1900)

    -   ティCDC

        -   Puller モジュールの解決済み TSレイテンシーモニタリングで誤った値[＃11561](https://github.com/pingcap/tiflow/issues/11561) @ [ウィリアム](https://github.com/wlwilliamx)が表示される問題を修正しました。
        -   `enable-table-across-nodes`が有効になっている場合、リージョン分割[＃11675](https://github.com/pingcap/tiflow/issues/11675) @ [989898 円](https://github.com/wk989898)中にテーブルの一部のスパン レプリケーション タスクが失われる可能性がある問題を修正しました。
        -   やり直しモジュールがエラー[＃11744](https://github.com/pingcap/tiflow/issues/11744) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)を適切に報告できない問題を修正
        -   TiDB DDL 所有者の変更中に DDL タスクのスキーマ バージョンが非増分になったときに、TiCDC が誤って DDL タスクを破棄する問題を修正[＃11714](https://github.com/pingcap/tiflow/issues/11714) @ [ウィリアム](https://github.com/wlwilliamx)
        -   変更フィード チェックポイントの**バリア ts**監視メトリックが不正確になる可能性がある問題を修正[＃11553](https://github.com/pingcap/tiflow/issues/11553) @ [3エースショーハンド](https://github.com/3AceShowHand)

    -   TiDB データ移行 (DM)

        -   複数の DM マスター ノードが同時にリーダーになり、データの不整合が発生する可能性がある問題を修正しました[＃11602](https://github.com/pingcap/tiflow/issues/11602) @ [GMHDBJD](https://github.com/GMHDBJD)
