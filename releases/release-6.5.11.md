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
    -   v6.5.11以降、この設定項目はTiKVからTiDBに送信されるgRPC応答メッセージの圧縮アルゴリズムにも影響します。圧縮を有効にすると、CPUリソースの消費量が増加する可能性があります[＃17176](https://github.com/tikv/tikv/issues/17176) @ [ekexium](https://github.com/ekexium)

## 改善点 {#improvements}

-   TiDB

    -   TiFlash配置ルールを一括削除することで、パーティションテーブルで`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。 [＃54068](https://github.com/pingcap/tidb/issues/54068) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

-   TiKV

    -   RocksDB の圧縮トリガー メカニズムを最適化し、多数の DELETE バージョンを処理するときにディスク領域の再利用を高速化します。 [＃17269](https://github.com/tikv/tikv/issues/17269) @ [AndreMouche](https://github.com/AndreMouche)

-   TiFlash

    -   同時実行性の高いデータ読み取り操作におけるロック競合を減らし、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [JinheLin](https://github.com/JinheLin)
    -   `LENGTH()`と`ASCII()`関数の実行効率を最適化 [＃9344](https://github.com/pingcap/tiflash/issues/9344) @ [xzhangxian1008](https://github.com/xzhangxian1008)

-   ツール

    -   TiCDC

        -   下流が`SUPER`権限が付与されたTiDBの場合、TiCDCは下流データベースから`ADD INDEX DDL`の実行ステータスを照会することをサポートします。これにより、DDL文の実行を再試行する際のタイムアウトによるデータ複製の失敗を回避できる場合があります。 [＃10682](https://github.com/pingcap/tiflow/issues/10682) @ [CharlesCheung96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   再帰CTE演算子がメモリ使用量を誤って追跡する問題を修正しました [＃54181](https://github.com/pingcap/tidb/issues/54181) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `PipelinedWindow`の`Open`メソッドのパラメータをリセットして、 `PipelinedWindow`が`Apply`の子ノードとして使用されたときに発生する予期しないエラーを修正します。これはの繰り返し操作による以前のパラメータ値の再利用が原因です。 [＃53600](https://github.com/pingcap/tidb/issues/53600) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   トランザクションで使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [ekexium](https://github.com/ekexium)
    -   `HashJoin`または`IndexLookUp`演算子が`Apply`演算子の駆動側サブノードである場合に`memTracker`切り離されないことで発生する異常に高いメモリ使用量の問題を修正しました。 [＃54005](https://github.com/pingcap/tidb/issues/54005) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   SQLが異常に中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [wshwsh12](https://github.com/wshwsh12)
    -   DMから複製されたテーブルのインデックスの長さが`max-index-length` で指定された最大長を超えるとテーブル複製が失敗する問題を修正しました [＃55138](https://github.com/pingcap/tidb/issues/55138) @ [lance6716](https://github.com/lance6716)
    -   `GROUP BY`ステートメント内の間接プレースホルダ`?`参照が列を見つけられない問題を修正しました [＃53872](https://github.com/pingcap/tidb/issues/53872) @ [qw4990](https://github.com/qw4990)
    -   場合によっては無効な列タイプ`DECIMAL(0,0)`が作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [tangenta](https://github.com/tangenta)
    -   SQLクエリのフィルタ条件に仮想列が含まれており、実行条件に`UnionScan` が含まれている場合に述語を適切にプッシュダウンできない問題を修正しました。 [＃54870](https://github.com/pingcap/tidb/issues/54870) @ [qw4990](https://github.com/qw4990)
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [hawkingrei](https://github.com/hawkingrei)
    -   `SELECT ... FOR UPDATE` の間違ったPointGetプランを再利用する問題を修正しました [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)
    -   厳密に自己増分ではないRANGEパーティションテーブルが作成できる問題を修正 [＃54829](https://github.com/pingcap/tidb/issues/54829) @ [Defined2014](https://github.com/Defined2014)
    -   最初の引数が`month`で、2番目の引数が負の場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。 [＃54908](https://github.com/pingcap/tidb/issues/54908) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `auth_socket`認証プラグインを使用しているときに、TiDB が認証されていないユーザーの接続を拒否できないことがある問題を修正しました。 [＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)
    -   分散実行フレームワーク (DXF) を使用してインデックスを追加する際のネットワーク パーティションによって、データ インデックスの不整合が発生する可能性がある問題を修正しました。 [＃54897](https://github.com/pingcap/tidb/issues/54897) @ [tangenta](https://github.com/tangenta)
    -   メモリ使用量が`tidb_mem_quota_query` で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [yibin87](https://github.com/yibin87)
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [zimulala](https://github.com/zimulala)
    -   再帰CTEクエリが無効なポインタを生成する可能性がある問題を修正しました [＃54449](https://github.com/pingcap/tidb/issues/54449) @ [hawkingrei](https://github.com/hawkingrei)
    -   `mysql.stats_histograms`表の`tot_col_size`番目の列が負の数になる可能性がある問題を修正しました [＃55126](https://github.com/pingcap/tidb/issues/55126) @ [qw4990](https://github.com/qw4990)
    -   ビュー定義でサブクエリが列定義として使用されている場合、 `information_schema.columns`を使用して列情報を取得すると警告1356が返される問題を修正しました。 [＃54343](https://github.com/pingcap/tidb/issues/54343) @ [lance6716](https://github.com/lance6716)
    -   TiDBが接続を閉じるときにログにエラーを報告する場合がある問題を修正[＃53689](https://github.com/pingcap/tidb/issues/53689) @ [jackysp](https://github.com/jackysp)
    -   `SELECT ... WHERE ... ORDER BY ...`文の実行パフォーマンスが場合によっては低下する問題を修正[＃54969](https://github.com/pingcap/tidb/issues/54969) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `INFORMATION_SCHEMA.STATISTICS`テーブルの`SUB_PART`値が`NULL` になる問題を修正しました [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [Defined2014](https://github.com/Defined2014)
    -   クエリが強制終了された後にエラーではなく誤った結果を返す可能性がある問題を修正[＃50089](https://github.com/pingcap/tidb/issues/50089) @ [D3Hunter](https://github.com/D3Hunter)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリすると TiDB がpanicを起こす可能性がある問題を修正[＃54324](https://github.com/pingcap/tidb/issues/54324) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `StreamAggExec`分の`groupOffset`空の場合に TiDB がpanicを起こす可能性がある問題を修正しました [＃53867](https://github.com/pingcap/tidb/issues/53867) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `Sort`演算子がスピルした後にディスクファイルが削除されず、クエリエラーが発生する可能性がある問題を修正[＃55061](https://github.com/pingcap/tidb/issues/55061) @ [wshwsh12](https://github.com/wshwsh12)
    -   `IndexNestedLoopHashJoin` のデータ競合問題を修正 [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [solotzg](https://github.com/solotzg)
    -   `SHOW COLUMNS`を使用してビューの列を表示するとエラーが発生する問題を修正しました [＃54964](https://github.com/pingcap/tidb/issues/54964) @ [lance6716](https://github.com/lance6716)
    -   DML文にネストされた生成列が含まれている場合にエラーが発生する問題を修正しました [＃53967](https://github.com/pingcap/tidb/issues/53967) @ [wjhuang2016](https://github.com/wjhuang2016)

-   TiKV

    -   マスターキーがキー管理サービス (KMS) に保存されているときにマスターキーのローテーションを妨げる問題を修正しました [＃17410](https://github.com/tikv/tikv/issues/17410) @ [hhwyt](https://github.com/hhwyt)
    -   大きなテーブルやパーティションを削除した後に発生する可能性のあるトラフィック制御の問題を修正しました [＃17304](https://github.com/tikv/tikv/issues/17304) @ [Connor1996](https://github.com/Connor1996)
    -   削除された`sst_importer` SST ファイルを取り込むことにより TiKV がpanicになる可能性がある問題を修正しました [＃15053](https://github.com/tikv/tikv/issues/15053) @ [lance6716](https://github.com/lance6716)
    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカの即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。 [＃17469](https://github.com/tikv/tikv/issues/17469) @ [hbisheng](https://github.com/hbisheng)
    -   破損したRaftデータ スナップショットを適用すると TiKV が繰り返しpanicする可能性がある問題を修正しました。 [＃15292](https://github.com/tikv/tikv/issues/15292) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB に送信されるメッセージには反映されない問題を修正しました。 [＃17176](https://github.com/tikv/tikv/issues/17176) @ [ekexium](https://github.com/ekexium)
    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [MyonKeminta](https://github.com/MyonKeminta)

-   PD

    -   一部のログが編集されない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [rleungx](https://github.com/rleungx)
    -   TiKV構成項目[`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 1 MiB未満の値に設定するとPD panicが発生する問題を修正しました [＃8323](https://github.com/tikv/pd/issues/8323) @ [JmPotato](https://github.com/JmPotato)
    -   `replication.strictly-match-label`から`true`に設定するとTiFlash が起動しなくなる問題を修正 [＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)
    -   PD がオペレータ チェック中に遭遇するデータ競合問題を修正しました [＃8263](https://github.com/tikv/pd/issues/8263) @ [lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [solotzg](https://github.com/solotzg)
    -   データベースが作成直後に削除されるとTiFlash がpanicする可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashで SSL 証明書の構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlash が起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashとPD間のネットワークパーティション（ネットワーク切断）により、読み取り要求タイムアウトエラーが発生する可能性がある問題を修正しました。 [＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   外部結合を含むクエリの実行中にエラーが発生した場合にTiFlashがクラッシュする可能性がある問題を修正しました。 [＃9190](https://github.com/pingcap/tiflash/issues/9190) @ [windtalker](https://github.com/windtalker)
    -   データ型を`DECIMAL`に変換すると、一部のコーナーケースで誤ったクエリ結果が発生する可能性がある問題を修正しました[＃53892](https://github.com/pingcap/tidb/issues/53892) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   クラスタ内で長期間にわたって頻繁に`EXCHANGE PARTITION`と`DROP TABLE`操作を行うと、 TiFlashテーブル メタデータのレプリケーションが遅くなり、クエリ パフォーマンスが低下する可能性がある問題を修正しました[＃9227](https://github.com/pingcap/tiflash/issues/9227) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   バックアップと復元のチェックポイントパスが一部の外部ストレージと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [Leavrth](https://github.com/Leavrth)
        -   増分バックアップ中の DDL ジョブのスキャンの非効率性の問題を修正 [＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3pointer](https://github.com/3pointer)
        -   リージョンリーダーの探索の中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。 [＃17168](https://github.com/tikv/tikv/issues/17168) @ [Leavrth](https://github.com/Leavrth)
        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア中に正しく回復されない可能性がある問題を修正しました。 [＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3pointer](https://github.com/3pointer)
        -   ログバックアップ PITR タスクが失敗して停止すると、そのタスクに関連するセーフポイントが PD で適切にクリアされない問題を修正しました。 [＃17316](https://github.com/tikv/tikv/issues/17316) @ [Leavrth](https://github.com/Leavrth)
        -   バックアッププロセス中に TiKV が応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正[＃53480](https://github.com/pingcap/tidb/issues/53480) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップが有効になっているときにBRログに機密の資格情報が出力される可能性がある問題を修正[＃55273](https://github.com/pingcap/tidb/issues/55273) @ [RidRisR](https://github.com/RidRisR)

    -   TiCDC

        -   ソーターモジュールがディスクデータを読み取るときにTiCDCがpanicになる可能性がある問題を修正しました [＃10853](https://github.com/pingcap/tiflow/issues/10853) @ [hicqu](https://github.com/hicqu)
        -   下流の Kafka にアクセスできない場合にプロセッサモジュールがスタックする可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [asddongmen](https://github.com/asddongmen)

    -   TiDB Data Migration (DM)

        -   インデックスの長さがデフォルト値の`max-index-length` を超えるとデータレプリケーションが中断される問題を修正しました [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [michaelmdeng](https://github.com/michaelmdeng)
        -   スキーマ トラッカーが LIST パーティション テーブルを誤って処理し、DM エラーが発生する問題を修正しました。 [＃11408](https://github.com/pingcap/tiflow/issues/11408) @ [lance6716](https://github.com/lance6716)
        -   LISTパーティションテーブルの`ALTER TABLE ... DROP PARTITION`文を複製するときにDMがエラーを返す問題を修正しました。 [＃54760](https://github.com/pingcap/tidb/issues/54760) @ [lance6716](https://github.com/lance6716)
        -   DMが`ALTER DATABASE`ステートメントを処理するときにデフォルトのデータベースを設定せず、レプリケーションエラーが発生する問題を修正しました。 [＃11503](https://github.com/pingcap/tiflow/issues/11503) @ [lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightning を使用してデータのインポート中にトランザクションの競合が発生する問題を修正しました [＃49826](https://github.com/pingcap/tidb/issues/49826) @ [lance6716](https://github.com/lance6716)
        -   TiDB Lightning のインポートモードを無効にした後にデータをインポートすると TiKV データが破損する可能性がある問題を修正しました [＃47694](https://github.com/pingcap/tidb/issues/47694) @ [lance6716](https://github.com/lance6716) [＃15003](https://github.com/tikv/tikv/issues/15003)
        -   TiDB Lightningを使用してデータをインポート中に、TiKV を再起動するとエラーが発生する問題を修正しました。 [＃15912](https://github.com/tikv/tikv/issues/15912) @ [lance6716](https://github.com/lance6716)
