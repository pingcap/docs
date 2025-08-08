---
title: TiDB 3.0.16 Release Notes
summary: TiDB 3.0.16は2020年7月3日にリリースされました。このリリースには、「is null」フィルター条件のサポート、SQLタイムアウト問題への対応、スロークエリログ内の機密情報の削除などの改善が含まれています。バグ修正には、データの不整合の問題の解決、panic問題の修正、JSON比較およびクエリ結果のエラーへの対応が含まれます。TiKVとPDについても、ストアハートビート、ピアの削除、エラー処理に関するバグ修正が行われました。
---

# TiDB 3.0.16 リリースノート {#tidb-3-0-16-release-notes}

発売日：2020年7月3日

TiDB バージョン: 3.0.16

## 改善点 {#improvements}

-   TiDB

    -   ハッシュパーティションプルーニング[＃17308](https://github.com/pingcap/tidb/pull/17308)の`is null`フィルタ条件をサポート
    -   複数のリージョンリクエストが同時に失敗した場合にSQLタイムアウトの問題を回避するために、各リージョンに異なる`Backoffer`秒を割り当てます[＃17583](https://github.com/pingcap/tidb/pull/17583)
    -   新しく追加されたパーティション[＃17668](https://github.com/pingcap/tidb/pull/17668)個別の領域を分割します
    -   `delete`または`update`ステートメント[＃17841](https://github.com/pingcap/tidb/pull/17841)から生成されたフィードバックを破棄します
    -   将来の Go バージョン[＃17887](https://github.com/pingcap/tidb/pull/17887)との互換性を保つために、 `json.Unmarshal` in `job.DecodeArgs`の使用法を修正します。
    -   スロークエリログとステートメントサマリーテーブル[＃18128](https://github.com/pingcap/tidb/pull/18128)から機密情報を削除します
    -   MySQLの動作を`DateTime`区切り文字[＃17499](https://github.com/pingcap/tidb/pull/17499)に一致させる
    -   MySQL [＃17496](https://github.com/pingcap/tidb/pull/17496)と一致する範囲の日付形式で`%h`処理します

-   TiKV

    -   スナップショットを受信した後にストアハートビートをPDに送信しないようにする[＃8145](https://github.com/tikv/tikv/pull/8145)
    -   PDクライアントログ[＃8091](https://github.com/tikv/tikv/pull/8091)改善

## バグ修正 {#bug-fixes}

-   TiDB

    -   あるトランザクションで書き込まれ削除された主キーのロックが別のトランザクションによって解決されたために発生したデータの不整合の問題を修正しました[＃18248](https://github.com/pingcap/tidb/pull/18248)
    -   PDサーバー側フォロワー[＃17944](https://github.com/pingcap/tidb/pull/17944)の`Got too many pings`エラーログを修正
    -   HashJoinの子が`TypeNull`列[＃17935](https://github.com/pingcap/tidb/pull/17935)を返すときに発生する可能性のあるpanic問題を修正しました。
    -   アクセスが拒否されたときのエラーメッセージを修正[＃17722](https://github.com/pingcap/tidb/pull/17722)
    -   `int`と`float`タイプのJSON比較の問題を修正[＃17715](https://github.com/pingcap/tidb/pull/17715)
    -   データ競合[＃17710](https://github.com/pingcap/tidb/pull/17710)原因となる障害ポイントを更新する
    -   テーブル[＃17617](https://github.com/pingcap/tidb/pull/17617)作成時にタイムアウト前の分割領域が機能しない可能性がある問題を修正しました。
    -   送信失敗後のあいまいなエラーメッセージによって引き起こされるpanicを修正[＃17378](https://github.com/pingcap/tidb/pull/17378)
    -   `FLASHBACK TABLE`特殊なケースで失敗する可能性がある問題を修正[＃17165](https://github.com/pingcap/tidb/pull/17165)
    -   ステートメントに文字列列[＃16658](https://github.com/pingcap/tidb/pull/16658)のみがある場合に範囲計算結果が不正確になる問題を修正しました
    -   `only_full_group_by` SQLモードが[＃16620](https://github.com/pingcap/tidb/pull/16620)設定されている場合に発生するクエリエラーを修正
    -   `case when`関数から返される結果のフィールド長が不正確であるという問題を修正[＃16562](https://github.com/pingcap/tidb/pull/16562)
    -   `count`集計関数[＃17702](https://github.com/pingcap/tidb/pull/17702)の 10 進プロパティの型推論を修正

-   TiKV

    -   取り込んだファイルから読み取られる結果が誤っている可能性を修正[＃8039](https://github.com/tikv/tikv/pull/8039)
    -   複数のマージプロセス中にストアが分離されている場合にピアを削除できない問題を修正[＃8005](https://github.com/tikv/tikv/pull/8005)

-   PD

    -   PD Control [＃2577](https://github.com/pingcap/pd/pull/2577)でリージョンキーを照会する際の`404`エラーを修正しました
