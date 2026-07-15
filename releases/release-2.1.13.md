---
title: TiDB 2.1.13 Release Notes
summary: TiDB 2.1.13は2019年6月21日にリリースされました。行IDの分散、DDLメタデータの有効期間の最適化、OOM問題の修正、統計の更新、リージョン事前分割のサポート、MySQL互換性の向上、推定問題の修正などの機能が含まれています。TiKVは不完全なスナップショットを修正し、ブロックサイズ設定の妥当性をチェックする機能を追加しました。TiDB Binlogは誤ったオフセットを修正し、 Drainerにadvertise-addr設定を追加しました。
---

# TiDB 2.1.13 リリースノート {#tidb-2-1-13-release-notes}

発売日：2019年6月21日

TiDB バージョン: 2.1.13

TiDB Ansible バージョン: 2.1.13

## TiDB {#tidb}

-   ホットスポットの問題を軽減するために、列に`AUTO_INCREMENT`属性が含まれている場合に`SHARD_ROW_ID_BITS`使用して行 ID を分散させる機能を追加します[＃10788](https://github.com/pingcap/tidb/pull/10788)
-   無効な DDL メタデータの有効期間を最適化して、TiDB クラスタアップグレード後に DDL 操作の通常の実行を回復する速度を向上します。 [＃10789](https://github.com/pingcap/tidb/pull/10789)
-   `execdetails.ExecDetails`ポインタの結果としてコプロセッサーリソースを迅速に解放できないことによって引き起こされる、高同時シナリオでのOOM問題を修正しました。 [＃10833](https://github.com/pingcap/tidb/pull/10833)
-   統計情報を更新するかどうかを制御する`update-stats`構成項目を追加します[＃10772](https://github.com/pingcap/tidb/pull/10772)
-   ホットスポット問題を解決するために、リージョンプリスプリットをサポートする次の TiDB 固有の構文を追加します。
-   `PRE_SPLIT_REGIONS`テーブルオプションを追加する [＃10863](https://github.com/pingcap/tidb/pull/10863)
-   `SPLIT TABLE table_name INDEX index_name`構文追加する [＃10865](https://github.com/pingcap/tidb/pull/10865)
-   `SPLIT TABLE [table_name] BETWEEN (min_value...) AND (max_value...) REGIONS [region_num]`構文追加する [＃10882](https://github.com/pingcap/tidb/pull/10882)
-   `KILL`構文によって発生するpanic問題を修正[＃10879](https://github.com/pingcap/tidb/pull/10879)
-   MySQLとの互換性を`ADD_DATE`の場合改善 [＃10718](https://github.com/pingcap/tidb/pull/10718)
-   インデックス結合における内部テーブル選択の選択率の誤った推定を修正 [＃10856](https://github.com/pingcap/tidb/pull/10856)

## TiKV {#tikv}

-   イテレータがステータスをチェックしないために、システム内に不完全なスナップショットが生成される問題を修正しました。 [＃4940](https://github.com/tikv/tikv/pull/4940)
-   `block-size`構成の有効性をチェックする機能を追加します [＃4930](https://github.com/tikv/tikv/pull/4930)

## ツール {#tools}

-   TiDB Binlog
    -   データの書き込みに失敗したときにPumpが戻り値をチェックしないことによって発生する間違ったオフセットの問題を修正しました[＃640](https://github.com/pingcap/tidb-binlog/pull/640)
    -   コンテナ環境でブリッジモードをサポートするために、 Drainerに`advertise-addr`構成を追加します。 [＃634](https://github.com/pingcap/tidb-binlog/pull/634)
