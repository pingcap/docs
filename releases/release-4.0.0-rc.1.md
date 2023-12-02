---
title: TiDB 4.0 RC.1 Release Notes
---

# TiDB 4.0 RC.1 リリース ノート {#tidb-4-0-rc-1-release-notes}

発売日：2020年4月28日

TiDB バージョン: 4.0.0-rc.1

## 互換性の変更 {#compatibility-changes}

-   TiKV

    -   デフォルトで休止状態リージョン機能を無効にする[#7618](https://github.com/tikv/tikv/pull/7618)

-   TiDBBinlog

    -   Drainer [#950](https://github.com/pingcap/tidb-binlog/pull/950)でのシーケンス DDL 操作のサポート

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `MemBuffer`がチェックされていないため、明示的なトランザクション内の複数の行で`INSERT ... ON DUPLICATE UPDATE`ステートメントが誤って実行される可能性がある問題を修正します[#16689](https://github.com/pingcap/tidb/pull/16689)
    -   複数の行で重複したキーをロックするときのデータの不整合を修正[#16769](https://github.com/pingcap/tidb/pull/16769)
    -   TiDB インスタンス間の非スーパーバッチ アイドル接続をリサイクルするときに発生するpanicを修正します[#16303](https://github.com/pingcap/tidb/pull/16303)

-   TiKV

    -   TiDB [#7540](https://github.com/tikv/tikv/pull/7540)からのプローブ要求によって引き起こされるデッドロックの問題を修正しました。
    -   トランザクションの最小コミット タイムスタンプがオーバーフローする可能性があり、データの正確性に影響を与える問題を修正します[#7638](https://github.com/tikv/tikv/pull/7638)

-   TiFlash

    -   複数のデータ パスが構成されている場合に`rename table`操作によって発生するデータ損失の問題を修正
    -   マージされたリージョンからデータを読み取るときにエラーが発生する問題を修正
    -   異常状態のリージョンからデータを読み込むとエラーが発生する問題を修正
    -   `recover table` / `flashback table`を正しくサポートするようにTiFlashのテーブル名のマッピングを変更します。
    -   storageパスを変更して、テーブルの名前を変更するときに発生する潜在的なデータ損失の問題を修正します。
    -   スーパー バッチが有効になっている場合の TiDB の潜在的なpanicを修正
    -   オンライン更新シナリオの読み取りモードを変更して、読み取りパフォーマンスを向上させます。

-   TiCDC

    -   TiCDC で内部的に維持されているスキーマが読み取りおよび書き込み操作のタイミングの問題を正しく処理できないために発生するレプリケーション エラーを修正します[#438](https://github.com/pingcap/tiflow/pull/438) [#450](https://github.com/pingcap/tiflow/pull/450) [#478](https://github.com/pingcap/tiflow/pull/478) [#496](https://github.com/pingcap/tiflow/pull/496)
    -   TiKV の異常が発生したときに TiKV クライアントが内部リソースを正しく維持できないバグを修正[#499](https://github.com/pingcap/tiflow/pull/499) [#492](https://github.com/pingcap/tiflow/pull/492)
    -   メタデータが正しくクリーンアップされず、TiCDC ノードに異常に残るバグを修正[#488](https://github.com/pingcap/tiflow/pull/488) [#504](https://github.com/pingcap/tiflow/pull/504)
    -   TiKV クライアントが事前書き込みイベント[#446](https://github.com/pingcap/tiflow/pull/446)の繰り返し送信を正しく処理できない問題を修正します。
    -   TiKV クライアントが初期化前に受信した冗長事前書き込みイベントを正しく処理できない問題を修正します[#448](https://github.com/pingcap/tiflow/pull/448)

-   バックアップと復元 (BR)

    -   チェックサムが無効になっている場合でもチェックサムが実行される問題を修正[#223](https://github.com/pingcap/br/pull/223)
    -   TiDB [#230](https://github.com/pingcap/br/pull/230) [#231](https://github.com/pingcap/br/pull/231)で`auto-random`または`alter-pk`が有効になっている場合の増分レプリケーションの失敗を修正

## 新機能 {#new-features}

-   TiDB

    -   TiFlashへのコプロセッサ リクエストのコプロセッサー送信をサポート[#16226](https://github.com/pingcap/tidb/pull/16226)
    -   デフォルトでコプロセッサーキャッシュ機能を有効にする[#16710](https://github.com/pingcap/tidb/pull/16710)
    -   SQL ステートメントの特別なコメント内のステートメントの登録済みセクションのみを解析します[#16157](https://github.com/pingcap/tidb/pull/16157)
    -   PD および TiKV インスタンスの構成を表示するための`SHOW CONFIG`構文の使用のサポート[#16475](https://github.com/pingcap/tidb/pull/16475)

-   TiKV

    -   データを S3 にバックアップする際のサーバー側暗号化にユーザー所有の KMS キーの使用をサポート[#7630](https://github.com/tikv/tikv/pull/7630)
    -   負荷ベース`split region`操作[#7623](https://github.com/tikv/tikv/pull/7623)を有効にする
    -   共通名の検証のサポート[#7468](https://github.com/tikv/tikv/pull/7468)
    -   ファイル ロック チェックを追加して、同じアドレス[#7447](https://github.com/tikv/tikv/pull/7447)にバインドされている複数の TiKV インスタンスの起動を回避します。
    -   保存時の暗号化で AWS KMS をサポート[#7465](https://github.com/tikv/tikv/pull/7465)

-   配置Driver(PD)

    -   `config manager`を削除すると、他のコンポーネントがコンポーネント構成を制御できるようになります[#2349](https://github.com/pingcap/pd/pull/2349)

-   TiFlash

    -   DeltaTree エンジンの読み取りおよび書き込みワークロードに関連するメトリクス レポートを追加します。
    -   `handle`列と`version`列をキャッシュして、単一の読み取りまたは書き込みリクエストのディスク I/O を削減します。
    -   `fromUnixTime`と`dateFormat`関数の押し下げをサポート
    -   最初のディスクに従ってグローバル状態を評価し、この評価を報告します
    -   DeltaTree エンジンの読み取りおよび書き込みワークロードに関連するグラフィックスを Grafana に追加します。
    -   `Chunk`コーデックでの 10 進数データのエンコーディングを最適化します。
    -   診断 (SQL 診断) の gRPC API を実装して、 `INFORMATION_SCHEMA.CLUSTER_INFO`のようなシステム テーブルのクエリをサポートします。

-   TiCDC

    -   Kafka シンク モジュール[#426](https://github.com/pingcap/tiflow/pull/426)でのバッチでのメッセージ送信のサポート
    -   プロセッサー[#477](https://github.com/pingcap/tiflow/pull/477)でのファイルのソートをサポート
    -   自動`resolve lock` [#459](https://github.com/pingcap/tiflow/pull/459)をサポート
    -   TiCDC サービスの GC セーフ ポイントを自動更新する機能を PD [#487](https://github.com/pingcap/tiflow/pull/487)に追加
    -   データレプリケーションのタイムゾーン設定を追加[#498](https://github.com/pingcap/tiflow/pull/498)

-   バックアップと復元 (BR)

    -   storageURL [#246](https://github.com/pingcap/br/pull/246)での S3/GCS の構成のサポート

## バグの修正 {#bug-fixes}

-   TiDB

<!---->

-   列が符号なし[#16004](https://github.com/pingcap/tidb/pull/16004)として定義されているため、システム テーブルで負の数値が正しく表示されない問題を修正します。
-   `use_index_merge`ヒントに無効なインデックス名が含まれている場合に警告を追加します[#15960](https://github.com/pingcap/tidb/pull/15960)
-   同じ一時ディレクトリを共有する TiDBサーバーの複数のインスタンスを禁止します[#16026](https://github.com/pingcap/tidb/pull/16026)
-   プラン キャッシュが有効になっている場合に`explain for connection`の実行中に発生するpanicを修正します[#16285](https://github.com/pingcap/tidb/pull/16285)
-   `tidb_capture_plan_baselines`システム変数の結果が正しく表示されない問題を修正[#16048](https://github.com/pingcap/tidb/pull/16048)
-   `prepare`ステートメントの`group by`句が正しく解析されない問題を修正します[#16377](https://github.com/pingcap/tidb/pull/16377)
-   `analyze primary key`ステートメント[#16081](https://github.com/pingcap/tidb/pull/16081)の実行中に発生する可能性のpanicを修正します。
-   `cluster_info`システムテーブルのTiFlashストア情報が間違っている問題を修正[#16024](https://github.com/pingcap/tidb/pull/16024)
-   インデックスの結合プロセス中に発生する可能性のpanicを修正します[#16360](https://github.com/pingcap/tidb/pull/16360)
-   Index Merge リーダーが生成された列を読み取るときに誤った結果が発生する可能性がある問題を修正します[#16359](https://github.com/pingcap/tidb/pull/16359)
-   `show create table`ステートメント[#16526](https://github.com/pingcap/tidb/pull/16526)のデフォルトのシーケンス値の誤った表示を修正しました。
-   主キー[#16510](https://github.com/pingcap/tidb/pull/16510)のデフォルト値としてシーケンスが使用されているため、 `not-null`エラーが返される問題を修正
-   TiKV が`StaleCommand`エラー[#16530](https://github.com/pingcap/tidb/pull/16530)を返し続ける場合、ブロックされた SQL 実行に対してエラーが報告されない問題を修正します。
-   データベース作成時に`COLLATE`のみを指定するとエラーが報告される問題を修正しました。 `SHOW CREATE DATABASE` [#16540](https://github.com/pingcap/tidb/pull/16540)の結果に不足している`COLLATE`部分を追加します
-   プラン キャッシュが有効になっている場合のパーティション プルーニングの失敗を修正[#16723](https://github.com/pingcap/tidb/pull/16723)
-   `PointGet`オーバーフロー処理時に間違った結果が返されるバグを修正[#16755](https://github.com/pingcap/tidb/pull/16755)
-   等しい時間値[#16806](https://github.com/pingcap/tidb/pull/16806)を使用して`slow_query`システム テーブルをクエリすると、間違った結果が返される問題を修正します。

<!---->

-   TiKV

    -   OpenSSL のセキュリティ問題に対処します: CVE-2020-1967 [#7622](https://github.com/tikv/tikv/pull/7622)
    -   楽観的トランザクションに多くの書き込み競合が存在する場合、パフォーマンスを向上させるために`BatchRollback`によって書き込まれたロールバック レコードの保護を回避します[#7604](https://github.com/tikv/tikv/pull/7604)
    -   トランザクションの不必要なウェイクアップにより、無駄な再試行が発生し、重いロック競合ワークロードでパフォーマンスが低下する問題を修正します[#7551](https://github.com/tikv/tikv/pull/7551)
    -   リージョンが複数回のマージでスタックする可能性がある問題を修正[#7518](https://github.com/tikv/tikv/pull/7518)
    -   学習者[#7518](https://github.com/tikv/tikv/pull/7518)を削除しても学習者が削除されない問題を修正
    -   フォロワーの読み取りが raft-rs [#7408](https://github.com/tikv/tikv/pull/7408)でpanicを引き起こす可能性がある問題を修正
    -   `group by constant`エラー[#7383](https://github.com/tikv/tikv/pull/7383)により SQL 操作が失敗する可能性があるバグを修正
    -   対応する楽観的ロックが悲観的ロック[#7328](https://github.com/tikv/tikv/pull/7328)の場合、悲観的的ロックが読み取りをブロックする可能性がある問題を修正します。

-   PD

    -   一部の API が TLS 検証で失敗する可能性がある問題を修正[#2363](https://github.com/pingcap/pd/pull/2363)
    -   構成 API がプレフィックス[#2354](https://github.com/pingcap/pd/pull/2354)の構成アイテムを受け入れられない問題を修正します。
    -   スケジューラが見つからない場合に`500`エラーが返される問題を修正[#2328](https://github.com/pingcap/pd/pull/2328)
    -   `scheduler config balance-hot-region-scheduler list`コマンド[#2321](https://github.com/pingcap/pd/pull/2321)に対して`404`エラーが返される問題を修正

-   TiFlash

    -   storageエンジンの粗粒度のインデックス最適化を無効にする
    -   リージョンのロックを解決するときに例外がスローされ、一部のロックをスキップする必要があるバグを修正
    -   コプロセッサー統計を収集する際のヌル ポインター例外 (NPE) を修正しました。
    -   リージョンの分割/リージョンのマージのプロセスが正しいことを確認するために、リージョンメタのチェックを修正しました。
    -   コプロセッサー応答のサイズが見積もられていないため、メッセージ サイズが gRPC の制限を超える問題を修正
    -   TiFlashの`AdminCmdType::Split`コマンドの処理を修正
