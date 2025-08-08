---
title: TiDB 2.1 RC3 Release Notes
summary: TiDB 2.1 RC3は2018年9月29日にリリースされ、安定性、互換性、SQLオプティマイザ、実行エンジンが改善されました。このリリースには、SQLオプティマイザ、実行エンジン、サーバー、互換性、式、DML、DDL、PDに関する修正と機能強化が含まれています。TiKVにもパフォーマンスの最適化、新機能、バグ修正が施されています。
---

# TiDB 2.1 RC3 リリースノート {#tidb-2-1-rc3-release-notes}

2018年9月29日にTiDB 2.1 RC3がリリースされました。このリリースでは、TiDB 2.1 RC2と比較して、安定性、互換性、SQLオプティマイザー、実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   文に埋め込み`LEFT OUTER JOIN` [＃7689](https://github.com/pingcap/tidb/pull/7689)が含まれている場合の誤った結果の問題を修正しました
    -   `JOIN`文[＃7645](https://github.com/pingcap/tidb/pull/7645)の述語プッシュダウンの最適化ルールを強化する
    -   `UnionScan`演算子[＃7695](https://github.com/pingcap/tidb/pull/7695)述語プッシュダウンの最適化ルールを修正
    -   `Union`演算子の一意のキープロパティが正しく設定されていない問題を修正[＃7680](https://github.com/pingcap/tidb/pull/7680)
    -   定数畳み込みの最適化ルールの強化[＃7696](https://github.com/pingcap/tidb/pull/7696)
    -   テーブルデュアル[＃7756](https://github.com/pingcap/tidb/pull/7756)への伝播後にフィルターがnullになるデータソースを最適化します
-   SQL実行エンジン
    -   トランザクション[＃7717](https://github.com/pingcap/tidb/pull/7717)における読み取り要求のパフォーマンスを最適化する
    -   一部のエグゼキュータにおけるChunkメモリの割り当てコストを最適化する[＃7540](https://github.com/pingcap/tidb/pull/7540)
    -   ポイントクエリですべての NULL 値が取得される列によって発生する「インデックス範囲外」panicを修正[＃7790](https://github.com/pingcap/tidb/pull/7790)
-   サーバ
    -   設定ファイル内のメモリクォータが有効にならない問題を修正[＃7729](https://github.com/pingcap/tidb/pull/7729)
    -   各ステートメント[＃7694](https://github.com/pingcap/tidb/pull/7694)実行優先度を設定するためのシステム変数`tidb_force_priority`追加します。
    -   `admin show slow`文を使用してスロークエリログ[＃7785](https://github.com/pingcap/tidb/pull/7785)を取得することをサポートします
-   互換性
    -   `information_schema.schemata` [＃7751](https://github.com/pingcap/tidb/pull/7751)で`charset/collation`の結果が正しくない問題を修正
    -   `hostname`システム変数の値が空になる問題を修正[＃7750](https://github.com/pingcap/tidb/pull/7750)
-   表現
    -   `AES_ENCRYPT` `AES_DECRYPT`関数[＃7425](https://github.com/pingcap/tidb/pull/7425)の`init_vecter`引数をサポート
    -   `Format`の結果が一部の式で正しくない問題を修正[＃7770](https://github.com/pingcap/tidb/pull/7770)
    -   `JSON_LENGTH`組み込み関数[＃7739](https://github.com/pingcap/tidb/pull/7739)サポート
    -   符号なし整数型を小数型[＃7792](https://github.com/pingcap/tidb/pull/7792)にキャストする際の誤った結果の問題を修正
-   DML
    -   ユニークキー[＃7675](https://github.com/pingcap/tidb/pull/7675)を更新する際に`INSERT … ON DUPLICATE KEY UPDATE`文の結果が正しくない問題を修正
-   DDL
    -   タイムスタンプ型[＃7724](https://github.com/pingcap/tidb/pull/7724)の新しい列に新しいインデックスを作成するときに、インデックス値がタイムゾーン間で変換されない問題を修正しました。
    -   列挙型[＃7767](https://github.com/pingcap/tidb/pull/7767)に新しい値を追加することをサポート
    -   etcdセッションの迅速な作成をサポートし、ネットワーク分離後のクラスタの可用性を向上します[＃7774](https://github.com/pingcap/tidb/pull/7774)

## PD {#pd}

-   新機能
    -   逆順にリージョンリストを取得するAPIを追加する[＃1254](https://github.com/pingcap/pd/pull/1254)
-   改善
    -   リージョン API [＃1252](https://github.com/pingcap/pd/pull/1252)でより詳細な情報を返す
-   バグ修正
    -   PDがリーダーを切り替えた後に`adjacent-region-scheduler`が発生する可能性がある問題を修正[＃1250](https://github.com/pingcap/pd/pull/1250)

## TiKV {#tikv}

-   パフォーマンス
    -   コプロセッサ要求の同時実行を最適化する[＃3515](https://github.com/tikv/tikv/pull/3515)
-   新機能
    -   ログ関数のサポートを追加[＃3603](https://github.com/tikv/tikv/pull/3603)
    -   `sha1`関数[＃3612](https://github.com/tikv/tikv/pull/3612)サポートを追加
    -   `truncate_int`関数[＃3532](https://github.com/tikv/tikv/pull/3532)サポートを追加
    -   `year`関数[＃3622](https://github.com/tikv/tikv/pull/3622)サポートを追加
    -   `truncate_real`関数[＃3633](https://github.com/tikv/tikv/pull/3633)サポートを追加
-   バグ修正
    -   時間関数[＃3487](https://github.com/tikv/tikv/pull/3487)に関連するレポートエラーの動作[＃3615](https://github.com/tikv/tikv/pull/3615)修正しました
    -   文字列から解析した時間が TiDB [＃3589](https://github.com/tikv/tikv/pull/3589)時間と一致しない問題を修正しました
