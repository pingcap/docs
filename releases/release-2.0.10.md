---
title: TiDB 2.0.10 Release Notes
---

# TiDB 2.0.10 リリースノート {#tidb-2-0-10-release-notes}

2018 年 12 月 18 日に、TiDB 2.0.10 がリリースされました。対応する TiDB Ansible 2.0.10 もリリースされています。 TiDB 2.0.9 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   DDL ジョブのキャンセルによって発生する可能性のある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8513">#8513</a>](https://github.com/pingcap/tidb/pull/8513)
-   `ORDER BY`と`UNION`句でテーブル名を含む列を引用できない問題を修正[<a href="https://github.com/pingcap/tidb/pull/8514">#8514</a>](https://github.com/pingcap/tidb/pull/8514)
-   `UNCOMPRESS`関数が不正な入力長[<a href="https://github.com/pingcap/tidb/pull/8607">#8607</a>](https://github.com/pingcap/tidb/pull/8607)を判定しない問題を修正
-   TiDB [<a href="https://github.com/pingcap/tidb/pull/8575">#8575</a>](https://github.com/pingcap/tidb/pull/8575)のアップグレード時に`ANSI_QUOTES SQL_MODE`で発生した問題を修正
-   `select`場合によっては間違った結果を返す問題を修正[<a href="https://github.com/pingcap/tidb/pull/8570">#8570</a>](https://github.com/pingcap/tidb/pull/8570)
-   TiDB が終了信号を受信したときに終了できない可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8501">#8501</a>](https://github.com/pingcap/tidb/pull/8501)
-   `IndexLookUpJoin`場合によっては間違った結果を返す問題を修正[<a href="https://github.com/pingcap/tidb/pull/8508">#8508</a>](https://github.com/pingcap/tidb/pull/8508)
-   `GetVar`または`SetVar` [<a href="https://github.com/pingcap/tidb/pull/8454">#8454</a>](https://github.com/pingcap/tidb/pull/8454)を含むフィルターを押し下げないでください。
-   `UNION`句の結果の長さが正しくない場合がある問題を修正[<a href="https://github.com/pingcap/tidb/pull/8491">#8491</a>](https://github.com/pingcap/tidb/pull/8491)
-   `PREPARE FROM @var_name` [<a href="https://github.com/pingcap/tidb/pull/8488">#8488</a>](https://github.com/pingcap/tidb/pull/8488)の問題を修正
-   場合によっては統計情報をダンプする際のpanicの問題を修正[<a href="https://github.com/pingcap/tidb/pull/8464">#8464</a>](https://github.com/pingcap/tidb/pull/8464)
-   場合によってはポイントクエリの統計推定の問題を修正[<a href="https://github.com/pingcap/tidb/pull/8493">#8493</a>](https://github.com/pingcap/tidb/pull/8493)
-   返されたデフォルト値`enum`が文字列[<a href="https://github.com/pingcap/tidb/pull/8476">#8476</a>](https://github.com/pingcap/tidb/pull/8476)である場合のpanicの問題を修正
-   幅の広いテーブル[<a href="https://github.com/pingcap/tidb/pull/8467">#8467</a>](https://github.com/pingcap/tidb/pull/8467)のシナリオでメモリが過剰に消費される問題を修正します。
-   パーサーが mod オペコード[<a href="https://github.com/pingcap/tidb/pull/8431">#8431</a>](https://github.com/pingcap/tidb/pull/8431)を誤ってフォーマットしたときに発生する問題を修正
-   場合によっては外部キー制約を追加することによって引き起こされるpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8421">#8421</a>](https://github.com/pingcap/tidb/pull/8421) 、 [<a href="https://github.com/pingcap/tidb/pull/8410">#8410</a>](https://github.com/pingcap/tidb/pull/8410)
-   `YEAR`列タイプがゼロ値[<a href="https://github.com/pingcap/tidb/pull/8396">#8396</a>](https://github.com/pingcap/tidb/pull/8396)を誤って変換する問題を修正します。
-   `VALUES`関数の引数が列[<a href="https://github.com/pingcap/tidb/pull/8404">#8404</a>](https://github.com/pingcap/tidb/pull/8404)ではない場合に発生するpanicの問題を修正
-   サブクエリを含むステートメントのプラン キャッシュを無効にする[<a href="https://github.com/pingcap/tidb/pull/8395">#8395</a>](https://github.com/pingcap/tidb/pull/8395)

## PD {#pd}

-   デッドロック[<a href="https://github.com/pingcap/pd/pull/1370">#1370</a>](https://github.com/pingcap/pd/pull/1370)が原因で RaftCluster が停止できない可能性がある問題を修正

## TiKV {#tikv}

-   起こり得る遅延を最適化するために、リーダーを新しく作成されたピアに転送しないようにします[<a href="https://github.com/tikv/tikv/pull/3929">#3929</a>](https://github.com/tikv/tikv/pull/3929)
-   冗長なリージョンハートビートを修正[<a href="https://github.com/tikv/tikv/pull/3930">#3930</a>](https://github.com/tikv/tikv/pull/3930)
