---
title: TiDB 2.1.13 Release Notes
---

# TiDB 2.1.13 リリースノート {#tidb-2-1-13-release-notes}

発売日：2019年6月21日

TiDB バージョン: 2.1.13

TiDB Ansible バージョン: 2.1.13

## TiDB {#tidb}

-   ホットスポットの問題を軽減するために、列に`AUTO_INCREMENT`属性が含まれる場合に`SHARD_ROW_ID_BITS`を使用して行 ID を分散する機能を追加します[<a href="https://github.com/pingcap/tidb/pull/10788">#10788</a>](https://github.com/pingcap/tidb/pull/10788)
-   無効な DDL メタデータの存続期間を最適化し、TiDB クラスターのアップグレード後の DDL 操作の通常の実行の回復を高速化します[<a href="https://github.com/pingcap/tidb/pull/10789">#10789</a>](https://github.com/pingcap/tidb/pull/10789)
-   `execdetails.ExecDetails`ポインタ[<a href="https://github.com/pingcap/tidb/pull/10833">#10833</a>](https://github.com/pingcap/tidb/pull/10833)によってコプロセッサーリソースを迅速に解放できないことが原因で発生する、同時実行シナリオの OOM 問題を修正します。
-   統計[<a href="https://github.com/pingcap/tidb/pull/10772">#10772</a>](https://github.com/pingcap/tidb/pull/10772)を更新するかどうかを制御する`update-stats`構成項目を追加します。
-   ホットスポットの問題を解決するために、リージョンの事前分割をサポートする次の TiDB 固有の構文を追加します。
-   `PRE_SPLIT_REGIONS`テーブルのオプション[<a href="https://github.com/pingcap/tidb/pull/10863">#10863</a>](https://github.com/pingcap/tidb/pull/10863)を追加します。
-   `SPLIT TABLE table_name INDEX index_name`構文[<a href="https://github.com/pingcap/tidb/pull/10865">#10865</a>](https://github.com/pingcap/tidb/pull/10865)を追加します。
-   `SPLIT TABLE [table_name] BETWEEN (min_value...) AND (max_value...) REGIONS [region_num]`構文[<a href="https://github.com/pingcap/tidb/pull/10882">#10882</a>](https://github.com/pingcap/tidb/pull/10882)を追加します。
-   場合によっては`KILL`構文によって引き起こされるpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/10879">#10879</a>](https://github.com/pingcap/tidb/pull/10879)
-   `ADD_DATE`場合によっては MySQL との互換性を向上[<a href="https://github.com/pingcap/tidb/pull/10718">#10718</a>](https://github.com/pingcap/tidb/pull/10718)
-   インデックス結合[<a href="https://github.com/pingcap/tidb/pull/10856">#10856</a>](https://github.com/pingcap/tidb/pull/10856)における内部テーブル選択の選択率の誤った推定を修正しました。

## TiKV {#tikv}

-   イテレータがステータス[<a href="https://github.com/tikv/tikv/pull/4940">#4940</a>](https://github.com/tikv/tikv/pull/4940)をチェックしないことにより、システム内で不完全なスナップショットが生成される問題を修正します。
-   `block-size`構成の妥当性をチェックする機能を追加[<a href="https://github.com/tikv/tikv/pull/4930">#4930</a>](https://github.com/tikv/tikv/pull/4930)

## ツール {#tools}

-   TiDBBinlog
    -   データ[<a href="https://github.com/pingcap/tidb-binlog/pull/640">#640</a>](https://github.com/pingcap/tidb-binlog/pull/640)の書き込みに失敗したときにPumpが戻り値をチェックしないことによって引き起こされる間違ったオフセットの問題を修正しました。
    -   コンテナ環境[<a href="https://github.com/pingcap/tidb-binlog/pull/634">#634</a>](https://github.com/pingcap/tidb-binlog/pull/634)でブリッジ モードをサポートするために、 Drainerに`advertise-addr`構成を追加します。
