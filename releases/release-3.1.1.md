---
title: TiDB 3.1.1 Release Notes
---

# TiDB3.1.1リリースノート {#tidb-3-1-1-release-notes}

発売日：2020年4月30日

TiDBバージョン：3.1.1

TiDB Ansibleバージョン：3.1.1

## 新機能 {#new-features}

-   TiDB

    -   [＃16812](https://github.com/pingcap/tidb/pull/16812)のテーブルオプションを追加し`auto_rand_base`
    -   `Feature ID`のコメントを追加します。SQLステートメントの特別なコメントでは、登録されたステートメントフラグメントのみがパーサーによって解析できます。それ以外の場合、ステートメントは無視されます[＃16155](https://github.com/pingcap/tidb/pull/16155)

-   TiFlash

    -   `handle`列と`version`列をキャッシュして、単一の読み取り要求のディスクI/Oを削減します
    -   DeltaTreeエンジンの読み取りおよび書き込みワークロードに関連するグラフィックをGrafanaに追加します
    -   `Chunk`コーデックの10進データエンコーディングを最適化する
    -   TiFlashのワークロードが低いときに、開いているファイル記述子の数を減らします

## バグの修正 {#bug-fixes}

-   TiDB

    -   インスタンスレベルでの分離読み取り設定が有効にならず、TiDBのアップグレード後に分離読み取り設定が誤って保持される問題を修正します[＃16482](https://github.com/pingcap/tidb/pull/16482) [＃16802](https://github.com/pingcap/tidb/pull/16802)
    -   `partition (P0)` [＃16076](https://github.com/pingcap/tidb/pull/16076)などの構文でエラーが報告されないように、ハッシュパーティションテーブルのパーティション選択構文を修正します。
    -   `UPDATE` SQLステートメントがビューからのみクエリを実行し、ビューを更新しない場合でも、更新ステートメントがエラー[＃16789](https://github.com/pingcap/tidb/pull/16789)を報告する問題を修正します。
    -   ネストされたクエリ[＃16423](https://github.com/pingcap/tidb/pull/16423)から`not not`を削除することによって引き起こされる誤った結果の問題を修正します

-   TiFlash

    -   異常状態のリージョンからデータを読み取るときにエラーが発生する問題を修正します
    -   `recover table`を正しくサポートするように、TiFlashのテーブル名のマッピングを変更し`flashback table`
    -   ストレージパスを変更して、テーブルの名前を変更するときに発生する可能性のあるデータ損失の問題を修正します
    -   オンライン更新シナリオで読み取りモードを変更して、読み取りパフォーマンスを向上させます
    -   データベース/テーブル名に特殊文字が含まれている場合、アップグレード後にTiFlashが正常に起動しない問題を修正します

-   ツール

    -   バックアップと復元（BR）

        -   BRが`auto_random`属性のテーブルを復元した後、データを挿入すると重複エントリエラー[＃241](https://github.com/pingcap/br/issues/241)がトリガーされる可能性がある問題を修正します。
