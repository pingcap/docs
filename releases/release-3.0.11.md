---
title: TiDB 3.0.11 Release Notes
---

# TiDB 3.0.11 リリースノート {#tidb-3-0-11-release-notes}

発売日：2020年3月4日

TiDB バージョン: 3.0.11

TiDB Ansible バージョン: 3.0.11

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかり、これらの問題は新しいバージョンで修正されています。最新の 3.0.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   最大インデックス長を制御する`max-index-length`構成項目を追加します。これは、3.0.7 より前の TiDB バージョンまたは MySQL [<a href="https://github.com/pingcap/tidb/pull/15057">#15057</a>](https://github.com/pingcap/tidb/pull/15057)の動作と互換性があります。

## 新機能 {#new-features}

-   TiDB
    -   `information_schema.PARTITIONS`テーブル[<a href="https://github.com/pingcap/tidb/pull/14849">#14849</a>](https://github.com/pingcap/tidb/pull/14849)のパーティションテーブルのメタ情報の表示をサポート

-   TiDBBinlog
    -   TiDB クラスター間の双方向データ レプリケーションをサポート[<a href="https://github.com/pingcap/tidb-binlog/pull/884">#884</a>](https://github.com/pingcap/tidb-binlog/pull/884) [<a href="https://github.com/pingcap/tidb-binlog/pull/909">#909</a>](https://github.com/pingcap/tidb-binlog/pull/909)

-   TiDB Lightning
    -   TLS 構成のサポート[<a href="https://github.com/tikv/importer/pull/44">#44</a>](https://github.com/tikv/importer/pull/44) [<a href="https://github.com/pingcap/tidb-lightning/pull/270">#270</a>](https://github.com/pingcap/tidb-lightning/pull/270)

-   TiDB Ansible
    -   制御マシンのユーザーが`ansible_user` [<a href="https://github.com/pingcap/tidb-ansible/pull/1184">#1184</a>](https://github.com/pingcap/tidb-ansible/pull/1184)と一致する必要がないように`create_users.yml`のロジックを変更します。

## バグの修正 {#bug-fixes}

-   TiDB
    -   `Union`使用するクエリは読み取り専用としてマークされないため、楽観的トランザクションを再試行するときに Goroutine リークが発生する問題を修正します[<a href="https://github.com/pingcap/tidb/pull/15076">#15076</a>](https://github.com/pingcap/tidb/pull/15076)
    -   `SET SESSION tidb_snapshot = 'xxx';`ステートメントの実行時に`tidb_snapshot`パラメータの値が正しく使用されないため、 `SHOW TABLE STATUS`スナップショット時のテーブルのステータスを正しく出力できない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/14391">#14391</a>](https://github.com/pingcap/tidb/pull/14391)
    -   `Sort Merge Join`と`ORDER BY DESC`を同時に含む SQL ステートメントによって引き起こされる誤った結果を修正します[<a href="https://github.com/pingcap/tidb/pull/14664">#14664</a>](https://github.com/pingcap/tidb/pull/14664)
    -   サポートされていない式を使用してパーティション テーブルを作成するときの TiDBサーバーのpanicを修正しました。このpanicを修正すると、エラー情報`This partition function is not allowed`が返されます。 [<a href="https://github.com/pingcap/tidb/pull/14769">#14769</a>](https://github.com/pingcap/tidb/pull/14769)
    -   `Union` [<a href="https://github.com/pingcap/tidb/pull/14944">#14944</a>](https://github.com/pingcap/tidb/pull/14944)を含むサブクエリを使用して`select max() from subquery`ステートメントを実行すると、誤った結果が発生する問題を修正しました。
    -   実行バインディング[<a href="https://github.com/pingcap/tidb/pull/14865">#14865</a>](https://github.com/pingcap/tidb/pull/14865)を削除する`DROP BINDING`を実行した後に`SHOW BINDINGS`ステートメントを実行すると、エラー メッセージが返される問題を修正します。
    -   MySQL プロトコルではクエリ内のエイリアスの最大長は 256 文字ですが、TiDB はこのプロトコルに従ってクエリ結果に[<a href="https://dev.mysql.com/doc/refman/8.0/en/identifier-length.html">エイリアスを切り取る</a>](https://dev.mysql.com/doc/refman/8.0/en/identifier-length.html)含まないため、接続が切断される問題を修正します[<a href="https://github.com/pingcap/tidb/pull/14940">#14940</a>](https://github.com/pingcap/tidb/pull/14940)
    -   `DIV`の文字列型を使用した場合に発生する可能性がある誤ったクエリ結果を修正します。たとえば、 `select 1 / '2007' div 1`ステートメント[<a href="https://github.com/pingcap/tidb/pull/14098">#14098</a>](https://github.com/pingcap/tidb/pull/14098)を正しく実行できるようになりました。

-   TiKV
    -   不要なログを削除してログ出力を最適化する[<a href="https://github.com/tikv/tikv/pull/6657">#6657</a>](https://github.com/tikv/tikv/pull/6657)
    -   高負荷時にピアが削除されたときに発生する可能性のあるpanicを修正しました[<a href="https://github.com/tikv/tikv/pull/6704">#6704</a>](https://github.com/tikv/tikv/pull/6704)
    -   場合によっては Hibernate リージョンが起動しない問題を修正[<a href="https://github.com/tikv/tikv/pull/6732">#6732</a>](https://github.com/tikv/tikv/pull/6732) [<a href="https://github.com/tikv/tikv/pull/6738">#6738</a>](https://github.com/tikv/tikv/pull/6738)

-   TiDB Ansible
    -   `tidb-ansible` [<a href="https://github.com/pingcap/tidb-ansible/pull/1169">#1169</a>](https://github.com/pingcap/tidb-ansible/pull/1169)に古いドキュメントのリンクを更新します
    -   `wait for region replication complete`タスク[<a href="https://github.com/pingcap/tidb-ansible/pull/1173">#1173</a>](https://github.com/pingcap/tidb-ansible/pull/1173)で未定義変数が発生することがある問題を修正
