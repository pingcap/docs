---
title: TiDB 2.1 RC3 Release Notes
summary: TiDB 2.1 RC3 は、安定性、互換性、SQL オプティマイザー、実行エンジンの改善を伴い、2018 年 9 月 29 日にリリースされました。このリリースには、SQL オプティマイザー、実行エンジン、サーバー、互換性、式、DML、DDL、PD の修正と機能強化が含まれています。TiKV にも、パフォーマンスの最適化、新機能、バグ修正が加えられています。
---

# TiDB 2.1 RC3 リリースノート {#tidb-2-1-rc3-release-notes}

2018 年 9 月 29 日に、TiDB 2.1 RC3 がリリースされました。TiDB 2.1 RC2 と比較して、このリリースでは安定性、互換性、SQL オプティマイザー、実行エンジンが大幅に改善されています。

## ティビ {#tidb}

-   SQL オプティマイザー
    -   文に埋め込み`LEFT OUTER JOIN` [＃7689](https://github.com/pingcap/tidb/pull/7689)が含まれている場合に誤った結果が発生する問題を修正
    -   `JOIN`文[＃7645](https://github.com/pingcap/tidb/pull/7645)の述語プッシュダウンの最適化ルールを強化する
    -   `UnionScan`演算子[＃7695](https://github.com/pingcap/tidb/pull/7695)の述語プッシュダウンの最適化ルールを修正
    -   `Union`演算子の一意のキープロパティが正しく設定されていない問題を修正[＃7680](https://github.com/pingcap/tidb/pull/7680)
    -   定数畳み込みの最適化ルールを強化する[＃7696](https://github.com/pingcap/tidb/pull/7696)
    -   テーブルデュアル[＃7756](https://github.com/pingcap/tidb/pull/7756)への伝播後にフィルターがnullであるデータソースを最適化する
-   SQL実行エンジン
    -   トランザクション[＃7717](https://github.com/pingcap/tidb/pull/7717)における読み取り要求のパフォーマンスを最適化する
    -   一部のエグゼキュータにおけるChunkメモリの割り当てコストを最適化する[＃7540](https://github.com/pingcap/tidb/pull/7540)
    -   ポイントクエリがすべて NULL 値を取得する列によって発生する「インデックスが範囲外」panicを修正[＃7790](https://github.com/pingcap/tidb/pull/7790)
-   サーバ
    -   設定ファイル内のメモリクォータが有効にならない問題を修正[＃7729](https://github.com/pingcap/tidb/pull/7729)
    -   各ステートメントの実行優先度を設定するためのシステム変数`tidb_force_priority`を追加します[＃7694](https://github.com/pingcap/tidb/pull/7694)
    -   `admin show slow`ステートメントを使用してスロークエリログ[＃7785](https://github.com/pingcap/tidb/pull/7785)を取得することをサポートします
-   互換性
    -   `information_schema.schemata` [＃7751](https://github.com/pingcap/tidb/pull/7751)で`charset/collation`の結果が間違っている問題を修正
    -   `hostname`システム変数の値が空になる問題を修正[＃7750](https://github.com/pingcap/tidb/pull/7750)
-   表現
    -   `AES_ENCRYPT` `AES_DECRYPT`関数[＃7425](https://github.com/pingcap/tidb/pull/7425)の`init_vecter`引数をサポート
    -   いくつかの式で`Format`の結果が正しくない問題を修正[＃7770](https://github.com/pingcap/tidb/pull/7770)
    -   `JSON_LENGTH`組み込み関数[＃7739](https://github.com/pingcap/tidb/pull/7739)をサポート
    -   符号なし整数型を小数型[＃7792](https://github.com/pingcap/tidb/pull/7792)にキャストする際の誤った結果の問題を修正
-   DMML の
    -   ユニークキー[＃7675](https://github.com/pingcap/tidb/pull/7675)を更新する際に`INSERT … ON DUPLICATE KEY UPDATE`文の結果が正しくない問題を修正
-   DDL
    -   タイムスタンプ型[＃7724](https://github.com/pingcap/tidb/pull/7724)の新しい列に新しいインデックスを作成するときに、インデックス値がタイムゾーン間で変換されない問題を修正しました。
    -   列挙型[＃7767](https://github.com/pingcap/tidb/pull/7767)に新しい値を追加することをサポート
    -   etcdセッションの迅速な作成をサポートし、ネットワーク分離後のクラスターの可用性を向上します[＃7774](https://github.com/pingcap/tidb/pull/7774)

## PD {#pd}

-   新機能
    -   逆順にサイズ別にリージョンリストを取得する API を追加します[＃1254](https://github.com/pingcap/pd/pull/1254)
-   改善
    -   リージョンAPI [＃1252](https://github.com/pingcap/pd/pull/1252)でより詳細な情報を返す
-   バグ修正
    -   `adjacent-region-scheduler`がリーダーを切り替えた後にクラッシュが発生する可能性がある問題を修正[＃1250](https://github.com/pingcap/pd/pull/1250)

## ティクヴ {#tikv}

-   パフォーマンス
    -   コプロセッサ要求の同時実行を最適化する[＃3515](https://github.com/tikv/tikv/pull/3515)
-   新機能
    -   ログ関数のサポートを追加[＃3603](https://github.com/tikv/tikv/pull/3603)
    -   `sha1`機能[＃3612](https://github.com/tikv/tikv/pull/3612)のサポートを追加
    -   `truncate_int`機能[＃3532](https://github.com/tikv/tikv/pull/3532)のサポートを追加
    -   `year`機能[＃3622](https://github.com/tikv/tikv/pull/3622)のサポートを追加
    -   `truncate_real`機能[＃3633](https://github.com/tikv/tikv/pull/3633)のサポートを追加
-   バグの修正
    -   時間関数[＃3487](https://github.com/tikv/tikv/pull/3487) 、 [＃3615](https://github.com/tikv/tikv/pull/3615)に関連するレポートエラーの動作を修正しました
    -   文字列から解析された時間が TiDB [＃3589](https://github.com/tikv/tikv/pull/3589)の時間と一致しない問題を修正
