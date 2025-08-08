---
title: TiDB 6.1.7 Release Notes
summary: TiDB 6.1.7 の改善点とバグ修正について説明します。
---

# TiDB 6.1.7 リリースノート {#tidb-6-1-7-release-notes}

発売日：2023年7月12日

TiDB バージョン: 6.1.7

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 改善点 {#improvements}

-   TiDB

    -   内部トランザクションの再試行で悲観的トランザクションを使用して再試行の失敗を回避し、時間の消費を削減します[＃38136](https://github.com/pingcap/tidb/issues/38136) @ [ジャッキーsp](https://github.com/jackysp)

-   ツール

    -   TiCDC

        -   TiCDC レプリケーションのパフォーマンスを向上させるためにバッチ`UPDATE` DML ステートメントをサポートする[＃8084](https://github.com/pingcap/tiflow/issues/8084) @ [アミャンフェイ](https://github.com/amyangfei)

    -   TiDB Lightning

        -   インポート後にSQLでチェックサムを検証し、検証[＃41941](https://github.com/pingcap/tidb/issues/41941) @ [GMHDBJD](https://github.com/GMHDBJD)の安定性を向上

## バグ修正 {#bug-fixes}

-   TiDB

    -   空の`processInfo` [＃43829](https://github.com/pingcap/tidb/issues/43829) @ [ジムララ](https://github.com/zimulala)によって引き起こされるpanic問題を修正
    -   PD時間[＃44822](https://github.com/pingcap/tidb/issues/44822) @ [ジグアン](https://github.com/zyguan)に突然の変化があったときに`resolve lock`ハングする可能性がある問題を修正しました
    -   共通テーブル式（CTE）を含むクエリによってディスク容量不足が発生する可能性がある問題を修正[＃44477](https://github.com/pingcap/tidb/issues/44477) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   CTEと相関サブクエリを同時に使用すると、クエリ結果が不正確になったり、panicが発生する可能性がある問題を修正[＃44649](https://github.com/pingcap/tidb/issues/44649) [＃38170](https://github.com/pingcap/tidb/issues/38170) [＃44774](https://github.com/pingcap/tidb/issues/44774) @ [ウィノロス](https://github.com/winoros) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   文中の`n`負の数[＃44786](https://github.com/pingcap/tidb/issues/44786) @ [xhebox](https://github.com/xhebox)の場合に文`SELECT CAST(n AS CHAR)`のクエリ結果が正しくない問題を修正しました
    -   特定のケースにおける TiDB のpanic問題を修正[＃40857](https://github.com/pingcap/tidb/issues/40857) @ [ドゥーシル9](https://github.com/Dousir9)
    -   SQLコンパイルエラーログが編集されない問題を修正[＃41831](https://github.com/pingcap/tidb/issues/41831) @ [ランス6716](https://github.com/lance6716)
    -   テーブルパーティション定義で`FLOOR()`関数を使用してパーティション列を[＃42323](https://github.com/pingcap/tidb/issues/42323) @ [ジフハウス](https://github.com/jiyfhust)に丸めた場合、 `SELECT`ステートメントがパーティションテーブルに対してエラーを返す問題を修正しました。
    -   リージョン[＃43144](https://github.com/pingcap/tidb/issues/43144) @ [lcwangchao](https://github.com/lcwangchao)分割中にパーティション テーブルをクエリするとエラーが発生する可能性がある問題を修正しました。
    -   統計情報[＃42052](https://github.com/pingcap/tidb/issues/42052) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)読み取り中に不要なメモリが使用される問題を修正
    -   多数の空のパーティションテーブル[＃44308](https://github.com/pingcap/tidb/issues/44308) @ [ホーキングレイ](https://github.com/hawkingrei)を作成した後に過剰なメモリ使用が発生する問題を修正しました
    -   `tidb_opt_agg_push_down`有効になっている場合にクエリが誤った結果を返す可能性がある問題を修正[＃44795](https://github.com/pingcap/tidb/issues/44795) @ [アイリンキッド](https://github.com/AilinKid)
    -   共通テーブル式の結合結果が間違っている可能性がある問題を修正[＃38170](https://github.com/pingcap/tidb/issues/38170) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   GC がロック[＃43243](https://github.com/pingcap/tidb/issues/43243) @ [ミョンケミンタ](https://github.com/MyonKeminta)を解決するときに、まれに悲観的トランザクションの残余悲観的ロックがデータの正確性に影響を与える可能性がある問題を修正しました。
    -   キャッシュテーブルに新しい列が追加された後、列[＃42928](https://github.com/pingcap/tidb/issues/42928) @ [lqs](https://github.com/lqs)のデフォルト値ではなく値が`NULL`なる問題を修正しました。
    -   インデックス結合[＃43686](https://github.com/pingcap/tidb/issues/43686) @ [アイリンキッド](https://github.com/AilinKid) @ [ミョンス](https://github.com/mjonss)のプローブフェーズでパーティションテーブル内の対応する行が見つからない場合に TiDB がエラーを返す問題を修正しました。
    -   データベースを削除するとGCの進行が遅くなる問題を修正[＃33069](https://github.com/pingcap/tidb/issues/33069) @ [天菜まお](https://github.com/tiancaiamao)
    -   `ON UPDATE`文が主キー[＃44565](https://github.com/pingcap/tidb/issues/44565) @ [ジグアン](https://github.com/zyguan)を正しく更新しない場合にデータとインデックスが不整合になる問題を修正しました
    -   テーブル名の変更中に TiCDC が行の変更の一部を失う可能性がある問題を修正[＃43338](https://github.com/pingcap/tidb/issues/43338) @ [接線](https://github.com/tangenta)
    -   パーティション化されたテーブルにおける配置ルールの動作の問題を修正し、削除されたパーティションにおける配置ルールが正しく設定され、再利用されるようになりました[＃44116](https://github.com/pingcap/tidb/issues/44116) @ [lcwangchao](https://github.com/lcwangchao)
    -   `tidb_scatter_region`有効にすると、パーティションが切り捨てられた後にリージョンが自動的に分割されない問題を修正しました[＃43174](https://github.com/pingcap/tidb/issues/43174) [＃43028](https://github.com/pingcap/tidb/issues/43028)
    -   多数のパーティションとTiFlashレプリカ[＃42940](https://github.com/pingcap/tidb/issues/42940) @ [ミョンス](https://github.com/mjonss)を持つパーティション テーブルに対して`TRUNCATE TABLE`実行するときに書き込み競合によって発生する DDL 再試行の問題を修正しました。
    -   ウィンドウ関数をTiFlash [＃43922](https://github.com/pingcap/tidb/issues/43922) @ [ゲンリキ](https://github.com/gengliqi)にプッシュダウンする際の実行プランが正しくない問題を修正しました
    -   非相関サブクエリ[＃44051](https://github.com/pingcap/tidb/issues/44051) @ [ウィノロス](https://github.com/winoros)を含むステートメントで共通テーブル式 (CTE) を使用すると誤った結果が返される可能性がある問題を修正しました
    -   カーソルフェッチで`memTracker`使用するとメモリリークが発生する問題を修正[＃44254](https://github.com/pingcap/tidb/issues/44254) @ [ヤンケオ](https://github.com/YangKeao)
    -   `INFORMATION_SCHEMA.DDL_JOBS`テーブルの`QUERY`列目のデータ長が列定義[＃42440](https://github.com/pingcap/tidb/issues/42440) @ [天菜まお](https://github.com/tiancaiamao)を超える可能性がある問題を修正しました
    -   `min, max`クエリ結果が正しくない問題を修正[＃43805](https://github.com/pingcap/tidb/issues/43805) @ [wshwsh12](https://github.com/wshwsh12)
    -   TiDBがテーブル[＃43392](https://github.com/pingcap/tidb/issues/43392) @ [グオシャオゲ](https://github.com/guo-shaoge)を分析するときに構文エラーを報告する問題を修正しました
    -   `SHOW PROCESSLIST`文でサブクエリ時間が長い文のトランザクションの TxnStart を表示できない問題を修正[＃40851](https://github.com/pingcap/tidb/issues/40851) @ [crazycs520](https://github.com/crazycs520)
    -   `DROP TABLE`操作が実行されているときに`ADMIN SHOW DDL JOBS`結果にテーブル名が表示されない問題を修正[＃42268](https://github.com/pingcap/tidb/issues/42268) @ [天菜まお](https://github.com/tiancaiamao)
    -   IPv6環境で誤ったTiDBアドレスが表示される問題を修正[＃43260](https://github.com/pingcap/tidb/issues/43260) @ [ネクスター](https://github.com/nexustar)
    -   `AES_DECRYPT`式[＃43063](https://github.com/pingcap/tidb/issues/43063) @ [lcwangchao](https://github.com/lcwangchao)を使用すると SQL 文が`runtime error: index out of range`エラーを報告する問題を修正しました
    -   `SUBPARTITION`を使用してパーティションテーブル[＃41198](https://github.com/pingcap/tidb/issues/41198) [＃41200](https://github.com/pingcap/tidb/issues/41200) @ [ミョンス](https://github.com/mjonss)を作成するときに警告が表示されない問題を修正しました
    -   CTE を含むクエリによって TiDB がハングする問題を修正[＃43749](https://github.com/pingcap/tidb/issues/43749) [＃36896](https://github.com/pingcap/tidb/issues/36896) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   パーティションテーブルのパーティションを切り捨てるとパーティションの配置ルールが無効になる可能性がある問題を修正[＃44031](https://github.com/pingcap/tidb/issues/44031) @ [lcwangchao](https://github.com/lcwangchao)
    -   述語[＃43645](https://github.com/pingcap/tidb/issues/43645) @ [ウィノロス](https://github.com/winoros)をプッシュダウンするときに CTE 結果が正しくない問題を修正しました
    -   `auto-commit`変更がトランザクションのコミット動作[＃36581](https://github.com/pingcap/tidb/issues/36581) @ [cfzjywxk](https://github.com/cfzjywxk)に影響を与える問題を修正しました

-   TiKV

    -   TiDB Lightning がSST ファイルの漏洩を引き起こす可能性がある問題を修正[＃14745](https://github.com/tikv/tikv/issues/14745) @ [ユジュンセン](https://github.com/YuJuncen)
    -   暗号化キーIDの競合により古いキー[＃14585](https://github.com/tikv/tikv/issues/14585) @ [タボキ](https://github.com/tabokie)が削除される可能性がある問題を修正しました
    -   継続的プロファイリング[＃14224](https://github.com/tikv/tikv/issues/14224) @ [タボキ](https://github.com/tabokie)におけるファイル ハンドル リークの問題を修正しました

-   PD

    -   gRPC が予期しない形式[＃5161](https://github.com/tikv/pd/issues/5161) @ [HuSharp](https://github.com/HuSharp)でエラーを返す問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   `resolved lock timeout`場合によっては誤って報告される問題を修正[＃43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)
        -   クラスター[＃42973](https://github.com/pingcap/tidb/issues/42973) @ [ユジュンセン](https://github.com/YuJuncen)で TiKV ノードがクラッシュしたときにバックアップ速度が低下する問題を修正しました

    -   TiCDC

        -   TiCDC が下流の Kafka-on-Pulsar [＃8892](https://github.com/pingcap/tiflow/issues/8892) @ [ハイラスティン](https://github.com/Rustin170506)で変更フィードを作成できない問題を修正しました
        -   PDアドレスまたはリーダーに障害が発生したときにTiCDCが自動的に回復できない問題を修正[＃8812](https://github.com/pingcap/tiflow/issues/8812) [＃8877](https://github.com/pingcap/tiflow/issues/8877) @ [アズドンメン](https://github.com/asddongmen)
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームに過度のワークロードが発生する問題を修正しました[＃8957](https://github.com/pingcap/tiflow/issues/8957) [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [ハイラスティン](https://github.com/Rustin170506)
        -   ネットワーク分離やPDオーナーノードの再起動などのPD障害時にTiCDCが停止する問題を修正[＃8808](https://github.com/pingcap/tiflow/issues/8808) [＃8812](https://github.com/pingcap/tiflow/issues/8812) [＃8877](https://github.com/pingcap/tiflow/issues/8877) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB Lightning

        -   論理インポートモードで、インポート中に下流のテーブルを削除すると、 TiDB Lightningメタデータが時間[＃44614](https://github.com/pingcap/tidb/issues/44614) @ [dsdashun](https://github.com/dsdashun)で更新されない可能性がある問題を修正しました。
        -   競合条件[＃44867](https://github.com/pingcap/tidb/issues/44867) @ [D3ハンター](https://github.com/D3Hunter)によりディスククォータが不正確になる可能性がある問題を修正
        -   大量のデータをインポートする際の`write to tikv with no leader returned`の問題を修正[＃43055](https://github.com/pingcap/tidb/issues/43055) @ [ランス6716](https://github.com/lance6716)
        -   データファイル[＃40400](https://github.com/pingcap/tidb/issues/40400) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)に閉じられていない区切り文字がある場合に発生する可能性のある OOM 問題を修正しました。
        -   幅の広いテーブル[＃43728](https://github.com/pingcap/tidb/issues/43728) @ [D3ハンター](https://github.com/D3Hunter)をインポートするときに OOM が発生する可能性がある問題を修正しました

    -   TiDBBinlog

        -   etcdクライアントが初期化中に最新のノード情報を自動的に同期しない問題を修正[＃1236](https://github.com/pingcap/tidb-binlog/issues/1236) @ [リチュンジュ](https://github.com/lichunzhu)
        -   TiKVクライアント[＃1170](https://github.com/pingcap/tidb-binlog/issues/1170)を[リチュンジュ](https://github.com/lichunzhu)にアップグレードすることで、古いTiKVクライアントバージョンによるDrainerのpanic問題を修正しました。
        -   フィルタリングされていない失敗したDDL文がタスクエラー[＃1228](https://github.com/pingcap/tidb-binlog/issues/1228) @ [リチュンジュ](https://github.com/lichunzhu)を引き起こす問題を修正
