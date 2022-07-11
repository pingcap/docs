---
title: TiDB 2.1.3 Release Notes
---

# TiDB2.1.3リリースノート {#tidb-2-1-3-release-notes}

2019年1月28日、TiDB2.1.3がリリースされました。対応するTiDBAnsible2.1.3もリリースされています。このリリースでは、TiDB 2.1.2と比較して、システムの安定性、SQLオプティマイザー、統計情報、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー/エグゼキューター
    -   場合によっては、プリペアドプランキャッシュのpanicの問題を修正します[＃8826](https://github.com/pingcap/tidb/pull/8826)
    -   インデックスがプレフィックスインデックス[＃8851](https://github.com/pingcap/tidb/pull/8851)の場合に範囲計算が間違っている問題を修正します
    -   `SQL_MODE`が厳密でない場合に文字列が不正な`TIME`形式である場合、 `CAST(str AS TIME(N))`はnullを返します[＃8966](https://github.com/pingcap/tidb/pull/8966)
    -   `UPDATE` 、場合によっては[＃8980](https://github.com/pingcap/tidb/pull/8980)の処理中に生成されたカラムのpanicの問題を修正します
    -   場合によっては、統計ヒストグラムの上限オーバーフローの問題を修正します[＃8989](https://github.com/pingcap/tidb/pull/8989)
    -   全表スキャンを回避し、クラスタのストレスを軽減するための`_tidb_rowid`の構築クエリのサポート範囲[＃9059](https://github.com/pingcap/tidb/pull/9059)
    -   `CAST(AS TIME)`の精度が大きすぎる場合はエラーを返します[＃9058](https://github.com/pingcap/tidb/pull/9058)
    -   デカルト積[＃9037](https://github.com/pingcap/tidb/pull/9037)で`Sort Merge Join`の使用を許可する
    -   場合によっては、panic後に統計ワーカーが再開できない問題を修正します[＃9085](https://github.com/pingcap/tidb/pull/9085)
    -   `Sort Merge Join`が場合によっては間違った結果を返すという問題を修正します[＃9046](https://github.com/pingcap/tidb/pull/9046)
    -   `CASE`節[＃8355](https://github.com/pingcap/tidb/pull/8355)でJSONタイプを返すことをサポートします
-   サーバ
    -   コメント[＃8766](https://github.com/pingcap/tidb/pull/8766)にTiDB以外のヒントが含まれている場合、エラーではなく警告を返します。
    -   構成されたTIMEZONE値[＃8879](https://github.com/pingcap/tidb/pull/8879)の有効性を確認します
    -   `QueryDurationHistogram`のメトリック項目を最適化して、より多くのステートメントタイプを表示します[＃8875](https://github.com/pingcap/tidb/pull/8875)
    -   場合によってはbigintの下限オーバーフローの問題を修正します[＃8544](https://github.com/pingcap/tidb/pull/8544)
    -   `ALLOW_INVALID_DATES`モード[＃9110](https://github.com/pingcap/tidb/pull/9110)をサポートする
-   DDL
    -   MySQL [＃8808](https://github.com/pingcap/tidb/pull/8808)の動作と一貫性を保つために、 `RENAME TABLE`の互換性の問題を修正します
    -   `ADD INDEX`の同時変更のサポートはすぐに有効になります[＃8786](https://github.com/pingcap/tidb/pull/8786)
    -   場合によっては`ADD COLUMN`のプロセス中に`UPDATE`のpanicの問題を修正します[＃8906](https://github.com/pingcap/tidb/pull/8906)
    -   場合によってはテーブルパーティションを同時に作成する問題を修正します[＃8902](https://github.com/pingcap/tidb/pull/8902)
    -   `utf8` [＃9152](https://github.com/pingcap/tidb/pull/9152)セットの`utf8mb4`への変換を[＃8951](https://github.com/pingcap/tidb/pull/8951)
    -   シャードビットオーバーフローの問題を修正[＃8976](https://github.com/pingcap/tidb/pull/8976)
    -   13の列文字セットの`SHOW CREATE TABLE`をサポートし[＃9053](https://github.com/pingcap/tidb/pull/9053)
    -   [＃8818](https://github.com/pingcap/tidb/pull/8818)のvarcharタイプ列の最大長制限の問題を修正し`utf8mb4`
    -   [＃9093](https://github.com/pingcap/tidb/pull/9093) `ALTER TABLE TRUNCATE TABLE PARTITION`
    -   文字セットが提供されていない場合は、文字セットを解決します[＃9147](https://github.com/pingcap/tidb/pull/9147)

## PD {#pd}

-   リーダー選出に関連するウォッチの問題を修正[＃1396](https://github.com/pingcap/pd/pull/1396)

## TiKV {#tikv}

-   HTTPメソッド[＃3855](https://github.com/tikv/tikv/pull/3855)を使用した監視情報の取得のサポート
-   [＃4075](https://github.com/tikv/tikv/pull/4075)のNULLの問題を修正し`data_format`
-   スキャンリクエストの範囲の確認を追加[＃4124](https://github.com/tikv/tikv/pull/4124)

## ツール {#tools}

-   TiDB Binlog
    -   TiDBの起動中または再起動中の`no available pump`の問題を修正します[＃157](https://github.com/pingcap/tidb-tools/pull/158)
    -   Pumpクライアントログの出力を有効にする[＃165](https://github.com/pingcap/tidb-tools/pull/165)
    -   テーブルに一意のキーのみがあり、主キーがない場合に、NULL値を含む一意のキーによって引き起こされるデータの不整合の問題を修正します。
