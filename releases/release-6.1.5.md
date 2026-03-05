---
title: TiDB 6.1.5 Release Notes
summary: TiDB 6.1.5 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.1.5 リリースノート {#tidb-6-1-5-release-notes}

発売日：2023年2月28日

TiDB バージョン: 6.1.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   2023年2月20日以降、TiDBおよびTiDBダッシュボードの新しいバージョン（v6.1.5を含む）では、 [テレメトリ機能](/telemetry.md)デフォルトで無効化され、使用状況情報は収集されず、PingCAPと共有されません。これらのバージョンにアップグレードする前に、クラスターがデフォルトのテレメトリ設定を使用している場合、アップグレード後にテレメトリ機能が無効化されます。具体的なバージョンについては、 [TiDB リリース タイムライン](/releases/release-timeline.md)参照してください。

    -   [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数のデフォルト値が`ON`から`OFF`に変更されます。
    -   TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成項目のデフォルト値が`true`から`false`に変更されます。
    -   PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)構成項目のデフォルト値が`true`から`false`に変更されます。

-   v1.11.3 以降、新規に導入されたTiUPではテレメトリ機能がデフォルトで無効化され、使用状況情報は収集されません。v1.11.3 より前のバージョンのTiUPから v1.11.3 以降のバージョンにアップグレードした場合、テレメトリ機能はアップグレード前と同じ状態を維持します。

## 改善点 {#improvements}

-   TiDB

    -   `AUTO_RANDOM`列目をクラスター化複合インデックス[＃38572](https://github.com/pingcap/tidb/issues/38572) @ [接線](https://github.com/tangenta)の最初の列としてサポートします

## バグ修正 {#bug-fixes}

-   TiDB

    -   データ競合により TiDB が[＃27725](https://github.com/pingcap/tidb/issues/27725) @ [徐淮嶼](https://github.com/XuHuaiyu)で再起動する可能性がある問題を修正しました
    -   Read Committed分離レベルが使用されている場合、 `UPDATE`文が最新のデータを読み取らない可能性がある問題を修正しました[＃41581](https://github.com/pingcap/tidb/issues/41581) @ [cfzjywxk](https://github.com/cfzjywxk)

<!---->

-   PD

    -   `ReportMinResolvedTS`の呼び出しが[＃5965](https://github.com/tikv/pd/issues/5965) @ [フンドゥンDM](https://github.com/HunDunDM)で頻繁に発生する PD OOM 問題を修正しました

<!---->

-   ツール

    -   TiCDC

        -   レプリケーション遅延が過度に高い場合に、REDOログを適用するとOOMが発生する可能性がある問題を修正[＃8085](https://github.com/pingcap/tiflow/issues/8085) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   REDOログがメタ[＃8074](https://github.com/pingcap/tiflow/issues/8074) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)への書き込みを有効にするとパフォーマンスが低下する問題を修正しました

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドが[＃7373](https://github.com/pingcap/tiflow/issues/7373) @ [liumengya94](https://github.com/liumengya94)実行に失敗する問題を修正
        -   最後のbinlogがスキップされたDDL [＃8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3ハンター](https://github.com/D3Hunter)の場合にチェックポイントが進まない問題を修正しました
