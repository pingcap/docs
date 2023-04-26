---
title: TiDB 3.0.12 Release Notes
---

# TiDB 3.0.12 リリースノート {#tidb-3-0-12-release-notes}

発売日：2020年3月16日

TiDB バージョン: 3.0.12

TiDB アンシブル バージョン: 3.0.12

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の 3.0.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   スロー クエリ ログでbinlogの事前書き込みのタイミングが不正確になる問題を修正します。元のタイミング フィールドは`Binlog_prewrite_time`と呼ばれていました。この修正後、名前は`Wait_prewrite_binlog_time`に変更されました。 [#15276](https://github.com/pingcap/tidb/pull/15276)

## 新機能 {#new-features}

-   TiDB
    -   `alter instance`ステートメント[#15080](https://github.com/pingcap/tidb/pull/15080) [#15292](https://github.com/pingcap/tidb/pull/15292)を使用して、置き換えられた証明書ファイルの動的読み込みをサポートします。
    -   `cluster-verify-cn`構成アイテムを追加します。構成後、ステータス サービスは、対応する CN 証明書がある場合にのみ使用できます。 [#15164](https://github.com/pingcap/tidb/pull/15164)
    -   各 TiDBサーバーに DDL リクエストのフロー制限機能を追加して、DDL リクエストの競合によるエラー報告の頻度を減らします[#15148](https://github.com/pingcap/tidb/pull/15148)
    -   binlogの書き込みが失敗した場合の TiDBサーバーの終了をサポート[#15339](https://github.com/pingcap/tidb/pull/15339)

-   ツール
    -   TiDBBinlog
        -   クライアント ID [#929](https://github.com/pingcap/tidb-binlog/pull/929)を構成するために Kafka クライアントへの接続をサポートするDrainerに`kafka-client-id`構成項目を追加します。

## バグの修正 {#bug-fixes}

-   TiDB
    -   複数のユーザーを変更する際に`GRANT` 、 `REVOKE`原子性を保証するようにする[#15092](https://github.com/pingcap/tidb/pull/15092)
    -   パーティション テーブルの悲観的ロックのロックが正しい行をロックできなかった問題を修正します[#15114](https://github.com/pingcap/tidb/pull/15114)
    -   インデックス長が制限[#15130](https://github.com/pingcap/tidb/pull/15130)を超えた場合、構成の`max-index-length`の値に従ってエラー メッセージを表示するようにします。
    -   `FROM_UNIXTIME`関数[#15270](https://github.com/pingcap/tidb/pull/15270)の誤った小数点の問題を修正
    -   トランザクションで自分が書き込んだレコードを削除すると、競合の検出に失敗したり、データ インデックスの不一致が発生したりする問題を修正します[#15176](https://github.com/pingcap/tidb/pull/15176)

-   TiKV
    -   整合性チェック パラメーター[#7054](https://github.com/tikv/tikv/pull/7054)無効にするときに、既存のキーをトランザクションに挿入し、すぐに削除することによって発生する、競合検出の失敗またはデータ インデックスの不整合の問題を修正します。
    -   Raftstoreにフロー制御メカニズムを導入して、フロー制御がないと追跡が遅すぎてクラスターがスタックする可能性があり、トランザクション サイズによって TiKV 接続の頻繁な再接続が発生する可能性があるという問題を解決します[#7072](https://github.com/tikv/tikv/pull/7072) [#6993](https://github.com/tikv/tikv/pull/6993)

-   PD
    -   PD がリージョンハートビートを処理するときのデータ競合によって発生する誤ったリージョン情報の問題を修正します[#2233](https://github.com/pingcap/pd/pull/2233)

-   TiDB アンシブル
    -   クラスター内での複数の Grafana/Prometheus/Alertmanager のデプロイのサポート[#1198](https://github.com/pingcap/tidb-ansible/pull/1198)
