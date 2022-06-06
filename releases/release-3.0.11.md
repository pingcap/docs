---
title: TiDB 3.0.11 Release Notes
---

# TiDB3.0.11リリースノート {#tidb-3-0-11-release-notes}

発売日：2020年3月4日

TiDBバージョン：3.0.11

TiDB Ansibleバージョン：3.0.11

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の3.0.xバージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   `max-index-length`の構成アイテムを追加して、最大インデックス長を制御します。これは、3.0.7より前のバージョンのTiDBまたは[＃15057](https://github.com/pingcap/tidb/pull/15057)の動作と互換性があります。

## 新機能 {#new-features}

-   TiDB
    -   `information_schema.PARTITIONS`テーブル[＃14849](https://github.com/pingcap/tidb/pull/14849)でのパーティションテーブルのメタ情報の表示をサポート

-   TiDB Binlog
    -   TiDBクラスター間の双方向データレプリケーションをサポートする[＃884](https://github.com/pingcap/tidb-binlog/pull/884) [＃909](https://github.com/pingcap/tidb-binlog/pull/909)

-   TiDB Lightning
    -   TLS構成をサポートする[＃44](https://github.com/tikv/importer/pull/44) [＃270](https://github.com/pingcap/tidb-lightning/pull/270)

-   TiDB Ansible
    -   制御マシンのユーザーが[＃1184](https://github.com/pingcap/tidb-ansible/pull/1184)と一致している必要がないように、 `create_users.yml`のロジックを変更し`ansible_user` 。

## バグの修正 {#bug-fixes}

-   TiDB
    -   `Union`を使用するクエリは読み取り専用としてマークされていないため、楽観的なトランザクションを再試行するときのGoroutineリークの問題を修正します[＃15076](https://github.com/pingcap/tidb/pull/15076)
    -   `SET SESSION tidb_snapshot = 'xxx';`ステートメント[＃14391](https://github.com/pingcap/tidb/pull/14391)の実行時に`tidb_snapshot`パラメーターの値が正しく使用されないため、スナップショット時に`SHOW TABLE STATUS`がテーブルステータスを正しく出力できない問題を修正します。
    -   `Sort Merge Join`と`ORDER BY DESC`を同時に含むSQLステートメントによって引き起こされる誤った結果を修正します[＃14664](https://github.com/pingcap/tidb/pull/14664)
    -   サポートされていない式を使用してパーティションテーブルを作成するときのTiDBサーバーのパニックを修正します。このパニックを修正すると、エラー情報`This partition function is not allowed`が返されます。 [＃14769](https://github.com/pingcap/tidb/pull/14769)
    -   [＃14944](https://github.com/pingcap/tidb/pull/14944)を含むサブクエリで`select max() from subquery`ステートメントを実行したときに発生した誤った結果を修正し`Union`
    -   `DROP BINDING`を実行した後に`SHOW BINDINGS`ステートメントを実行するとエラーメッセージが返され、実行バインディング[＃14865](https://github.com/pingcap/tidb/pull/14865)がドロップされる問題を修正します。
    -   クエリのエイリアスの最大長がMySQLプロトコルで256文字であるために接続が切断される問題を修正しますが、このプロトコル[＃14940](https://github.com/pingcap/tidb/pull/14940)に従ってクエリ結果でTiDBが[エイリアスをカット](https://dev.mysql.com/doc/refman/8.0/en/identifier-length.html)になりません
    -   `DIV`で文字列タイプを使用するときに発生する可能性のある誤ったクエリ結果を修正します。たとえば、 `select 1 / '2007' div 1`ステートメント[＃14098](https://github.com/pingcap/tidb/pull/14098)を正しく実行できるようになりました。

-   TiKV
    -   不要なログを削除してログ出力を最適化する[＃6657](https://github.com/tikv/tikv/pull/6657)
    -   高負荷でピアを取り外したときに発生する可能性のあるパニックを修正する[＃6704](https://github.com/tikv/tikv/pull/6704)
    -   場合によっては休止状態のリージョンがウェイクアップされない問題を修正し[＃6738](https://github.com/tikv/tikv/pull/6738) [＃6732](https://github.com/tikv/tikv/pull/6732)

-   TiDB Ansible
    -   [＃1169](https://github.com/pingcap/tidb-ansible/pull/1169)で古いドキュメントリンクを更新し`tidb-ansible`
    -   `wait for region replication complete`タスク[＃1173](https://github.com/pingcap/tidb-ansible/pull/1173)で未定義の変数が発生する可能性がある問題を修正します
