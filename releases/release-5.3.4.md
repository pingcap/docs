---
title: TiDB 5.3.4 Release Notes
---

# TiDB 5.3.4 リリースノート {#tidb-5-3-4-release-notes}

発売日：2022年11月24日

TiDB バージョン: 5.3.4

## 改善点 {#improvements}

-   TiKV

    -   可用性を向上させるために更新ごとに TLS 証明書を自動的にリロードする[<a href="https://github.com/tikv/tikv/issues/12546">#12546</a>](https://github.com/tikv/tikv/issues/12546)

## バグの修正 {#bug-fixes}

-   TiDB

    -   リージョンがマージされるときにリージョンキャッシュが時間内にクリーンアップされない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/37141">#37141</a>](https://github.com/pingcap/tidb/issues/37141)
    -   `ENUM`列または`SET`列のエンコーディングが間違っているため、TiDB が間違ったデータを書き込む問題を修正します[<a href="https://github.com/pingcap/tidb/issues/32302">#32302</a>](https://github.com/pingcap/tidb/issues/32302)
    -   データベースレベルの権限が誤ってクリーンアップされる問題を修正[<a href="https://github.com/pingcap/tidb/issues/38363">#38363</a>](https://github.com/pingcap/tidb/issues/38363)
    -   `mysql.tables_priv`テーブル[<a href="https://github.com/pingcap/tidb/issues/38293">#38293</a>](https://github.com/pingcap/tidb/issues/38293)の`grantor`フィールドが欠落している問題を修正
    -   アイドル状態の接続で`KILL TIDB`がすぐに有効にならない問題を修正[<a href="https://github.com/pingcap/tidb/issues/24031">#24031</a>](https://github.com/pingcap/tidb/issues/24031)
    -   TiDB と MySQL [<a href="https://github.com/pingcap/tidb/issues/36394">#36394</a>](https://github.com/pingcap/tidb/issues/36394) 、 [<a href="https://github.com/pingcap/tidb/issues/27573">#27573</a>](https://github.com/pingcap/tidb/issues/27573)で`date_add`と`date_sub`の戻り値の型が異なる問題を修正
    -   パーサーがテーブル オプション[<a href="https://github.com/pingcap/tidb/issues/38368">#38368</a>](https://github.com/pingcap/tidb/issues/38368)を復元するときの誤った`INSERT_METHOD`値を修正しました。
    -   v5.1 以前の MySQL クライアントが TiDBサーバーに接続するときに認証が失敗する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/29725">#29725</a>](https://github.com/pingcap/tidb/issues/29725)
    -   符号なし`BIGINT`引数[<a href="https://github.com/pingcap/tidb/issues/30101">#30101</a>](https://github.com/pingcap/tidb/issues/30101)を渡すときの`GREATEST`と`LEAST`の間違った結果を修正
    -   TiDB の`concat(ifnull(time(3))`の結果が MySQL [<a href="https://github.com/pingcap/tidb/issues/29498">#29498</a>](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   TiFlash [<a href="https://github.com/pingcap/tidb/issues/29952">#29952</a>](https://github.com/pingcap/tidb/issues/29952)からクエリすると`avg()`関数が`ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.`を返す問題を修正
    -   `HashJoinExec` [<a href="https://github.com/pingcap/tidb/issues/30289">#30289</a>](https://github.com/pingcap/tidb/issues/30289)を使用すると`ERROR 1105 (HY000): close of nil channel`が返される問題を修正
    -   論理演算のクエリ時に TiKV とTiFlashが異なる結果を返す問題を修正[<a href="https://github.com/pingcap/tidb/issues/37258">#37258</a>](https://github.com/pingcap/tidb/issues/37258)
    -   DML エグゼキュータを使用した`EXPLAIN ANALYZE`ステートメントが、トランザクションのコミットが完了する前に結果を返す可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/37373">#37373</a>](https://github.com/pingcap/tidb/issues/37373)
    -   多くのリージョンをマージした後、リージョンキャッシュが適切にクリアされない問題を修正[<a href="https://github.com/pingcap/tidb/issues/37174">#37174</a>](https://github.com/pingcap/tidb/issues/37174)
    -   特定のシナリオで`EXECUTE`ステートメントが予期しないエラーをスローする可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/37187">#37187</a>](https://github.com/pingcap/tidb/issues/37187)
    -   `ORDER BY`句に相関サブクエリ[<a href="https://github.com/pingcap/tidb/issues/18216">#18216</a>](https://github.com/pingcap/tidb/issues/18216)が含まれている場合、 `GROUP CONCAT`と`ORDER BY`が失敗する可能性がある問題を修正します。
    -   プラン キャッシュ[<a href="https://github.com/pingcap/tidb/issues/29565">#29565</a>](https://github.com/pingcap/tidb/issues/29565)の使用時に長さと幅が 10 進数と実数に正しく設定されていない場合に返される間違った結果を修正しました。

-   PD

    -   PD がダッシュボード プロキシ リクエストを正しく処理できない問題を修正します[<a href="https://github.com/tikv/pd/issues/5321">#5321</a>](https://github.com/tikv/pd/issues/5321)
    -   特定のシナリオ[<a href="https://github.com/tikv/pd/issues/5401">#5401</a>](https://github.com/tikv/pd/issues/5401)でTiFlash学習者レプリカが作成されないことがある問題を修正します。
    -   不正確なストリーム タイムアウトを修正し、リーダーの切り替えを加速します[<a href="https://github.com/tikv/pd/issues/5207">#5207</a>](https://github.com/tikv/pd/issues/5207)

-   TiFlash

    -   引数の型が UInt8 [<a href="https://github.com/pingcap/tiflash/issues/6127">#6127</a>](https://github.com/pingcap/tiflash/issues/6127)の場合、論理演算子が間違った結果を返す問題を修正
    -   整数のデフォルト値として`0.0`が使用されている場合 (例: `` `i` int(11) NOT NULL DEFAULT '0.0'`` [<a href="https://github.com/pingcap/tiflash/issues/3157">#3157</a>](https://github.com/pingcap/tiflash/issues/3157) 、 TiFlashブートストラップが失敗する問題を修正します。

-   ツール

    -   Dumpling

        -   `--compress`オプションと S3 出力ディレクトリが同時に設定されている場合、 Dumpling がデータをダンプできない問題を修正[<a href="https://github.com/pingcap/tidb/issues/30534">#30534</a>](https://github.com/pingcap/tidb/issues/30534)

    -   TiCDC

        -   MySQL 関連のエラーが時間内に所有者に報告されないため、変更フィードの状態が正しくない問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/6698">#6698</a>](https://github.com/pingcap/tiflow/issues/6698)
