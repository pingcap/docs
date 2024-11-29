---
title: TiDB 6.1.5 Release Notes
summary: TiDB 6.1.5 の互換性の変更、改善、バグ修正について説明します。
---

# TiDB 6.1.5 リリースノート {#tidb-6-1-5-release-notes}

発売日: 2023年2月28日

TiDB バージョン: 6.1.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   2023 年 2 月 20 日以降、v6.1.5 を含む TiDB および TiDB Dashboard の新しいバージョンでは[テレメトリ機能](/telemetry.md)がデフォルトで無効になっており、使用状況情報は収集されず、PingCAP と共有されません。これらのバージョンにアップグレードする前に、クラスターがデフォルトのテレメトリ構成を使用している場合、アップグレード後にテレメトリ機能が無効になります。特定のバージョンについては[TiDB リリース タイムライン](/releases/release-timeline.md)参照してください。

    -   [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402-and-deprecated-in-v810)システム変数のデフォルト値が`ON`から`OFF`に変更されます。
    -   TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402-and-deprecated-in-v810)構成項目のデフォルト値が`true`から`false`に変更されます。
    -   PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)構成項目のデフォルト値が`true`から`false`に変更されます。

-   v1.11.3 以降、新しく導入されたTiUPではテレメトリ機能がデフォルトで無効になっており、使用状況情報は収集されません。v1.11.3 より前のバージョンのTiUPから v1.11.3 以降のバージョンにアップグレードした場合、テレメトリ機能はアップグレード前と同じ状態を維持します。

## 改善点 {#improvements}

-   ティビ

    -   クラスター化複合インデックス[＃38572](https://github.com/pingcap/tidb/issues/38572) @ [タンジェンタ](https://github.com/tangenta)の最初の列として`AUTO_RANDOM`列をサポートします。

## バグ修正 {#bug-fixes}

-   ティビ

    -   データ競合により TiDB が[＃27725](https://github.com/pingcap/tidb/issues/27725) @ [徐懐玉](https://github.com/XuHuaiyu)で再起動する可能性がある問題を修正しました
    -   Read Committed分離レベルが使用されている場合、 `UPDATE`ステートメントが最新のデータを読み取らない可能性がある問題を修正しました[＃41581](https://github.com/pingcap/tidb/issues/41581) @ [翻訳](https://github.com/cfzjywxk)

<!---->

-   PD

    -   `ReportMinResolvedTS`の呼び出しが頻繁すぎる場合に発生する PD OOM 問題を修正[＃5965](https://github.com/tikv/pd/issues/5965) @ [フンドゥンDM](https://github.com/HunDunDM)

<!---->

-   ツール

    -   ティCDC

        -   レプリケーション遅延が過度に大きい場合に、REDO ログを適用すると OOM が発生する可能性がある問題を修正[＃8085](https://github.com/pingcap/tiflow/issues/8085) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   メタ[＃8074](https://github.com/pingcap/tiflow/issues/8074) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)への書き込みに REDO ログが有効になっている場合にパフォーマンスが低下する問題を修正しました。

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドが[＃7373](https://github.com/pingcap/tiflow/issues/7373) @ [りゅうめんぎゃ](https://github.com/liumengya94)の実行に失敗する問題を修正
        -   最後のbinlogがスキップされた DDL [＃8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3ハンター](https://github.com/D3Hunter)の場合にチェックポイントが進まない問題を修正しました
