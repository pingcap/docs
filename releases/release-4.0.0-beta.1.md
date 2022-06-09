---
title: TiDB 4.0.0 Beta.1 Release Notes
---

# TiDB4.0.0Beta.1リリースノート {#tidb-4-0-0-beta-1-release-notes}

発売日：2020年2月28日

TiDBバージョン：4.0.0-beta.1

TiDB Ansibleバージョン：4.0.0-beta.1

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   `log.enable-slow-log`構成項目のタイプを整数からブール[＃14864](https://github.com/pingcap/tidb/pull/14864)に変更します
    -   MySQL 5.7との整合性を保つために、 `mysql.user`システムテーブルの`password`フィールド名を`authentication_string`に変更します（**この互換性の変更は、以前のバージョンにロールバックできないことを意味します**[＃14598](https://github.com/pingcap/tidb/pull/14598) 。
    -   `txn-total-size-limit`構成項目のデフォルト値を`1GB`から[＃14522](https://github.com/pingcap/tidb/pull/14522)に調整し`100MB` 。
    -   [＃14830](https://github.com/pingcap/tidb/pull/14830)から[＃14303](https://github.com/pingcap/tidb/pull/14303)た構成アイテムの動的な変更または更新をサポート[＃14750](https://github.com/pingcap/tidb/pull/14750)

-   TiKV
    -   `readpool.unify-read-pool`の構成項目（デフォルトでは`True` ）を追加して、ポイント・クエリがコ[＃6597](https://github.com/tikv/tikv/pull/6597) [＃6375](https://github.com/tikv/tikv/pull/6375) [＃6401](https://github.com/tikv/tikv/pull/6401) [＃6534](https://github.com/tikv/tikv/pull/6534) [＃6582](https://github.com/tikv/tikv/pull/6582) [＃6585](https://github.com/tikv/tikv/pull/6585) [＃6593](https://github.com/tikv/tikv/pull/6593)で同じ[＃6677](https://github.com/tikv/tikv/pull/6677)を使用するかどうかを制御します。

-   PD
    -   HTTP APIを最適化して、構成マネージャーと互換性を持たせる[＃2080](https://github.com/pingcap/pd/pull/2080)

-   TiDB Lightning
    -   構成ファイルで構成されていない特定の項目については、ドキュメントで指定されているデフォルトの構成を使用してください[＃255](https://github.com/pingcap/tidb-lightning/pull/255)

-   TiDB Ansible
    -   名前を`theflash`から`tiflash`に[＃1130](https://github.com/pingcap/tidb-ansible/pull/1130)
    -   TiFlashの構成ファイル[＃1138](https://github.com/pingcap/tidb-ansible/pull/1138)のデフォルト値と関連する構成を最適化する

## 新機能 {#new-features}

-   TiDB
    -   `SLOW_QUERY / CLUSTER_SLOW_QUERY`システムテーブルで[＃14878](https://github.com/pingcap/tidb/pull/14878)でも遅いログのクエリをサポート[＃14840](https://github.com/pingcap/tidb/pull/14840)
    -   SQLパフォーマンス診断をサポートする
        -   [＃14843](https://github.com/pingcap/tidb/pull/14843) [＃14810](https://github.com/pingcap/tidb/pull/14810) [＃14835](https://github.com/pingcap/tidb/pull/14835) [＃14801](https://github.com/pingcap/tidb/pull/14801) [＃14743](https://github.com/pingcap/tidb/pull/14743)
        -   [＃14718](https://github.com/pingcap/tidb/pull/14718) [＃14721](https://github.com/pingcap/tidb/pull/14721) [＃14670](https://github.com/pingcap/tidb/pull/14670) [＃14663](https://github.com/pingcap/tidb/pull/14663) [＃14668](https://github.com/pingcap/tidb/pull/14668)
        -   [＃14896](https://github.com/pingcap/tidb/pull/14896)
    -   `Sequence`機能を[＃14830](https://github.com/pingcap/tidb/pull/14830) [＃14303](https://github.com/pingcap/tidb/pull/14303) [＃14731](https://github.com/pingcap/tidb/pull/14731) [＃14589](https://github.com/pingcap/tidb/pull/14589) [＃14442](https://github.com/pingcap/tidb/pull/14442) [＃14674](https://github.com/pingcap/tidb/pull/14674)
    -   [＃14830](https://github.com/pingcap/tidb/pull/14830)から[＃14303](https://github.com/pingcap/tidb/pull/14303)た構成アイテムの動的な変更または更新をサポート[＃14750](https://github.com/pingcap/tidb/pull/14750)
    -   負荷分散ポリシーに従ってさまざまな役割からデータを自動的に読み取る機能を追加し、この機能を有効にするために`leader-and-follower`のシステム変数を追加します[＃14761](https://github.com/pingcap/tidb/pull/14761)
    -   `Coercibility`の関数を追加します[＃14739](https://github.com/pingcap/tidb/pull/14739)
    -   パーティションテーブルでの[＃14735](https://github.com/pingcap/tidb/pull/14735) [＃14644](https://github.com/pingcap/tidb/pull/14644)の設定のサポート[＃14713](https://github.com/pingcap/tidb/pull/14713)
    -   `SLOW_QUERY`テーブル[＃14451](https://github.com/pingcap/tidb/pull/14451)の特権チェックを改善します。
    -   SQL結合を使用するときにメモリが不足している場合、サポートは中間結果をディスクファイルに自動的に書き込みます[＃14708](https://github.com/pingcap/tidb/pull/14708) [＃14279](https://github.com/pingcap/tidb/pull/14279)
    -   `information_schema.PARTITIONS`のシステムテーブル[＃14347](https://github.com/pingcap/tidb/pull/14347)をクエリすることにより、テーブルパーティションのチェックをサポートします。
    -   `json_objectagg`の集計関数を追加します[＃11154](https://github.com/pingcap/tidb/pull/11154)
    -   監査ログ[＃14594](https://github.com/pingcap/tidb/pull/14594)で拒否された接続試行のログ記録をサポートする
    -   `max-server-connections`の構成アイテム（デフォルトでは`4096` ）を追加して、単一サーバーへの接続数を制御します[＃14409](https://github.com/pingcap/tidb/pull/14409)
    -   サーバーレベル[＃14440](https://github.com/pingcap/tidb/pull/14440)で複数のストレージエンジンを指定する分離読み取りをサポートする
    -   `Apply`オペレーターと`Sort`オペレーターのコストモデルを最適化して、安定性を向上させます[＃13550](https://github.com/pingcap/tidb/pull/13550) [＃14708](https://github.com/pingcap/tidb/pull/14708)

-   TiKV
    -   [＃6480](https://github.com/tikv/tikv/pull/6480)を介したステータスポートからの構成アイテムのフェッチをサポート
    -   コプロセッサー[＃6341](https://github.com/tikv/tikv/pull/6341)で`Chunk Encoder`のパフォーマンスを最適化する

-   PD
    -   ダッシュボード[＃2086](https://github.com/pingcap/pd/pull/2086)を介したクラスタのホットスポットの分散へのアクセスのサポート
    -   クラスタコンポーネント[＃2116](https://github.com/pingcap/pd/pull/2116)の`START_TIME`と`UPTIME`のキャプチャと表示をサポートします
    -   `member`の返されたメッセージにデプロイメントパスとコンポーネントバージョンの情報を追加し[＃2130](https://github.com/pingcap/pd/pull/2130)
    -   pd-ctlに`component`つのサブコマンドを追加して、他のコンポーネントの構成を変更および確認します（実験的） [＃2092](https://github.com/pingcap/pd/pull/2092)

-   TiDB Binlog
    -   コンポーネント間の[＃894](https://github.com/pingcap/tidb-binlog/pull/894)をサポート[＃904](https://github.com/pingcap/tidb-binlog/pull/904)
    -   Drainerに`kafka-client-id`の構成アイテムを追加して、Kafkaのクライアント[＃902](https://github.com/pingcap/tidb-binlog/pull/902)を構成します。
    -   [＃885](https://github.com/pingcap/tidb-binlog/pull/885)での増分バックアップデータのパージをサポート

-   TiDB Ansible
    -   1つのクラスタでの複数のGrafana/Prometheus/Alertmanagersのデプロイをサポート[＃1142](https://github.com/pingcap/tidb-ansible/pull/1142)
    -   TiFlashの設定ファイルに`metric_port`の設定項目（デフォルトでは`8234` ）を追加します[＃1145](https://github.com/pingcap/tidb-ansible/pull/1145)
    -   TiFlashの設定ファイルに`flash_proxy_status_port`の設定項目（デフォルトでは`20292` ）を追加します[＃1141](https://github.com/pingcap/tidb-ansible/pull/1141)
    -   [＃1151](https://github.com/pingcap/tidb-ansible/pull/1151)モニタリングダッシュボードを追加する[＃1147](https://github.com/pingcap/tidb-ansible/pull/1147)

## バグの修正 {#bug-fixes}

-   TiDB
    -   列名が64文字を超える`view`を作成するとエラーが報告される問題を修正します[＃14850](https://github.com/pingcap/tidb/pull/14850)
    -   `create or replace view`ステートメントが正しく処理されないために`information_schema.views`に重複データが存在する問題を修正します[＃14832](https://github.com/pingcap/tidb/pull/14832)
    -   `plan cache`が有効になっている場合の`BatchPointGet`の誤った結果を修正します[＃14855](https://github.com/pingcap/tidb/pull/14855)
    -   タイムゾーンが変更された後にデータが間違ったパーティションテーブルに挿入される問題を修正します[＃14370](https://github.com/pingcap/tidb/pull/14370)
    -   外部結合の簡略化中に`IsTrue`関数の無効な名前を使用して式を再構築するときに発生したパニックを修正します[＃14515](https://github.com/pingcap/tidb/pull/14515)
    -   `show binding`ステートメント[＃14443](https://github.com/pingcap/tidb/pull/14443)の誤った特権チェックを修正します

-   TiKV
    -   [＃6569](https://github.com/tikv/tikv/pull/6569)と[＃6463](https://github.com/tikv/tikv/pull/6463)の`CAST`関数の一貫性のない動作を修正し[＃6461](https://github.com/tikv/tikv/pull/6461) 357 [＃6459](https://github.com/tikv/tikv/pull/6459) [＃6474](https://github.com/tikv/tikv/pull/6474) [＃6492](https://github.com/tikv/tikv/pull/6492)

-   TiDB Lightning
    -   サーバーモード[＃259](https://github.com/pingcap/tidb-lightning/pull/259)以外ではWebインターフェイスが機能しないというバグを修正します。
