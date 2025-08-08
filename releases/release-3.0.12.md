---
title: TiDB 3.0.12 Release Notes
summary: TiDB 3.0.12は2020年3月16日にリリースされました。TiDB、TiKV、PD、TiDB Ansibleの互換性変更、新機能、バグ修正、および機能改善が含まれています。新しいバージョンでは一部の既知の問題が修正されているため、最新の3.0.xバージョンを使用することをお勧めします。新機能には、置換された証明書ファイルの動的ロード、DDLリクエストのフロー制限、およびbinlog書き込み失敗時のTiDBサーバーの終了のサポートが含まれます。バグ修正では、ロック、エラーメッセージの表示、小数点の精度、およびデータインデックスの不整合に関する問題が修正されています。さらに、TiKVのフロー制御メカニズムとPDのリージョン情報処理にも改善が加えられています。
---

# TiDB 3.0.12 リリースノート {#tidb-3-0-12-release-notes}

発売日：2020年3月16日

TiDB バージョン: 3.0.12

TiDB Ansible バージョン: 3.0.12

> **警告：**
>
> このバージョンにはいくつかの既知の問題が見つかりましたが、これらの問題は新しいバージョンで修正されています。最新の3.0.xバージョンをご利用いただくことをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   スロークエリログにおける事前書き込みbinlogのタイミングが不正確になる問題を修正しました。以前のタイミングフィールドは`Binlog_prewrite_time`でした。この修正後、名前は`Wait_prewrite_binlog_time`に変更されます。 [＃15276](https://github.com/pingcap/tidb/pull/15276)

## 新機能 {#new-features}

-   TiDB
    -   `alter instance`文[＃15080](https://github.com/pingcap/tidb/pull/15080) [＃15292](https://github.com/pingcap/tidb/pull/15292)を使用して、置き換えられた証明書ファイルの動的読み込みをサポートします。
    -   `cluster-verify-cn`設定項目を追加します。設定後、ステータスサービスは対応するCN証明書がある場合にのみ使用できます[＃15164](https://github.com/pingcap/tidb/pull/15164)
    -   各 TiDBサーバーの DDL リクエストのフロー制限機能を追加して、DDL リクエストの競合のエラー報告頻度を削減します[＃15148](https://github.com/pingcap/tidb/pull/15148)
    -   binlogの書き込みが失敗した場合に TiDBサーバーの終了をサポートする[＃15339](https://github.com/pingcap/tidb/pull/15339)

-   ツール
    -   TiDBBinlog
        -   Drainerに`kafka-client-id`設定項目を追加します。これは、クライアント ID [＃929](https://github.com/pingcap/tidb-binlog/pull/929)を設定するために Kafka クライアントへの接続をサポートします。

## バグ修正 {#bug-fixes}

-   TiDB
    -   `GRANT`複数のユーザー`REVOKE`変更するときに原子性を保証する[＃15092](https://github.com/pingcap/tidb/pull/15092)
    -   パーティションテーブルに対する悲観的ロックのロックが正しい行[＃15114](https://github.com/pingcap/tidb/pull/15114)ロックできなかった問題を修正しました
    -   インデックスの長さが制限[＃15130](https://github.com/pingcap/tidb/pull/15130)超えたときに、構成の値`max-index-length`に応じてエラーメッセージを表示するようにします。
    -   `FROM_UNIXTIME`関数[＃15270](https://github.com/pingcap/tidb/pull/15270)の小数点の誤りの問題を修正
    -   トランザクション[＃15176](https://github.com/pingcap/tidb/pull/15176)で自分自身が書き込んだレコードを削除することで発生する競合検出の失敗やデータインデックスの不整合の問題を修正

-   TiKV
    -   整合性チェックパラメータ[＃7054](https://github.com/tikv/tikv/pull/7054)を無効にしたときに、既存のキーをトランザクションに挿入してすぐに削除すると競合検出が失敗したり、データ インデックスの不整合が発生したりする問題を修正しました。
    -   Raftstoreにフロー制御メカニズムを導入して、フロー制御がないと追跡が遅くなりすぎてクラスターがスタックする可能性があり、トランザクションのサイズによって TiKV 接続が頻繁に再接続される可能性があるという問題を解決します[＃7072](https://github.com/tikv/tikv/pull/7072) [＃6993](https://github.com/tikv/tikv/pull/6993)

-   PD
    -   PD がリージョンハートビート[＃2233](https://github.com/pingcap/pd/pull/2233)処理するときにデータ競合によって発生するリージョン情報の誤りの問題を修正しました。

-   TiDB アンシブル
    -   クラスター[＃1198](https://github.com/pingcap/tidb-ansible/pull/1198)内で複数の Grafana/Prometheus/Alertmanager のデプロイをサポート
