---
title: TiDB 3.0.16 Release Notes
---

# TiDB 3.0.16 リリースノート {#tidb-3-0-16-release-notes}

発売日：2020年7月3日

TiDB バージョン: 3.0.16

## 改善点 {#improvements}

-   TiDB

    -   ハッシュ パーティション プルーニング[<a href="https://github.com/pingcap/tidb/pull/17308">#17308</a>](https://github.com/pingcap/tidb/pull/17308)で`is null`フィルター条件をサポートします。
    -   複数のリージョンのリクエストが同時に失敗した場合の SQL タイムアウトの問題を回避するには、各リージョンに異なる`Backoffer`割り当てます[<a href="https://github.com/pingcap/tidb/pull/17583">#17583</a>](https://github.com/pingcap/tidb/pull/17583)
    -   新しく追加されたパーティション[<a href="https://github.com/pingcap/tidb/pull/17668">#17668</a>](https://github.com/pingcap/tidb/pull/17668)の個別のリージョンを分割する
    -   `delete`または`update`ステートメントから生成されたフィードバックを破棄します[<a href="https://github.com/pingcap/tidb/pull/17841">#17841</a>](https://github.com/pingcap/tidb/pull/17841)
    -   将来の Go バージョン[<a href="https://github.com/pingcap/tidb/pull/17887">#17887</a>](https://github.com/pingcap/tidb/pull/17887)と互換性があるように`json.Unmarshal` in `job.DecodeArgs`の使用法を修正します。
    -   スロークエリログとステートメント概要テーブル[<a href="https://github.com/pingcap/tidb/pull/18128">#18128</a>](https://github.com/pingcap/tidb/pull/18128)の機密情報を削除します。
    -   MySQL の動作を`DateTime`区切り文字[<a href="https://github.com/pingcap/tidb/pull/17499">#17499</a>](https://github.com/pingcap/tidb/pull/17499)と一致させます。
    -   MySQL [<a href="https://github.com/pingcap/tidb/pull/17496">#17496</a>](https://github.com/pingcap/tidb/pull/17496)と一致する範囲の日付形式で`%h`を処理します。

-   TiKV

    -   スナップショットの受信後にストア ハートビートを PD に送信しないようにします[<a href="https://github.com/tikv/tikv/pull/8145">#8145</a>](https://github.com/tikv/tikv/pull/8145)
    -   PDクライアントログの改善[<a href="https://github.com/tikv/tikv/pull/8091">#8091</a>](https://github.com/tikv/tikv/pull/8091)

## バグの修正 {#bug-fixes}

-   TiDB

    -   あるトランザクションで書き込まれ削除された主キーのロックが別のトランザクションによって解決されるために発生するデータの不整合の問題を修正します[<a href="https://github.com/pingcap/tidb/pull/18248">#18248</a>](https://github.com/pingcap/tidb/pull/18248)
    -   PD サーバー側フォロワー[<a href="https://github.com/pingcap/tidb/pull/17944">#17944</a>](https://github.com/pingcap/tidb/pull/17944)の`Got too many pings` gRPC エラー ログを修正します。
    -   HashJoin の子が`TypeNull`列[<a href="https://github.com/pingcap/tidb/pull/17935">#17935</a>](https://github.com/pingcap/tidb/pull/17935)を返したときに発生する可能性があるpanicの問題を修正します。
    -   アクセスが拒否された場合のエラーメッセージを修正[<a href="https://github.com/pingcap/tidb/pull/17722">#17722</a>](https://github.com/pingcap/tidb/pull/17722)
    -   タイプ`int`と`float`の JSON 比較の問題を修正[<a href="https://github.com/pingcap/tidb/pull/17715">#17715</a>](https://github.com/pingcap/tidb/pull/17715)
    -   データ競合[<a href="https://github.com/pingcap/tidb/pull/17710">#17710</a>](https://github.com/pingcap/tidb/pull/17710)を引き起こすフェイルポイントを更新します。
    -   テーブル[<a href="https://github.com/pingcap/tidb/pull/17617">#17617</a>](https://github.com/pingcap/tidb/pull/17617)の作成時にタイムアウト前の分割リージョンが機能しない可能性がある問題を修正します。
    -   送信失敗後のあいまいなエラー メッセージによって引き起こされるpanicを修正[<a href="https://github.com/pingcap/tidb/pull/17378">#17378</a>](https://github.com/pingcap/tidb/pull/17378)
    -   一部の特殊なケースで`FLASHBACK TABLE`失敗する可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/pull/17165">#17165</a>](https://github.com/pingcap/tidb/pull/17165)
    -   ステートメントに文字列列[<a href="https://github.com/pingcap/tidb/pull/16658">#16658</a>](https://github.com/pingcap/tidb/pull/16658)のみがある場合に不正確な範囲計算結果が発生する問題を修正
    -   `only_full_group_by` SQLモード設定時に発生するクエリエラーを修正[<a href="https://github.com/pingcap/tidb/pull/16620">#16620</a>](https://github.com/pingcap/tidb/pull/16620)
    -   `case when`関数から返される結果のフィールド長が不正確である問題を修正します[<a href="https://github.com/pingcap/tidb/pull/16562">#16562</a>](https://github.com/pingcap/tidb/pull/16562)
    -   `count`集計関数[<a href="https://github.com/pingcap/tidb/pull/17702">#17702</a>](https://github.com/pingcap/tidb/pull/17702)の 10 進数プロパティの型推論を修正しました。

-   TiKV

    -   取り込まれたファイルから読み取られた潜在的な間違った結果を修正[<a href="https://github.com/tikv/tikv/pull/8039">#8039</a>](https://github.com/tikv/tikv/pull/8039)
    -   複数のマージ プロセス中にピアのストアが分離されている場合にピアを削除できない問題を修正します[<a href="https://github.com/tikv/tikv/pull/8005">#8005</a>](https://github.com/tikv/tikv/pull/8005)

-   PD

    -   PD Control [<a href="https://github.com/pingcap/pd/pull/2577">#2577</a>](https://github.com/pingcap/pd/pull/2577)でリージョンキーをクエリする際の`404`エラーを修正
