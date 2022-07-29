---
title: TiDB 3.0.16 Release Notes
---

# TiDB3.0.16リリースノート {#tidb-3-0-16-release-notes}

発売日：2020年7月3日

TiDBバージョン：3.0.16

## 改善点 {#improvements}

-   TiDB

    -   ハッシュパーティションプルーニング[＃17308](https://github.com/pingcap/tidb/pull/17308)で`is null`フィルター条件をサポートする
    -   複数のリージョンリクエストが同時に失敗した場合のSQLタイムアウトの問題を回避するために、各リージョンに異なる`Backoffer`を割り当てます[＃17583](https://github.com/pingcap/tidb/pull/17583)
    -   新しく追加されたパーティション[＃17668](https://github.com/pingcap/tidb/pull/17668)の個別のリージョンを分割する
    -   `delete`または`update`ステートメントから生成されたフィードバックを破棄します[＃17841](https://github.com/pingcap/tidb/pull/17841)
    -   将来のGoバージョン[＃17887](https://github.com/pingcap/tidb/pull/17887)と互換性があるように、 `job.DecodeArgs`分の`json.Unmarshal`の使用法を修正してください
    -   遅いクエリログとステートメントサマリーテーブルの機密情報を削除する[＃18128](https://github.com/pingcap/tidb/pull/18128)
    -   MySQLの動作を`DateTime`の区切り文字[＃17499](https://github.com/pingcap/tidb/pull/17499)と一致させます
    -   MySQL3と一致する範囲の日付形式で`%h`を処理し[＃17496](https://github.com/pingcap/tidb/pull/17496)

-   TiKV

    -   スナップショットを受信した後、ストアのハートビートをPDに送信しないでください[＃8145](https://github.com/tikv/tikv/pull/8145)
    -   PDクライアントログを改善する[＃8091](https://github.com/tikv/tikv/pull/8091)

## バグの修正 {#bug-fixes}

-   TiDB

    -   あるトランザクションで書き込まれ、削除された主キーのロックが別のトランザクションによって解決されるために発生したデータの不整合の問題を修正します[＃18248](https://github.com/pingcap/tidb/pull/18248)
    -   PDサーバー側フォロワーの`Got too many pings`エラーログを修正します[＃17944](https://github.com/pingcap/tidb/pull/17944)
    -   HashJoinの子が`TypeNull`列[＃17935](https://github.com/pingcap/tidb/pull/17935)を返すときに発生する可能性があるpanicの問題を修正します
    -   アクセスが拒否されたときのエラーメッセージを修正する[＃17722](https://github.com/pingcap/tidb/pull/17722)
    -   `int`タイプと`float`タイプのJSON比較の問題を修正[＃17715](https://github.com/pingcap/tidb/pull/17715)
    -   データ競合の原因となるフェイルポイントを更新する[＃17710](https://github.com/pingcap/tidb/pull/17710)
    -   テーブルの作成時にタイムアウトの事前分割領域が機能しない可能性がある問題を修正します[＃17617](https://github.com/pingcap/tidb/pull/17617)
    -   送信失敗後のあいまいなエラーメッセージによって引き起こされるpanicを修正する[＃17378](https://github.com/pingcap/tidb/pull/17378)
    -   特別な場合に`FLASHBACK TABLE`が失敗する可能性があるという問題を修正します[＃17165](https://github.com/pingcap/tidb/pull/17165)
    -   ステートメントに文字列列のみがある場合の不正確な範囲計算結果の問題を修正します[＃16658](https://github.com/pingcap/tidb/pull/16658)
    -   `only_full_group_by`モードが設定されているときに発生したクエリエラーを修正します[＃16620](https://github.com/pingcap/tidb/pull/16620)
    -   `case when`関数から返される結果のフィールド長が不正確であるという問題を修正します[＃16562](https://github.com/pingcap/tidb/pull/16562)
    -   `count`集計関数[＃17702](https://github.com/pingcap/tidb/pull/17702)のdecimalプロパティの型推論を修正しました

-   TiKV

    -   取り込んだファイルから読み取られた潜在的な誤った結果を修正する[＃8039](https://github.com/tikv/tikv/pull/8039)
    -   複数のマージプロセス中にストアが分離されている場合、ピアを削除できない問題を修正します[＃8005](https://github.com/tikv/tikv/pull/8005)

-   PD

    -   PD Control[＃2577](https://github.com/pingcap/pd/pull/2577)でリージョンキーを照会するときの`404`のエラーを修正しました
