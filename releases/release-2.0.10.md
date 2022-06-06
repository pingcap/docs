---
title: TiDB 2.0.10 Release Notes
---

# TiDB2.0.10リリースノート {#tidb-2-0-10-release-notes}

2018年12月18日、TiDB2.0.10がリリースされました。対応するTiDBAnsible2.0.10もリリースされています。 TiDB 2.0.9と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   DDLジョブのキャンセルによって発生する可能性のある問題を修正する[＃8513](https://github.com/pingcap/tidb/pull/8513)
-   `ORDER BY`節と`UNION`節がテーブル名[＃8514](https://github.com/pingcap/tidb/pull/8514)を含む列を引用できない問題を修正します
-   `UNCOMPRESS`関数が誤った入力長[＃8607](https://github.com/pingcap/tidb/pull/8607)を判断しない問題を修正します
-   TiDB3をアップグレードするときに`ANSI_QUOTES SQL_MODE`が遭遇する問題を修正し[＃8575](https://github.com/pingcap/tidb/pull/8575)
-   `select`が場合によっては間違った結果を返すという問題を修正します[＃8570](https://github.com/pingcap/tidb/pull/8570)
-   TiDBが終了信号を受信したときに終了できない可能性のある問題を修正します[＃8501](https://github.com/pingcap/tidb/pull/8501)
-   `IndexLookUpJoin`が場合によっては間違った結果を返すという問題を修正します[＃8508](https://github.com/pingcap/tidb/pull/8508)
-   `GetVar`または`SetVar`を含むフィルターを[＃8454](https://github.com/pingcap/tidb/pull/8454)ないでください
-   `UNION`句の結果の長さが正しくない場合があるという問題を修正します[＃8491](https://github.com/pingcap/tidb/pull/8491)
-   [＃8488](https://github.com/pingcap/tidb/pull/8488)の問題を修正し`PREPARE FROM @var_name`
-   場合によっては統計情報をダンプするときのパニックの問題を修正します[＃8464](https://github.com/pingcap/tidb/pull/8464)
-   場合によっては、ポイントクエリの統計推定の問題を修正します[＃8493](https://github.com/pingcap/tidb/pull/8493)
-   返されたデフォルトの`enum`値が文字列[＃8476](https://github.com/pingcap/tidb/pull/8476)である場合のパニックの問題を修正します
-   ワイドテーブルのシナリオでメモリが過剰に消費される問題を修正します[＃8467](https://github.com/pingcap/tidb/pull/8467)
-   パーサーがmodオペコード[＃8431](https://github.com/pingcap/tidb/pull/8431)を誤ってフォーマットしたときに発生する問題を修正します
-   場合によっては外部キー制約を追加することによって引き起こされるパニックの問題を修正し[＃8410](https://github.com/pingcap/tidb/pull/8410) [＃8421](https://github.com/pingcap/tidb/pull/8421)
-   `YEAR`列タイプがゼロ値[＃8396](https://github.com/pingcap/tidb/pull/8396)を誤って変換する問題を修正します
-   `VALUES`関数の引数が列[＃8404](https://github.com/pingcap/tidb/pull/8404)ではない場合に発生したパニックの問題を修正します
-   サブクエリを含むステートメントのプランキャッシュを無効にする[＃8395](https://github.com/pingcap/tidb/pull/8395)

## PD {#pd}

-   デッドロック[＃1370](https://github.com/pingcap/pd/pull/1370)が原因でRaftClusterが停止できない可能性のある問題を修正します

## TiKV {#tikv}

-   遅延の可能性を最適化するために、リーダーを新しく作成されたピアに転送しないでください[＃3929](https://github.com/tikv/tikv/pull/3929)
-   冗長なリージョンハートビートを修正する[＃3930](https://github.com/tikv/tikv/pull/3930)
