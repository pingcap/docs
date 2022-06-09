---
title: TiDB 4.0.10 Release Notes
---

# TiDB4.0.10リリースノート {#tidb-4-0-10-release-notes}

発売日：2021年1月15日

TiDBバージョン：4.0.10

## 新機能 {#new-features}

-   PD

    -   ログ[＃3266](https://github.com/pingcap/pd/pull/3266)からユーザーデータを編集するために`enable-redact-log`の構成アイテムを追加します

-   TiFlash

    -   ログからユーザーデータを編集するために`security.redact_info_log`の構成アイテムを追加します

## 改善 {#improvements}

-   TiDB

    -   `txn-entry-size-limit` [＃21843](https://github.com/pingcap/tidb/pull/21843)を使用して、トランザクションのKey-Valueエントリのサイズ制限を構成可能にします。

-   PD

    -   `store-state-filter`のメトリックを最適化して、より多くの情報を表示します[＃3100](https://github.com/tikv/pd/pull/3100)
    -   `go.etcd.io/bbolt`の依存関係をv1.3.53にアップグレードし[＃3331](https://github.com/tikv/pd/pull/3331)

-   ツール

    -   TiCDC

        -   `maxwell`プロトコル[＃1144](https://github.com/pingcap/tiflow/pull/1144)の古い値機能を有効にします
        -   統合ソーター機能をデフォルトで有効にする[＃1230](https://github.com/pingcap/tiflow/pull/1230)

    -   Dumpling

        -   認識されない引数のチェックと、ダンプ中の現在の進行状況の出力をサポート[＃228](https://github.com/pingcap/dumpling/pull/228)

    -   TiDB Lightning

        -   [＃533](https://github.com/pingcap/tidb-lightning/pull/533)からの読み取り時に発生するエラーの再試行をサポート

## バグの修正 {#bug-fixes}

-   TiDB

    -   バッチクライアントのタイムアウトを引き起こす可能性のある同時実行のバグを修正します[＃22336](https://github.com/pingcap/tidb/pull/22336)
    -   同時ベースラインキャプチャによって引き起こされる重複バインディングの問題を修正します[＃22295](https://github.com/pingcap/tidb/pull/22295)
    -   ログレベルが`'debug'`のときに、SQLステートメントに[＃22293](https://github.com/pingcap/tidb/pull/22293)されたベースラインキャプチャを機能させる
    -   リージョンマージが発生したときにGCロックを正しく解放する[＃22267](https://github.com/pingcap/tidb/pull/22267)
    -   `datetime`タイプ[＃22143](https://github.com/pingcap/tidb/pull/22143)のユーザー変数の正しい値を返します
    -   複数のテーブルフィルターがある場合にインデックスマージを使用する問題を修正します[＃22124](https://github.com/pingcap/tidb/pull/22124)
    -   `prepare`プランキャッシュ[＃21960](https://github.com/pingcap/tidb/pull/21960)によって引き起こされるTiFlashの`wrong precision`の問題を修正します
    -   スキーマの変更によって引き起こされる誤った結果の問題を修正します[＃21596](https://github.com/pingcap/tidb/pull/21596)
    -   `ALTER TABLE`での不要な列フラグの変更を[＃21474](https://github.com/pingcap/tidb/pull/21474)する
    -   オプティマイザヒントで使用されるクエリブロックのテーブルエイリアスのデータベース名を設定します[＃21380](https://github.com/pingcap/tidb/pull/21380)
    -   `IndexHashJoin`および[＃21020](https://github.com/pingcap/tidb/pull/21020)の適切なオプティマイザヒントを生成し`IndexMergeJoin`

-   TiKV

    -   レディとピア[＃9409](https://github.com/tikv/tikv/pull/9409)の間の間違ったマッピングを修正
    -   `security.redact-info-log`が[＃9314](https://github.com/tikv/tikv/pull/9314)に設定されている場合、一部のログが編集されない問題を修正し`true` 。

-   PD

    -   ID割り当てが単調ではない問題を修正し[＃3323](https://github.com/tikv/pd/pull/3323) [＃3308](https://github.com/tikv/pd/pull/3308)
    -   PDクライアントがブロックされる場合があるという問題を修正します[＃3285](https://github.com/pingcap/pd/pull/3285)

-   TiFlash

    -   TiFlashが古いバージョンのTiDBスキーマを処理できないためにTiFlashが起動しない問題を修正します
    -   RedHatシステムで`cpu_time`が正しく処理されないためにTiFlashが起動しない問題を修正します
    -   `path_realtime_mode`が`true`に設定されているとTiFlashが起動しない問題を修正します
    -   3つのパラメーターで`substr`つの関数を呼び出すときの誤った結果の問題を修正します
    -   変更がロスレスであっても、TiFlashが`Enum`タイプの変更をサポートしない問題を修正します

-   ツール

    -   TiCDC

        -   `base64`のデータ出力の問題やUNIXタイムスタンプ[＃1173](https://github.com/pingcap/tiflow/pull/1173)へのTSOの出力の問題など、 `maxwell`のプロトコルの問題を修正します。
        -   古いメタデータが新しく作成されたチェンジフィードの異常を引き起こす可能性があるバグを修正します[＃1184](https://github.com/pingcap/tiflow/pull/1184)
        -   閉じた通知機能[＃1199](https://github.com/pingcap/tiflow/pull/1199)でレシーバーを作成する問題を修正します
        -   TiCDC所有者がetcdウォッチクライアントで大量のメモリを消費する可能性があるバグを修正します[＃1227](https://github.com/pingcap/tiflow/pull/1227)
        -   `max-batch-size`が有効にならない問題を修正します[＃1253](https://github.com/pingcap/tiflow/pull/1253)
        -   キャプチャ情報が構築される前に古いタスクをクリーンアップする問題を修正します[＃1280](https://github.com/pingcap/tiflow/pull/1280)
        -   MySQLシンク[＃1285](https://github.com/pingcap/tiflow/pull/1285)で`rollback`が呼び出されないため、dbconnのリサイクルがブロックされる問題を修正します。

    -   Dumpling

        -   デフォルトの動作を`tidb_mem_quota_query`に設定して、 [＃233](https://github.com/pingcap/dumpling/pull/233)のメモリ不足（OOM）を回避します。

    -   バックアップと復元（BR）

        -   BRv4.0.9がGCS1でBRv4.0.8を使用してバックアップされたファイルを復元できない問題を修正し[＃688](https://github.com/pingcap/br/pull/688)
        -   GCSストレージURLにプレフィックス[＃673](https://github.com/pingcap/br/pull/673)がない場合にBRがパニックになる問題を修正します
        -   BR OOM [＃693](https://github.com/pingcap/br/pull/693)を回避するために、デフォルトでバックアップ統計を無効にします

    -   TiDB Binlog

        -   `AMEND TRANSACTION`機能が有効になっている場合、DrainerがSQLステートメントを生成するために誤ったスキーマバージョンを選択する可能性があるという問題を修正します[＃1033](https://github.com/pingcap/tidb-binlog/pull/1033)

    -   TiDB Lightning

        -   リージョンキーが正しくエンコードされていないためにリージョンが分割されないバグを修正します[＃531](https://github.com/pingcap/tidb-lightning/pull/531)
        -   複数のテーブルが作成されたときに`CREATE TABLE`の失敗が失われる可能性があるという問題を修正します[＃530](https://github.com/pingcap/tidb-lightning/pull/530)
        -   TiDBバックエンド[＃535](https://github.com/pingcap/tidb-lightning/pull/535)を使用する場合の`column count mismatch`の問題を修正します
