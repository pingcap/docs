---
title: TiDB 6.5.11 Release Notes
summary: TiDB 6.5.11 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.11 リリースノート {#tidb-6-5-11-release-notes}

発売日：2024年9月20日

TiDBバージョン: 6.5.11

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiKV構成項目[`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type)のスコープを変更します。

    -   v6.5.11 より前の v6.5.x バージョンでは、この構成項目は TiKV ノード間の gRPC メッセージの圧縮アルゴリズムにのみ影響します。
    -   v6.5.11以降、この設定項目はTiKVからTiDBに送信されるgRPC応答メッセージの圧縮アルゴリズムにも影響します。圧縮を有効にすると、CPUリソースの消費量が増加する可能性があります[＃17176](https://github.com/tikv/tikv/issues/17176) @ [エキシウム](https://github.com/ekexium)

## 改善点 {#improvements}

-   ティドブ

    -   TiFlash配置ルールを一括削除することで、パーティションテーブル[＃54068](https://github.com/pingcap/tidb/issues/54068) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。

-   TiKV

    -   RocksDB の圧縮トリガー メカニズムを最適化し、多数の DELETE バージョン[＃17269](https://github.com/tikv/tikv/issues/17269) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)を処理するときにディスク領域の再利用を高速化します。

-   TiFlash

    -   同時実行性の高いデータ読み取り操作におけるロック競合を減らし、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [ジンヘリン](https://github.com/JinheLin)
    -   `LENGTH()`と`ASCII()`関数[＃9344](https://github.com/pingcap/tiflash/issues/9344) @ [xzhangxian1008](https://github.com/xzhangxian1008)の実行効率を最適化

-   ツール

    -   TiCDC

        -   下流が`SUPER`権限が付与されたTiDBの場合、TiCDCは下流データベースから`ADD INDEX DDL`の実行ステータスを照会することをサポートします。これにより、DDL文の実行を再試行する際のタイムアウトによるデータ複製の失敗を回避できます[＃10682](https://github.com/pingcap/tiflow/issues/10682) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)の場合）。

## バグ修正 {#bug-fixes}

-   ティドブ

    -   再帰CTE演算子がメモリ使用量[＃54181](https://github.com/pingcap/tidb/issues/54181) @ [グオシャオゲ](https://github.com/guo-shaoge)を誤って追跡する問題を修正しました
    -   `PipelinedWindow`の`Open`メソッドのパラメータをリセットして、 `PipelinedWindow`が`Apply`の子ノードとして使用されたときに発生する予期しないエラーを修正します。これは[＃53600](https://github.com/pingcap/tidb/issues/53600) @ [徐淮嶼](https://github.com/XuHuaiyu)の繰り返し操作による以前のパラメータ値の再利用が原因です。
    -   トランザクションで使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [エキシウム](https://github.com/ekexium)
    -   `HashJoin`または`IndexLookUp`演算子が`Apply`演算子[＃54005](https://github.com/pingcap/tidb/issues/54005) @ [徐淮嶼](https://github.com/XuHuaiyu)の駆動側サブノードである場合に`memTracker`切り離されないことで発生する異常に高いメモリ使用量の問題を修正しました。
    -   SQLが異常に中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [wshwsh12](https://github.com/wshwsh12)
    -   DMから複製されたテーブルのインデックスの長さが`max-index-length` [＃55138](https://github.com/pingcap/tidb/issues/55138) @ [ランス6716](https://github.com/lance6716)で指定された最大長を超えるとテーブル複製が失敗する問題を修正しました
    -   `GROUP BY`ステートメント内の間接プレースホルダ`?`参照が列[＃53872](https://github.com/pingcap/tidb/issues/53872) @ [qw4990](https://github.com/qw4990)を見つけられない問題を修正しました
    -   場合によっては無効な列タイプ`DECIMAL(0,0)`が作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [接線](https://github.com/tangenta)
    -   SQLクエリのフィルタ条件に仮想列が含まれており、実行条件に`UnionScan` [＃54870](https://github.com/pingcap/tidb/issues/54870) @ [qw4990](https://github.com/qw4990)が含まれている場合に述語を適切にプッシュダウンできない問題を修正しました。
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `SELECT ... FOR UPDATE` [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)の間違ったポイント取得プランを再利用する問題を修正しました
    -   厳密に自己増分ではないRANGEパーティションテーブルが[＃54829](https://github.com/pingcap/tidb/issues/54829) @ [定義2014](https://github.com/Defined2014)で作成できる問題を修正
    -   最初の引数が`month`で、2番目の引数が負の[＃54908](https://github.com/pingcap/tidb/issues/54908) @ [xzhangxian1008](https://github.com/xzhangxian1008)場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。
    -   `auth_socket`認証プラグイン[＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)を使用しているときに、TiDB が認証されていないユーザーの接続を拒否できないことがある問題を修正しました。
    -   分散実行フレームワーク (DXF) を使用してインデックスを追加する際のネットワーク パーティションによって、データ インデックス[＃54897](https://github.com/pingcap/tidb/issues/54897) @ [接線](https://github.com/tangenta)の不整合が発生する可能性がある問題を修正しました。
    -   メモリ使用量が`tidb_mem_quota_query` [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [yibin87](https://github.com/yibin87)で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [ジムララ](https://github.com/zimulala)
    -   再帰CTEクエリが無効なポインタ[＃54449](https://github.com/pingcap/tidb/issues/54449) @ [ホーキングレイ](https://github.com/hawkingrei)を生成する可能性がある問題を修正しました
    -   `mysql.stats_histograms`表の`tot_col_size`番目の列が負の数[＃55126](https://github.com/pingcap/tidb/issues/55126) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました
    -   ビュー定義[＃54343](https://github.com/pingcap/tidb/issues/54343) @ [ランス6716](https://github.com/lance6716)でサブクエリが列定義として使用されている場合、 `information_schema.columns`を使用して列情報を取得すると警告1356が返される問題を修正しました。
    -   TiDBが接続を閉じるときにログにエラーを報告する場合がある問題を修正[＃53689](https://github.com/pingcap/tidb/issues/53689) @ [ジャッキーsp](https://github.com/jackysp)
    -   `SELECT ... WHERE ... ORDER BY ...`文の実行パフォーマンスが場合によっては低下する問題を修正[＃54969](https://github.com/pingcap/tidb/issues/54969) @ [天菜麻緒](https://github.com/tiancaiamao)
    -   `INFORMATION_SCHEMA.STATISTICS`テーブルの`SUB_PART`値が`NULL` [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [定義2014](https://github.com/Defined2014)になる問題を修正しました
    -   クエリが強制終了された後にエラーではなく誤った結果を返す可能性がある問題を修正[＃50089](https://github.com/pingcap/tidb/issues/50089) @ [D3ハンター](https://github.com/D3Hunter)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリすると TiDB がpanicを起こす可能性がある問題を修正[＃54324](https://github.com/pingcap/tidb/issues/54324) @ [天菜麻緒](https://github.com/tiancaiamao)
    -   `StreamAggExec`分の`groupOffset`空の場合に TiDB が[＃53867](https://github.com/pingcap/tidb/issues/53867) @ [xzhangxian1008](https://github.com/xzhangxian1008)でpanicを起こす可能性がある問題を修正しました
    -   `Sort`演算子がスピルした後にディスクファイルが削除されず、クエリエラーが発生する可能性がある問題を修正[＃55061](https://github.com/pingcap/tidb/issues/55061) @ [wshwsh12](https://github.com/wshwsh12)
    -   `IndexNestedLoopHashJoin` [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [ソロツグ](https://github.com/solotzg)のデータ競合問題を修正
    -   `SHOW COLUMNS`を使用してビュー[＃54964](https://github.com/pingcap/tidb/issues/54964) @ [ランス6716](https://github.com/lance6716)の列を表示するとエラーが発生する問題を修正しました
    -   DML文にネストされた生成列[＃53967](https://github.com/pingcap/tidb/issues/53967) @ [wjhuang2016](https://github.com/wjhuang2016)が含まれている場合にエラーが発生する問題を修正しました

-   TiKV

    -   マスターキーがキー管理サービス (KMS) [＃17410](https://github.com/tikv/tikv/issues/17410) @ [hhwyt](https://github.com/hhwyt)に保存されているときにマスターキーのローテーションを妨げる問題を修正しました
    -   大きなテーブルやパーティション[＃17304](https://github.com/tikv/tikv/issues/17304) @ [コナー1996](https://github.com/Connor1996)を削除した後に発生する可能性のあるトラフィック制御の問題を修正しました
    -   削除された`sst_importer` SST ファイル[＃15053](https://github.com/tikv/tikv/issues/15053) @ [ランス6716](https://github.com/lance6716)を取り込むことにより TiKV がpanicになる可能性がある問題を修正しました
    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカ[＃17469](https://github.com/tikv/tikv/issues/17469) @ [ヒビシェン](https://github.com/hbisheng)の即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。
    -   破損したRaftデータ スナップショット[＃15292](https://github.com/tikv/tikv/issues/15292) @ [LykxSassinator](https://github.com/LykxSassinator)を適用すると TiKV が繰り返しpanic可能性がある問題を修正しました。
    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB [＃17176](https://github.com/tikv/tikv/issues/17176) @ [エキシウム](https://github.com/ekexium)に送信されるメッセージには反映されない問題を修正しました。
    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   PD

    -   一部のログが編集されない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [rleungx](https://github.com/rleungx)
    -   TiKV構成項目[`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 1 MiB未満の値に設定するとPDpanic[＃8323](https://github.com/tikv/pd/issues/8323) @ [Jmポテト](https://github.com/JmPotato)が発生する問題を修正しました
    -   `replication.strictly-match-label`から`true`に設定するとTiFlash が[＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)で起動しなくなる問題を修正
    -   PD がオペレータ チェック[＃8263](https://github.com/tikv/pd/issues/8263) @ [lhy1024](https://github.com/lhy1024)中に遭遇するデータ競合問題を修正しました

-   TiFlash

    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [ソロツグ](https://github.com/solotzg)
    -   データベースが作成直後に削除されるとTiFlash がpanic可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   TiFlashで SSL 証明書の構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlash が起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   TiFlashとPD間のネットワークパーティション（ネットワーク切断）により、読み取り要求タイムアウトエラー[＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)が発生する可能性がある問題を修正しました。
    -   外部結合[＃9190](https://github.com/pingcap/tiflash/issues/9190) @ [ウィンドトーカー](https://github.com/windtalker)を含むクエリの実行中にエラーが発生した場合にTiFlashがクラッシュする可能性がある問題を修正しました。
    -   データ型を`DECIMAL`に変換すると、一部のコーナーケースで誤ったクエリ結果が発生する可能性がある問題を修正しました[＃53892](https://github.com/pingcap/tidb/issues/53892) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   クラスタ内で長期間にわたって頻繁に`EXCHANGE PARTITION`と`DROP TABLE`操作を行うと、 TiFlashテーブル メタデータのレプリケーションが遅くなり、クエリ パフォーマンスが低下する可能性がある問題を修正しました[＃9227](https://github.com/pingcap/tiflash/issues/9227) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップと復元のチェックポイントパスが一部の外部storageと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [リーヴルス](https://github.com/Leavrth)
        -   増分バックアップ[＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3ポイントシュート](https://github.com/3pointer)中の DDL ジョブのスキャンの非効率性の問題を修正
        -   リージョンリーダー[＃17168](https://github.com/tikv/tikv/issues/17168) @ [リーヴルス](https://github.com/Leavrth)の探索の中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。
        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア[＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3ポイントシュート](https://github.com/3pointer)中に正しく回復されない可能性がある問題を修正しました。
        -   ログバックアップ PITR タスクが失敗して停止すると、そのタスクに関連するセーフポイントが PD [＃17316](https://github.com/tikv/tikv/issues/17316) @ [リーヴルス](https://github.com/Leavrth)で適切にクリアされない問題を修正しました。
        -   バックアッププロセス中に TiKV が応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正[＃53480](https://github.com/pingcap/tidb/issues/53480) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップが有効になっているときにBRログに機密の資格情報が出力される可能性がある問題を修正[＃55273](https://github.com/pingcap/tidb/issues/55273) @ [リドリスR](https://github.com/RidRisR)

    -   TiCDC

        -   ソーターモジュールがディスクデータ[＃10853](https://github.com/pingcap/tiflow/issues/10853) @ [ヒック](https://github.com/hicqu)を読み取るときにTiCDCがpanicになる可能性がある問題を修正しました
        -   下流の Kafka にアクセスできない場合にプロセッサモジュールがスタックする可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   インデックスの長さがデフォルト値の`max-index-length` [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [マイケル・ムデン](https://github.com/michaelmdeng)を超えるとデータレプリケーションが中断される問題を修正しました
        -   スキーマ トラッカーが LIST パーティション テーブルを誤って処理し、DM エラー[＃11408](https://github.com/pingcap/tiflow/issues/11408) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。
        -   LISTパーティションテーブル[＃54760](https://github.com/pingcap/tidb/issues/54760) @ [ランス6716](https://github.com/lance6716)の`ALTER TABLE ... DROP PARTITION`文を複製するときにDMがエラーを返す問題を修正しました。
        -   DMが`ALTER DATABASE`ステートメントを処理するときにデフォルトのデータベースを設定せず、レプリケーションエラー[＃11503](https://github.com/pingcap/tiflow/issues/11503) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。

    -   TiDB Lightning

        -   TiDB Lightning [＃49826](https://github.com/pingcap/tidb/issues/49826) @ [ランス6716](https://github.com/lance6716)を使用してデータのインポート中にトランザクションの競合が発生する問題を修正しました
        -   TiDB Lightning [＃15003](https://github.com/tikv/tikv/issues/15003) [＃47694](https://github.com/pingcap/tidb/issues/47694) @ [ランス6716](https://github.com/lance6716)のインポートモードを無効にした後にデータをインポートすると TiKV データが破損する可能性がある問題を修正しました
        -   TiDB Lightningを使用してデータをインポート中に、TiKV [＃15912](https://github.com/tikv/tikv/issues/15912) @ [ランス6716](https://github.com/lance6716)を再起動するとエラーが発生する問題を修正しました。
