---
title: TiDB 2.1.13 Release Notes
---

# TiDB2.1.13リリースノート {#tidb-2-1-13-release-notes}

発売日：2019年6月21日

TiDBバージョン：2.1.13

TiDB Ansibleバージョン：2.1.13

## TiDB {#tidb}

-   ホットスポットの問題を軽減するために、列に`AUTO_INCREMENT`属性が含まれている場合に、 `SHARD_ROW_ID_BITS`を使用して行IDを分散する機能を追加します[＃10788](https://github.com/pingcap/tidb/pull/10788)
-   無効なDDLメタデータの有効期間を最適化して、TiDBクラスタのアップグレード後のDDL操作の通常の実行の回復を高速化します[＃10789](https://github.com/pingcap/tidb/pull/10789)
-   `execdetails.ExecDetails`ポインター[＃10833](https://github.com/pingcap/tidb/pull/10833)が原因で、コプロセッサーリソースを迅速に解放できなかったために発生した、同時発生率の高いシナリオでのOOMの問題を修正します。
-   `update-stats`の構成アイテムを追加して、統計を更新するかどうかを制御します[＃10772](https://github.com/pingcap/tidb/pull/10772)
-   ホットスポットの問題を解決するためにリージョンをサポートするには、次のTiDB固有の構文を追加します。
-   `PRE_SPLIT_REGIONS`テーブルオプション[＃10863](https://github.com/pingcap/tidb/pull/10863)を追加します
-   `SPLIT TABLE table_name INDEX index_name`構文[＃10865](https://github.com/pingcap/tidb/pull/10865)を追加します
-   `SPLIT TABLE [table_name] BETWEEN (min_value...) AND (max_value...) REGIONS [region_num]`構文[＃10882](https://github.com/pingcap/tidb/pull/10882)を追加します
-   場合によっては`KILL`構文によって引き起こされるpanicの問題を修正します[＃10879](https://github.com/pingcap/tidb/pull/10879)
-   MySQLとの互換性を改善する`ADD_DATE`場合によっては[＃10718](https://github.com/pingcap/tidb/pull/10718)
-   インデックス結合[＃10856](https://github.com/pingcap/tidb/pull/10856)での内部テーブル選択の選択率の誤った推定を修正しました

## TiKV {#tikv}

-   イテレータがステータスをチェックしないためにシステムで不完全なスナップショットが生成される問題を修正します[＃4940](https://github.com/tikv/tikv/pull/4940)
-   `block-size`構成の有効性を確認する機能を追加します[＃4930](https://github.com/tikv/tikv/pull/4930)

## ツール {#tools}

-   TiDB Binlog
    -   データの書き込みに失敗したときにPumpが戻り値をチェックしないことによって引き起こされる誤ったオフセットの問題を修正します[＃640](https://github.com/pingcap/tidb-binlog/pull/640)
    -   コンテナ環境でブリッジモードをサポートするために、 Drainerに`advertise-addr`の構成を追加します[＃634](https://github.com/pingcap/tidb-binlog/pull/634)
