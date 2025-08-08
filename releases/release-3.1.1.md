---
title: TiDB 3.1.1 Release Notes
summary: TiDB 3.1.1は2020年4月30日にリリースされました。新機能には、auto_rand_base`のテーブルオプションと`Feature ID`コメントが含まれます。バグ修正には、分離読み取り設定、パーティション選択構文、ネストされたクエリからの誤った結果が含まれます。TiFlashTiFlash、バグ修正とデータ読み取りおよびstorageパス変更の改善が行われました。バックアップとリストア（BR）では、テーブルの復元とデータ挿入に関する問題が修正されました。
---

# TiDB 3.1.1 リリースノート {#tidb-3-1-1-release-notes}

発売日：2020年4月30日

TiDB バージョン: 3.1.1

TiDB Ansible バージョン: 3.1.1

## 新機能 {#new-features}

-   TiDB

    -   `auto_rand_base` [＃16812](https://github.com/pingcap/tidb/pull/16812)のテーブルオプションを追加
    -   `Feature ID`コメントを追加: SQL文の特別なコメントでは、登録された文のフラグメントのみがパーサーによって解析されます。それ以外の場合、文は無視されます[＃16155](https://github.com/pingcap/tidb/pull/16155)

-   TiFlash

    -   `handle`目と`version`列目をキャッシュして、単一の読み取り要求のディスクI/Oを削減します。
    -   DeltaTreeエンジンの読み取りおよび書き込みワークロードに関連するグラフィックスをGrafanaに追加します
    -   `Chunk`コーデックの 10 進データエンコードを最適化します
    -   TiFlashの負荷が低いときに開いているファイル記述子の数を減らす

## バグ修正 {#bug-fixes}

-   TiDB

    -   インスタンスレベルでの分離読み取り設定が有効にならない問題と、TiDB をアップグレードした後に分離読み取り設定が誤って保持される問題を修正しました[＃16482](https://github.com/pingcap/tidb/pull/16482) [＃16802](https://github.com/pingcap/tidb/pull/16802)
    -   ハッシュパーティションテーブルのパーティション選択構文を修正し、 `partition (P0)` [＃16076](https://github.com/pingcap/tidb/pull/16076)などの構文でエラーが報告されないようにしました。
    -   `UPDATE` SQL 文がビューからのクエリのみ実行し、ビューを更新しない場合でも、更新文でエラーが報告される問題を修正しました[＃16789](https://github.com/pingcap/tidb/pull/16789)
    -   ネストされたクエリ[＃16423](https://github.com/pingcap/tidb/pull/16423)から`not not`削除することによって誤った結果が発生する問題を修正しました

-   TiFlash

    -   異常状態にあるリージョンからデータを読み取る際にエラーが発生する問題を修正しました
    -   TiFlashのテーブル名のマッピングを修正して、 `recover table` / `flashback table`正しくサポートする
    -   テーブル名を変更するときに発生する可能性のあるデータ損失の問題を修正するためにstorageパスを変更します
    -   オンライン更新シナリオの読み取りモードを変更して読み取りパフォーマンスを向上させる
    -   データベース/テーブル名に特殊文字が含まれている場合、アップグレード後にTiFlash が正常に起動しない問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   BRが`auto_random`属性を持つテーブルを復元した後、データを挿入すると重複エントリエラー[＃241](https://github.com/pingcap/br/issues/241)が発生する可能性がある問題を修正しました。
