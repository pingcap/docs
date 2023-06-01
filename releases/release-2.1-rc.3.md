---
title: TiDB 2.1 RC3 Release Notes
---

# TiDB 2.1 RC3 リリースノート {#tidb-2-1-rc3-release-notes}

2018 年 9 月 29 日に、TiDB 2.1 RC3 がリリースされました。 TiDB 2.1 RC2 と比較して、このリリースでは安定性、互換性、SQL オプティマイザー、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   ステートメントに埋め込み`LEFT OUTER JOIN` [<a href="https://github.com/pingcap/tidb/pull/7689">#7689</a>](https://github.com/pingcap/tidb/pull/7689)が含まれている場合の誤った結果の問題を修正
    -   `JOIN`ステートメントの述語プッシュダウンの最適化ルールを強化[<a href="https://github.com/pingcap/tidb/pull/7645">#7645</a>](https://github.com/pingcap/tidb/pull/7645)
    -   `UnionScan`演算子[<a href="https://github.com/pingcap/tidb/pull/7695">#7695</a>](https://github.com/pingcap/tidb/pull/7695)の述語プッシュダウンの最適化ルールを修正
    -   `Union`演算子の固有キー プロパティが正しく設定されない問題を修正[<a href="https://github.com/pingcap/tidb/pull/7680">#7680</a>](https://github.com/pingcap/tidb/pull/7680)
    -   定数折り込みの最適化ルールを強化[<a href="https://github.com/pingcap/tidb/pull/7696">#7696</a>](https://github.com/pingcap/tidb/pull/7696)
    -   テーブル デュアル[<a href="https://github.com/pingcap/tidb/pull/7756">#7756</a>](https://github.com/pingcap/tidb/pull/7756)への伝播後にフィルターが null になるデータ ソースを最適化します。
-   SQL実行エンジン
    -   トランザクション内の読み取りリクエストのパフォーマンスを最適化する[<a href="https://github.com/pingcap/tidb/pull/7717">#7717</a>](https://github.com/pingcap/tidb/pull/7717)
    -   一部のエグゼキュータでChunkメモリを割り当てるコストを最適化します[<a href="https://github.com/pingcap/tidb/pull/7540">#7540</a>](https://github.com/pingcap/tidb/pull/7540)
    -   ポイントクエリがすべて NULL 値を取得する列によって引き起こされる「インデックスが範囲外」panicを修正します[<a href="https://github.com/pingcap/tidb/pull/7790">#7790</a>](https://github.com/pingcap/tidb/pull/7790)
-   サーバ
    -   設定ファイルのメモリクォータが有効にならない問題を修正[<a href="https://github.com/pingcap/tidb/pull/7729">#7729</a>](https://github.com/pingcap/tidb/pull/7729)
    -   `tidb_force_priority`システム変数を追加して、各ステートメントの実行優先順位を設定します[<a href="https://github.com/pingcap/tidb/pull/7694">#7694</a>](https://github.com/pingcap/tidb/pull/7694)
    -   `admin show slow`ステートメントを使用したスロー クエリ ログ[<a href="https://github.com/pingcap/tidb/pull/7785">#7785</a>](https://github.com/pingcap/tidb/pull/7785)の取得のサポート
-   互換性
    -   `information_schema.schemata` [<a href="https://github.com/pingcap/tidb/pull/7751">#7751</a>](https://github.com/pingcap/tidb/pull/7751)で`charset/collation`の結果が正しくない問題を修正
    -   `hostname`システム変数の値が空である問題を修正します[<a href="https://github.com/pingcap/tidb/pull/7750">#7750</a>](https://github.com/pingcap/tidb/pull/7750)
-   式
    -   `AES_ENCRYPT` / `AES_DECRYPT`組み込み関数[<a href="https://github.com/pingcap/tidb/pull/7425">#7425</a>](https://github.com/pingcap/tidb/pull/7425)で`init_vecter`引数をサポート
    -   一部の式[<a href="https://github.com/pingcap/tidb/pull/7770">#7770</a>](https://github.com/pingcap/tidb/pull/7770)で`Format`の結果が正しくない問題を修正
    -   `JSON_LENGTH`組み込み関数をサポート[<a href="https://github.com/pingcap/tidb/pull/7739">#7739</a>](https://github.com/pingcap/tidb/pull/7739)
    -   符号なし整数型を 10 進数型[<a href="https://github.com/pingcap/tidb/pull/7792">#7792</a>](https://github.com/pingcap/tidb/pull/7792)にキャストするときの誤った結果の問題を修正
-   DML
    -   一意のキー[<a href="https://github.com/pingcap/tidb/pull/7675">#7675</a>](https://github.com/pingcap/tidb/pull/7675)の更新中に`INSERT … ON DUPLICATE KEY UPDATE`ステートメントの結果が正しくない問題を修正します。
-   DDL
    -   タイムスタンプ タイプ[<a href="https://github.com/pingcap/tidb/pull/7724">#7724</a>](https://github.com/pingcap/tidb/pull/7724)の新しい列に新しいインデックスを作成するときに、タイム ゾーン間でインデックス値が変換されない問題を修正します。
    -   列挙型[<a href="https://github.com/pingcap/tidb/pull/7767">#7767</a>](https://github.com/pingcap/tidb/pull/7767)の新しい値の追加をサポート
    -   etcd セッションの迅速な作成をサポートし、ネットワーク分離後のクラスターの可用性を向上させます[<a href="https://github.com/pingcap/tidb/pull/7774">#7774</a>](https://github.com/pingcap/tidb/pull/7774)

## PD {#pd}

-   新機能
    -   逆順でサイズ別にリージョンリストを取得する API を追加します[<a href="https://github.com/pingcap/pd/pull/1254">#1254</a>](https://github.com/pingcap/pd/pull/1254)
-   改善
    -   リージョンAPI [<a href="https://github.com/pingcap/pd/pull/1252">#1252</a>](https://github.com/pingcap/pd/pull/1252)でより詳細な情報を返します。
-   バグ修正
    -   PDがリーダーを切り替えた後、 `adjacent-region-scheduler`がクラッシュを引き起こす可能性がある問題を修正します[<a href="https://github.com/pingcap/pd/pull/1250">#1250</a>](https://github.com/pingcap/pd/pull/1250)

## TiKV {#tikv}

-   パフォーマンス
    -   コプロセッサー要求の同時実行性を最適化する[<a href="https://github.com/tikv/tikv/pull/3515">#3515</a>](https://github.com/tikv/tikv/pull/3515)
-   新機能
    -   ログ関数のサポートを追加[<a href="https://github.com/tikv/tikv/pull/3603">#3603</a>](https://github.com/tikv/tikv/pull/3603)
    -   `sha1`機能[<a href="https://github.com/tikv/tikv/pull/3612">#3612</a>](https://github.com/tikv/tikv/pull/3612)のサポートを追加します。
    -   `truncate_int`機能[<a href="https://github.com/tikv/tikv/pull/3532">#3532</a>](https://github.com/tikv/tikv/pull/3532)のサポートを追加します。
    -   `year`機能[<a href="https://github.com/tikv/tikv/pull/3622">#3622</a>](https://github.com/tikv/tikv/pull/3622)のサポートを追加します。
    -   `truncate_real`機能[<a href="https://github.com/tikv/tikv/pull/3633">#3633</a>](https://github.com/tikv/tikv/pull/3633)のサポートを追加します。
-   バグの修正
    -   時間関数[<a href="https://github.com/tikv/tikv/pull/3487">#3487</a>](https://github.com/tikv/tikv/pull/3487) 、 [<a href="https://github.com/tikv/tikv/pull/3615">#3615</a>](https://github.com/tikv/tikv/pull/3615)に関連するレポート エラー動作を修正しました。
    -   文字列から解析された時間が TiDB [<a href="https://github.com/tikv/tikv/pull/3589">#3589</a>](https://github.com/tikv/tikv/pull/3589)の時間と一致しない問題を修正
