---
title: Use Resource Control to Achieve Resource Isolation
summary: Learn how to use the resource control feature to control and schedule application resources.
---

# リソース制御を使用してリソースの分離を実現する {#use-resource-control-to-achieve-resource-isolation}

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

クラスター管理者は、リソース制御機能を使用して、リソース グループの作成、リソース グループのクォータの設定、およびそれらのグループへのユーザーのバインドを行うことができます。

TiDB リソース制御機能は、TiDBレイヤーのフロー制御機能と TiKVレイヤーの優先スケジューリング機能の 2 層のリソース管理機能を提供します。 2 つの機能は個別に有効にすることも、同時に有効にすることもできます。詳細は[リソース制御用パラメータ](#parameters-for-resource-control)を参照してください。これにより、TiDBレイヤーがリソース グループに設定されたクォータに基づいてユーザーの読み取りおよび書き込みリクエストのフローを制御できるようになり、TiKVレイヤーが読み取りおよび書き込みクォータにマップされた優先順位に基づいてリクエストをスケジュールできるようになります。これにより、アプリケーションのリソース分離を確保し、サービス品質 (QoS) 要件を満たすことができます。

-   TiDB フロー制御: TiDB フロー制御は[トークンバケットアルゴリズム](https://en.wikipedia.org/wiki/Token_bucket)を使用します。バケット内に十分なトークンがなく、リソース グループが`BURSTABLE`オプションを指定していない場合、リソース グループへのリクエストは、トークン バケットにトークンがバックフィルされるまで待機して、再試行します。タイムアウトにより再試行が失敗する場合があります。

-   TiKV スケジューリング: 必要に応じて絶対優先度[（ `PRIORITY` ）](/information-schema/information-schema-resource-groups.md#examples)を設定できます。 `PRIORITY`の設定に従って、さまざまなリソースがスケジュールされます。高`PRIORITY`のタスクが最初にスケジュールされます。絶対優先度を設定しない場合、TiKV は各リソース グループの値`RU_PER_SEC`を使用して、各リソース グループの読み取りおよび書き込みリクエストの優先度を決定します。優先順位に基づいて、storageレイヤーは優先キューを使用してリクエストをスケジュールし、処理します。

v7.4.0 以降、リソース制御機能はTiFlashリソースの制御をサポートします。その原理は、TiDB フロー制御および TiKV スケジューリングの原理と似ています。

<CustomContent platform="tidb">

-   TiFlashフロー制御: [TiFlashパイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)を使用すると、 TiFlash はさまざまなクエリの CPU 消費量をより正確に取得し、それを差し引くために[リクエストユニット (RU)](#what-is-request-unit-ru)に変換できます。トラフィック制御はトークン バケット アルゴリズムを使用して実装されます。
-   TiFlashスケジューリング: システム リソースが不十分な場合、 TiFlash は優先順位に基づいて複数のリソース グループ間でパイプライン タスクをスケジュールします。具体的なロジックは次のとおりです。まず、 TiFlash はリソース グループの`PRIORITY`評価し、次に CPU 使用率と`RU_PER_SEC`を考慮します。その結果、 `rg1`と`rg2`の`PRIORITY`同じですが、 `rg2`の`RU_PER_SEC`が`rg1`の 2 倍である場合、 `rg2`の CPU 使用率は`rg1`の 2 倍になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiFlashフロー制御: [TiFlashパイプライン実行モデル](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)を使用すると、 TiFlash はさまざまなクエリの CPU 消費量をより正確に取得し、それを差し引くために[リクエストユニット (RU)](#what-is-request-unit-ru)に変換できます。トラフィック制御はトークン バケット アルゴリズムを使用して実装されます。
-   TiFlashスケジューリング: システム リソースが不十分な場合、 TiFlash は優先順位に基づいて複数のリソース グループ間でパイプライン タスクをスケジュールします。具体的なロジックは次のとおりです。まず、 TiFlash はリソース グループの`PRIORITY`評価し、次に CPU 使用率と`RU_PER_SEC`を考慮します。その結果、 `rg1`と`rg2`の`PRIORITY`同じですが、 `rg2`の`RU_PER_SEC`が`rg1`の 2 倍である場合、 `rg2`の CPU 使用率は`rg1`の 2 倍になります。

</CustomContent>

## リソース制御のシナリオ {#scenarios-for-resource-control}

リソース制御機能の導入は、TiDB にとってマイルストーンです。分散データベース クラスターを複数の論理ユニットに分割できます。たとえ個々のユニットがリソースを過剰に使用しても、他のユニットが必要とするリソースがクラウドアウトされることはありません。

この機能を使用すると、次のことが可能になります。

-   異なるシステムからの複数の中小規模のアプリケーションを単一の TiDB クラスターに結合します。アプリケーションのワークロードが大きくなっても、他のアプリケーションの通常の動作には影響しません。システムのワークロードが低い場合は、設定されたクォータを超えている場合でも、ビジー状態のアプリケーションに必要なシステム リソースを割り当てることができ、リソースを最大限に活用することができます。
-   すべてのテスト環境を単一の TiDB クラスターに結合するか、より多くのリソースを消費するバッチ タスクを単一のリソース グループにグループ化するかを選択します。重要なアプリケーションが常に必要なリソースを確実に取得できるようにしながら、ハードウェアの使用率を向上させ、運用コストを削減できます。
-   システム内にワークロードが混在している場合、異なるワークロードを別々のリソース グループに入れることができます。リソース制御機能を使用すると、トランザクション アプリケーションの応答時間がデータ分析やバッチ アプリケーションの影響を受けないようにすることができます。
-   クラスターで予期しない SQL パフォーマンスの問題が発生した場合は、SQL バインディングとリソース グループを使用して、SQL ステートメントのリソース消費を一時的に制限できます。

さらに、リソース制御機能を合理的に使用することで、クラスタ数を削減し、運用保守の困難を軽減し、管理コストを節約できます。

## 制限事項 {#limitations}

リソース制御により、追加のスケジューリング オーバーヘッドが発生します。したがって、この機能を有効にすると、パフォーマンスがわずかに低下する可能性があります (5% 未満)。

## リクエストユニット(RU)とは {#what-is-request-unit-ru}

リクエスト ユニット (RU) は、システム リソースに対する TiDB の統合抽象化ユニットであり、現在、CPU、IOPS、および IO 帯域幅のメトリクスが含まれています。これは、データベースへの 1 回のリクエストによって消費されるリソースの量を示すために使用されます。要求によって消費される RU の数は、操作の種類、クエリまたは変更されるデータの量などのさまざまな要因によって異なります。現在、RU には次の表のリソースの消費統計が含まれています。

<table><thead><tr><th>リソースの種類</th><th>RUの消費量</th></tr></thead><tbody><tr><td rowspan="3">読む</td><td>2 つのstorage読み取りバッチは 1 RU を消費します</td></tr><tr><td>8 つのstorage読み取りリクエストは 1 RU を消費します</td></tr><tr><td>64 KiB の読み取り要求ペイロードは 1 RU を消費します</td></tr><tr><td rowspan="3">書く</td><td>1 つのstorage書き込みバッチはレプリカごとに 1 RU を消費します</td></tr><tr><td>1 つのstorage書き込みリクエストは 1 RU を消費します</td></tr><tr><td>1 KiB の書き込み要求ペイロードは 1 RU を消費します</td></tr><tr><td>SQL CPU</td><td> 3 ミリ秒で 1 RU を消費</td></tr></tbody></table>

現在、 TiFlashリソース制御では、クエリのパイプライン タスクの実行によって消費される CPU 時間である SQL CPU と読み取り要求ペイロードのみが考慮されます。

> **注記：**
>
> -   各書き込み操作は、最終的にすべてのレプリカに複製されます (デフォルトでは、TiKV には 3 つのレプリカがあります)。各レプリケーション操作は、異なる書き込み操作とみなされます。
> -   ユーザーによって実行されるクエリに加えて、自動統計収集などのバックグラウンド タスクによって RU が消費される場合があります。
> -   上の表には、ネットワークとstorageの消費量を除いて、TiDB セルフホスト クラスターの RU 計算に関係するリソースのみがリストされています。 TiDB サーバーレス RU については、 [TiDB サーバーレスの料金詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/)を参照してください。

## SQL ステートメントの RU 消費量を見積もる {#estimate-ru-consumption-of-sql-statements}

[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption)ステートメントを使用すると、SQL の実行中に消費された RU の量を取得できます。 RU の量はキャッシュの影響を受けることに注意してください (たとえば、 [コプロセッサキャッシュ](/coprocessor-cache.md) )。同じ SQL が複数回実行されると、各実行で消費される RU の量が異なる場合があります。 RU 値は各実行の正確な値を表すものではありませんが、推定の参考として使用できます。

## リソース制御用パラメータ {#parameters-for-resource-control}

リソース制御機能では、次のシステム変数またはパラメータが導入されます。

-   TiDB: [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)システム変数を使用して、リソース グループのフロー制御を有効にするかどうかを制御できます。

<CustomContent platform="tidb">

-   TiKV: [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)パラメーターを使用して、リソース グループに基づいたリクエストのスケジューリングを使用するかどうかを制御できます。
-   TiFlash: [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)システム変数と[`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)構成項目 (v7.4.0 で導入) を使用して、 TiFlashリソース制御を有効にするかどうかを制御できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiKV: TiDB セルフホストの場合、 `resource-control.enabled`パラメーターを使用して、リソース グループ クォータに基づいてリクエストのスケジューリングを使用するかどうかを制御できます。 TiDB Cloudの場合、 `resource-control.enabled`パラメーターの値はデフォルトで`true`であり、動的変更はサポートされていません。
-   TiFlash: TiDB セルフホストの場合、 `tidb_enable_resource_control`システム変数と`enable_resource_control`構成項目 (v7.4.0 で導入) を使用して、 TiFlashリソース制御を有効にするかどうかを制御できます。

</CustomContent>

TiDB v7.0.0 以降、 `tidb_enable_resource_control`と`resource-control.enabled`がデフォルトで有効になります。これら 2 つのパラメータを組み合わせた結果を次の表に示します。

| `resource-control.enabled`     | `tidb_enable_resource_control` = オン | `tidb_enable_resource_control` = オフ |
| :----------------------------- | :---------------------------------- | :---------------------------------- |
| `resource-control.enabled` = 真 | フロー制御とスケジューリング (推奨)                 | 無効な組み合わせです                          |
| `resource-control.enabled` = 偽 | フロー制御のみ (非推奨)                       | 機能は無効になっています。                       |

<CustomContent platform="tidb">

v7.4.0 以降、 TiFlash構成項目`enable_resource_control`はデフォルトで有効になっています。 `tidb_enable_resource_control`と連携してTiFlashリソース制御機能を制御します。 TiFlashリソース制御は、 `enable_resource_control`と`tidb_enable_resource_control`の両方が有効な場合にのみ、フロー制御と優先スケジューリングを実行します。さらに、 `enable_resource_control`が有効な場合、 TiFlash は[パイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)を使用します。

</CustomContent>

<CustomContent platform="tidb-cloud">

v7.4.0 以降、 TiFlash構成項目`enable_resource_control`はデフォルトで有効になっています。 `tidb_enable_resource_control`と連携してTiFlashリソース制御機能を制御します。 TiFlashリソース制御は、 `enable_resource_control`と`tidb_enable_resource_control`の両方が有効な場合にのみ、フロー制御と優先スケジューリングを実行します。さらに、 `enable_resource_control`が有効な場合、 TiFlash は[パイプライン実行モデル](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)を使用します。

</CustomContent>

リソース制御メカニズムとパラメータの詳細については、 [RFC: TiDB におけるグローバル リソース制御](https://github.com/pingcap/tidb/blob/release-7.5/docs/design/2022-11-25-global-resource-control.md)および[TiFlashリソース制御](https://github.com/pingcap/tiflash/blob/release-7.5/docs/design/2023-09-21-tiflash-resource-control.md)を参照してください。

## リソース制御の使用方法 {#how-to-use-resource-control}

このセクションでは、リソース制御機能を使用してリソース グループを管理し、各リソース グループのリソース割り当てを制御する方法について説明します。

### クラスター容量の見積もり {#estimate-cluster-capacity}

<CustomContent platform="tidb">

リソースを計画する前に、クラスターの全体的な容量を把握する必要があります。 TiDB は、クラスター容量を見積もるためのステートメント[`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md)を提供します。次のいずれかの方法を使用できます。

-   [実際のワークロードに基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
-   [ハードウェア導入に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

[リソースマネージャーページ](/dashboard/dashboard-resource-manager.md) TiDB ダッシュボードで確認できます。詳細については、 [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md#methods-for-estimating-capacity)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB セルフホストの場合、 [`CALIBRATE RESOURCE`](https://docs.pingcap.com/zh/tidb/stable/sql-statement-calibrate-resource)ステートメントを使用してクラスター容量を見積もることができます。

TiDB Cloudの場合、 [`CALIBRATE RESOURCE`](https://docs.pingcap.com/zh/tidb/stable/sql-statement-calibrate-resource)ステートメントは適用されません。

</CustomContent>

### リソースグループの管理 {#manage-resource-groups}

リソース グループを作成、変更、または削除するには、 `SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

[`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)を使用してクラスターのリソース グループを作成できます。

既存のリソース グループの場合、 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)を使用して、リソース グループの`RU_PER_SEC`オプション (1 秒あたりの RU バックフィルの速度) を変更できます。リソース グループへの変更はすぐに有効になります。

[`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)を使用してリソース グループを削除できます。

### リソースグループを作成する {#create-a-resource-group}

以下にリソースグループの作成例を示します。

1.  リソース グループを作成します`rg1` 。リソース制限は 1 秒あたり 500 RU であり、このリソース グループ内のアプリケーションがリソースを超過することが許可されます。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2.  リソース グループを作成します`rg2` 。 RU バックフィル レートは 600 RU/秒であり、このリソース グループ内のアプリケーションがリソースを超過することはありません。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3.  絶対優先度を`HIGH`に設定してリソース グループ`rg3`を作成します。絶対優先度は現在`LOW|MEDIUM|HIGH`をサポートしています。デフォルト値は`MEDIUM`です。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg3 RU_PER_SEC = 100 PRIORITY = HIGH;
    ```

### リソースグループをバインドする {#bind-resource-groups}

TiDB は、次の 3 つのレベルのリソース グループ設定をサポートしています。

-   ユーザーレベル。 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)ステートメントを使用して、ユーザーを特定のリソース グループにバインドします。ユーザーがリソース グループにバインドされると、ユーザーが作成したセッションは、対応するリソース グループに自動的にバインドされます。
-   セッションレベル。 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)を介して現在のセッションのリソース グループを設定します。
-   発言レベル。 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)オプティマイザー ヒントを使用して、現在のステートメントのリソース グループを設定します。

#### ユーザーをリソース グループにバインドする {#bind-users-to-a-resource-group}

次の例では、ユーザー`usr1`を作成し、そのユーザーをリソース グループ`rg1`にバインドします。 `rg1`は、 [リソースグループの作成](#create-a-resource-group)の例で作成されたリソース グループです。

```sql
CREATE USER 'usr1'@'%' IDENTIFIED BY '123' RESOURCE GROUP rg1;
```

次の例では、 `ALTER USER`を使用してユーザー`usr2`リソース グループ`rg2`にバインドします。 `rg2`は、 [リソースグループの作成](#create-a-resource-group)の例で作成されたリソース グループです。

```sql
ALTER USER usr2 RESOURCE GROUP rg2;
```

ユーザーをバインドすると、新しく作成されたセッションのリソース消費は、指定されたクォータ (リクエスト ユニット、RU) によって制御されます。システムのワークロードが比較的高く、空き容量がない場合は、リソース消費率`usr2`クォータを超えないように厳密に制御されます。 `BURSTABLE`が構成されている場合、 `usr1`は`rg1`によってバインドされているため、 `usr1`の消費率がクォータを超えることが許可されます。

リクエストが多すぎてリソース グループのリソースが不足する場合、クライアントのリクエストは待機します。待機時間が長すぎる場合、リクエストはエラーを報告します。

> **注記：**
>
> -   `CREATE USER`または`ALTER USER`を使用してユーザーをリソース グループにバインドすると、その効果はユーザーの既存のセッションではなく、ユーザーの新しいセッションに対してのみ有効になります。
> -   TiDB は、クラスターの初期化中に`default`リソース グループを自動的に作成します。このリソース グループのデフォルト値`RU_PER_SEC`は`UNLIMITED` ( `INT`タイプの最大値、つまり`2147483647`に相当) で、 `BURSTABLE`モードです。リソース グループにバインドされていないステートメントは、自動的にこのリソース グループにバインドされます。このリソース グループは削除をサポートしていませんが、RU の構成は変更できます。

リソース グループからユーザーのバインドを解除するには、次のようにユーザーを`default`グループに再度バインドするだけです。

```sql
ALTER USER 'usr3'@'%' RESOURCE GROUP `default`;
```

詳細については、 [`ALTER USER ... RESOURCE GROUP`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)を参照してください。

#### 現在のセッションをリソース グループにバインドする {#bind-the-current-session-to-a-resource-group}

セッションをリソース グループにバインドすることにより、対応するセッションのリソース使用量は、指定された使用量 (RU) によって制限されます。

次の例では、現在のセッションをリソース グループ`rg1`にバインドします。

```sql
SET RESOURCE GROUP rg1;
```

#### 現在のステートメントをリソース グループにバインドします {#bind-the-current-statement-to-a-resource-group}

SQL ステートメントに[`RESOURCE_GROUP(resource_group_name)`](/optimizer-hints.md#resource_groupresource_group_name)ヒントを追加すると、ステートメントがバインドされるリソース グループを指定できます。このヒントは、 `SELECT` 、 `INSERT` 、 `UPDATE` 、および`DELETE`ステートメントをサポートします。

次の例では、現在のステートメントをリソース グループ`rg1`にバインドします。

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

### 予想よりも多くのリソースを消費するクエリを管理する (暴走クエリ) {#manage-queries-that-consume-more-resources-than-expected-runaway-queries}

> **警告：**
>
> この機能は実験的です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

暴走クエリとは、予想よりも多くの時間またはリソースを消費するクエリです。以下では、**ランナウェイ クエリという用語は、**ランナウェイ クエリを管理する機能を説明するために使用されます。

-   v7.2.0 以降、リソース制御機能に暴走クエリの管理が導入されています。リソース グループの基準を設定して暴走クエリを特定し、リソースを使い果たしたり他のクエリに影響を与えたりすることを防ぐためのアクションを自動的に実行できます。 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)または[`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)に`QUERY_LIMIT`フィールドを含めることで、リソース グループの暴走クエリを管理できます。
-   v7.3.0 以降、リソース制御機能に暴走監視の手動管理が導入され、特定の SQL ステートメントまたはダイジェストの暴走クエリを迅速に特定できるようになりました。ステートメント[`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)を実行して、リソース グループ内の暴走クエリ ウォッチ リストを手動で管理できます。

#### <code>QUERY_LIMIT</code>パラメータ {#code-query-limit-code-parameters}

サポートされている条件設定:

-   `EXEC_ELAPSED` : クエリの実行時間がこの制限を超えると、クエリは暴走クエリとして識別されます。

サポートされている操作 ( `ACTION` ):

-   `DRYRUN` : アクションは実行されません。レコードは暴走クエリに追加されます。主に条件設定が妥当かどうかを観察するために使用されます。
-   `COOLDOWN` : クエリの実行優先度は最低レベルに下げられます。クエリは最も低い優先順位で実行を継続し、他の操作のリソースを占有しません。
-   `KILL` : 識別されたクエリは自動的に終了し、 `Query execution was interrupted, identified as runaway query`を報告します。

システム リソースを使い果たす同時実行の暴走クエリを回避するために、リソース制御機能には、暴走クエリを迅速に特定して隔離できる迅速な識別メカニズムが導入されています。この機能は`WATCH`句を通じて使用できます。クエリが暴走クエリとして識別されると、このメカニズムはクエリの一致する特徴 ( `WATCH`の後のパラメータによって定義される) を抽出します。次の期間 ( `DURATION`で定義) では、暴走クエリの一致機能がウォッチ リストに追加され、TiDB インスタンスはクエリをウォッチ リストと一致させます。一致するクエリは、条件によって識別されるのを待つのではなく、暴走クエリとして直接マークされ、対応するアクションに従って分離されます。 `KILL`操作によりクエリが終了し、エラーが報告されます`Quarantined and interrupted because of being in runaway watch list` 。

`WATCH`素早く識別するために一致させる方法は 3 つあります。

-   `EXACT` 、まったく同じ SQL テキストを持つ SQL ステートメントのみがすぐに識別されることを示します。
-   `SIMILAR`同じパターンを持つすべての SQL ステートメントがプラン ダイジェストによって照合され、リテラル値が無視されることを示します。
-   `PLAN`同じパターンを持つすべての SQL ステートメントがプラン ダイジェストによって照合されることを示します。

`WATCH`の`DURATION`オプションは、識別アイテムの継続時間を示します。デフォルトでは無限です。

監視アイテムが追加された後、 `QUERY_LIMIT`構成が変更または削除されるたびに、マッチング機能も`ACTION`変更または削除されません。 `QUERY WATCH REMOVE`使用して監視アイテムを削除できます。

`QUERY_LIMIT`のパラメータは次のとおりです。

| パラメータ          | 説明                                                                 | 注記                                                                                           |
| -------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| `EXEC_ELAPSED` | クエリの実行時間がこの値を超えると、暴走クエリとして識別されます。                                  | EXEC_ELAPSED = `60s` 、実行に 60 秒以上かかる場合、クエリが暴走クエリとして識別されることを意味します。                             |
| `ACTION`       | 暴走クエリが特定されたときに実行されるアクション                                           | オプションの値は`DRYRUN` 、 `COOLDOWN` 、および`KILL`です。                                                  |
| `WATCH`        | 特定された暴走クエリを迅速に照合します。一定期間内に同じまたは類似のクエリが再び発生すると、対応するアクションが即座に実行されます。 | オプション。たとえば、 `WATCH=SIMILAR DURATION '60s'` 、 `WATCH=EXACT DURATION '1m'` 、および`WATCH=PLAN`です。 |

#### 例 {#examples}

1.  1 秒あたり 500 RU のクォータを持つリソース グループ`rg1`を作成し、60 秒を超える暴走クエリとして定義し、暴走クエリの優先順位を下げます。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=COOLDOWN);
    ```

2.  `rg1`リソース グループを変更して暴走クエリを終了し、次の 10 分間に同じパターンのクエリを直ちに暴走クエリとしてマークします。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=SIMILAR DURATION='10m');
    ```

3.  `rg1`リソース グループを変更して、暴走クエリのチェックをキャンセルします。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=NULL;
    ```

#### <code>QUERY WATCH</code>パラメータ {#code-query-watch-code-parameters}

`QUERY WATCH`のあらすじについて詳しくは、 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)をご覧ください。

パラメータは次のとおりです。

-   `RESOURCE GROUP`はリソース グループを指定します。このステートメントによって追加された暴走クエリの一致機能は、リソース グループのウォッチ リストに追加されます。このパラメータは省略可能です。省略した場合は、 `default`リソースグループに適用されます。

-   `ACTION`の意味は`QUERY LIMIT`と同じです。このパラメータは省略可能です。省略した場合、識別後の対応するアクションはリソースグループの`QUERY LIMIT`で設定された`ACTION`を採用し、 `QUERY LIMIT`の設定とアクションは変わりません。リソース グループに`ACTION`構成されていない場合、エラーが報告されます。

-   `QueryWatchTextOption`パラメーターには`SQL DIGEST` 、 `PLAN DIGEST` 、および`SQL TEXT`の 3 つのオプションがあります。
    -   `SQL DIGEST`は`SIMILAR`と同じです。次のパラメータは、文字列、ユーザー定義変数、または文字列の結果を生成するその他の式を受け入れます。文字列の長さは 64 である必要があり、これは TiDB のダイジェスト定義と同じです。
    -   `PLAN DIGEST`は`PLAN`と同じです。次のパラメータはダイジェスト文字列です。
    -   `SQL TEXT`入力 SQL を生の文字列 ( `EXACT` ) として照合するか、次のパラメータに応じて解析して`SQL DIGEST` ( `SIMILAR` ) または`PLAN DIGEST` ( `PLAN` ) にコンパイルします。

-   デフォルトのリソース グループの暴走クエリ ウォッチ リストにマッチング機能を追加します (デフォルトのリソース グループに事前に`QUERY LIMIT`を設定する必要があります)。

    ```sql
    QUERY WATCH ADD ACTION KILL SQL TEXT EXACT TO 'select * from test.t2';
    ```

-   SQL を SQL ダイジェストに解析して、 `rg1`リソース グループの暴走クエリ ウォッチ リストに一致機能を追加します。 `ACTION`が指定されていない場合は、 `rg1`リソース グループに対してすでに構成されている`ACTION`オプションが使用されます。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

-   `PLAN DIGEST`を使用して、 `rg1`リソース グループの暴走クエリ ウォッチ リストに一致機能を追加します。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION KILL PLAN DIGEST 'd08bc323a934c39dc41948b0a073725be3398479b6fa4f6dd1db2a9b115f7f57';
    ```

-   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`をクエリして監視アイテム ID を取得し、監視アイテムを削除します。

    ```sql
    SELECT * from information_schema.runaway_watches ORDER BY id;
    ```

    ```sql
    *************************** 1. row ***************************
                    ID: 20003
    RESOURCE_GROUP_NAME: rg2
            START_TIME: 2023-07-28 13:06:08
            END_TIME: UNLIMITED
                WATCH: Similar
            WATCH_TEXT: 5b7fd445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
                SOURCE: 127.0.0.1:4000
                ACTION: Kill
    1 row in set (0.00 sec)
    ```

    ```sql
    QUERY WATCH REMOVE 20003;
    ```

#### 可観測性 {#observability}

暴走クエリに関する詳細情報は、次のシステム テーブルと`INFORMATION_SCHEMA`から取得できます。

-   `mysql.tidb_runaway_queries`テーブルには、過去 7 日間に特定されたすべての暴走クエリの履歴レコードが含まれています。行の 1 つを例として取り上げます。

    ```sql
    MySQL [(none)]> SELECT * FROM mysql.tidb_runaway_queries LIMIT 1\G;
    *************************** 1. row ***************************
    resource_group_name: rg1
                   time: 2023-06-16 17:40:22
             match_type: identify
                 action: kill
           original_sql: select * from sbtest.sbtest1
            plan_digest: 5b7d445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
            tidb_server: 127.0.0.1:4000
    ```

    前述の出力では、 `match_type`暴走クエリがどのように識別されるかを示します。値は次のいずれかになります。

    -   `identify`は暴走クエリの条件に一致することを意味します。
    -   `watch` 、監視リストのクイック識別ルールに一致することを意味します。

-   `information_schema.runaway_watches`テーブルには、暴走クエリの迅速な識別ルールのレコードが含まれています。詳細については、 [`RUNAWAY_WATCHES`](/information-schema/information-schema-runaway-watches.md)を参照してください。

### バックグラウンドタスクを管理する {#manage-background-tasks}

> **警告：**
>
> この機能は実験的です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://docs.pingcap.com/tidb/stable/support)を報告できます。

データのバックアップや自動統計収集などのバックグラウンド タスクは優先度は低いですが、多くのリソースを消費します。これらのタスクは通常、定期的または不定期にトリガーされます。実行中に大量のリソースが消費されるため、オンラインの優先度の高いタスクのパフォーマンスに影響します。

v7.4.0 以降、TiDB リソース制御機能はバックグラウンド タスクの管理をサポートします。タスクがバックグラウンド タスクとしてマークされている場合、TiKV は、他のフォアグラウンド タスクのパフォーマンスへの影響を避けるために、このタイプのタスクによって使用されるリソースを動的に制限します。 TiKV は、すべてのフォアグラウンド タスクによって消費される CPU および IO リソースをリアルタイムで監視し、インスタンスの合計リソース制限に基づいてバックグラウンド タスクによって使用できるリソースのしきい値を計算します。すべてのバックグラウンド タスクは、実行中にこのしきい値によって制限されます。

#### <code>BACKGROUND</code>パラメータ {#code-background-code-parameters}

`TASK_TYPES` : バックグラウンド タスクとして管理する必要があるタスク タイプを指定します。複数のタスク タイプを区切るには、カンマ ( `,` ) を使用します。

TiDB は、次のタイプのバックグラウンド タスクをサポートします。

<CustomContent platform="tidb">

-   `lightning` : [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してインポート タスクを実行します。 TiDB Lightningの物理インポート モードと論理インポート モードの両方がサポートされています。
-   `br` : [BR](/br/backup-and-restore-overview.md)を使用してバックアップおよび復元タスクを実行します。 PITR はサポートされていません。
-   `ddl` : Reorg DDL のバッチ データ ライトバック フェーズ中のリソース使用量を制御します。
-   `stats` : 手動で実行されるか、TiDB によって自動的にトリガーされる[統計を収集する](/statistics.md#collect-statistics)タスク。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `lightning` : [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)を使用してインポート タスクを実行します。 TiDB Lightningの物理インポート モードと論理インポート モードの両方がサポートされています。
-   `br` : [BR](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)を使用してバックアップおよび復元タスクを実行します。 PITR はサポートされていません。
-   `ddl` : Reorg DDL のバッチ データ ライトバック フェーズ中のリソース使用量を制御します。
-   `stats` : 手動で実行されるか、TiDB によって自動的にトリガーされる[統計を収集する](/statistics.md#collect-statistics)タスク。

</CustomContent>

デフォルトでは、バックグラウンド タスクとしてマークされているタスク タイプは空であり、バックグラウンド タスクの管理は無効になっています。このデフォルトの動作は、TiDB v7.4.0 より前のバージョンの動作と同じです。バックグラウンド タスクを管理するには、 `default`リソース グループのバックグラウンド タスクの種類を手動で変更する必要があります。

#### 例 {#examples}

1.  `rg1`リソース グループを作成し、 `br`と`stats`バックグラウンド タスクとして設定します。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BACKGROUND=(TASK_TYPES='br,stats');
    ```

2.  `rg1`リソース グループを変更して、 `br`と`ddl`をバックグラウンド タスクとして設定します。

    ```sql
    ALTER RESOURCE GROUP rg1 BACKGROUND=(TASK_TYPES='br,ddl');
    ```

3.  `rg1`リソース グループのバックグラウンド タスクをデフォルト値に戻します。この場合、バックグラウンド タスクの種類は`default`リソース グループの構成に従います。

    ```sql
    ALTER RESOURCE GROUP rg1 BACKGROUND=NULL;
    ```

4.  `rg1`リソース グループを変更して、バックグラウンド タスク タイプを空に設定します。この場合、このリソース グループのすべてのタスクはバックグラウンド タスクとして扱われません。

    ```sql
    ALTER RESOURCE GROUP rg1 BACKGROUND=(TASK_TYPES="");
    ```

## リソース制御を無効にする {#disable-resource-control}

<CustomContent platform="tidb">

1.  リソース制御機能を無効にするには、次のステートメントを実行します。

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2.  リソース グループの RU に基づくスケジューリングを無効にするには、TiKV パラメーターを[`resource-control.enabled`](/tikv-configuration-file.md#resource-control) ～ `false`に設定します。

3.  TiFlash設定項目[`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) ～ `false`を設定して、 TiFlashリソース制御を無効にします。

</CustomContent>

<CustomContent platform="tidb-cloud">

1.  リソース制御機能を無効にするには、次のステートメントを実行します。

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2.  TiDB セルフホストの場合、 `resource-control.enabled`パラメーターを使用して、リソース グループ クォータに基づいてリクエストのスケジューリングを使用するかどうかを制御できます。 TiDB Cloudの場合、 `resource-control.enabled`パラメーターの値はデフォルトで`true`であり、動的変更はサポートされていません。 TiDB 専用クラスターでこれを無効にする必要がある場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

3.  TiDB セルフホストの場合、 `enable_resource_control`構成項目を使用して、 TiFlashリソース制御を有効にするかどうかを制御できます。 TiDB Cloudの場合、 `enable_resource_control`パラメーターの値はデフォルトで`true`であり、動的変更はサポートされていません。 TiDB 専用クラスターでこれを無効にする必要がある場合は、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

## モニタリング指標とグラフ {#monitoring-metrics-and-charts}

<CustomContent platform="tidb">

TiDB はリソース制御に関する実行時情報を定期的に収集し、Grafana の**[TiDB]** &gt; **[リソース制御]**ダッシュボードにメトリクスの視覚的なグラフを提供します。メトリクスについては、 [TiDB の重要なモニタリング指標](/grafana-tidb-dashboard.md)の**「リソース制御」**セクションで詳しく説明されています。

TiKV は、さまざまなリソース グループからのリクエスト QPS も記録します。詳細については、 [TiKV モニタリング メトリクスの詳細](/grafana-tikv-dashboard.md#grpc)を参照してください。

TiDB ダッシュボードの現在の[`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md)のテーブルでリソース グループのデータを表示できます。詳細については、 [リソースマネージャーページ](/dashboard/dashboard-resource-manager.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションは、TiDB セルフホスト型にのみ適用されます。現在、 TiDB Cloud はリソース制御メトリクスを提供していません。

TiDB はリソース制御に関するランタイム情報を定期的に収集し、Grafana の**[TiDB]** &gt; **[リソース制御]**ダッシュボードにメトリクスの視覚的なグラフを提供します。

TiKV は、Grafana の**TiKV**ダッシュボードにさまざまなリソース グループからのリクエスト QPS も記録します。

</CustomContent>

## ツールの互換性 {#tool-compatibility}

リソース制御機能は、データのインポート、エクスポート、その他のレプリケーション ツールの通常の使用には影響しません。 BR、 TiDB Lightning、および TiCDC は現在、リソース制御に関連する DDL 操作の処理をサポートしていません。また、それらのリソース消費はリソース制御によって制限されません。

## FAQ {#faq}

1.  リソース グループを使用したくない場合は、リソース制御を無効にする必要がありますか?

    いいえ。リソース グループを指定しないユーザーは、無制限のリソースを持つ`default`リソース グループにバインドされます。すべてのユーザーが`default`リソースグループに所属している場合、リソースの割り当て方法はリソース制御が無効な場合と同じになります。

2.  データベース ユーザーを複数のリソース グループにバインドできますか?

    いいえ。データベース ユーザーは 1 つのリソース グループにのみバインドできます。ただし、セッションの実行中は、 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)を使用して、現在のセッションで使用されるリソース グループを設定できます。オプティマイザ ヒント[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)使用して、実行中のステートメントのリソース グループを設定することもできます。

3.  すべてのリソース グループのリソース割り当ての合計 ( `RU_PER_SEC` ) がシステム容量を超えるとどうなりますか?

    TiDB は、リソース グループの作成時に容量を検証しません。システムに十分な使用可能なリソースがある限り、TiDB は各リソース グループのリソース要件を満たすことができます。システム リソースが制限を超えると、TiDB は優先度の高いリソース グループからの要求を満たすことを優先します。同じ優先度のリクエストをすべて満たすことができない場合、TiDB はリソース割り当て ( `RU_PER_SEC` ) に従って比例的にリソースを割り当てます。

## こちらも参照 {#see-also}

-   [リソースグループの作成](/sql-statements/sql-statement-create-resource-group.md)
-   [リソースグループの変更](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソースグループを削除](/sql-statements/sql-statement-drop-resource-group.md)
-   [リソースグループ RFC](https://github.com/pingcap/tidb/blob/release-7.5/docs/design/2022-11-25-global-resource-control.md)
