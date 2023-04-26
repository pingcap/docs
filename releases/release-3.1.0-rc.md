---
title: TiDB 3.1 RC Release Notes
---

# TiDB 3.1 RC リリースノート {#tidb-3-1-rc-release-notes}

発売日：2020年4月2日

TiDB バージョン: 3.1.0-rc

TiDB アンシブル バージョン: 3.1.0-rc

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の 3.1.x バージョンを使用することをお勧めします。

## 新機能 {#new-features}

-   TiDB

    -   二分探索を使用して、パフォーマンスを向上させるためにパーティションのプルーニングを再実装します[#15678](https://github.com/pingcap/tidb/pull/15678)
    -   切り捨てられたテーブルを復元するための`RECOVER`構文の使用のサポート[#15460](https://github.com/pingcap/tidb/pull/15460)
    -   ステートメントの再試行とテーブルのリカバリのために`AUTO_RANDOM` ID キャッシュを追加します[#15393](https://github.com/pingcap/tidb/pull/15393)
    -   `recover table`ステートメント[#15393](https://github.com/pingcap/tidb/pull/15393)を使用した`AUTO_RANDOM` ID アロケーターの状態の復元をサポート
    -   サポート`YEAR` `MONTH`および`TO_DAY`ハッシュパーティションテーブル[#15619](https://github.com/pingcap/tidb/pull/15619)の分割キーとして関数。
    -   `SELECT... FOR UPDATE`ステートメントでキーをロックする必要がある場合にのみ、スキーマ変更関連のテーブルにテーブル ID を追加します[#15708](https://github.com/pingcap/tidb/pull/15708)
    -   負荷分散ポリシーに従って異なるロールからデータを自動的に読み取る機能を追加し、この機能を有効にする`leader-and-follower`システム変数を追加します[#15721](https://github.com/pingcap/tidb/pull/15721)
    -   RPC クライアント側を再起動せずに期限切れのクライアント証明書を更新するために TiDB が新しい接続を確立するたびに TLS 証明書を動的に更新するサポート[#15163](https://github.com/pingcap/tidb/pull/15163)
    -   PD クライアントをアップグレードして、TiDB が新しい接続を確立するたびに最新の証明書のロードをサポートするようにします[#15425](https://github.com/pingcap/tidb/pull/15425)
    -   TiDBサーバーと PDサーバー間、または`cluster-ssl-*`が構成されている場合は 2 つの TiDB サーバー間で、構成済みの TLS 証明書を使用して HTTPS プロトコルを強制的に使用します[#15430](https://github.com/pingcap/tidb/pull/15430)
    -   MySQL 互換`--require-secure-transport`起動オプションを追加して、構成中にクライアントに TLS 認証を強制的に有効にします[#15442](https://github.com/pingcap/tidb/pull/15442)
    -   `cluster-verify-cn`構成アイテムを追加します。構成後、ステータス サービスは、対応する CN 証明書[#15137](https://github.com/pingcap/tidb/pull/15137)がある場合にのみ使用できます。

-   TiKV

    -   Raw KV API [#7051](https://github.com/tikv/tikv/pull/7051)を使用したデータのバックアップのサポート
    -   ステータスサーバー[#7142](https://github.com/tikv/tikv/pull/7142)のTLS認証をサポート
    -   KVサーバー[#7305](https://github.com/tikv/tikv/pull/7305)の TLS 認証をサポート
    -   バックアップ[#7202](https://github.com/tikv/tikv/pull/7202)のパフォーマンスを向上させるためにロックを保持する時間を最適化する

-   PD

    -   `shuffle-region-scheduler` [#2235](https://github.com/pingcap/pd/pull/2235)を使用して学習者のスケジューリングをサポート
    -   pd-ctl にコマンドを追加して、配置ルール[#2306](https://github.com/pingcap/pd/pull/2306)を構成します

-   ツール

    -   TiDBBinlog

        -   コンポーネント間の TLS 認証をサポートする[#931](https://github.com/pingcap/tidb-binlog/pull/931) [#937](https://github.com/pingcap/tidb-binlog/pull/937) [#939](https://github.com/pingcap/tidb-binlog/pull/939)
        -   Drainerに`kafka-client-id`構成項目を追加して、Kafka のクライアント ID [#929](https://github.com/pingcap/tidb-binlog/pull/929)を構成します。

    -   TiDB Lightning

        -   TiDB Lightning [#281](https://github.com/pingcap/tidb-lightning/pull/281) [#275](https://github.com/pingcap/tidb-lightning/pull/275)のパフォーマンスを最適化する
        -   TiDB Lightning [#270](https://github.com/pingcap/tidb-lightning/pull/270)の TLS 認証をサポート

    -   バックアップと復元 (BR)

        -   ログ出力の最適化[#189](https://github.com/pingcap/br/pull/189)

-   TiDB アンシブル

    -   TiFlashデータ ディレクトリの作成方法を最適化する[#1242](https://github.com/pingcap/tidb-ansible/pull/1242)
    -   TiFlash [#1234](https://github.com/pingcap/tidb-ansible/pull/1234)に監視項目を`Write Amplification`追加
    -   CPU epollexclusive が使用できない場合に失敗したプリフライト チェックのエラー メッセージを最適化します[#1243](https://github.com/pingcap/tidb-ansible/pull/1243)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiFlashレプリカ[#14884](https://github.com/pingcap/tidb/pull/14884)を頻繁に更新することによって発生する情報スキーマ エラーを修正します。
    -   `AUTO_RANDOM` [#15149](https://github.com/pingcap/tidb/pull/15149)適用時に`last_insert_id`が誤って生成される問題を修正
    -   TiFlashレプリカのステータスを更新すると、DDL 操作が停止する可能性がある問題を修正します[#15161](https://github.com/pingcap/tidb/pull/15161)
    -   [#15141](https://github.com/pingcap/tidb/pull/15141)ダウンできない述語がある場合、 `Aggregation`プッシュダウンと`TopN`プッシュダウンを禁止する
    -   ネストされた`view`作成を禁止する[#15440](https://github.com/pingcap/tidb/pull/15440)
    -   `SET ROLE ALL` [#15570](https://github.com/pingcap/tidb/pull/15570)の後に`SELECT CURRENT_ROLE()`実行するとエラーが発生するのを修正
    -   `select view_name.col_name from view_name`ステートメント[#15573](https://github.com/pingcap/tidb/pull/15573)の実行時に`view`名の識別に失敗する問題を修正
    -   binlog情報の書き込み時にDDL文を前処理するとエラーが発生することがある問題を修正[#15444](https://github.com/pingcap/tidb/pull/15444)
    -   `view`とパーティション化されたテーブルの両方にアクセスするとpanicを修正しました[#15560](https://github.com/pingcap/tidb/pull/15560)
    -   `bit(n)`データ型[#15487](https://github.com/pingcap/tidb/pull/15487)を含む`update duplicate key`ステートメントで`VALUES`関数を実行したときに発生したエラーを修正します。
    -   一部のシナリオで指定された最大実行時間が有効にならない問題を修正します[#15616](https://github.com/pingcap/tidb/pull/15616)
    -   `Index Scan` [#15773](https://github.com/pingcap/tidb/pull/15773)使用して実行計画を生成するときに、現在の`ReadEngine` TiKVサーバーが含まれているかどうかがチェックされない問題を修正します。

-   TiKV

    -   整合性チェック パラメーター[#7112](https://github.com/tikv/tikv/pull/7112)無効にするときに、既存のキーをトランザクションに挿入し、すぐに削除することによって発生する、競合チェックの失敗またはデータ インデックスの不整合の問題を修正します。
    -   `TopN`符号なし整数を比較するときの計算エラーを修正します[#7199](https://github.com/tikv/tikv/pull/7199)
    -   Raftstoreにフロー制御メカニズムを導入して、フロー制御がないとログの追跡が遅くなり、クラスターがスタックする可能性があるという問題を解決します。トランザクションサイズが大きいと、TiKV サーバー間の再接続が頻繁に発生する可能性があるという問題[#7087](https://github.com/tikv/tikv/pull/7087) [#7078](https://github.com/tikv/tikv/pull/7078)
    -   レプリカに送信された保留中の読み取り要求が永久にブロックされる可能性がある問題を修正します[#6543](https://github.com/tikv/tikv/pull/6543)
    -   スナップショットを適用するとレプリカの読み取りがブロックされる可能性がある問題を修正します[#7249](https://github.com/tikv/tikv/pull/7249)
    -   リーダーを転送すると TiKV がpanicになる可能性がある問題を修正します[#7240](https://github.com/tikv/tikv/pull/7240)
    -   データを S3 にバックアップするときに、すべての SST ファイルがゼロで埋められる問題を修正します[#6967](https://github.com/tikv/tikv/pull/6967)
    -   バックアップ中に SST ファイルのサイズが記録されず、復元後に空のリージョンが多数発生する問題を修正します[#6983](https://github.com/tikv/tikv/pull/6983)
    -   バックアップ用の AWS IAM Web ID をサポート[#7297](https://github.com/tikv/tikv/pull/7297)

-   PD

    -   PD がリージョンハートビートを処理するときのデータ競合によって発生する誤ったリージョン情報の問題を修正します[#2234](https://github.com/pingcap/pd/pull/2234)
    -   `random-merge-scheduler`場所のラベルと配置ルールに従わない問題を修正[#2212](https://github.com/pingcap/pd/pull/2221)
    -   配置ルールが同じ`startKey`と`endKey` [#2222](https://github.com/pingcap/pd/pull/2222)を持つ別の配置ルールによって上書きされる問題を修正します
    -   API のバージョン番号が PDサーバー[#2192](https://github.com/pingcap/pd/pull/2192)のバージョン番号と一致しない問題を修正

-   ツール

    -   TiDB Lightning

        -   TiDB バックエンド[#283](https://github.com/pingcap/tidb-lightning/pull/283)で`&`文字が`EOF`文字に置き換わるバグを修正

    -   バックアップと復元 (BR)

        -   BR がTiFlashクラスタ データを復元できない問題を修正します[#194](https://github.com/pingcap/br/pull/194)
