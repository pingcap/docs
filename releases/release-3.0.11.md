---
title: TiDB 3.0.11 Release Notes
---

# TiDB 3.0.11 リリースノート {#tidb-3-0-11-release-notes}

発売日：2020年3月4日

TiDB バージョン: 3.0.11

TiDB アンシブル バージョン: 3.0.11

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の 3.0.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   3.0.7 より前の TiDB バージョンまたは MySQL [#15057](https://github.com/pingcap/tidb/pull/15057)の動作と互換性のある、最大インデックス長を制御する`max-index-length`構成項目を追加します。

## 新機能 {#new-features}

-   TiDB
    -   `information_schema.PARTITIONS`テーブル[#14849](https://github.com/pingcap/tidb/pull/14849)で分割されたテーブルのメタ情報を表示するサポート

-   TiDBBinlog
    -   TiDB クラスタ間の双方向データ複製をサポート[#884](https://github.com/pingcap/tidb-binlog/pull/884) [#909](https://github.com/pingcap/tidb-binlog/pull/909)

-   TiDB Lightning
    -   TLS 構成のサポート[#44](https://github.com/tikv/importer/pull/44) [#270](https://github.com/pingcap/tidb-lightning/pull/270)

-   TiDB アンシブル
    -   制御マシンのユーザーが`ansible_user` [#1184](https://github.com/pingcap/tidb-ansible/pull/1184)と一致する必要がないように、 `create_users.yml`のロジックを変更します。

## バグの修正 {#bug-fixes}

-   TiDB
    -   `Union`使用するクエリは読み取り専用とマークされていないため、楽観的トランザクションを再試行するときにゴルーチン リークが発生する問題を修正します[#15076](https://github.com/pingcap/tidb/pull/15076)
    -   `SET SESSION tidb_snapshot = 'xxx';`ステートメントの実行時に`tidb_snapshot`パラメーターの値が正しく使用されていないため、 `SHOW TABLE STATUS`スナップショット時のテーブルステータスを正しく出力できない問題を修正[#14391](https://github.com/pingcap/tidb/pull/14391)
    -   `Sort Merge Join`と`ORDER BY DESC`を同時に含む SQL ステートメントによって引き起こされる誤った結果を修正する[#14664](https://github.com/pingcap/tidb/pull/14664)
    -   サポートされていない式を使用してパーティション テーブルを作成すると、TiDBサーバーがパニックにpanicを修正しました。このpanicを修正すると、エラー情報`This partition function is not allowed`が返されます。 [#14769](https://github.com/pingcap/tidb/pull/14769)
    -   `Union` [#14944](https://github.com/pingcap/tidb/pull/14944)を含むサブクエリで`select max() from subquery`ステートメントを実行すると、誤った結果が発生した問題を修正しました。
    -   実行バインディングをドロップする`DROP BINDING`を実行した後に`SHOW BINDINGS`ステートメントを実行すると、エラー メッセージが返される問題を修正します[#14865](https://github.com/pingcap/tidb/pull/14865)
    -   MySQL プロトコルではクエリのエイリアスの最大長が 256 文字であるために接続が切断される問題を修正しますが、TiDB はこのプロトコルによるクエリ結果で[エイリアスをカット](https://dev.mysql.com/doc/refman/8.0/en/identifier-length.html)を実行しません[#14940](https://github.com/pingcap/tidb/pull/14940)
    -   文字列型 in `DIV`を使用したときに発生する可能性のある誤ったクエリ結果を修正します。たとえば、 `select 1 / '2007' div 1`ステートメント[#14098](https://github.com/pingcap/tidb/pull/14098)を正しく実行できるようになりました。

-   TiKV
    -   不要なログを削除してログ出力を最適化する[#6657](https://github.com/tikv/tikv/pull/6657)
    -   高負荷時にピアが削除されたときに発生する可能性があるpanicを修正します[#6704](https://github.com/tikv/tikv/pull/6704)
    -   場合によっては Hibernate Regions が起動しない問題を修正[#6732](https://github.com/tikv/tikv/pull/6732) [#6738](https://github.com/tikv/tikv/pull/6738)

-   TiDB アンシブル
    -   `tidb-ansible` [#1169](https://github.com/pingcap/tidb-ansible/pull/1169)の古いドキュメント リンクを更新する
    -   `wait for region replication complete`タスク[#1173](https://github.com/pingcap/tidb-ansible/pull/1173)で未定義変数が発生することがある問題を修正
