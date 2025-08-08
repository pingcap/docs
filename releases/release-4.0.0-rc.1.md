---
title: TiDB 4.0 RC.1 Release Notes
summary: TiDB 4.0 RC.1は2020年4月28日にリリースされました。このリリースには、TiKV、TiDB、 TiFlash、TiCDC、バックアップ＆リストア（BR）、配置Driver（PD）の互換性変更、重要なバグ修正、新機能、バグ修正が含まれています。バグ修正では、データの不整合、デッドロック、レプリケーションの失敗などの問題が修正されています。新機能には、コプロセッサー要求をTiFlashにバッチ送信する機能のサポートと、負荷ベースの分割領域操作の有効化が含まれます。さらに、 TiFlashはfromUnixTime関数とdateFormat関数のプッシュダウンをサポートするようになりました。
---

# TiDB 4.0 RC.1 リリースノート {#tidb-4-0-rc-1-release-notes}

発売日：2020年4月28日

TiDB バージョン: 4.0.0-rc.1

## 互換性の変更 {#compatibility-changes}

-   TiKV

    -   デフォルトで休止リージョン機能を無効にする[＃7618](https://github.com/tikv/tikv/pull/7618)

-   TiDBBinlog

    -   Drainer [＃950](https://github.com/pingcap/tidb-binlog/pull/950)でのシーケンス DDL 操作のサポート

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `MemBuffer`がチェックされていないため、明示的なトランザクションで`INSERT ... ON DUPLICATE UPDATE`文が複数の行に対して誤って実行される可能性がある問題を修正しました[＃16689](https://github.com/pingcap/tidb/pull/16689)
    -   複数行の重複キーをロックする際のデータの不整合を修正[＃16769](https://github.com/pingcap/tidb/pull/16769)
    -   TiDBインスタンス間の非スーパーバッチアイドル接続をリサイクルするときに発生するpanicを修正[＃16303](https://github.com/pingcap/tidb/pull/16303)

-   TiKV

    -   TiDB [＃7540](https://github.com/tikv/tikv/pull/7540)からのプローブ要求によって発生するデッドロックの問題を修正
    -   トランザクションの最小コミットタイムスタンプがオーバーフローし、データの正確性に影響する可能性がある問題を修正しました[＃7638](https://github.com/tikv/tikv/pull/7638)

-   TiFlash

    -   複数のデータパスが構成されている場合に`rename table`操作によって発生するデータ損失の問題を修正しました
    -   マージされたリージョンからデータを読み取るときにエラーが発生する問題を修正しました
    -   異常状態にあるリージョンからデータを読み取る際にエラーが発生する問題を修正しました
    -   TiFlashのテーブル名のマッピングを修正して、 `recover table` / `flashback table`正しくサポートする
    -   テーブル名を変更する際に発生する可能性のあるデータ損失の問題を修正するためにstorageパスを変更します。
    -   スーパーバッチが有効な場合の TiDB の潜在的なpanicを修正
    -   オンライン更新シナリオの読み取りモードを変更して読み取りパフォーマンスを向上させる

-   TiCDC

    -   TiCDC で内部的に管理されているスキーマが読み取りおよび書き込み操作のタイミングの問題を正しく処理できないために発生するレプリケーション障害を修正します[＃438](https://github.com/pingcap/tiflow/pull/438) [＃450](https://github.com/pingcap/tiflow/pull/450) [＃478](https://github.com/pingcap/tiflow/pull/478) [＃496](https://github.com/pingcap/tiflow/pull/496)
    -   TiKVクライアントがTiKVの異常に遭遇したときに内部リソースを正しく維持できないバグを修正しました[＃499](https://github.com/pingcap/tiflow/pull/499) [＃492](https://github.com/pingcap/tiflow/pull/492)
    -   メタデータが正しくクリーンアップされず、TiCDCノード[＃488](https://github.com/pingcap/tiflow/pull/488) [＃504](https://github.com/pingcap/tiflow/pull/504)に異常に残るバグを修正
    -   TiKVクライアントがプリライトイベント[＃446](https://github.com/pingcap/tiflow/pull/446)の繰り返し送信を正しく処理できない問題を修正
    -   TiKVクライアントが初期化[＃448](https://github.com/pingcap/tiflow/pull/448)前に受信した冗長な事前書き込みイベントを正しく処理できない問題を修正しました。

-   バックアップと復元 (BR)

    -   チェックサムが無効になっている場合でもチェックサムが実行される問題を修正[＃223](https://github.com/pingcap/br/pull/223)
    -   TiDB [＃230](https://github.com/pingcap/br/pull/230) [＃231](https://github.com/pingcap/br/pull/231)で`auto-random`または`alter-pk`有効になっている場合に増分レプリケーションが失敗する問題を修正

## 新機能 {#new-features}

-   TiDB

    -   コプロセッサー要求をTiFlashにバッチで送信する機能をサポート[＃16226](https://github.com/pingcap/tidb/pull/16226)
    -   コプロセッサーキャッシュ機能をデフォルトで有効にする[＃16710](https://github.com/pingcap/tidb/pull/16710)
    -   SQL文[＃16157](https://github.com/pingcap/tidb/pull/16157)の特別なコメントに登録されたセクションのみを解析する
    -   PDおよびTiKVインスタンス[＃16475](https://github.com/pingcap/tidb/pull/16475)の構成を表示するための`SHOW CONFIG`構文の使用をサポート

-   TiKV

    -   S3 にデータをバックアップする際のサーバー側暗号化にユーザー所有の KMS キーの使用をサポート[＃7630](https://github.com/tikv/tikv/pull/7630)
    -   負荷ベースの`split region`操作[＃7623](https://github.com/tikv/tikv/pull/7623)を有効にする
    -   共通名の検証をサポート[＃7468](https://github.com/tikv/tikv/pull/7468)
    -   同じアドレスにバインドされた複数の TiKV インスタンスの起動を回避するためにファイルロックチェックを追加します[＃7447](https://github.com/tikv/tikv/pull/7447)
    -   保存時の暗号化で AWS KMS をサポート[＃7465](https://github.com/tikv/tikv/pull/7465)

-   配置Driver（PD）

    -   `config manager`削除して、他のコンポーネントがコンポーネント構成を制御できるようにします[＃2349](https://github.com/pingcap/pd/pull/2349)

-   TiFlash

    -   DeltaTreeエンジンの読み取りおよび書き込みワークロードに関連するメトリックレポートを追加します
    -   `handle`目と`version`列目をキャッシュして、単一の読み取りまたは書き込み要求のディスクI/Oを削減します。
    -   `fromUnixTime`と`dateFormat`押し下げ関数をサポート
    -   最初のディスクに従ってグローバル状態を評価し、この評価を報告する
    -   DeltaTreeエンジンの読み取りおよび書き込みワークロードに関連するグラフィックスをGrafanaに追加します
    -   `Chunk`コーデックの 10 進データエンコードを最適化します
    -   診断（SQL診断）のgRPC APIを実装して、 `INFORMATION_SCHEMA.CLUSTER_INFO`などのシステムテーブルのクエリをサポートします。

-   TiCDC

    -   Kafka シンクモジュール[＃426](https://github.com/pingcap/tiflow/pull/426)でのメッセージのバッチ送信をサポート
    -   プロセッサ[＃477](https://github.com/pingcap/tiflow/pull/477)でのファイルソートをサポート
    -   自動`resolve lock` [＃459](https://github.com/pingcap/tiflow/pull/459)サポート
    -   TiCDC サービスの GC セーフ ポイントを PD [＃487](https://github.com/pingcap/tiflow/pull/487)に自動的に更新する機能を追加します。
    -   データ複製[＃498](https://github.com/pingcap/tiflow/pull/498)タイムゾーン設定を追加する

-   バックアップと復元 (BR)

    -   storageURL [＃246](https://github.com/pingcap/br/pull/246)での S3/GCS の設定をサポート

## バグ修正 {#bug-fixes}

-   TiDB

<!---->

-   列が unsigned [＃16004](https://github.com/pingcap/tidb/pull/16004)として定義されているため、システム テーブルで負の数が正しく表示されない問題を修正しました。
-   `use_index_merge`ヒントに無効なインデックス名[＃15960](https://github.com/pingcap/tidb/pull/15960)が含まれている場合に警告を追加します
-   同じ一時ディレクトリを共有する TiDBサーバーの複数のインスタンスを禁止する[＃16026](https://github.com/pingcap/tidb/pull/16026)
-   プランキャッシュが有効な場合の`explain for connection`の実行中に発生するpanicを修正[＃16285](https://github.com/pingcap/tidb/pull/16285)
-   `tidb_capture_plan_baselines`システム変数の結果が正しく表示されない問題を修正[＃16048](https://github.com/pingcap/tidb/pull/16048)
-   `prepare`文の`group by`節が正しく解析されない問題を修正[＃16377](https://github.com/pingcap/tidb/pull/16377)
-   `analyze primary key`文[＃16081](https://github.com/pingcap/tidb/pull/16081)実行中に発生する可能性のあるpanicを修正
-   `cluster_info`システムテーブル内のTiFlashストア情報が間違っている問題を修正[＃16024](https://github.com/pingcap/tidb/pull/16024)
-   インデックスマージプロセス中に発生する可能性のあるpanicを修正[＃16360](https://github.com/pingcap/tidb/pull/16360)
-   インデックスマージリーダーが生成された列[＃16359](https://github.com/pingcap/tidb/pull/16359)を読み取るときに誤った結果が発生する可能性がある問題を修正しました
-   `show create table`文[＃16526](https://github.com/pingcap/tidb/pull/16526)のデフォルトシーケンス値の誤った表示を修正
-   シーケンスが主キー[＃16510](https://github.com/pingcap/tidb/pull/16510)のデフォルト値として使用されるために`not-null`エラーが返される問題を修正しました
-   TiKVが`StaleCommand`エラー[＃16530](https://github.com/pingcap/tidb/pull/16530)を返し続けているときに、ブロックされたSQL実行に対してエラーが報告されない問題を修正しました。
-   データベースの作成時に`COLLATE`を指定するとエラーが報告される問題を修正しました。5 `SHOW CREATE DATABASE`の結果に不足している`COLLATE`部分を追加します[＃16540](https://github.com/pingcap/tidb/pull/16540)
-   プランキャッシュが有効な場合のパーティションプルーニングの失敗を修正[＃16723](https://github.com/pingcap/tidb/pull/16723)
-   オーバーフロー[＃16755](https://github.com/pingcap/tidb/pull/16755)処理時に誤った結果を返すバグ`PointGet`修正
-   同じ時間値を持つ`slow_query`システムテーブルをクエリすると間違った結果が返される問題を修正しました[＃16806](https://github.com/pingcap/tidb/pull/16806)

<!---->

-   TiKV

    -   OpenSSLのセキュリティ問題に対処する: CVE-2020-1967 [＃7622](https://github.com/tikv/tikv/pull/7622)
    -   楽観的トランザクション[＃7604](https://github.com/tikv/tikv/pull/7604)で多くの書き込み競合が発生する場合、パフォーマンスを向上させるために`BatchRollback`で書き込まれたロールバックレコードを保護しないようにする
    -   ロック競合の負荷が高いワークロードで、トランザクションの不要なウェイクアップによって無駄な再試行が発生し、パフォーマンスが低下する問題を修正しました[＃7551](https://github.com/tikv/tikv/pull/7551)
    -   リージョンが複数回のマージでスタックする可能性がある問題を修正[＃7518](https://github.com/tikv/tikv/pull/7518)
    -   学習者[＃7518](https://github.com/tikv/tikv/pull/7518)削除しても学習者が削除されない問題を修正
    -   raft-rs [＃7408](https://github.com/tikv/tikv/pull/7408)でフォロワーの読み取りによってpanicが発生する可能性がある問題を修正しました
    -   `group by constant`エラー[＃7383](https://github.com/tikv/tikv/pull/7383)によりSQL操作が失敗する可能性があるバグを修正しました
    -   対応するプライマリロックが悲観的ロックの場合に楽観的ロックが読み取りをブロックする可能性がある問題を修正[＃7328](https://github.com/tikv/tikv/pull/7328)

-   PD

    -   一部のAPIがTLS検証に失敗する可能性がある問題を修正[＃2363](https://github.com/pingcap/pd/pull/2363)
    -   構成APIがプレフィックス[＃2354](https://github.com/pingcap/pd/pull/2354)を持つ構成項目を受け入れることができない問題を修正しました
    -   スケジューラが見つからない場合に`500`エラーが返される問題を修正しました[＃2328](https://github.com/pingcap/pd/pull/2328)
    -   `scheduler config balance-hot-region-scheduler list`コマンド[＃2321](https://github.com/pingcap/pd/pull/2321)で`404`エラーが返される問題を修正

-   TiFlash

    -   storageエンジンの粗粒度インデックス最適化を無効にする
    -   リージョンのロックを解決するときに例外がスローされ、一部のロックをスキップする必要があるというバグを修正しました。
    -   コプロセッサー統計の収集時に発生するヌルポインタ例外 (NPE) を修正しました
    -   リージョン分割/リージョン結合のプロセスが正しいことを確認するために、リージョンメタのチェックを修正しました。
    -   コプロセッサー応答のサイズが予測されないため、メッセージサイズが gRPC の制限を超える問題を修正しました
    -   TiFlashの`AdminCmdType::Split`コマンドの処理を修正
