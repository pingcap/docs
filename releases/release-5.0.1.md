---
title: TiDB 5.0.1 Release Notes
---

# TiDB 5.0.1 リリースノート {#tidb-5-0-1-release-notes}

発売日：2021年4月24日

TiDB バージョン: 5.0.1

## 互換性の変更 {#compatibility-change}

-   `committer-concurrency`構成アイテムのデフォルト値が`16`から`128`に変更されました。

## 改良点 {#improvements}

-   TiDB

    -   内蔵機能をサポート`VITESS_HASH()` [#23915](https://github.com/pingcap/tidb/pull/23915)

-   TiKV

    -   `zstd`を使用してリージョンのスナップショットを圧縮します[#10005](https://github.com/tikv/tikv/pull/10005)

-   PD

    -   リージョンスコア計算機を変更して、異性店舗をより適切に満たすようにします[#3605](https://github.com/pingcap/pd/pull/3605)
    -   `scatter region`スケジューラー[#3602](https://github.com/pingcap/pd/pull/3602)を追加した後の予期しない統計の回避

-   ツール

    -   バックアップと復元 (BR)

        -   要約ログ[#1009](https://github.com/pingcap/br/pull/1009)から誤解を招く情報を削除する

## バグの修正 {#bug-fixes}

-   TiDB

    -   射影結果が空の場合、プロジェクト消去の実行結果がおかしくなることがある問題を修正[#24093](https://github.com/pingcap/tidb/pull/24093)
    -   場合によっては列に`NULL`値が含まれている場合に、間違ったクエリ結果が返される問題を修正します[#24063](https://github.com/pingcap/tidb/pull/24063)
    -   スキャンに仮想列が含まれている場合、MPP プランの生成を禁止する[#24058](https://github.com/pingcap/tidb/pull/24058)
    -   Plan Cache [#24043](https://github.com/pingcap/tidb/pull/24043)での`PointGet`と`TableDual`の間違った再利用を修正
    -   オプティマイザーがクラスター化インデックス[#24042](https://github.com/pingcap/tidb/pull/24042)の`IndexMerge`プランを構築するときに発生するエラーを修正します。
    -   BIT 型エラーの型推論を修正します[#24027](https://github.com/pingcap/tidb/pull/24027)
    -   `PointGet`演算子が存在する場合、一部のオプティマイザー ヒントが有効にならない問題を修正します[#23685](https://github.com/pingcap/tidb/pull/23685)
    -   エラーが原因でロールバックすると DDL 操作が失敗する可能性がある問題を修正します[#24080](https://github.com/pingcap/tidb/pull/24080)
    -   バイナリ リテラル定数のインデックス範囲が正しく構築されていない問題を修正します[#24041](https://github.com/pingcap/tidb/pull/24041)
    -   場合によっては`IN`句の潜在的な間違った結果を修正します[#24023](https://github.com/pingcap/tidb/pull/24023)
    -   一部の文字列関数の間違った結果を修正します[#23879](https://github.com/pingcap/tidb/pull/23879)
    -   ユーザーが`REPLACE`操作を実行するには、テーブルに対して`INSERT`と`DELETE`両方の権限が必要です[#23939](https://github.com/pingcap/tidb/pull/23939)
    -   ポイント クエリ[#24070](https://github.com/pingcap/tidb/pull/24070)を実行するときのパフォーマンスの低下を修正します。
    -   間違った`TableDual`バイナリとバイトの比較によって引き起こされた計画を修正します[#23918](https://github.com/pingcap/tidb/pull/23918)

-   TiKV

    -   コプロセッサが`IN`式の符号付きまたは符号なし整数型を適切に処理できない問題を修正します[#10018](https://github.com/tikv/tikv/pull/10018)
    -   SST ファイルのバッチ取り込み後に空のリージョンが多数発生する問題を修正します[#10015](https://github.com/tikv/tikv/pull/10015)
    -   `cast_string_as_time`の入力が無効な UTF-8 バイト[#9995](https://github.com/tikv/tikv/pull/9995)の場合に発生する潜在的なpanicを修正します。
    -   ファイル辞書ファイルが破損した後、TiKV が起動できなくなるバグを修正[#9992](https://github.com/tikv/tikv/pull/9992)

-   TiFlash

    -   storageエンジンが一部の範囲のデータを削除できない問題を修正
    -   時刻型を整数型にキャストすると、結果が正しくなくなる問題を修正
    -   `receiver`が 10 秒以内に対応するタスクを見つけられないバグを修正
    -   `cancelMPPQuery`に無効なイテレータが存在する可能性がある問題を修正
    -   `bitwise`オペレータの挙動がTiDBと異なる不具合を修正
    -   `prefix key`を使用するときに範囲が重複することによって引き起こされるアラートの問題を修正します。
    -   文字列型を整数型にキャストしたときに誤った結果が返される問題を修正
    -   連続した高速書き込みによってTiFlash がメモリ不足になる問題を修正
    -   列名が重複しているとTiFlash でエラーが発生する問題を修正
    -   TiFlash がMPP プランの解析に失敗する問題を修正
    -   テーブル GC 中に null ポインターの例外が発生する可能性がある潜在的な問題を修正します。
    -   削除されたテーブルにデータを書き込むときに発生するTiFlashpanicの問題を修正します
    -   BR復元中にTiFlash がpanicすることがある問題を修正

-   ツール

    -   TiDB Lightning

        -   インポート中の進捗ログの不正確なテーブル数の問題を修正します[#1005](https://github.com/pingcap/br/pull/1005)

    -   バックアップと復元 (BR)

        -   実際のバックアップ速度が`--ratelimit`制限[#1026](https://github.com/pingcap/br/pull/1026)を超える不具合を修正
        -   いくつかの TiKV ノードの障害によって引き起こされるバックアップの中断の問題を修正します[#1019](https://github.com/pingcap/br/pull/1019)
        -   TiDB Lightning のインポート[#1005](https://github.com/pingcap/br/pull/1005)中の進捗ログのテーブル数が不正確になる問題を修正

    -   TiCDC

        -   Unified Sorter の同時実行の問題を修正し、役に立たないエラー メッセージをフィルター処理する[#1678](https://github.com/pingcap/tiflow/pull/1678)
        -   MinIO [#1672](https://github.com/pingcap/tiflow/pull/1672)で冗長ディレクトリを作成するとレプリケーションが中断することがある不具合を修正
        -   `explicit_defaults_for_timestamp`セッション変数のデフォルト値を`ON`に設定して、 MySQL 5.7ダウンストリームがアップストリーム TiDB [#1659](https://github.com/pingcap/tiflow/pull/1659)と同じ動作を維持するようにします。
        -   `io.EOF`の扱いを誤るとレプリケーションが中断することがある問題を修正[#1648](https://github.com/pingcap/tiflow/pull/1648)
        -   TiCDC ダッシュボードで TiKV CDC エンドポイントの CPU メトリックを修正する[#1645](https://github.com/pingcap/tiflow/pull/1645)
        -   `defaultBufferChanSize`を増やして、場合によってはレプリケーションのブロックを回避します[#1632](https://github.com/pingcap/tiflow/pull/1632)
