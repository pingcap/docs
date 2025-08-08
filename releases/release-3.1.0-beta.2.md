---
title: TiDB 3.1 Beta.2 Release Notes
summary: TiDB 3.1 Beta.2は2020年3月9日にリリースされました。TiDB、TiKV、PDクライアント、バックアップ、PD、 TiFlash、およびTiDB Ansibleの互換性の変更、新機能、バグ修正、および改善が含まれています。新しいバージョンでは一部の既知の問題が修正されているため、最新の3.1.xバージョンを使用することをお勧めします。
---

# TiDB 3.1 ベータ 2 リリースノート {#tidb-3-1-beta-2-release-notes}

発売日：2020年3月9日

TiDB バージョン: 3.1.0-beta.2

TiDB Ansible バージョン: 3.1.0-beta.2

> **警告：**
>
> このバージョンにはいくつかの既知の問題が見つかりましたが、これらの問題は新しいバージョンで修正されています。最新の3.1.xバージョンをご利用いただくことをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   ツール
    -   TiDB Lightning
        -   構成ファイル[＃255](https://github.com/pingcap/tidb-lightning/pull/255)で設定されていない特定の項目については、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)で指定されたデフォルト設定を使用します。
        -   TiDBパスワードを設定するための`--tidb-password` CLIパラメータを追加する[＃253](https://github.com/pingcap/tidb-lightning/pull/253)

## 新機能 {#new-features}

-   TiDB
    -   列属性に`AutoRandom`キーワードを追加することで、TiDB が主キーにランダムな整数を自動的に割り当てるようになり、主キー`AUTO_INCREMENT`によって発生する書き込みホットスポットを回避します[＃14555](https://github.com/pingcap/tidb/pull/14555)
    -   DDL ステートメント[＃14537](https://github.com/pingcap/tidb/pull/14537)による列ストアのレプリカの作成または削除のサポート
    -   オプティマイザが異なるstorageエンジンを独立して選択できる機能を追加[＃14537](https://github.com/pingcap/tidb/pull/14537)
    -   SQLヒントが異なるstorageエンジンをサポートする機能を追加[＃14537](https://github.com/pingcap/tidb/pull/14537)
    -   `tidb_replica_read`システム変数[＃13464](https://github.com/pingcap/tidb/pull/13464)を使用してフォロワーからのデータの読み取りをサポート
-   TiKV
    -   Raftstore
        -   他のノードをTiKVサーバー[＃6491](https://github.com/tikv/tikv/pull/6491)に接続するための`peer_address`パラメータを追加します
        -   `read_index`と`read_index_resp`監視メトリックを追加して、 `ReadIndex`リクエストの数を監視します[＃6610](https://github.com/tikv/tikv/pull/6610)
-   PDクライアント
    -   ローカルスレッドの統計情報をPD [＃6605](https://github.com/tikv/tikv/pull/6605)に報告する機能をサポート
-   バックアップ
    -   `RocksIOLimiter`フロー制御ライブラリを Rust の`async-speed-limit`フロー制御ライブラリに置き換えて、ファイル[＃6462](https://github.com/tikv/tikv/pull/6462)をバックアップするときに余分なメモリコピーを排除します。
-   PD
    -   場所ラベル名[＃2084](https://github.com/pingcap/pd/pull/2084)でバックスラッシュを許容する
-   TiFlash
    -   初回リリース
-   TiDB アンシブル
    -   1つのクラスターに複数のGrafana/Prometheus/Alertmanagerをデプロイすることをサポート[＃1143](https://github.com/pingcap/tidb-ansible/pull/1143)
    -   TiFlashコンポーネント[＃1148](https://github.com/pingcap/tidb-ansible/pull/1148)展開をサポート
    -   TiFlashコンポーネント[＃1152](https://github.com/pingcap/tidb-ansible/pull/1152)に関連する監視メトリックを追加します

## バグ修正 {#bug-fixes}

-   TiKV
    -   Raftstore
        -   Hibernate Regions [＃6450](https://github.com/tikv/tikv/pull/6450)からデータが正しく読み込まれないため、読み取り要求を処理できない問題を修正しました。
        -   リーダー移行プロセス中の`ReadIndex`リクエストによって引き起こされるpanic問題を修正しました[＃6613](https://github.com/tikv/tikv/pull/6613)
        -   一部の特殊な状況で休止状態領域が正しく起動しない問題を修正[＃6730](https://github.com/tikv/tikv/pull/6730) [＃6737](https://github.com/tikv/tikv/pull/6737) [＃6972](https://github.com/tikv/tikv/pull/6972)
    -   バックアップ
        -   追加データ[＃6659](https://github.com/tikv/tikv/pull/6659)のバックアップによって復元中に発生した不整合なデータインデックスを修正
        -   バックアップ中に削除された値を誤って処理することによって発生するpanicを修正[＃6726](https://github.com/tikv/tikv/pull/6726)
-   PD
    -   ルールチェッカーがリージョン[＃2161](https://github.com/pingcap/pd/pull/2161)にストアを割り当てられないために発生するpanicを修正
-   ツール
    -   TiDB Lightning
        -   サーバーモード[＃259](https://github.com/pingcap/tidb-lightning/pull/259)以外ではWebインターフェースが動作しないバグを修正
    -   BR (バックアップと復元)
        -   データの復元時に回復不能なエラーが発生し、 BR が時間内に終了できない問題を修正しました[＃152](https://github.com/pingcap/br/pull/152)
-   TiDB アンシブル
    -   一部のシナリオでPDLeaderを取得できないためにローリングアップデートコマンドが失敗する問題を修正しました[＃1122](https://github.com/pingcap/tidb-ansible/pull/1122)
