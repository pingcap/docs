---
title: TiDB 4.0.0 Beta.1 Release Notes
summary: TiDB 4.0.0 Beta.1は2020年2月28日にリリースされました。互換性の変更、新機能、バグ修正が含まれています。主な変更点としては、SQLパフォーマンス診断のサポート、シーケンス関数、コンポーネント間のTLSサポートなどが挙げられます。さらに、 TiDB LightningのWebインターフェースのバグ修正も行われました。
---

# TiDB 4.0.0 ベータ.1 リリースノート {#tidb-4-0-0-beta-1-release-notes}

発売日：2020年2月28日

TiDB バージョン: 4.0.0-beta.1

TiDB Ansible バージョン: 4.0.0-beta.1

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   `log.enable-slow-log`構成項目の型を整数からブール型に変更します[＃14864](https://github.com/pingcap/tidb/pull/14864)
    -   MySQL 5.7と一致するように、 `mysql.user`システム テーブルの`password`フィールド名を`authentication_string`に変更します (**この互換性の変更により、以前のバージョンにロールバックできなくなります**) [＃14598](https://github.com/pingcap/tidb/pull/14598)
    -   `txn-total-size-limit`構成項目のデフォルト値を`1GB`から`100MB`に調整します[＃14522](https://github.com/pingcap/tidb/pull/14522)
    -   PD [＃14750](https://github.com/pingcap/tidb/pull/14750) [＃14303](https://github.com/pingcap/tidb/pull/14303) [＃14830](https://github.com/pingcap/tidb/pull/14830)から読み取った構成項目の動的な変更または更新をサポート

-   TiKV
    -   ポイントクエリがコプロセッサー[＃6375](https://github.com/tikv/tikv/pull/6375) [＃6401](https://github.com/tikv/tikv/pull/6401) [＃6534](https://github.com/tikv/tikv/pull/6534) [＃6582](https://github.com/tikv/tikv/pull/6582) [＃6585](https://github.com/tikv/tikv/pull/6585) [＃6593](https://github.com/tikv/tikv/pull/6593) [＃6597](https://github.com/tikv/tikv/pull/6597) [＃6677](https://github.com/tikv/tikv/pull/6677)と同じスレッドを使用するかどうかを制御するために、 `readpool.unify-read-pool`構成項目（デフォルトでは`True` ）を追加します。

-   PD
    -   HTTP APIを最適化して構成マネージャー[＃2080](https://github.com/pingcap/pd/pull/2080)と互換性を持たせる

-   TiDB Lightning
    -   構成ファイル[＃255](https://github.com/pingcap/tidb-lightning/pull/255)で設定されていない特定の項目については、ドキュメントで指定されたデフォルト設定を使用します。

-   TiDB アンシブル
    -   `theflash`を`tiflash` [＃1130](https://github.com/pingcap/tidb-ansible/pull/1130)に名前変更
    -   TiFlashの設定ファイル[＃1138](https://github.com/pingcap/tidb-ansible/pull/1138)のデフォルト値と関連設定を最適化します

## 新機能 {#new-features}

-   TiDB
    -   `SLOW_QUERY / CLUSTER_SLOW_QUERY`システムテーブル[＃14840](https://github.com/pingcap/tidb/pull/14840) [＃14878](https://github.com/pingcap/tidb/pull/14878)の任意の時点のスローログのクエリをサポート
    -   SQLパフォーマンス診断をサポート
        -   [＃14843](https://github.com/pingcap/tidb/pull/14843) [＃14810](https://github.com/pingcap/tidb/pull/14810) [＃14835](https://github.com/pingcap/tidb/pull/14835) [＃14801](https://github.com/pingcap/tidb/pull/14801) [＃14743](https://github.com/pingcap/tidb/pull/14743)
        -   [＃14718](https://github.com/pingcap/tidb/pull/14718) [＃14721](https://github.com/pingcap/tidb/pull/14721) [＃14670](https://github.com/pingcap/tidb/pull/14670) [＃14663](https://github.com/pingcap/tidb/pull/14663) [＃14668](https://github.com/pingcap/tidb/pull/14668)
        -   [＃14896](https://github.com/pingcap/tidb/pull/14896)
    -   `Sequence`機能[＃14731](https://github.com/pingcap/tidb/pull/14731) [＃14589](https://github.com/pingcap/tidb/pull/14589) [＃14674](https://github.com/pingcap/tidb/pull/14674) [＃14442](https://github.com/pingcap/tidb/pull/14442) [＃14303](https://github.com/pingcap/tidb/pull/14303) [＃14830](https://github.com/pingcap/tidb/pull/14830)をサポート
    -   PD [＃14750](https://github.com/pingcap/tidb/pull/14750) [＃14303](https://github.com/pingcap/tidb/pull/14303) [＃14830](https://github.com/pingcap/tidb/pull/14830)から読み取った構成項目の動的な変更または更新をサポート
    -   負荷分散ポリシーに従って異なるロールからデータを自動的に読み取る機能を追加し、この機能を有効にするために`leader-and-follower`システム変数を追加します[＃14761](https://github.com/pingcap/tidb/pull/14761)
    -   `Coercibility`関数[＃14739](https://github.com/pingcap/tidb/pull/14739)追加する
    -   パーティションテーブル[＃14735](https://github.com/pingcap/tidb/pull/14735) [＃14713](https://github.com/pingcap/tidb/pull/14713) [＃14644](https://github.com/pingcap/tidb/pull/14644)でのTiFlashレプリカの設定をサポート
    -   `SLOW_QUERY`テーブル[＃14451](https://github.com/pingcap/tidb/pull/14451)の権限チェックを改善
    -   SQL結合を使用する際にメモリが不足している場合、中間結果をディスクファイルに自動的に書き込む機能をサポート[＃14708](https://github.com/pingcap/tidb/pull/14708) [＃14279](https://github.com/pingcap/tidb/pull/14279)
    -   `information_schema.PARTITIONS`システムテーブル[＃14347](https://github.com/pingcap/tidb/pull/14347)をクエリしてテーブルパーティションのチェックをサポート
    -   `json_objectagg`集計関数[＃11154](https://github.com/pingcap/tidb/pull/11154)追加する
    -   監査ログに拒否された接続試行を記録することをサポート[＃14594](https://github.com/pingcap/tidb/pull/14594)
    -   1つのサーバーへの接続数を制御するために、 `max-server-connections`構成項目（デフォルトでは`4096` ）を追加します[＃14409](https://github.com/pingcap/tidb/pull/14409)
    -   サーバーレベル[＃14440](https://github.com/pingcap/tidb/pull/14440)で複数のstorageエンジンを指定して分離読み取りをサポート
    -   `Apply`オペレータと`Sort`オペレータのコストモデルを最適化して安定性を向上させる[＃13550](https://github.com/pingcap/tidb/pull/13550) [＃14708](https://github.com/pingcap/tidb/pull/14708)

-   TiKV
    -   HTTP API [＃6480](https://github.com/tikv/tikv/pull/6480)経由でステータス ポートから構成項目を取得する機能をサポート
    -   コプロセッサー[＃6341](https://github.com/tikv/tikv/pull/6341)の`Chunk Encoder`のパフォーマンスを最適化

-   PD
    -   ダッシュボード UI [＃2086](https://github.com/pingcap/pd/pull/2086)を通じてクラスター内のホットスポットの分布へのアクセスをサポート
    -   クラスターコンポーネント[＃2116](https://github.com/pingcap/pd/pull/2116)の`START_TIME`と`UPTIME`キャプチャと表示をサポート
    -   `member` API [＃2130](https://github.com/pingcap/pd/pull/2130)の返されたメッセージにデプロイメントパスとコンポーネントバージョンの情報を追加します。
    -   pd-ctlに`component`サブコマンドを追加して、他のコンポーネントの構成を変更および確認します（実験的） [＃2092](https://github.com/pingcap/pd/pull/2092)

-   TiDBBinlog
    -   コンポーネント間のTLSをサポート[＃904](https://github.com/pingcap/tidb-binlog/pull/904) [＃894](https://github.com/pingcap/tidb-binlog/pull/894)
    -   Drainerに`kafka-client-id`設定項目を追加して、KafkaのクライアントID [＃902](https://github.com/pingcap/tidb-binlog/pull/902)を設定します。
    -   Drainer [＃885](https://github.com/pingcap/tidb-binlog/pull/885)の増分バックアップ データの削除をサポート

-   TiDB アンシブル
    -   1 つのクラスターに複数の Grafana/Prometheus/Alertmanager をデプロイすることをサポート[＃1142](https://github.com/pingcap/tidb-ansible/pull/1142)
    -   TiFlashの設定ファイル[＃1145](https://github.com/pingcap/tidb-ansible/pull/1145)に`metric_port`設定項目（デフォルトでは`8234` ）を追加します。
    -   TiFlashの設定ファイル[＃1141](https://github.com/pingcap/tidb-ansible/pull/1141)に`flash_proxy_status_port`設定項目（デフォルトでは`20292` ）を追加します。
    -   TiFlash監視ダッシュボードを追加する[＃1147](https://github.com/pingcap/tidb-ansible/pull/1147) [＃1151](https://github.com/pingcap/tidb-ansible/pull/1151)

## バグ修正 {#bug-fixes}

-   TiDB
    -   64文字を超える列名で`view`作成するとエラーが報告される問題を修正しました[＃14850](https://github.com/pingcap/tidb/pull/14850)
    -   `create or replace view`文が正しく処理されていないため、 `information_schema.views`に重複データが存在する問題を修正[＃14832](https://github.com/pingcap/tidb/pull/14832)
    -   `plan cache`有効になっている場合の`BatchPointGet`の誤った結果を修正[＃14855](https://github.com/pingcap/tidb/pull/14855)
    -   タイムゾーンを変更した後にデータが間違ったパーティションテーブルに挿入される問題を修正[＃14370](https://github.com/pingcap/tidb/pull/14370)
    -   外部結合の簡素化[＃14515](https://github.com/pingcap/tidb/pull/14515)中に`IsTrue`関数の無効な名前を使用して式を再構築するときに発生するpanicを修正しました
    -   `show binding`文[＃14443](https://github.com/pingcap/tidb/pull/14443)不正な権限チェックを修正

-   TiKV
    -   TiDBとTiKVの`CAST`関数の不一致な動作を修正[＃6463](https://github.com/tikv/tikv/pull/6463) [＃6461](https://github.com/tikv/tikv/pull/6461) [＃6459](https://github.com/tikv/tikv/pull/6459) [＃6474](https://github.com/tikv/tikv/pull/6474) [＃6492](https://github.com/tikv/tikv/pull/6492) [＃6569](https://github.com/tikv/tikv/pull/6569)

-   TiDB Lightning
    -   サーバーモード[＃259](https://github.com/pingcap/tidb-lightning/pull/259)以外ではWebインターフェースが動作しないバグを修正
