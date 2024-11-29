---
title: TiDB 2.1.13 Release Notes
summary: TiDB 2.1.13 は、2019 年 6 月 21 日にリリースされました。行 ID を分散する機能、DDL メタデータの有効期間を最適化する機能、OOM 問題を修正する機能、統計情報を更新する機能、リージョンプリスプリットをサポートする機能、MySQL 互換性を向上させる機能、および推定問題を修正する機能が含まれています。TiKV は不完全なスナップショットを修正し、ブロック サイズ構成の有効性をチェックする機能を追加します。TiDB Binlog は間違ったオフセットを修正し、 Drainerに Advertise-addr 構成を追加します。
---

# TiDB 2.1.13 リリースノート {#tidb-2-1-13-release-notes}

発売日: 2019年6月21日

TiDB バージョン: 2.1.13

TiDB Ansible バージョン: 2.1.13

## ティビ {#tidb}

-   ホットスポットの問題を軽減するために、列に`AUTO_INCREMENT`属性が含まれている場合に`SHARD_ROW_ID_BITS`使用して行 ID を分散させる機能を追加します[＃10788](https://github.com/pingcap/tidb/pull/10788)
-   無効な DDL メタデータの有効期間を最適化して、TiDB クラスター[＃10789](https://github.com/pingcap/tidb/pull/10789)のアップグレード後に DDL 操作の通常の実行を回復する時間を短縮します。
-   `execdetails.ExecDetails`ポインタ[＃10833](https://github.com/pingcap/tidb/pull/10833)の結果としてコプロセッサーリソースを迅速に解放できないことによって引き起こされる、高同時シナリオでのOOM問題を修正しました。
-   統計情報を更新するかどうかを制御する`update-stats`構成項目を追加します[＃10772](https://github.com/pingcap/tidb/pull/10772)
-   ホットスポットの問題を解決するために、リージョンの事前分割をサポートする次の TiDB 固有の構文を追加します。
-   `PRE_SPLIT_REGIONS`テーブルオプション[＃10863](https://github.com/pingcap/tidb/pull/10863)を追加
-   `SPLIT TABLE table_name INDEX index_name`構文[＃10865](https://github.com/pingcap/tidb/pull/10865)追加する
-   `SPLIT TABLE [table_name] BETWEEN (min_value...) AND (max_value...) REGIONS [region_num]`構文[＃10882](https://github.com/pingcap/tidb/pull/10882)追加する
-   場合によっては`KILL`構文によって発生するpanic問題を修正[＃10879](https://github.com/pingcap/tidb/pull/10879)
-   MySQLとの互換性を`ADD_DATE`の場合[＃10718](https://github.com/pingcap/tidb/pull/10718)で改善
-   インデックス結合[＃10856](https://github.com/pingcap/tidb/pull/10856)における内部テーブル選択の選択率の誤った推定を修正

## ティクヴ {#tikv}

-   イテレータがステータス[＃4940](https://github.com/tikv/tikv/pull/4940)をチェックしないために、システム内に不完全なスナップショットが生成される問題を修正しました。
-   `block-size`構成[＃4930](https://github.com/tikv/tikv/pull/4930)の有効性をチェックする機能を追加する

## ツール {#tools}

-   TiDBBinlog
    -   データの書き込みに失敗したときにPumpが戻り値をチェックしないことによって発生する間違ったオフセットの問題を修正[＃640](https://github.com/pingcap/tidb-binlog/pull/640)
    -   コンテナ環境[＃634](https://github.com/pingcap/tidb-binlog/pull/634)でブリッジモードをサポートするために、 Drainerに`advertise-addr`構成を追加します。
