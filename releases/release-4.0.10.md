---
title: TiDB 4.0.10 Release Notes
---

# TiDB 4.0.10 リリースノート {#tidb-4-0-10-release-notes}

発売日：2021年1月15日

TiDB バージョン: 4.0.10

## 新機能 {#new-features}

-   PD

    -   ログ[#3266](https://github.com/pingcap/pd/pull/3266)からユーザー データを編集するための`enable-redact-log`構成項目を追加します。

-   TiFlash

    -   ログからユーザー データを編集するための`security.redact_info_log`構成項目を追加します

## 改善点 {#improvements}

-   TiDB

    -   トランザクション内のキーと値のエントリのサイズ制限を`txn-entry-size-limit` [#21843](https://github.com/pingcap/tidb/pull/21843)を使用して構成可能にします。

-   PD

    -   `store-state-filter`メトリクスを最適化して、より多くの情報を表示する[#3100](https://github.com/tikv/pd/pull/3100)
    -   `go.etcd.io/bbolt`依存関係を v1.3.5 にアップグレードします[#3331](https://github.com/tikv/pd/pull/3331)

-   ツール

    -   TiCDC

        -   `maxwell`プロトコル[#1144](https://github.com/pingcap/tiflow/pull/1144)の古い値機能を有効にする
        -   統合ソーター機能をデフォルトで有効にする[#1230](https://github.com/pingcap/tiflow/pull/1230)

    -   Dumpling

        -   認識されない引数のチェックとダンプ中の現在の進行状況の出力をサポート[#228](https://github.com/pingcap/dumpling/pull/228)

    -   TiDB Lightning

        -   S3 [#533](https://github.com/pingcap/tidb-lightning/pull/533)からの読み取り時に発生するエラーの再試行をサポート

## バグの修正 {#bug-fixes}

-   TiDB

    -   バッチクライアントのタイムアウトを引き起こす可能性がある同時実行性のバグを修正します[#22336](https://github.com/pingcap/tidb/pull/22336)
    -   同時ベースライン キャプチャによって発生する重複バインディングの問題を修正[#22295](https://github.com/pingcap/tidb/pull/22295)
    -   ログ レベルが`'debug'` [#22293](https://github.com/pingcap/tidb/pull/22293)の場合に、SQL ステートメントにバインドされたベースライン キャプチャが機能するようにします。
    -   リージョンのマージが発生したときに GC ロックが正しく解放されるようになりました[#22267](https://github.com/pingcap/tidb/pull/22267)
    -   `datetime`タイプ[#22143](https://github.com/pingcap/tidb/pull/22143)のユーザー変数に対して正しい値を返す
    -   複数のテーブル フィルターがある場合のインデックス マージの使用の問題を修正します[#22124](https://github.com/pingcap/tidb/pull/22124)
    -   `prepare`プラン キャッシュ[#21960](https://github.com/pingcap/tidb/pull/21960)によって引き起こされるTiFlashの`wrong precision`の問題を修正
    -   スキーマ変更[#21596](https://github.com/pingcap/tidb/pull/21596)によって引き起こされる誤った結果の問題を修正します。
    -   `ALTER TABLE` [#21474](https://github.com/pingcap/tidb/pull/21474)での不必要な列フラグの変更を避ける
    -   オプティマイザ ヒント[#21380](https://github.com/pingcap/tidb/pull/21380)で使用されるクエリ ブロックのテーブル エイリアスのデータベース名を設定します。
    -   `IndexHashJoin`と`IndexMergeJoin`の適切なオプティマイザ ヒントを生成します[#21020](https://github.com/pingcap/tidb/pull/21020)

-   TiKV

    -   レディとピア[#9409](https://github.com/tikv/tikv/pull/9409)の間の間違ったマッピングを修正
    -   `security.redact-info-log`を`true` [#9314](https://github.com/tikv/tikv/pull/9314)に設定すると一部のログが編集されない問題を修正

-   PD

    -   ID割り当てが単調でない問題を修正[#3308](https://github.com/tikv/pd/pull/3308) [#3323](https://github.com/tikv/pd/pull/3323)
    -   PDクライアントがブロックされる場合がある問題を修正[#3285](https://github.com/pingcap/pd/pull/3285)

-   TiFlash

    -   TiFlashが古いバージョンの TiDB スキーマの処理に失敗するため、 TiFlashが起動できない問題を修正
    -   RedHat システムでの`cpu_time`誤った処理が原因でTiFlash が起動できない問題を修正
    -   `path_realtime_mode`を`true`に設定するとTiFlashが起動できない問題を修正
    -   3 つのパラメーターを指定して`substr`関数を呼び出したときに誤った結果が表示される問題を修正
    -   TiFlash が`Enum`タイプの変更がロスレスであってもサポートされない問題を修正

-   ツール

    -   TiCDC

        -   `base64`データ出力の問題と TSO を UNIX タイムスタンプ[#1173](https://github.com/pingcap/tiflow/pull/1173)に出力する問題を含む、 `maxwell`プロトコルの問題を修正します。
        -   古いメタデータにより、新しく作成された変更フィードが異常になる可能性があるバグを修正しました[#1184](https://github.com/pingcap/tiflow/pull/1184)
        -   クローズされたノーティファイア[#1199](https://github.com/pingcap/tiflow/pull/1199)でレシーバーを作成する問題を修正します。
        -   TiCDC 所有者が etcd 監視クライアント[#1227](https://github.com/pingcap/tiflow/pull/1227)でメモリを過剰に消費する可能性があるバグを修正
        -   `max-batch-size`が反映されない問題を修正[#1253](https://github.com/pingcap/tiflow/pull/1253)
        -   キャプチャ情報が構築される前に古いタスクをクリーンアップする問題を修正します[#1280](https://github.com/pingcap/tiflow/pull/1280)
        -   MySQL シンク[#1285](https://github.com/pingcap/tiflow/pull/1285)で`rollback`が呼び出されないため、db conn のリサイクルがブロックされる問題を修正

    -   Dumpling

        -   デフォルトの動作を[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) [#233](https://github.com/pingcap/dumpling/pull/233)に設定することで、TiDB のメモリ不足 (OOM) を回避します。

    -   バックアップと復元 (BR)

        -   GCS [#688](https://github.com/pingcap/br/pull/688)でBR v4.0.8 を使用してバックアップされたファイルをBR v4.0.9 が復元できない問題を修正
        -   GCSstorageURL にプレフィックス[#673](https://github.com/pingcap/br/pull/673)がない場合にBRパニックが発生する問題を修正
        -   BR OOM [#693](https://github.com/pingcap/br/pull/693)を回避するには、デフォルトでバックアップ統計を無効にします

    -   TiDBBinlog

        -   `AMEND TRANSACTION`機能が有効になっている場合、 Drainer がSQL ステートメントを生成するために間違ったスキーマ バージョンを選択する可能性がある問題を修正します[#1033](https://github.com/pingcap/tidb-binlog/pull/1033)

    -   TiDB Lightning

        -   リージョンキーのエンコードが間違っているためリージョンが分割されないバグを修正[#531](https://github.com/pingcap/tidb-lightning/pull/531)
        -   複数のテーブルを作成すると`CREATE TABLE`の失敗が失われる可能性がある問題を修正[#530](https://github.com/pingcap/tidb-lightning/pull/530)
        -   TiDB-backend [#535](https://github.com/pingcap/tidb-lightning/pull/535)を使用する場合の`column count mismatch`の問題を修正します。
