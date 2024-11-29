---
title: TiDB 6.5.11 Release Notes
summary: TiDB 6.5.11 の改善点とバグ修正について説明します。
---

# TiDB 6.5.11 リリースノート {#tidb-6-5-11-release-notes}

発売日: 2024年9月20日

TiDB バージョン: 6.5.11

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 改善点 {#improvements}

-   ティビ

    -   TiFlash配置ルールを一括削除することで、パーティションテーブル[＃54068](https://github.com/pingcap/tidb/issues/54068) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。

-   ティクヴ

    -   RocksDB の圧縮トリガー メカニズムを最適化し、多数の DELETE バージョン[＃17269](https://github.com/tikv/tikv/issues/17269) @ [アンドレ・ムーシュ](https://github.com/AndreMouche)を処理するときにディスク領域の再利用を高速化します。

-   TiFlash

    -   同時実行性の高いデータ読み取り操作でのロック競合を減らし、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [ジンヘリン](https://github.com/JinheLin)
    -   `LENGTH()`と`ASCII()`関数の実行効率を最適化[＃9344](https://github.com/pingcap/tiflash/issues/9344) @ [翻訳者](https://github.com/xzhangxian1008)

-   ツール

    -   ティCDC

        -   ダウンストリームが`SUPER`権限が付与された TiDB の場合、TiCDC は、場合によっては DDL ステートメントの実行を再試行する際のタイムアウトによるデータ複製の失敗を回避するために、ダウンストリーム データベースから`ADD INDEX DDL`の実行ステータスを照会することをサポートします[＃10682](https://github.com/pingcap/tiflow/issues/10682) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   ティビ

    -   再帰 CTE 演算子がメモリ使用量[＃54181](https://github.com/pingcap/tidb/issues/54181) @ [グオシャオゲ](https://github.com/guo-shaoge)を誤って追跡する問題を修正しました
    -   `PipelinedWindow`の`Open`メソッドのパラメータをリセットして、 `PipelinedWindow`が`Apply`の子ノードとして使用されたときに、繰り返しの開閉操作[＃53600](https://github.com/pingcap/tidb/issues/53600) @ [徐懐玉](https://github.com/XuHuaiyu)によって以前のパラメータ値が再利用されたために発生する予期しないエラーを修正します。
    -   トランザクションによって使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [エキシウム](https://github.com/ekexium)
    -   `HashJoin`または`IndexLookUp`演算子が`Apply`演算子[＃54005](https://github.com/pingcap/tidb/issues/54005) @ [徐懐玉](https://github.com/XuHuaiyu)の駆動側サブノードである場合に`memTracker`切り離されないことが原因で異常に高いメモリ使用量が発生する問題を修正しました。
    -   SQLが異常に中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [うわー](https://github.com/wshwsh12)
    -   DMから複製されたテーブルのインデックス長が`max-index-length` [＃55138](https://github.com/pingcap/tidb/issues/55138) @ [ランス6716](https://github.com/lance6716)で指定された最大長を超えるとテーブル複製が失敗する問題を修正しました。
    -   `GROUP BY`ステートメント内の間接プレースホルダー`?`参照が列[＃53872](https://github.com/pingcap/tidb/issues/53872) @ [qw4990](https://github.com/qw4990)を見つけられない問題を修正しました
    -   場合によっては不正な列タイプ`DECIMAL(0,0)`が作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [タンジェンタ](https://github.com/tangenta)
    -   SQLクエリのフィルタ条件に仮想列が含まれ、実行条件に`UnionScan` [＃54870](https://github.com/pingcap/tidb/issues/54870) @ [qw4990](https://github.com/qw4990)が含まれている場合に述語を適切にプッシュダウンできない問題を修正しました。
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `SELECT ... FOR UPDATE` [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)の間違ったポイント取得プランを再利用する問題を修正
    -   厳密に自己増分ではないRANGEパーティションテーブルが[＃54829](https://github.com/pingcap/tidb/issues/54829) @ [定義2014](https://github.com/Defined2014)で作成できる問題を修正
    -   最初の引数が`month`で、2 番目の引数が負の[＃54908](https://github.com/pingcap/tidb/issues/54908) @ [翻訳者](https://github.com/xzhangxian1008)場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。
    -   `auth_socket`認証プラグイン[＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)を使用する場合、TiDB が認証されていないユーザー接続を拒否できないことがある問題を修正しました。
    -   分散実行フレームワーク (DXF) を使用してインデックスを追加するときにネットワーク パーティションが発生すると、データ インデックス[＃54897](https://github.com/pingcap/tidb/issues/54897) @ [タンジェンタ](https://github.com/tangenta)に不整合が発生する可能性がある問題を修正しました。
    -   メモリ使用量が`tidb_mem_quota_query` [＃55042](https://github.com/pingcap/tidb/issues/55042) @ [いびん87](https://github.com/yibin87)で設定された制限を超えたためにクエリが終了したときに停止する可能性がある問題を修正しました
    -   特定の状況下でプラン キャッシュを使用する際に、メタデータ ロックを不適切に使用すると異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [ジムララ](https://github.com/zimulala)
    -   再帰 CTE クエリによって無効なポインタ[＃54449](https://github.com/pingcap/tidb/issues/54449) @ [ホーキングレイ](https://github.com/hawkingrei)が生成される可能性がある問題を修正しました。
    -   `mysql.stats_histograms`の表の`tot_col_size`列目が負の数[＃55126](https://github.com/pingcap/tidb/issues/55126) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました
    -   ビュー定義[＃54343](https://github.com/pingcap/tidb/issues/54343) @ [ランス6716](https://github.com/lance6716)でサブクエリが列定義として使用されている場合、 `information_schema.columns`使用して列情報を取得すると警告 1356 が返される問題を修正しました。
    -   一部のケースで接続を閉じるときに TiDB がログにエラーを報告する問題を修正[＃53689](https://github.com/pingcap/tidb/issues/53689) @ [ジャッキー](https://github.com/jackysp)
    -   `SELECT ... WHERE ... ORDER BY ...`ステートメント実行のパフォーマンスが場合によっては低下する問題を修正[＃54969](https://github.com/pingcap/tidb/issues/54969) @ [天菜まお](https://github.com/tiancaiamao)
    -   `INFORMATION_SCHEMA.STATISTICS`テーブルの`SUB_PART`値が`NULL` [＃55812](https://github.com/pingcap/tidb/issues/55812) @ [定義2014](https://github.com/Defined2014)になる問題を修正しました
    -   クエリが強制終了された後にエラーではなく誤った結果を返す可能性がある問題を修正[＃50089](https://github.com/pingcap/tidb/issues/50089) @ [D3ハンター](https://github.com/D3Hunter)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリすると TiDB がpanicになる可能性がある問題を修正[＃54324](https://github.com/pingcap/tidb/issues/54324) @ [天菜まお](https://github.com/tiancaiamao)
    -   `StreamAggExec`分の`groupOffset`空の場合に TiDB がpanicを起こす可能性がある問題を修正しました[＃53867](https://github.com/pingcap/tidb/issues/53867) @ [翻訳者](https://github.com/xzhangxian1008)
    -   `Sort`演算子がスピルした後にディスク ファイルが削除されず、クエリ エラーが発生する可能性がある問題を修正しました[＃55061](https://github.com/pingcap/tidb/issues/55061) @ [うわー](https://github.com/wshwsh12)
    -   `IndexNestedLoopHashJoin` [＃49692](https://github.com/pingcap/tidb/issues/49692) @ [ソロッツ](https://github.com/solotzg)のデータ競合問題を修正
    -   `SHOW COLUMNS`使用してビュー[＃54964](https://github.com/pingcap/tidb/issues/54964) @ [ランス6716](https://github.com/lance6716)列を表示するとエラーが発生する問題を修正しました
    -   DML文にネストされた生成列[＃53967](https://github.com/pingcap/tidb/issues/53967) @ [翻訳:](https://github.com/wjhuang2016)が含まれている場合にエラーが発生する問題を修正

-   ティクヴ

    -   マスターキーがキー管理サービス (KMS) [＃17410](https://github.com/tikv/tikv/issues/17410) @ [いいえ](https://github.com/hhwyt)に保存されている場合にマスターキーのローテーションが妨げられる問題を修正しました
    -   大きなテーブルやパーティションを削除した後に発生する可能性のあるトラフィック制御の問題を修正[＃17304](https://github.com/tikv/tikv/issues/17304) @ [コナー1996](https://github.com/Connor1996)
    -   削除された`sst_importer` SST ファイル[＃15053](https://github.com/tikv/tikv/issues/15053) @ [ランス6716](https://github.com/lance6716)を取り込むことで TiKV がpanicになる可能性がある問題を修正
    -   古いレプリカがRaftスナップショットを処理するときに、遅い分割操作と新しいレプリカ[＃17469](https://github.com/tikv/tikv/issues/17469) @ [ビシェン](https://github.com/hbisheng)の即時削除によってトリガーされ、TiKV がpanicになる可能性がある問題を修正しました。
    -   破損したRaftデータ スナップショット[＃15292](https://github.com/tikv/tikv/issues/15292) @ [リクササシネーター](https://github.com/LykxSassinator)を適用すると TiKV が繰り返しpanic可能性がある問題を修正しました。
    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB [＃17176](https://github.com/tikv/tikv/issues/17176) @ [エキシウム](https://github.com/ekexium)に送信されるメッセージには反映されない問題を修正しました。
    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   PD

    -   一部のログが編集されていない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [rleungx](https://github.com/rleungx)
    -   TiKV 構成項目[`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 1 MiB 未満の値に設定すると PDpanic[＃8323](https://github.com/tikv/pd/issues/8323) @ [じゃがいも](https://github.com/JmPotato)が発生する問題を修正しました。
    -   `replication.strictly-match-label`から`true`に設定するとTiFlash が[＃8480](https://github.com/tikv/pd/issues/8480) @ [rleungx](https://github.com/rleungx)で起動しなくなる問題を修正
    -   オペレータチェック[＃8263](https://github.com/tikv/pd/issues/8263) @ [翻訳者](https://github.com/lhy1024)中に PD が遭遇するデータ競合問題を修正

-   TiFlash

    -   `CAST()`関数を使用して文字列をタイムゾーンまたは無効な文字を含む日付時刻に変換すると、結果が正しくなくなる問題を修正しました[＃8754](https://github.com/pingcap/tiflash/issues/8754) @ [ソロッツ](https://github.com/solotzg)
    -   データベースが作成直後に削除されるとTiFlash がpanic可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   TiFlashで SSL 証明書構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlash が起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   TiFlashと PD 間のネットワーク パーティション (ネットワーク切断) により読み取り要求タイムアウト エラーが発生する可能性がある問題を修正[＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   外部結合[＃9190](https://github.com/pingcap/tiflash/issues/9190) @ [風の話し手](https://github.com/windtalker)を含むクエリの実行中にエラーが発生するとTiFlash がクラッシュする可能性がある問題を修正しました。
    -   データ型を`DECIMAL`に変換すると、一部のコーナーケースで誤ったクエリ結果が発生する可能性がある問題を修正しました[＃53892](https://github.com/pingcap/tidb/issues/53892) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   クラスタ内で長期間にわたって`EXCHANGE PARTITION`と`DROP TABLE`操作を頻繁に実行すると、 TiFlashテーブル メタデータのレプリケーションが遅くなり、クエリ パフォーマンスが低下する可能性がある問題を修正しました[＃9227](https://github.com/pingcap/tiflash/issues/9227) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップと復元のチェックポイントパスが一部の外部storageと互換性がない問題を修正[＃55265](https://github.com/pingcap/tidb/issues/55265) @ [リーヴルス](https://github.com/Leavrth)
        -   増分バックアップ[＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3ポインター](https://github.com/3pointer)中の DDL ジョブのスキャンにおける非効率性の問題を修正
        -   リージョンリーダー[＃17168](https://github.com/tikv/tikv/issues/17168) @ [リーヴルス](https://github.com/Leavrth)シークの中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。
        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア[＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3ポインター](https://github.com/3pointer)中に正しく回復されない可能性がある問題を修正しました。
        -   ログ バックアップ PITR タスクが失敗して停止すると、そのタスクに関連するセーフポイントが PD [＃17316](https://github.com/tikv/tikv/issues/17316) @ [リーヴルス](https://github.com/Leavrth)で適切にクリアされない問題を修正しました。
        -   バックアッププロセス中に TiKV が応答しなくなった場合にバックアップタスクが停止する可能性がある問題を修正[＃53480](https://github.com/pingcap/tidb/issues/53480) @ [リーヴルス](https://github.com/Leavrth)
        -   ログバックアップが有効になっている場合にBRログに機密の資格情報が出力される可能性がある問題を修正[＃55273](https://github.com/pingcap/tidb/issues/55273) @ [リドリス](https://github.com/RidRisR)

    -   ティCDC

        -   ソーターモジュールがディスクデータ[＃10853](https://github.com/pingcap/tiflow/issues/10853) @ [ヒック](https://github.com/hicqu)を読み取るときに TiCDC がpanicになる可能性がある問題を修正しました。
        -   下流の Kafka にアクセスできない場合にプロセッサ モジュールが停止する可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   インデックスの長さがデフォルト値の`max-index-length` [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [マイケル・ムデン](https://github.com/michaelmdeng)を超えるとデータレプリケーションが中断される問題を修正
        -   スキーマ トラッカーが LIST パーティション テーブルを誤って処理し、DM エラー[＃11408](https://github.com/pingcap/tiflow/issues/11408) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。
        -   LIST パーティション テーブル[＃54760](https://github.com/pingcap/tidb/issues/54760) @ [ランス6716](https://github.com/lance6716)の`ALTER TABLE ... DROP PARTITION`ステートメントを複製するときに DM がエラーを返す問題を修正しました。
        -   DM が`ALTER DATABASE`ステートメントを処理するときにデフォルトのデータベースを設定せず、レプリケーション エラー[＃11503](https://github.com/pingcap/tiflow/issues/11503) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。

    -   TiDB Lightning

        -   TiDB Lightning [＃49826](https://github.com/pingcap/tidb/issues/49826) @ [ランス6716](https://github.com/lance6716)使用してデータインポート中にトランザクションの競合が発生する問題を修正
        -   TiDB Lightning [＃15003](https://github.com/tikv/tikv/issues/15003) [＃47694](https://github.com/pingcap/tidb/issues/47694) @ [ランス6716](https://github.com/lance6716)のインポート モードを無効にした後にデータをインポートすると TiKV データが破損する可能性がある問題を修正しました
        -   TiDB Lightningを使用してデータをインポート中に、TiKV [＃15912](https://github.com/tikv/tikv/issues/15912) @ [ランス6716](https://github.com/lance6716)を再起動するとエラーが発生する問題を修正しました。
