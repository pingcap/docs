---
title: TiDB 4.0.10 Release Notes
---

# TiDB 4.0.10 リリースノート {#tidb-4-0-10-release-notes}

発売日：2021年1月15日

TiDB バージョン: 4.0.10

## 新機能 {#new-features}

-   PD

    -   ログ[#3266](https://github.com/pingcap/pd/pull/3266)からユーザー データを秘匿化する`enable-redact-log`構成項目を追加します。

-   TiFlash

    -   ログからユーザー データを編集するための`security.redact_info_log`構成項目を追加します。

## 改良点 {#improvements}

-   TiDB

    -   `txn-entry-size-limit` [#21843](https://github.com/pingcap/tidb/pull/21843)を使用して、トランザクションのキー値エントリのサイズ制限を構成可能にする

-   PD

    -   `store-state-filter`メトリクスを最適化して、より多くの情報を表示する[#3100](https://github.com/tikv/pd/pull/3100)
    -   `go.etcd.io/bbolt`依存関係を v1.3.5 にアップグレードする[#3331](https://github.com/tikv/pd/pull/3331)

-   ツール

    -   TiCDC

        -   `maxwell`プロトコル[#1144](https://github.com/pingcap/tiflow/pull/1144)の古い値機能を有効にします
        -   デフォルトで統合ソーター機能を有効にする[#1230](https://github.com/pingcap/tiflow/pull/1230)

    -   Dumpling

        -   認識されていない引数のチェックと、ダンプ中の現在の進行状況の出力をサポートします[#228](https://github.com/pingcap/dumpling/pull/228)

    -   TiDB Lightning

        -   S3 [#533](https://github.com/pingcap/tidb-lightning/pull/533)からの読み取り時に発生するエラーのリトライをサポート

## バグの修正 {#bug-fixes}

-   TiDB

    -   バッチ クライアントのタイムアウト[#22336](https://github.com/pingcap/tidb/pull/22336)を引き起こす可能性のある同時実行のバグを修正します。
    -   同時ベースライン キャプチャ[#22295](https://github.com/pingcap/tidb/pull/22295)によって引き起こされる重複バインディングの問題を修正します。
    -   ログ レベルが`'debug'` [#22293](https://github.com/pingcap/tidb/pull/22293)の場合に、SQL ステートメントにバインドされたベースライン キャプチャが機能するようにします。
    -   リージョンのマージが発生したときに GC ロックを正しく解放する[#22267](https://github.com/pingcap/tidb/pull/22267)
    -   `datetime`タイプ[#22143](https://github.com/pingcap/tidb/pull/22143)のユーザー変数の正しい値を返す
    -   複数のテーブル フィルターがある場合にインデックス マージを使用する際の問題を修正します[#22124](https://github.com/pingcap/tidb/pull/22124)
    -   `prepare`プラン キャッシュが原因で発生したTiFlashの`wrong precision`問題を修正[#21960](https://github.com/pingcap/tidb/pull/21960)
    -   スキーマの変更[#21596](https://github.com/pingcap/tidb/pull/21596)による誤った結果の問題を修正します。
    -   `ALTER TABLE` [#21474](https://github.com/pingcap/tidb/pull/21474)で不要な列フラグの変更を避ける
    -   オプティマイザ ヒントで使用されるクエリ ブロックのテーブル エイリアスのデータベース名を設定します[#21380](https://github.com/pingcap/tidb/pull/21380)
    -   `IndexHashJoin`と`IndexMergeJoin` [#21020](https://github.com/pingcap/tidb/pull/21020)の適切なオプティマイザ ヒントを生成する

-   TiKV

    -   準備完了とピア[#9409](https://github.com/tikv/tikv/pull/9409)の間の間違ったマッピングを修正します
    -   `security.redact-info-log`を`true` [#9314](https://github.com/tikv/tikv/pull/9314)に設定すると一部のログが編集されない問題を修正

-   PD

    -   ID の割り当てが単調でない問題を修正[#3308](https://github.com/tikv/pd/pull/3308) [#3323](https://github.com/tikv/pd/pull/3323)
    -   場合によっては PD クライアントがブロックされる可能性がある問題を修正します[#3285](https://github.com/pingcap/pd/pull/3285)

-   TiFlash

    -   TiFlashが旧バージョンの TiDB スキーマの処理に失敗するため、 TiFlashの起動に失敗する問題を修正
    -   RedHat システムで`cpu_time`の処理が正しくないためにTiFlash が起動しない問題を修正
    -   `path_realtime_mode`を`true`に設定するとTiFlashが起動しない問題を修正
    -   3 つのパラメーターを指定して`substr`関数を呼び出すと、誤った結果が返される問題を修正
    -   変更がロスレスであっても、 TiFlash が`Enum`タイプの変更をサポートしていない問題を修正します。

-   ツール

    -   TiCDC

        -   `base64`データ出力の問題と TSO を unix タイムスタンプに出力する問題を含む`maxwell`プロトコルの問題を修正します[#1173](https://github.com/pingcap/tiflow/pull/1173)
        -   古いメタデータにより、新しく作成された変更フィードが異常になる可能性があるバグを修正します[#1184](https://github.com/pingcap/tiflow/pull/1184)
        -   クローズされたノーティファイアー[#1199](https://github.com/pingcap/tiflow/pull/1199)でレシーバーを作成する問題を修正します。
        -   TiCDC 所有者が etcd ウォッチ クライアントでメモリを消費しすぎる可能性があるバグを修正します[#1227](https://github.com/pingcap/tiflow/pull/1227)
        -   `max-batch-size`が効かない問題を修正[#1253](https://github.com/pingcap/tiflow/pull/1253)
        -   キャプチャ情報が構築される前に古いタスクをクリーンアップする問題を修正します[#1280](https://github.com/pingcap/tiflow/pull/1280)
        -   MySQL シンク[#1285](https://github.com/pingcap/tiflow/pull/1285)で`rollback`が呼び出されないため、db conn のリサイクルがブロックされる問題を修正

    -   Dumpling

        -   デフォルトの動作を[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) [#233](https://github.com/pingcap/dumpling/pull/233)に設定して、TiDB のメモリ不足 (OOM) を回避します。

    -   バックアップと復元 (BR)

        -   GCS [#688](https://github.com/pingcap/br/pull/688)でBR v4.0.8 を使用してバックアップしたファイルをBR v4.0.9 で復元できない問題を修正します。
        -   GCSstorageURL にプレフィックス[#673](https://github.com/pingcap/br/pull/673)がない場合にBR がパニックになる問題を修正します
        -   BR OOM [#693](https://github.com/pingcap/br/pull/693)を回避するために、デフォルトでバックアップ統計を無効にします

    -   TiDBBinlog

        -   `AMEND TRANSACTION`機能が有効になっている場合、 Drainer が誤ったスキーマ バージョンを選択して SQL ステートメントを生成する可能性があるという問題を修正します[#1033](https://github.com/pingcap/tidb-binlog/pull/1033)

    -   TiDB Lightning

        -   リージョンキーが正しくエンコードされていないためにリージョンが分割されないバグを修正[#531](https://github.com/pingcap/tidb-lightning/pull/531)
        -   複数のテーブルを作成すると`CREATE TABLE`の失敗が失われる場合がある問題を修正[#530](https://github.com/pingcap/tidb-lightning/pull/530)
        -   TiDB バックエンド使用時の`column count mismatch`の問題を修正[#535](https://github.com/pingcap/tidb-lightning/pull/535)
