---
title: TiDB 3.1 Beta.2 Release Notes
---

# TiDB3.1Beta.2リリースノート {#tidb-3-1-beta-2-release-notes}

発売日：2020年3月9日

TiDBバージョン：3.1.0-beta.2

TiDB Ansibleバージョン：3.1.0-beta.2

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の3.1.xバージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   ツール
    -   TiDB Lightning
        -   構成ファイル[＃255](https://github.com/pingcap/tidb-lightning/pull/255)で構成されていない特定の項目については、 [TiDB LightningConfiguration / コンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)で指定されたデフォルト構成を使用します。
        -   `--tidb-password` CLIパラメーターを追加して、TiDBパスワードを設定します[＃253](https://github.com/pingcap/tidb-lightning/pull/253)

## 新機能 {#new-features}

-   TiDB
    -   列属性に`AutoRandom`キーワードを追加して、TiDBがランダムな整数を主キーに自動的に割り当てることができるようにすることをサポートします。これにより、 `AUTO_INCREMENT`の主キーによって引き起こされる書き込みホットスポットが回避されます[＃14555](https://github.com/pingcap/tidb/pull/14555)
    -   DDLステートメントによる列ストアレプリカの作成または削除のサポート[＃14537](https://github.com/pingcap/tidb/pull/14537)
    -   オプティマイザーが異なるストレージエンジンを個別に選択できる機能を追加する[＃14537](https://github.com/pingcap/tidb/pull/14537)
    -   SQLヒントがさまざまなストレージエンジンをサポートする機能を追加する[＃14537](https://github.com/pingcap/tidb/pull/14537)
    -   `tidb_replica_read`システム変数[＃13464](https://github.com/pingcap/tidb/pull/13464)を使用して、フォロワーからのデータの読み取りをサポートします
-   TiKV
    -   ラフトストア
        -   `peer_address`つのパラメーターを追加して、他のノードをTiKVサーバーに接続します[＃6491](https://github.com/tikv/tikv/pull/6491)
        -   `read_index`と`read_index_resp`の監視メトリックを追加して、 `ReadIndex`のリクエストの数を監視します[＃6610](https://github.com/tikv/tikv/pull/6610)
-   PDクライアント
    -   [＃6605](https://github.com/tikv/tikv/pull/6605)へのローカルスレッドの統計レポートのサポート
-   バックアップ
    -   `RocksIOLimiter`のフロー制御ライブラリをRustの`async-speed-limit`のフロー制御ライブラリに置き換えて、ファイルをバックアップするときに余分なメモリコピーを排除します[＃6462](https://github.com/tikv/tikv/pull/6462)
-   PD
    -   ロケーションラベル名[＃2084](https://github.com/pingcap/pd/pull/2084)の円記号を許容します
-   TiFlash
    -   初回リリース
-   TiDB Ansible
    -   1つのクラスタでの複数のGrafana/Prometheus/Alertmanagerのデプロイをサポート[＃1143](https://github.com/pingcap/tidb-ansible/pull/1143)
    -   TiFlashコンポーネントの展開をサポートする[＃1148](https://github.com/pingcap/tidb-ansible/pull/1148)
    -   TiFlashコンポーネントに関連する監視メトリックを追加する[＃1152](https://github.com/pingcap/tidb-ansible/pull/1152)

## バグの修正 {#bug-fixes}

-   TiKV
    -   ラフトストア
        -   Hibernate Regions [＃6450](https://github.com/tikv/tikv/pull/6450)からデータが適切に読み取られないため、読み取り要求を処理できない問題を修正します。
        -   リーダーの転送プロセス中に`ReadIndex`のリクエストによって引き起こされるpanicの問題を修正します[＃6613](https://github.com/tikv/tikv/pull/6613)
        -   一部の特別な条件で休止状態の[＃6730](https://github.com/tikv/tikv/pull/6730)が正しく起動されない問題を修正し[＃6737](https://github.com/tikv/tikv/pull/6737) [＃6972](https://github.com/tikv/tikv/pull/6972)
    -   バックアップ
        -   余分なデータのバックアップによって引き起こされた復元中の一貫性のないデータインデックスを修正します[＃6659](https://github.com/tikv/tikv/pull/6659)
        -   バックアップ中に削除された値を誤って処理することによって引き起こされるpanicを修正します[＃6726](https://github.com/tikv/tikv/pull/6726)
-   PD
    -   ルールチェッカーがリージョン[＃2161](https://github.com/pingcap/pd/pull/2161)へのストアの割り当てに失敗したために発生したpanicを修正します
-   ツール
    -   TiDB Lightning
        -   Webインターフェイスがサーバーモード[＃259](https://github.com/pingcap/tidb-lightning/pull/259)以外では機能しないというバグを修正します
    -   BR（バックアップと復元）
        -   データの復元時に発生した回復不能なエラーのためにBRが時間内に終了できない問題を修正します[＃152](https://github.com/pingcap/br/pull/152)
-   TiDB Ansible
    -   一部のシナリオでPDリーダーを取得できないためにローリングアップデートコマンドが失敗する問題を修正します[＃1122](https://github.com/pingcap/tidb-ansible/pull/1122)
