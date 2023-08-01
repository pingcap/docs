---
title: TiDB 3.0.16 Release Notes
---

# TiDB 3.0.16 リリースノート {#tidb-3-0-16-release-notes}

発売日：2020年7月3日

TiDB バージョン: 3.0.16

## 改善点 {#improvements}

-   TiDB

    -   ハッシュ パーティション プルーニング[#17308](https://github.com/pingcap/tidb/pull/17308)で`is null`フィルター条件をサポートします。
    -   複数のリージョンのリクエストが同時に失敗した場合の SQL タイムアウトの問題を回避するには、各リージョンに異なる`Backoffer`割り当てます[#17583](https://github.com/pingcap/tidb/pull/17583)
    -   新しく追加されたパーティション[#17668](https://github.com/pingcap/tidb/pull/17668)の個別のリージョンを分割する
    -   `delete`または`update`ステートメントから生成されたフィードバックを破棄します[#17841](https://github.com/pingcap/tidb/pull/17841)
    -   将来の Go バージョン[#17887](https://github.com/pingcap/tidb/pull/17887)と互換性があるように`json.Unmarshal` in `job.DecodeArgs`の使用法を修正します。
    -   スロークエリログとステートメント概要テーブル[#18128](https://github.com/pingcap/tidb/pull/18128)の機密情報を削除します。
    -   MySQL の動作を`DateTime`区切り文字[#17499](https://github.com/pingcap/tidb/pull/17499)と一致させます。
    -   MySQL [#17496](https://github.com/pingcap/tidb/pull/17496)と一致する範囲の日付形式で`%h`​​を処理します。

-   TiKV

    -   スナップショットの受信後にストア ハートビートを PD に送信しないようにします[#8145](https://github.com/tikv/tikv/pull/8145)
    -   PDクライアントログの改善[#8091](https://github.com/tikv/tikv/pull/8091)

## バグの修正 {#bug-fixes}

-   TiDB

    -   あるトランザクションで書き込まれ削除された主キーのロックが別のトランザクションによって解決されるために発生するデータの不整合の問題を修正します[#18248](https://github.com/pingcap/tidb/pull/18248)
    -   PD サーバー側フォロワー[#17944](https://github.com/pingcap/tidb/pull/17944)の`Got too many pings` gRPC エラー ログを修正します。
    -   HashJoin の子が`TypeNull`列[#17935](https://github.com/pingcap/tidb/pull/17935)を返したときに発生する可能性があるpanicの問題を修正します。
    -   アクセスが拒否された場合のエラーメッセージを修正[#17722](https://github.com/pingcap/tidb/pull/17722)
    -   タイプ`int`と`float`の JSON 比較の問題を修正[#17715](https://github.com/pingcap/tidb/pull/17715)
    -   データ競合[#17710](https://github.com/pingcap/tidb/pull/17710)を引き起こすフェイルポイントを更新します。
    -   テーブル[#17617](https://github.com/pingcap/tidb/pull/17617)の作成時にタイムアウト前の分割リージョンが機能しない可能性がある問題を修正します。
    -   送信失敗後のあいまいなエラー メッセージによって引き起こされるpanicを修正[#17378](https://github.com/pingcap/tidb/pull/17378)
    -   一部の特殊なケースで`FLASHBACK TABLE`失敗する可能性がある問題を修正[#17165](https://github.com/pingcap/tidb/pull/17165)
    -   ステートメントに文字列列[#16658](https://github.com/pingcap/tidb/pull/16658)のみがある場合に不正確な範囲計算結果が発生する問題を修正
    -   `only_full_group_by` SQLモード設定時に発生するクエリエラーを修正[#16620](https://github.com/pingcap/tidb/pull/16620)
    -   `case when`関数から返される結果のフィールド長が不正確である問題を修正します[#16562](https://github.com/pingcap/tidb/pull/16562)
    -   `count`集計関数[#17702](https://github.com/pingcap/tidb/pull/17702)の 10 進数プロパティの型推論を修正しました。

-   TiKV

    -   取り込まれたファイルから読み取られた潜在的な間違った結果を修正[#8039](https://github.com/tikv/tikv/pull/8039)
    -   複数のマージ プロセス中にピアのストアが分離されている場合にピアを削除できない問題を修正します[#8005](https://github.com/tikv/tikv/pull/8005)

-   PD

    -   PD Control [#2577](https://github.com/pingcap/pd/pull/2577)でリージョンキーをクエリする際の`404`エラーを修正
