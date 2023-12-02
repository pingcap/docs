---
title: TiDB 5.0.1 Release Notes
---

# TiDB 5.0.1 リリースノート {#tidb-5-0-1-release-notes}

発売日：2021年4月24日

TiDB バージョン: 5.0.1

## 互換性の変更 {#compatibility-change}

-   `committer-concurrency`設定項目のデフォルト値が`16`から`128`に変更されます。

## 改善点 {#improvements}

-   TiDB

    -   組み込み関数のサポート`VITESS_HASH()` [#23915](https://github.com/pingcap/tidb/pull/23915)

-   TiKV

    -   `zstd`を使用してリージョンスナップショット[#10005](https://github.com/tikv/tikv/pull/10005)を圧縮します。

-   PD

    -   異性ストア[#3605](https://github.com/pingcap/pd/pull/3605)をより適切に満たすようにリージョンスコア計算ツールを変更します。
    -   `scatter region`スケジューラ[#3602](https://github.com/pingcap/pd/pull/3602)を追加した後の予期しない統計を回避します

-   ツール

    -   バックアップと復元 (BR)

        -   概要ログ[#1009](https://github.com/pingcap/br/pull/1009)から誤解を招く情報を削除します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   投影結果が空の場合、プロジェクトの削除の実行結果が正しくない場合がある問題を修正[#24093](https://github.com/pingcap/tidb/pull/24093)
    -   列に`NULL`値が含まれる場合に、場合によっては間違ったクエリ結果が表示される問題を修正します[#24063](https://github.com/pingcap/tidb/pull/24063)
    -   スキャンに仮想列が含まれる場合、MPP プランの生成を禁止する[#24058](https://github.com/pingcap/tidb/pull/24058)
    -   プラン キャッシュ[#24043](https://github.com/pingcap/tidb/pull/24043)の`PointGet`と`TableDual`の誤った再利用を修正
    -   オプティマイザーがクラスター化インデックス`IndexMerge`のプランを構築するときに発生するエラーを修正します[#24042](https://github.com/pingcap/tidb/pull/24042)
    -   BIT 型エラーの型推論を修正[#24027](https://github.com/pingcap/tidb/pull/24027)
    -   `PointGet`演算子が存在する場合、一部のオプティマイザ ヒントが有効にならない問題を修正[#23685](https://github.com/pingcap/tidb/pull/23685)
    -   ロールバック時にエラー[#24080](https://github.com/pingcap/tidb/pull/24080)が原因で DDL 操作が失敗する可能性がある問題を修正します。
    -   バイナリリテラル定数のインデックス範囲が正しく構築されない問題を修正[#24041](https://github.com/pingcap/tidb/pull/24041)
    -   場合によっては`IN`節の誤った結果が生じる可能性がある問題を修正[#24023](https://github.com/pingcap/tidb/pull/24023)
    -   一部の文字列関数の間違った結果を修正[#23879](https://github.com/pingcap/tidb/pull/23879)
    -   ユーザーが`REPLACE`操作を実行するには、テーブルに対する`INSERT`と`DELETE`両方の権限が必要になる[#23939](https://github.com/pingcap/tidb/pull/23939)
    -   ポイント クエリ[#24070](https://github.com/pingcap/tidb/pull/24070)を実行するときのパフォーマンスの低下を修正しました。
    -   バイナリとバイト[#23918](https://github.com/pingcap/tidb/pull/23918)の誤った比較によって引き起こされる間違った`TableDual`プランを修正します。

-   TiKV

    -   コプロセッサが`IN`式[#10018](https://github.com/tikv/tikv/pull/10018)の符号付き整数型または符号なし整数型を適切に処理できない問題を修正します。
    -   SST ファイルのバッチ取り込み後に多数の空のリージョンが発生する問題を修正[#10015](https://github.com/tikv/tikv/pull/10015)
    -   `cast_string_as_time`の入力が無効な UTF-8 バイト[#9995](https://github.com/tikv/tikv/pull/9995)である場合に発生する潜在的なpanicを修正しました。
    -   ファイル辞書ファイルが破損するとTiKVが起動できなくなるバグを修正[#9992](https://github.com/tikv/tikv/pull/9992)

-   TiFlash

    -   storageエンジンが一部の範囲のデータを削除できない問題を修正
    -   時刻型を整数型にキャストするときに誤った結果が表示される問題を修正
    -   `receiver`が10秒以内に対応するタスクを見つけられないバグを修正
    -   `cancelMPPQuery`に無効な反復子が存在する可能性がある問題を修正
    -   `bitwise`オペレーターの挙動がTiDBと異なるバグを修正
    -   `prefix key`を使用するときに範囲が重複することによって引き起こされるアラートの問題を修正します。
    -   文字列型を整数型にキャストするときに誤った結果が発生する問題を修正
    -   連続した高速書き込みによりTiFlash がメモリ不足になる可能性がある問題を修正
    -   列名が重複するとTiFlash でエラーが発生する問題を修正
    -   TiFlash がMPP プランの解析に失敗する問題を修正
    -   テーブル GC 中に null ポインターの例外が発生する可能性がある潜在的な問題を修正
    -   ドロップされたテーブルにデータを書き込むときに発生するTiFlashpanicの問題を修正
    -   BR復元中にTiFlash がpanicになる可能性がある問題を修正

-   ツール

    -   TiDB Lightning

        -   インポート中の進行状況ログ内のテーブル数が不正確になる問題を修正[#1005](https://github.com/pingcap/br/pull/1005)

    -   バックアップと復元 (BR)

        -   実際のバックアップ速度が`--ratelimit`制限[#1026](https://github.com/pingcap/br/pull/1026)を超えるバグを修正
        -   いくつかの TiKV ノードの障害によって引き起こされるバックアップ中断の問題を修正します[#1019](https://github.com/pingcap/br/pull/1019)
        -   TiDB Lightning のインポート[#1005](https://github.com/pingcap/br/pull/1005)中に進行状況ログに表示されるテーブル数が不正確になる問題を修正しました。

    -   TiCDC

        -   統合ソーターの同時実行の問題を修正し、役に立たないエラー メッセージをフィルタリングします[#1678](https://github.com/pingcap/tiflow/pull/1678)
        -   冗長ディレクトリの作成により MinIO [#1672](https://github.com/pingcap/tiflow/pull/1672)でのレプリケーションが中断される可能性があるバグを修正
        -   `explicit_defaults_for_timestamp`セッション変数のデフォルト値を`ON`に設定して、 MySQL 5.7ダウンストリームがアップストリームの TiDB [#1659](https://github.com/pingcap/tiflow/pull/1659)と同じ動作を維持できるようにします。
        -   `io.EOF`の処理を​​誤るとレプリケーションが中断される可能性がある問題を修正[#1648](https://github.com/pingcap/tiflow/pull/1648)
        -   TiCDC ダッシュボード[#1645](https://github.com/pingcap/tiflow/pull/1645)で TiKV CDC エンドポイントの CPU メトリックを修正します。
        -   場合によってはレプリケーションのブロックを避けるために`defaultBufferChanSize`を増やします[#1632](https://github.com/pingcap/tiflow/pull/1632)
