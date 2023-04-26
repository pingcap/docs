---
title: TiDB 3.0.16 Release Notes
---

# TiDB 3.0.16 リリースノート {#tidb-3-0-16-release-notes}

発売日：2020年07月03日

TiDB バージョン: 3.0.16

## 改良点 {#improvements}

-   TiDB

    -   ハッシュ パーティション プルーニング[#17308](https://github.com/pingcap/tidb/pull/17308)で`is null`フィルター条件をサポート
    -   複数のリージョンリクエストが同時に失敗した場合の SQL タイムアウトの問題を回避するために、各リージョンに異なる`Backoffer`割り当てます[#17583](https://github.com/pingcap/tidb/pull/17583)
    -   新しく追加されたパーティション[#17668](https://github.com/pingcap/tidb/pull/17668)の別々のリージョンを分割します
    -   `delete`または`update`ステートメントから生成されたフィードバックを破棄する[#17841](https://github.com/pingcap/tidb/pull/17841)
    -   `json.Unmarshal` in `job.DecodeArgs`の使用法を修正して、将来の Go バージョン[#17887](https://github.com/pingcap/tidb/pull/17887)と互換性を持たせます。
    -   スロー クエリ ログとステートメント サマリー テーブルの機密情報を削除します[#18128](https://github.com/pingcap/tidb/pull/18128)
    -   MySQL の動作に合わせて`DateTime`区切り文字[#17499](https://github.com/pingcap/tidb/pull/17499)
    -   MySQL [#17496](https://github.com/pingcap/tidb/pull/17496)と一致する範囲の日付形式で`%h`を処理する

-   TiKV

    -   スナップショットの受信後にストア ハートビートを PD に送信しないようにする[#8145](https://github.com/tikv/tikv/pull/8145)
    -   PD クライアント ログ[#8091](https://github.com/tikv/tikv/pull/8091)を改善します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   [#18248](https://github.com/pingcap/tidb/pull/18248)つのトランザクションで書き込まれ、削除された主キーのロックが別のトランザクションによって解決されるために発生したデータの不整合の問題を修正します。
    -   `Got too many pings` PD サーバー側フォロワーの gRPC エラー ログを修正[#17944](https://github.com/pingcap/tidb/pull/17944)
    -   HashJoin の子が`TypeNull`列[#17935](https://github.com/pingcap/tidb/pull/17935)を返すときに発生する可能性があるpanicの問題を修正します
    -   アクセスが拒否されたときのエラー メッセージを修正します[#17722](https://github.com/pingcap/tidb/pull/17722)
    -   `int`と`float`型の JSON 比較の問題を修正[#17715](https://github.com/pingcap/tidb/pull/17715)
    -   データ競合[#17710](https://github.com/pingcap/tidb/pull/17710)を引き起こす障害点を更新します。
    -   テーブル[#17617](https://github.com/pingcap/tidb/pull/17617)の作成時に、事前に分割されたリージョンのタイムアウトが機能しない可能性があるという問題を修正します。
    -   送信失敗後のあいまいなエラー メッセージによるpanicを修正します[#17378](https://github.com/pingcap/tidb/pull/17378)
    -   特殊なケースで`FLASHBACK TABLE`失敗する可能性がある問題を修正[#17165](https://github.com/pingcap/tidb/pull/17165)
    -   ステートメントに文字列列[#16658](https://github.com/pingcap/tidb/pull/16658)しかない場合の範囲計算結果が不正確になる問題を修正
    -   `only_full_group_by` SQL モードが設定されている場合に発生したクエリ エラーを修正[#16620](https://github.com/pingcap/tidb/pull/16620)
    -   `case when`関数から返される結果のフィールド長が不正確であるという問題を修正します[#16562](https://github.com/pingcap/tidb/pull/16562)
    -   `count`集計関数の decimal プロパティの型推論を修正します[#17702](https://github.com/pingcap/tidb/pull/17702)

-   TiKV

    -   取り込まれたファイルから読み取られた潜在的な間違った結果を修正します[#8039](https://github.com/tikv/tikv/pull/8039)
    -   複数のマージ プロセス中にピアのストアが分離されている場合、ピアを削除できない問題を修正します[#8005](https://github.com/tikv/tikv/pull/8005)

-   PD

    -   PD Control[#2577](https://github.com/pingcap/pd/pull/2577)でリージョンキーをクエリするときの`404`エラーを修正します。
