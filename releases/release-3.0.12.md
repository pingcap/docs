---
title: TiDB 3.0.12 Release Notes
---

# TiDB3.0.12リリースノート {#tidb-3-0-12-release-notes}

発売日：2020年3月16日

TiDBバージョン：3.0.12

TiDB Ansibleバージョン：3.0.12

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の3.0.xバージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   遅いクエリログでの事前書き込みbinlogの不正確なタイミングの問題を修正します。元のタイミングフィールドは`Binlog_prewrite_time`と呼ばれていました。この修正後、名前は`Wait_prewrite_binlog_time`に変更されます。 [＃15276](https://github.com/pingcap/tidb/pull/15276)

## 新機能 {#new-features}

-   TiDB
    -   `alter instance`ステートメント[＃15292](https://github.com/pingcap/tidb/pull/15292)を使用して、置き換えられた証明書ファイルの動的ロードをサポートし[＃15080](https://github.com/pingcap/tidb/pull/15080) 。
    -   `cluster-verify-cn`の構成アイテムを追加します。構成後、ステータスサービスは、対応するCN証明書がある場合にのみ使用できます。 [＃15164](https://github.com/pingcap/tidb/pull/15164)
    -   各TiDBサーバーにDDL要求のフロー制限機能を追加して、DDL要求の競合のエラー報告頻度を減らします[＃15148](https://github.com/pingcap/tidb/pull/15148)
    -   binlog書き込みが失敗した場合のTiDBサーバーの終了をサポート[＃15339](https://github.com/pingcap/tidb/pull/15339)

-   ツール
    -   TiDB Binlog
        -   Drainerに`kafka-client-id`の構成アイテムを追加します。これは、Kafkaクライアントへの接続をサポートしてクライアント[＃929](https://github.com/pingcap/tidb-binlog/pull/929)を構成します。

## バグの修正 {#bug-fixes}

-   TiDB
    -   複数のユーザーを変更するときに`GRANT`が[＃15092](https://github.com/pingcap/tidb/pull/15092)性を保証するようにする`REVOKE`
    -   パーティションテーブルでのペシミスティックロックのロックが正しい行[＃15114](https://github.com/pingcap/tidb/pull/15114)のロックに失敗した問題を修正します。
    -   インデックスの長さが制限[＃15130](https://github.com/pingcap/tidb/pull/15130)を超えた場合、構成の値`max-index-length`に従ってエラーメッセージを表示します。
    -   `FROM_UNIXTIME`関数[＃15270](https://github.com/pingcap/tidb/pull/15270)の誤った小数点の問題を修正します
    -   トランザクション[＃15176](https://github.com/pingcap/tidb/pull/15176)で自分で書き込んだレコードを削除することによって引き起こされる競合検出の失敗またはデータインデックスの不整合の問題を修正します

-   TiKV
    -   既存のキーをトランザクションに挿入し、整合性チェックパラメータを無効にしたときにすぐに削除することによって引き起こされる競合検出の失敗またはデータインデックスの不整合の問題を修正します[＃7054](https://github.com/tikv/tikv/pull/7054)
    -   Raftstoreにフロー制御メカニズムを導入して、フロー制御がないと追跡が遅くなり、クラスタがスタックし、トランザクションサイズによってTiKV接続が頻繁に再接続される可能性があるという問題を解決します[＃7072](https://github.com/tikv/tikv/pull/7072) [＃6993](https://github.com/tikv/tikv/pull/6993)

-   PD
    -   PDがリージョンハートビートを処理するときにデータ競合が原因で発生するリージョン情報が正しくない問題を修正します[＃2233](https://github.com/pingcap/pd/pull/2233)

-   TiDB Ansible
    -   クラスタでの複数のGrafana/Prometheus/Alertmanagerのデプロイをサポート[#1198](https://github.com/pingcap/tidb-ansible/pull/1198)
