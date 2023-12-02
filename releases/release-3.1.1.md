---
title: TiDB 3.1.1 Release Notes
---

# TiDB 3.1.1 リリースノート {#tidb-3-1-1-release-notes}

発売日：2020年4月30日

TiDB バージョン: 3.1.1

TiDB Ansible バージョン: 3.1.1

## 新機能 {#new-features}

-   TiDB

    -   `auto_rand_base` [#16812](https://github.com/pingcap/tidb/pull/16812)のテーブル オプションを追加します
    -   `Feature ID`コメントを追加します。SQL ステートメントの特別なコメントでは、登録されたステートメントのフラグメントのみがパーサーによって解析されます。それ以外の場合、ステートメントは無視されます[#16155](https://github.com/pingcap/tidb/pull/16155)

-   TiFlash

    -   `handle`列と`version`列をキャッシュして、1 回の読み取りリクエストのディスク I/O を削減します。
    -   DeltaTree エンジンの読み取りおよび書き込みワークロードに関連するグラフィックスを Grafana に追加します。
    -   `Chunk`コーデックでの 10 進数データのエンコーディングを最適化します。
    -   TiFlashのワークロードが低いときに開いているファイル記述子の数を減らす

## バグの修正 {#bug-fixes}

-   TiDB

    -   インスタンス レベルでの分離読み取り設定が有効にならず、TiDB のアップグレード後に分離読み取り設定が誤って保持される問題を修正します[#16482](https://github.com/pingcap/tidb/pull/16482) [#16802](https://github.com/pingcap/tidb/pull/16802)
    -   `partition (P0)` [#16076](https://github.com/pingcap/tidb/pull/16076)などの構文でエラーが報告されないように、ハッシュパーティションテーブルのパーティション選択構文を修正しました。
    -   `UPDATE` SQL ステートメントがビューからクエリのみを実行し、ビューを更新しない場合でも、更新ステートメントでエラーが報告される問題を修正します[#16789](https://github.com/pingcap/tidb/pull/16789)
    -   ネストされたクエリ[#16423](https://github.com/pingcap/tidb/pull/16423)から`not not`を削除することによって引き起こされる間違った結果の問題を修正します。

-   TiFlash

    -   異常状態のリージョンからデータを読み込むとエラーが発生する問題を修正
    -   `recover table` / `flashback table`を正しくサポートするようにTiFlashのテーブル名のマッピングを変更します。
    -   storageパスを変更して、テーブルの名前を変更するときに発生する潜在的なデータ損失の問題を修正します。
    -   オンライン更新シナリオの読み取りモードを変更して、読み取りパフォーマンスを向上させます。
    -   データベース/テーブル名に特殊文字が含まれている場合、アップグレード後にTiFlash が正常に起動できない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   BR が`auto_random`属性を持つテーブルを復元した後、データを挿入すると重複エントリ エラー[#241](https://github.com/pingcap/br/issues/241)が発生する可能性がある問題を修正します。
