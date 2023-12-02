---
title: TiDB 6.1.7 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 6.1.7.
---

# TiDB 6.1.7 リリースノート {#tidb-6-1-7-release-notes}

発売日：2023年7月12日

TiDB バージョン: 6.1.7

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.1.7#version-list)

## 改善点 {#improvements}

-   TiDB

    -   内部トランザクションの再試行では悲観的トランザクションを使用して、再試行の失敗を回避し、時間の消費を削減します[#38136](https://github.com/pingcap/tidb/issues/38136) @ [ジャッキースプ](https://github.com/jackysp)

-   ツール

    -   TiCDC

        -   バッチ`UPDATE` DML ステートメントをサポートして、TiCDC レプリケーションのパフォーマンス[#8084](https://github.com/pingcap/tiflow/issues/8084) @ [咸陽飛](https://github.com/amyangfei)を向上させます。

    -   TiDB Lightning

        -   インポート後に SQL でチェックサムを検証し、検証の安定性を向上させる[#41941](https://github.com/pingcap/tidb/issues/41941) @ [GMHDBJD](https://github.com/GMHDBJD)

## バグの修正 {#bug-fixes}

-   TiDB

    -   空の`processInfo` [#43829](https://github.com/pingcap/tidb/issues/43829) @ [ジムララ](https://github.com/zimulala)によって引き起こされるpanicの問題を修正
    -   PD時間[#44822](https://github.com/pingcap/tidb/issues/44822) @ [ジグアン](https://github.com/zyguan)が急変した場合に`resolve lock`がハングすることがある問題を修正
    -   共通テーブル式 (CTE) を含むクエリによりディスク容量不足が発生する可能性がある問題を修正します[#44477](https://github.com/pingcap/tidb/issues/44477) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   CTE と相関サブクエリを同時に使用すると、不正なクエリ結果またはpanicが発生する可能性がある問題を修正します[#44649](https://github.com/pingcap/tidb/issues/44649) [#38170](https://github.com/pingcap/tidb/issues/38170) [#44774](https://github.com/pingcap/tidb/issues/44774) @ [ウィノロス](https://github.com/winoros) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   ステートメント内の`n`負の数[#44786](https://github.com/pingcap/tidb/issues/44786) @ [ゼボックス](https://github.com/xhebox)である場合、 `SELECT CAST(n AS CHAR)`ステートメントのクエリ結果が正しくない問題を修正します。
    -   特定の場合における TiDB のpanic問題を修正[#40857](https://github.com/pingcap/tidb/issues/40857) @ [ドゥーシール9](https://github.com/Dousir9)
    -   SQL コンパイル エラー ログが編集されない問題を修正[#41831](https://github.com/pingcap/tidb/issues/41831) @ [ランス6716](https://github.com/lance6716)
    -   テーブル パーティション定義で`FLOOR()`関数を使用してパーティション列[#42323](https://github.com/pingcap/tidb/issues/42323) @ [ジフフスト](https://github.com/jiyfhust)を四捨五入する場合、 `SELECT`ステートメントがパーティションテーブルに対してエラーを返す問題を修正します。
    -   パーティション分割テーブルのクエリを実行すると、リージョン分割[#43144](https://github.com/pingcap/tidb/issues/43144) @ [ルクワンチャオ](https://github.com/lcwangchao)中にエラーが発生する可能性がある問題を修正
    -   統計情報[#42052](https://github.com/pingcap/tidb/issues/42052) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)の読み込み時に不要なメモリが使用される問題を修正
    -   多数の空のパーティションテーブル[#44308](https://github.com/pingcap/tidb/issues/44308) @ [ホーキングレイ](https://github.com/hawkingrei)を作成した後の過剰なメモリ使用量の問題を修正
    -   `tidb_opt_agg_push_down`が有効になっている場合にクエリが間違った結果を返す可能性がある問題を修正します[#44795](https://github.com/pingcap/tidb/issues/44795) @ [アイリンキッド](https://github.com/AilinKid)
    -   共通テーブル式の結合結果が間違っている場合がある問題を修正[#38170](https://github.com/pingcap/tidb/issues/38170) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   まれに、GC がロック[#43243](https://github.com/pingcap/tidb/issues/43243) @ [ミョンケミンタ](https://github.com/MyonKeminta)を解決するときに、悲観的トランザクションの残存する悲観的ロックがデータの正確性に影響を与える可能性がある問題を修正します。
    -   キャッシュ テーブルに新しい列が追加された後、値が列のデフォルト値[#42928](https://github.com/pingcap/tidb/issues/42928) @ [lqs](https://github.com/lqs)ではなく`NULL`になる問題を修正します。
    -   インデックス結合[#43686](https://github.com/pingcap/tidb/issues/43686) @ [アイリンキッド](https://github.com/AilinKid) @ [むじょん](https://github.com/mjonss)のプローブフェーズでパーティションテーブル内の対応する行が見つからない場合、TiDB がエラーを返す問題を修正します。
    -   データベースを削除すると GC の進行が遅くなる問題を修正[#33069](https://github.com/pingcap/tidb/issues/33069) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   `ON UPDATE`ステートメントが主キー[#44565](https://github.com/pingcap/tidb/issues/44565) @ [ジグアン](https://github.com/zyguan)を正しく更新しない場合、データとインデックスが矛盾する問題を修正します。
    -   テーブルの名前変更[#43338](https://github.com/pingcap/tidb/issues/43338) @ [タンジェンタ](https://github.com/tangenta)中に TiCDC が行の変更の一部を失う可能性がある問題を修正
    -   パーティション化されたテーブルの配置ルールの動作の問題を修正し、削除されたパーティションの配置ルールを正しく設定してリサイクルできるようにします[#44116](https://github.com/pingcap/tidb/issues/44116) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   `tidb_scatter_region`が有効な場合、パーティションが切り詰められた後にリージョンが自動的に分割されない問題を修正します[#43174](https://github.com/pingcap/tidb/issues/43174) [#43028](https://github.com/pingcap/tidb/issues/43028)
    -   多くのパーティションとTiFlashレプリカを含むパーティション テーブルに対して`TRUNCATE TABLE`を実行するときに、書き込み競合によって引き起こされる DDL 再試行の問題を修正します[#42940](https://github.com/pingcap/tidb/issues/42940) @ [むじょん](https://github.com/mjonss)
    -   ウィンドウ関数をTiFlash [#43922](https://github.com/pingcap/tidb/issues/43922) @ [ゲンリチ](https://github.com/gengliqi)にプッシュダウンするときに実行プランが正しくない問題を修正
    -   非相関サブクエリ[#44051](https://github.com/pingcap/tidb/issues/44051) @ [ウィノロス](https://github.com/winoros)を含むステートメントで共通テーブル式 (CTE) を使用すると、誤った結果が返される可能性がある問題を修正します。
    -   カーソルフェッチで`memTracker`を使用するとメモリリーク[#44254](https://github.com/pingcap/tidb/issues/44254) @ [ヤンケオ](https://github.com/YangKeao)が発生する問題を修正
    -   `INFORMATION_SCHEMA.DDL_JOBS`テーブルの`QUERY`列のデータ長が列定義[#42440](https://github.com/pingcap/tidb/issues/42440) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を超える場合がある問題を修正
    -   `min, max`クエリ結果が正しくない問題を修正[#43805](https://github.com/pingcap/tidb/issues/43805) @ [wshwsh12](https://github.com/wshwsh12)
    -   テーブル[#43392](https://github.com/pingcap/tidb/issues/43392) @ [グオシャオゲ](https://github.com/guo-shaoge)を分析するときに TiDB が構文エラーを報告する問題を修正
    -   `SHOW PROCESSLIST`ステートメントがサブクエリ時間の長いステートメント[#40851](https://github.com/pingcap/tidb/issues/40851) @ [クレイジークス520](https://github.com/crazycs520)のトランザクションの TxnStart を表示できない問題を修正
    -   `DROP TABLE`操作の実行時に`ADMIN SHOW DDL JOBS`の結果でテーブル名が欠落する問題を修正[#42268](https://github.com/pingcap/tidb/issues/42268) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   IPv6 環境[#43260](https://github.com/pingcap/tidb/issues/43260) @ [ネクスター](https://github.com/nexustar)で誤った TiDB アドレスが表示される問題を修正
    -   `AES_DECRYPT`式[#43063](https://github.com/pingcap/tidb/issues/43063) @ [ルクワンチャオ](https://github.com/lcwangchao)を使用すると、SQL ステートメントで`runtime error: index out of range`エラーが報告される問題を修正します。
    -   `SUBPARTITION`使用してパーティション テーブル[#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @ [むじょん](https://github.com/mjonss)を作成するときに警告が表示されない問題を修正します。
    -   CTE を使用したクエリにより TiDB がハングする問題を修正[#43749](https://github.com/pingcap/tidb/issues/43749) [#36896](https://github.com/pingcap/tidb/issues/36896) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   パーティションテーブルのパーティションを切り捨てると、パーティションの配置ルールが無効になる可能性がある問題を修正します[#44031](https://github.com/pingcap/tidb/issues/44031) @ [ルクワンチャオ](https://github.com/lcwangchao)
    -   述語[#43645](https://github.com/pingcap/tidb/issues/43645) @ [ウィノロス](https://github.com/winoros)をプッシュダウンすると CTE の結果が正しくなくなる問題を修正
    -   `auto-commit`変更がトランザクションのコミット動作[#36581](https://github.com/pingcap/tidb/issues/36581) @ [cfzjywxk](https://github.com/cfzjywxk)に影響を与える問題を修正

-   TiKV

    -   TiDB Lightning がSST ファイル漏洩を引き起こす可能性がある問題を修正[#14745](https://github.com/tikv/tikv/issues/14745) @ [ユジュンセン](https://github.com/YuJuncen)
    -   暗号化キー ID の競合により古いキー[#14585](https://github.com/tikv/tikv/issues/14585) @ [タボキー](https://github.com/tabokie)が削除される可能性がある問題を修正
    -   継続的プロファイリング[#14224](https://github.com/tikv/tikv/issues/14224) @ [タボキー](https://github.com/tabokie)でのファイル ハンドル リークの問題を修正

-   PD

    -   gRPC が予期しない形式[#5161](https://github.com/tikv/pd/issues/5161) @ [ヒューシャープ](https://github.com/HuSharp)のエラーを返す問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   `resolved lock timeout`が[#43236](https://github.com/pingcap/tidb/issues/43236) @ [ユジュンセン](https://github.com/YuJuncen)と誤って報告される場合がある問題を修正
        -   クラスター[#42973](https://github.com/pingcap/tidb/issues/42973) @ [ユジュンセン](https://github.com/YuJuncen)で TiKV ノードがクラッシュした場合のバックアップの速度低下の問題を修正

    -   TiCDC

        -   TiCDC がダウンストリーム Kafka-on-Pulsar [#8892](https://github.com/pingcap/tiflow/issues/8892) @ [こんにちはラスティン](https://github.com/hi-rustin)でチェンジフィードを作成できない問題を修正
        -   PD アドレスまたはリーダーに障害が発生した場合、TiCDC が自動的に回復できない問題を修正[#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @ [東門](https://github.com/asddongmen)
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームで過度のワークロードが発生する問題を修正します[#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @ [こんにちはラスティン](https://github.com/hi-rustin)
        -   ネットワーク分離や PD オーナー ノードの再起動など、PD が失敗したときに TiCDC がスタックする問題を修正[#8808](https://github.com/pingcap/tiflow/issues/8808) [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @ [東門](https://github.com/asddongmen)

    -   TiDB Lightning

        -   論理インポート モードで、インポート中にダウンストリームのテーブルを削除すると、 TiDB Lightningメタデータが時間内に更新されなくなる可能性がある問題を修正します[#44614](https://github.com/pingcap/tidb/issues/44614) @ [dsダシュン](https://github.com/dsdashun)
        -   競合条件[#44867](https://github.com/pingcap/tidb/issues/44867) @ [D3ハンター](https://github.com/D3Hunter)によりディスク クォータが不正確になる可能性がある問題を修正
        -   大量のデータをインポートする場合の`write to tikv with no leader returned`の問題を修正[#43055](https://github.com/pingcap/tidb/issues/43055) @ [ランス6716](https://github.com/lance6716)
        -   データ ファイル[#40400](https://github.com/pingcap/tidb/issues/40400) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)に閉じられていない区切り文字がある場合に発生する可能性がある OOM の問題を修正します。
        -   ワイドテーブル[#43728](https://github.com/pingcap/tidb/issues/43728) @ [D3ハンター](https://github.com/D3Hunter)をインポートするときに OOM が発生する可能性がある問題を修正

    -   TiDBBinlog

        -   etcd クライアントが初期化中に最新のノード情報を自動的に同期しない問題を修正[#1236](https://github.com/pingcap/tidb-binlog/issues/1236) @ [リチュンジュ](https://github.com/lichunzhu)
        -   TiKV クライアント[#1170](https://github.com/pingcap/tidb-binlog/issues/1170) @ [リチュンジュ](https://github.com/lichunzhu)をアップグレードすることで、古い TiKV クライアント バージョンに起因するDrainerのpanic問題を修正します。
        -   フィルターされていない失敗した DDL ステートメントによりタスク エラー[#1228](https://github.com/pingcap/tidb-binlog/issues/1228) @ [リチュンジュ](https://github.com/lichunzhu)が発生する問題を修正
