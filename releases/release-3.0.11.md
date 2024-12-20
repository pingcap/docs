---
title: TiDB 3.0.11 Release Notes
summary: TiDB 3.0.11 は 2020 年 3 月 4 日にリリースされました。これには、TiDB、TiDB Binlog、 TiDB Lightning、TiKV、TiDB Ansible の互換性の変更、新機能、バグ修正、アップデートが含まれています。一部の既知の問題は新しいバージョンで修正されているため、最新の 3.0.x バージョンを使用することをお勧めします。
---

# TiDB 3.0.11 リリースノート {#tidb-3-0-11-release-notes}

発売日: 2020年3月4日

TiDB バージョン: 3.0.11

TiDB Ansible バージョン: 3.0.11

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかりましたが、これらの問題は新しいバージョンで修正されています。最新の 3.0.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   ティビ
    -   最大インデックス長を制御するための`max-index-length`設定項目を追加します。これは、TiDBバージョン3.0.7より前またはMySQL [＃15057](https://github.com/pingcap/tidb/pull/15057)の動作と互換性があります。

## 新機能 {#new-features}

-   ティビ
    -   `information_schema.PARTITIONS`テーブル[＃14849](https://github.com/pingcap/tidb/pull/14849)のパーティションテーブルのメタ情報の表示をサポート

-   TiDBBinlog
    -   TiDBクラスタ間の双方向データレプリケーションをサポート[＃884](https://github.com/pingcap/tidb-binlog/pull/884) [＃909](https://github.com/pingcap/tidb-binlog/pull/909)

-   TiDB Lightning
    -   TLS構成をサポートする[＃44](https://github.com/tikv/importer/pull/44) [＃270](https://github.com/pingcap/tidb-lightning/pull/270)

-   TiDB アンシブル
    -   `create_users.yml`のロジックを変更して、制御マシンのユーザーが`ansible_user` [＃1184](https://github.com/pingcap/tidb-ansible/pull/1184)と一貫性を保つ必要がないようにします。

## バグ修正 {#bug-fixes}

-   ティビ
    -   `Union`使用するクエリが読み取り専用としてマークされていないため、楽観的トランザクションを再試行するときに Goroutine リークが発生する問題を修正しました[＃15076](https://github.com/pingcap/tidb/pull/15076)
    -   `SET SESSION tidb_snapshot = 'xxx';`ステートメント[＃14391](https://github.com/pingcap/tidb/pull/14391)を実行するときに`tidb_snapshot`パラメータの値が正しく使用されていないため`SHOW TABLE STATUS`スナップショット時にテーブルの状態を正しく出力できない問題を修正しました。
    -   `Sort Merge Join`と`ORDER BY DESC`同時に含まれるSQL文によって発生する誤った結果を修正する[＃14664](https://github.com/pingcap/tidb/pull/14664)
    -   サポートされていない式を使用してパーティション テーブルを作成するときに TiDBサーバーのpanicを修正しました。このpanicを修正すると、エラー情報`This partition function is not allowed`が返されます[＃14769](https://github.com/pingcap/tidb/pull/14769)
    -   `Union` [＃14944](https://github.com/pingcap/tidb/pull/14944)を含むサブクエリで`select max() from subquery`ステートメントを実行したときに発生した誤った結果を修正します。
    -   実行バインディング[＃14865](https://github.com/pingcap/tidb/pull/14865)を削除する`DROP BINDING`を実行した後に`SHOW BINDINGS`ステートメントを実行するとエラー メッセージが返される問題を修正しました。
    -   MySQLプロトコルではクエリ内のエイリアスの最大長が256文字であるが、TiDBはこのプロトコル[＃14940](https://github.com/pingcap/tidb/pull/14940)に従ってクエリ結果に[別名を切る](https://dev.mysql.com/doc/refman/8.0/en/identifier-length.html)返さないため、接続が切断される問題を修正しました。
    -   `DIV`で文字列型を使用した場合に発生する可能性のある誤ったクエリ結果を修正しました。たとえば、 `select 1 / '2007' div 1`ステートメント[＃14098](https://github.com/pingcap/tidb/pull/14098)を正しく実行できるようになりました。

-   ティクヴ
    -   不要なログを削除してログ出力を最適化する[＃6657](https://github.com/tikv/tikv/pull/6657)
    -   高負荷時にピアが削除されたときに発生する可能性のあるpanicを修正[＃6704](https://github.com/tikv/tikv/pull/6704)
    -   一部のケースで休止状態領域が起動しない問題を修正[＃6732](https://github.com/tikv/tikv/pull/6732) [＃6738](https://github.com/tikv/tikv/pull/6738)

-   TiDB アンシブル
    -   `tidb-ansible` [＃1169](https://github.com/pingcap/tidb-ansible/pull/1169)の古いドキュメントリンクを更新
    -   `wait for region replication complete`タスク[＃1173](https://github.com/pingcap/tidb-ansible/pull/1173)で未定義の変数が発生する可能性がある問題を修正
