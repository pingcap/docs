---
title: TiDB 6.1.7 Release Notes
summary: TiDB 6.1.7 の改善点とバグ修正について説明します。
---

# TiDB 6.1.7 リリースノート {#tidb-6-1-7-release-notes}

発売日：2023年7月12日

TiDB バージョン: 6.1.7

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番環境への展開](https://docs-archive.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 改善点 {#improvements}

-   TiDB

    -   内部トランザクションの再試行で悲観的トランザクションを使用して再試行の失敗を回避し、時間の消費を削減します[＃38136](https://github.com/pingcap/tidb/issues/38136) @ [jackysp](https://github.com/jackysp)

-   ツール

    -   TiCDC

        -   TiCDC レプリケーションのパフォーマンスを向上させるためにバッチ`UPDATE` DML ステートメントをサポートする[＃8084](https://github.com/pingcap/tiflow/issues/8084) @ [amyangfei](https://github.com/amyangfei)

    -   TiDB Lightning

        -   インポート後にSQLでチェックサムを検証し、検証の安定性を向上 [＃41941](https://github.com/pingcap/tidb/issues/41941) @ [GMHDBJD](https://github.com/GMHDBJD)

## バグ修正 {#bug-fixes}

-   TiDB

    -   空の`processInfo` によって引き起こされるpanic問題を修正 [＃43829](https://github.com/pingcap/tidb/issues/43829) @ [zimulala](https://github.com/zimulala)
    -   PD時間に突然の変化があったときに`resolve lock`ハングする可能性がある問題を修正しました [＃44822](https://github.com/pingcap/tidb/issues/44822) @ [zyguan](https://github.com/zyguan)
    -   共通テーブル式（CTE）を含むクエリによってディスク容量不足が発生する可能性がある問題を修正[＃44477](https://github.com/pingcap/tidb/issues/44477) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   CTEと相関サブクエリを同時に使用すると、クエリ結果が不正確になったり、panicが発生する可能性がある問題を修正[＃44649](https://github.com/pingcap/tidb/issues/44649) [＃38170](https://github.com/pingcap/tidb/issues/38170) [＃44774](https://github.com/pingcap/tidb/issues/44774) @ [winoros](https://github.com/winoros) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   文中の`n`負の数の場合に文`SELECT CAST(n AS CHAR)`のクエリ結果が正しくない問題を修正しました [＃44786](https://github.com/pingcap/tidb/issues/44786) @ [xhebox](https://github.com/xhebox)
    -   特定のケースにおける TiDB のpanic問題を修正[＃40857](https://github.com/pingcap/tidb/issues/40857) @ [Dousir9](https://github.com/Dousir9)
    -   SQLコンパイルエラーログが編集されない問題を修正[＃41831](https://github.com/pingcap/tidb/issues/41831) @ [lance6716](https://github.com/lance6716)
    -   テーブルパーティション定義で`FLOOR()`関数を使用してパーティション列をに丸めた場合、 `SELECT`ステートメントがパーティションテーブルに対してエラーを返す問題を修正しました。 [＃42323](https://github.com/pingcap/tidb/issues/42323) @ [jiyfhust](https://github.com/jiyfhust)
    -   リージョン分割中にパーティション テーブルをクエリするとエラーが発生する可能性がある問題を修正しました。 [＃43144](https://github.com/pingcap/tidb/issues/43144) @ [lcwangchao](https://github.com/lcwangchao)
    -   統計情報読み取り中に不要なメモリが使用される問題を修正 [＃42052](https://github.com/pingcap/tidb/issues/42052) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   多数の空のパーティションテーブルを作成した後に過剰なメモリ使用が発生する問題を修正しました [＃44308](https://github.com/pingcap/tidb/issues/44308) @ [hawkingrei](https://github.com/hawkingrei)
    -   `tidb_opt_agg_push_down`有効になっている場合にクエリが誤った結果を返す可能性がある問題を修正[＃44795](https://github.com/pingcap/tidb/issues/44795) @ [AilinKid](https://github.com/AilinKid)
    -   共通テーブル式の結合結果が間違っている可能性がある問題を修正[＃38170](https://github.com/pingcap/tidb/issues/38170) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   GC がロックを解決するときに、まれに悲観的トランザクションの残余悲観的ロックがデータの正確性に影響を与える可能性がある問題を修正しました。 [＃43243](https://github.com/pingcap/tidb/issues/43243) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   キャッシュテーブルに新しい列が追加された後、列のデフォルト値ではなく値が`NULL`なる問題を修正しました。 [＃42928](https://github.com/pingcap/tidb/issues/42928) @ [lqs](https://github.com/lqs)
    -   インデックス結合のプローブフェーズでパーティションテーブル内の対応する行が見つからない場合に TiDB がエラーを返す問題を修正しました。 [＃43686](https://github.com/pingcap/tidb/issues/43686) @ [AilinKid](https://github.com/AilinKid) @ [mjonss](https://github.com/mjonss)
    -   データベースを削除するとGCの進行が遅くなる問題を修正[＃33069](https://github.com/pingcap/tidb/issues/33069) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `ON UPDATE`文が主キーを正しく更新しない場合にデータとインデックスが不整合になる問題を修正しました [＃44565](https://github.com/pingcap/tidb/issues/44565) @ [zyguan](https://github.com/zyguan)
    -   テーブル名の変更中に TiCDC が行の変更の一部を失う可能性がある問題を修正[＃43338](https://github.com/pingcap/tidb/issues/43338) @ [tangenta](https://github.com/tangenta)
    -   パーティション化されたテーブルにおける配置ルールの動作の問題を修正し、削除されたパーティションにおける配置ルールが正しく設定され、再利用されるようになりました[＃44116](https://github.com/pingcap/tidb/issues/44116) @ [lcwangchao](https://github.com/lcwangchao)
    -   `tidb_scatter_region`有効にすると、パーティションが切り捨てられた後にリージョンが自動的に分割されない問題を修正しました[＃43174](https://github.com/pingcap/tidb/issues/43174) [＃43028](https://github.com/pingcap/tidb/issues/43028)
    -   多数のパーティションとTiFlashレプリカを持つパーティション テーブルに対して`TRUNCATE TABLE`実行するときに書き込み競合によって発生する DDL 再試行の問題を修正しました。 [＃42940](https://github.com/pingcap/tidb/issues/42940) @ [mjonss](https://github.com/mjonss)
    -   ウィンドウ関数をTiFlash にプッシュダウンする際の実行プランが正しくない問題を修正しました [＃43922](https://github.com/pingcap/tidb/issues/43922) @ [gengliqi](https://github.com/gengliqi)
    -   非相関サブクエリを含むステートメントで共通テーブル式 (CTE) を使用すると誤った結果が返される可能性がある問題を修正しました [＃44051](https://github.com/pingcap/tidb/issues/44051) @ [winoros](https://github.com/winoros)
    -   カーソルフェッチで`memTracker`使用するとメモリリークが発生する問題を修正[＃44254](https://github.com/pingcap/tidb/issues/44254) @ [YangKeao](https://github.com/YangKeao)
    -   `INFORMATION_SCHEMA.DDL_JOBS`テーブルの`QUERY`列のデータ長が列定義を超える可能性がある問題を修正しました [＃42440](https://github.com/pingcap/tidb/issues/42440) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   `min, max`クエリ結果が正しくない問題を修正[＃43805](https://github.com/pingcap/tidb/issues/43805) @ [wshwsh12](https://github.com/wshwsh12)
    -   TiDBがテーブルを分析するときに構文エラーを報告する問題を修正しました [＃43392](https://github.com/pingcap/tidb/issues/43392) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `SHOW PROCESSLIST`文でサブクエリ時間が長い文のトランザクションの TxnStart を表示できない問題を修正[＃40851](https://github.com/pingcap/tidb/issues/40851) @ [crazycs520](https://github.com/crazycs520)
    -   `DROP TABLE`操作が実行されているときに`ADMIN SHOW DDL JOBS`結果にテーブル名が表示されない問題を修正[＃42268](https://github.com/pingcap/tidb/issues/42268) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   IPv6環境で誤ったTiDBアドレスが表示される問題を修正[＃43260](https://github.com/pingcap/tidb/issues/43260) @ [nexustar](https://github.com/nexustar)
    -   `AES_DECRYPT`式を使用すると SQL 文が`runtime error: index out of range`エラーを報告する問題を修正しました [＃43063](https://github.com/pingcap/tidb/issues/43063) @ [lcwangchao](https://github.com/lcwangchao)
    -   `SUBPARTITION`を使用してパーティションテーブル を作成するときに警告が表示されない問題を修正しました [＃41200](https://github.com/pingcap/tidb/issues/41200) @ [mjonss](https://github.com/mjonss) [＃41198](https://github.com/pingcap/tidb/issues/41198)
    -   CTE を含むクエリによって TiDB がハングする問題を修正[＃43749](https://github.com/pingcap/tidb/issues/43749) [＃36896](https://github.com/pingcap/tidb/issues/36896) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   パーティションテーブルのパーティションを切り捨てるとパーティションの配置ルールが無効になる可能性がある問題を修正[＃44031](https://github.com/pingcap/tidb/issues/44031) @ [lcwangchao](https://github.com/lcwangchao)
    -   述語をプッシュダウンするときに CTE 結果が正しくない問題を修正しました [＃43645](https://github.com/pingcap/tidb/issues/43645) @ [winoros](https://github.com/winoros)
    -   `auto-commit`変更がトランザクションのコミット動作に影響を与える問題を修正しました [＃36581](https://github.com/pingcap/tidb/issues/36581) @ [cfzjywxk](https://github.com/cfzjywxk)

-   TiKV

    -   TiDB Lightning がSST ファイルの漏洩を引き起こす可能性がある問題を修正[＃14745](https://github.com/tikv/tikv/issues/14745) @ [YuJuncen](https://github.com/YuJuncen)
    -   暗号化キーIDの競合により古いキーが削除される可能性がある問題を修正しました [＃14585](https://github.com/tikv/tikv/issues/14585) @ [tabokie](https://github.com/tabokie)
    -   継続的プロファイリングにおけるファイル ハンドル リークの問題を修正しました [＃14224](https://github.com/tikv/tikv/issues/14224) @ [tabokie](https://github.com/tabokie)

-   PD

    -   gRPC が予期しない形式でエラーを返す問題を修正しました [＃5161](https://github.com/tikv/pd/issues/5161) @ [HuSharp](https://github.com/HuSharp)

-   ツール

    -   Backup & Restore (BR)

        -   `resolved lock timeout`が場合によっては誤って報告される問題を修正[＃43236](https://github.com/pingcap/tidb/issues/43236) @ [YuJuncen](https://github.com/YuJuncen)
        -   クラスターで TiKV ノードがクラッシュしたときにバックアップ速度が低下する問題を修正しました [＃42973](https://github.com/pingcap/tidb/issues/42973) @ [YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   TiCDC が下流の Kafka-on-Pulsar で変更フィードを作成できない問題を修正しました [＃8892](https://github.com/pingcap/tiflow/issues/8892) @ [Rustin170506](https://github.com/Rustin170506)
        -   PDアドレスまたはリーダーに障害が発生したときにTiCDCが自動的に回復できない問題を修正[＃8812](https://github.com/pingcap/tiflow/issues/8812) [＃8877](https://github.com/pingcap/tiflow/issues/8877) @ [asddongmen](https://github.com/asddongmen)
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームに過度のワークロードが発生する問題を修正しました[＃8957](https://github.com/pingcap/tiflow/issues/8957) [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [Rustin170506](https://github.com/Rustin170506)
        -   ネットワーク分離やPDオーナーノードの再起動などのPD障害時にTiCDCが停止する問題を修正[＃8808](https://github.com/pingcap/tiflow/issues/8808) [＃8812](https://github.com/pingcap/tiflow/issues/8812) [＃8877](https://github.com/pingcap/tiflow/issues/8877) @ [asddongmen](https://github.com/asddongmen)

    -   TiDB Lightning

        -   論理インポートモードで、インポート中に下流のテーブルを削除すると、 TiDB Lightningメタデータが時間で更新されない可能性がある問題を修正しました。 [＃44614](https://github.com/pingcap/tidb/issues/44614) @ [dsdashun](https://github.com/dsdashun)
        -   競合条件によりディスククォータが不正確になる可能性がある問題を修正 [＃44867](https://github.com/pingcap/tidb/issues/44867) @ [D3Hunter](https://github.com/D3Hunter)
        -   大量のデータをインポートする際の`write to tikv with no leader returned`の問題を修正[＃43055](https://github.com/pingcap/tidb/issues/43055) @ [lance6716](https://github.com/lance6716)
        -   データファイルに閉じられていない区切り文字がある場合に発生する可能性のある OOM 問題を修正しました。 [＃40400](https://github.com/pingcap/tidb/issues/40400) @ [buchuitoudegou](https://github.com/buchuitoudegou)
        -   幅の広いテーブルをインポートするときに OOM が発生する可能性がある問題を修正しました [＃43728](https://github.com/pingcap/tidb/issues/43728) @ [D3Hunter](https://github.com/D3Hunter)

    -   TiDB Binlog

        -   etcdクライアントが初期化中に最新のノード情報を自動的に同期しない問題を修正[＃1236](https://github.com/pingcap/tidb-binlog/issues/1236) @ [lichunzhu](https://github.com/lichunzhu)
        -   TiKVクライアントを@ [lichunzhu](https://github.com/lichunzhu)にアップグレードすることで、古いTiKVクライアントバージョンによるDrainerのpanic問題を修正しました。 [＃1170](https://github.com/pingcap/tidb-binlog/issues/1170)
        -   フィルタリングされていない失敗したDDL文がタスクエラーを引き起こす問題を修正 [＃1228](https://github.com/pingcap/tidb-binlog/issues/1228) @ [lichunzhu](https://github.com/lichunzhu)
