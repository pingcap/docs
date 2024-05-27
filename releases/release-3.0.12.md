---
title: TiDB 3.0.12 Release Notes
summary: TiDB 3.0.12 は、2020 年 3 月 16 日にリリースされました。これには、TiDB、TiKV、PD、TiDB Ansible の互換性の変更、新機能、バグ修正、および改善が含まれています。新しいバージョンでは既知の問題がいくつか修正されているため、最新の 3.0.x バージョンを使用することをお勧めします。新しい機能には、置き換えられた証明書ファイルの動的読み込み、DDL 要求のフロー制限、およびbinlog書き込みが失敗した場合に TiDBサーバーを終了するためのサポートが含まれます。バグ修正では、ロック、エラー メッセージの表示、小数点の精度、およびデータ インデックスの不整合に関する問題に対処しています。さらに、TiKV のフロー制御メカニズムと PD のリージョン情報処理が改善されました。
---

# TiDB 3.0.12 リリースノート {#tidb-3-0-12-release-notes}

発売日: 2020年3月16日

TiDB バージョン: 3.0.12

TiDB Ansible バージョン: 3.0.12

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかりましたが、これらの問題は新しいバージョンで修正されています。最新の 3.0.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   ティビ
    -   スロークエリログの事前書き込みbinlogのタイミングが不正確になる問題を修正しました。元のタイミングフィールドは`Binlog_prewrite_time`と呼ばれていました。この修正後、名前は`Wait_prewrite_binlog_time`に変更されました[＃15276](https://github.com/pingcap/tidb/pull/15276)

## 新機能 {#new-features}

-   ティビ
    -   `alter instance`ステートメント[＃15080](https://github.com/pingcap/tidb/pull/15080) [＃15292](https://github.com/pingcap/tidb/pull/15292)を使用して、置き換えられた証明書ファイルの動的読み込みをサポートします。
    -   `cluster-verify-cn`設定項目を追加します。設定後、ステータス サービスは対応する CN 証明書がある場合にのみ使用できます[＃15164](https://github.com/pingcap/tidb/pull/15164)
    -   各 TiDBサーバーの DDL 要求のフロー制限機能を追加して、DDL 要求の競合のエラー報告頻度を減らします[＃15148](https://github.com/pingcap/tidb/pull/15148)
    -   binlog書き込みが失敗した場合に TiDBサーバーの終了をサポートする[＃15339](https://github.com/pingcap/tidb/pull/15339)

-   ツール
    -   TiDBBinlog
        -   Drainerに`kafka-client-id`設定項目を追加します。これは、Kafkaクライアントへの接続をサポートし、クライアントID [＃929](https://github.com/pingcap/tidb-binlog/pull/929)を設定します。

## バグの修正 {#bug-fixes}

-   ティビ
    -   `GRANT`複数のユーザーを変更するときにアトミック`REVOKE`を保証する[＃15092](https://github.com/pingcap/tidb/pull/15092)
    -   パーティションテーブル上の悲観的ロックのロックが正しい行[＃15114](https://github.com/pingcap/tidb/pull/15114)をロックできなかった問題を修正しました。
    -   インデックスの長さが制限[＃15130](https://github.com/pingcap/tidb/pull/15130)を超えた場合に、構成の値`max-index-length`に従ってエラー メッセージを表示するようにします。
    -   `FROM_UNIXTIME`関数[＃15270](https://github.com/pingcap/tidb/pull/15270)の小数点の誤りを修正
    -   トランザクション[＃15176](https://github.com/pingcap/tidb/pull/15176)で自分自身が書き込んだレコードを削除することによって発生する競合検出の失敗またはデータ インデックスの不整合の問題を修正しました。

-   ティクヴ
    -   整合性チェックパラメータ[＃7054](https://github.com/tikv/tikv/pull/7054)を無効にすると、既存のキーをトランザクションに挿入してすぐに削除することによって発生する競合検出の失敗またはデータ インデックスの不整合の問題を修正しました。
    -   Raftstoreにフロー制御メカニズムを導入して、フロー制御がないと追跡が遅くなりすぎてクラスターがスタックしたり、トランザクション サイズによって TiKV 接続が頻繁に再接続されたりする可能性がある問題を解決します[＃7072](https://github.com/tikv/tikv/pull/7072) [＃6993](https://github.com/tikv/tikv/pull/6993)

-   PD
    -   PD がリージョンハートビート[＃2233](https://github.com/pingcap/pd/pull/2233)を処理するときにデータ競合によって発生するリージョン情報の誤りの問題を修正しました。

-   TiDB アンシブル
    -   クラスター[＃1198](https://github.com/pingcap/tidb-ansible/pull/1198)内で複数の Grafana/Prometheus/Alertmanager のデプロイをサポート
