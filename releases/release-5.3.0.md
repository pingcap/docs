---
title: TiDB 5.3 Release Notes
summary: TiDB 5.3.0では、TiDBダッシュボードに一時テーブル、テーブル属性、ユーザー権限が導入され、パフォーマンスとセキュリティが向上しました。また、TiDBデータ移行の強化、複数のTiDB Lightningインスタンスを使用した並列インポートのサポート、継続的なプロファイリングによる可観測性の向上も実現しました。互換性の変更と設定ファイルのパラメータが変更されました。このリリースには、新しいSQL機能、セキュリティ強化、安定性の向上、診断効率の向上も含まれています。さらに、TiDB、TiKV、PD、 TiFlash、TiCDCのバグ修正と改善も行われました。TiDBクラスター間の循環レプリケーション機能は削除されました。テレメトリに、TEMPORARY TABLE機能の使用状況に関する情報が含まれるようになりました。
---

# TiDB 5.3 リリースノート {#tidb-5-3-release-notes}

発売日：2021年11月30日

TiDB バージョン: 5.3.0

v5.3 の主な新機能または改善点は次のとおりです。

-   一時テーブルを導入してアプリケーションロジックを簡素化し、パフォーマンスを向上させる
-   テーブルとパーティションの属性設定をサポート
-   システムセキュリティを強化するために、TiDBダッシュボードで最小限の権限を持つユーザーの作成をサポートします。
-   TiDBのタイムスタンプ処理フローを最適化して全体的なパフォーマンスを向上させる
-   TiDBデータ移行（DM）のパフォーマンスを強化し、MySQLからTiDBへのデータ移行のレイテンシーを低減します。
-   複数のTiDB Lightningインスタンスを使用した並列インポートをサポートし、完全なデータ移行の効率を向上します。
-   単一のSQL文でクラスタのオンサイト情報を保存・復元する機能をサポートし、実行計画に関する問題のトラブルシューティング効率を向上します。
-   データベースパフォーマンスの観測性を向上させるために、継続的なプロファイリングの実験的機能をサポートします。
-   システムのパフォーマンスと安定性を向上させるために、storageとコンピューティングエンジンの最適化を継続します。
-   I/O 操作をRaftstoreスレッド プールから分離することで、TiKV の書き込みレイテンシーを削減します (デフォルトでは無効)

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v5.3.0 にアップグレードする場合、すべての中間バージョンの互換性変更ノートを知りたい場合は、該当するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                               | タイプを変更   | 説明                                                                                                                                                                                                                                                                            |
| :---------------------------------------------------------------------------------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)                        | 修正済み     | 一時テーブルが TiDB でサポートされるようになったため、 `CREATE TEMPORARY TABLE`と`DROP TEMPORARY TABLE` `tidb_enable_noop_functions`有効にする必要がなくなりました。                                                                                                                                                   |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530) | 新しく追加された | テーブルの統計情報が期限切れになった場合のオプティマイザの動作を制御します。デフォルト値は`ON`です。テーブル内の変更された行数が総行数の80%を超える場合（この比率は設定[`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)で調整できます）、オプティマイザは総行数以外の統計情報は信頼できないと判断し、代わりに疑似統計情報を使用します。値を`OFF`に設定すると、統計情報が期限切れになってもオプティマイザは引き続きそれらを使用します。 |
| [`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)               | 新しく追加された | TSOFollowerプロキシ機能を有効または無効にします。デフォルト値は`OFF`で、これはTSOFollowerプロキシ機能が無効であることを意味します。この場合、TiDBはPDリーダーからのみTSOを取得します。この機能を有効にすると、TiDBはTSOを取得する際にすべてのPDノードに均等にリクエストを送信します。PDフォロワーはTSOリクエストを転送することで、PDリーダーのCPU負荷を軽減します。                                                                 |
| [`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530)     | 新しく追加された | TiDBがPDにTSOを要求した際に、バッチ保存操作の最大待機時間を設定します。デフォルト値は`0`で、追加の待機時間はありません。                                                                                                                                                                                                            |
| [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530)                             | 新しく追加された | [一時テーブル](/temporary-tables.md)個の最大サイズを制限します。一時テーブルがこのサイズを超えるとエラーが発生します。                                                                                                                                                                                                       |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション項目                                                                                       | タイプを変更   | 説明                                                                                                                                                                                            |
| :------------- | :------------------------------------------------------------------------------------------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティドブ           | [`prepared-plan-cache.capacity`](/tidb-configuration-file.md#capacity)                             | 修正済み     | キャッシュされるステートメントの数を制御します。デフォルト値は`100`から`1000`に変更されます。                                                                                                                                          |
| TiKV           | [`storage.reserve-space`](/tikv-configuration-file.md#reserve-space)                               | 修正済み     | TiKV起動時にディスク保護のために予約される領域を制御します。v5.3.0以降では、予約領域の80%がディスク容量不足時の運用・保守に必要な追加ディスク領域として使用され、残りの20%は一時ファイルの保存に使用されます。                                                                               |
| ティクブ           | `memory-usage-limit`                                                                               | 修正済み     | この構成項目は TiDB v5.3.0 で新しく追加され、その値はstorageの.block-cache.capacity に基づいて計算されます。                                                                                                                   |
| TiKV           | [`raftstore.store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)       | 新しく追加された | Raft I/Oタスクを処理するスレッドの許容数。これはStoreWriterスレッドプールのサイズです。このスレッドプールのサイズを変更する場合は、 [TiKV スレッドプールのパフォーマンスチューニング](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools)を参照してください。 |
| TiKV           | [`raftstore.raft-write-size-limit`](/tikv-configuration-file.md#raft-write-size-limit-new-in-v530) | 新しく追加された | Raftデータがディスクに書き込まれるしきい値を決定します。データサイズがこの設定項目の値より大きい場合、データはディスクに書き込まれます。1の値が`raftstore.store-io-pool-size` `0`場合、この設定項目は有効になりません。                                                               |
| TiKV           | `raftstore.raft-msg-flush-interval`                                                                | 新しく追加された | Raftメッセージをバッチ送信する間隔を指定します。バッチ送信されたRaftメッセージは、この設定項目で指定された間隔ごとに送信されます。1の値が`raftstore.store-io-pool-size` `0`場合、この設定項目は無効になります。                                                                 |
| TiKV           | `raftstore.raft-reject-transfer-leader-duration`                                                   | 削除済み     | Leaderが新しく追加されたノードに転送される最小期間を決定します。                                                                                                                                                           |
| PD             | [`log.file.max-days`](/pd-configuration-file.md#max-days)                                          | 修正済み     | ログを保持する最大日数を制御します。デフォルト値は`1`から`0`に変更されます。                                                                                                                                                     |
| PD             | [`log.file.max-backups`](/pd-configuration-file.md#max-backups)                                    | 修正済み     | 保持されるログの最大数を制御します。デフォルト値は`7`から`0`に変更されます。                                                                                                                                                     |
| PD             | [`patrol-region-interval`](/pd-configuration-file.md#patrol-region-interval)                       | 修正済み     | replicaChecker がリージョンのヘルス状態をチェックする実行頻度を制御します。この値が小さいほど、replicaChecker の実行速度が速くなります。通常、このパラメータを調整する必要はありません。デフォルト値は`100ms`から`10ms`に変更されています。                                                   |
| PD             | [`max-snapshot-count`](/pd-configuration-file.md#max-snapshot-count)                               | 修正済み     | 単一のストアが同時に受信または送信するスナップショットの最大数を制御します。PDスケジューラは、この設定に基づいて、通常のトラフィックに使用されるリソースがプリエンプトされるのを防ぎます。デフォルト値は`3`から`64`に変更されました。                                                                       |
| PD             | [`max-pending-peer-count`](/pd-configuration-file.md#max-pending-peer-count)                       | 修正済み     | 単一ストア内の保留中のピアの最大数を制御します。PDスケジューラはこの設定に依存して、一部のノードで古いログを持つリージョンが過剰に生成されるのを防ぎます。デフォルト値は`16`から`64`に変更されました。                                                                                      |
| TiDライトニング      | `meta-schema-name`                                                                                 | 新しく追加された | ターゲットクラスター内の各TiDB Lightningインスタンスのメタ情報が格納されるスキーマ名。デフォルト値は「lightning_metadata」です。                                                                                                              |

### その他 {#others}

-   一時テーブル:

    -   TiDB クラスター v5.3.0 より前のバージョンでローカル一時テーブルを作成した場合、これらのテーブルは通常のテーブルであり、クラスターを v5.3.0 以降にアップグレードした後も通常のテーブルとして扱われます。v5.3.0 以降のバージョンの TiDB クラスターでグローバル一時テーブルを作成した場合、クラスターを v5.3.0 より前のバージョンにダウングレードすると、これらのテーブルは通常のテーブルとして扱われ、データエラーが発生します。
    -   v5.3.0以降、TiCDCとBRは[グローバル一時テーブル](/temporary-tables.md#global-temporary-tables)サポートします。v5.3.0より前のバージョンのTiCDCとBRを使用してグローバル一時テーブルをダウンストリームに複製すると、テーブル定義エラーが発生します。
    -   次のクラスターは、v5.3.0 以降である必要があります。そうでない場合、グローバル一時テーブルを作成するときにデータ エラーが報告されます。

        -   TiDB移行ツールを使用してインポートするクラスター
        -   TiDB移行ツールを使用してクラスタを復元しました
        -   TiDB移行ツールを使用したレプリケーションタスクの下流クラスタ
    -   一時テーブルの互換性情報については、 [MySQL 一時テーブルとの互換性](/temporary-tables.md#compatibility-with-mysql-temporary-tables)および[他の TiDB 機能との互換性の制限](/temporary-tables.md#compatibility-restrictions-with-other-tidb-features)を参照してください。

-   v5.3.0より前のリリースでは、システム変数が無効な値に設定された場合、TiDBはエラーを報告します。v5.3.0以降のリリースでは、システム変数が無効な値に設定された場合、TiDBは「|警告 | 1292 | 切り捨てられた不正なxxx: &#39;xx&#39;」などの警告とともに成功を返します。

-   `SHOW CREATE VIEW`実行するために`SHOW VIEW`権限が必要ない問題を修正しました。これで、 `SHOW CREATE VIEW`文を実行するには`SHOW VIEW`権限が必要になります。

-   システム変数`sql_auto_is_null`が noop関数に追加されます。 `tidb_enable_noop_functions = 0/OFF`の場合、この変数値を変更するとエラーが発生します。

-   `GRANT ALL ON performance_schema.*`構文は許可されなくなりました。この文を TiDB で実行するとエラーが発生します。

-   バージョン5.3.0より前のバージョンでは、新しいインデックスが追加されると、指定期間外でも自動分析が予期せず実行される問題を修正しました。バージョン5.3.0では、変数`tidb_auto_analyze_start_time`と`tidb_auto_analyze_end_time`で期間を設定すると、その期間のみ自動分析が実行されます。

-   プラグインのデフォルトのstorageディレクトリが`""`から`/data/deploy/plugin`に変更されます。

-   DMコードは[TiCDCコードリポジトリのフォルダ「dm」](https://github.com/pingcap/tiflow/tree/release-5.3/dm)に移行されました。DMのバージョン番号はTiDBに準じます。v2.0.xの次に新しいDMバージョンはv5.3.0となり、v2.0.xからv5.3.0へのアップグレードはリスクなしで行えます。

-   Prometheusのデフォルトのデプロイバージョンは、v2.8.1から2021年5月にリリースされる[バージョン2.27.1](https://github.com/prometheus/prometheus/releases/tag/v2.27.1)にアップグレードされました。このバージョンでは、より多くの機能が提供され、セキュリティ問題が修正されています。Prometheus v2.8.1と比較して、v2.27.1ではアラートの時刻表示がUnixタイムスタンプからUTCに変更されました。詳細は[プロメテウスコミット](https://github.com/prometheus/prometheus/commit/7646cbca328278585be15fa615e22f2a50b47d06)を参照してください。

## 新機能 {#new-features}

### SQL {#sql}

-   **SQL インターフェースを使用してデータの配置ルールを設定する（実験的機能）**

    データの配置ルールを設定するためのSQLインターフェースを提供する`[CREATE | ALTER] PLACEMENT POLICY`構文をサポートします。この機能を使用すると、特定のリージョン、データセンター、ラック、ホスト、またはレプリカ数ルールにスケジュールするテーブルとパーティションを指定できます。これにより、コスト削減と柔軟性の向上というアプリケーションの要求を満たすことができます。一般的なユーザーシナリオは以下のとおりです。

    -   異なるアプリケーションの複数のデータベースを統合してデータベースのメンテナンスコストを削減し、ルール構成を通じてアプリケーションリソースの分離を実現します。
    -   重要なデータのレプリカ数を増やして、アプリケーションの可用性とデータの信頼性を向上させます。
    -   新しいデータを SSD に保存し、古いデータを HHD に保存することで、データのアーカイブとstorageのコストを削減します。
    -   ホットスポットデータのリーダーを高性能TiKVインスタンスにスケジュールする
    -   コスト効率を向上させるために、コールドデータを低コストのstorageメディアに分離する

    [ユーザードキュメント](/placement-rules-in-sql.md) [＃18030](https://github.com/pingcap/tidb/issues/18030)

-   **一時テーブル**

    一時テーブルを作成するための`CREATE [GLOBAL] TEMPORARY TABLE`文をサポートします。この機能を使用すると、アプリケーションの計算処理中に生成される一時データを簡単に管理できます。一時データはメモリに保存され、 `tidb_tmp_table_max_size`変数を使用して一時テーブルのサイズを制限できます。TiDBは以下の種類の一時テーブルをサポートしています。

    -   グローバル一時テーブル
        -   クラスター内のすべてのセッションに表示され、テーブル スキーマは永続的です。
        -   トランザクションレベルのデータ分離を提供します。一時データはトランザクション内でのみ有効です。トランザクションが終了すると、データは自動的に削除されます。
    -   ローカル一時テーブル

        -   現在のセッションにのみ表示され、テーブル スキーマは永続的ではありません。
        -   重複したテーブル名をサポートします。アプリケーションに複雑な命名規則を設計する必要はありません。
        -   セッションレベルのデータ分離を提供し、よりシンプルなアプリケーションロジックの設計を可能にします。トランザクションが完了すると、一時テーブルは削除されます。

        [ユーザードキュメント](/temporary-tables.md) [＃24169](https://github.com/pingcap/tidb/issues/24169)

-   **`FOR UPDATE OF TABLES`構文をサポートする**

    複数のテーブルを結合する SQL 文の場合、 TiDB は、 `OF TABLES`に含まれるテーブルに関連付けられた行に対する悲観的ロックの取得をサポートします。

    [ユーザードキュメント](/sql-statements/sql-statement-select.md) [＃28689](https://github.com/pingcap/tidb/issues/28689)

-   **表属性**

    テーブルまたはパーティションの属性を設定できる`ALTER TABLE [PARTITION] ATTRIBUTES`ステートメントをサポートします。現在、TiDB は`merge_option`属性の設定のみをサポートしています。この属性を追加することで、リージョンのマージ動作を明示的に制御できます。

    ユーザーシナリオ： `SPLIT TABLE`操作を実行すると、一定期間（PDパラメータ[`split-merge-interval`](/pd-configuration-file.md#split-merge-interval)で制御）経過してもデータが挿入されない場合、空のリージョンはデフォルトで自動的にマージされます。この場合、テーブル属性を`merge_option=deny`に設定することで、リージョンの自動マージを回避できます。

    [ユーザードキュメント](/table-attributes.md) [＃3839](https://github.com/tikv/pd/issues/3839)

### Security {#security}

-   **TiDB ダッシュボードで最小限の権限を持つユーザーの作成をサポート**

    TiDBダッシュボードのアカウントシステムは、 TiDB SQLのアカウントシステムと一致しています。TiDBダッシュボードにアクセスするユーザーは、TiDB SQLユーザーの権限に基づいて認証および承認されます。そのため、TiDBダッシュボードでは限定的な権限、つまり読み取り専用権限のみが必要です。最小限の権限の原則に基づいてユーザーがTiDBダッシュボードにアクセスできるように設定することで、高い権限を持つユーザーのアクセスを回避できます。

    TiDBダッシュボードにアクセスしてサインインするには、最小限の権限を持つSQLユーザーを作成することをお勧めします。これにより、高い権限を持つユーザーによるアクセスを回避し、セキュリティを向上できます。

    [ユーザードキュメント](/dashboard/dashboard-user.md)

### パフォーマンス {#performance}

-   **PDのタイムスタンプ処理フローを最適化**

    TiDBは、PDFollowerプロキシを有効にし、PDクライアントがTSOをバッチで要求する際に必要なバッチ待機時間を変更することで、タイムスタンプ処理フローを最適化し、PDのタイムスタンプ処理負荷を軽減します。これにより、システム全体のスケーラビリティが向上します。

    -   システム変数[`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)を介して PDFollowerプロキシの有効化/無効化をサポートします。PD の TSO リクエスト負荷が高すぎる場合、PD フォロワープロキシを有効にすると、フォロワーのリクエストサイクル中に収集された TSO リクエストをリーダーノードに一括転送できます。このソリューションにより、クライアントとリーダー間の直接的なインタラクション数を効果的に削減し、リーダーへの負荷を軽減し、TiDB 全体のパフォーマンスを向上させることができます。

    > **注記：**
    >
    > クライアント数が少なく、PD リーダーの CPU 負荷が満杯でない場合は、PDFollowerプロキシを有効にすることはお勧めしません。

    -   システム変数[`tidb_tso_client_batch_max_wait_time`](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530)を使用して、PDクライアントがTSOをバッチリクエストするために必要な最大待機時間を設定できます。この時間の単位はミリ秒です。PDのTSOリクエスト負荷が高い場合は、待機時間を増やしてバッチサイズを大きくすることで、負荷を軽減し、スループットを向上させることができます。

    > **注記：**
    >
    > TSO 要求負荷が高くない場合は、この変数値を変更することはお勧めしません。

    [ユーザードキュメント](/system-variables.md#tidb_tso_client_batch_max_wait_time-new-in-v530) [＃3149](https://github.com/tikv/pd/issues/3149)

### 安定性 {#stability}

-   **一部の店舗が永久的に損傷した後のオンラインの安全でない回復をサポートします（実験的機能）**

    オンラインデータアンセーフリカバリを実行するコマンド`pd-ctl unsafe remove-failed-stores`をサポートします。データレプリカの大部分が永続的な損傷（ディスク損傷など）などの問題に遭遇し、それらの問題によってアプリケーションのデータ範囲が読み取りまたは書き込み不能になったとします。このような場合、PDに実装されているオンラインアンセーフリカバリ機能を使用してデータをリカバリし、再び読み取りまたは書き込み可能になります。

    機能関連の操作は、TiDB チームのサポートを受けて実行することをお勧めします。

    [ユーザードキュメント](/online-unsafe-recovery.md) [＃10483](https://github.com/tikv/tikv/issues/10483)

### データ移行 {#data-migration}

-   **DMレプリケーションパフォーマンスの強化**

    MySQL から TiDB への低レイテンシのデータレプリケーションを保証するために、次の機能をサポートしています。

    -   1行の複数の更新を1つのステートメントにまとめる
    -   複数行のバッチ更新を1つのステートメントにマージする

-   **DM クラスターをより適切に管理するために DM OpenAPI を追加します (実験的機能)**

    DMは、DMクラスタのクエリと操作のためのOpenAPI機能を提供します。これは[dmctlツール](/dm/dmctl-introduction.md)の機能に類似しています。

    現在、DM OpenAPI は実験的機能であり、デフォルトで無効になっています。本番環境での使用は推奨されません。

    [ユーザードキュメント](/dm/dm-open-api.md)

-   **TiDB Lightning並行輸入品**

    TiDB Lightningは、従来の機能を拡張し、並列インポート機能を提供します。複数のLightningインスタンスを同時にデプロイすることで、単一または複数のテーブルを下流のTiDBに並列インポートできます。お客様の利用方法を変えることなく、データ移行能力を大幅に向上させ、よりリアルタイムなデータ移行を実現し、さらなる処理、統合、分析を可能にします。これにより、企業のデータ管理効率が向上します。

    当社のテストでは、10個のTiDB Lightningインスタンスを使用して、合計20TiBのMySQLデータを8時間以内にTiDBにインポートできました。複数テーブルのインポートパフォーマンスも向上しました。1個のTiDB Lightningインスタンスで250GiB/hのインポートをサポートし、全体的な移行速度は従来の8倍に向上しました。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-distributed-import.md)

-   **TiDB Lightning事前チェック**

    TiDB Lightningは、移行タスクを実行する前に設定を確認する機能を提供します。これはデフォルトで有効になっています。この機能は、ディスク容量と実行設定に関するいくつかの定期的なチェックを自動的に実行します。主な目的は、後続のインポートプロセス全体がスムーズに実行されるようにすることです。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-prechecks.md)

-   **TiDB LightningはGBK文字セットのファイルのインポートをサポートします**

    ソースデータファイルの文字セットを指定できます。TiDB TiDB Lightningは、インポートプロセス中に、指定された文字セットからUTF-8エンコードに変換します。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-configuration.md)

-   **同期差分インスペクタの改善**

    -   比較速度を375 MB/秒から700 MB/秒に向上
    -   比較中にTiDBノードのメモリ消費量をほぼ半分に削減
    -   ユーザーインターフェースを最適化し、比較中に進行状況バーを表示します

    [ユーザードキュメント](/sync-diff-inspector/sync-diff-inspector-overview.md)

### 診断効率 {#diagnostic-efficiency}

-   **クラスターのオンサイト情報を保存および復元する**

    TiDB クラスタの問題を特定してトラブルシューティングする際には、システム情報やクエリプランの情報が必要になることがよくあります。より便利かつ効率的に情報を取得し、クラスタの問題をトラブルシューティングできるよう、TiDB v5.3.0 では`PLAN REPLAYER`コマンドが導入されました。このコマンドを使用すると、クラスタのオンサイト情報を簡単に保存・復元できるため、トラブルシューティングの効率が向上し、管理のために問題をアーカイブしやすくなります。

    `PLAN REPLAYER`の特徴は以下のとおりです。

    -   オンサイトトラブルシューティング時の TiDB クラスターの情報を ZIP 形式のファイルにエクスポートしてstorage。
    -   別のTiDBクラスタからエクスポートされたZIP形式のファイルをクラスタにインポートします。このファイルには、オンサイトトラブルシューティング時の後者のTiDBクラスタの情報が含まれています。

    [ユーザードキュメント](/sql-plan-replayer.md) [＃26325](https://github.com/pingcap/tidb/issues/26325)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   **TiCDC 結果的に一貫性のあるレプリケーション**

    TiCDCは、災害シナリオにおいて結果整合性のあるレプリケーション機能を提供します。プライマリTiDBクラスタで災害が発生し、短期間でサービスを再開できない場合、TiCDCはセカンダリクラスタのデータの整合性を確保する機能を提供する必要があります。同時に、TiCDCは、データベースが長時間利用できなくなり業務に支障をきたすことを回避するため、ビジネス部門がトラフィックをセカンダリクラスタに迅速に切り替えられるようにする必要があります。

    この機能は、TiCDC が TiDB クラスターからセカンダリリレーショナルデータベース TiDB/ Aurora/MySQL/MariaDB に増分データをレプリケーションすることをサポートします。プライマリクラスターがクラッシュした場合、災害発生前の TiCDC のレプリケーション状態が正常で、レプリケーション遅延が小さいという条件付きで、TiCDC は 5 分以内にセカンダリクラスターをプライマリクラスター内の特定のスナップショットに復旧できます。これにより、データ損失は 30 分未満、つまり RTO &lt;= 5 分、RPO &lt;= 30 分を実現できます。

    [ユーザードキュメント](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios)

-   **TiCDCは、TiCDCタスクを管理するためのHTTPプロトコルOpenAPIをサポートしています。**

    TiDB v5.3.0以降、TiCDC OpenAPIが一般提供（GA）されました。本番環境では、OpenAPIを使用してTiCDCクラスターのクエリと操作を行うことができます。

### 展開と保守 {#deployment-and-maintenance}

-   **継続的なプロファイリング（実験的機能）**

    TiDBダッシュボードは、TiDBクラスターの稼働中にインスタンスのパフォーマンス分析結果をリアルタイムで自動保存する継続的プロファイリング機能をサポートしています。パフォーマンス分析結果はフレームグラフで確認できるため、より詳細な観察が可能になり、トラブルシューティングにかかる時間を短縮できます。

    この機能はデフォルトで無効になっており、TiDB ダッシュボードの**継続プロファイル**ページで有効にする必要があります。

    この機能は、 TiUP v1.7.0 以降を使用してアップグレードまたはインストールされたクラスターでのみ使用できます。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

## テレメトリー {#telemetry}

TiDBは、TEMPORARY TABLE機能が使用されているかどうかに関する情報をテレメトリレポートに追加します。これにはテーブル名やテーブルデータは含まれません。

テレメトリの詳細とこの動作を無効にする方法については、 [テレメトリー](/telemetry.md)を参照してください。

## 削除された機能 {#removed-feature}

TiCDC v5.3.0以降、TiDBクラスター間の循環レプリケーション機能（v5.0.0では実験的機能）は削除されました。TiCDCのアップグレード前にこの機能を使用してデータをレプリケーションしていた場合、アップグレード後も関連データは影響を受けません。

## 改善点 {#improvements}

-   ティドブ

    -   コプロセッサがロックに遭遇したときに影響を受けるSQL文をデバッグログに表示します。これは問題の診断に役立ちます[＃27718](https://github.com/pingcap/tidb/issues/27718)
    -   SQL論理レイヤー[＃27247](https://github.com/pingcap/tidb/issues/27247)でデータをバックアップおよび復元するときに、バックアップおよび復元データのサイズを表示する機能をサポート
    -   `tidb_analyze_version`が`2`場合の ANALYZE のデフォルトのコレクション ロジックを改善し、コレクションを高速化し、リソースのオーバーヘッドを削減します。
    -   `ANALYZE TABLE table_name COLUMNS col_1, col_2, ... , col_n`構文を導入します。この構文を使用すると、幅の広いテーブル内の一部の列のみの統計情報を収集できるため、統計収集の速度が向上します。

-   ティクブ

    -   ディスクスペース保護を強化してstorageの安定性を向上

        ディスク書き込みエラーが発生した場合にTiKVがpanicに陥る可能性がある問題を解決するため、TiKVは2段階のしきい値防御メカニズムを導入し、過剰なトラフィックによるディスク残容量の枯渇を防ぎます。さらに、このメカニズムは、しきい値に達した際に領域を回収する機能も提供します。残容量しきい値に達すると、一部の書き込み操作が失敗し、TiKVはディスクフルエラーとディスクフルノードのリストを返します。この場合、領域を回復してサービスを復旧するには、 `Drop/Truncate Table`実行するか、ノードをスケールアウトします。

    -   L0フロー制御[＃10879](https://github.com/tikv/tikv/issues/10879)のアルゴリズムを簡素化する

    -   ラフトクライアントモジュール[＃10944](https://github.com/tikv/tikv/pull/10944)のエラーログレポートを改善

    -   パフォーマンスのボトルネックにならないようにログスレッドを改善する[＃10841](https://github.com/tikv/tikv/issues/10841)

    -   書き込みクエリの統計タイプを追加する[＃10507](https://github.com/tikv/tikv/issues/10507)

    -   I/O操作をRaftstoreスレッドプールから分離することで、書き込みレイテンシーを削減します（デフォルトでは無効）。チューニングの詳細については、 [TiKV スレッド プールのパフォーマンスを調整する](/tune-tikv-thread-performance.md) [＃10540](https://github.com/tikv/tikv/issues/10540)を参照してください。

-   PD

    -   ホットスポット スケジューラ[＃3869](https://github.com/tikv/pd/issues/3869)の QPS ディメンションに書き込みクエリの種類を追加する
    -   バランスリージョンスケジューラの再試行制限を動的に調整して、スケジューラ[＃3744](https://github.com/tikv/pd/issues/3744)のパフォーマンスを向上させることをサポートします。
    -   TiDBダッシュボードをv2021.10.08.1 [＃4070](https://github.com/tikv/pd/pull/4070)に更新
    -   リーダー排除スケジューラが不健全なピアを持つリージョンをスケジュールできるようにサポート[＃4093](https://github.com/tikv/pd/issues/4093)
    -   スケジューラ[＃4146](https://github.com/tikv/pd/issues/4146)の終了プロセスを高速化

-   TiFlash

    -   TableScanオペレータの実行効率を大幅に向上

    -   Exchangeオペレーターの実行効率を向上させる

    -   storageエンジンの GC 中の書き込み増幅とメモリ使用量を削減します (実験的機能)

    -   TiFlash の再起動時にTiFlashの安定性と可用性が向上し、再起動後に発生する可能性のあるクエリの失敗が減少します。

    -   複数の新しい文字列および時間関数を MPP エンジンにプッシュダウンする機能をサポート

        -   文字列関数: LIKE パターン、FORMAT()、LOWER()、LTRIM()、RTRIM()、SUBSTRING_INDEX()、TRIM()、UCASE()、UPPER()
        -   数学関数：ROUND（小数点、整数）
        -   日付と時刻関数: HOUR(), MICROSECOND(), MINUTE(), SECOND(), SYSDATE()
        -   型変換関数: CAST(time, real)
        -   集計関数: GROUP_CONCAT(), SUM(enum)

    -   512ビットSIMDをサポート

    -   古いデータのクリーンアップアルゴリズムを強化してディスク使用量を削減し、ファイルをより効率的に読み取ります

    -   一部のLinux以外のシステムでダッシュボードにメモリやCPUの情報が表示されない問題を修正

    -   TiFlashログ ファイルの命名スタイルを統一し (TiKV の命名スタイルと一貫性を保つ)、logger.count と logger.size の動的な変更をサポートします。

    -   列ベースのファイルのデータ検証機能の改善（チェックサム、実験的機能）

-   ツール

    -   TiCDC

        -   Kafka シンク構成項目`MaxMessageBytes`のデフォルト値を 64 MB から 1 MB に減らし、大きなメッセージが Kafka ブローカー[＃3104](https://github.com/pingcap/tiflow/pull/3104)によって拒否される問題を修正しました。
        -   レプリケーションパイプラインのメモリ使用量を削減する[＃2553](https://github.com/pingcap/tiflow/issues/2553) [＃3037](https://github.com/pingcap/tiflow/pull/3037) [＃2726](https://github.com/pingcap/tiflow/pull/2726)
        -   監視項目とアラートルールを最適化して、同期リンク、メモリGC、および在庫データスキャンプロセスの可観測性を向上させる[＃2735](https://github.com/pingcap/tiflow/pull/2735) [＃1606](https://github.com/pingcap/tiflow/issues/1606) [＃3000](https://github.com/pingcap/tiflow/pull/3000) [＃2985](https://github.com/pingcap/tiflow/issues/2985) [＃2156](https://github.com/pingcap/tiflow/issues/2156)
        -   同期タスクのステータスが正常であれば、ユーザーの誤解を避けるために、過去のエラーメッセージは表示されなくなります[＃2242](https://github.com/pingcap/tiflow/issues/2242)

## バグ修正 {#bug-fixes}

-   ティドブ

    -   実行中に発生するエラーを修正しました。これは、パーティションテーブル[＃27797](https://github.com/pingcap/tidb/issues/27797) [＃26554](https://github.com/pingcap/tidb/issues/26554)で集計演算子をプッシュダウンする際に、スキーマ列の浅いコピーが行われることが原因で発生します。
    -   `plan cache`符号なしフラグの変更を検出できない問題を修正[＃28254](https://github.com/pingcap/tidb/issues/28254)
    -   パーティション関数が範囲外の場合の誤ったパーティションプルーニングを修正[＃28233](https://github.com/pingcap/tidb/issues/28233)
    -   プランナーが場合によっては無効なプランをキャッシュする可能性がある問題を修正`join` [＃28087](https://github.com/pingcap/tidb/issues/28087)
    -   ハッシュ列の型が`enum` [＃27893](https://github.com/pingcap/tidb/issues/27893)の場合の誤った`IndexLookUpJoin`修正
    -   アイドル接続をリサイクルすると、まれにリクエストの送信がブロックされる可能性があるバッチクライアントのバグを修正しました[＃27688](https://github.com/pingcap/tidb/pull/27688)
    -   ターゲット クラスタ[＃27686](https://github.com/pingcap/tidb/pull/27686)でチェックサムの実行に失敗した場合のTiDB Lightningpanic問題を修正しました。
    -   いくつかのケースで`date_add`と`date_sub`関数の誤った結果を修正[＃27232](https://github.com/pingcap/tidb/issues/27232)
    -   ベクトル化された式[＃28643](https://github.com/pingcap/tidb/issues/28643)の関数`hour`の誤った結果を修正します
    -   MySQL 5.1 またはそれ以前のクライアントバージョン[＃27855](https://github.com/pingcap/tidb/issues/27855)に接続する際の認証の問題を修正しました
    -   新しいインデックスが追加されたときに、指定された時間外にauto analyzeがトリガーされる可能性がある問題を修正しました[＃28698](https://github.com/pingcap/tidb/issues/28698)
    -   セッション変数を設定すると`tidb_snapshot` [＃28683](https://github.com/pingcap/tidb/pull/28683)が無効になるバグを修正
    -   ピアが見つからないリージョンが多数あるクラスタでBRが機能しないバグを修正[＃27534](https://github.com/pingcap/tidb/issues/27534)
    -   サポートされていない`cast` TiFlash [＃23907](https://github.com/pingcap/tidb/issues/23907)にプッシュダウンされたときに発生する`tidb_cast to Int32 is not supported`のような予期しないエラーを修正しました
    -   `%s value is out of range in '%s'`エラーメッセージ[＃27964](https://github.com/pingcap/tidb/issues/27964)に`DECIMAL overflow`が欠落している問題を修正
    -   MPPノードの可用性検出が一部のコーナーケースで機能しないバグを修正[＃3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [＃27952](https://github.com/pingcap/tidb/issues/27952)を割り当てる際の`DATA RACE`問題を修正
    -   空の`dual table` [＃28250](https://github.com/pingcap/tidb/issues/28250)を削除した後のMPPクエリの`INDEX OUT OF RANGE`エラーを修正
    -   MPPクエリ[＃1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラーログ`invalid cop task execution summaries length`の問題を修正
    -   MPPクエリ[＃28149](https://github.com/pingcap/tidb/pull/28149)のエラーログ`cannot found column in Schema column`の問題を修正
    -   TiFlashがシャットダウンするときに TiDB がpanic可能性がある問題を修正[＃28096](https://github.com/pingcap/tidb/issues/28096)
    -   安全でない3DES（トリプルデータ暗号化アルゴリズム）ベースのTLS暗号スイート[＃27859](https://github.com/pingcap/tidb/pull/27859)のサポートを削除します。
    -   Lightning が事前チェック中にオフラインの TiKV ノードに接続し、インポートに失敗する問題を修正しました[＃27826](https://github.com/pingcap/tidb/pull/27826)
    -   多数のファイルをテーブル[＃27605](https://github.com/pingcap/tidb/issues/27605)にインポートするときに事前チェックに時間がかかりすぎる問題を修正しました
    -   式[＃27146](https://github.com/pingcap/tidb/issues/27146)書き換えると間違った照合順序が推測される問題を修正`between`
    -   `group_concat`関数が照合順序を考慮していなかった問題を修正[＃27429](https://github.com/pingcap/tidb/issues/27429)
    -   `extract`関数の引数が負の期間[＃27236](https://github.com/pingcap/tidb/issues/27236)場合に発生する結果の誤りを修正
    -   `NO_UNSIGNED_SUBTRACTION` [＃26765](https://github.com/pingcap/tidb/issues/26765)に設定されている場合にパーティションの作成が失敗する問題を修正
    -   列プルーニングと集計プッシュダウン[＃27106](https://github.com/pingcap/tidb/issues/27106)で副作用のある式を避ける
    -   不要なgRPCログを削除する[＃24190](https://github.com/pingcap/tidb/issues/24190)
    -   有効な小数点以下の桁数を制限することで精度関連の問題を修正する[＃3091](https://github.com/pingcap/tics/issues/3091)
    -   `plus`式[＃26977](https://github.com/pingcap/tidb/issues/26977)のオーバーフローのチェック方法が間違っている問題を修正
    -   `new collation`データを持つテーブルから統計をダンプするときに`data too long`エラーが発生する問題を修正しました[＃27024](https://github.com/pingcap/tidb/issues/27024)
    -   再試行されたトランザクションのステートメントが`TIDB_TRX` [＃28670](https://github.com/pingcap/tidb/pull/28670)に含まれない問題を修正
    -   `plugin_dir`構成[＃28084](https://github.com/pingcap/tidb/issues/28084)の誤ったデフォルト値を修正
    -   名前付きタイムゾーンとUTCオフセット[＃8311](https://github.com/pingcap/tidb/issues/8311)が指定された場合、 `CONVERT_TZ`関数が`NULL`返す問題を修正しました。
    -   `CREATE SCHEMA`ステートメント[＃27214](https://github.com/pingcap/tidb/issues/27214)の一部として何も提供されていない場合、新しいスキーマに対して`character_set_server`と`collation_server`で指定された文字セットを使用しない問題を修正しました。

-   ティクブ

    -   リージョン移行時にRaftstoreのデッドロックによりTiKVが利用できなくなる問題を修正しました。回避策としては、スケジュールを無効にし、利用できないTiKV [＃10909](https://github.com/tikv/tikv/issues/10909)を再起動してください。
    -   輻輳エラー[＃11082](https://github.com/tikv/tikv/issues/11082)によりCDCがスキャン再試行を頻繁に追加する問題を修正
    -   チャネルがいっぱいになるとRaft接続が切断される問題を修正[＃11047](https://github.com/tikv/tikv/issues/11047)
    -   Raftクライアント実装[＃9714](https://github.com/tikv/tikv/issues/9714)でバッチメッセージが大きすぎる問題を修正
    -   `resolved_ts` [＃10965](https://github.com/tikv/tikv/issues/10965)で一部のコルーチンがリークする問題を修正
    -   応答サイズが4 GiBを超えるとコプロセッサに発生するpanic問題を修正[＃9012](https://github.com/tikv/tikv/issues/9012)
    -   スナップショット ファイルがガベージ コレクションできない場合に、スナップショット ガベージ コレクション (GC) で GC スナップショット ファイルが失われる問題を修正しました[＃10813](https://github.com/tikv/tikv/issues/10813)
    -   コプロセッサー要求の処理中にタイムアウトによって発生するpanic問題を修正[＃10852](https://github.com/tikv/tikv/issues/10852)
    -   統計スレッド[＃11195](https://github.com/tikv/tikv/issues/11195)の監視データによって発生するメモリリークを修正しました
    -   一部のプラットフォームから cgroup 情報を取得する際に発生するpanic問題を修正[＃10980](https://github.com/tikv/tikv/pull/10980)
    -   MVCC 削除バージョンが圧縮フィルタ GC [＃11248](https://github.com/tikv/tikv/pull/11248)によって削除されないため、スキャン パフォーマンスが低下する問題を修正しました。

-   PD

    -   ピア数が設定されたピア数[＃4045](https://github.com/tikv/pd/issues/4045)を超えたために、PD がデータがあり保留中の状態のピアを誤って削除する問題を修正しました。
    -   PDが時間内にピアを固定しない問題を修正[＃4077](https://github.com/tikv/pd/issues/4077)
    -   散布範囲スケジューラが空のリージョン[＃4118](https://github.com/tikv/pd/pull/4118)をスケジュールできない問題を修正しました
    -   キーマネージャのCPU使用率が高すぎる問題を修正[＃4071](https://github.com/tikv/pd/issues/4071)
    -   ホットリージョンスケジューラ[＃4159](https://github.com/tikv/pd/issues/4159)の設定時に発生する可能性のあるデータ競合の問題を修正しました。
    -   リージョン機能[＃3936](https://github.com/tikv/pd/issues/3936)スタックによりリーダー選出が遅くなる問題を修正

-   TiFlash

    -   TiFlashストアサイズ統計の不正確さの問題を修正
    -   ライブラリ`nsl`がないため、一部のプラットフォームでTiFlashが起動に失敗する問題を修正しました。
    -   書き込み圧力が大きい場合、 `wait index`の無限待機をブロックします (デフォルトの 5 分のタイムアウトが追加されます)。これにより、 TiFlash がデータ複製を待機してサービスを提供するのに時間がかかりすぎるのを防ぎます。
    -   ログボリュームが大きい場合にログ検索が遅くなり、結果が表示されない問題を修正しました
    -   古い履歴ログを検索するときに最新のログしか検索できない問題を修正しました
    -   新しい照合順序が有効になっているときに間違った結果になる可能性を修正しました
    -   SQL 文に非常に長いネストされた式が含まれている場合に発生する可能性のある解析エラーを修正しました。
    -   Exchangeオペレータの`Block schema mismatch`エラーを修正
    -   Decimal型の比較時に発生する可能性のある`Can't compare`エラーを修正
    -   `left/substring`番目の関数の`3rd arguments of function substringUTF8 must be constants`エラーを修正する

-   ツール

    -   TiCDC

        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正しました[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[＃2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信したときに TiCDC プロセスがpanicになる可能性がある問題を修正しました。
        -   下流の TiDB/MySQL の可用性を検証する際の不要な CPU 消費を修正[＃3073](https://github.com/pingcap/tiflow/issues/3073)
        -   TiCDCによって生成されるKafkaメッセージの量が`max-message-size` [＃2962](https://github.com/pingcap/tiflow/issues/2962)に制限されない問題を修正
        -   Kafka メッセージの書き込み中にエラーが発生すると、TiCDC 同期タスクが一時停止する可能性がある問題を修正しました[＃2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`有効になっているときに、有効なインデックスのない一部のパーティションテーブルが無視される可能性がある問題を修正[＃2834](https://github.com/pingcap/tiflow/issues/2834)
        -   株価データのスキャンに時間がかかりすぎると、TiKV が GC を実行するため株価データのスキャンが失敗する可能性がある問題を修正しました[＃2470](https://github.com/pingcap/tiflow/issues/2470)
        -   一部のタイプの列を Open Protocol 形式[＃2758](https://github.com/pingcap/tiflow/issues/2758)にエンコードするときに発生する可能性のあるpanic問題を修正しました。
        -   一部のタイプの列をAvro形式[＃2648](https://github.com/pingcap/tiflow/issues/2648)にエンコードする際に発生する可能性のあるpanic問題を修正しました

    -   TiDBBinlog

        -   ほとんどのテーブルがフィルタリングされると、特定の負荷[＃1075](https://github.com/pingcap/tidb-binlog/pull/1075)でチェックポイントを更新できない問題を修正しました。
