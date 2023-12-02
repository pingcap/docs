---
title: TiDB 2.1.3 Release Notes
---

# TiDB 2.1.3 リリースノート {#tidb-2-1-3-release-notes}

2019 年 1 月 28 日に、TiDB 2.1.3 がリリースされました。対応する TiDB Ansible 2.1.3 もリリースされています。 TiDB 2.1.2 と比較して、このリリースではシステムの安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   場合によってはプリペアドプランキャッシュのpanic問題を修正[#8826](https://github.com/pingcap/tidb/pull/8826)
    -   インデックスがプレフィックス インデックス[#8851](https://github.com/pingcap/tidb/pull/8851)の場合に範囲計算が間違っている問題を修正
    -   文字列が不正`TIME`形式の場合は`CAST(str AS TIME(N))` null を返すようにします。 `SQL_MODE`が厳密でない場合は[#8966](https://github.com/pingcap/tidb/pull/8966)
    -   `UPDATE`の処理中に生成されたカラムがpanicになる場合がある問題を修正[#8980](https://github.com/pingcap/tidb/pull/8980)
    -   場合によっては統計ヒストグラムの上限オーバーフローの問題を修正します[#8989](https://github.com/pingcap/tidb/pull/8989)
    -   テーブル全体のスキャンを回避し、クラスターのストレスを軽減するための`_tidb_rowid`構築クエリのサポート範囲[#9059](https://github.com/pingcap/tidb/pull/9059)
    -   `CAST(AS TIME)`精度が大きすぎる場合はエラーを返す[#9058](https://github.com/pingcap/tidb/pull/9058)
    -   デカルト積[#9037](https://github.com/pingcap/tidb/pull/9037)で`Sort Merge Join`使用を許可する
    -   場合によってはpanic後に統計ワーカーが再開できない問題を修正[#9085](https://github.com/pingcap/tidb/pull/9085)
    -   `Sort Merge Join`場合によっては間違った結果を返す問題を修正[#9046](https://github.com/pingcap/tidb/pull/9046)
    -   `CASE`条項[#8355](https://github.com/pingcap/tidb/pull/8355)で JSON タイプを返すサポート
-   サーバ
    -   コメント[#8766](https://github.com/pingcap/tidb/pull/8766)に非 TiDB ヒントが存在する場合、エラーではなく警告を返します。
    -   構成された TIMEZONE 値の有効性を確認します[#8879](https://github.com/pingcap/tidb/pull/8879)
    -   `QueryDurationHistogram`メトリクス項目を最適化して、より多くのステートメント タイプを表示する[#8875](https://github.com/pingcap/tidb/pull/8875)
    -   場合によっては bigint の下限オーバーフローの問題を修正します[#8544](https://github.com/pingcap/tidb/pull/8544)
    -   `ALLOW_INVALID_DATES` SQL モードをサポート[#9110](https://github.com/pingcap/tidb/pull/9110)
-   DDL
    -   MySQL [#8808](https://github.com/pingcap/tidb/pull/8808)の動作との一貫性を保つために`RENAME TABLE`互換性の問題を修正しました。
    -   `ADD INDEX`の同時変更をすぐに有効にするサポート[#8786](https://github.com/pingcap/tidb/pull/8786)
    -   `UPDATE`プロセス中に発生するpanicの問題を修正`ADD COLUMN`場合によっては[#8906](https://github.com/pingcap/tidb/pull/8906)
    -   場合によってはテーブル パーティションが同時に作成される問題を修正[#8902](https://github.com/pingcap/tidb/pull/8902)
    -   `utf8`文字セットから`utf8mb4` [#8951](https://github.com/pingcap/tidb/pull/8951) [#9152](https://github.com/pingcap/tidb/pull/9152)への変換をサポート
    -   シャードビットのオーバーフローの問題を修正[#8976](https://github.com/pingcap/tidb/pull/8976)
    -   `SHOW CREATE TABLE` [#9053](https://github.com/pingcap/tidb/pull/9053)の列文字セットの出力をサポート
    -   `utf8mb4` [#8818](https://github.com/pingcap/tidb/pull/8818)の varchar 型カラムの最大長制限の問題を修正
    -   サポート`ALTER TABLE TRUNCATE TABLE PARTITION` [#9093](https://github.com/pingcap/tidb/pull/9093)
    -   文字セットが提供されていない場合に文字セットを解決する[#9147](https://github.com/pingcap/tidb/pull/9147)

## PD {#pd}

-   リーダー選挙[#1396](https://github.com/pingcap/pd/pull/1396)に関連する Watch の問題を修正

## TiKV {#tikv}

-   HTTPメソッドを使用した監視情報の取得をサポート[#3855](https://github.com/tikv/tikv/pull/3855)
-   `data_format` [#4075](https://github.com/tikv/tikv/pull/4075)の NULL 問題を修正
-   スキャン要求の範囲の検証を追加[#4124](https://github.com/tikv/tikv/pull/4124)

## ツール {#tools}

-   TiDBBinlog
    -   TiDB の起動中または再起動中の`no available pump`問題を修正します[#157](https://github.com/pingcap/tidb-tools/pull/158)
    -   Pumpクライアント ログの出力を有効にする[#165](https://github.com/pingcap/tidb-tools/pull/165)
    -   テーブルに一意キーのみがあり、主キーがない場合に、NULL 値を含む一意キーによって引き起こされるデータの不整合の問題を修正します。
