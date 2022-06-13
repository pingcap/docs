---
title: TiDB 4.0 RC.1 Release Notes
---

# TiDB4.0RC.1リリースノート {#tidb-4-0-rc-1-release-notes}

発売日：2020年4月28日

TiDBバージョン：4.0.0-rc.1

## 互換性の変更 {#compatibility-changes}

-   TiKV

    -   デフォルトでHibernateリージョン機能を無効にする[＃7618](https://github.com/tikv/tikv/pull/7618)

-   TiDB Binlog

    -   [＃950](https://github.com/pingcap/tidb-binlog/pull/950)でシーケンスDDL操作をサポートする

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `MemBuffer`がチェックされていないため、明示的なトランザクションで`INSERT ... ON DUPLICATE UPDATE`のステートメントが複数の行で誤って実行される可能性がある問題を修正します[＃16689](https://github.com/pingcap/tidb/pull/16689)
    -   複数の行で重複したキーをロックするときのデータの不整合を修正[＃16769](https://github.com/pingcap/tidb/pull/16769)
    -   TiDBインスタンス間の非スーパーバッチアイドル接続をリサイクルするときに発生するパニックを修正します[＃16303](https://github.com/pingcap/tidb/pull/16303)

-   TiKV

    -   TiDB1からのプローブ要求によって引き起こされるデッドロックの問題を修正し[＃7540](https://github.com/tikv/tikv/pull/7540)
    -   トランザクションの最小コミットタイムスタンプがオーバーフローし、データの正確性に影響を与える可能性がある問題を修正します[＃7638](https://github.com/tikv/tikv/pull/7638)

-   TiFlash

    -   複数のデータパスが構成されている場合の`rename table`の操作によって引き起こされるデータ損失の問題を修正します
    -   マージされたリージョンからデータを読み取るときにエラーが発生する問題を修正します
    -   異常状態のリージョンからデータを読み取るときにエラーが発生する問題を修正します
    -   `recover table`を正しくサポートするように、TiFlashのテーブル名のマッピングを変更し`flashback table`
    -   テーブルの名前を変更するときに発生する可能性のあるデータ損失の問題を修正するために、ストレージパスを変更します
    -   スーパーバッチが有効になっている場合のTiDBの潜在的なパニックを修正します
    -   オンライン更新シナリオで読み取りモードを変更して、読み取りパフォーマンスを向上させます

-   TiCDC

    -   [＃450](https://github.com/pingcap/tiflow/pull/450)で内部的に維持されているスキーマが読み取りおよび書き込み操作のタイミングの問題を正しく処理できないために発生するレプリケーションの失敗を修正し[＃438](https://github.com/pingcap/tiflow/pull/438) [＃496](https://github.com/pingcap/tiflow/pull/496) [＃478](https://github.com/pingcap/tiflow/pull/478)
    -   いくつかのTiKV異常が発生したときに、TiKVクライアントが内部リソースを正しく維持できないというバグを修正します[＃499](https://github.com/pingcap/tiflow/pull/499) [＃492](https://github.com/pingcap/tiflow/pull/492)
    -   メタデータが正しくクリーンアップされず、TiCDCノードに異常に残るというバグを修正します[＃488](https://github.com/pingcap/tiflow/pull/488) [＃504](https://github.com/pingcap/tiflow/pull/504)
    -   TiKVクライアントがプリライトイベントの繰り返し送信を正しく処理できない問題を修正します[＃446](https://github.com/pingcap/tiflow/pull/446)
    -   TiKVクライアントが初期化前に受信した冗長なプリライトイベントを正しく処理できない問題を修正します[＃448](https://github.com/pingcap/tiflow/pull/448)

-   バックアップと復元（BR）

    -   チェックサムが無効になっている場合でもチェックサムが実行される問題を修正します[＃223](https://github.com/pingcap/br/pull/223)
    -   [＃231](https://github.com/pingcap/br/pull/231)で`auto-random`または`alter-pk`が有効になっている場合の増分レプリケーションの失敗を修正し[＃230](https://github.com/pingcap/br/pull/230) 。

## 新機能 {#new-features}

-   TiDB

    -   コプロセッサー要求のバッチでのTiFlashへの送信をサポート[＃16226](https://github.com/pingcap/tidb/pull/16226)
    -   コプロセッサーのキャッシュ機能をデフォルトで有効にする[＃16710](https://github.com/pingcap/tidb/pull/16710)
    -   SQLステートメントの特別なコメントでステートメントの登録されたセクションのみを解析します[＃16157](https://github.com/pingcap/tidb/pull/16157)
    -   PDおよびTiKVインスタンスの構成を表示するための`SHOW CONFIG`構文の使用をサポートします[＃16475](https://github.com/pingcap/tidb/pull/16475)

-   TiKV

    -   S3 [＃7630](https://github.com/tikv/tikv/pull/7630)にデータをバックアップするときに、サーバー側の暗号化にユーザー所有のKMSキーを使用することをサポートします。
    -   負荷ベースの`split region`操作を有効にする[＃7623](https://github.com/tikv/tikv/pull/7623)
    -   一般名の検証をサポート[＃7468](https://github.com/tikv/tikv/pull/7468)
    -   同じアドレスにバインドされている複数のTiKVインスタンスが開始されないように、ファイルロックチェックを追加します[＃7447](https://github.com/tikv/tikv/pull/7447)
    -   安静時の暗号化でAWSKMSをサポートする[＃7465](https://github.com/tikv/tikv/pull/7465)

-   配置ドライバー（PD）

    -   `config manager`を削除して、他のコンポーネントがコンポーネント構成を制御できるようにします[＃2349](https://github.com/pingcap/pd/pull/2349)

-   TiFlash

    -   DeltaTreeエンジンの読み取りおよび書き込みワークロードに関連するメトリックレポートを追加します
    -   `handle`列と`version`列をキャッシュして、単一の読み取りまたは書き込み要求のディスクI/Oを削減します
    -   `fromUnixTime`と`dateFormat`の機能のプッシュダウンをサポート
    -   最初のディスクに従ってグローバル状態を評価し、この評価を報告します
    -   DeltaTreeエンジンの読み取りおよび書き込みワークロードに関連するグラフィックをGrafanaに追加します
    -   `Chunk`コーデックの10進データエンコーディングを最適化する
    -   `INFORMATION_SCHEMA.CLUSTER_INFO`などのシステムテーブルのクエリをサポートするために、診断（SQL診断）のgRPCAPIを実装します。

-   TiCDC

    -   Kafkaシンクモジュール[＃426](https://github.com/pingcap/tiflow/pull/426)でのメッセージのバッチ送信のサポート
    -   プロセッサでのファイルの並べ替えをサポート[＃477](https://github.com/pingcap/tiflow/pull/477)
    -   自動[＃459](https://github.com/pingcap/tiflow/pull/459) `resolve lock`
    -   TiCDCサービスGCセーフポイントをPD1に自動的に更新する機能を追加し[＃487](https://github.com/pingcap/tiflow/pull/487)
    -   データレプリケーションのタイムゾーン設定を追加する[＃498](https://github.com/pingcap/tiflow/pull/498)

-   バックアップと復元（BR）

    -   ストレージ[＃246](https://github.com/pingcap/br/pull/246)でのS3/GCSの設定のサポート

## バグの修正 {#bug-fixes}

-   TiDB

<!---->

-   列が符号なし[＃16004](https://github.com/pingcap/tidb/pull/16004)として定義されているため、システムテーブルに負の数が正しく表示されない問題を修正します。
-   `use_index_merge`のヒントに無効なインデックス名が含まれている場合に警告を追加します[＃15960](https://github.com/pingcap/tidb/pull/15960)
-   同じ一時ディレクトリを共有するTiDBサーバーの複数のインスタンスを禁止する[＃16026](https://github.com/pingcap/tidb/pull/16026)
-   プランキャッシュが有効になっている場合に`explain for connection`の実行中に発生するパニックを修正します[＃16285](https://github.com/pingcap/tidb/pull/16285)
-   `tidb_capture_plan_baselines`システム変数の結果が正しく表示されない問題を修正します[＃16048](https://github.com/pingcap/tidb/pull/16048)
-   `prepare`ステートメントの`group by`句が誤って解析される問題を修正します[＃16377](https://github.com/pingcap/tidb/pull/16377)
-   `analyze primary key`ステートメントの実行中に発生する可能性のあるパニックを修正します[＃16081](https://github.com/pingcap/tidb/pull/16081)
-   `cluster_info`システムテーブルのTiFlashストア情報が間違っている問題を修正します[＃16024](https://github.com/pingcap/tidb/pull/16024)
-   インデックスマージプロセス中に発生する可能性のあるパニックを修正する[＃16360](https://github.com/pingcap/tidb/pull/16360)
-   インデックスマージリーダーが生成された列を読み取るときに誤った結果が発生する可能性がある問題を修正します[＃16359](https://github.com/pingcap/tidb/pull/16359)
-   `show create table`ステートメント[＃16526](https://github.com/pingcap/tidb/pull/16526)のデフォルトシーケンス値の誤った表示を修正します。
-   シーケンスが主キー[＃16510](https://github.com/pingcap/tidb/pull/16510)のデフォルト値として使用されるため、 `not-null`エラーが返される問題を修正します。
-   TiKVが`StaleCommand`エラー[＃16530](https://github.com/pingcap/tidb/pull/16530)を返し続けたときに、ブロックされたSQL実行に対してエラーが報告されないという問題を修正します。
-   データベースの作成時に`COLLATE`のみを指定すると、エラーが報告される問題を修正します。 [＃16540](https://github.com/pingcap/tidb/pull/16540)の結果に欠落している`COLLATE`の部分を追加し`SHOW CREATE DATABASE`
-   プランキャッシュが有効になっている場合のパーティションプルーニングの失敗を修正する[＃16723](https://github.com/pingcap/tidb/pull/16723)
-   オーバーフロー[＃16755](https://github.com/pingcap/tidb/pull/16755)を処理するときに`PointGet`が間違った結果を返すというバグを修正します
-   等しい時間値[＃16806](https://github.com/pingcap/tidb/pull/16806)で`slow_query`のシステムテーブルをクエリすると、間違った結果が返される問題を修正します。

<!---->

-   TiKV

    -   OpenSSLのセキュリティ問題に対処する：CVE-2020-1967 [＃7622](https://github.com/tikv/tikv/pull/7622)
    -   楽観的なトランザクション[＃7604](https://github.com/tikv/tikv/pull/7604)に多くの書き込み競合が存在する場合は、パフォーマンスを向上させるために`BatchRollback`で書き込まれたロールバックレコードを保護しないでください。
    -   トランザクションの不必要なウェイクアップにより、重いロックレースワークロードで無駄な再試行とパフォーマンスの低下が発生する問題を修正します[＃7551](https://github.com/tikv/tikv/pull/7551)
    -   リージョンが複数回のマージでスタックする可能性がある問題を修正します[＃7518](https://github.com/tikv/tikv/pull/7518)
    -   学習者[＃7518](https://github.com/tikv/tikv/pull/7518)を削除するときに学習者が削除されない問題を修正します
    -   フォロワーの読み取りがraft-rs1でパニックを引き起こす可能性がある問題を修正し[＃7408](https://github.com/tikv/tikv/pull/7408)
    -   `group by constant`エラー[＃7383](https://github.com/tikv/tikv/pull/7383)が原因でSQL操作が失敗する可能性があるバグを修正します
    -   対応するプライマリロックがペシミスティックロックの場合、オプティミスティックロックが読み取りをブロックする可能性がある問題を修正します[＃7328](https://github.com/tikv/tikv/pull/7328)

-   PD

    -   一部のAPIがTLS検証で失敗する可能性がある問題を修正します[＃2363](https://github.com/pingcap/pd/pull/2363)
    -   構成APIがプレフィックス[＃2354](https://github.com/pingcap/pd/pull/2354)の構成アイテムを受け入れられない問題を修正します
    -   スケジューラーが見つからない場合に`500`エラーが返される問題を修正します[＃2328](https://github.com/pingcap/pd/pull/2328)
    -   `scheduler config balance-hot-region-scheduler list`コマンド[＃2321](https://github.com/pingcap/pd/pull/2321)に対して`404`エラーが返される問題を修正します。

-   TiFlash

    -   ストレージエンジンの粗粒度インデックスの最適化を無効にする
    -   リージョンのロックを解決するときに例外がスローされ、一部のロックをスキップする必要があるというバグを修正します
    -   コプロセッサー統計を収集するときのヌルポインター例外（NPE）を修正
    -   リージョンメタのチェックを修正して、リージョン分割/リージョンマージのプロセスが正しいことを確認します
    -   コプロセッサーの応答のサイズが推定されないため、メッセージサイズがgRPCの制限を超える問題を修正します
    -   TiFlashの`AdminCmdType::Split`コマンドの処理を修正しました
