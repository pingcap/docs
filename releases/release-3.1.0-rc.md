---
title: TiDB 3.1 RC Release Notes
---

# TiDB 3.1 RC リリースノート {#tidb-3-1-rc-release-notes}

発売日：2020年4月2日

TiDB バージョン: 3.1.0-rc

TiDB Ansible バージョン: 3.1.0-rc

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかり、これらの問題は新しいバージョンで修正されています。最新の 3.1.x バージョンを使用することをお勧めします。

## 新機能 {#new-features}

-   TiDB

    -   バイナリ検索を使用してパーティション プルーニングを再実装し、パフォーマンスを向上させます[#15678](https://github.com/pingcap/tidb/pull/15678)
    -   `RECOVER`構文を使用した切り捨てられたテーブルの復元のサポート[#15460](https://github.com/pingcap/tidb/pull/15460)
    -   ステートメントの再試行とテーブルのリカバリのための`AUTO_RANDOM` ID キャッシュを追加します[#15393](https://github.com/pingcap/tidb/pull/15393)
    -   `recover table`ステートメントを使用した`AUTO_RANDOM` ID アロケータの状態の復元をサポート[#15393](https://github.com/pingcap/tidb/pull/15393)
    -   ハッシュパーティションテーブルの分割キーとして`YEAR` 、 `MONTH` 、および`TO_DAY`関数をサポート[#15619](https://github.com/pingcap/tidb/pull/15619)
    -   `SELECT... FOR UPDATE`ステートメントでキーをロックする必要がある場合にのみ、スキーマ変更関連テーブルにテーブル ID を追加します[#15708](https://github.com/pingcap/tidb/pull/15708)
    -   負荷分散ポリシーに従ってさまざまなロールからデータを自動的に読み取る機能を追加し、この機能を有効にする`leader-and-follower`システム変数を追加します[#15721](https://github.com/pingcap/tidb/pull/15721)
    -   TiDB が新しい接続を確立するたびに TLS 証明書を動的に更新して、RPC クライアント側を再起動せずに期限切れのクライアント証明書を更新することをサポートします[#15163](https://github.com/pingcap/tidb/pull/15163)
    -   TiDB が新しい接続を確立するたびに最新の証明書をロードできるように PD クライアントをアップグレードします[#15425](https://github.com/pingcap/tidb/pull/15425)
    -   TiDBサーバーと PDサーバー間、または`cluster-ssl-*`が構成されている場合は 2 つの TiDB サーバー間で、構成された TLS 証明書を使用して HTTPS プロトコルを強制的に使用します[#15430](https://github.com/pingcap/tidb/pull/15430)
    -   MySQL 互換`--require-secure-transport`起動オプションを追加して、構成中にクライアントに TLS 認証を強制的に有効にします[#15442](https://github.com/pingcap/tidb/pull/15442)
    -   `cluster-verify-cn`設定項目を追加します。構成後、ステータス サービスは、対応する CN 証明書[#15137](https://github.com/pingcap/tidb/pull/15137)がある場合にのみ使用できます。

-   TiKV

    -   Raw KV API [#7051](https://github.com/tikv/tikv/pull/7051)を使用したデータのバックアップのサポート
    -   ステータスサーバー[#7142](https://github.com/tikv/tikv/pull/7142)のTLS認証をサポート
    -   KVサーバーの TLS 認証のサポート[#7305](https://github.com/tikv/tikv/pull/7305)
    -   ロックを保持する時間を最適化して、バックアップ[#7202](https://github.com/tikv/tikv/pull/7202)のパフォーマンスを向上させます。

-   PD

    -   `shuffle-region-scheduler` [#2235](https://github.com/pingcap/pd/pull/2235)を使用して学習者のスケジュール設定をサポート
    -   pd-ctl にコマンドを追加して、配置ルール[#2306](https://github.com/pingcap/pd/pull/2306)を設定します。

-   ツール

    -   TiDBBinlog

        -   コンポーネント間の TLS 認証をサポート[#931](https://github.com/pingcap/tidb-binlog/pull/931) [#937](https://github.com/pingcap/tidb-binlog/pull/937) [#939](https://github.com/pingcap/tidb-binlog/pull/939)
        -   Drainerに`kafka-client-id`構成項目を追加して、Kafka のクライアント ID [#929](https://github.com/pingcap/tidb-binlog/pull/929)を構成します。

    -   TiDB Lightning

        -   TiDB Lightning [#281](https://github.com/pingcap/tidb-lightning/pull/281) [#275](https://github.com/pingcap/tidb-lightning/pull/275)のパフォーマンスを最適化する
        -   TiDB Lightning [#270](https://github.com/pingcap/tidb-lightning/pull/270)の TLS 認証をサポート

    -   バックアップと復元 (BR)

        -   ログ出力の最適化[#189](https://github.com/pingcap/br/pull/189)

-   TiDB Ansible

    -   TiFlashデータ ディレクトリの作成方法を最適化する[#1242](https://github.com/pingcap/tidb-ansible/pull/1242)
    -   TiFlash [#1234](https://github.com/pingcap/tidb-ansible/pull/1234)に監視項目を`Write Amplification`追加
    -   CPU epollexclusive が使用できない場合に失敗したプリフライト チェックのエラー メッセージを最適化します[#1243](https://github.com/pingcap/tidb-ansible/pull/1243)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiFlashレプリカ[#14884](https://github.com/pingcap/tidb/pull/14884)を頻繁に更新することによって発生する情報スキーマ エラーを修正します。
    -   `AUTO_RANDOM` [#15149](https://github.com/pingcap/tidb/pull/15149)を適用すると`last_insert_id`が誤って生成される問題を修正
    -   TiFlashレプリカのステータスを更新すると DDL 操作が停止する可能性がある問題を修正します[#15161](https://github.com/pingcap/tidb/pull/15161)
    -   プッシュダウンできない述語がある場合、 `Aggregation`プッシュダウンと`TopN`プッシュダウンを禁止します[#15141](https://github.com/pingcap/tidb/pull/15141)
    -   ネストされた`view`作成を禁止します[#15440](https://github.com/pingcap/tidb/pull/15440)
    -   `SET ROLE ALL` [#15570](https://github.com/pingcap/tidb/pull/15570)以降に`SELECT CURRENT_ROLE()`を実行するとエラーが発生する問題を修正
    -   `select view_name.col_name from view_name`ステートメントの実行時に`view`名前を識別できない問題を修正[#15573](https://github.com/pingcap/tidb/pull/15573)
    -   binlog情報[#15444](https://github.com/pingcap/tidb/pull/15444)の書き込み中に DDL ステートメントの前処理を行うときにエラーが発生することがある問題を修正します。
    -   `view`とパーティションテーブル[#15560](https://github.com/pingcap/tidb/pull/15560)の両方にアクセスするときに発生するpanicを修正しました。
    -   `bit(n)`データ型[#15487](https://github.com/pingcap/tidb/pull/15487)を含む`update duplicate key`ステートメントで`VALUES`関数を実行するときに発生したエラーを修正しました。
    -   一部のシナリオで指定した最大実行時間が有効にならない問題を修正[#15616](https://github.com/pingcap/tidb/pull/15616)
    -   `Index Scan` [#15773](https://github.com/pingcap/tidb/pull/15773)使用して実行プランを生成するときに、現在の`ReadEngine` TiKVサーバーが含まれているかどうかがチェックされない問題を修正

-   TiKV

    -   整合性チェック パラメータ[#7112](https://github.com/tikv/tikv/pull/7112)無効にすると、既存のキーをトランザクションに挿入し、すぐに削除することによって発生する競合チェックの失敗またはデータ インデックスの不整合の問題を修正しました。
    -   `TopN`符号なし整数[#7199](https://github.com/tikv/tikv/pull/7199)を比較するときの計算エラーを修正
    -   Raftstoreにフロー制御メカニズムを導入して、フロー制御がないとログ追跡が遅くなり、クラスターがスタックする可能性があるという問題を解決します。トランザクションサイズが大きいため、TiKV サーバー間の再接続が頻繁に発生する可能性があるという問題[#7087](https://github.com/tikv/tikv/pull/7087) [#7078](https://github.com/tikv/tikv/pull/7078)
    -   レプリカに送信された保留中の読み取りリクエストが永続的にブロックされる可能性がある問題を修正します[#6543](https://github.com/tikv/tikv/pull/6543)
    -   スナップショット[#7249](https://github.com/tikv/tikv/pull/7249)を適用するとレプリカの読み取りがブロックされる可能性がある問題を修正します。
    -   リーダーを移動すると TiKV がpanicになる可能性がある問題を修正[#7240](https://github.com/tikv/tikv/pull/7240)
    -   データを S3 [#6967](https://github.com/tikv/tikv/pull/6967)にバックアップするときに、すべての SST ファイルがゼロで埋められる問題を修正します。
    -   SST ファイルのサイズがバックアップ中に記録されず、復元後に多くの空のリージョンが発生する問題を修正します[#6983](https://github.com/tikv/tikv/pull/6983)
    -   バックアップ用の AWS IAM Web ID をサポート[#7297](https://github.com/tikv/tikv/pull/7297)

-   PD

    -   PD がリージョンハートビート[#2234](https://github.com/pingcap/pd/pull/2234)を処理するときに、データ競合によって引き起こされる不正確なリージョン情報の問題を修正します。
    -   `random-merge-scheduler`が場所ラベルと配置ルール[#2212](https://github.com/pingcap/pd/pull/2221)に従わない問題を修正
    -   配置ルールが同じ`startKey`と`endKey`を持つ別の配置ルールによって上書きされる問題を修正[#2222](https://github.com/pingcap/pd/pull/2222)
    -   APIのバージョン番号がPDサーバー[#2192](https://github.com/pingcap/pd/pull/2192)のバージョン番号と一致しない問題を修正

-   ツール

    -   TiDB Lightning

        -   TiDB バックエンド[#283](https://github.com/pingcap/tidb-lightning/pull/283)で`&`文字が`EOF`文字に置き換えられるバグを修正

    -   バックアップと復元 (BR)

        -   BR がTiFlashクラスター データを復元できない問題を修正[#194](https://github.com/pingcap/br/pull/194)
