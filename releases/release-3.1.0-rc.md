---
title: TiDB 3.1 RC Release Notes
summary: TiDB 3.1 RC は 2020 年 4 月 2 日にリリースされました。パーティション プルーニングの改善、`RECOVER` 構文のサポート、TLS 証明書の更新などの新機能が含まれています。バグ修正には、 TiFlashレプリカ、`last_insert_id`、`集計` プッシュダウンに関する問題の解決が含まれます。TiKV は、バックアップ用に TLS 認証と AWS IAM Web ID をサポートするようになりました。PD では、データ競合の問題と配置ルールの不整合が修正されました。TiDB TiDB LightningやBRなどのツールも最適化され、修正されました。
---

# TiDB 3.1 RC リリースノート {#tidb-3-1-rc-release-notes}

発売日: 2020年4月2日

TiDB バージョン: 3.1.0-rc

TiDB Ansible バージョン: 3.1.0-rc

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかりましたが、これらの問題は新しいバージョンで修正されています。最新の 3.1.x バージョンを使用することをお勧めします。

## 新機能 {#new-features}

-   ティビ

    -   バイナリ検索を使用してパーティションプルーニングを再実装し、パフォーマンスを向上する[＃15678](https://github.com/pingcap/tidb/pull/15678)
    -   切り捨てられたテーブル[＃15460](https://github.com/pingcap/tidb/pull/15460)を回復するために`RECOVER`構文の使用をサポートします
    -   ステートメントの再試行とテーブルの回復のための`AUTO_RANDOM` ID キャッシュを追加します[＃15393](https://github.com/pingcap/tidb/pull/15393)
    -   `recover table`ステートメント[＃15393](https://github.com/pingcap/tidb/pull/15393)を使用して`AUTO_RANDOM` ID アロケータの状態を復元するサポート
    -   ハッシュパーティションテーブル[＃15619](https://github.com/pingcap/tidb/pull/15619)のパーティションキーとして`YEAR` `MONTH`関数を`TO_DAY`する
    -   `SELECT... FOR UPDATE`ステートメント[＃15708](https://github.com/pingcap/tidb/pull/15708)でキーをロックする必要がある場合にのみ、スキーマ変更関連テーブルにテーブル ID を追加します。
    -   負荷分散ポリシーに従って異なるロールからデータを自動的に読み取る機能を追加し、この機能を有効にするために`leader-and-follower`システム変数を追加します[＃15721](https://github.com/pingcap/tidb/pull/15721)
    -   TiDB が新しい接続を確立するたびに TLS 証明書を動的に更新し、RPC クライアント側を再起動せずに期限切れのクライアント証明書を更新できるようにします[＃15163](https://github.com/pingcap/tidb/pull/15163)
    -   TiDB が新しい接続を確立するたびに最新の証明書をロードできるように PD クライアントをアップグレードする[＃15425](https://github.com/pingcap/tidb/pull/15425)
    -   `cluster-ssl-*`設定されている場合は TiDBサーバーと PDサーバー間、または 2 つの TiDB サーバー間で、設定された TLS 証明書を使用して HTTPS プロトコルを強制的に使用します[＃15430](https://github.com/pingcap/tidb/pull/15430)
    -   MySQL互換の`--require-secure-transport`起動オプションを追加して、構成中にクライアントにTLS認証を強制的に有効にする[＃15442](https://github.com/pingcap/tidb/pull/15442)
    -   `cluster-verify-cn`設定項目を追加します。設定後、ステータスサービスは対応するCN証明書[＃15137](https://github.com/pingcap/tidb/pull/15137)がある場合にのみ使用できます。

-   ティクヴ

    -   Raw KV API [＃7051](https://github.com/tikv/tikv/pull/7051)によるデータのバックアップをサポート
    -   ステータスサーバー[＃7142](https://github.com/tikv/tikv/pull/7142)のTLS認証をサポート
    -   KVサーバー[＃7305](https://github.com/tikv/tikv/pull/7305)のTLS認証をサポート
    -   ロックを保持する時間を最適化してバックアップ[＃7202](https://github.com/tikv/tikv/pull/7202)のパフォーマンスを向上させる

-   PD

    -   `shuffle-region-scheduler` [＃2235](https://github.com/pingcap/pd/pull/2235)を使用して学習者のスケジュール管理をサポート
    -   配置ルール[＃2306](https://github.com/pingcap/pd/pull/2306)を設定するためのコマンドを pd-ctl に追加します。

-   ツール

    -   TiDBBinlog

        -   コンポーネント間のTLS認証をサポート[＃931](https://github.com/pingcap/tidb-binlog/pull/931) [＃937](https://github.com/pingcap/tidb-binlog/pull/937) [＃939](https://github.com/pingcap/tidb-binlog/pull/939)
        -   Drainerに`kafka-client-id`設定項目を追加して、KafkaのクライアントID [＃929](https://github.com/pingcap/tidb-binlog/pull/929)を設定します。

    -   TiDB Lightning

        -   TiDB Lightning [＃281](https://github.com/pingcap/tidb-lightning/pull/281) [＃275](https://github.com/pingcap/tidb-lightning/pull/275)のパフォーマンスを最適化する
        -   TiDB Lightning [＃270](https://github.com/pingcap/tidb-lightning/pull/270)の TLS 認証をサポート

    -   バックアップと復元 (BR)

        -   ログ出力を最適化する[＃189](https://github.com/pingcap/br/pull/189)

-   TiDB アンシブル

    -   TiFlashデータディレクトリの作成方法を最適化する[＃1242](https://github.com/pingcap/tidb-ansible/pull/1242)
    -   TiFlash [＃1234](https://github.com/pingcap/tidb-ansible/pull/1234)に`Write Amplification`監視項目を追加
    -   CPU epollexclusive が利用できない場合の失敗したプリフライトチェックのエラーメッセージを最適化します[＃1243](https://github.com/pingcap/tidb-ansible/pull/1243)

## バグの修正 {#bug-fixes}

-   ティビ

    -   TiFlashレプリカ[＃14884](https://github.com/pingcap/tidb/pull/14884)を頻繁に更新することで発生する情報スキーマエラーを修正
    -   `AUTO_RANDOM` [＃15149](https://github.com/pingcap/tidb/pull/15149)を適用すると`last_insert_id`誤って生成される問題を修正
    -   TiFlashレプリカのステータスを更新するとDDL操作が停止する可能性がある問題を修正[＃15161](https://github.com/pingcap/tidb/pull/15161)
    -   プッシュダウンできない述語がある場合、 `Aggregation`プッシュダウンと`TopN`プッシュダウンを禁止する[＃15141](https://github.com/pingcap/tidb/pull/15141)
    -   ネストされた`view`作成[＃15440](https://github.com/pingcap/tidb/pull/15440)を禁止する
    -   `SET ROLE ALL` [＃15570](https://github.com/pingcap/tidb/pull/15570)の後に`SELECT CURRENT_ROLE()`実行したときに発生したエラーを修正
    -   `select view_name.col_name from view_name`文[＃15573](https://github.com/pingcap/tidb/pull/15573)を実行するときに`view`名前を識別できない問題を修正
    -   binlog情報の書き込み中にDDL文を前処理するとエラーが発生する可能性がある問題を修正[＃15444](https://github.com/pingcap/tidb/pull/15444)
    -   `view` s とパーティションテーブル[＃15560](https://github.com/pingcap/tidb/pull/15560)の両方にアクセスするときに発生するpanicを修正
    -   `bit(n)`データ型[＃15487](https://github.com/pingcap/tidb/pull/15487)を含む`update duplicate key`ステートメントで`VALUES`関数を実行したときに発生したエラーを修正します。
    -   一部のシナリオで指定された最大実行時間が有効にならない問題を修正[＃15616](https://github.com/pingcap/tidb/pull/15616)
    -   `Index Scan` [＃15773](https://github.com/pingcap/tidb/pull/15773)を使用して実行プランを生成するときに、現在の`ReadEngine` TiKVサーバーが含まれているかどうかがチェックされない問題を修正しました。

-   ティクヴ

    -   整合性チェックパラメータ[＃7112](https://github.com/tikv/tikv/pull/7112)を無効にするときに既存のキーをトランザクションに挿入し、すぐに削除することによって発生する競合チェックの失敗またはデータ インデックスの不整合の問題を修正しました。
    -   符号なし整数を比較する際の計算エラーを修正`TopN` [＃7199](https://github.com/tikv/tikv/pull/7199)
    -   Raftstoreにフロー制御メカニズムを導入し、フロー制御がないとログの追跡が遅くなり、クラスターが停止する可能性がある問題と、トランザクション サイズが大きいと TiKV サーバー間で頻繁に再接続が発生する可能性がある問題を解決します[＃7087](https://github.com/tikv/tikv/pull/7087) [＃7078](https://github.com/tikv/tikv/pull/7078)
    -   レプリカに送信された保留中の読み取り要求が永久にブロックされる可能性がある問題を修正[＃6543](https://github.com/tikv/tikv/pull/6543)
    -   スナップショット[＃7249](https://github.com/tikv/tikv/pull/7249)を適用することでレプリカの読み取りがブロックされる可能性がある問題を修正
    -   リーダーの移行により TiKV がpanicを起こす可能性がある問題を修正[＃7240](https://github.com/tikv/tikv/pull/7240)
    -   S3 [＃6967](https://github.com/tikv/tikv/pull/6967)にデータをバックアップするときにすべての SST ファイルがゼロで埋められる問題を修正
    -   バックアップ中に SST ファイルのサイズが記録されず、復元後に多くの空の領域が残る問題を修正[＃6983](https://github.com/tikv/tikv/pull/6983)
    -   バックアップ[＃7297](https://github.com/tikv/tikv/pull/7297)用の AWS IAM Web ID をサポート

-   PD

    -   PD がリージョンハートビート[＃2234](https://github.com/pingcap/pd/pull/2234)を処理するときにデータ競合によって発生するリージョン情報の誤りの問題を修正しました。
    -   `random-merge-scheduler`場所ラベルと配置ルール[＃2212](https://github.com/pingcap/pd/pull/2221)に従わない問題を修正
    -   配置ルールが、同じ`startKey`と`endKey` [＃2222](https://github.com/pingcap/pd/pull/2222)を持つ別の配置ルールによって上書きされる問題を修正しました。
    -   APIのバージョン番号がPDサーバー[＃2192](https://github.com/pingcap/pd/pull/2192)のバージョン番号と一致しない問題を修正

-   ツール

    -   TiDB Lightning

        -   TiDBバックエンド[＃283](https://github.com/pingcap/tidb-lightning/pull/283)で`&`文字目が`EOF`文字目に置き換えられるバグを修正

    -   バックアップと復元 (BR)

        -   BRがTiFlashクラスタデータを復元できない問題を修正[＃194](https://github.com/pingcap/br/pull/194)
