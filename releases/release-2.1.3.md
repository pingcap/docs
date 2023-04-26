---
title: TiDB 2.1.3 Release Notes
---

# TiDB 2.1.3 リリースノート {#tidb-2-1-3-release-notes}

2019 年 1 月 28 日に、TiDB 2.1.3 がリリースされました。対応する TiDB Ansible 2.1.3 もリリースされています。 TiDB 2.1.2 と比較すると、このリリースでは、システムの安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   場合によっては、 プリペアドプランキャッシュのpanic問題を修正します[#8826](https://github.com/pingcap/tidb/pull/8826)
    -   インデックスがプレフィックス インデックス[#8851](https://github.com/pingcap/tidb/pull/8851)の場合、Range 計算が正しくない問題を修正します。
    -   `SQL_MODE`が厳密でない場合、文字列が不正な`TIME`形式の場合、 `CAST(str AS TIME(N))` null を返すようにする[#8966](https://github.com/pingcap/tidb/pull/8966)
    -   場合によっては`UPDATE`の処理中に生成されたカラムがpanicになる問題を修正します[#8980](https://github.com/pingcap/tidb/pull/8980)
    -   場合によっては統計ヒストグラムの上限オーバーフローの問題を修正します[#8989](https://github.com/pingcap/tidb/pull/8989)
    -   フル テーブル スキャンを回避し、クラスタ ストレスを軽減するための`_tidb_rowid`構築クエリのサポート範囲[#9059](https://github.com/pingcap/tidb/pull/9059)
    -   `CAST(AS TIME)`精度が大きすぎる場合にエラーを返す[#9058](https://github.com/pingcap/tidb/pull/9058)
    -   デカルト積[#9037](https://github.com/pingcap/tidb/pull/9037)で`Sort Merge Join`使用を許可する
    -   場合によっては、panic後に統計ワーカーが再開できない問題を修正します[#9085](https://github.com/pingcap/tidb/pull/9085)
    -   `Sort Merge Join`場合によっては間違った結果を返す問題を修正[#9046](https://github.com/pingcap/tidb/pull/9046)
    -   `CASE`節[#8355](https://github.com/pingcap/tidb/pull/8355)で JSON 型を返すサポート
-   サーバ
    -   TiDB 以外のヒントがコメントに存在する場合、エラーではなく警告を返します[#8766](https://github.com/pingcap/tidb/pull/8766)
    -   設定された TIMEZONE 値[#8879](https://github.com/pingcap/tidb/pull/8879)の有効性を確認します
    -   `QueryDurationHistogram`メトリクス アイテムを最適化して、より多くのステートメント タイプを表示する[#8875](https://github.com/pingcap/tidb/pull/8875)
    -   場合によっては bigint の下限オーバーフローの問題を修正します[#8544](https://github.com/pingcap/tidb/pull/8544)
    -   `ALLOW_INVALID_DATES` SQL モード[#9110](https://github.com/pingcap/tidb/pull/9110)をサポート
-   DDL
    -   `RENAME TABLE`互換性の問題を修正して、MySQL [#8808](https://github.com/pingcap/tidb/pull/8808)の動作と一貫した動作を維持します。
    -   同時変更のサポート`ADD INDEX`すぐに有効になる[#8786](https://github.com/pingcap/tidb/pull/8786)
    -   場合によっては`ADD COLUMN`プロセス中に`UPDATE`panicの問題を修正します[#8906](https://github.com/pingcap/tidb/pull/8906)
    -   場合によってはテーブル パーティションを同時に作成する問題を修正します[#8902](https://github.com/pingcap/tidb/pull/8902)
    -   `utf8`文字セットから`utf8mb4` [#8951](https://github.com/pingcap/tidb/pull/8951) [#9152](https://github.com/pingcap/tidb/pull/9152)への変換をサポート
    -   シャードビットのオーバーフローの問題を修正[#8976](https://github.com/pingcap/tidb/pull/8976)
    -   列文字セットの出力を`SHOW CREATE TABLE` [#9053](https://github.com/pingcap/tidb/pull/9053)でサポート
    -   `utf8mb4` [#8818](https://github.com/pingcap/tidb/pull/8818)の varchar 型列の最大長制限の問題を修正します。
    -   サポート`ALTER TABLE TRUNCATE TABLE PARTITION` [#9093](https://github.com/pingcap/tidb/pull/9093)
    -   文字セットが提供されていない場合に文字セットを解決する[#9147](https://github.com/pingcap/tidb/pull/9147)

## PD {#pd}

-   リーダー選挙[#1396](https://github.com/pingcap/pd/pull/1396)に関連するウォッチの問題を修正

## TiKV {#tikv}

-   HTTPメソッド[#3855](https://github.com/tikv/tikv/pull/3855)を使用した監視情報の取得をサポート
-   `data_format` [#4075](https://github.com/tikv/tikv/pull/4075)の NULL の問題を修正
-   スキャン要求の範囲の検証を追加[#4124](https://github.com/tikv/tikv/pull/4124)

## ツール {#tools}

-   TiDBBinlog
    -   TiDB の起動中または再起動中の`no available pump`問題を修正[#157](https://github.com/pingcap/tidb-tools/pull/158)
    -   Pumpクライアント ログ[#165](https://github.com/pingcap/tidb-tools/pull/165)の出力を有効にする
    -   テーブルに一意のキーのみがあり、主キーがない場合に、NULL 値を含む一意のキーによって引き起こされるデータの不整合の問題を修正します。
