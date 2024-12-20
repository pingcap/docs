---
title: TiDB 5.3.4 Release Notes
summary: TiDB 5.3.4 は 2022 年 11 月 24 日にリリースされました。このリリースには、TiKV の改善と、TiDB、PD、 TiFlash、 Dumpling、TiCDC のバグ修正が含まれています。主なバグ修正には、TLS 証明書の再読み込み、リージョンキャッシュのクリーンアップ、誤ったデータの書き込み、データベース レベルの権限、認証の失敗に関連する問題が含まれます。その他の修正では、論理演算子、ストリームのタイムアウト、リーダーの切り替え、データのダンプに関する問題に対処しています。
---

# TiDB 5.3.4 リリースノート {#tidb-5-3-4-release-notes}

発売日: 2022年11月24日

TiDB バージョン: 5.3.4

## 改善点 {#improvements}

-   ティクヴ

    -   可用性を向上させるために、更新ごとに TLS 証明書を自動的に再読み込みします[＃12546](https://github.com/tikv/tikv/issues/12546)

## バグ修正 {#bug-fixes}

-   ティビ

    -   リージョンがマージされたときにリージョンキャッシュが時間内にクリーンアップされない問題を修正[＃37141](https://github.com/pingcap/tidb/issues/37141)
    -   `ENUM`列目または`SET`列目のエンコードが間違っているためにTiDBが間違ったデータを書き込む問題を修正しました[＃32302](https://github.com/pingcap/tidb/issues/32302)
    -   データベースレベルの権限が誤ってクリーンアップされる問題を修正[＃38363](https://github.com/pingcap/tidb/issues/38363)
    -   `mysql.tables_priv`テーブル[＃38293](https://github.com/pingcap/tidb/issues/38293)の`grantor`フィールドが欠落している問題を修正
    -   `KILL TIDB`アイドル接続ですぐに効果を発揮できない問題を修正[＃24031](https://github.com/pingcap/tidb/issues/24031)
    -   TiDBとMySQL [＃36394](https://github.com/pingcap/tidb/issues/36394) [＃27573](https://github.com/pingcap/tidb/issues/27573)間で戻り値の型`date_add`と`date_sub`が異なる問題を修正
    -   パーサーがテーブルオプション[＃38368](https://github.com/pingcap/tidb/issues/38368)を復元するときに誤った`INSERT_METHOD`値を修正します
    -   バージョン5.1以前のMySQLクライアントがTiDBサーバー[＃29725](https://github.com/pingcap/tidb/issues/29725)に接続する際に認証が失敗する問題を修正
    -   符号なし`BIGINT`引数[#30101](https://github.com/pingcap/tidb/issues/30101)渡すときに`GREATEST`と`LEAST`の間違った結果を修正
    -   TiDBの`concat(ifnull(time(3))`の結果がMySQL [＃29498](https://github.com/pingcap/tidb/issues/29498)の結果と異なる問題を修正
    -   TiFlash [＃29952](https://github.com/pingcap/tidb/issues/29952)からクエリされたときに`avg()`関数が`ERROR 1105 (HY000): other error for mpp stream: Could not convert to the target type - -value is out of range.`返す問題を修正
    -   `HashJoinExec` [＃30289](https://github.com/pingcap/tidb/issues/30289)使用すると`ERROR 1105 (HY000): close of nil channel`が返される問題を修正
    -   論理演算をクエリするときに TiKV とTiFlash が異なる結果を返す問題を修正[＃37258](https://github.com/pingcap/tidb/issues/37258)
    -   DMLエグゼキュータを使用した`EXPLAIN ANALYZE`文がトランザクションコミットが完了する前に結果を返す可能性がある問題を修正しました[＃37373](https://github.com/pingcap/tidb/issues/37373)
    -   多数のリージョンをマージした後にリージョンキャッシュが適切にクリアされない問題を修正[＃37174](https://github.com/pingcap/tidb/issues/37174)
    -   特定のシナリオで`EXECUTE`ステートメントが予期しないエラーをスローする可能性がある問題を修正[＃37187](https://github.com/pingcap/tidb/issues/37187)
    -   `ORDER BY`節に相関サブクエリ[＃18216](https://github.com/pingcap/tidb/issues/18216)含まれている場合に`GROUP CONCAT` with `ORDER BY`が失敗する可能性がある問題を修正しました。
    -   プラン キャッシュ[＃29565](https://github.com/pingcap/tidb/issues/29565)を使用するときに、10 進数と実数の長さと幅が誤って設定されている場合に返される誤った結果を修正しました。

-   PD

    -   PDがダッシュボードプロキシリクエストを正しく処理できない問題を修正[＃5321](https://github.com/tikv/pd/issues/5321)
    -   特定のシナリオでTiFlash学習レプリカが作成されない可能性がある問題を修正[＃5401](https://github.com/tikv/pd/issues/5401)
    -   不正確なストリームタイムアウトを修正し、リーダーの切り替えを高速化[＃5207](https://github.com/tikv/pd/issues/5207)

-   TiFlash

    -   引数の型がUInt8 [＃6127](https://github.com/pingcap/tiflash/issues/6127)の場合に論理演算子が間違った結果を返す問題を修正
    -   整数のデフォルト値として`0.0`が使用されるとTiFlashブートストラップが失敗する問題を修正しました (例: `` `i` int(11) NOT NULL DEFAULT '0.0'`` [＃3157](https://github.com/pingcap/tiflash/issues/3157)

-   ツール

    -   Dumpling

        -   `--compress`オプションと S3 出力ディレクトリが同時に設定されている場合にDumpling がデータをダンプできない問題を修正[＃30534](https://github.com/pingcap/tidb/issues/30534)

    -   ティCDC

        -   MySQL関連のエラーが時間内に所有者に報告されないため、changefeedの状態が正しくない問題を修正しました[＃6698](https://github.com/pingcap/tiflow/issues/6698)
