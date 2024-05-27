---
title: TiDB 3.1.1 Release Notes
summary: TiDB 3.1.1 は 2020 年 4 月 30 日にリリースされました。新機能には、`auto_rand_base` のテーブル オプションと `Feature ID` コメントが含まれます。バグ修正には、分離読み取り設定、パーティション選択構文、ネストされたクエリからの誤った結果が含まれます。TiFlashTiFlash、バグ修正と、データ読み取りおよびstorageパス変更の改善も行われました。バックアップと復元 (BR) では、テーブルの復元とデータ挿入に関連する問題が修正されました。
---

# TiDB 3.1.1 リリースノート {#tidb-3-1-1-release-notes}

発売日: 2020年4月30日

TiDB バージョン: 3.1.1

TiDB Ansible バージョン: 3.1.1

## 新機能 {#new-features}

-   ティビ

    -   `auto_rand_base` [＃16812](https://github.com/pingcap/tidb/pull/16812)のテーブルオプションを追加
    -   `Feature ID`コメントを追加します: SQL文の特別なコメントでは、登録された文のフラグメントのみがパーサーによって解析されます。それ以外の場合、文は無視されます[＃16155](https://github.com/pingcap/tidb/pull/16155)

-   TiFlash

    -   `handle`列目と`version`列目をキャッシュして、1回の読み取り要求のディスクI/Oを削減します。
    -   DeltaTreeエンジンの読み取りおよび書き込みワークロードに関連するグラフィックスをGrafanaに追加します。
    -   `Chunk`コーデックの10進データエンコーディングを最適化する
    -   TiFlashの負荷が低いときに開いているファイル記述子の数を減らす

## バグの修正 {#bug-fixes}

-   ティビ

    -   インスタンスレベルでの分離読み取り設定が有効にならない問題と、TiDB のアップグレード後に分離読み取り設定が誤って保持される問題を修正[＃16482](https://github.com/pingcap/tidb/pull/16482) [＃16802](https://github.com/pingcap/tidb/pull/16802)
    -   ハッシュパーティションテーブルのパーティション選択構文を修正し、 `partition (P0)` [＃16076](https://github.com/pingcap/tidb/pull/16076)などの構文でエラーが報告されないようにする。
    -   `UPDATE` SQL 文がビューからのクエリのみを実行し、ビューを更新しない場合でも、更新文がエラーを報告する問題を修正しました[＃16789](https://github.com/pingcap/tidb/pull/16789)
    -   ネストされたクエリ[＃16423](https://github.com/pingcap/tidb/pull/16423)から`not not`削除することによって間違った結果が発生する問題を修正しました

-   TiFlash

    -   異常な状態にあるリージョンからデータを読み取るときにエラーが発生する問題を修正
    -   TiFlashのテーブル名のマッピングを修正して、 `recover table` / `flashback table`を正しくサポートする
    -   テーブル名を変更するときに発生する可能性のあるデータ損失の問題を修正するためにstorageパスを変更します。
    -   オンライン更新シナリオの読み取りモードを変更して読み取りパフォーマンスを向上させる
    -   データベース/テーブル名に特殊文字が含まれている場合、アップグレード後にTiFlash が正常に起動しない問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   BRが`auto_random`属性のテーブルを復元した後、データを挿入すると重複エントリエラー[＃241](https://github.com/pingcap/br/issues/241)が発生する可能性がある問題を修正しました。
