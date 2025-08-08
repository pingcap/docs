---
title: TiDB 5.0.1 Release Notes
summary: TiDB 5.0.1は2021年4月24日にリリースされました。committer-concurrency`のデフォルト値が128に変更されました。TiDB、TiKV、PD、 TiFlash、およびツールに様々なバグ修正と改善が行われました。例えば、TiDBではクエリ結果とパフォーマンスの低下に関する問題が修正され、TiKVではコプロセッサと起動エラーに関する問題が修正されました。TiDB TiDB LightningやBackup & Restoreなどのツールにもバグ修正が行われました。
---

# TiDB 5.0.1 リリースノート {#tidb-5-0-1-release-notes}

発売日：2021年4月24日

TiDB バージョン: 5.0.1

## 互換性の変更 {#compatibility-change}

-   `committer-concurrency`構成項目のデフォルト値が`16`から`128`に変更されます。

## 改善点 {#improvements}

-   TiDB

    -   組み込み関数`VITESS_HASH()` [＃23915](https://github.com/pingcap/tidb/pull/23915)をサポート

-   TiKV

    -   `zstd`使用してリージョンスナップショット[＃10005](https://github.com/tikv/tikv/pull/10005)を圧縮します

-   PD

    -   異性体ストア[＃3605](https://github.com/pingcap/pd/pull/3605)より適切に満たすようにリージョンスコア計算機を修正する
    -   `scatter region`スケジューラ[＃3602](https://github.com/pingcap/pd/pull/3602)追加した後の予期しない統計を回避する

-   ツール

    -   バックアップと復元 (BR)

        -   要約ログ[＃1009](https://github.com/pingcap/br/pull/1009)から誤解を招く情報を削除する

## バグ修正 {#bug-fixes}

-   TiDB

    -   投影結果が空の場合にプロジェクト除去の実行結果が間違っている可能性がある問題を修正[＃24093](https://github.com/pingcap/tidb/pull/24093)
    -   列に`NULL`値が含まれている場合に間違ったクエリ結果が表示される問題を修正しました[＃24063](https://github.com/pingcap/tidb/pull/24063)
    -   スキャンに仮想列[＃24058](https://github.com/pingcap/tidb/pull/24058)が含まれている場合、MPP プランの生成を禁止します。
    -   プランキャッシュ[＃24043](https://github.com/pingcap/tidb/pull/24043)の`PointGet`と`TableDual`の誤った再利用を修正
    -   オプティマイザがクラスタ化インデックス[＃24042](https://github.com/pingcap/tidb/pull/24042) `IndexMerge`プランを構築するときに発生するエラーを修正します
    -   BIT型エラーの型推論を修正[＃24027](https://github.com/pingcap/tidb/pull/24027)
    -   `PointGet`演算子が存在する場合に一部のオプティマイザヒントが有効にならない問題を修正[＃23685](https://github.com/pingcap/tidb/pull/23685)
    -   エラー[＃24080](https://github.com/pingcap/tidb/pull/24080)によりロールバック時にDDL操作が失敗する可能性がある問題を修正
    -   バイナリリテラル定数のインデックス範囲が正しく構築されない問題を修正[＃24041](https://github.com/pingcap/tidb/pull/24041)
    -   いくつかのケースで`IN`節の潜在的な誤った結果を修正[＃24023](https://github.com/pingcap/tidb/pull/24023)
    -   いくつかの文字列関数の誤った結果を修正[＃23879](https://github.com/pingcap/tidb/pull/23879)
    -   ユーザーは、テーブルに対して`REPLACE`操作を実行するために`INSERT`と`DELETE`両方の権限が必要になります[＃23939](https://github.com/pingcap/tidb/pull/23939)
    -   ポイントクエリ[＃24070](https://github.com/pingcap/tidb/pull/24070)を実行する際のパフォーマンスの低下を修正
    -   バイナリとバイトを誤って比較することによって発生した間違った`TableDual`計画を修正[＃23918](https://github.com/pingcap/tidb/pull/23918)

-   TiKV

    -   コプロセッサが`IN`式[＃10018](https://github.com/tikv/tikv/pull/10018)の符号付きまたは符号なし整数型を適切に処理できない問題を修正しました。
    -   SST ファイルのバッチ取り込み後に多くの空の領域が発生する問題を修正[＃10015](https://github.com/tikv/tikv/pull/10015)
    -   `cast_string_as_time`の入力が無効なUTF-8バイトである場合に発生する潜在的なpanicを修正[＃9995](https://github.com/tikv/tikv/pull/9995)
    -   ファイル辞書ファイルが破損した後にTiKVが起動できなくなるバグを修正[＃9992](https://github.com/tikv/tikv/pull/9992)

-   TiFlash

    -   storageエンジンが一部の範囲のデータの削除に失敗する問題を修正しました
    -   時間型を整数型にキャストしたときに誤った結果が返される問題を修正しました
    -   `receiver`秒以内に対応するタスクが見つからないバグを修正
    -   `cancelMPPQuery`に無効なイテレータが存在する可能性がある問題を修正
    -   `bitwise`演算子の動作がTiDBと異なるバグを修正
    -   `prefix key`使用する際に範囲が重複することで発生するアラートの問題を修正
    -   文字列型を整数型にキャストするときに誤った結果が返される問題を修正しました
    -   連続した高速書き込みによりTiFlashのメモリが不足する可能性がある問題を修正しました
    -   重複した列名によりTiFlashでエラーが発生する問題を修正しました
    -   TiFlashがMPPプランを解析できない問題を修正
    -   テーブルGC中にヌルポインタの例外が発生する可能性がある問題を修正しました
    -   ドロップされたテーブルにデータを書き込むときに発生するTiFlashpanic問題を修正しました
    -   BRの復元中にTiFlashがpanic可能性がある問題を修正

-   ツール

    -   TiDB Lightning

        -   インポート中に進行ログに不正確なテーブル数が表示される問題を修正[＃1005](https://github.com/pingcap/br/pull/1005)

    -   バックアップと復元 (BR)

        -   実際のバックアップ速度が`--ratelimit`制限を超えるバグを修正[＃1026](https://github.com/pingcap/br/pull/1026)
        -   いくつかの TiKV ノードの障害によって発生するバックアップ中断の問題を修正[＃1019](https://github.com/pingcap/br/pull/1019)
        -   TiDB Lightning のインポート中に進行ログでテーブル数が不正確になる問題を修正[＃1005](https://github.com/pingcap/br/pull/1005)

    -   TiCDC

        -   Unified Sorter の同時実行の問題を修正し、役に立たないエラーメッセージをフィルタリングします[＃1678](https://github.com/pingcap/tiflow/pull/1678)
        -   冗長ディレクトリの作成によりMinIO [＃1672](https://github.com/pingcap/tiflow/pull/1672)でのレプリケーションが中断される可能性があるバグを修正
        -   MySQL 5.7ダウンストリームがアップストリーム TiDB [＃1659](https://github.com/pingcap/tiflow/pull/1659)と同じ動作を維持するように、 `explicit_defaults_for_timestamp`セッション変数のデフォルト値を`ON`に設定します。
        -   `io.EOF`の誤った処理によりレプリケーションが中断される可能性がある問題を修正[＃1648](https://github.com/pingcap/tiflow/pull/1648)
        -   TiCDCダッシュボード[＃1645](https://github.com/pingcap/tiflow/pull/1645)のTiKV CDCエンドポイントCPUメトリックを修正
        -   場合によってはレプリケーションのブロックを回避するために`defaultBufferChanSize`増やす[＃1632](https://github.com/pingcap/tiflow/pull/1632)
