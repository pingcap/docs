---
title: TiDB 3.0.0-rc.2 Release Notes
---

# TiDB 3.0.0-rc.2 リリースノート {#tidb-3-0-0-rc-2-release-notes}

発売日：2019年5月28日

TiDB バージョン: 3.0.0-rc.2

TiDB Ansible バージョン: 3.0.0-rc.2

## 概要 {#overview}

2019 年 5 月 28 日に、TiDB 3.0.0-rc.2 がリリースされました。対応する TiDB Ansible バージョンは 3.0.0-rc.2 です。 TiDB 3.0.0-rc.1 と比較して、このリリースでは安定性、使いやすさ、機能、SQL オプティマイザー、統計、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   サポートインデックス 他のシナリオに参加する[#10540](https://github.com/pingcap/tidb/pull/10540)
    -   履歴統計のエクスポートのサポート[#10291](https://github.com/pingcap/tidb/pull/10291)
    -   単調増加するインデックス列[#10355](https://github.com/pingcap/tidb/pull/10355)に対する増分`Analyze`操作をサポートします。
    -   `Order By`節[#10488](https://github.com/pingcap/tidb/pull/10488)の NULL 値を無視します。
    -   列情報[#10384](https://github.com/pingcap/tidb/pull/10384)を簡略化する際の`UnionAll`論理演算子の間違ったスキーマ情報計算を修正しました。
    -   `Not`演算子[#10363](https://github.com/pingcap/tidb/pull/10363/files)を押すときは、元の式を変更しないでください。
    -   ヒストグラム`load` `dump`相関をサポート[#10573](https://github.com/pingcap/tidb/pull/10573)

-   実行エンジン
    -   `batchChecker` [#10370](https://github.com/pingcap/tidb/pull/10370)で重複行をフェッチするときに、一意のインデックスを持つ仮想列を適切に処理する
    -   `CHAR`列[#10124](https://github.com/pingcap/tidb/pull/10124)のスキャン範囲計算の問題を修正
    -   `PointGet`負の数が正しく処理されない問題を修正[#10113](https://github.com/pingcap/tidb/pull/10113)
    -   実行効率を向上させるために、同じ名前の関数`Window`をマージします[#9866](https://github.com/pingcap/tidb/pull/9866)
    -   `Window`関数の`RANGE`フレームに`OrderBy`節[#10496](https://github.com/pingcap/tidb/pull/10496)を含めないようにする

-   サーバ
    -   TiKV [#10301](https://github.com/pingcap/tidb/pull/10301)で障害が発生したときに、TiDB が TiKV への新しい接続を継続的に作成する問題を修正します。
    -   `tidb_disable_txn_auto_retry`書き込み競合エラーのみではなく、すべての再試行可能なエラーに影響させる[#10339](https://github.com/pingcap/tidb/pull/10339)
    -   `prepare` / `execute` [#10144](https://github.com/pingcap/tidb/pull/10144)を使用してパラメータなしの DDL ステートメントを実行できるようにする
    -   バックオフ時間を制御する`tidb_back_off_weight`変数を追加します[#10266](https://github.com/pingcap/tidb/pull/10266)
    -   デフォルト値`tidb_disable_txn_auto_retry` ～ `on` [#10266](https://github.com/pingcap/tidb/pull/10266)設定することで、TiDB がデフォルト条件で非自動的にコミットされたトランザクションを再試行することを禁止します。
    -   `RBAC` [#10261](https://github.com/pingcap/tidb/pull/10261)の`role`というデータベース権限判定を修正
    -   悲観的トランザクション モードのサポート (実験的) [#10297](https://github.com/pingcap/tidb/pull/10297)
    -   場合によっては、ロックの競合を処理するための待ち時間を短縮します[#10006](https://github.com/pingcap/tidb/pull/10006)
    -   リーダー ノード[#10256](https://github.com/pingcap/tidb/pull/10256)で障害が発生したときに、リージョンキャッシュがフォロワー ノードにアクセスできるようにします。
    -   変数`tidb_low_resolution_tso`を追加して、バッチで取得される TSO の数を制御し、データの整合性がそれほど厳密に要求されないシナリオに適応するために TSO を取得するトランザクションの時間を短縮します[#10428](https://github.com/pingcap/tidb/pull/10428)

-   DDL
    -   古いバージョンの TiDB [#10272](https://github.com/pingcap/tidb/pull/10272)のstorage内の文字セット名の大文字の問題を修正
    -   テーブル パーティションのサポート`preSplit`これは、テーブル作成時にテーブル領域を事前に割り当て、テーブル作成後の書き込みホットスポットを回避します[#10221](https://github.com/pingcap/tidb/pull/10221)
    -   TiDB が PD のバージョン情報を誤って更新する場合がある問題を修正[#10324](https://github.com/pingcap/tidb/pull/10324)
    -   `ALTER DATABASE`ステートメント[#10393](https://github.com/pingcap/tidb/pull/10393)を使用した文字セットと照合順序の変更のサポート
    -   ホットスポットの問題を軽減するために、指定されたテーブルのインデックスと範囲に基づいてリージョンの分割をサポートします[#10203](https://github.com/pingcap/tidb/pull/10203)
    -   `alter table`ステートメントを使用して 10 進数列の精度を変更することを禁止します[#10433](https://github.com/pingcap/tidb/pull/10433)
    -   ハッシュ パーティション[#10273](https://github.com/pingcap/tidb/pull/10273)の式と関数の制限を修正
    -   パーティションを含むテーブルにインデックスを追加すると、場合によっては TiDBpanic[#10475](https://github.com/pingcap/tidb/pull/10475)が発生する問題を修正します。
    -   無効なテーブル スキーマを回避するために、DDL を実行する前にテーブル情報を検証します[#10464](https://github.com/pingcap/tidb/pull/10464)
    -   デフォルトでハッシュ パーティションを有効にします。パーティション定義に列が 1 つしかない場合、範囲列パーティションを有効にします[#9936](https://github.com/pingcap/tidb/pull/9936)

## PD {#pd}

-   デフォルトでリージョンstorageを有効にして、リージョンメタデータを保存します[#1524](https://github.com/pingcap/pd/pull/1524)
-   ホットリージョンのスケジューリングが別のスケジューラによってプリエンプトされる問題を修正します[#1522](https://github.com/pingcap/pd/pull/1522)
-   リーダーの優先度が反映されない問題を修正[#1533](https://github.com/pingcap/pd/pull/1533)
-   `ScanRegions` [#1535](https://github.com/pingcap/pd/pull/1535)の gRPC インターフェイスを追加します
-   オペレータを積極的にプッシュする[#1536](https://github.com/pingcap/pd/pull/1536)
-   店舗ごとにオペレーターの速度を個別に制御するための店舗制限メカニズムを追加[#1474](https://github.com/pingcap/pd/pull/1474)
-   `Config`ステータス[#1476](https://github.com/pingcap/pd/pull/1476)が矛盾する問題を修正

## TiKV {#tikv}

-   エンジン
    -   ブロックキャッシュを共有する複数の列ファミリーをサポート[#4563](https://github.com/tikv/tikv/pull/4563)

-   サーバ
    -   `TxnScheduler` [#4098](https://github.com/tikv/tikv/pull/4098)を削除
    -   悲観的ロックトランザクションのサポート[#4698](https://github.com/tikv/tikv/pull/4698)

-   Raftstore
    -   raftstore CPU の消費を削減するための休止状態リージョンのサポート[#4591](https://github.com/tikv/tikv/pull/4591)
    -   リーダーが学習者`ReadIndex`リクエストに応答しない問題を修正[#4653](https://github.com/tikv/tikv/pull/4653)
    -   場合によってはリーダーの転送に失敗する問題を修正[#4684](https://github.com/tikv/tikv/pull/4684)
    -   場合によってはダーティ リードの問題を修正[#4688](https://github.com/tikv/tikv/pull/4688)
    -   スナップショットにより適用されたデータが失われる場合がある問題を修正[#4716](https://github.com/tikv/tikv/pull/4716)

-   コプロセッサー
    -   RPN関数をさらに追加する
        -   `LogicalOr` [#4691](https://github.com/tikv/tikv/pull/4601)
        -   `LTReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        -   `LEReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        -   `GTReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        -   `GEReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        -   `NEReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        -   `EQReal` [#4602](https://github.com/tikv/tikv/pull/4602)
        -   `IsNull` [#4720](https://github.com/tikv/tikv/pull/4720)
        -   `IsTrue` [#4720](https://github.com/tikv/tikv/pull/4720)
        -   `IsFalse` [#4720](https://github.com/tikv/tikv/pull/4720)
        -   `Int` [#4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Decimal` [#4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `String` [#4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Time` [#4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Duration` [#4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Json` [#4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Int` [#4733](https://github.com/tikv/tikv/pull/4733)の算術演算をサポート
        -   `Real` [#4733](https://github.com/tikv/tikv/pull/4733)の算術演算をサポート
        -   `Decimal` [#4733](https://github.com/tikv/tikv/pull/4733)の算術演算をサポート
        -   `Int` [#4727](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Real` [#4727](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Decimal` [#4727](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Int` [#4746](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート
        -   `Real` [#4746](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート
        -   `Decimal` [#4746](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート

## ツール {#tools}

-   TiDBBinlog
    -   データ レプリケーションのダウンストリーム[#594](https://github.com/pingcap/tidb-binlog/pull/594)の遅延を追跡するためのメトリクスを追加します。

-   TiDB Lightning

    -   シャードデータベースとテーブルのマージをサポート[#95](https://github.com/pingcap/tidb-lightning/pull/95)
    -   KV 書き込み失敗に対する再試行メカニズムを追加[#176](https://github.com/pingcap/tidb-lightning/pull/176)
    -   デフォルト値の`table-concurrency`を 6 に更新します[#175](https://github.com/pingcap/tidb-lightning/pull/175)
    -   `tidb.pd-addr`と`tidb.port`が提供されていない場合は自動的に検出することで、必要な構成項目を削減します[#173](https://github.com/pingcap/tidb-lightning/pull/173)
