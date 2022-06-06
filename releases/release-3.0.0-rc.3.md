---
title: TiDB 3.0.0-rc.3 Release Notes
---

# TiDB3.0.0-rc.3リリースノート {#tidb-3-0-0-rc-3-release-notes}

発売日：2019年6月21日

TiDBバージョン：3.0.0-rc.3

TiDB Ansibleバージョン：3.0.0-rc.3

## 概要 {#overview}

2019年6月21日、TiDB3.0.0-rc.3がリリースされました。対応するTiDBAnsibleのバージョンは3.0.0-rc.3です。 TiDB 3.0.0-rc.2と比較して、このリリースでは、安定性、使いやすさ、機能、SQLオプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   仮想生成された列統計を収集する機能を削除する[＃10629](https://github.com/pingcap/tidb/pull/10629)
    -   ポイントクエリ中に主キー定数がオーバーフローする問題を修正[＃10699](https://github.com/pingcap/tidb/pull/10699)
    -   `fast analyze`で初期化されていない情報を使用するとパニック[＃10691](https://github.com/pingcap/tidb/pull/10691)が発生する問題を修正します
    -   `prepare`を使用して`create view`ステートメントを実行すると、列情報が間違っているためにパニックが発生する問題を修正します[＃10713](https://github.com/pingcap/tidb/pull/10713)
    -   ウィンドウ関数を処理するときに列情報が複製されない問題を修正します[＃10720](https://github.com/pingcap/tidb/pull/10720)
    -   インデックス結合[＃10854](https://github.com/pingcap/tidb/pull/10854)での内部テーブル選択の選択率の誤った推定を修正しました
    -   `stats-lease`変数値が[＃10811](https://github.com/pingcap/tidb/pull/10811)の場合の自動ロード統計をサポートします

-   実行エンジン
    -   [＃10636](https://github.com/pingcap/tidb/pull/10636)で`Close`関数を呼び出すときにリソースが正しく解放されない問題を修正し`StreamAggExec`
    -   パーティションテーブル[＃10689](https://github.com/pingcap/tidb/pull/10689)に対して`show create table`ステートメントを実行した結果、 `table_option`と`partition_options`の順序が正しくない問題を修正します。
    -   逆順のスキャンデータをサポートすることにより、 `admin show ddl jobs`のパフォーマンスを向上させます[＃10687](https://github.com/pingcap/tidb/pull/10687)
    -   このステートメントに`current_user`フィールド[＃10684](https://github.com/pingcap/tidb/pull/10684)がある場合、RBACの`show grants`ステートメントの結果がMySQLの結果と互換性がないという問題を修正します。
    -   UUIDが複数のノードで重複する値を生成する可能性がある問題を修正します[＃10712](https://github.com/pingcap/tidb/pull/10712)
    -   [＃10635](https://github.com/pingcap/tidb/pull/10635)で`show view`特権が考慮されない問題を修正し`explain`
    -   ホットスポットの問題を軽減するために、テーブルRegionを手動で分割する`split table region`ステートメントを追加します[＃10765](https://github.com/pingcap/tidb/pull/10765)
    -   ホットスポットの問題を軽減するためにインデックスリージョンを手動で分割する`split index region`ステートメントを追加します[＃10764](https://github.com/pingcap/tidb/pull/10764)
    -   `create user`などの複数のステートメントを連続[＃10737](https://github.com/pingcap/tidb/pull/10737)て実行する場合の誤った実行の問題を修正し`revoke` `grant`
    -   ブロックリストを追加して、式をコプロセッサー[＃10791](https://github.com/pingcap/tidb/pull/10791)にプッシュダウンすることを禁止します。
    -   クエリがメモリ構成の制限を超えたときに`expensive query`ログを出力する機能を追加します[＃10849](https://github.com/pingcap/tidb/pull/10849)
    -   `bind-info-lease`の構成アイテムを追加して、変更されたバインディング実行プラン[＃10727](https://github.com/pingcap/tidb/pull/10727)の更新時間を制御します。
    -   `execdetails.ExecDetails`ポインター[＃10832](https://github.com/pingcap/tidb/pull/10832)に起因する、コプロセッサー・リソースの迅速な解放の失敗によって引き起こされる、同時発生率の高いシナリオでのOOMの問題を修正します。
    -   場合によっては`kill`ステートメントによって引き起こされるパニックの問題を修正します[＃10876](https://github.com/pingcap/tidb/pull/10876)

-   サーバ
    -   GC1の修復時にゴルーチンがリークする可能性がある問題を修正し[＃10683](https://github.com/pingcap/tidb/pull/10683)
    -   遅いクエリで`host`の情報を表示することをサポートします[＃10693](https://github.com/pingcap/tidb/pull/10693)
    -   [＃10632](https://github.com/pingcap/tidb/pull/10632)と相互作用するアイドルリンクの再利用をサポート
    -   RBAC3で`skip-grant-table`オプションを有効にするためのサポートを修正し[＃10738](https://github.com/pingcap/tidb/pull/10738)
    -   `pessimistic-txn`の構成が無効になる問題を修正します[＃10825](https://github.com/pingcap/tidb/pull/10825)
    -   アクティブにキャンセルされたticlientリクエストがまだ再試行される問題を修正します[＃10850](https://github.com/pingcap/tidb/pull/10850)
    -   悲観的なトランザクションが楽観的なトランザクションと競合する場合のパフォーマンスを向上させる[＃10881](https://github.com/pingcap/tidb/pull/10881)

-   DDL
    -   `alter table`を使用して文字セットを変更すると`blob`タイプが変更される問題を修正します[＃10698](https://github.com/pingcap/tidb/pull/10698)
    -   ホットスポットの問題を軽減するために、列に`AUTO_INCREMENT`属性が含まれている場合に、 `SHARD_ROW_ID_BITS`を使用して行IDを分散する機能を追加します[＃10794](https://github.com/pingcap/tidb/pull/10794)
    -   `alter table`ステートメント[＃10808](https://github.com/pingcap/tidb/pull/10808)を使用して、保存された生成列の追加を禁止します。
    -   DDLメタデータの無効な存続時間を最適化して、クラスタのアップグレード後にDDL操作が遅くなる期間を短縮します[＃10795](https://github.com/pingcap/tidb/pull/10795)

## PD {#pd}

-   `enable-two-way-merge`つの構成アイテムを追加して、一方向のマージのみを許可します[＃1583](https://github.com/pingcap/pd/pull/1583)
-   `AddLightLearner`と`AddLightPeer`のスケジューリング操作を追加して、リージョンスキャッターのスケジューリングを制限メカニズムによって制限されないようにします[＃1563](https://github.com/pingcap/pd/pull/1563)
-   システムの起動時にデータにレプリカレプリケーションが1つしかない可能性があるため、信頼性が不十分であるという問題を修正します[＃1581](https://github.com/pingcap/pd/pull/1581)
-   構成アイテムのエラーを回避するために構成チェックロジックを最適化する[＃1585](https://github.com/pingcap/pd/pull/1585)
-   `store-balance-rate`構成の定義を、1分あたりに生成されるバランス演算子の数の上限に調整します[＃1591](https://github.com/pingcap/pd/pull/1591)
-   ストアがスケジュールされた操作を生成できなかった可能性がある問題を修正します[＃1590](https://github.com/pingcap/pd/pull/1590)

## TiKV {#tikv}

-   エンジン
    -   イテレータがステータスをチェックしないためにシステムで不完全なスナップショットが生成される問題を修正します[＃4936](https://github.com/tikv/tikv/pull/4936)
    -   異常状態での停電後にスナップショットを受信するときにディスクへのデータのフラッシュが遅れることによって引き起こされるデータ損失の問題を修正します[＃4850](https://github.com/tikv/tikv/pull/4850)

-   サーバ
    -   `block-size`構成の有効性を確認する機能を追加します[＃4928](https://github.com/tikv/tikv/pull/4928)
    -   `READ_INDEX`関連の監視メトリックを追加[＃4830](https://github.com/tikv/tikv/pull/4830)
    -   GCワーカー関連の監視メトリックを追加する[＃4922](https://github.com/tikv/tikv/pull/4922)

-   ラフトストア
    -   ローカルリーダーのキャッシュが正しくクリアされない問題を修正します[＃4778](https://github.com/tikv/tikv/pull/4778)
    -   リーダーを転送して`conf`を変更すると、リクエストの遅延が増える可能性がある問題を修正し[＃4734](https://github.com/tikv/tikv/pull/4734) 。
    -   古いコマンドが誤って報告される問題を修正します[＃4682](https://github.com/tikv/tikv/pull/4682)
    -   コマンドが長時間保留される可能性がある問題を修正します[＃4810](https://github.com/tikv/tikv/pull/4810)
    -   スナップショットファイルのディスクへの同期の遅延が原因で発生する停電後にファイルが破損する問題を修正し[＃4850](https://github.com/tikv/tikv/pull/4850) [＃4807](https://github.com/tikv/tikv/pull/4807)

-   コプロセッサー
    -   ベクトル計算でTop-Nをサポート[＃4827](https://github.com/tikv/tikv/pull/4827)
    -   ベクトル計算[＃4786](https://github.com/tikv/tikv/pull/4786)で`Stream`の集計をサポート
    -   ベクトル計算[＃4777](https://github.com/tikv/tikv/pull/4777)で`AVG`集計関数をサポートする
    -   ベクトル計算[＃4771](https://github.com/tikv/tikv/pull/4771)で`First`集計関数をサポートする
    -   ベクトル計算[＃4797](https://github.com/tikv/tikv/pull/4797)で`SUM`集計関数をサポートする
    -   ベクトル計算で`MAX`集計関数を[＃4837](https://github.com/tikv/tikv/pull/4837) `MIN`
    -   ベクトル計算[＃4747](https://github.com/tikv/tikv/pull/4747)で`Like`式をサポートする
    -   ベクトル計算[＃4849](https://github.com/tikv/tikv/pull/4849)で`MultiplyDecimal`式をサポートする
    -   ベクトル計算で`BitAnd` `BitXor`を[＃4724](https://github.com/tikv/tikv/pull/4724) `BitOr`
    -   ベクトル計算[＃4808](https://github.com/tikv/tikv/pull/4808)で`UnaryNot`式をサポートする

-   取引
    -   悲観的なトランザクションでの非悲観的なロックの競合が原因でエラーが発生する問題を修正し[＃4883](https://github.com/tikv/tikv/pull/4883) [＃4801](https://github.com/tikv/tikv/pull/4801)
    -   悲観的なトランザクションを有効にしてパフォーマンスを向上させた後、楽観的なトランザクションの不要な計算を減らします[＃4813](https://github.com/tikv/tikv/pull/4813)
    -   デッドロック状態でトランザクション全体がロールバック操作を必要としないようにするために、単一ステートメントのロールバック機能を追加します[＃4848](https://github.com/tikv/tikv/pull/4848)
    -   悲観的なトランザクション関連の監視項目を追加する[＃4852](https://github.com/tikv/tikv/pull/4852)
    -   `ResolveLockLite`コマンドを使用して軽量ロックを解決し、重大な競合が存在する場合のパフォーマンスを向上させることをサポートします[＃4882](https://github.com/tikv/tikv/pull/4882)

-   tikv-ctl
    -   より多くの異常状態のチェックをサポートするために`bad-regions`コマンドを追加します[＃4862](https://github.com/tikv/tikv/pull/4862)
    -   `tombstone`コマンドを強制実行する機能を追加[＃4862](https://github.com/tikv/tikv/pull/4862)

-   その他
    -   `dist_release`コンパイルコマンド[＃4841](https://github.com/tikv/tikv/pull/4841)を追加します

## ツール {#tools}

-   TiDB Binlog
    -   データの書き込みに失敗したときにポンプが戻り値をチェックしないことによって引き起こされる誤ったオフセットの問題を修正します[＃640](https://github.com/pingcap/tidb-binlog/pull/640)
    -   コンテナ環境でブリッジモードをサポートするために、Drainerに`advertise-addr`の構成を追加します[＃634](https://github.com/pingcap/tidb-binlog/pull/634)
    -   Pumpに`GetMvccByEncodeKey`関数を追加して、トランザクションステータスのクエリを高速化します[＃632](https://github.com/pingcap/tidb-binlog/pull/632)

## TiDB Ansible {#tidb-ansible}

-   監視項目を追加して、クラスタの最大QPS値を予測します（デフォルトでは「非表示」） [＃f5cfa4d](https://github.com/pingcap/tidb-ansible/commit/f5cfa4d903bbcd77e01eddc8d31eabb6e6157f73)
