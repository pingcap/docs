---
title: TiDB 4.0.10 Release Notes
summary: TiDB 4.0.10は2021年1月15日にリリースされました。新機能には、ログからのユーザーデータの編集機能や、キーバリューエントリのサイズ制限の設定機能などが含まれます。バグ修正では、同時実行の問題、重複バインディング、および誤った結果が修正されています。改善点としては、メトリクスの最適化と依存関係のアップグレードが挙げられます。TiCDC、 Dumpling、Backup & Restore、TiDB Binlog、 TiDB Lightningなどの各種ツールも更新および修正されています。
---

# TiDB 4.0.10 リリースノート {#tidb-4-0-10-release-notes}

発売日：2021年1月15日

TiDB バージョン: 4.0.10

## 新機能 {#new-features}

-   PD

    -   ログ[＃3266](https://github.com/pingcap/pd/pull/3266)からユーザーデータを編集するための`enable-redact-log`構成項目を追加します。

-   TiFlash

    -   ログからユーザーデータを編集するための`security.redact_info_log`構成項目を追加します

## 改善点 {#improvements}

-   TiDB

    -   `txn-entry-size-limit` [＃21843](https://github.com/pingcap/tidb/pull/21843)を使用してトランザクション内のキー値エントリのサイズ制限を設定可能にする

-   PD

    -   `store-state-filter`指標を最適化して、より多くの情報を表示する[＃3100](https://github.com/tikv/pd/pull/3100)
    -   `go.etcd.io/bbolt`依存関係を v1.3.5 [＃3331](https://github.com/tikv/pd/pull/3331)にアップグレードします

-   ツール

    -   TiCDC

        -   統合ソート機能をデフォルトで有効にする[＃1230](https://github.com/pingcap/tiflow/pull/1230)

    -   Dumpling

        -   認識されない引数のチェックとダンプ中の現在の進行状況の表示をサポート[＃228](https://github.com/pingcap/dumpling/pull/228)

    -   TiDB Lightning

        -   S3 [＃533](https://github.com/pingcap/tidb-lightning/pull/533)からの読み取り時に発生するエラーの再試行をサポート

## バグ修正 {#bug-fixes}

-   TiDB

    -   バッチクライアントのタイムアウトを引き起こす可能性のある同時実行バグを修正[＃22336](https://github.com/pingcap/tidb/pull/22336)
    -   同時ベースラインキャプチャによって発生する重複バインディングの問題を修正[＃22295](https://github.com/pingcap/tidb/pull/22295)
    -   ログレベルが`'debug'` [＃22293](https://github.com/pingcap/tidb/pull/22293)ときにSQL文にバインドされたベースラインキャプチャを機能させる
    -   リージョンマージが発生したときにGCロックを正しく解放する[＃22267](https://github.com/pingcap/tidb/pull/22267)
    -   `datetime`型[＃22143](https://github.com/pingcap/tidb/pull/22143)のユーザー変数に正しい値を返す
    -   複数のテーブルフィルターがある場合のインデックスマージの使用に関する問題を修正[＃22124](https://github.com/pingcap/tidb/pull/22124)
    -   `prepare`プランキャッシュ[＃21960](https://github.com/pingcap/tidb/pull/21960)によって引き起こされるTiFlashの`wrong precision`問題を修正
    -   スキーマ変更[＃21596](https://github.com/pingcap/tidb/pull/21596)によって発生する誤った結果の問題を修正しました
    -   `ALTER TABLE` [＃21474](https://github.com/pingcap/tidb/pull/21474)の不要な列フラグの変更を避ける
    -   オプティマイザヒント[＃21380](https://github.com/pingcap/tidb/pull/21380)で使用されるクエリブロックのテーブルエイリアスのデータベース名を設定します
    -   `IndexHashJoin`と`IndexMergeJoin`適切なオプティマイザヒントを生成する[＃21020](https://github.com/pingcap/tidb/pull/21020)

-   TiKV

    -   準備完了とピア[＃9409](https://github.com/tikv/tikv/pull/9409)間の誤ったマッピングを修正
    -   `security.redact-info-log` `true` [＃9314](https://github.com/tikv/tikv/pull/9314)に設定すると一部のログが編集されない問題を修正しました

-   PD

    -   IDの割り当てが単調ではない問題を修正[＃3308](https://github.com/tikv/pd/pull/3308) [＃3323](https://github.com/tikv/pd/pull/3323)
    -   PDクライアントがブロックされる可能性がある問題を修正[＃3285](https://github.com/pingcap/pd/pull/3285)

-   TiFlash

    -   TiFlashが古いバージョンの TiDB スキーマを処理できないために起動に失敗する問題を修正しました
    -   RedHatシステムで`cpu_time`が正しく処理されないためTiFlashが起動に失敗する問題を修正
    -   `path_realtime_mode` `true`に設定するとTiFlash が起動に失敗する問題を修正しました
    -   3つのパラメータを持つ`substr`関数を呼び出すときに誤った結果が返される問題を修正しました
    -   TiFlashがロスレスの変更であっても`Enum`タイプの変更をサポートしない問題を修正

-   ツール

    -   TiCDC

        -   古いメタデータにより、新しく作成された変更フィードが異常になる可能性があるバグを修正しました[＃1184](https://github.com/pingcap/tiflow/pull/1184)
        -   クローズド通知[＃1199](https://github.com/pingcap/tiflow/pull/1199)で受信者を作成する問題を修正しました
        -   TiCDC 所有者が etcd ウォッチクライアント[＃1227](https://github.com/pingcap/tiflow/pull/1227)でメモリを過剰に消費する可能性があるバグを修正しました
        -   `max-batch-size`が有効にならない問題を修正[＃1253](https://github.com/pingcap/tiflow/pull/1253)
        -   キャプチャ情報が構築される前に古いタスクをクリーンアップする問題を修正[＃1280](https://github.com/pingcap/tiflow/pull/1280)
        -   MySQLシンク[＃1285](https://github.com/pingcap/tiflow/pull/1285)で`rollback`が呼び出されないため、db connのリサイクルがブロックされる問題を修正しました

    -   Dumpling

        -   デフォルトの動作を[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) [＃233](https://github.com/pingcap/dumpling/pull/233)に設定して、TiDBのメモリ不足（OOM）を回避します。

    -   バックアップと復元 (BR)

        -   GCS [＃688](https://github.com/pingcap/br/pull/688)でBR v4.0.8を使用してバックアップされたファイルをBR v4.0.9で復元できない問題を修正しました。
        -   GCSstorageURL にプレフィックス[＃673](https://github.com/pingcap/br/pull/673)がない場合にBR がパニックになる問題を修正しました
        -   BR OOM [＃693](https://github.com/pingcap/br/pull/693)回避するために、デフォルトでバックアップ統計を無効にする

    -   TiDBBinlog

        -   `AMEND TRANSACTION`機能が有効になっている場合、 Drainer がSQL 文を生成するために間違ったスキーマバージョンを選択する可能性がある問題を修正しました[＃1033](https://github.com/pingcap/tidb-binlog/pull/1033)

    -   TiDB Lightning

        -   リージョンキーが正しくエンコードされていないためにリージョンが分割されないバグを修正[＃531](https://github.com/pingcap/tidb-lightning/pull/531)
        -   複数のテーブルを作成すると`CREATE TABLE`の失敗が失われる可能性がある問題を修正[＃530](https://github.com/pingcap/tidb-lightning/pull/530)
        -   TiDBバックエンド[＃535](https://github.com/pingcap/tidb-lightning/pull/535)使用時の`column count mismatch`の問題を修正
