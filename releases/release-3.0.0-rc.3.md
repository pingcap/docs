---
title: TiDB 3.0.0-rc.3 Release Notes
summary: TiDB 3.0.0-rc.3は2019年6月21日にリリースされ、安定性、ユーザビリティ、機能、SQLオプティマイザー、統計、実行エンジンが改善されました。TiDB、PD、TiKV、TiDB Ansibleに修正と新機能が追加されました。主な改善点としては、統計情報の自動読み込み、テーブルとインデックス領域の手動分割、TiKVにおける悲観的トランザクションのサポートなどが挙げられます。
---

# TiDB 3.0.0-rc.3 リリースノート {#tidb-3-0-0-rc-3-release-notes}

発売日：2019年6月21日

TiDB バージョン: 3.0.0-rc.3

TiDB Ansible バージョン: 3.0.0-rc.3

## 概要 {#overview}

2019年6月21日にTiDB 3.0.0-rc.3がリリースされました。対応するTiDB Ansibleバージョンは3.0.0-rc.3です。このリリースでは、TiDB 3.0.0-rc.2と比較して、安定性、使いやすさ、機能、SQLオプティマイザー、統計、実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   仮想生成列統計[＃10629](https://github.com/pingcap/tidb/pull/10629)を収集する機能を削除します
    -   ポイントクエリ中に主キー定数がオーバーフローする問題を修正[＃10699](https://github.com/pingcap/tidb/pull/10699)
    -   `fast analyze`で初期化されていない情報を使用するとpanicが発生する問題を修正[＃10691](https://github.com/pingcap/tidb/pull/10691)
    -   `prepare`使用して`create view`文を実行すると、間違った列情報[＃10713](https://github.com/pingcap/tidb/pull/10713)のためにpanicが発生する問題を修正しました
    -   ウィンドウ関数[＃10720](https://github.com/pingcap/tidb/pull/10720)処理時に列情報が複製されない問題を修正
    -   インデックス結合[＃10854](https://github.com/pingcap/tidb/pull/10854)における内部テーブル選択の選択率の誤った推定を修正
    -   `stats-lease`変数値が0の場合の自動読み込み統計をサポート[＃10811](https://github.com/pingcap/tidb/pull/10811)

-   実行エンジン
    -   `StreamAggExec` [＃10636](https://github.com/pingcap/tidb/pull/10636)の`Close`関数を呼び出すときにリソースが正しく解放されない問題を修正しました
    -   パーティションテーブル[＃10689](https://github.com/pingcap/tidb/pull/10689)の`show create table`のステートメントを実行した結果、 `table_option`と`partition_options`の順序が正しくない問題を修正しました。
    -   逆順スキャンデータ[＃10687](https://github.com/pingcap/tidb/pull/10687)サポートすることで`admin show ddl jobs`のパフォーマンスを向上
    -   このステートメントに`current_user`フィールド[＃10684](https://github.com/pingcap/tidb/pull/10684)がある場合、RBACの`show grants`ステートメントの結果がMySQLの結果と互換性がない問題を修正しました。
    -   UUIDが複数のノードで重複した値を生成する可能性がある問題を修正[＃10712](https://github.com/pingcap/tidb/pull/10712)
    -   `show view`権限が`explain` [＃10635](https://github.com/pingcap/tidb/pull/10635)で考慮されない問題を修正
    -   ホットスポットの問題を軽減するために、テーブルリージョンを手動で分割する`split table region`ステートメントを追加します[＃10765](https://github.com/pingcap/tidb/pull/10765)
    -   ホットスポットの問題を軽減するために、インデックスリージョンを手動で分割する`split index region`ステートメントを追加します[＃10764](https://github.com/pingcap/tidb/pull/10764)
    -   `create user`などの複数`revoke`ステートメント`grant`連続して実行した場合の不正な実行問題を修正しました[＃10737](https://github.com/pingcap/tidb/pull/10737)
    -   コプロセッサー[＃10791](https://github.com/pingcap/tidb/pull/10791)への式のプッシュダウンを禁止するブロックリストを追加します。
    -   クエリがメモリ構成制限[＃10849](https://github.com/pingcap/tidb/pull/10849)を超えたときに`expensive query`ログを出力する機能を追加
    -   変更されたバインディング実行プラン[＃10727](https://github.com/pingcap/tidb/pull/10727)の更新時間を制御する`bind-info-lease`構成項目を追加します。
    -   `execdetails.ExecDetails`ポインタ[＃10832](https://github.com/pingcap/tidb/pull/10832)の結果としてコプロセッサーリソースを迅速に解放できないことによって引き起こされる、高同時シナリオでのOOM問題を修正しました。
    -   `kill`文によって発生するpanic問題を修正[＃10876](https://github.com/pingcap/tidb/pull/10876)

-   サーバ
    -   GC [＃10683](https://github.com/pingcap/tidb/pull/10683)を修復する際に goroutine がリークする可能性がある問題を修正しました
    -   低速クエリ[＃10693](https://github.com/pingcap/tidb/pull/10693)で`host`情報を表示することをサポート
    -   TiKV [＃10632](https://github.com/pingcap/tidb/pull/10632)と相互作用するアイドルリンクの再利用をサポート
    -   RBAC [＃10738](https://github.com/pingcap/tidb/pull/10738)で`skip-grant-table`オプションを有効にするためのサポートを修正
    -   `pessimistic-txn`構成が無効になる問題を修正[＃10825](https://github.com/pingcap/tidb/pull/10825)
    -   アクティブにキャンセルされた ticlient リクエストが再試行される問題を修正[＃10850](https://github.com/pingcap/tidb/pull/10850)
    -   悲観的トランザクションが楽観的トランザクションと競合する場合のパフォーマンスを改善する[＃10881](https://github.com/pingcap/tidb/pull/10881)

-   DDL
    -   `alter table`を使用して文字セットを変更すると`blob`型が変更される問題を修正[＃10698](https://github.com/pingcap/tidb/pull/10698)
    -   ホットスポットの問題を軽減するために、列に`AUTO_INCREMENT`属性が含まれている場合に`SHARD_ROW_ID_BITS`使用して行 ID を分散させる機能を追加します[＃10794](https://github.com/pingcap/tidb/pull/10794)
    -   `alter table`文[＃10808](https://github.com/pingcap/tidb/pull/10808)を使用して、保存された生成列の追加を禁止します。
    -   DDLメタデータの無効な生存時間を最適化し、クラスタのアップグレード後にDDL操作が遅くなる期間を短縮します[＃10795](https://github.com/pingcap/tidb/pull/10795)

## PD {#pd}

-   一方向のマージのみを許可するには、 `enable-two-way-merge`構成項目を追加します[＃1583](https://github.com/pingcap/pd/pull/1583)
-   `AddLightLearner`と`AddLightPeer`スケジューリング操作を追加して、 リージョン Scatterスケジューリングを制限メカニズム[＃1563](https://github.com/pingcap/pd/pull/1563)によって制限されないようにします。
-   システムの起動時にデータのレプリカレプリケーションが 1 つしか存在しないため信頼性が不十分になる問題を修正しました[＃1581](https://github.com/pingcap/pd/pull/1581)
-   構成チェックロジックを最適化して構成項目エラーを回避する[＃1585](https://github.com/pingcap/pd/pull/1585)
-   `store-balance-rate`構成の定義を、1分あたりに生成されるバランスオペレータ数の上限[＃1591](https://github.com/pingcap/pd/pull/1591)に調整します。
-   ストアがスケジュールされた操作を生成できない可能性がある問題を修正[＃1590](https://github.com/pingcap/pd/pull/1590)

## TiKV {#tikv}

-   エンジン
    -   イテレータがステータス[＃4936](https://github.com/tikv/tikv/pull/4936)をチェックしないために、システム内に不完全なスナップショットが生成される問題を修正しました。
    -   異常な状況で電源障害が発生した後にスナップショットを受信するときに、ディスクへのデータのフラッシュが遅れることによって発生するデータ損失の問題を修正しました[＃4850](https://github.com/tikv/tikv/pull/4850)

-   サーバ
    -   `block-size`構成[＃4928](https://github.com/tikv/tikv/pull/4928)の有効性をチェックする機能を追加する
    -   `READ_INDEX`関連の監視指標[＃4830](https://github.com/tikv/tikv/pull/4830)追加
    -   GCワーカー関連の監視メトリック[＃4922](https://github.com/tikv/tikv/pull/4922)を追加する

-   Raftstore
    -   ローカルリーダーのキャッシュが正しくクリアされない問題を修正[＃4778](https://github.com/tikv/tikv/pull/4778)
    -   リーダーの移行や`conf` [＃4734](https://github.com/tikv/tikv/pull/4734)変更時にリクエストの遅延が増加する可能性がある問題を修正しました
    -   古いコマンドが誤って報告される問題を修正[＃4682](https://github.com/tikv/tikv/pull/4682)
    -   コマンドが長時間保留になる可能性がある問題を修正[＃4810](https://github.com/tikv/tikv/pull/4810)
    -   スナップショットファイルをディスク[＃4807](https://github.com/tikv/tikv/pull/4807)に同期する際の遅延により、停電後にファイルが破損する問題を修正しました[＃4850](https://github.com/tikv/tikv/pull/4850)

-   コプロセッサー
    -   ベクトル計算におけるTop-Nのサポート[＃4827](https://github.com/tikv/tikv/pull/4827)
    -   ベクトル計算[＃4786](https://github.com/tikv/tikv/pull/4786)における`Stream`集計をサポート
    -   ベクトル計算[＃4777](https://github.com/tikv/tikv/pull/4777)における`AVG`集計関数をサポート
    -   ベクトル計算[＃4771](https://github.com/tikv/tikv/pull/4771)における`First`集計関数をサポート
    -   ベクトル計算[＃4797](https://github.com/tikv/tikv/pull/4797)における`SUM`集計関数をサポート
    -   ベクトル計算[＃4837](https://github.com/tikv/tikv/pull/4837)における`MAX`集計関数`MIN`サポート
    -   ベクトル計算[＃4747](https://github.com/tikv/tikv/pull/4747)における`Like`式のサポート
    -   ベクトル計算[＃4849](https://github.com/tikv/tikv/pull/4849)における`MultiplyDecimal`式のサポート
    -   ベクトル計算[＃4724](https://github.com/tikv/tikv/pull/4724)における`BitAnd` `BitXor` `BitOr`サポート
    -   ベクトル計算[＃4808](https://github.com/tikv/tikv/pull/4808)における`UnaryNot`式のサポート

-   トランザクション
    -   悲観的トランザクション[＃4801](https://github.com/tikv/tikv/pull/4801)で非悲観的ロック競合によりエラー[＃4883](https://github.com/tikv/tikv/pull/4883)発生する問題を修正
    -   悲観的トランザクションを有効にした後、楽観的的トランザクションの不要な計算を削減してパフォーマンスを向上させる[＃4813](https://github.com/tikv/tikv/pull/4813)
    -   デッドロック状況でトランザクション全体のロールバック操作が必要ないことを保証するために、単一ステートメントのロールバック機能を追加します[＃4848](https://github.com/tikv/tikv/pull/4848)
    -   悲観的トランザクション関連の監視項目[＃4852](https://github.com/tikv/tikv/pull/4852)追加
    -   深刻な競合が存在する場合のパフォーマンスを向上させるために、 `ResolveLockLite`コマンドを使用して軽量ロックを解決することをサポートします[＃4882](https://github.com/tikv/tikv/pull/4882)

-   tikv-ctl
    -   より多くの異常状態をチェックするためのコマンド`bad-regions`を追加[＃4862](https://github.com/tikv/tikv/pull/4862)
    -   `tombstone`コマンド[＃4862](https://github.com/tikv/tikv/pull/4862)強制的に実行する機能を追加

-   その他
    -   `dist_release`コンパイルコマンド[＃4841](https://github.com/tikv/tikv/pull/4841)を追加する

## ツール {#tools}

-   TiDBBinlog
    -   データの書き込みに失敗したときにPumpが戻り値をチェックしないことによって発生する間違ったオフセットの問題を修正しました[＃640](https://github.com/pingcap/tidb-binlog/pull/640)
    -   コンテナ環境[＃634](https://github.com/pingcap/tidb-binlog/pull/634)でブリッジモードをサポートするために、 Drainerに`advertise-addr`構成を追加します。
    -   Pumpに`GetMvccByEncodeKey`関数を追加して、トランザクションステータス[＃632](https://github.com/pingcap/tidb-binlog/pull/632)クエリを高速化します。

## TiDB アンシブル {#tidb-ansible}

-   クラスターの最大QPS値を予測するための監視項目を追加する（デフォルトでは「非表示」） [#f5cfa4d](https://github.com/pingcap/tidb-ansible/commit/f5cfa4d903bbcd77e01eddc8d31eabb6e6157f73)
