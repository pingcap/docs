---
title: TiDB 3.0.0-rc.2 Release Notes
summary: TiDB 3.0.0-rc.2は2019年5月28日にリリースされ、安定性、ユーザビリティ、機能、SQLオプティマイザ、統計、実行エンジンが改善されました。このリリースには、SQLオプティマイザ、実行エンジン、サーバー、DDL、PD、TiKV、そしてTiDB BinlogやTiDB Lightningなどのツールの機能強化が含まれています。注目すべき改善点としては、より多くのシナリオでのインデックス結合のサポート、仮想列の適切な処理、下流のデータレプリケーションを追跡するためのメトリックの追加などが挙げられます。
---

# TiDB 3.0.0-rc.2 リリースノート {#tidb-3-0-0-rc-2-release-notes}

発売日：2019年5月28日

TiDB バージョン: 3.0.0-rc.2

TiDB Ansible バージョン: 3.0.0-rc.2

## 概要 {#overview}

2019年5月28日にTiDB 3.0.0-rc.2がリリースされました。対応するTiDB Ansibleバージョンは3.0.0-rc.2です。このリリースでは、TiDB 3.0.0-rc.1と比較して、安定性、使いやすさ、機能、SQLオプティマイザー、統計、実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   サポートインデックス より多くのシナリオに参加[＃10540](https://github.com/pingcap/tidb/pull/10540)
    -   履歴統計のエクスポートをサポート[＃10291](https://github.com/pingcap/tidb/pull/10291)
    -   単調に増加するインデックス列[＃10355](https://github.com/pingcap/tidb/pull/10355)に対する増分`Analyze`操作をサポートする
    -   `Order By`節[＃10488](https://github.com/pingcap/tidb/pull/10488)のNULL値は無視する
    -   列情報[＃10384](https://github.com/pingcap/tidb/pull/10384)を簡素化する際の`UnionAll`論理演算子の誤ったスキーマ情報計算を修正
    -   `Not`演算子[＃10363](https://github.com/pingcap/tidb/pull/10363/files)押し下げるときに元の式を変更しないでください
    -   ヒストグラム[＃10573](https://github.com/pingcap/tidb/pull/10573)の`dump`相関`load`サポート

-   実行エンジン
    -   `batchChecker` [＃10370](https://github.com/pingcap/tidb/pull/10370)で重複行をフェッチするときに、一意のインデックスを持つ仮想列を適切に処理します。
    -   `CHAR`列[＃10124](https://github.com/pingcap/tidb/pull/10124)スキャン範囲計算の問題を修正
    -   `PointGet`負の数を誤って処理する問題を修正[＃10113](https://github.com/pingcap/tidb/pull/10113)
    -   同じ名前の関数を`Window`マージして実行効率を向上させる[＃9866](https://github.com/pingcap/tidb/pull/9866)
    -   `Window`関数の`RANGE`フレームに`OrderBy`節[＃10496](https://github.com/pingcap/tidb/pull/10496)を含めないようにする

-   サーバ
    -   TiKV [＃10301](https://github.com/pingcap/tidb/pull/10301)で障害が発生したときに TiDB が TiKV への新しい接続を継続的に作成する問題を修正しました
    -   `tidb_disable_txn_auto_retry`書き込み競合エラー[＃10339](https://github.com/pingcap/tidb/pull/10339)のみではなく、再試行可能なすべてのエラーに適用する
    -   パラメータなしのDDL文の実行を許可する`prepare` / `execute` [＃10144](https://github.com/pingcap/tidb/pull/10144)
    -   バックオフ時間を制御する変数`tidb_back_off_weight`を追加する[＃10266](https://github.com/pingcap/tidb/pull/10266)
    -   デフォルト値を`tidb_disable_txn_auto_retry`から`on` [＃10266](https://github.com/pingcap/tidb/pull/10266)に設定することで、デフォルト条件で自動的にコミットされていないトランザクションをTiDBが再試行することを禁止します。
    -   `RBAC` [＃10261](https://github.com/pingcap/tidb/pull/10261)分の`role`のデータベース権限判定を修正
    -   悲観的トランザクションモードのサポート（実験的） [＃10297](https://github.com/pingcap/tidb/pull/10297)
    -   いくつかのケースでロック競合の処理の待ち時間を短縮[＃10006](https://github.com/pingcap/tidb/pull/10006)
    -   リーダーノード[＃10256](https://github.com/pingcap/tidb/pull/10256)に障害が発生したときにリージョンキャッシュがフォロワーノードを訪問できるようにする
    -   `tidb_low_resolution_tso`変数を追加して、バッチで取得されるTSOの数を制御し、TSOを取得するトランザクションの回数を減らし、データの一貫性がそれほど厳密に要求されないシナリオに適応します[＃10428](https://github.com/pingcap/tidb/pull/10428)

-   DDL
    -   TiDB [＃10272](https://github.com/pingcap/tidb/pull/10272)の旧バージョンのstorage内の文字セット名の大文字の問題を修正しました
    -   テーブル作成時にテーブル領域を事前割り当てして、 [＃10221](https://github.com/pingcap/tidb/pull/10221)作成後の書き込みホットスポットを回避するテーブルパーティションのサポート`preSplit`
    -   TiDBがPDのバージョン情報を誤って更新する場合がある問題を修正[＃10324](https://github.com/pingcap/tidb/pull/10324)
    -   `ALTER DATABASE`文[＃10393](https://github.com/pingcap/tidb/pull/10393)を使用して文字セットと照合順序を変更することをサポートします
    -   ホットスポットの問題を軽減するために、指定されたテーブルのインデックスと範囲に基づいて領域を分割することをサポートします[＃10203](https://github.com/pingcap/tidb/pull/10203)
    -   `alter table`文[＃10433](https://github.com/pingcap/tidb/pull/10433)を使用して小数列の精度を変更することを禁止します。
    -   ハッシュパーティション[＃10273](https://github.com/pingcap/tidb/pull/10273)式と関数の制限を修正
    -   パーティションを含むテーブルにインデックスを追加すると、場合によっては TiDBpanicが発生する問題を修正しました[＃10475](https://github.com/pingcap/tidb/pull/10475)
    -   無効なテーブルスキーマを回避するために、DDLを実行する前にテーブル情報を検証します[＃10464](https://github.com/pingcap/tidb/pull/10464)
    -   デフォルトでハッシュパーティションを有効にし、パーティション定義に列が1つしかない場合は範囲列パーティションを有効にします[＃9936](https://github.com/pingcap/tidb/pull/9936)

## PD {#pd}

-   リージョンメタデータを保存するために、デフォルトでリージョンstorageを有効にします[＃1524](https://github.com/pingcap/pd/pull/1524)
-   ホットリージョンのスケジューリングが別のスケジューラによって優先される問題を修正[＃1522](https://github.com/pingcap/pd/pull/1522)
-   リーダーの優先順位が有効にならない問題を修正[＃1533](https://github.com/pingcap/pd/pull/1533)
-   `ScanRegions` [＃1535](https://github.com/pingcap/pd/pull/1535)の gRPC インターフェースを追加する
-   プッシュ演算子をアクティブにする[＃1536](https://github.com/pingcap/pd/pull/1536)
-   各店舗ごとにオペレーターの速度を個別に制御するための店舗制限機構を追加[＃1474](https://github.com/pingcap/pd/pull/1474)
-   不一致の`Config`ステータス[＃1476](https://github.com/pingcap/pd/pull/1476)の問題を修正

## TiKV {#tikv}

-   エンジン
    -   ブロックキャッシュを共有する複数の列ファミリをサポート[＃4563](https://github.com/tikv/tikv/pull/4563)

-   サーバ
    -   `TxnScheduler` [＃4098](https://github.com/tikv/tikv/pull/4098)を削除
    -   悲観的ロックトランザクションをサポート[＃4698](https://github.com/tikv/tikv/pull/4698)

-   Raftstore
    -   ラフトストアCPUの消費を減らすために休止状態領域をサポートする[＃4591](https://github.com/tikv/tikv/pull/4591)
    -   リーダーが学習者[＃4653](https://github.com/tikv/tikv/pull/4653) `ReadIndex`リクエストに返信しない問題を修正
    -   一部のケースでリーダーの転送に失敗する問題を修正[＃4684](https://github.com/tikv/tikv/pull/4684)
    -   いくつかのケースでダーティリードの問題を修正[＃4688](https://github.com/tikv/tikv/pull/4688)
    -   スナップショットで適用されたデータが失われる場合がある問題を修正[＃4716](https://github.com/tikv/tikv/pull/4716)

-   コプロセッサー
    -   RPN関数を追加する
        -   `LogicalOr` [＃4691](https://github.com/tikv/tikv/pull/4601)
        -   `LTReal` [＃4602](https://github.com/tikv/tikv/pull/4602)
        -   `LEReal` [＃4602](https://github.com/tikv/tikv/pull/4602)
        -   `GTReal` [＃4602](https://github.com/tikv/tikv/pull/4602)
        -   `GEReal` [＃4602](https://github.com/tikv/tikv/pull/4602)
        -   `NEReal` [＃4602](https://github.com/tikv/tikv/pull/4602)
        -   `EQReal` [＃4602](https://github.com/tikv/tikv/pull/4602)
        -   `IsNull` [＃4720](https://github.com/tikv/tikv/pull/4720)
        -   `IsTrue` [＃4720](https://github.com/tikv/tikv/pull/4720)
        -   `IsFalse` [＃4720](https://github.com/tikv/tikv/pull/4720)
        -   `Int` [＃4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Decimal` [＃4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `String` [＃4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Time` [＃4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Duration` [＃4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Json` [＃4625](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Int` [＃4733](https://github.com/tikv/tikv/pull/4733)のサポートプラス算術
        -   `Real` [＃4733](https://github.com/tikv/tikv/pull/4733)のサポートプラス算術
        -   `Decimal` [＃4733](https://github.com/tikv/tikv/pull/4733)のサポートプラス算術
        -   `Int` [＃4727](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Real` [＃4727](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Decimal` [＃4727](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Int` [＃4746](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート
        -   `Real` [＃4746](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート
        -   `Decimal` [＃4746](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート

## ツール {#tools}

-   TiDBBinlog
    -   データレプリケーション下流の遅延を追跡するためのメトリックを追加する[＃594](https://github.com/pingcap/tidb-binlog/pull/594)

-   TiDB Lightning

    -   シャードデータベースとテーブルのマージをサポート[＃95](https://github.com/pingcap/tidb-lightning/pull/95)
    -   KV書き込み失敗[＃176](https://github.com/pingcap/tidb-lightning/pull/176)再試行メカニズムを追加
    -   デフォルト値`table-concurrency`を6 [＃175](https://github.com/pingcap/tidb-lightning/pull/175)に更新
    -   `tidb.pd-addr`と`tidb.port`提供されていない場合は自動的に検出して必要な構成項目を削減します[＃173](https://github.com/pingcap/tidb-lightning/pull/173)
