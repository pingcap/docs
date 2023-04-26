---
title: TiDB 3.1 Beta.2 Release Notes
---

# TiDB 3.1 Beta.2 リリースノート {#tidb-3-1-beta-2-release-notes}

発売日：2020年3月9日

TiDB バージョン: 3.1.0-beta.2

TiDB アンシブル バージョン: 3.1.0-beta.2

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の 3.1.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   ツール
    -   TiDB Lightning
        -   構成ファイルで構成されていない特定の項目については、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)で指定されたデフォルト構成を使用します[#255](https://github.com/pingcap/tidb-lightning/pull/255)
        -   `--tidb-password` CLI パラメータを追加して、TiDB パスワードを設定します[#253](https://github.com/pingcap/tidb-lightning/pull/253)

## 新機能 {#new-features}

-   TiDB
    -   列属性に`AutoRandom`キーワードを追加して、TiDB がランダムな整数を主キーに自動的に割り当てることをサポートします。これにより、主キー`AUTO_INCREMENT`によって引き起こされる書き込みホットスポットが回避されます[#14555](https://github.com/pingcap/tidb/pull/14555)
    -   DDL ステートメントによる列ストア レプリカの作成または削除のサポート[#14537](https://github.com/pingcap/tidb/pull/14537)
    -   オプティマイザが異なるstorageエンジンを個別に選択できる機能を追加します[#14537](https://github.com/pingcap/tidb/pull/14537)
    -   SQL ヒントが異なるstorageエンジンをサポートする機能を追加します[#14537](https://github.com/pingcap/tidb/pull/14537)
    -   `tidb_replica_read`システム変数[#13464](https://github.com/pingcap/tidb/pull/13464)を使用して、フォロワーからのデータの読み取りをサポートします。
-   TiKV
    -   Raftstore
        -   `peer_address`パラメータを追加して、他のノードを TiKVサーバーに接続します[#6491](https://github.com/tikv/tikv/pull/6491)
        -   `read_index`と`read_index_resp`モニタリング メトリックを追加して、 `ReadIndex`リクエストの数をモニタリングします[#6610](https://github.com/tikv/tikv/pull/6610)
-   PD クライアント
    -   PD [#6605](https://github.com/tikv/tikv/pull/6605)へのローカル スレッドの統計レポートのサポート
-   バックアップ
    -   `RocksIOLimiter`フロー制御ライブラリを Rust の`async-speed-limit`フロー制御ライブラリに置き換えて、ファイルのバックアップ時に余分なメモリコピーを排除します[#6462](https://github.com/tikv/tikv/pull/6462)
-   PD
    -   ロケーション ラベル名でバックスラッシュを許容する[#2084](https://github.com/pingcap/pd/pull/2084)
-   TiFlash
    -   初回リリース
-   TiDB アンシブル
    -   複数の Grafana/Prometheus/Alertmanager を 1 つのクラスターにデプロイするサポート[#1143](https://github.com/pingcap/tidb-ansible/pull/1143)
    -   TiFlashコンポーネントの展開をサポート[#1148](https://github.com/pingcap/tidb-ansible/pull/1148)
    -   TiFlashコンポーネント[#1152](https://github.com/pingcap/tidb-ansible/pull/1152)に関連するモニタリング メトリックを追加します。

## バグの修正 {#bug-fixes}

-   TiKV
    -   Raftstore
        -   Hibernate Regions [#6450](https://github.com/tikv/tikv/pull/6450)からデータが正しく読み取られないため、読み取り要求を処理できない問題を修正します。
        -   リーダーの転送プロセス中の`ReadIndex`要求によって引き起こされるpanicの問題を修正します[#6613](https://github.com/tikv/tikv/pull/6613)
        -   一部の特殊な状況でハイバネート領域が正しく目覚めない問題を修正[#6730](https://github.com/tikv/tikv/pull/6730) [#6737](https://github.com/tikv/tikv/pull/6737) [#6972](https://github.com/tikv/tikv/pull/6972)
    -   バックアップ
        -   余分なデータのバックアップによって引き起こされた復元中の不整合なデータ インデックスを修正します[#6659](https://github.com/tikv/tikv/pull/6659)
        -   バックアップ中に削除された値を誤って処理することによって引き起こされるpanicを修正します[#6726](https://github.com/tikv/tikv/pull/6726)
-   PD
    -   ルール チェッカーがリージョン[#2161](https://github.com/pingcap/pd/pull/2161)へのストアの割り当てに失敗したために発生したpanicを修正します。
-   ツール
    -   TiDB Lightning
        -   サーバーモード[#259](https://github.com/pingcap/tidb-lightning/pull/259)以外でWebインターフェースが動かない不具合を修正
    -   BR (バックアップと復元)
        -   データの復元時に発生した回復不能なエラーにより、 BR が時間内に終了できない問題を修正します[#152](https://github.com/pingcap/br/pull/152)
-   TiDB アンシブル
    -   一部のシナリオで PDLeaderを取得できないため、ローリング アップデート コマンドが失敗する問題を修正します[#1122](https://github.com/pingcap/tidb-ansible/pull/1122)
