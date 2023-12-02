---
title: TiDB 6.1.5 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.1.5.
---

# TiDB 6.1.5 リリースノート {#tidb-6-1-5-release-notes}

発売日：2023年2月28日

TiDB バージョン: 6.1.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.1.5#version-list)

## 互換性の変更 {#compatibility-changes}

-   2023 年 2 月 20 日以降、v6.1.5 を含む TiDB および TiDB ダッシュボードの新しいバージョンでは[テレメトリ機能](/telemetry.md)がデフォルトで無効になり、使用状況情報は収集されず、PingCAP と共有されません。これらのバージョンにアップグレードする前に、クラスターでデフォルトのテレメトリ構成が使用されている場合、アップグレード後にテレメトリ機能は無効になります。特定のバージョンについては[TiDB リリース タイムライン](/releases/release-timeline.md)を参照してください。

    -   [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-new-in-v402)システム変数のデフォルト値が`ON`から`OFF`に変更されました。
    -   TiDB [`enable-telemetry`](/tidb-configuration-file.md#enable-telemetry-new-in-v402)構成項目のデフォルト値が`true`から`false`に変更されました。
    -   PD [`enable-telemetry`](/pd-configuration-file.md#enable-telemetry)設定項目のデフォルト値が`true`から`false`に変更されます。

-   v1.11.3 以降、新しく展開されたTiUPではテレメトリ機能がデフォルトで無効になっており、使用状況情報は収集されません。 TiUP のv1.11.3 より前のバージョンから v1.11.3 以降のバージョンにアップグレードすると、テレメトリ機能はアップグレード前と同じステータスを維持します。

## 改善点 {#improvements}

-   TiDB

    -   クラスター化複合インデックス[#38572](https://github.com/pingcap/tidb/issues/38572) @ [タンジェンタ](https://github.com/tangenta)の最初の列として`AUTO_RANDOM`列をサポートします。

## バグの修正 {#bug-fixes}

-   TiDB

    -   データ競合により TiDB が[#27725](https://github.com/pingcap/tidb/issues/27725) @ [徐淮嶼](https://github.com/XuHuaiyu)で再起動される可能性がある問題を修正
    -   Read Committed 分離レベル[#41581](https://github.com/pingcap/tidb/issues/41581) @ [cfzjywxk](https://github.com/cfzjywxk)が使用されている場合、 `UPDATE`ステートメントが最新のデータを読み取れない可能性がある問題を修正します。

<!---->

-   PD

    -   `ReportMinResolvedTS` [#5965](https://github.com/tikv/pd/issues/5965) @ [フンドゥンDM](https://github.com/HunDunDM)の呼び出しが頻繁すぎる場合に発生する PD OOM 問題を修正します。

<!---->

-   ツール

    -   TiCDC

        -   レプリケーション ラグが過度に高い場合に REDO ログを適用すると OOM が発生する可能性がある問題を修正[#8085](https://github.com/pingcap/tiflow/issues/8085) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDO ログがメタ[#8074](https://github.com/pingcap/tiflow/issues/8074) @ [CharlesCheung96](https://github.com/CharlesCheung96)への書き込みを有効にするとパフォーマンスが低下する問題を修正

    -   TiDB データ移行 (DM)

        -   `binlog-schema delete`コマンドの実行に失敗する問題を修正[#7373](https://github.com/pingcap/tiflow/issues/7373) @ [リウメンギャ94](https://github.com/liumengya94)
        -   最後のbinlogがスキップされた DDL [#8175](https://github.com/pingcap/tiflow/issues/8175) @ [D3ハンター](https://github.com/D3Hunter)である場合、チェックポイントが進められない問題を修正します。
