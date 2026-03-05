---
title: TiDB 8.5.1 Release Notes
summary: TiDB 8.5.1 におけるオペレーティング システムとプラットフォームの要件の変更、互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 8.5.1 リリースノート {#tidb-8-5-1-release-notes}

発売日：2025年1月17日

TiDB バージョン: 8.5.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## オペレーティングシステムとプラットフォーム要件の変更 {#operating-system-and-platform-requirement-changes}

TiDBはv8.5.1以降、CentOS Linux 7のテストを再開し、互換性を確保しています。TiDB v8.5を導入する場合、またはクラスターをv8.5にアップグレードする場合は、TiDB v8.5.1以降のバージョンをご使用ください。

-   TiDB v8.4.0 DMR および v8.5.0 リリースは、CentOS Linux 7 が[2024年6月30日でEOLステータス](https://www.redhat.com/en/topics/linux/centos-linux-eol)達したため、サポートとテストを終了しました。CentOS 7 上の TiDB クラスターを v8.4.0 または v8.5.0 にアップグレードすると、クラスターが使用できなくなるリスクがあります。

-   CentOS Linux 7を引き続きご利用のユーザーの皆様を支援するため、TiDBはCentOS Linux 7のテストをv8.5.1から再開します。ただし、CentOS LinuxはEOL状態にあるため、CentOS Linux 7のバージョン[公式発表とセキュリティガイダンス](https://www.redhat.com/en/blog/centos-linux-has-reached-its-end-life-eol)ご確認いただき、本番環境ではRocky Linux 9.1以降などのバージョン[TiDB でサポートされているオペレーティング システム](/hardware-and-software-requirements.md#os-and-platform-requirements)に移行することを強くお勧めします。

CentOS Linux 7 は EOL に達したため、このディストリビューションのテストは将来の TiDB リリースで停止されます。

## 互換性の変更 {#compatibility-changes}

-   TiDB 統計キャッシュによるメモリ使用量を削減するために、システム変数[`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)のデフォルト値`0`の意味が変更されます。

    -   v8.5.1 より前では、 `0`統計キャッシュのメモリクォータが TiDB インスタンスの合計メモリの 50% であることを意味します。
    -   v8.5.1 以降、 `0`統計キャッシュのメモリクォータが TiDB インスタンスの合計メモリの 20% であることを意味します。

## 改善点 {#improvements}

-   TiDB

    -   読み取り専用のユーザー定義変数を定数[＃52742](https://github.com/pingcap/tidb/issues/52742) @ [ウィノロス](https://github.com/winoros)に折りたたむことをサポート
    -   nulleq条件付きの直積セミ結合を等価条件[＃57583](https://github.com/pingcap/tidb/issues/57583) @ [ホーキングレイ](https://github.com/hawkingrei)のセミ結合に変換する
    -   統計メモリキャッシュのデフォルトのしきい値を合計メモリの20％に調整します[＃58014](https://github.com/pingcap/tidb/issues/58014) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   タイムスタンプの有効性チェックを強化する[＃57786](https://github.com/pingcap/tidb/issues/57786) @ [ミョンケミンタ](https://github.com/MyonKeminta)

-   TiKV

    -   無効な`max_ts`更新の検出メカニズムを追加[＃17916](https://github.com/tikv/tikv/issues/17916) @ [エキシウム](https://github.com/ekexium)

-   TiFlash

    -   分散storageおよびコンピューティングアーキテクチャ内のTiFlashコンピューティングノードの再試行戦略を最適化して、Amazon S3 [＃9695](https://github.com/pingcap/tiflash/issues/9695) @ [ジンヘリン](https://github.com/JinheLin)からファイルをダウンロードする際の例外を処理します。

-   ツール

    -   TiCDC

        -   不要なリソース消費を避けるために、TiCDC によって事前にサブスクライブされていないイベントを除外します[＃17877](https://github.com/tikv/tikv/issues/17877) @ [ヒック](https://github.com/hicqu)

## バグ修正 {#bug-fixes}

-   TiDB

    -   TiFlashシステムテーブルを照会する際のデフォルトのタイムアウトが短すぎる問題を修正[＃57816](https://github.com/pingcap/tidb/issues/57816) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   `tidb_gogc_tuner_max_value`と`tidb_gogc_tuner_min_value`設定するときに最大値がnullの場合に誤った警告メッセージが表示される問題を修正しました[＃57889](https://github.com/pingcap/tidb/issues/57889) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   プランキャッシュがインデックス[＃56733](https://github.com/pingcap/tidb/issues/56733) @ [wjhuang2016](https://github.com/wjhuang2016)を追加するときに間違ったスキーマを使用するため、データインデックスが不整合になる問題を修正しました。
    -   Grafanaの**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正しました[＃57176](https://github.com/pingcap/tidb/issues/57176) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   統計情報が収集されていないテーブルの最後の`ANALYZE`回がNULLにならない可能性がある問題を修正しました[＃57735](https://github.com/pingcap/tidb/issues/57735) @ [ウィノロス](https://github.com/winoros)
    -   統計の不適切な例外処理により、バックグラウンドタスクがタイムアウトしたときにメモリ内の統計が誤って削除される問題を修正しました[＃57901](https://github.com/pingcap/tidb/issues/57901) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `DROP DATABASE`文[＃57230](https://github.com/pingcap/tidb/issues/57230) @ [ラスティン170506](https://github.com/Rustin170506)を実行した後に統計がクリアされない問題を修正しました
    -   `IndexMerge` [＃58476](https://github.com/pingcap/tidb/issues/58476) @ [ホーキングレイ](https://github.com/hawkingrei)を構築するときに一部の述語が失われる可能性がある問題を修正しました
    -   3000次元以上の列にベクトル検索インデックスを作成すると、 `KeyTooLong`エラー[＃58836](https://github.com/pingcap/tidb/issues/58836) @ [そよ風のような](https://github.com/breezewish)が発生する問題を修正しました。
    -   `REORGANIZE PARTITION`操作で置換されたグローバルインデックスが正しくクリーンアップされず、非クラスタ化テーブル[＃56822](https://github.com/pingcap/tidb/issues/56822) @ [ミョンス](https://github.com/mjonss)の一意のインデックスが処理されない問題を修正しました。
    -   パーティションテーブルの範囲INTERVAL構文シュガーが、間隔[＃57698](https://github.com/pingcap/tidb/issues/57698) @ [ミョンス](https://github.com/mjonss)として`MINUTE`使用することをサポートしない問題を修正しました。
    -   タイムゾーンを変更すると、スローログ[＃58452](https://github.com/pingcap/tidb/issues/58452) @ [lcwangchao](https://github.com/lcwangchao)をクエリするときに誤ったクエリ結果が発生する問題を修正しました。
    -   スキャンタスク[＃57708](https://github.com/pingcap/tidb/issues/57708) @ [ヤンケオ](https://github.com/YangKeao)の TTL ワーカーを縮小するときに、タスクのキャンセルが失敗するとタスクがリークする可能性がある問題を修正しました。
    -   ハートビートが失われ、TTLテーブルが削除または無効になった後も、TTLジョブが[＃57702](https://github.com/pingcap/tidb/issues/57702) @ [ヤンケオ](https://github.com/YangKeao)で実行され続ける問題を修正しました。
    -   TTLジョブがキャンセルされた後に`last_job_finish_time`誤って表示される問題を修正[＃58109](https://github.com/pingcap/tidb/issues/58109) @ [ヤンケオ](https://github.com/YangKeao)
    -   TiDBハートビートが失われた場合に TTL ジョブをキャンセルできない問題を修正[＃57784](https://github.com/pingcap/tidb/issues/57784) @ [ヤンケオ](https://github.com/YangKeao)
    -   ハートビートを失った TTL ジョブが他のジョブのハートビート[＃57915](https://github.com/pingcap/tidb/issues/57915) @ [ヤンケオ](https://github.com/YangKeao)の取得をブロックする問題を修正しました
    -   TTLワーカーを縮小するときに、期限切れの行が削除されない問題を修正[＃57990](https://github.com/pingcap/tidb/issues/57990) @ [lcwangchao](https://github.com/lcwangchao)
    -   TTL削除レートリミッタが中断されたときに残りの行が再試行されない問題を修正[＃58205](https://github.com/pingcap/tidb/issues/58205) @ [lcwangchao](https://github.com/lcwangchao)
    -   特定のケースでTTLが大量の警告ログを生成する可能性がある問題を修正[＃58305](https://github.com/pingcap/tidb/issues/58305) @ [lcwangchao](https://github.com/lcwangchao)
    -   `tidb_ttl_delete_rate_limit` [＃58484](https://github.com/pingcap/tidb/issues/58484) @ [lcwangchao](https://github.com/lcwangchao)を変更するときに一部の TTL ジョブがハングする可能性がある問題を修正しました
    -   `REORGANIZE PARTITION`中にデータのバックフィルを行うと、同時更新が[＃58226](https://github.com/pingcap/tidb/issues/58226) @ [ミョンス](https://github.com/mjonss)にロールバックされる可能性がある問題を修正しました。
    -   `cluster_slow_query table`クエリするときに`ORDER BY`使用すると、順序付けられていない結果[＃51723](https://github.com/pingcap/tidb/issues/51723) @ [定義2014](https://github.com/Defined2014)が生成される可能性がある問題を修正しました。

-   TiKV

    -   GBK/GB18030エンコードデータ[＃17618](https://github.com/tikv/tikv/issues/17618) @ [CbcWestwolf](https://github.com/CbcWestwolf)処理時にエンコードが失敗する可能性がある問題を修正
    -   TiKV MVCC インメモリエンジン (IME) が[＃18046](https://github.com/tikv/tikv/issues/18046) @ [金星の上](https://github.com/overvenus)でレプリカをプリロードするときに、初期化されていないレプリカが原因で TiKV がパニックになる問題を修正しました。
    -   リージョンを[＃17602](https://github.com/tikv/tikv/issues/17602)対[LykxSassinator](https://github.com/LykxSassinator)に分割した後、リーダーをすぐに選出できない問題を修正しました
    -   ディスクが[＃17939](https://github.com/tikv/tikv/issues/17939) @ [LykxSassinator](https://github.com/LykxSassinator)でスタックしているときに TiKV が PD にハートビートを報告できない問題を修正しました

-   PD

    -   `tidb_enable_tso_follower_proxy`システム変数が有効になっているときに PD がpanic可能性がある問題を修正[＃8950](https://github.com/tikv/pd/issues/8950) @ [okJiang](https://github.com/okJiang)
    -   同じストアID [＃8756](https://github.com/tikv/pd/issues/8756) @ [okJiang](https://github.com/okJiang)で繰り返し作成された場合に`evict-leader-scheduler`正常に動作しない問題を修正

-   TiFlash

    -   分散storageとコンピューティングアーキテクチャ[＃9665](https://github.com/pingcap/tiflash/issues/9665) @ [ジムララ](https://github.com/zimulala)で新しい列をクエリすると誤った結果が返される可能性がある問題を修正しました
    -   メモリ使用量が少ないときにTiFlash が予期せずRaftメッセージの処理を拒否する可能性がある問題を修正[＃9745](https://github.com/pingcap/tiflash/issues/9745) @ [カルビンネオ](https://github.com/CalvinNeo)
    -   TiFlashの`POSITION()`関数が文字セット照合[＃9377](https://github.com/pingcap/tiflash/issues/9377) @ [xzhangxian1008](https://github.com/xzhangxian1008)をサポートしていない問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   PITRが3072バイトを超えるインデックスの復元に失敗する問題を修正[＃58430](https://github.com/pingcap/tidb/issues/58430) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   新しい TiKV ノードがクラスター[＃11766](https://github.com/pingcap/tiflow/issues/11766) @ [リデジュ](https://github.com/lidezhu)に追加された後に、変更フィードが停止する可能性がある問題を修正しました。
        -   `RENAME TABLE` DDL 文[＃11946](https://github.com/pingcap/tiflow/issues/11946) @ [ケニーtm](https://github.com/kennytm)を処理するときに、イベント フィルタがフィルタリングに古いテーブル名ではなく新しいテーブル名を誤って使用する問題を修正しました。
        -   チェンジフィードが削除された後に goroutines リークが発生する問題を修正[＃11954](https://github.com/pingcap/tiflow/issues/11954) @ [ヒック](https://github.com/hicqu)
        -   Sarama クライアントによって再送信された順序が乱れたメッセージによって Kafka メッセージの順序が正しくなくなる問題を修正[＃11935](https://github.com/pingcap/tiflow/issues/11935) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   DebeziumプロトコルのNOT NULLタイムスタンプフィールドのデフォルト値が正しくない問題を修正[＃11966](https://github.com/pingcap/tiflow/issues/11966) @ [wk989898](https://github.com/wk989898)
