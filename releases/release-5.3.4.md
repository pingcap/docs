---
title: TiDB 5.3.4 Release Notes
---

# TiDB 5.3.4 リリースノート {#tidb-5-3-4-release-notes}

発売日：2022年11月24日

TiDB バージョン: 5.3.4

## 改良点 {#improvements}

-   TiKV

    -   更新ごとに TLS 証明書を自動的にリロードして、可用性を向上させます[#12546](https://github.com/tikv/tikv/issues/12546)

## バグの修正 {#bug-fixes}

-   TiDB

    -   リージョンのマージ時にリージョンのキャッシュが時間内にクリーンアップされない問題を修正します[#37141](https://github.com/pingcap/tidb/issues/37141)
    -   `ENUM`列または`SET`列のエンコーディングが間違っているため、TiDB が間違ったデータを書き込む問題を修正します[#32302](https://github.com/pingcap/tidb/issues/32302)
    -   データベース レベルの権限が正しくクリーンアップされない問題を修正します[#38363](https://github.com/pingcap/tidb/issues/38363)
    -   `mysql.tables_priv`テーブル[#38293](https://github.com/pingcap/tidb/issues/38293)で`grantor`フィールドが欠落している問題を修正します。
    -   `KILL TIDB`がアイドル状態の接続ですぐに有効にならない問題を修正します[#24031](https://github.com/pingcap/tidb/issues/24031)
    -   TiDB と MySQL で`date_add`と`date_sub`の戻り値の型が異なる問題を修正[#36394](https://github.com/pingcap/tidb/issues/36394) , [#27573](https://github.com/pingcap/tidb/issues/27573)
    -   パーサーがテーブル オプション[#38368](https://github.com/pingcap/tidb/issues/38368)を復元するときの誤った値`INSERT_METHOD`を修正します。
    -   v5.1以前のMySQLクライアントがTiDBサーバー[#29725](https://github.com/pingcap/tidb/issues/29725)に接続すると認証に失敗する問題を修正
    -   符号なし`BIGINT`引数を渡すときの`GREATEST`と`LEAST`の間違った結果を修正[#30101](https://github.com/pingcap/tidb/issues/30101)
    -   TiDB の`concat(ifnull(time(3))`の結果が MySQL [#29498](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   TiFlash [#29952](https://github.com/pingcap/tidb/issues/29952)からクエリを実行すると`avg()`関数が`ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.`を返す問題を修正
    -   `HashJoinExec` [#30289](https://github.com/pingcap/tidb/issues/30289)を使用すると`ERROR 1105 (HY000): close of nil channel`が返される問題を修正
    -   論理演算のクエリ時に TiKV とTiFlashが異なる結果を返す問題を修正します[#37258](https://github.com/pingcap/tidb/issues/37258)
    -   トランザクションのコミットが完了する前に、DML executor を含む`EXPLAIN ANALYZE`ステートメントが結果を返す可能性があるという問題を修正します[#37373](https://github.com/pingcap/tidb/issues/37373)
    -   多くのリージョンをマージした後、リージョンキャッシュが適切にクリアされない問題を修正します[#37174](https://github.com/pingcap/tidb/issues/37174)
    -   特定のシナリオで`EXECUTE`ステートメントが予期しないエラーをスローする可能性がある問題を修正します[#37187](https://github.com/pingcap/tidb/issues/37187)
    -   `ORDER BY`句に相関サブクエリが含まれている場合、 `GROUP CONCAT` with `ORDER BY`が失敗する可能性がある問題を修正します[#18216](https://github.com/pingcap/tidb/issues/18216)
    -   プラン キャッシュ[#29565](https://github.com/pingcap/tidb/issues/29565)を使用しているときに、長さと幅が Decimal と Real に正しく設定されていない場合に返される間違った結果を修正します。

-   PD

    -   PD がダッシュボード プロキシ リクエストを正しく処理できない問題を修正します[#5321](https://github.com/tikv/pd/issues/5321)
    -   特定のシナリオでTiFlash学習者のレプリカが作成されない場合がある問題を修正します[#5401](https://github.com/tikv/pd/issues/5401)
    -   不正確なストリーム タイムアウトを修正し、リーダーの切り替えを高速化します[#5207](https://github.com/tikv/pd/issues/5207)

-   TiFlash

    -   引数の型が UInt8 [#6127](https://github.com/pingcap/tiflash/issues/6127)の場合、論理演算子が間違った結果を返す問題を修正
    -   整数のデフォルト値として`0.0`を使用すると、 TiFlashブートストラップが失敗する問題を修正します (例: `` `i` int(11) NOT NULL DEFAULT '0.0'`` [#3157](https://github.com/pingcap/tiflash/issues/3157) 。

-   ツール

    -   Dumpling

        -   `--compress`オプションと S3 出力ディレクトリを同時に設定するとDumpling がデータをダンプできない問題を修正[#30534](https://github.com/pingcap/tidb/issues/30534)

    -   TiCDC

        -   MySQL 関連のエラーが時間[#6698](https://github.com/pingcap/tiflow/issues/6698)で所有者に報告されないため、changefeed の状態が正しくない問題を修正します。
