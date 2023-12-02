---
title: TiDB 3.0.12 Release Notes
---

# TiDB 3.0.12 リリースノート {#tidb-3-0-12-release-notes}

発売日：2020年3月16日

TiDB バージョン: 3.0.12

TiDB Ansible バージョン: 3.0.12

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかり、これらの問題は新しいバージョンで修正されています。最新の 3.0.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   低速クエリ ログにおける事前書き込みbinlogのタイミングが不正確である問題を修正します。元のタイミング フィールドは`Binlog_prewrite_time`と呼ばれていました。この修正後、名前は`Wait_prewrite_binlog_time`に変更されます。 [#15276](https://github.com/pingcap/tidb/pull/15276)

## 新機能 {#new-features}

-   TiDB
    -   `alter instance`ステートメントを使用して、置き換えられた証明書ファイルの動的ロードをサポートします[#15080](https://github.com/pingcap/tidb/pull/15080) [#15292](https://github.com/pingcap/tidb/pull/15292)
    -   `cluster-verify-cn`設定項目を追加します。構成後、ステータス サービスは、対応する CN 証明書がある場合にのみ使用できます。 [#15164](https://github.com/pingcap/tidb/pull/15164)
    -   各 TiDBサーバーに DDL リクエストのフロー制限機能を追加して、DDL リクエストの競合によるエラー報告の頻度を減らします[#15148](https://github.com/pingcap/tidb/pull/15148)
    -   binlogの書き込みが失敗した場合の TiDBサーバーの終了をサポート[#15339](https://github.com/pingcap/tidb/pull/15339)

-   ツール
    -   TiDBBinlog
        -   Drainerに`kafka-client-id`構成項目を追加します。これは、クライアント ID [#929](https://github.com/pingcap/tidb-binlog/pull/929)を構成するための Kafka クライアントへの接続をサポートします。

## バグの修正 {#bug-fixes}

-   TiDB
    -   複数のユーザーを変更するときに`GRANT` 、 `REVOKE`でアトミック性を保証する[#15092](https://github.com/pingcap/tidb/pull/15092)
    -   パーティションテーブルの悲観的ロックのロックで正しい行[#15114](https://github.com/pingcap/tidb/pull/15114)のロックに失敗する問題を修正
    -   インデックスの長さが制限[#15130](https://github.com/pingcap/tidb/pull/15130)を超えた場合、設定の値`max-index-length`に従ってエラー メッセージが表示されるようにします。
    -   `FROM_UNIXTIME`関数[#15270](https://github.com/pingcap/tidb/pull/15270)の小数点が正しくない問題を修正しました。
    -   トランザクションで自分が書き込んだレコードを削除することによって発生する競合検出の失敗またはデータ インデックスの不一致の問題を修正します[#15176](https://github.com/pingcap/tidb/pull/15176)

-   TiKV
    -   整合性チェック パラメータ[#7054](https://github.com/tikv/tikv/pull/7054)を無効にすると、既存のキーをトランザクションに挿入し、すぐに削除することによって発生する競合検出エラーまたはデータ インデックスの不整合の問題を修正しました。
    -   Raftstoreにフロー制御メカニズムを導入して、フロー制御がないとトラッキングが遅すぎてクラスターがスタックする可能性があり、トランザクション サイズによって TiKV 接続が頻繁に再接続される可能性があるという問題を解決します[#7072](https://github.com/tikv/tikv/pull/7072) [#6993](https://github.com/tikv/tikv/pull/6993)

-   PD
    -   PD がリージョンハートビート[#2233](https://github.com/pingcap/pd/pull/2233)を処理するときに、データ競合によって引き起こされる不正確なリージョン情報の問題を修正します。

-   TiDB Ansible
    -   クラスター内での複数の Grafana/Prometheus/Alertmanager のデプロイのサポート[#1198](https://github.com/pingcap/tidb-ansible/pull/1198)
