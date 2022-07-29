---
title: TiDB 2.1 RC3 Release Notes
---

# TiDB2.1RC3リリースノート {#tidb-2-1-rc3-release-notes}

2018年9月29日、TiDB2.1RC3がリリースされました。このリリースでは、TiDB 2.1 RC2と比較して、安定性、互換性、SQLオプティマイザー、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   ステートメントに埋め込み`LEFT OUTER JOIN`が含まれている場合の誤った結果の問題を修正し[＃7689](https://github.com/pingcap/tidb/pull/7689)
    -   `JOIN`ステートメント[＃7645](https://github.com/pingcap/tidb/pull/7645)の述語プッシュダウンの最適化ルールを強化します。
    -   `UnionScan`演算子[＃7695](https://github.com/pingcap/tidb/pull/7695)の述語プッシュダウンの最適化ルールを修正します。
    -   `Union`演算子の一意キープロパティが正しく設定されていない問題を修正します[＃7680](https://github.com/pingcap/tidb/pull/7680)
    -   定数畳み込みの最適化ルールを強化する[＃7696](https://github.com/pingcap/tidb/pull/7696)
    -   テーブルデュアル[＃7756](https://github.com/pingcap/tidb/pull/7756)に伝播した後、フィルターがnullであるデータソースを最適化します
-   SQL実行エンジン
    -   トランザクション[＃7717](https://github.com/pingcap/tidb/pull/7717)での読み取り要求のパフォーマンスを最適化する
    -   一部のエグゼキュータでChunkメモリを割り当てるコストを最適化する[＃7540](https://github.com/pingcap/tidb/pull/7540)
    -   ポイントクエリがすべてのNULL値を取得する列によって引き起こされる「インデックスが範囲外」のpanicを修正します[＃7790](https://github.com/pingcap/tidb/pull/7790)
-   サーバ
    -   構成ファイルのメモリクォータが有効にならない問題を修正します[＃7729](https://github.com/pingcap/tidb/pull/7729)
    -   `tidb_force_priority`のシステム変数を追加して、各ステートメントの実行優先度を設定します[＃7694](https://github.com/pingcap/tidb/pull/7694)
    -   `admin show slow`ステートメントを使用して遅いクエリログを取得することをサポート[＃7785](https://github.com/pingcap/tidb/pull/7785)
-   互換性
    -   [＃7751](https://github.com/pingcap/tidb/pull/7751)で`charset/collation`の結果が正しくない問題を修正し`information_schema.schemata`
    -   `hostname`システム変数の値が空であるという問題を修正します[＃7750](https://github.com/pingcap/tidb/pull/7750)
-   式
    -   `AES_ENCRYPT`組み込み関数[＃7425](https://github.com/pingcap/tidb/pull/7425)で`init_vecter`引数をサポートし`AES_DECRYPT`
    -   一部の式で`Format`の結果が正しくない問題を修正します[＃7770](https://github.com/pingcap/tidb/pull/7770)
    -   `JSON_LENGTH`組み込み機能[＃7739](https://github.com/pingcap/tidb/pull/7739)をサポート
    -   符号なし整数型を10進型[＃7792](https://github.com/pingcap/tidb/pull/7792)にキャストするときの誤った結果の問題を修正します
-   DML
    -   一意キー[＃7675](https://github.com/pingcap/tidb/pull/7675)の更新中に`INSERT … ON DUPLICATE KEY UPDATE`ステートメントの結果が正しくないという問題を修正します
-   DDL
    -   タイムスタンプタイプ[＃7724](https://github.com/pingcap/tidb/pull/7724)の新しい列に新しいインデックスを作成すると、タイムゾーン間でインデックス値が変換されない問題を修正します。
    -   列挙型[＃7767](https://github.com/pingcap/tidb/pull/7767)の新しい値の追加をサポート
    -   etcdセッションの迅速な作成をサポートします。これにより、ネットワーク分離後のクラスタの可用性が向上します[＃7774](https://github.com/pingcap/tidb/pull/7774)

## PD {#pd}

-   新機能
    -   APIを追加して、リージョンリストをサイズ別に逆順で取得します[＃1254](https://github.com/pingcap/pd/pull/1254)
-   改善
    -   リージョンで[＃1252](https://github.com/pingcap/pd/pull/1252)詳細な情報を返す
-   バグ修正
    -   PDがリーダー[＃1250](https://github.com/pingcap/pd/pull/1250)を切り替えた後、 `adjacent-region-scheduler`がクラッシュにつながる可能性がある問題を修正します

## TiKV {#tikv}

-   パフォーマンス
    -   コプロセッサー要求の並行性を最適化する[＃3515](https://github.com/tikv/tikv/pull/3515)
-   新機能
    -   ログ関数のサポートを追加する[＃3603](https://github.com/tikv/tikv/pull/3603)
    -   `sha1`機能[＃3612](https://github.com/tikv/tikv/pull/3612)のサポートを追加します
    -   `truncate_int`機能[＃3532](https://github.com/tikv/tikv/pull/3532)のサポートを追加します
    -   `year`機能[＃3622](https://github.com/tikv/tikv/pull/3622)のサポートを追加します
    -   `truncate_real`機能[＃3633](https://github.com/tikv/tikv/pull/3633)のサポートを追加します
-   バグの修正
    -   時間関数[＃3487](https://github.com/tikv/tikv/pull/3487)に関連するレポートエラーの動作を修正し[＃3615](https://github.com/tikv/tikv/pull/3615)た
    -   文字列から解析された時間がTiDB1の時間と矛盾する問題を修正し[＃3589](https://github.com/tikv/tikv/pull/3589)
