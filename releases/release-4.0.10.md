---
title: TiDB 4.0.10 Release Notes
summary: TiDB 4.0.10 は 2021 年 1 月 15 日にリリースされました。新機能には、ログからのユーザー データの編集や、キー値エントリのサイズ制限の設定が含まれます。バグ修正では、同時実行の問題、重複バインディング、および誤った結果に対処しています。改善点には、最適化されたメトリックとアップグレードされた依存関係が含まれます。TiCDC、 Dumpling、Backup & Restore、TiDB Binlog、 TiDB Lightningなどのさまざまなツールも更新および修正されています。
---

# TiDB 4.0.10 リリースノート {#tidb-4-0-10-release-notes}

発売日: 2021年1月15日

TiDB バージョン: 4.0.10

## 新機能 {#new-features}

-   PD

    -   ログ[＃3266](https://github.com/pingcap/pd/pull/3266)からユーザーデータを編集するための`enable-redact-log`構成項目を追加します。

-   TiFlash

    -   ログからユーザーデータを編集するための`security.redact_info_log`構成項目を追加します

## 改善点 {#improvements}

-   ティビ

    -   トランザクション内のキー値エントリのサイズ制限を`txn-entry-size-limit` [＃21843](https://github.com/pingcap/tidb/pull/21843)を使用して設定可能にする

-   PD

    -   `store-state-filter`メトリックを最適化して、より多くの情報を表示します[＃3100](https://github.com/tikv/pd/pull/3100)
    -   `go.etcd.io/bbolt`依存関係を v1.3.5 [＃3331](https://github.com/tikv/pd/pull/3331)にアップグレードします

-   ツール

    -   ティCDC

        -   `maxwell`プロトコル[＃1144](https://github.com/pingcap/tiflow/pull/1144)の古い値機能を有効にする
        -   統合ソート機能をデフォルトで有効にする[＃1230](https://github.com/pingcap/tiflow/pull/1230)

    -   Dumpling

        -   認識されない引数のチェックとダンプ中の現在の進行状況の表示をサポート[＃228](https://github.com/pingcap/dumpling/pull/228)

    -   TiDB Lightning

        -   S3 [＃533](https://github.com/pingcap/tidb-lightning/pull/533)からの読み取り時に発生するエラーの再試行をサポート

## バグの修正 {#bug-fixes}

-   ティビ

    -   バッチクライアントのタイムアウトを引き起こす可能性のある同時実行バグを修正[＃22336](https://github.com/pingcap/tidb/pull/22336)
    -   同時ベースラインキャプチャによって発生する重複バインディングの問題を修正[＃22295](https://github.com/pingcap/tidb/pull/22295)
    -   ログレベルが`'debug'` [＃22293](https://github.com/pingcap/tidb/pull/22293)のときにSQL文にバインドされたベースラインキャプチャを機能させる
    -   リージョンのマージが発生したときにGCロックを正しく解放する[＃22267](https://github.com/pingcap/tidb/pull/22267)
    -   `datetime`タイプのユーザー変数の正しい値を返す[＃22143](https://github.com/pingcap/tidb/pull/22143)
    -   複数のテーブルフィルターがある場合のインデックスマージの使用に関する問題を修正[＃22124](https://github.com/pingcap/tidb/pull/22124)
    -   `prepare`プラン キャッシュ[＃21960](https://github.com/pingcap/tidb/pull/21960)によって発生するTiFlashの`wrong precision`問題を修正
    -   スキーマ変更[＃21596](https://github.com/pingcap/tidb/pull/21596)によって誤った結果が発生する問題を修正
    -   `ALTER TABLE` [＃21474](https://github.com/pingcap/tidb/pull/21474)で不要な列フラグの変更を避ける
    -   オプティマイザヒント[＃21380](https://github.com/pingcap/tidb/pull/21380)で使用されるクエリブロックのテーブルエイリアスのデータベース名を設定します
    -   `IndexHashJoin`と`IndexMergeJoin`の適切なオプティマイザヒントを生成する[＃21020](https://github.com/pingcap/tidb/pull/21020)

-   ティクヴ

    -   準備完了とピア[＃9409](https://github.com/tikv/tikv/pull/9409)間の誤ったマッピングを修正
    -   `security.redact-info-log` `true` [＃9314](https://github.com/tikv/tikv/pull/9314)に設定すると一部のログが編集されない問題を修正

-   PD

    -   ID割り当てが単調ではない問題を修正[＃3308](https://github.com/tikv/pd/pull/3308) [＃3323](https://github.com/tikv/pd/pull/3323)
    -   PDクライアントがブロックされる可能性がある問題を修正[＃3285](https://github.com/pingcap/pd/pull/3285)

-   TiFlash

    -   TiFlashが古いバージョンの TiDB スキーマを処理できないために起動に失敗する問題を修正しました。
    -   RedHat システムで`cpu_time`の誤った処理によりTiFlash が起動に失敗する問題を修正しました。
    -   `path_realtime_mode` `true`に設定するとTiFlash が起動しない問題を修正
    -   3 つのパラメータを持つ`substr`関数を呼び出すときに誤った結果が返される問題を修正しました。
    -   TiFlash がロスレスの変更であっても`Enum`タイプの変更をサポートしない問題を修正

-   ツール

    -   ティCDC

        -   `base64`データ出力の問題と TSO を Unix タイムスタンプ[＃1173](https://github.com/pingcap/tiflow/pull/1173)に出力する際の問題を含む`maxwell`プロトコルの問題を修正しました。
        -   古いメタデータにより、新しく作成された変更フィードが異常になる可能性があるバグを修正[＃1184](https://github.com/pingcap/tiflow/pull/1184)
        -   クローズド通知[＃1199](https://github.com/pingcap/tiflow/pull/1199)で受信者を作成する問題を修正
        -   TiCDC 所有者が etcd ウォッチ クライアント[＃1227](https://github.com/pingcap/tiflow/pull/1227)でメモリを過剰に消費する可能性があるバグを修正しました。
        -   `max-batch-size`有効にならない問題を修正[＃1253](https://github.com/pingcap/tiflow/pull/1253)
        -   キャプチャ情報が構築される前に古いタスクをクリーンアップする問題を修正[＃1280](https://github.com/pingcap/tiflow/pull/1280)
        -   MySQLシンク[＃1285](https://github.com/pingcap/tiflow/pull/1285)で`rollback`呼び出されないため、db connのリサイクルがブロックされる問題を修正

    -   Dumpling

        -   デフォルトの動作を[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) [＃233](https://github.com/pingcap/dumpling/pull/233)に設定してTiDBのメモリ不足（OOM）を回避する

    -   バックアップと復元 (BR)

        -   GCS [＃688](https://github.com/pingcap/br/pull/688)でBR v4.0.8 を使用してバックアップされたファイルをBR v4.0.9 で復元できない問題を修正しました。
        -   GCSstorageURL にプレフィックスがない場合にBR がパニックになる問題を修正[＃673](https://github.com/pingcap/br/pull/673)
        -   BR OOM [＃693](https://github.com/pingcap/br/pull/693)を回避するために、デフォルトでバックアップ統計を無効にする

    -   TiDBBinlog

        -   `AMEND TRANSACTION`機能が有効になっている場合、 Drainer がSQL ステートメントを生成するために誤ったスキーマ バージョンを選択する可能性がある問題を修正しました[＃1033](https://github.com/pingcap/tidb-binlog/pull/1033)

    -   TiDB Lightning

        -   リージョンキーが誤ってエンコードされているためリージョンが分割されないバグを修正[＃531](https://github.com/pingcap/tidb-lightning/pull/531)
        -   複数のテーブルを作成すると`CREATE TABLE`の失敗が失われる可能性がある問題を修正[＃530](https://github.com/pingcap/tidb-lightning/pull/530)
        -   TiDBバックエンド[＃535](https://github.com/pingcap/tidb-lightning/pull/535)使用時の`column count mismatch`の問題を修正
