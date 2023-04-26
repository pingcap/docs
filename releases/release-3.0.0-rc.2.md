---
title: TiDB 3.0.0-rc.2 Release Notes
---

# TiDB 3.0.0-rc.2 リリースノート {#tidb-3-0-0-rc-2-release-notes}

発売日：2019年5月28日

TiDB バージョン: 3.0.0-rc.2

TiDB アンシブル バージョン: 3.0.0-rc.2

## 概要 {#overview}

2019 年 5 月 28 日に、TiDB 3.0.0-rc.2 がリリースされました。対応する TiDB Ansible のバージョンは 3.0.0-rc.2 です。 TiDB 3.0.0-rc.1 と比較して、このリリースでは、安定性、使いやすさ、機能、SQL オプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー
    -   より多くのシナリオで Index Join をサポート[#10540](https://github.com/pingcap/tidb/pull/10540)
    -   履歴統計のエクスポートをサポート[#10291](https://github.com/pingcap/tidb/pull/10291)
    -   単調に増加するインデックス列[#10355](https://github.com/pingcap/tidb/pull/10355)での増分`Analyze`操作をサポートします
    -   `Order By`節[#10488](https://github.com/pingcap/tidb/pull/10488)の NULL 値を無視する
    -   列情報を簡略化する際に`UnionAll`論理演算子の間違ったスキーマ情報計算を修正[#10384](https://github.com/pingcap/tidb/pull/10384)
    -   `Not`演算子[#10363](https://github.com/pingcap/tidb/pull/10363/files)を押し下げるときは、元の式を変更しないでください
    -   ヒストグラム`load` `dump`相関をサポート[#10573](https://github.com/pingcap/tidb/pull/10573)

-   実行エンジン
    -   `batchChecker` [#10370](https://github.com/pingcap/tidb/pull/10370)で重複する行をフェッチするときに、一意のインデックスを持つ仮想列を適切に処理する
    -   `CHAR`列[#10124](https://github.com/pingcap/tidb/pull/10124)のスキャン範囲計算の問題を修正
    -   `PointGet`が負の数を誤って処理する問題を修正[#10113](https://github.com/pingcap/tidb/pull/10113)
    -   `Window`同名の関数をマージして実行効率を上げる[#9866](https://github.com/pingcap/tidb/pull/9866)
    -   `Window`関数の`RANGE`フレームに`OrderBy`節[#10496](https://github.com/pingcap/tidb/pull/10496)が含まれないようにする

-   サーバ
    -   TiKV [#10301](https://github.com/pingcap/tidb/pull/10301)で障害が発生した場合、TiDB が TiKV への新しい接続を継続的に作成する問題を修正します。
    -   書き込み競合エラー[#10339](https://github.com/pingcap/tidb/pull/10339)だけではなく、 `tidb_disable_txn_auto_retry`すべての再試行可能なエラーに影響を与えるようにします。
    -   `prepare` / `execute` [#10144](https://github.com/pingcap/tidb/pull/10144)を使用して、パラメーターのない DDL ステートメントの実行を許可する
    -   `tidb_back_off_weight`変数を追加して、バックオフ時間を制御します[#10266](https://github.com/pingcap/tidb/pull/10266)
    -   デフォルト値を`tidb_disable_txn_auto_retry`から`on` [#10266](https://github.com/pingcap/tidb/pull/10266)に設定することにより、TiDB がデフォルト条件で自動コミットされていないトランザクションを再試行することを禁止する
    -   `RBAC` [#10261](https://github.com/pingcap/tidb/pull/10261)に`role`のデータベース権限判定を修正
    -   悲観的トランザクション モードのサポート (実験的) [#10297](https://github.com/pingcap/tidb/pull/10297)
    -   場合によっては、ロックの競合を処理するための待機時間を短縮します[#10006](https://github.com/pingcap/tidb/pull/10006)
    -   リーダーノードで障害が発生したときにリージョンキャッシュがフォロワーノードを訪問できるようにする[#10256](https://github.com/pingcap/tidb/pull/10256)
    -   `tidb_low_resolution_tso`変数を追加して、バッチで取得される TSO の数を制御し、TSO を取得するトランザクションの時間を短縮して、データの一貫性がそれほど厳密に必要とされないシナリオに適応します[#10428](https://github.com/pingcap/tidb/pull/10428)

-   DDL
    -   古いバージョンの TiDB [#10272](https://github.com/pingcap/tidb/pull/10272)のstorage内の文字セット名の大文字の問題を修正します。
    -   テーブルの作成後に書き込みホットスポットを回避するために、テーブルの作成時にテーブル リージョンを事前に割り当てるテーブル パーティションのサポート`preSplit` [#10221](https://github.com/pingcap/tidb/pull/10221)
    -   TiDB が PD のバージョン情報を誤って更新することがある問題を修正[#10324](https://github.com/pingcap/tidb/pull/10324)
    -   `ALTER DATABASE`ステートメント[#10393](https://github.com/pingcap/tidb/pull/10393)を使用した文字セットと照合順序の変更をサポート
    -   ホットスポットの問題を緩和するために、指定されたテーブルのインデックスと範囲に基づいてリージョンを分割することをサポートします[#10203](https://github.com/pingcap/tidb/pull/10203)
    -   `alter table`ステートメント[#10433](https://github.com/pingcap/tidb/pull/10433)を使用した 10 進列の精度の変更を禁止する
    -   ハッシュ パーティション[#10273](https://github.com/pingcap/tidb/pull/10273)の式と関数の制限を修正します。
    -   パーティションを含むテーブルにインデックスを追加すると、場合によっては TiDBpanic[#10475](https://github.com/pingcap/tidb/pull/10475)が発生する問題を修正します
    -   無効なテーブル スキーマを回避するために、DDL を実行する前にテーブル情報を検証する[#10464](https://github.com/pingcap/tidb/pull/10464)
    -   デフォルトでハッシュ パーティションを有効にします。パーティション定義[#9936](https://github.com/pingcap/tidb/pull/9936)に列が 1 つしかない場合は、範囲列パーティションを有効にします。

## PD {#pd}

-   デフォルトでリージョンstorageを有効にして、リージョンメタデータを保存します[#1524](https://github.com/pingcap/pd/pull/1524)
-   ホットリージョンスケジューリングが別のスケジューラによってプリエンプトされる問題を修正します[#1522](https://github.com/pingcap/pd/pull/1522)
-   リーダーの優先度が反映されない問題を修正[#1533](https://github.com/pingcap/pd/pull/1533)
-   `ScanRegions` [#1535](https://github.com/pingcap/pd/pull/1535)の gRPC インターフェイスを追加する
-   オペレータを積極的にプッシュ[#1536](https://github.com/pingcap/pd/pull/1536)
-   店舗ごとにオペレーターの速度を個別に制御するための店舗制限メカニズムを追加します[#1474](https://github.com/pingcap/pd/pull/1474)
-   一貫性のない`Config`ステータス[#1476](https://github.com/pingcap/pd/pull/1476)の問題を修正

## TiKV {#tikv}

-   エンジン
    -   ブロックキャッシュを共有する複数の列ファミリーをサポート[#4563](https://github.com/tikv/tikv/pull/4563)

-   サーバ
    -   削除`TxnScheduler` [#4098](https://github.com/tikv/tikv/pull/4098)
    -   悲観的ロック トランザクションのサポート[#4698](https://github.com/tikv/tikv/pull/4698)

-   Raftstore
    -   raftstore CPU [#4591](https://github.com/tikv/tikv/pull/4591)の消費を削減するための休止状態リージョンのサポート
    -   リーダーが学習者の`ReadIndex`要求に応答しない問題を修正[#4653](https://github.com/tikv/tikv/pull/4653)
    -   場合によってはリーダーの転送に失敗する問題を修正[#4684](https://github.com/tikv/tikv/pull/4684)
    -   場合によってはダーティ リードの問題を修正します[#4688](https://github.com/tikv/tikv/pull/4688)
    -   場合によってはスナップショットが適用されたデータを失う可能性がある問題を修正します[#4716](https://github.com/tikv/tikv/pull/4716)

-   コプロセッサー
    -   RPN関数を追加
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
        -   `Int` [#4733](https://github.com/tikv/tikv/pull/4733)のプラス算術をサポート
        -   `Real` [#4733](https://github.com/tikv/tikv/pull/4733)のプラス算術をサポート
        -   `Decimal` [#4733](https://github.com/tikv/tikv/pull/4733)のプラス算術をサポート
        -   `Int` [#4727](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Real` [#4727](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Decimal` [#4727](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Int` [#4746](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート
        -   `Real` [#4746](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート
        -   `Decimal` [#4746](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート

## ツール {#tools}

-   TiDBBinlog
    -   メトリクスを追加して、ダウンストリーム[#594](https://github.com/pingcap/tidb-binlog/pull/594)のデータ レプリケーションの遅延を追跡します

-   TiDB Lightning

    -   シャードされたデータベースとテーブルのマージをサポート[#95](https://github.com/pingcap/tidb-lightning/pull/95)
    -   KV 書き込み失敗[#176](https://github.com/pingcap/tidb-lightning/pull/176)のリトライ メカニズムを追加します。
    -   デフォルト値の`table-concurrency`を 6 [#175](https://github.com/pingcap/tidb-lightning/pull/175)に更新します
    -   `tidb.pd-addr`と`tidb.port`が提供されていない場合は、それらを自動的に検出して必要な構成項目を削減します[#173](https://github.com/pingcap/tidb-lightning/pull/173)
