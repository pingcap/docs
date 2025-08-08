---
title: TiDB 2.0.10 Release Notes
summary: TiDB 2.0.10およびTiDB Ansible 2.0.10は、2018年12月18日にリリースされました。このリリースでは、システムの互換性と安定性が向上しています。DDLジョブ、ORDER BY句およびUNION句、UNCOMPRESS関数、ANSI_QUOTES SQL_MODE、SELECT結果などに関する問題が修正されています。PDではRaftClusterのデッドロックの可能性が修正され、TiKVではリーダー転送が最適化され、冗長なリージョンハートビートが修正されています。
---

# TiDB 2.0.10 リリースノート {#tidb-2-0-10-release-notes}

2018年12月18日にTiDB 2.0.10がリリースされました。対応するTiDB Ansible 2.0.10もリリースされました。TiDB 2.0.9と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   DDLジョブ[＃8513](https://github.com/pingcap/tidb/pull/8513)キャンセルによって発生する可能性のある問題を修正
-   `ORDER BY`と`UNION`句でテーブル名を含む列を引用符で囲めない問題を修正[＃8514](https://github.com/pingcap/tidb/pull/8514)
-   `UNCOMPRESS`関数が不正な入力長[＃8607](https://github.com/pingcap/tidb/pull/8607)を判断しない問題を修正
-   TiDB [＃8575](https://github.com/pingcap/tidb/pull/8575)アップグレード時に`ANSI_QUOTES SQL_MODE`で発生した問題を修正
-   `select`場合によっては間違った結果が返される問題を修正[＃8570](https://github.com/pingcap/tidb/pull/8570)
-   終了信号[＃8501](https://github.com/pingcap/tidb/pull/8501)受信してもTiDBが終了できない可能性がある問題を修正しました
-   `IndexLookUpJoin`場合によっては間違った結果が返される問題を修正[＃8508](https://github.com/pingcap/tidb/pull/8508)
-   `GetVar`または`SetVar` [＃8454](https://github.com/pingcap/tidb/pull/8454)を含むフィルターを押し下げないでください
-   `UNION`節の結果の長さが場合によっては正しくない問題を修正[＃8491](https://github.com/pingcap/tidb/pull/8491)
-   `PREPARE FROM @var_name` [＃8488](https://github.com/pingcap/tidb/pull/8488)の問題を修正
-   一部のケースで統計情報をダンプするときにpanic問題を修正[＃8464](https://github.com/pingcap/tidb/pull/8464)
-   いくつかのケースにおけるポイントクエリの統計推定の問題を修正[＃8493](https://github.com/pingcap/tidb/pull/8493)
-   返されるデフォルト値`enum`が文字列[＃8476](https://github.com/pingcap/tidb/pull/8476)場合にpanic問題を修正
-   ワイドテーブル[＃8467](https://github.com/pingcap/tidb/pull/8467)のシナリオでメモリ消費量が多すぎる問題を修正
-   パーサーがmod opcode [＃8431](https://github.com/pingcap/tidb/pull/8431)を誤ってフォーマットした場合に発生する問題を修正しました
-   一部のケースで外部キー制約を追加することで発生するpanic問題を修正[＃8421](https://github.com/pingcap/tidb/pull/8421) 、 [＃8410](https://github.com/pingcap/tidb/pull/8410)
-   `YEAR`列型がゼロ値を誤って変換する問題を修正[＃8396](https://github.com/pingcap/tidb/pull/8396)
-   `VALUES`関数の引数が[＃8404](https://github.com/pingcap/tidb/pull/8404)列目ではない場合に発生するpanic問題を修正しました
-   サブクエリを含むステートメントのプランキャッシュを無効にする[＃8395](https://github.com/pingcap/tidb/pull/8395)

## PD {#pd}

-   デッドロック[＃1370](https://github.com/pingcap/pd/pull/1370)によりRaftClusterが停止できない問題を修正

## TiKV {#tikv}

-   遅延を最適化するために、リーダーを新しく作成されたピアに転送しないでください[＃3929](https://github.com/tikv/tikv/pull/3929)
-   冗長なリージョンハートビートを修正[＃3930](https://github.com/tikv/tikv/pull/3930)
