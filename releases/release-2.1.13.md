---
title: TiDB 2.1.13 Release Notes
---

# TiDB 2.1.13 リリースノート {#tidb-2-1-13-release-notes}

発売日：2019年6月21日

TiDB バージョン: 2.1.13

TiDB アンシブル バージョン: 2.1.13

## TiDB {#tidb}

-   ホットスポットの問題を軽減するために、列に`AUTO_INCREMENT`属性が含まれている場合に`SHARD_ROW_ID_BITS`を使用して行 ID を分散させる機能を追加します[#10788](https://github.com/pingcap/tidb/pull/10788)
-   無効な DDL メタデータの有効期間を最適化して、TiDB クラスターのアップグレード後に DDL 操作の通常の実行を回復する速度を上げます[#10789](https://github.com/pingcap/tidb/pull/10789)
-   `execdetails.ExecDetails`ポインター[#10833](https://github.com/pingcap/tidb/pull/10833)が原因で、コプロセッサーリソースを迅速に解放できなかったことが原因で発生した同時実行の多いシナリオでの OOM の問題を修正します。
-   統計を更新するかどうかを制御する`update-stats`構成項目を追加します[#10772](https://github.com/pingcap/tidb/pull/10772)
-   次の TiDB 固有の構文を追加して、リージョンの事前分割をサポートし、ホットスポットの問題を解決します。
-   `PRE_SPLIT_REGIONS`テーブル オプション[#10863](https://github.com/pingcap/tidb/pull/10863)を追加します。
-   `SPLIT TABLE table_name INDEX index_name`構文[#10865](https://github.com/pingcap/tidb/pull/10865)を追加
-   `SPLIT TABLE [table_name] BETWEEN (min_value...) AND (max_value...) REGIONS [region_num]`構文[#10882](https://github.com/pingcap/tidb/pull/10882)を追加
-   場合によっては`KILL`構文によって引き起こされるpanicの問題を修正します[#10879](https://github.com/pingcap/tidb/pull/10879)
-   場合によっては`ADD_DATE`の MySQL との互換性を向上させます[#10718](https://github.com/pingcap/tidb/pull/10718)
-   インデックス結合[#10856](https://github.com/pingcap/tidb/pull/10856)の内部テーブル選択の選択率の間違った見積もりを修正します。

## TiKV {#tikv}

-   イテレーターがステータスをチェックしないために、システムで不完全なスナップショットが生成される問題を修正します[#4940](https://github.com/tikv/tikv/pull/4940)
-   `block-size`構成の有効性をチェックする機能を追加します[#4930](https://github.com/tikv/tikv/pull/4930)

## ツール {#tools}

-   TiDBBinlog
    -   データの書き込みに失敗したときにPumpが戻り値をチェックしないことによって引き起こされる間違ったオフセットの問題を修正します[#640](https://github.com/pingcap/tidb-binlog/pull/640)
    -   Drainerに`advertise-addr`構成を追加して、コンテナー環境でブリッジ モードをサポートする[#634](https://github.com/pingcap/tidb-binlog/pull/634)
