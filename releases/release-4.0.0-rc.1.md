---
title: TiDB 4.0 RC.1 Release Notes
---

# TiDB 4.0 RC.1 リリースノート {#tidb-4-0-rc-1-release-notes}

発売日：2020年4月28日

TiDB バージョン: 4.0.0-rc.1

## 互換性の変更 {#compatibility-changes}

-   TiKV

    -   デフォルトで Hibernate リージョン機能を無効にする[#7618](https://github.com/tikv/tikv/pull/7618)

-   TiDBBinlog

    -   Drainer [#950](https://github.com/pingcap/tidb-binlog/pull/950)でのシーケンス DDL 操作のサポート

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `MemBuffer`がチェックされていないため、明示的なトランザクションで複数の行に対して`INSERT ... ON DUPLICATE UPDATE`ステートメントが誤って実行される可能性がある問題を修正します[#16689](https://github.com/pingcap/tidb/pull/16689)
    -   複数の行で重複したキーをロックするときのデータの不整合を修正します[#16769](https://github.com/pingcap/tidb/pull/16769)
    -   TiDB インスタンス間の非スーパーバッチ アイドル接続をリサイクルするときに発生するpanicを修正します[#16303](https://github.com/pingcap/tidb/pull/16303)

-   TiKV

    -   TiDB [#7540](https://github.com/tikv/tikv/pull/7540)からのプローブ要求によって引き起こされるデッドロックの問題を修正します。
    -   データの正確性に影響するトランザクションの最小コミット タイムスタンプがオーバーフローする可能性がある問題を修正します[#7638](https://github.com/tikv/tikv/pull/7638)

-   TiFlash

    -   複数のデータ パスが構成されている場合に`rename table`操作が原因で発生するデータ損失の問題を修正します。
    -   マージされたリージョンからデータを読み取るとエラーが発生する問題を修正
    -   異常な状態のリージョンからデータを読み取るとエラーが発生する問題を修正
    -   `recover table` / `flashback table`を正しくサポートするように、 TiFlashのテーブル名のマッピングを変更します。
    -   storageパスを変更して、テーブルの名前を変更するときに発生する潜在的なデータ損失の問題を修正します。
    -   Super Batch が有効な場合に TiDB がパニックになる可能panicを修正
    -   オンライン更新シナリオの読み取りモードを変更して、読み取りパフォーマンスを向上させます

-   TiCDC

    -   TiCDC で内部的に維持されているスキーマが読み取りおよび書き込み操作のタイミングの問題を正しく処理できないために発生するレプリケーションの失敗を修正します。 [#438](https://github.com/pingcap/tiflow/pull/438) [#450](https://github.com/pingcap/tiflow/pull/450) [#478](https://github.com/pingcap/tiflow/pull/478) [#496](https://github.com/pingcap/tiflow/pull/496)
    -   一部の TiKV 異常が発生したときに、TiKV クライアントが内部リソースを正しく維持できないというバグを修正します[#499](https://github.com/pingcap/tiflow/pull/499) [#492](https://github.com/pingcap/tiflow/pull/492)
    -   メタデータが正しくクリーンアップされず、TiCDC ノードに異常に残る不具合を修正[#488](https://github.com/pingcap/tiflow/pull/488) [#504](https://github.com/pingcap/tiflow/pull/504)
    -   TiKV クライアントがプリライト イベント[#446](https://github.com/pingcap/tiflow/pull/446)の繰り返し送信を正しく処理できない問題を修正します。
    -   TiKV クライアントが、初期化の前に受信した冗長な事前書き込みイベントを正しく処理できないという問題を修正します[#448](https://github.com/pingcap/tiflow/pull/448)

-   バックアップと復元 (BR)

    -   チェックサムが無効になっている場合でもチェックサムが実行される問題を修正します[#223](https://github.com/pingcap/br/pull/223)
    -   TiDB [#230](https://github.com/pingcap/br/pull/230) [#231](https://github.com/pingcap/br/pull/231)で`auto-random`または`alter-pk`が有効になっている場合の増分レプリケーションの失敗を修正します。

## 新機能 {#new-features}

-   TiDB

    -   コプロセッサー要求のバッチでのTiFlashへの送信をサポート[#16226](https://github.com/pingcap/tidb/pull/16226)
    -   デフォルトでコプロセッサーのキャッシュ機能を有効にする[#16710](https://github.com/pingcap/tidb/pull/16710)
    -   SQL ステートメントの特別なコメント内のステートメントの登録されたセクションのみを解析します[#16157](https://github.com/pingcap/tidb/pull/16157)
    -   PD および TiKV インスタンスの構成を示す`SHOW CONFIG`構文を使用したサポート[#16475](https://github.com/pingcap/tidb/pull/16475)

-   TiKV

    -   データを S3 にバックアップする際のサーバー側の暗号化にユーザー所有の KMS キーを使用するサポート[#7630](https://github.com/tikv/tikv/pull/7630)
    -   負荷ベース`split region`操作[#7623](https://github.com/tikv/tikv/pull/7623)を有効にする
    -   一般名の検証をサポート[#7468](https://github.com/tikv/tikv/pull/7468)
    -   ファイル ロック チェックを追加して、同じアドレスにバインドされた複数の TiKV インスタンスを開始しないようにします[#7447](https://github.com/tikv/tikv/pull/7447)
    -   保存時の暗号化で AWS KMS をサポート[#7465](https://github.com/tikv/tikv/pull/7465)

-   プレースメントDriver(PD)

    -   `config manager`を削除して、他のコンポーネントがコンポーネント構成を制御できるようにします[#2349](https://github.com/pingcap/pd/pull/2349)

-   TiFlash

    -   DeltaTree エンジンの読み取りおよび書き込みワークロードに関連するメトリック レポートを追加します。
    -   `handle`列と`version`列をキャッシュして、1 回の読み取りまたは書き込み要求のディスク I/O を削減します。
    -   `fromUnixTime`および`dateFormat`関数のプッシュ ダウンをサポート
    -   最初のディスクに従ってグローバルな状態を評価し、この評価を報告します
    -   DeltaTree エンジンの読み取りおよび書き込みワークロードに関連する Grafana のグラフィックを追加します。
    -   `Chunk`コーデックの 10 進データ エンコーディングを最適化する
    -   `INFORMATION_SCHEMA.CLUSTER_INFO`のようなシステム テーブルのクエリをサポートするために、診断 (SQL 診断) の gRPC API を実装します。

-   TiCDC

    -   Kafka シンク モジュール[#426](https://github.com/pingcap/tiflow/pull/426)でメッセージのバッチ送信をサポート
    -   プロセッサ[#477](https://github.com/pingcap/tiflow/pull/477)でファイルの並べ替えをサポート
    -   自動`resolve lock` [#459](https://github.com/pingcap/tiflow/pull/459)をサポート
    -   [#487](https://github.com/pingcap/tiflow/pull/487)にTiCDCサービスのGCセーフポイントを自動更新する機能を追加
    -   データ レプリケーション[#498](https://github.com/pingcap/tiflow/pull/498)のタイムゾーン設定を追加します。

-   バックアップと復元 (BR)

    -   storageURL [#246](https://github.com/pingcap/br/pull/246)での S3/GCS の構成のサポート

## バグの修正 {#bug-fixes}

-   TiDB

<!---->

-   列が符号なし[#16004](https://github.com/pingcap/tidb/pull/16004)として定義されているため、システム テーブルに負の数が正しく表示されない問題を修正します。
-   `use_index_merge`ヒントに無効なインデックス名が含まれている場合に警告を追加します[#15960](https://github.com/pingcap/tidb/pull/15960)
-   同じ一時ディレクトリを共有する TiDBサーバーの複数のインスタンスを禁止する[#16026](https://github.com/pingcap/tidb/pull/16026)
-   プランキャッシュが有効な場合に`explain for connection`の実行中に発生するpanicを修正します[#16285](https://github.com/pingcap/tidb/pull/16285)
-   `tidb_capture_plan_baselines`システム変数の結果が正しく表示されない問題を修正[#16048](https://github.com/pingcap/tidb/pull/16048)
-   `prepare`ステートメントの`group by`句が正しく解析されない問題を修正します[#16377](https://github.com/pingcap/tidb/pull/16377)
-   `analyze primary key`ステートメントの実行中に発生する可能性のpanicを修正します[#16081](https://github.com/pingcap/tidb/pull/16081)
-   `cluster_info`システムテーブルのTiFlashストア情報が間違っている問題を修正[#16024](https://github.com/pingcap/tidb/pull/16024)
-   インデックス マージ プロセス中に発生する可能性のpanicを修正します[#16360](https://github.com/pingcap/tidb/pull/16360)
-   インデックス マージ リーダーが生成された列を読み取ると、誤った結果が発生する可能性がある問題を修正します[#16359](https://github.com/pingcap/tidb/pull/16359)
-   `show create table`ステートメント[#16526](https://github.com/pingcap/tidb/pull/16526)のデフォルト シーケンス値の誤った表示を修正します。
-   主キー[#16510](https://github.com/pingcap/tidb/pull/16510)のデフォルト値にシーケンスを使用しているため`not-null`エラーが返る問題を修正
-   TiKV が`StaleCommand`エラー[#16530](https://github.com/pingcap/tidb/pull/16530)を返し続けると、ブロックされた SQL 実行に対してエラーが報告されない問題を修正します。
-   データベースの作成時に`COLLATE`のみを指定するとエラーが報告される問題を修正します。欠落している`COLLATE`部分を`SHOW CREATE DATABASE` [#16540](https://github.com/pingcap/tidb/pull/16540)の結果に追加します
-   プラン キャッシュが有効な場合のパーティション プルーニングの失敗を修正します[#16723](https://github.com/pingcap/tidb/pull/16723)
-   オーバーフローの処理で`PointGet`が間違った結果を返すバグを修正[#16755](https://github.com/pingcap/tidb/pull/16755)
-   `slow_query`システム テーブルを等しい時間値[#16806](https://github.com/pingcap/tidb/pull/16806)でクエリすると、間違った結果が返される問題を修正します。

<!---->

-   TiKV

    -   OpenSSL のセキュリティ問題に対処します: CVE-2020-1967 [#7622](https://github.com/tikv/tikv/pull/7622)
    -   楽観的トランザクションで多くの書き込み競合が存在する場合は、パフォーマンスを向上させるために`BatchRollback`によって書き込まれたロールバック レコードを保護しないでください[#7604](https://github.com/tikv/tikv/pull/7604)
    -   トランザクションの不必要なウェイクアップにより、無駄な再試行が発生し、重いロック競合ワークロードでパフォーマンスが低下する問題を修正します[#7551](https://github.com/tikv/tikv/pull/7551)
    -   リージョンがマルチタイム マージ[#7518](https://github.com/tikv/tikv/pull/7518)でスタックする可能性がある問題を修正します。
    -   学習者を削除しても学習者が削除されない問題を修正[#7518](https://github.com/tikv/tikv/pull/7518)
    -   raft-rs [#7408](https://github.com/tikv/tikv/pull/7408)でフォロワーの読み取りがpanicを引き起こす可能性がある問題を修正します。
    -   `group by constant`エラーが原因で SQL 操作が失敗する可能性があるバグを修正[#7383](https://github.com/tikv/tikv/pull/7383)
    -   対応する楽観的ロックがペシミスティック ロック[#7328](https://github.com/tikv/tikv/pull/7328)の場合、オプティ悲観的ロックが読み取りをブロックする可能性がある問題を修正します。

-   PD

    -   一部の API が TLS 検証で失敗する可能性がある問題を修正します[#2363](https://github.com/pingcap/pd/pull/2363)
    -   構成 API がプレフィックス[#2354](https://github.com/pingcap/pd/pull/2354)の構成アイテムを受け入れることができないという問題を修正します。
    -   スケジューラーが見つからない場合に`500`エラーが返される問題を修正[#2328](https://github.com/pingcap/pd/pull/2328)
    -   `scheduler config balance-hot-region-scheduler list`コマンド[#2321](https://github.com/pingcap/pd/pull/2321)に対して`404`エラーが返される問題を修正

-   TiFlash

    -   storageエンジンの粗粒度インデックス最適化を無効にする
    -   リージョンのロックを解決するときに例外がスローされ、一部のロックをスキップする必要があるというバグを修正します
    -   コプロセッサーの統計を収集するときのヌルポインター例外 (NPE) を修正します。
    -   リージョンメタのチェックを修正して、リージョンスプリット/リージョンマージのプロセスが正しいことを確認します
    -   コプロセッサー応答のサイズが推定されないため、メッセージ サイズが gRPC の制限を超える問題を修正します。
    -   TiFlashの`AdminCmdType::Split`コマンドの処理を修正
