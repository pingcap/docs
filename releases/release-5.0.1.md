---
title: TiDB 5.0.1 Release Notes
---

# TiDB5.0.1リリースノート {#tidb-5-0-1-release-notes}

発売日：2021年4月24日

TiDBバージョン：5.0.1

## 互換性の変更 {#compatibility-change}

-   `committer-concurrency`構成項目のデフォルト値が`16`から`128`に変更されました。

## 改善 {#improvements}

-   TiDB

    -   組み込み機能をサポートする`VITESS_HASH()` [＃23915](https://github.com/pingcap/tidb/pull/23915)

-   TiKV

    -   `zstd`を使用してリージョンスナップショット[＃10005](https://github.com/tikv/tikv/pull/10005)を圧縮します

-   PD

    -   地域スコア計算機を変更して、異性の店舗をより満足させる[＃3605](https://github.com/pingcap/pd/pull/3605)
    -   `scatter region`スケジューラーを追加した後の予期しない統計を回避する[＃3602](https://github.com/pingcap/pd/pull/3602)

-   ツール

    -   バックアップと復元（BR）

        -   要約ログから誤解を招く情報を削除する[＃1009](https://github.com/pingcap/br/pull/1009)

## バグの修正 {#bug-fixes}

-   TiDB

    -   投影結果が空の場合、プロジェクト除去の実行結果が間違っている可能性がある問題を修正します[＃24093](https://github.com/pingcap/tidb/pull/24093)
    -   列に`NULL`の値が含まれている場合の誤ったクエリ結果の問題を修正します[＃24063](https://github.com/pingcap/tidb/pull/24063)
    -   スキャンに仮想列が含まれている場合にMPPプランの生成を禁止する[＃24058](https://github.com/pingcap/tidb/pull/24058)
    -   プランキャッシュ[＃24043](https://github.com/pingcap/tidb/pull/24043)での`PointGet`と`TableDual`の誤った再利用を修正
    -   オプティマイザーがクラスター化インデックスの`IndexMerge`プランを作成するときに発生するエラーを修正します[＃24042](https://github.com/pingcap/tidb/pull/24042)
    -   BITタイプエラーのタイプ推論を修正します[＃24027](https://github.com/pingcap/tidb/pull/24027)
    -   `PointGet`演算子が存在する場合に一部のオプティマイザヒントが有効にならない問題を修正します[＃23685](https://github.com/pingcap/tidb/pull/23685)
    -   エラー[＃24080](https://github.com/pingcap/tidb/pull/24080)が原因でロールバック時にDDL操作が失敗する可能性がある問題を修正します
    -   バイナリリテラル定数のインデックス範囲が正しく構築されない問題を修正します[＃24041](https://github.com/pingcap/tidb/pull/24041)
    -   場合によっては`IN`句の潜在的な誤った結果を修正します[＃24023](https://github.com/pingcap/tidb/pull/24023)
    -   一部の文字列関数の誤った結果を修正する[＃23879](https://github.com/pingcap/tidb/pull/23879)
    -   ユーザーは、 `REPLACE`の操作を実行するために、テーブルに対して`INSERT`と`DELETE`の両方の特権が必要になります[＃23939](https://github.com/pingcap/tidb/pull/23939)
    -   ポイントクエリ[＃24070](https://github.com/pingcap/tidb/pull/24070)を実行する際のパフォーマンスの低下を修正する
    -   バイナリとバイト[＃23918](https://github.com/pingcap/tidb/pull/23918)を誤って比較することによって引き起こされた間違った`TableDual`プランを修正します

-   TiKV

    -   コプロセッサーが`IN`式[＃10018](https://github.com/tikv/tikv/pull/10018)の符号付きまたは符号なし整数型を適切に処理できない問題を修正します。
    -   SSTファイルをバッチ取り込みした後の多くの空のリージョンの問題を修正します[＃10015](https://github.com/tikv/tikv/pull/10015)
    -   `cast_string_as_time`の入力が無効なUTF-8バイト[＃9995](https://github.com/tikv/tikv/pull/9995)の場合に発生する可能性のあるpanicを修正します。
    -   ファイル辞書ファイルが破損した後にTiKVが起動できないバグを修正します[＃9992](https://github.com/tikv/tikv/pull/9992)

-   TiFlash

    -   ストレージエンジンが一部の範囲のデータを削除できない問題を修正します
    -   時間型を整数型にキャストするときの誤った結果の問題を修正します
    -   `receiver`が10秒以内に対応するタスクを見つけることができないバグを修正します
    -   `cancelMPPQuery`に無効なイテレータが存在する可能性があるという問題を修正します
    -   `bitwise`演算子の動作がTiDBの動作と異なるバグを修正します
    -   `prefix key`を使用するときに範囲が重複することによって発生するアラートの問題を修正します
    -   文字列型を整数型にキャストするときの誤った結果の問題を修正します
    -   連続した高速書き込みによってTiFlashのメモリが不足する可能性がある問題を修正します
    -   列名が重複するとTiFlashでエラーが発生する問題を修正します
    -   TiFlashがMPPプランの解析に失敗する問題を修正します
    -   テーブルGC中にnullポインタの例外が発生する可能性があるという潜在的な問題を修正します
    -   ドロップされたテーブルにデータを書き込むときに発生するTiFlashpanicの問題を修正します
    -   BRの復元中にTiFlashがpanicになる可能性がある問題を修正します

-   ツール

    -   TiDB Lightning

        -   インポート中の進行状況ログの不正確なテーブルカウントの問題を修正します[＃1005](https://github.com/pingcap/br/pull/1005)

    -   バックアップと復元（BR）

        -   実際のバックアップ速度が`--ratelimit`の制限を超えるバグを修正します[＃1026](https://github.com/pingcap/br/pull/1026)
        -   いくつかのTiKVノードの障害によって引き起こされるバックアップ中断の問題を修正します[＃1019](https://github.com/pingcap/br/pull/1019)
        -   TiDBLightningのインポート中の進行状況ログの不正確なテーブルカウントの問題を修正します[＃1005](https://github.com/pingcap/br/pull/1005)

    -   TiCDC

        -   Unified Sorterの同時実行の問題を修正し、役に立たないエラーメッセージをフィルタリングします[＃1678](https://github.com/pingcap/tiflow/pull/1678)
        -   冗長ディレクトリの作成がMinIO1でのレプリケーションを中断する可能性があるバグを修正し[＃1672](https://github.com/pingcap/tiflow/pull/1672)
        -   `explicit_defaults_for_timestamp`セッション変数のデフォルト値を`ON`に設定して、 MySQL 5.7ダウンストリームがアップストリームTiDB5と同じ動作を維持するようにし[＃1659](https://github.com/pingcap/tiflow/pull/1659) 。
        -   `io.EOF`を誤って処理すると、レプリケーションが中断される可能性があるという問題を修正します[＃1648](https://github.com/pingcap/tiflow/pull/1648)
        -   TiCDCダッシュボードのTiKVCDCエンドポイントCPUメトリックを修正します[＃1645](https://github.com/pingcap/tiflow/pull/1645)
        -   場合によってはレプリケーションのブロックを回避するために`defaultBufferChanSize`を増やします[＃1632](https://github.com/pingcap/tiflow/pull/1632)
