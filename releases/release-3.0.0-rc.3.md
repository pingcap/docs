---
title: TiDB 3.0.0-rc.3 Release Notes
---

# TiDB 3.0.0-rc.3 リリースノート {#tidb-3-0-0-rc-3-release-notes}

発売日：2019年6月21日

TiDB バージョン: 3.0.0-rc.3

TiDB Ansible バージョン: 3.0.0-rc.3

## 概要 {#overview}

2019 年 6 月 21 日に、TiDB 3.0.0-rc.3 がリリースされました。対応する TiDB Ansible バージョンは 3.0.0-rc.3 です。 TiDB 3.0.0-rc.2 と比較して、このリリースでは安定性、使いやすさ、機能、SQL オプティマイザー、統計、実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   仮想生成列統計を収集する機能を削除[<a href="https://github.com/pingcap/tidb/pull/10629">#10629</a>](https://github.com/pingcap/tidb/pull/10629)
    -   ポイントクエリ時に主キー定数がオーバーフローする問題を修正[<a href="https://github.com/pingcap/tidb/pull/10699">#10699</a>](https://github.com/pingcap/tidb/pull/10699)
    -   `fast analyze`で初期化されていない情報を使用するとpanic[<a href="https://github.com/pingcap/tidb/pull/10691">#10691</a>](https://github.com/pingcap/tidb/pull/10691)が発生する問題を修正
    -   `prepare`を使用して`create view`ステートメントを実行すると、間違った列情報によりpanicが発生する問題を修正[<a href="https://github.com/pingcap/tidb/pull/10713">#10713</a>](https://github.com/pingcap/tidb/pull/10713)
    -   ウィンドウ関数の処理時に列情報が複製されない問題を修正[<a href="https://github.com/pingcap/tidb/pull/10720">#10720</a>](https://github.com/pingcap/tidb/pull/10720)
    -   インデックス結合[<a href="https://github.com/pingcap/tidb/pull/10854">#10854</a>](https://github.com/pingcap/tidb/pull/10854)における内部テーブル選択の選択率の誤った推定を修正しました。
    -   `stats-lease`変数値が 0 [<a href="https://github.com/pingcap/tidb/pull/10811">#10811</a>](https://github.com/pingcap/tidb/pull/10811)の場合の統計の自動読み込みをサポートします。

-   実行エンジン
    -   `StreamAggExec` [<a href="https://github.com/pingcap/tidb/pull/10636">#10636</a>](https://github.com/pingcap/tidb/pull/10636)の`Close`関数呼び出し時にリソースが正しく解放されない問題を修正
    -   パーティションテーブル[<a href="https://github.com/pingcap/tidb/pull/10689">#10689</a>](https://github.com/pingcap/tidb/pull/10689)の`show create table`文の実行結果で`table_option`と`partition_options`の順序が正しくない問題を修正
    -   データの逆順スキャンをサポートすることで`admin show ddl jobs`のパフォーマンスを向上させます[<a href="https://github.com/pingcap/tidb/pull/10687">#10687</a>](https://github.com/pingcap/tidb/pull/10687)
    -   このステートメントに`current_user`フィールド[<a href="https://github.com/pingcap/tidb/pull/10684">#10684</a>](https://github.com/pingcap/tidb/pull/10684)がある場合、RBAC の`show grants`ステートメントの結果が MySQL の結果と互換性がないという問題を修正します。
    -   UUID が複数のノードで重複した値を生成する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/10712">#10712</a>](https://github.com/pingcap/tidb/pull/10712)
    -   `explain` [<a href="https://github.com/pingcap/tidb/pull/10635">#10635</a>](https://github.com/pingcap/tidb/pull/10635)で`show view`特権が考慮されない問題を修正
    -   `split table region`ステートメントを追加してテーブルリージョンを手動で分割し、ホットスポットの問題[<a href="https://github.com/pingcap/tidb/pull/10765">#10765</a>](https://github.com/pingcap/tidb/pull/10765)を軽減します。
    -   `split index region`ステートメントを追加してインデックスリージョンを手動で分割し、ホットスポットの問題を軽減します[<a href="https://github.com/pingcap/tidb/pull/10764">#10764</a>](https://github.com/pingcap/tidb/pull/10764)
    -   `create user` 、 `grant` 、 `revoke`などの複数のステートメントを連続して実行する場合の誤った実行の問題を修正します[<a href="https://github.com/pingcap/tidb/pull/10737">#10737</a>](https://github.com/pingcap/tidb/pull/10737)
    -   コプロセッサー[<a href="https://github.com/pingcap/tidb/pull/10791">#10791</a>](https://github.com/pingcap/tidb/pull/10791)への式のプッシュダウンを禁止するブロックリストを追加します。
    -   クエリがメモリ構成制限を超えた場合に`expensive query`ログを出力する機能を追加[<a href="https://github.com/pingcap/tidb/pull/10849">#10849</a>](https://github.com/pingcap/tidb/pull/10849)
    -   `bind-info-lease`構成アイテムを追加して、変更されたバインディング実行プランの更新時間を制御します[<a href="https://github.com/pingcap/tidb/pull/10727">#10727</a>](https://github.com/pingcap/tidb/pull/10727)
    -   `execdetails.ExecDetails`ポインタ[<a href="https://github.com/pingcap/tidb/pull/10832">#10832</a>](https://github.com/pingcap/tidb/pull/10832)によってコプロセッサーリソースを迅速に解放できないことが原因で発生する、同時実行シナリオの OOM 問題を修正します。
    -   場合によっては`kill`ステートメントによって引き起こされるpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/10876">#10876</a>](https://github.com/pingcap/tidb/pull/10876)

-   サーバ
    -   GC [<a href="https://github.com/pingcap/tidb/pull/10683">#10683</a>](https://github.com/pingcap/tidb/pull/10683)を修復するときに goroutine がリークする可能性がある問題を修正
    -   スロークエリでの`host`情報の表示をサポート[<a href="https://github.com/pingcap/tidb/pull/10693">#10693</a>](https://github.com/pingcap/tidb/pull/10693)
    -   TiKV [<a href="https://github.com/pingcap/tidb/pull/10632">#10632</a>](https://github.com/pingcap/tidb/pull/10632)と対話するアイドル状態のリンクの再利用をサポート
    -   RBAC [<a href="https://github.com/pingcap/tidb/pull/10738">#10738</a>](https://github.com/pingcap/tidb/pull/10738)の`skip-grant-table`オプションを有効にするサポートを修正
    -   `pessimistic-txn`設定が無効になる問題を修正[<a href="https://github.com/pingcap/tidb/pull/10825">#10825</a>](https://github.com/pingcap/tidb/pull/10825)
    -   アクティブにキャンセルされた ticlient リクエストがまだ再試行される問題を修正します[<a href="https://github.com/pingcap/tidb/pull/10850">#10850</a>](https://github.com/pingcap/tidb/pull/10850)
    -   楽観的トランザクションが悲観的トランザクションと競合する場合のパフォーマンスを改善します[<a href="https://github.com/pingcap/tidb/pull/10881">#10881</a>](https://github.com/pingcap/tidb/pull/10881)

-   DDL
    -   `alter table`を使用して文字セットを変更すると`blob`型が変更される問題を修正します[<a href="https://github.com/pingcap/tidb/pull/10698">#10698</a>](https://github.com/pingcap/tidb/pull/10698)
    -   ホットスポットの問題を軽減するために、列に`AUTO_INCREMENT`属性が含まれる場合に`SHARD_ROW_ID_BITS`を使用して行 ID を分散する機能を追加します[<a href="https://github.com/pingcap/tidb/pull/10794">#10794</a>](https://github.com/pingcap/tidb/pull/10794)
    -   `alter table`ステートメント[<a href="https://github.com/pingcap/tidb/pull/10808">#10808</a>](https://github.com/pingcap/tidb/pull/10808)を使用して、格納された生成列を追加することを禁止します。
    -   DDL メタデータの無効な生存時間を最適化して、クラスターのアップグレード後に DDL 操作が遅くなる期間を短縮します[<a href="https://github.com/pingcap/tidb/pull/10795">#10795</a>](https://github.com/pingcap/tidb/pull/10795)

## PD {#pd}

-   一方向のマージのみを許可するには`enable-two-way-merge`構成項目を追加します[<a href="https://github.com/pingcap/pd/pull/1583">#1583</a>](https://github.com/pingcap/pd/pull/1583)
-   `AddLightLearner`と`AddLightPeer`のスケジューリング操作を追加して、リージョン分散スケジューリングが制限メカニズム[<a href="https://github.com/pingcap/pd/pull/1563">#1563</a>](https://github.com/pingcap/pd/pull/1563)によって制限されないようにする
-   システムの起動時にデータのレプリカ レプリケーションが 1 つしかない可能性があるため、信頼性が不十分になる問題を修正します[<a href="https://github.com/pingcap/pd/pull/1581">#1581</a>](https://github.com/pingcap/pd/pull/1581)
-   構成アイテムのエラーを回避するために構成チェック ロジックを最適化する[<a href="https://github.com/pingcap/pd/pull/1585">#1585</a>](https://github.com/pingcap/pd/pull/1585)
-   `store-balance-rate`構成の定義を、1 分あたりに生成されるバランス オペレーターの数の上限に調整します[<a href="https://github.com/pingcap/pd/pull/1591">#1591</a>](https://github.com/pingcap/pd/pull/1591)
-   ストアがスケジュールされた操作を生成できなかった可能性がある問題を修正します[<a href="https://github.com/pingcap/pd/pull/1590">#1590</a>](https://github.com/pingcap/pd/pull/1590)

## TiKV {#tikv}

-   エンジン
    -   イテレータがステータス[<a href="https://github.com/tikv/tikv/pull/4936">#4936</a>](https://github.com/tikv/tikv/pull/4936)をチェックしないことにより、システム内で不完全なスナップショットが生成される問題を修正します。
    -   異常な状態での停電後のスナップショットの受信時にディスクへのデータのフラッシュの遅延によって引き起こされるデータ損失の問題を修正します[<a href="https://github.com/tikv/tikv/pull/4850">#4850</a>](https://github.com/tikv/tikv/pull/4850)

-   サーバ
    -   `block-size`設定の妥当性をチェックする機能を追加[<a href="https://github.com/tikv/tikv/pull/4928">#4928</a>](https://github.com/tikv/tikv/pull/4928)
    -   追加`READ_INDEX`関連の監視メトリクス[<a href="https://github.com/tikv/tikv/pull/4830">#4830</a>](https://github.com/tikv/tikv/pull/4830)
    -   GC ワーカー関連の監視メトリクスを追加[<a href="https://github.com/tikv/tikv/pull/4922">#4922</a>](https://github.com/tikv/tikv/pull/4922)

-   Raftstore
    -   ローカルリーダーのキャッシュが正しくクリアされない問題を修正[<a href="https://github.com/tikv/tikv/pull/4778">#4778</a>](https://github.com/tikv/tikv/pull/4778)
    -   リーダーの移動および`conf` [<a href="https://github.com/tikv/tikv/pull/4734">#4734</a>](https://github.com/tikv/tikv/pull/4734)の変更時にリクエスト遅延が増加する場合がある問題を修正
    -   古いコマンドが誤って報告される問題を修正[<a href="https://github.com/tikv/tikv/pull/4682">#4682</a>](https://github.com/tikv/tikv/pull/4682)
    -   コマンドが長時間保留される可能性がある問題を修正[<a href="https://github.com/tikv/tikv/pull/4810">#4810</a>](https://github.com/tikv/tikv/pull/4810)
    -   スナップショット ファイルとディスク[<a href="https://github.com/tikv/tikv/pull/4807">#4807</a>](https://github.com/tikv/tikv/pull/4807)の同期の遅延が原因で、停電後にファイル[<a href="https://github.com/tikv/tikv/pull/4850">#4850</a>](https://github.com/tikv/tikv/pull/4850)破損する問題を修正します。

-   コプロセッサー
    -   ベクトル計算で上位 N をサポート[<a href="https://github.com/tikv/tikv/pull/4827">#4827</a>](https://github.com/tikv/tikv/pull/4827)
    -   ベクトル計算[<a href="https://github.com/tikv/tikv/pull/4786">#4786</a>](https://github.com/tikv/tikv/pull/4786)での集計`Stream`をサポート
    -   ベクトル計算で`AVG`集計関数をサポート[<a href="https://github.com/tikv/tikv/pull/4777">#4777</a>](https://github.com/tikv/tikv/pull/4777)
    -   ベクトル計算で`First`集計関数をサポート[<a href="https://github.com/tikv/tikv/pull/4771">#4771</a>](https://github.com/tikv/tikv/pull/4771)
    -   ベクトル計算で`SUM`集計関数をサポート[<a href="https://github.com/tikv/tikv/pull/4797">#4797</a>](https://github.com/tikv/tikv/pull/4797)
    -   ベクトル`MIN`で`MAX`集計関数をサポート[<a href="https://github.com/tikv/tikv/pull/4837">#4837</a>](https://github.com/tikv/tikv/pull/4837)
    -   ベクトル計算[<a href="https://github.com/tikv/tikv/pull/4747">#4747</a>](https://github.com/tikv/tikv/pull/4747)で`Like`式をサポート
    -   ベクトル計算[<a href="https://github.com/tikv/tikv/pull/4849">#4849</a>](https://github.com/tikv/tikv/pull/4849)で`MultiplyDecimal`式をサポート
    -   ベクトル計算で`BitAnd` / `BitOr` / `BitXor`式をサポート[<a href="https://github.com/tikv/tikv/pull/4724">#4724</a>](https://github.com/tikv/tikv/pull/4724)
    -   ベクトル計算[<a href="https://github.com/tikv/tikv/pull/4808">#4808</a>](https://github.com/tikv/tikv/pull/4808)で`UnaryNot`式をサポート

-   トランザクション
    -   悲観的トランザクション[<a href="https://github.com/tikv/tikv/pull/4801">#4801</a>](https://github.com/tikv/tikv/pull/4801)で非悲観的ロック[<a href="https://github.com/tikv/tikv/pull/4883">#4883</a>](https://github.com/tikv/tikv/pull/4883)競合によりエラーが発生する問題を修正
    -   パフォーマンスを向上させるために楽観的トランザクションを有効にした後、悲観的トランザクションの不要な計算を削減します[<a href="https://github.com/tikv/tikv/pull/4813">#4813</a>](https://github.com/tikv/tikv/pull/4813)
    -   単一ステートメントのロールバック機能を追加して、デッドロック状況でトランザクション全体がロールバック操作を必要としないようにします[<a href="https://github.com/tikv/tikv/pull/4848">#4848</a>](https://github.com/tikv/tikv/pull/4848)
    -   悲観的トランザクション関連の監視項目を追加[<a href="https://github.com/tikv/tikv/pull/4852">#4852</a>](https://github.com/tikv/tikv/pull/4852)
    -   `ResolveLockLite`コマンドを使用して軽量ロックを解決し、重大な競合が存在する場合のパフォーマンスを向上させるサポート[<a href="https://github.com/tikv/tikv/pull/4882">#4882</a>](https://github.com/tikv/tikv/pull/4882)

-   tikv-ctl
    -   より多くの異常状態のチェックをサポートする`bad-regions`コマンドを追加[<a href="https://github.com/tikv/tikv/pull/4862">#4862</a>](https://github.com/tikv/tikv/pull/4862)
    -   `tombstone`コマンド[<a href="https://github.com/tikv/tikv/pull/4862">#4862</a>](https://github.com/tikv/tikv/pull/4862)を強制実行する機能を追加

-   その他
    -   `dist_release`コンパイルコマンドを追加[<a href="https://github.com/tikv/tikv/pull/4841">#4841</a>](https://github.com/tikv/tikv/pull/4841)

## ツール {#tools}

-   TiDBBinlog
    -   データ[<a href="https://github.com/pingcap/tidb-binlog/pull/640">#640</a>](https://github.com/pingcap/tidb-binlog/pull/640)の書き込みに失敗したときにPumpが戻り値をチェックしないことによって引き起こされる間違ったオフセットの問題を修正しました。
    -   コンテナ環境[<a href="https://github.com/pingcap/tidb-binlog/pull/634">#634</a>](https://github.com/pingcap/tidb-binlog/pull/634)でブリッジ モードをサポートするために、 Drainerに`advertise-addr`構成を追加します。
    -   Pumpに`GetMvccByEncodeKey`関数を追加して、トランザクション ステータスのクエリを高速化します[<a href="https://github.com/pingcap/tidb-binlog/pull/632">#632</a>](https://github.com/pingcap/tidb-binlog/pull/632)

## TiDB Ansible {#tidb-ansible}

-   クラスタの最大QPS値を予測する監視項目を追加（デフォルトは「非表示」） [<a href="https://github.com/pingcap/tidb-ansible/commit/f5cfa4d903bbcd77e01eddc8d31eabb6e6157f73">#f5cfa4d</a>](https://github.com/pingcap/tidb-ansible/commit/f5cfa4d903bbcd77e01eddc8d31eabb6e6157f73)
