---
title: TiDB 2.1.3 Release Notes
summary: TiDB 2.1.3 および TiDB Ansible 2.1.3 がリリースされ、システムの安定性、SQL オプティマイザー、統計、および実行エンジンが改善されました。修正には、 プリペアドプランキャッシュ、Range コンピューティング、`CAST(str AS TIME(N))`、Generated カラム、統計ヒストグラム、`Sort Merge Join` などの問題が含まれます。その他の改善には、`_tidb_rowid` 構築クエリの範囲のサポート、`ALLOW_INVALID_DATES` SQL モードなどが含まれます。PD および TiKV にも修正と改善が加えられています。TiDB Binlog は、 Pumpクライアント ログの問題と、NULL 値を含む一意のキーによって発生するデータの不整合を修正します。
---

# TiDB 2.1.3 リリースノート {#tidb-2-1-3-release-notes}

2019 年 1 月 28 日に、TiDB 2.1.3 がリリースされました。対応する TiDB Ansible 2.1.3 もリリースされました。TiDB 2.1.2 と比較して、このリリースでは、システムの安定性、SQL オプティマイザー、統計情報、実行エンジンが大幅に改善されています。

## ティビ {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   一部のケースでプリペアドプランキャッシュのpanic問題を修正[＃8826](https://github.com/pingcap/tidb/pull/8826)
    -   インデックスがプレフィックスインデックスの場合に範囲計算が間違っている問題を修正[＃8851](https://github.com/pingcap/tidb/pull/8851)
    -   `SQL_MODE`が厳密でない場合に文字列が不正な`TIME`形式の場合、 `CAST(str AS TIME(N))` nullを返すようにする[＃8966](https://github.com/pingcap/tidb/pull/8966)
    -   `UPDATE`の処理中に生成されるカラムがpanic問題を修正[＃8980](https://github.com/pingcap/tidb/pull/8980)
    -   いくつかのケースにおける統計ヒストグラムの上限オーバーフロー問題を修正[＃8989](https://github.com/pingcap/tidb/pull/8989)
    -   `_tidb_rowid`構築クエリの範囲をサポートし、テーブル全体のスキャンを回避してクラスターのストレスを軽減します[＃9059](https://github.com/pingcap/tidb/pull/9059)
    -   `CAST(AS TIME)`精度が大きすぎる場合はエラーを返す[＃9058](https://github.com/pingcap/tidb/pull/9058)
    -   直積[＃9037](https://github.com/pingcap/tidb/pull/9037)で`Sort Merge Join`使用を許可する
    -   panic後に統計ワーカーが再開できないことがある問題を修正[＃9085](https://github.com/pingcap/tidb/pull/9085)
    -   `Sort Merge Join`場合によっては間違った結果が返される問題を修正[＃9046](https://github.com/pingcap/tidb/pull/9046)
    -   `CASE`節[＃8355](https://github.com/pingcap/tidb/pull/8355)でJSON型を返すことをサポート
-   サーバ
    -   コメント[＃8766](https://github.com/pingcap/tidb/pull/8766)に非TiDBヒントが存在する場合、エラーではなく警告を返します。
    -   設定されたTIMEZONE値[＃8879](https://github.com/pingcap/tidb/pull/8879)の有効性を確認する
    -   `QueryDurationHistogram`メトリック項目を最適化して、より多くのステートメント タイプを表示する[＃8875](https://github.com/pingcap/tidb/pull/8875)
    -   一部のケースにおける bigint の下限オーバーフローの問題を修正[＃8544](https://github.com/pingcap/tidb/pull/8544)
    -   `ALLOW_INVALID_DATES` SQLモード[＃9110](https://github.com/pingcap/tidb/pull/9110)サポート
-   DDL
    -   MySQL [＃8808](https://github.com/pingcap/tidb/pull/8808)の動作と一貫性を保つために`RENAME TABLE`互換性問題を修正しました。
    -   `ADD INDEX`の同時変更をすぐに有効にする[＃8786](https://github.com/pingcap/tidb/pull/8786)
    -   `ADD COLUMN`のプロセス中に発生する`UPDATE`panic問題を修正する (場合によっては[＃8906](https://github.com/pingcap/tidb/pull/8906)
    -   一部のケースでテーブルパーティションが同時に作成される問題を修正[＃8902](https://github.com/pingcap/tidb/pull/8902)
    -   `utf8`文字セットを`utf8mb4` [＃8951](https://github.com/pingcap/tidb/pull/8951) [＃9152](https://github.com/pingcap/tidb/pull/9152)に変換するサポート
    -   シャードビットオーバーフローの問題を修正[＃8976](https://github.com/pingcap/tidb/pull/8976)
    -   `SHOW CREATE TABLE` [＃9053](https://github.com/pingcap/tidb/pull/9053)の列文字セットの出力をサポート
    -   `utf8mb4` [＃8818](https://github.com/pingcap/tidb/pull/8818)のvarchar型列の最大長制限の問題を修正
    -   サポート`ALTER TABLE TRUNCATE TABLE PARTITION` [＃9093](https://github.com/pingcap/tidb/pull/9093)
    -   文字セットが指定されていない場合は文字セットを解決する[＃9147](https://github.com/pingcap/tidb/pull/9147)

## PD {#pd}

-   リーダー選挙に関連するウォッチの問題を修正[＃1396](https://github.com/pingcap/pd/pull/1396)

## ティクヴ {#tikv}

-   HTTPメソッド[＃3855](https://github.com/tikv/tikv/pull/3855)を使用した監視情報の取得をサポート
-   `data_format` [＃4075](https://github.com/tikv/tikv/pull/4075)のNULL問題を修正
-   スキャン要求の範囲の検証を追加[＃4124](https://github.com/tikv/tikv/pull/4124)

## ツール {#tools}

-   TiDBBinlog
    -   TiDBの起動または再起動中に発生する`no available pump`問題を修正する[＃157](https://github.com/pingcap/tidb-tools/pull/158)
    -   Pumpクライアントログ[＃165](https://github.com/pingcap/tidb-tools/pull/165)出力を有効にする
    -   テーブルに一意キーのみがあり、主キーがない場合に、一意キーに NULL 値が含まれることで発生するデータの不整合の問題を修正しました。
