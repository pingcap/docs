---
title: TiDB 2.1.13 Release Notes
---

# TiDB 2.1.13 リリースノート {#tidb-2-1-13-release-notes}

発売日：2019年6月21日

TiDB バージョン: 2.1.13

TiDB Ansible バージョン: 2.1.13

## TiDB {#tidb}

-   ホットスポットの問題を軽減するために、列に`AUTO_INCREMENT`属性が含まれる場合に`SHARD_ROW_ID_BITS`を使用して行 ID を分散する機能を追加します[#10788](https://github.com/pingcap/tidb/pull/10788)
-   無効な DDL メタデータの存続期間を最適化し、TiDB クラスターのアップグレード後の DDL 操作の通常の実行の回復を高速化します[#10789](https://github.com/pingcap/tidb/pull/10789)
-   `execdetails.ExecDetails`ポインタ[#10833](https://github.com/pingcap/tidb/pull/10833)によってコプロセッサーリソースを迅速に解放できないことが原因で発生する、同時実行シナリオでの OOM 問題を修正します。
-   統計[#10772](https://github.com/pingcap/tidb/pull/10772)を更新するかどうかを制御する`update-stats`構成項目を追加します。
-   ホットスポットの問題を解決するために、リージョンの事前分割をサポートする次の TiDB 固有の構文を追加します。
-   `PRE_SPLIT_REGIONS`テーブルのオプション[#10863](https://github.com/pingcap/tidb/pull/10863)を追加します。
-   `SPLIT TABLE table_name INDEX index_name`構文[#10865](https://github.com/pingcap/tidb/pull/10865)を追加します。
-   `SPLIT TABLE [table_name] BETWEEN (min_value...) AND (max_value...) REGIONS [region_num]`構文[#10882](https://github.com/pingcap/tidb/pull/10882)を追加します。
-   場合によっては`KILL`構文によって引き起こされるpanicの問題を修正します[#10879](https://github.com/pingcap/tidb/pull/10879)
-   `ADD_DATE`場合によっては MySQL との互換性を向上[#10718](https://github.com/pingcap/tidb/pull/10718)
-   インデックス結合[#10856](https://github.com/pingcap/tidb/pull/10856)における内部テーブル選択の選択率の誤った推定を修正しました。

## TiKV {#tikv}

-   イテレータがステータス[#4940](https://github.com/tikv/tikv/pull/4940)をチェックしないことにより、システム内で不完全なスナップショットが生成される問題を修正します。
-   `block-size`構成の妥当性をチェックする機能を追加[#4930](https://github.com/tikv/tikv/pull/4930)

## ツール {#tools}

-   TiDBBinlog
    -   データ[#640](https://github.com/pingcap/tidb-binlog/pull/640)の書き込みに失敗したときにPumpが戻り値をチェックしないことによって引き起こされる間違ったオフセットの問題を修正しました。
    -   コンテナ環境[#634](https://github.com/pingcap/tidb-binlog/pull/634)でブリッジ モードをサポートするために、 Drainerに`advertise-addr`構成を追加します。
