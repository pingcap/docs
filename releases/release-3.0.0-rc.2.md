---
title: TiDB 3.0.0-rc.2 Release Notes
---

# TiDB 3.0.0-rc.2 リリースノート {#tidb-3-0-0-rc-2-release-notes}

発売日：2019年5月28日

TiDB バージョン: 3.0.0-rc.2

TiDB Ansible バージョン: 3.0.0-rc.2

## 概要 {#overview}

2019 年 5 月 28 日に、TiDB 3.0.0-rc.2 がリリースされました。対応する TiDB Ansible バージョンは 3.0.0-rc.2 です。 TiDB 3.0.0-rc.1 と比較して、このリリースでは安定性、使いやすさ、機能、SQL オプティマイザー、統計、実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   サポートインデックス 他のシナリオに参加する[<a href="https://github.com/pingcap/tidb/pull/10540">#10540</a>](https://github.com/pingcap/tidb/pull/10540)
    -   履歴統計のエクスポートのサポート[<a href="https://github.com/pingcap/tidb/pull/10291">#10291</a>](https://github.com/pingcap/tidb/pull/10291)
    -   単調増加するインデックス列[<a href="https://github.com/pingcap/tidb/pull/10355">#10355</a>](https://github.com/pingcap/tidb/pull/10355)に対する増分`Analyze`操作をサポートします。
    -   `Order By`節[<a href="https://github.com/pingcap/tidb/pull/10488">#10488</a>](https://github.com/pingcap/tidb/pull/10488)の NULL 値を無視します。
    -   列情報[<a href="https://github.com/pingcap/tidb/pull/10384">#10384</a>](https://github.com/pingcap/tidb/pull/10384)を簡略化する際の`UnionAll`論理演算子の間違ったスキーマ情報計算を修正しました。
    -   `Not`演算子[<a href="https://github.com/pingcap/tidb/pull/10363/files">#10363</a>](https://github.com/pingcap/tidb/pull/10363/files)を押すときは、元の式を変更しないでください。
    -   ヒストグラム`load` `dump`相関をサポート[<a href="https://github.com/pingcap/tidb/pull/10573">#10573</a>](https://github.com/pingcap/tidb/pull/10573)

-   実行エンジン
    -   `batchChecker` [<a href="https://github.com/pingcap/tidb/pull/10370">#10370</a>](https://github.com/pingcap/tidb/pull/10370)で重複行をフェッチするときに、一意のインデックスを持つ仮想列を適切に処理する
    -   `CHAR`列[<a href="https://github.com/pingcap/tidb/pull/10124">#10124</a>](https://github.com/pingcap/tidb/pull/10124)のスキャン範囲計算の問題を修正
    -   `PointGet`負の数が正しく処理されない問題を修正[<a href="https://github.com/pingcap/tidb/pull/10113">#10113</a>](https://github.com/pingcap/tidb/pull/10113)
    -   実行効率を向上させるために、同じ名前の関数`Window`をマージします[<a href="https://github.com/pingcap/tidb/pull/9866">#9866</a>](https://github.com/pingcap/tidb/pull/9866)
    -   `Window`関数の`RANGE`フレームに`OrderBy`節[<a href="https://github.com/pingcap/tidb/pull/10496">#10496</a>](https://github.com/pingcap/tidb/pull/10496)を含めないようにする

-   サーバ
    -   TiKV [<a href="https://github.com/pingcap/tidb/pull/10301">#10301</a>](https://github.com/pingcap/tidb/pull/10301)で障害が発生したときに、TiDB が TiKV への新しい接続を継続的に作成する問題を修正します。
    -   `tidb_disable_txn_auto_retry`書き込み競合エラーのみではなく、すべての再試行可能なエラーに影響させる[<a href="https://github.com/pingcap/tidb/pull/10339">#10339</a>](https://github.com/pingcap/tidb/pull/10339)
    -   `prepare` / `execute` [<a href="https://github.com/pingcap/tidb/pull/10144">#10144</a>](https://github.com/pingcap/tidb/pull/10144)を使用してパラメータなしの DDL ステートメントを実行できるようにする
    -   バックオフ時間を制御する`tidb_back_off_weight`変数を追加します[<a href="https://github.com/pingcap/tidb/pull/10266">#10266</a>](https://github.com/pingcap/tidb/pull/10266)
    -   デフォルト値`tidb_disable_txn_auto_retry` ～ `on` [<a href="https://github.com/pingcap/tidb/pull/10266">#10266</a>](https://github.com/pingcap/tidb/pull/10266)設定することで、TiDB がデフォルト条件で非自動的にコミットされたトランザクションを再試行することを禁止します。
    -   `RBAC` [<a href="https://github.com/pingcap/tidb/pull/10261">#10261</a>](https://github.com/pingcap/tidb/pull/10261)の`role`というデータベース権限判定を修正
    -   悲観的トランザクション モードのサポート (実験的) [<a href="https://github.com/pingcap/tidb/pull/10297">#10297</a>](https://github.com/pingcap/tidb/pull/10297)
    -   場合によっては、ロックの競合を処理するための待ち時間を短縮します[<a href="https://github.com/pingcap/tidb/pull/10006">#10006</a>](https://github.com/pingcap/tidb/pull/10006)
    -   リーダー ノード[<a href="https://github.com/pingcap/tidb/pull/10256">#10256</a>](https://github.com/pingcap/tidb/pull/10256)で障害が発生したときに、リージョンキャッシュがフォロワー ノードにアクセスできるようにします。
    -   `tidb_low_resolution_tso`変数を追加して、バッチで取得される TSO の数を制御し、データの整合性がそれほど厳密に要求されないシナリオに適応するために TSO を取得するトランザクションの時間を短縮します[<a href="https://github.com/pingcap/tidb/pull/10428">#10428</a>](https://github.com/pingcap/tidb/pull/10428)

-   DDL
    -   古いバージョンの TiDB [<a href="https://github.com/pingcap/tidb/pull/10272">#10272</a>](https://github.com/pingcap/tidb/pull/10272)のstorage内の文字セット名の大文字の問題を修正
    -   テーブル パーティションのサポート`preSplit`これは、テーブル作成時にテーブル領域を事前に割り当て、テーブル作成後の書き込みホットスポットを回避します[<a href="https://github.com/pingcap/tidb/pull/10221">#10221</a>](https://github.com/pingcap/tidb/pull/10221)
    -   TiDB が PD のバージョン情報を誤って更新する場合がある問題を修正[<a href="https://github.com/pingcap/tidb/pull/10324">#10324</a>](https://github.com/pingcap/tidb/pull/10324)
    -   `ALTER DATABASE`ステートメント[<a href="https://github.com/pingcap/tidb/pull/10393">#10393</a>](https://github.com/pingcap/tidb/pull/10393)を使用した文字セットと照合順序の変更のサポート
    -   ホットスポットの問題を軽減するために、指定されたテーブルのインデックスと範囲に基づいてリージョンの分割をサポートします[<a href="https://github.com/pingcap/tidb/pull/10203">#10203</a>](https://github.com/pingcap/tidb/pull/10203)
    -   `alter table`ステートメントを使用して 10 進数列の精度を変更することを禁止します[<a href="https://github.com/pingcap/tidb/pull/10433">#10433</a>](https://github.com/pingcap/tidb/pull/10433)
    -   ハッシュ パーティション[<a href="https://github.com/pingcap/tidb/pull/10273">#10273</a>](https://github.com/pingcap/tidb/pull/10273)の式と関数の制限を修正
    -   パーティションを含むテーブルにインデックスを追加すると、場合によっては TiDBpanic[<a href="https://github.com/pingcap/tidb/pull/10475">#10475</a>](https://github.com/pingcap/tidb/pull/10475)が発生する問題を修正します。
    -   無効なテーブル スキーマを回避するために、DDL を実行する前にテーブル情報を検証します[<a href="https://github.com/pingcap/tidb/pull/10464">#10464</a>](https://github.com/pingcap/tidb/pull/10464)
    -   デフォルトでハッシュ パーティションを有効にします。パーティション定義に列が 1 つしかない場合、範囲列パーティションを有効にします[<a href="https://github.com/pingcap/tidb/pull/9936">#9936</a>](https://github.com/pingcap/tidb/pull/9936)

## PD {#pd}

-   デフォルトでリージョンstorageを有効にして、リージョンメタデータを保存します[<a href="https://github.com/pingcap/pd/pull/1524">#1524</a>](https://github.com/pingcap/pd/pull/1524)
-   ホットリージョンのスケジューリングが別のスケジューラによってプリエンプトされる問題を修正します[<a href="https://github.com/pingcap/pd/pull/1522">#1522</a>](https://github.com/pingcap/pd/pull/1522)
-   リーダーの優先度が反映されない問題を修正[<a href="https://github.com/pingcap/pd/pull/1533">#1533</a>](https://github.com/pingcap/pd/pull/1533)
-   `ScanRegions` [<a href="https://github.com/pingcap/pd/pull/1535">#1535</a>](https://github.com/pingcap/pd/pull/1535)の gRPC インターフェイスを追加します
-   オペレータを積極的にプッシュする[<a href="https://github.com/pingcap/pd/pull/1536">#1536</a>](https://github.com/pingcap/pd/pull/1536)
-   店舗ごとにオペレーターの速度を個別に制御するための店舗制限メカニズムを追加[<a href="https://github.com/pingcap/pd/pull/1474">#1474</a>](https://github.com/pingcap/pd/pull/1474)
-   `Config`ステータス[<a href="https://github.com/pingcap/pd/pull/1476">#1476</a>](https://github.com/pingcap/pd/pull/1476)が矛盾する問題を修正

## TiKV {#tikv}

-   エンジン
    -   ブロックキャッシュを共有する複数の列ファミリーをサポート[<a href="https://github.com/tikv/tikv/pull/4563">#4563</a>](https://github.com/tikv/tikv/pull/4563)

-   サーバ
    -   `TxnScheduler` [<a href="https://github.com/tikv/tikv/pull/4098">#4098</a>](https://github.com/tikv/tikv/pull/4098)を削除
    -   悲観的ロックトランザクションのサポート[<a href="https://github.com/tikv/tikv/pull/4698">#4698</a>](https://github.com/tikv/tikv/pull/4698)

-   Raftstore
    -   raftstore CPU の消費を削減するための休止状態リージョンのサポート[<a href="https://github.com/tikv/tikv/pull/4591">#4591</a>](https://github.com/tikv/tikv/pull/4591)
    -   リーダーが学習者`ReadIndex`リクエストに応答しない問題を修正[<a href="https://github.com/tikv/tikv/pull/4653">#4653</a>](https://github.com/tikv/tikv/pull/4653)
    -   場合によってはリーダーの転送に失敗する問題を修正[<a href="https://github.com/tikv/tikv/pull/4684">#4684</a>](https://github.com/tikv/tikv/pull/4684)
    -   場合によってはダーティ リードの問題を修正[<a href="https://github.com/tikv/tikv/pull/4688">#4688</a>](https://github.com/tikv/tikv/pull/4688)
    -   スナップショットにより適用されたデータが失われる場合がある問題を修正[<a href="https://github.com/tikv/tikv/pull/4716">#4716</a>](https://github.com/tikv/tikv/pull/4716)

-   コプロセッサー
    -   RPN関数をさらに追加する
        -   `LogicalOr` [<a href="https://github.com/tikv/tikv/pull/4601">#4691</a>](https://github.com/tikv/tikv/pull/4601)
        -   `LTReal` [<a href="https://github.com/tikv/tikv/pull/4602">#4602</a>](https://github.com/tikv/tikv/pull/4602)
        -   `LEReal` [<a href="https://github.com/tikv/tikv/pull/4602">#4602</a>](https://github.com/tikv/tikv/pull/4602)
        -   `GTReal` [<a href="https://github.com/tikv/tikv/pull/4602">#4602</a>](https://github.com/tikv/tikv/pull/4602)
        -   `GEReal` [<a href="https://github.com/tikv/tikv/pull/4602">#4602</a>](https://github.com/tikv/tikv/pull/4602)
        -   `NEReal` [<a href="https://github.com/tikv/tikv/pull/4602">#4602</a>](https://github.com/tikv/tikv/pull/4602)
        -   `EQReal` [<a href="https://github.com/tikv/tikv/pull/4602">#4602</a>](https://github.com/tikv/tikv/pull/4602)
        -   `IsNull` [<a href="https://github.com/tikv/tikv/pull/4720">#4720</a>](https://github.com/tikv/tikv/pull/4720)
        -   `IsTrue` [<a href="https://github.com/tikv/tikv/pull/4720">#4720</a>](https://github.com/tikv/tikv/pull/4720)
        -   `IsFalse` [<a href="https://github.com/tikv/tikv/pull/4720">#4720</a>](https://github.com/tikv/tikv/pull/4720)
        -   `Int` [<a href="https://github.com/tikv/tikv/pull/4625">#4625</a>](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Decimal` [<a href="https://github.com/tikv/tikv/pull/4625">#4625</a>](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `String` [<a href="https://github.com/tikv/tikv/pull/4625">#4625</a>](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Time` [<a href="https://github.com/tikv/tikv/pull/4625">#4625</a>](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Duration` [<a href="https://github.com/tikv/tikv/pull/4625">#4625</a>](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Json` [<a href="https://github.com/tikv/tikv/pull/4625">#4625</a>](https://github.com/tikv/tikv/pull/4625)の比較演算をサポート
        -   `Int` [<a href="https://github.com/tikv/tikv/pull/4733">#4733</a>](https://github.com/tikv/tikv/pull/4733)の算術演算をサポート
        -   `Real` [<a href="https://github.com/tikv/tikv/pull/4733">#4733</a>](https://github.com/tikv/tikv/pull/4733)の算術演算をサポート
        -   `Decimal` [<a href="https://github.com/tikv/tikv/pull/4733">#4733</a>](https://github.com/tikv/tikv/pull/4733)の算術演算をサポート
        -   `Int` [<a href="https://github.com/tikv/tikv/pull/4727">#4727</a>](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Real` [<a href="https://github.com/tikv/tikv/pull/4727">#4727</a>](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Decimal` [<a href="https://github.com/tikv/tikv/pull/4727">#4727</a>](https://github.com/tikv/tikv/pull/4727)のMOD関数をサポート
        -   `Int` [<a href="https://github.com/tikv/tikv/pull/4746">#4746</a>](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート
        -   `Real` [<a href="https://github.com/tikv/tikv/pull/4746">#4746</a>](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート
        -   `Decimal` [<a href="https://github.com/tikv/tikv/pull/4746">#4746</a>](https://github.com/tikv/tikv/pull/4746)のマイナス演算をサポート

## ツール {#tools}

-   TiDBBinlog
    -   データ レプリケーションのダウンストリーム[<a href="https://github.com/pingcap/tidb-binlog/pull/594">#594</a>](https://github.com/pingcap/tidb-binlog/pull/594)の遅延を追跡するためのメトリクスを追加します。

-   TiDB Lightning

    -   シャードデータベースとテーブルのマージをサポート[<a href="https://github.com/pingcap/tidb-lightning/pull/95">#95</a>](https://github.com/pingcap/tidb-lightning/pull/95)
    -   KV 書き込み失敗に対する再試行メカニズムを追加[<a href="https://github.com/pingcap/tidb-lightning/pull/176">#176</a>](https://github.com/pingcap/tidb-lightning/pull/176)
    -   デフォルト値の`table-concurrency`を 6 に更新します[<a href="https://github.com/pingcap/tidb-lightning/pull/175">#175</a>](https://github.com/pingcap/tidb-lightning/pull/175)
    -   `tidb.pd-addr`と`tidb.port`が提供されていない場合は自動的に検出することで、必要な構成項目を削減します[<a href="https://github.com/pingcap/tidb-lightning/pull/173">#173</a>](https://github.com/pingcap/tidb-lightning/pull/173)
