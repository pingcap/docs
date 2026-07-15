---
title: TiDB 2.1 RC3 Release Notes
summary: TiDB 2.1 RC3は2018年9月29日にリリースされ、安定性、互換性、SQLオプティマイザ、実行エンジンが改善されました。このリリースには、SQLオプティマイザ、実行エンジン、サーバー、互換性、式、DML、DDL、PDに関する修正と機能強化が含まれています。TiKVにもパフォーマンスの最適化、新機能、バグ修正が施されています。
---

# TiDB 2.1 RC3 リリースノート {#tidb-2-1-rc3-release-notes}

2018年9月29日にTiDB 2.1 RC3がリリースされました。このリリースでは、TiDB 2.1 RC2と比較して、安定性、互換性、SQLオプティマイザー、実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   文に埋め込み`LEFT OUTER JOIN` が含まれている場合の誤った結果の問題を修正しました [＃7689](https://github.com/pingcap/tidb/pull/7689)
    -   `JOIN`文の述語プッシュダウンの最適化ルールを強化する [＃7645](https://github.com/pingcap/tidb/pull/7645)
    -   `UnionScan`演算子述語プッシュダウンの最適化ルールを修正 [＃7695](https://github.com/pingcap/tidb/pull/7695)
    -   `Union`演算子の一意のキープロパティが正しく設定されていない問題を修正[＃7680](https://github.com/pingcap/tidb/pull/7680)
    -   定数畳み込みの最適化ルールの強化[＃7696](https://github.com/pingcap/tidb/pull/7696)
    -   テーブルデュアルへの伝播後にフィルターがnullになるデータソースを最適化します [＃7756](https://github.com/pingcap/tidb/pull/7756)
-   SQL実行エンジン
    -   トランザクションにおける読み取り要求のパフォーマンスを最適化する [＃7717](https://github.com/pingcap/tidb/pull/7717)
    -   一部のエグゼキュータにおけるChunkメモリの割り当てコストを最適化する[＃7540](https://github.com/pingcap/tidb/pull/7540)
    -   ポイントクエリですべての NULL 値が取得される列によって発生する「インデックス範囲外」panicを修正[＃7790](https://github.com/pingcap/tidb/pull/7790)
-   サーバ
    -   設定ファイル内のメモリクォータが有効にならない問題を修正[＃7729](https://github.com/pingcap/tidb/pull/7729)
    -   各ステートメント実行優先度を設定するためのシステム変数`tidb_force_priority`追加します。 [＃7694](https://github.com/pingcap/tidb/pull/7694)
    -   `admin show slow`文を使用してスロークエリログを取得することをサポートします [＃7785](https://github.com/pingcap/tidb/pull/7785)
-   互換性
    -   `information_schema.schemata` で`charset/collation`の結果が正しくない問題を修正 [＃7751](https://github.com/pingcap/tidb/pull/7751)
    -   `hostname`システム変数の値が空になる問題を修正[＃7750](https://github.com/pingcap/tidb/pull/7750)
-   表現
    -   `AES_ENCRYPT` `AES_DECRYPT`関数の`init_vecter`引数をサポート [＃7425](https://github.com/pingcap/tidb/pull/7425)
    -   `Format`の結果が一部の式で正しくない問題を修正[＃7770](https://github.com/pingcap/tidb/pull/7770)
    -   `JSON_LENGTH`組み込み関数サポート [＃7739](https://github.com/pingcap/tidb/pull/7739)
    -   符号なし整数型を小数型にキャストする際の誤った結果の問題を修正 [＃7792](https://github.com/pingcap/tidb/pull/7792)
-   DML
    -   一意キーを更新する際に`INSERT … ON DUPLICATE KEY UPDATE`文の結果が正しくない問題を修正 [＃7675](https://github.com/pingcap/tidb/pull/7675)
-   DDL
    -   タイムスタンプ型の新しい列に新しいインデックスを作成するときに、インデックス値がタイムゾーン間で変換されない問題を修正しました。 [＃7724](https://github.com/pingcap/tidb/pull/7724)
    -   列挙型に新しい値を追加することをサポート [＃7767](https://github.com/pingcap/tidb/pull/7767)
    -   etcdセッションの迅速な作成をサポートし、ネットワーク分離後のクラスタの可用性を向上します[＃7774](https://github.com/pingcap/tidb/pull/7774)

## PD {#pd}

-   新機能
    -   逆順にリージョンリストを取得するAPIを追加する[＃1254](https://github.com/pingcap/pd/pull/1254)
-   改善
    -   リージョン API でより詳細な情報を返す [＃1252](https://github.com/pingcap/pd/pull/1252)
-   バグ修正
    -   PDがリーダーを切り替えた後に`adjacent-region-scheduler`が発生する可能性がある問題を修正[＃1250](https://github.com/pingcap/pd/pull/1250)

## TiKV {#tikv}

-   パフォーマンス
    -   コプロセッサ要求の同時実行を最適化する[＃3515](https://github.com/tikv/tikv/pull/3515)
-   新機能
    -   ログ関数のサポートを追加[＃3603](https://github.com/tikv/tikv/pull/3603)
    -   `sha1`関数サポートを追加 [＃3612](https://github.com/tikv/tikv/pull/3612)
    -   `truncate_int`関数サポートを追加 [＃3532](https://github.com/tikv/tikv/pull/3532)
    -   `year`関数サポートを追加 [＃3622](https://github.com/tikv/tikv/pull/3622)
    -   `truncate_real`関数サポートを追加 [＃3633](https://github.com/tikv/tikv/pull/3633)
-   バグ修正
    -   時間関数に関連するレポートエラーの動作修正しました [＃3487](https://github.com/tikv/tikv/pull/3487) [＃3615](https://github.com/tikv/tikv/pull/3615)
    -   文字列から解析した時間が TiDB 時間と一致しない問題を修正しました [＃3589](https://github.com/tikv/tikv/pull/3589)
