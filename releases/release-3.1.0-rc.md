---
title: TiDB 3.1 RC Release Notes
---

# TiDB3.1RCリリースノート {#tidb-3-1-rc-release-notes}

発売日：2020年4月2日

TiDBバージョン：3.1.0-rc

TiDB Ansibleバージョン：3.1.0-rc

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の3.1.xバージョンを使用することをお勧めします。

## 新機能 {#new-features}

-   TiDB

    -   パフォーマンスを向上させるために、バイナリ検索を使用してパーティションプルーニングを再実装します[＃15678](https://github.com/pingcap/tidb/pull/15678)
    -   切り捨てられたテーブル[＃15460](https://github.com/pingcap/tidb/pull/15460)を回復するための`RECOVER`構文の使用をサポート
    -   ステートメントの再試行とテーブルの回復のために`AUTO_RANDOM`のIDキャッシュを追加します[＃15393](https://github.com/pingcap/tidb/pull/15393)
    -   `recover table`ステートメント`AUTO_RANDOM`を使用した1IDアロケータの状態の復元をサポートし[＃15393](https://github.com/pingcap/tidb/pull/15393) 。
    -   サポート`YEAR` 、および`MONTH`は、ハッシュパーティションテーブル[＃15619](https://github.com/pingcap/tidb/pull/15619)のパーティションキーとして関数し`TO_DAY` 。
    -   `SELECT... FOR UPDATE`ステートメントでキーをロックする必要がある場合にのみ、テーブルIDをスキーマ変更関連テーブルに追加します[＃15708](https://github.com/pingcap/tidb/pull/15708)
    -   負荷分散ポリシーに従ってさまざまな役割からデータを自動的に読み取る機能を追加し、 `leader-and-follower`のシステム変数を追加してこの機能を有効にします[＃15721](https://github.com/pingcap/tidb/pull/15721)
    -   TiDBが新しい接続を確立するたびにTLS証明書を動的に更新して、RPCクライアント側を再起動せずに期限切れのクライアント証明書を更新することをサポートします[＃15163](https://github.com/pingcap/tidb/pull/15163)
    -   TiDBが新しい接続を確立するたびに最新の証明書のロードをサポートするようにPDクライアントをアップグレードします[＃15425](https://github.com/pingcap/tidb/pull/15425)
    -   TiDBサーバーとPDサーバー間、または`cluster-ssl-*`が構成されている場合は2つのTiDBサーバー間で構成されたTLS証明書を使用してHTTPSプロトコルを強制的に使用します[＃15430](https://github.com/pingcap/tidb/pull/15430)
    -   MySQL互換の`--require-secure-transport`スタートアップオプションを追加して、構成中にクライアントにTLS認証を有効にするように強制します[＃15442](https://github.com/pingcap/tidb/pull/15442)
    -   `cluster-verify-cn`の構成アイテムを追加します。構成後、ステータスサービスは、対応するCN証明書[＃15137](https://github.com/pingcap/tidb/pull/15137)を使用している場合にのみ使用できます。

-   TiKV

    -   Raw [＃7051](https://github.com/tikv/tikv/pull/7051)を使用したデータのバックアップをサポート
    -   ステータスサーバーのTLS認証をサポートする[＃7142](https://github.com/tikv/tikv/pull/7142)
    -   KVサーバーのTLS認証をサポートする[＃7305](https://github.com/tikv/tikv/pull/7305)
    -   ロックを保持する時間を最適化して、バックアップ[＃7202](https://github.com/tikv/tikv/pull/7202)のパフォーマンスを向上させます

-   PD

    -   `shuffle-region-scheduler`を使用して学習者の[＃2235](https://github.com/pingcap/pd/pull/2235)をサポートする
    -   pd-ctlにコマンドを追加して、配置ルールを構成します[＃2306](https://github.com/pingcap/pd/pull/2306)

-   ツール

    -   TiDB Binlog

        -   コンポーネント間の[＃939](https://github.com/pingcap/tidb-binlog/pull/939)認証をサポートする[＃931](https://github.com/pingcap/tidb-binlog/pull/931) [＃937](https://github.com/pingcap/tidb-binlog/pull/937)
        -   Drainerに`kafka-client-id`の構成アイテムを追加して、Kafkaのクライアント[＃929](https://github.com/pingcap/tidb-binlog/pull/929)を構成します。

    -   TiDB Lightning

        -   TiDB Lightning [＃281](https://github.com/pingcap/tidb-lightning/pull/281) [＃275](https://github.com/pingcap/tidb-lightning/pull/275)を最適化する
        -   TiDB Lightningの[＃270](https://github.com/pingcap/tidb-lightning/pull/270)認証をサポートする

    -   バックアップと復元（BR）

        -   ログ出力を最適化する[＃189](https://github.com/pingcap/br/pull/189)

-   TiDB Ansible

    -   TiFlashデータディレクトリの作成方法を最適化する[＃1242](https://github.com/pingcap/tidb-ansible/pull/1242)
    -   TiFlash3に`Write Amplification`の監視項目を追加し[＃1234](https://github.com/pingcap/tidb-ansible/pull/1234)
    -   CPUepollexclusiveが利用できない場合に失敗したプリフライトチェックのエラーメッセージを最適化する[＃1243](https://github.com/pingcap/tidb-ansible/pull/1243)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiFlashレプリカを頻繁に更新することによって引き起こされる情報スキーマエラーを修正します[＃14884](https://github.com/pingcap/tidb/pull/14884)
    -   [＃15149](https://github.com/pingcap/tidb/pull/15149)を適用すると`last_insert_id`が誤って生成される問題を修正し`AUTO_RANDOM`
    -   TiFlashレプリカのステータスを更新すると、DDL操作がスタックする可能性がある問題を修正します[＃15161](https://github.com/pingcap/tidb/pull/15161)
    -   プッシュダウンできない述語がある場合、 `Aggregation`プッシュダウンと`TopN`プッシュダウンを禁止します[＃15141](https://github.com/pingcap/tidb/pull/15141)
    -   ネストされた`view`の作成を禁止する[＃15440](https://github.com/pingcap/tidb/pull/15440)
    -   [＃15570](https://github.com/pingcap/tidb/pull/15570)の後に`SELECT CURRENT_ROLE()`を実行したときに発生したエラーを修正し`SET ROLE ALL`
    -   `select view_name.col_name from view_name`ステートメントを実行するときに`view`の名前を識別できない問題を修正します[＃15573](https://github.com/pingcap/tidb/pull/15573)
    -   binlog情報の書き込み中にDDLステートメントを前処理するときにエラーが発生する可能性がある問題を修正します[＃15444](https://github.com/pingcap/tidb/pull/15444)
    -   `view`とパーティションテーブルの両方にアクセスするときに発生したpanicを修正します[＃15560](https://github.com/pingcap/tidb/pull/15560)
    -   `bit(n)`データ型[＃15487](https://github.com/pingcap/tidb/pull/15487)を含む`update duplicate key`ステートメントで`VALUES`関数を実行するときに発生したエラーを修正します
    -   一部のシナリオで、指定された最大実行時間が有効にならない問題を修正します[＃15616](https://github.com/pingcap/tidb/pull/15616)
    -   `Index Scan` [＃15773](https://github.com/pingcap/tidb/pull/15773)を使用して実行プランを生成するときに、現在の`ReadEngine`にTiKVサーバーが含まれているかどうかがチェックされない問題を修正します。

-   TiKV

    -   既存のキーをトランザクションに挿入し、整合性チェックパラメータを無効にしたときにすぐに削除することによって引き起こされる競合チェックの失敗またはデータインデックスの不整合の問題を修正します[＃7112](https://github.com/tikv/tikv/pull/7112)
    -   `TopN`が符号なし整数を比較するときの計算エラーを修正します[＃7199](https://github.com/tikv/tikv/pull/7199)
    -   Raftstoreにフロー制御メカニズムを導入して、フロー制御がないと、ログの追跡が遅くなり、クラスタがスタックする可能性があるという問題を解決します。トランザクションサイズが大きいと、TiKVサーバー間で頻繁に再接続される可能性があるという問題[＃7087](https://github.com/tikv/tikv/pull/7087) [＃7078](https://github.com/tikv/tikv/pull/7078)
    -   レプリカに送信される保留中の読み取り要求が永続的にブロックされる可能性がある問題を修正します[＃6543](https://github.com/tikv/tikv/pull/6543)
    -   スナップショットを適用すると、レプリカの読み取りがブロックされる可能性がある問題を修正します[＃7249](https://github.com/tikv/tikv/pull/7249)
    -   リーダーの異動によりTiKVがpanicになる可能性がある問題を修正[＃7240](https://github.com/tikv/tikv/pull/7240)
    -   データをS31にバックアップするときに、すべてのSSTファイルがゼロで埋められる問題を修正し[＃6967](https://github.com/tikv/tikv/pull/6967) 。
    -   バックアップ中にSSTファイルのサイズが記録されず、復元後に多くの空のリージョンが発生する問題を修正します[＃6983](https://github.com/tikv/tikv/pull/6983)
    -   バックアップ[＃7297](https://github.com/tikv/tikv/pull/7297)でIAMをサポートする

-   PD

    -   PDがリージョンハートビートを処理するときにデータ競合によって引き起こされる誤ったリージョン情報の問題を修正します[＃2234](https://github.com/pingcap/pd/pull/2234)
    -   `random-merge-scheduler`がロケーションラベルと配置ルールに従わないという問題を修正します[＃2212](https://github.com/pingcap/pd/pull/2221)
    -   配置ルールが同じ`startKey`と[＃2222](https://github.com/pingcap/pd/pull/2222)の別の配置ルールによって上書きされる問題を修正し`endKey`
    -   APIのバージョン番号がPDサーバー[＃2192](https://github.com/pingcap/pd/pull/2192)のバージョン番号と一致しない問題を修正します

-   ツール

    -   TiDB Lightning

        -   TiDBバックエンド[＃283](https://github.com/pingcap/tidb-lightning/pull/283)で`&`文字が`EOF`文字に置き換えられるバグを修正しました

    -   バックアップと復元（BR）

        -   BRがTiFlashクラスタデータを復元できない問題を修正する[＃194](https://github.com/pingcap/br/pull/194)
