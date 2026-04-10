---
title: TiDB 8.5.1 Release Notes
summary: TiDB 8.5.1におけるオペレーティングシステムとプラットフォームの要件変更、互換性の変更、改善点、およびバグ修正について学びましょう。
---

# TiDB 8.5.1 リリースノート {#tidb-8-5-1-release-notes}

発売日：2025年1月17日

TiDBバージョン：8.5.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb)| [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## オペレーティングシステムとプラットフォームの要件変更 {#operating-system-and-platform-requirement-changes}

バージョン8.5.1以降、TiDBはCentOS Linux 7のテストを再開し、互換性を確保しています。TiDB v8.5をデプロイする場合、またはクラスタをv8.5にアップグレードする場合は、TiDB v8.5.1以降のバージョンを使用してください。

-   TiDB v8.4.0 DMR および v8.5.0 リリースは[2024年6月30日をもってサポート終了となります。](https://www.redhat.com/en/topics/linux/centos-linux-eol) CentOS 7 上の TiDB クラスターを v8.4.0 または v8.5.0 にアップグレードすると、クラスターが使用できなくなるリスクが発生します。

-   現在も CentOS Linux 7 を使用しているユーザーを支援するために、TiDB は v8.5.1 から CentOS Linux 7 のテストを再開します。ただし、CentOS Linux の EOL ステータスのため、CentOS Linux 7 の[公式発表およびセキュリティに関するガイダンス](https://www.redhat.com/en/blog/centos-linux-has-reached-its-end-life-eol)およびセキュリティに関するガイダンスを確認し、Rocky Linux 9.1 以降などの本番使用用の[TiDBがサポートするオペレーティングシステム](/hardware-and-software-requirements.md#os-and-platform-requirements)する報酬システムに移行することを強くお勧めします。

CentOS Linux 7はサポート終了（EOL）を迎えたため、今後のTiDBリリースではこのディストリビューションのテストは中止されます。

## 互換性の変更 {#compatibility-changes}

-   TiDB統計キャッシュによるメモリ使用量を削減するため、 [`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)システム変数のデフォルト値`0`の意味が変更されました。

    -   v8.5.1より前では、 `0`統計キャッシュのメモリクォータがTiDBインスタンスの総メモリの50%であることを意味します。
    -   v8.5.1以降、 `0`は、統計キャッシュのメモリ割り当てがTiDBインスタンスの総メモリの20%であることを意味します。

## 改善点 {#improvements}

-   TiDB

    -   読み取り専用のユーザー定義変数を定数に折り畳む機能のサポート [#52742](https://github.com/pingcap/tidb/issues/52742) @[winoros](https://github.com/winoros)
    -   カルテシアン積セミジョイン（nulleq条件）をセミジョイン（等価条件）に変換 [#57583](https://github.com/pingcap/tidb/issues/57583) @[hawkingrei](https://github.com/hawkingrei)
    -   統計メモリキャッシュのデフォルトしきい値を総メモリの20%に調整 [#58014](https://github.com/pingcap/tidb/issues/58014) @[hawkingrei](https://github.com/hawkingrei)
    -   タイムスタンプの有効性チェックを強化 [#57786](https://github.com/pingcap/tidb/issues/57786) @[MyonKeminta](https://github.com/MyonKeminta)

-   ティクヴ

    -   無効な`max_ts`更新の検出メカニズムを追加 [#17916](https://github.com/tikv/tikv/issues/17916) @[ekexium](https://github.com/ekexium)

-   TiFlash

    -   分散型storageおよびコンピューティングアーキテクチャにおけるTiFlashコンピューティングノードの再試行戦略を最適化し、Amazon S3からのファイルダウンロード時に発生する例外を処理する [#9695](https://github.com/pingcap/tiflash/issues/9695) @[JinheLin](https://github.com/JinheLin)

-   ツール

    -   TiCDC

        -   TiCDCが購読していないイベントを事前にフィルタリングして、不要なリソース消費を回避する [#17877](https://github.com/tikv/tikv/issues/17877) @[hicqu](https://github.com/hicqu)

## バグ修正 {#bug-fixes}

-   TiDB

    -   TiFlashシステムテーブルへのクエリのデフォルトのタイムアウトが短すぎる問題を修正 [#57816](https://github.com/pingcap/tidb/issues/57816) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   `tidb_gogc_tuner_max_value`と`tidb_gogc_tuner_min_value`を設定する際に、最大値がnullの場合に誤った警告メッセージが表示される問題を修正しました。 [#57889](https://github.com/pingcap/tidb/issues/57889) @[hawkingrei](https://github.com/hawkingrei)
    -   プランキャッシュがインデックスを追加する際に誤ったスキーマを使用するため、データインデックスに一貫性がない問題を修正します [#56733](https://github.com/pingcap/tidb/issues/56733) @[wjhuang2016](https://github.com/wjhuang2016)
    -   Grafana の**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    -   収集された統計情報のないテーブルの最後の`ANALYZE`時刻が NULL にならない可能性がある問題を修正 [#57735](https://github.com/pingcap/tidb/issues/57735) @[winoros](https://github.com/winoros)
    -   バックグラウンドタスクがタイムアウトした際に、統計情報の例外処理が不適切であるためにメモリ内の統計情報が誤って削除される問題を修正 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    -   `DROP DATABASE`ステートメントの実行後に統計情報がクリアされない問題を修正しました [#57230](https://github.com/pingcap/tidb/issues/57230) @[Rustin170506](https://github.com/Rustin170506)
    -   `IndexMerge`を構築する際に一部の述語が失われる可能性がある問題を修正しました [#58476](https://github.com/pingcap/tidb/issues/58476) @[hawkingrei](https://github.com/hawkingrei)
    -   3000次元を超える列にベクトル検索インデックスを作成すると`KeyTooLong`エラーが発生する問題を修正 [#58836](https://github.com/pingcap/tidb/issues/58836) @[breezewish](https://github.com/breezewish)
    -   `REORGANIZE PARTITION`操作が置換されたグローバル インデックスを正しくクリーンアップせず、非クラスター化テーブルの一意インデックスを処理する問題を修正しました [#56822](https://github.com/pingcap/tidb/issues/56822) @[mjonss](https://github.com/mjonss)
    -   パーティションテーブルの Range INTERVAL 構文糖衣が`MINUTE`間隔として使用できない問題を修正 [#57698](https://github.com/pingcap/tidb/issues/57698) @[mjonss](https://github.com/mjonss)
    -   タイムゾーンを変更すると、スローログのクエリ時にクエリ結果が正しくなくなる問題を修正しました [#58452](https://github.com/pingcap/tidb/issues/58452) @[lcwangchao](https://github.com/lcwangchao)
    -   スキャンタスクのTTLワーカーを縮小する際に、タスクキャンセルの失敗によってタスクがリークする可能性がある問題を修正しました [#57708](https://github.com/pingcap/tidb/issues/57708) @[YangKeao](https://github.com/YangKeao)
    -   ハートビートが失われ、TTLテーブルが削除または無効化された後もTTLジョブが実行され続ける問題を修正 [#57702](https://github.com/pingcap/tidb/issues/57702) @[YangKeao](https://github.com/YangKeao)
    -   TTLジョブがキャンセルされた後に`last_job_finish_time`が正しく表示されない問題を修正 [#58109](https://github.com/pingcap/tidb/issues/58109) @[YangKeao](https://github.com/YangKeao)
    -   TiDBハートビートが失われた場合にTTLジョブをキャンセルできない問題を修正 [#57784](https://github.com/pingcap/tidb/issues/57784) @[YangKeao](https://github.com/YangKeao)
    -   ハートビートを失ったTTLジョブが他のジョブのハートビート受信をブロックする問題を修正 [#57915](https://github.com/pingcap/tidb/issues/57915) @[YangKeao](https://github.com/YangKeao)
    -   TTLワーカーを縮小した際に、期限切れの行の一部が削除されない問題を修正しました [#57990](https://github.com/pingcap/tidb/issues/57990) @[lcwangchao](https://github.com/lcwangchao)
    -   TTL削除レートリミッターが中断されたときに残りの行が再試行されない問題を修正 [#58205](https://github.com/pingcap/tidb/issues/58205) @[lcwangchao](https://github.com/lcwangchao)
    -   TTLが特定の場合に大量の警告ログを生成する可能性がある問題を修正 [#58305](https://github.com/pingcap/tidb/issues/58305) @[lcwangchao](https://github.com/lcwangchao)
    -   `tidb_ttl_delete_rate_limit`を変更する際に一部の TTL ジョブがハングアップする問題を修正しました [#58484](https://github.com/pingcap/tidb/issues/58484) @[lcwangchao](https://github.com/lcwangchao)
    -   `REORGANIZE PARTITION`のデータバックフィル中に同時更新がロールバックされる可能性がある問題を修正 [#58226](https://github.com/pingcap/tidb/issues/58226) @[mjonss](https://github.com/mjonss)
    -   `ORDER BY`をクエリする際に`cluster_slow_query table`を使用すると、結果が順不同になる可能性がある問題を修正しました [#51723](https://github.com/pingcap/tidb/issues/51723) @[Defined2014](https://github.com/Defined2014)

-   ティクヴ

    -   GBK/GB18030でエンコードされたデータを処理する際にエンコードが失敗する可能性がある問題を修正しました [#17618](https://github.com/tikv/tikv/issues/17618) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   TiKV MVCC In-Memory Engine (IME) がレプリカをプリロードするときに初期化されていないレプリカが原因で TiKV パニックが発生する問題を修正 [#18046](https://github.com/tikv/tikv/issues/18046) @[overvenus](https://github.com/overvenus)
    -   リージョン分割後にリーダーが迅速に選出されない問題を修正 [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    -   ディスクがスタックしているときに TiKV が PD にハートビートを報告できない問題を修正 [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator)

-   PD

    -   `tidb_enable_tso_follower_proxy`システム変数が有効になっている場合に PD がpanic可能性がある問題を修正しました [#8950](https://github.com/tikv/pd/issues/8950) @[okJiang](https://github.com/okJiang)
    -   `evict-leader-scheduler`が同じストア ID [#8756](https://github.com/tikv/pd/issues/8756)で繰り返し作成された場合に正しく動作しない問題を修正しました。@[okJiang](https://github.com/okJiang)

-   TiFlash

    -   分散storageおよびコンピューティングアーキテクチャにおいて、新しい列をクエリすると誤った結果が返される可能性がある問題を修正しました [#9665](https://github.com/pingcap/tiflash/issues/9665) @[zimulala](https://github.com/zimulala)
    -   メモリ使用量が低い場合、 TiFlash がRaftメッセージの処理を予期せず拒否する可能性がある問題を修正 [#9745](https://github.com/pingcap/tiflash/issues/9745) @[CalvinNeo](https://github.com/CalvinNeo)
    -   TiFlashの`POSITION()`関数が文字セット照合をサポートしていない問題を修正 [#9377](https://github.com/pingcap/tiflash/issues/9377) @[xzhangxian1008](https://github.com/xzhangxian1008)

-   ツール

    -   バックアップと復元 (BR)

        -   PITR が 3072 バイトを超えるインデックスの復元に失敗する問題を修正 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   新しい TiKV ノードがクラスターに追加された後に変更フィードが停止する可能性がある問題を修正します [#11766](https://github.com/pingcap/tiflow/issues/11766) @[lidezhu](https://github.com/lidezhu)
        -   イベントフィルターが`RENAME TABLE` DDL ステートメントを処理する際に、フィルタリングに古いテーブル名ではなく新しいテーブル名を誤って使用する問題を修正しました [#11946](https://github.com/pingcap/tiflow/issues/11946) @[kennytm](https://github.com/kennytm)
        -   変更フィードが削除された後にゴルーチンがリークする問題を修正 [#11954](https://github.com/pingcap/tiflow/issues/11954) @[hicqu](https://github.com/hicqu)
        -   Sarama クライアントによって再送信される順序が崩れたメッセージによって Kafka メッセージの順序が正しくなくなる問題を修正 [#11935](https://github.com/pingcap/tiflow/issues/11935) @[3AceShowHand](https://github.com/3AceShowHand)
        -   DebeziumプロトコルのNOT NULLタイムスタンプフィールドのデフォルト値が間違っている問題を修正 [#11966](https://github.com/pingcap/tiflow/issues/11966) @[wk989898](https://github.com/wk989898)
