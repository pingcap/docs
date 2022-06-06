---
title: TiDB 3.0.0-rc.2 Release Notes
---

# TiDB3.0.0-rc.2リリースノート {#tidb-3-0-0-rc-2-release-notes}

発売日：2019年5月28日

TiDBバージョン：3.0.0-rc.2

TiDB Ansibleバージョン：3.0.0-rc.2

## 概要 {#overview}

2019年5月28日、TiDB3.0.0-rc.2がリリースされました。対応するTiDBAnsibleのバージョンは3.0.0-rc.2です。このリリースでは、TiDB 3.0.0-rc.1と比較して、安定性、使いやすさ、機能、SQLオプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   より多くのシナリオに参加するインデックスをサポートする[＃10540](https://github.com/pingcap/tidb/pull/10540)
    -   履歴統計のエクスポートをサポート[＃10291](https://github.com/pingcap/tidb/pull/10291)
    -   単調に増加するインデックス列[＃10355](https://github.com/pingcap/tidb/pull/10355)でインクリメンタル`Analyze`操作をサポートします。
    -   `Order By`節[＃10488](https://github.com/pingcap/tidb/pull/10488)のNULL値を無視します
    -   列情報を単純化するときの`UnionAll`論理演算子の誤ったスキーマ情報計算を修正します[＃10384](https://github.com/pingcap/tidb/pull/10384)
    -   `Not`演算子[＃10363](https://github.com/pingcap/tidb/pull/10363/files)を押し下げるときは、元の式を変更しないでください。
    -   ヒストグラムの`dump`相関を[＃10573](https://github.com/pingcap/tidb/pull/10573) `load`

-   実行エンジン
    -   `batchChecker` [＃10370](https://github.com/pingcap/tidb/pull/10370)で重複する行をフェッチするときに、一意のインデックスを持つ仮想列を適切に処理する
    -   `CHAR`列[＃10124](https://github.com/pingcap/tidb/pull/10124)のスキャン範囲計算の問題を修正しました
    -   `PointGet`が負の数を誤って処理する問題を修正します[＃10113](https://github.com/pingcap/tidb/pull/10113)
    -   同じ名前の`Window`の関数をマージして、実行効率を向上させます[＃9866](https://github.com/pingcap/tidb/pull/9866)
    -   `Window`関数の`RANGE`フレームに`OrderBy`節[＃10496](https://github.com/pingcap/tidb/pull/10496)が含まれないようにする

-   サーバ
    -   TiKV [＃10301](https://github.com/pingcap/tidb/pull/10301)で障害が発生したときに、TiDBがTiKVへの新しい接続を継続的に作成する問題を修正します。
    -   書き込み競合エラーだけでなく、 `tidb_disable_txn_auto_retry`をすべての再試行可能なエラーに影響させる[＃10339](https://github.com/pingcap/tidb/pull/10339)
    -   パラメータなしの`execute` [＃10144](https://github.com/pingcap/tidb/pull/10144)を`prepare`を使用して実行できるようにする
    -   `tidb_back_off_weight`変数を追加して、バックオフ時間を制御します[＃10266](https://github.com/pingcap/tidb/pull/10266)
    -   デフォルト値の`tidb_disable_txn_auto_retry`から35を設定することにより、 `on`がデフォルト条件で自動コミットされていないトランザクションを再試行することを禁止し[＃10266](https://github.com/pingcap/tidb/pull/10266) 。
    -   `RBAC`分の`role`のデータベース特権判断を修正[＃10261](https://github.com/pingcap/tidb/pull/10261)
    -   悲観的なトランザクションモードをサポートする（実験的） [＃10297](https://github.com/pingcap/tidb/pull/10297)
    -   場合によっては、ロックの競合を処理するための待機時間を短縮します[＃10006](https://github.com/pingcap/tidb/pull/10006)
    -   リーダーノード[＃10256](https://github.com/pingcap/tidb/pull/10256)で障害が発生したときに、リージョンキャッシュがフォロワーノードにアクセスできるようにします。
    -   `tidb_low_resolution_tso`変数を追加して、バッチで取得されるTSOの数を制御し、TSOを取得するトランザクションの時間を短縮して、データの一貫性がそれほど厳密に要求されないシナリオに適応させます[＃10428](https://github.com/pingcap/tidb/pull/10428)

-   DDL
    -   古いバージョンの[＃10272](https://github.com/pingcap/tidb/pull/10272)のストレージにある文字セット名の大文字の問題を修正しました
    -   テーブルパーティションの`preSplit`をサポートします。これは、テーブルの作成時にテーブルリージョンを事前に割り当てて、テーブルの作成後にホットスポットを書き込まないようにします[＃10221](https://github.com/pingcap/tidb/pull/10221)
    -   TiDBがPDのバージョン情報を誤って更新する場合がある問題を修正します[＃10324](https://github.com/pingcap/tidb/pull/10324)
    -   `ALTER DATABASE`ステートメント[＃10393](https://github.com/pingcap/tidb/pull/10393)を使用した文字セットと照合順序の変更をサポートします。
    -   ホットスポットの問題を軽減するために、指定されたテーブルのインデックスと範囲に基づいてリージョンを分割することをサポートします[＃10203](https://github.com/pingcap/tidb/pull/10203)
    -   `alter table`ステートメントを使用して10進列の精度を変更することを禁止する[＃10433](https://github.com/pingcap/tidb/pull/10433)
    -   ハッシュパーティション[＃10273](https://github.com/pingcap/tidb/pull/10273)の式と関数の制限を修正しました
    -   パーティションを含むテーブルにインデックスを追加すると、場合によってはTiDBパニックが発生する問題を修正します[＃10475](https://github.com/pingcap/tidb/pull/10475)
    -   無効なテーブルスキーマを回避するために、DDLを実行する前にテーブル情報を検証します[＃10464](https://github.com/pingcap/tidb/pull/10464)
    -   デフォルトでハッシュパーティションを有効にします。パーティション定義に列が1つしかない場合は、範囲列パーティションを有効にします[＃9936](https://github.com/pingcap/tidb/pull/9936)

## PD {#pd}

-   リージョンメタデータを保存するには、デフォルトでリージョンストレージを有効にします[＃1524](https://github.com/pingcap/pd/pull/1524)
-   ホットリージョンスケジューリングが別のスケジューラによってプリエンプトされる問題を修正します[＃1522](https://github.com/pingcap/pd/pull/1522)
-   リーダーの優先順位が有効にならない問題を修正します[＃1533](https://github.com/pingcap/pd/pull/1533)
-   13の[＃1535](https://github.com/pingcap/pd/pull/1535)インターフェースを追加し`ScanRegions`
-   オペレーターを積極的にプッシュする[＃1536](https://github.com/pingcap/pd/pull/1536)
-   各店舗のオペレーターの速度を個別に制御するための店舗制限メカニズムを追加します[＃1474](https://github.com/pingcap/pd/pull/1474)
-   一貫性のない`Config`ステータス[＃1476](https://github.com/pingcap/pd/pull/1476)の問題を修正します

## TiKV {#tikv}

-   エンジン
    -   ブロックキャッシュを共有する複数の列ファミリーをサポートする[＃4563](https://github.com/tikv/tikv/pull/4563)

-   サーバ
    -   [＃4098](https://github.com/tikv/tikv/pull/4098)を削除し`TxnScheduler`
    -   悲観的なロックトランザクションをサポートする[＃4698](https://github.com/tikv/tikv/pull/4698)

-   ラフトストア
    -   休止状態のリージョンをサポートして、raftstoreCPU1の消費を削減し[＃4591](https://github.com/tikv/tikv/pull/4591)
    -   リーダーが学習者の`ReadIndex`の要求に応答しない問題を修正します[＃4653](https://github.com/tikv/tikv/pull/4653)
    -   場合によってはリーダーの転送の失敗を修正[＃4684](https://github.com/tikv/tikv/pull/4684)
    -   場合によってはダーティリードの問題を修正します[＃4688](https://github.com/tikv/tikv/pull/4688)
    -   スナップショットが適用されたデータを失う場合があるという問題を修正します[＃4716](https://github.com/tikv/tikv/pull/4716)

-   コプロセッサー
    -   RPN関数を追加する
        -   [＃4691](https://github.com/tikv/tikv/pull/4601) `LogicalOr`
        -   [＃4602](https://github.com/tikv/tikv/pull/4602) `LTReal`
        -   [＃4602](https://github.com/tikv/tikv/pull/4602) `LEReal`
        -   [＃4602](https://github.com/tikv/tikv/pull/4602) `GTReal`
        -   [＃4602](https://github.com/tikv/tikv/pull/4602) `GEReal`
        -   [＃4602](https://github.com/tikv/tikv/pull/4602) `NEReal`
        -   [＃4602](https://github.com/tikv/tikv/pull/4602) `EQReal`
        -   [＃4720](https://github.com/tikv/tikv/pull/4720) `IsNull`
        -   [＃4720](https://github.com/tikv/tikv/pull/4720) `IsTrue`
        -   [＃4720](https://github.com/tikv/tikv/pull/4720) `IsFalse`
        -   `Int`の比較演算を[＃4625](https://github.com/tikv/tikv/pull/4625)
        -   `Decimal`の比較演算を[＃4625](https://github.com/tikv/tikv/pull/4625)
        -   `String`の比較演算を[＃4625](https://github.com/tikv/tikv/pull/4625)
        -   `Time`の比較演算を[＃4625](https://github.com/tikv/tikv/pull/4625)
        -   `Duration`の比較演算を[＃4625](https://github.com/tikv/tikv/pull/4625)
        -   `Json`の比較演算を[＃4625](https://github.com/tikv/tikv/pull/4625)
        -   `Int`のサポートと[＃4733](https://github.com/tikv/tikv/pull/4733)
        -   `Real`のサポートと[＃4733](https://github.com/tikv/tikv/pull/4733)
        -   `Decimal`のサポートと[＃4733](https://github.com/tikv/tikv/pull/4733)
        -   `Int`のMOD機能を[＃4727](https://github.com/tikv/tikv/pull/4727)
        -   `Real`のMOD機能を[＃4727](https://github.com/tikv/tikv/pull/4727)
        -   `Decimal`のMOD機能を[＃4727](https://github.com/tikv/tikv/pull/4727)
        -   `Int`のマイナス演算を[＃4746](https://github.com/tikv/tikv/pull/4746)
        -   `Real`のマイナス演算を[＃4746](https://github.com/tikv/tikv/pull/4746)
        -   `Decimal`のマイナス演算を[＃4746](https://github.com/tikv/tikv/pull/4746)

## ツール {#tools}

-   TiDB Binlog
    -   ダウンストリームのデータレプリケーションの遅延を追跡するためのメトリックを追加します[＃594](https://github.com/pingcap/tidb-binlog/pull/594)

-   TiDB Lightning

    -   シャーディングされたデータベースとテーブルのマージをサポート[＃95](https://github.com/pingcap/tidb-lightning/pull/95)
    -   KV書き込み失敗の再試行メカニズムを追加します[＃176](https://github.com/pingcap/tidb-lightning/pull/176)
    -   デフォルト値の`table-concurrency`を63に更新し[＃175](https://github.com/pingcap/tidb-lightning/pull/175) 。
    -   提供されていない場合は`tidb.pd-addr`と`tidb.port`を自動的に検出して、必要な構成アイテムを減らします[＃173](https://github.com/pingcap/tidb-lightning/pull/173)
