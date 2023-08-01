---
title: TiDB 2.0.10 Release Notes
---

# TiDB 2.0.10 リリースノート {#tidb-2-0-10-release-notes}

2018 年 12 月 18 日に、TiDB 2.0.10 がリリースされました。対応する TiDB Ansible 2.0.10 もリリースされています。 TiDB 2.0.9 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   DDL ジョブのキャンセルによって発生する可能性のある問題を修正します[#8513](https://github.com/pingcap/tidb/pull/8513)
-   `ORDER BY`と`UNION`句でテーブル名を含む列を引用できない問題を修正[#8514](https://github.com/pingcap/tidb/pull/8514)
-   `UNCOMPRESS`関数が不正な入力長[#8607](https://github.com/pingcap/tidb/pull/8607)を判定しない問題を修正
-   TiDB [#8575](https://github.com/pingcap/tidb/pull/8575)のアップグレード時に`ANSI_QUOTES SQL_MODE`で発生した問題を修正
-   `select`場合によっては間違った結果を返す問題を修正[#8570](https://github.com/pingcap/tidb/pull/8570)
-   TiDB が終了信号を受信したときに終了できない可能性がある問題を修正します[#8501](https://github.com/pingcap/tidb/pull/8501)
-   `IndexLookUpJoin`場合によっては間違った結果を返す問題を修正[#8508](https://github.com/pingcap/tidb/pull/8508)
-   `GetVar`または`SetVar` [#8454](https://github.com/pingcap/tidb/pull/8454)を含むフィルターを押し下げないでください。
-   `UNION`句の結果の長さが正しくない場合がある問題を修正[#8491](https://github.com/pingcap/tidb/pull/8491)
-   `PREPARE FROM @var_name` [#8488](https://github.com/pingcap/tidb/pull/8488)の問題を修正
-   場合によっては統計情報をダンプする際のpanicの問題を修正[#8464](https://github.com/pingcap/tidb/pull/8464)
-   場合によってはポイントクエリの統計推定の問題を修正[#8493](https://github.com/pingcap/tidb/pull/8493)
-   返されたデフォルト値`enum`が文字列[#8476](https://github.com/pingcap/tidb/pull/8476)である場合のpanicの問題を修正
-   幅の広いテーブル[#8467](https://github.com/pingcap/tidb/pull/8467)のシナリオでメモリが過剰に消費される問題を修正します。
-   パーサーが mod オペコード[#8431](https://github.com/pingcap/tidb/pull/8431)を誤ってフォーマットしたときに発生する問題を修正
-   場合によっては外部キー制約を追加することによって引き起こされるpanicの問題を修正します[#8421](https://github.com/pingcap/tidb/pull/8421) 、 [#8410](https://github.com/pingcap/tidb/pull/8410)
-   `YEAR`列タイプがゼロ値[#8396](https://github.com/pingcap/tidb/pull/8396)を誤って変換する問題を修正します。
-   `VALUES`関数の引数が列[#8404](https://github.com/pingcap/tidb/pull/8404)ではない場合に発生するpanicの問題を修正
-   サブクエリを含むステートメントのプラン キャッシュを無効にする[#8395](https://github.com/pingcap/tidb/pull/8395)

## PD {#pd}

-   デッドロック[#1370](https://github.com/pingcap/pd/pull/1370)により RaftCluster が停止できない可能性がある問題を修正

## TiKV {#tikv}

-   起こり得る遅延を最適化するために、リーダーを新しく作成されたピアに転送しないようにします[#3929](https://github.com/tikv/tikv/pull/3929)
-   冗長なリージョンハートビートを修正[#3930](https://github.com/tikv/tikv/pull/3930)
