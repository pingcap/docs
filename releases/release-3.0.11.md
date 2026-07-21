---
title: TiDB 3.0.11 Release Notes
summary: TiDB 3.0.11は2020年3月4日にリリースされました。TiDB、TiDB Binlog、 TiDB Lightning、TiKV、TiDB Ansibleの互換性変更、新機能、バグ修正、アップデートが含まれています。一部の既知の問題は新しいバージョンで修正されているため、最新の3.0.xバージョンをご利用いただくことをお勧めします。
---

# TiDB 3.0.11 リリースノート {#tidb-3-0-11-release-notes}

発売日：2020年3月4日

TiDB バージョン: 3.0.11

TiDB Ansible バージョン: 3.0.11

> **Warning:**
>
> このバージョンにはいくつかの既知の問題が見つかりましたが、これらの問題は新しいバージョンで修正されています。最新の3.0.xバージョンをご利用いただくことをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   最大インデックス長を制御するための`max-index-length`設定項目を追加します。これは、TiDB バージョン 3.0.7 以前または MySQL の動作と互換性があります。 [＃15057](https://github.com/pingcap/tidb/pull/15057)

## 新機能 {#new-features}

-   TiDB
    -   `information_schema.PARTITIONS`テーブルのパーティションテーブルのメタ情報の表示をサポート [＃14849](https://github.com/pingcap/tidb/pull/14849)

-   TiDB Binlog
    -   TiDBクラスタ間の双方向データレプリケーションをサポート[＃884](https://github.com/pingcap/tidb-binlog/pull/884) [＃909](https://github.com/pingcap/tidb-binlog/pull/909)

-   TiDB Lightning
    -   TLS構成 をサポートする [＃270](https://github.com/pingcap/tidb-lightning/pull/270) [＃44](https://github.com/tikv/importer/pull/44)

-   TiDB Ansible
    -   `create_users.yml`のロジックを変更して、制御マシンのユーザーが`ansible_user` と一貫性を保つ必要がないようにします。 [＃1184](https://github.com/pingcap/tidb-ansible/pull/1184)

## バグ修正 {#bug-fixes}

-   TiDB
    -   `Union`使用するクエリが読み取り専用としてマークされていないため、楽観的トランザクションを再試行するときに Goroutine リークが発生する問題を修正しました[＃15076](https://github.com/pingcap/tidb/pull/15076)
    -   `SET SESSION tidb_snapshot = 'xxx';`ステートメント実行時に`tidb_snapshot`パラメータの値が正しく使用されていないため、スナップショット時に`SHOW TABLE STATUS`でテーブルの状態を正しく出力できない問題を修正しました [＃14391](https://github.com/pingcap/tidb/pull/14391)
    -   `Sort Merge Join`と`ORDER BY DESC`同時に含まれるSQL文によって発生する誤った結果を修正する[＃14664](https://github.com/pingcap/tidb/pull/14664)
    -   サポートされていない式を使用してパーティションテーブルを作成する際にTiDBサーバーがpanicを修正しました。このpanicを修正すると、エラー情報`This partition function is not allowed`返されます[＃14769](https://github.com/pingcap/tidb/pull/14769)
    -   `Union` を含むサブクエリで`select max() from subquery`文を実行したときに発生した誤った結果を修正しました [＃14944](https://github.com/pingcap/tidb/pull/14944)
    -   実行バインディングを削除する`DROP BINDING`を実行した後に`SHOW BINDINGS`ステートメントを実行するとエラーメッセージが返される問題を修正しました [＃14865](https://github.com/pingcap/tidb/pull/14865)
    -   MySQLプロトコルではクエリのエイリアスの最大長が256文字であるにもかかわらず、TiDBがこのプロトコルに従ってクエリ結果の[エイリアスを切り詰め](https://dev.mysql.com/doc/refman/8.0/en/identifier-length.html)ないため、接続が切断される問題を修正しました。 [＃14940](https://github.com/pingcap/tidb/pull/14940)
    -   `DIV`で文字列型を使用した際に発生する可能性のある誤ったクエリ結果を修正しました。例えば、 `select 1 / '2007' div 1`文正しく実行できるようになりました。 [＃14098](https://github.com/pingcap/tidb/pull/14098)

-   TiKV
    -   不要なログを削除してログ出力を最適化する[＃6657](https://github.com/tikv/tikv/pull/6657)
    -   高負荷時にピアが削除されたときに発生する可能性のあるpanicを修正[＃6704](https://github.com/tikv/tikv/pull/6704)
    -   一部のケースで休止状態領域が起動しない問題を修正[＃6732](https://github.com/tikv/tikv/pull/6732) [＃6738](https://github.com/tikv/tikv/pull/6738)

-   TiDB Ansible
    -   `tidb-ansible` の古いドキュメントリンクを更新 [＃1169](https://github.com/pingcap/tidb-ansible/pull/1169)
    -   `wait for region replication complete`タスクで未定義の変数が発生する可能性がある問題を修正しました [＃1173](https://github.com/pingcap/tidb-ansible/pull/1173)
