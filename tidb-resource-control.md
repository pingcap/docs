---
title: Use Resource Control to Achieve Resource Isolation
summary: リソース制御機能を使用してアプリケーション リソースを制御およびスケジュールする方法を学習します。
---

# リソース制御を使用してリソースの分離を実現する {#use-resource-control-to-achieve-resource-isolation}

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

クラスター管理者は、リソース制御機能を使用して、リソース グループを作成したり、リソース グループのクォータを設定したり、ユーザーをそれらのグループにバインドしたりできます。

TiDB リソース制御機能は、TiDBレイヤーでのフロー制御機能と TiKVレイヤーでの優先度スケジューリング機能という 2 つのレイヤーのリソース管理機能を提供します。この 2 つの機能は、別々に有効にすることも、同時に有効にすることもできます。詳細については、 [リソース制御のパラメータ](#parameters-for-resource-control)を参照してください。これにより、TiDBレイヤーはリソース グループに設定されたクォータに基づいてユーザーの読み取りおよび書き込み要求のフローを制御し、TiKVレイヤーは読み取りおよび書き込みクォータにマップされた優先度に基づいて要求をスケジュールすることができます。これにより、アプリケーションのリソース分離を確保し、サービス品質 (QoS) 要件を満たすことができます。

-   TiDB フロー制御: TiDB フロー制御では[トークンバケットアルゴリズム](https://en.wikipedia.org/wiki/Token_bucket)を使用します。バケットに十分なトークンがなく、リソース グループで`BURSTABLE`オプションが指定されていない場合、リソース グループへの要求はトークン バケットがトークンをバックフィルするまで待機し、再試行します。再試行はタイムアウトにより失敗する可能性があります。

-   TiKV スケジューリング: 必要に応じて絶対優先度[（ `PRIORITY` ）](/information-schema/information-schema-resource-groups.md#examples)を設定できます。3 `PRIORITY`設定に応じて、さまざまなリソースがスケジュールされます。5 `PRIORITY`高いタスクが最初にスケジュールされます。絶対優先度を設定しない場合、TiKV は各リソース グループの`RU_PER_SEC`の値を使用して、各リソース グループの読み取りおよび書き込み要求の優先度を決定します。優先度に基づいて、storageレイヤーは優先度キューを使用して要求をスケジュールおよび処理します。

v7.4.0 以降、リソース制御機能はTiFlashリソースの制御をサポートします。その原理は、TiDB フロー制御や TiKV スケジューリングの原理に似ています。

<CustomContent platform="tidb">

-   TiFlashフロー制御: [TiFlashパイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)を使用すると、 TiFlash はさまざまなクエリの CPU 消費量をより正確に取得し、それを[リクエストユニット (RU)](#what-is-request-unit-ru)に変換して控除することができます。トラフィック制御は、トークン バケット アルゴリズムを使用して実装されます。
-   TiFlashスケジューリング: システム リソースが不足している場合、 TiFlash は、優先順位に基づいて複数のリソース グループ間でパイプライン タスクをスケジュールします。具体的なロジックは次のとおりです。まず、 TiFlash はリソース グループの`PRIORITY`を評価し、次に CPU 使用率と`RU_PER_SEC`を考慮します。結果として、 `rg1`と`rg2` `PRIORITY`は同じですが、 `rg2`の`RU_PER_SEC`が`rg1`の 2 倍である場合、 `rg2`の CPU 使用率は`rg1`の 2 倍になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiFlashフロー制御: [TiFlashパイプライン実行モデル](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)を使用すると、 TiFlash はさまざまなクエリの CPU 消費量をより正確に取得し、それを[リクエストユニット (RU)](#what-is-request-unit-ru)に変換して控除することができます。トラフィック制御は、トークン バケット アルゴリズムを使用して実装されます。
-   TiFlashスケジューリング: システム リソースが不足している場合、 TiFlash は、優先順位に基づいて複数のリソース グループ間でパイプライン タスクをスケジュールします。具体的なロジックは次のとおりです。まず、 TiFlash はリソース グループの`PRIORITY`を評価し、次に CPU 使用率と`RU_PER_SEC`を考慮します。結果として、 `rg1`と`rg2` `PRIORITY`は同じですが、 `rg2`の`RU_PER_SEC`が`rg1`の 2 倍である場合、 `rg2`の CPU 使用率は`rg1`の 2 倍になります。

</CustomContent>

## リソース制御のシナリオ {#scenarios-for-resource-control}

リソース制御機能の導入は、TiDB にとって画期的な出来事です。この機能により、分散データベース クラスターを複数の論理ユニットに分割できます。個々のユニットがリソースを過剰に使用しても、他のユニットに必要なリソースが圧迫されることはありません。

この機能を使用すると、次のことが可能になります。

-   異なるシステムの複数の中小規模のアプリケーションを 1 つの TiDB クラスターに統合します。アプリケーションのワークロードが大きくなっても、他のアプリケーションの正常な動作には影響しません。システムのワークロードが低い場合は、設定されたクォータを超えても、ビジー状態のアプリケーションに必要なシステム リソースを割り当てることができるため、リソースを最大限に活用できます。
-   すべてのテスト環境を単一の TiDB クラスターに結合するか、より多くのリソースを消費するバッチ タスクを単一のリソース グループにグループ化するかを選択します。これにより、重要なアプリケーションが常に必要なリソースを取得できるようにしながら、ハードウェアの使用率を向上させ、運用コストを削減できます。
-   システム内に混在するワークロードがある場合、異なるワークロードを別々のリソース グループに配置できます。リソース制御機能を使用すると、トランザクション アプリケーションの応答時間がデータ分析やバッチ アプリケーションの影響を受けないようにすることができます。
-   クラスターで予期しない SQL パフォーマンスの問題が発生した場合、SQL バインディングをリソース グループとともに使用して、SQL ステートメントのリソース消費を一時的に制限できます。

さらに、リソース制御機能を合理的に使用すると、クラスターの数を減らし、運用と保守の難易度を軽減し、管理コストを節約できます。

> **注記：**
>
> -   リソース管理の有効性を評価するには、独立したコンピューティング ノードとstorageノードにクラスターを展開することをお勧めします。 `tiup playground`によって作成された、インスタンス間でリソースが共有される展開では、スケジューリングやその他のクラスター リソースに依存する機能は、ほとんど正常に動作しません。

## 制限事項 {#limitations}

リソース制御により、追加のスケジューリング オーバーヘッドが発生します。そのため、この機能を有効にすると、パフォーマンスがわずかに低下する可能性があります (5% 未満)。

## リクエストユニット（RU）とは {#what-is-request-unit-ru}

リクエスト ユニット (RU) は、TiDB のシステム リソースの統合抽象化ユニットであり、現在 CPU、IOPS、および IO 帯域幅のメトリックが含まれています。これは、データベースへの単一のリクエストによって消費されるリソースの量を示すために使用されます。リクエストによって消費される RU の数は、操作の種類、クエリまたは変更されるデータの量など、さまざまな要因によって異なります。現在、RU には、次の表のリソースの消費統計が含まれています。

<table><thead><tr><th>リソースタイプ</th><th>RU消費量</th></tr></thead><tbody><tr><td rowspan="3">読む</td><td>2 つのstorage読み取りバッチは 1 RU を消費します</td></tr><tr><td>8 つのstorage読み取り要求は 1 RU を消費します</td></tr><tr><td>64 KiBの読み取り要求ペイロードは1RUを消費します</td></tr><tr><td rowspan="3">書く</td><td>1 回のstorage書き込みバッチで 1 RU が消費される</td></tr><tr><td>1 回のstorage書き込み要求で 1 RU が消費される</td></tr><tr><td>1 KiBの書き込み要求ペイロードは1 RUを消費します</td></tr><tr><td>CPU</td><td> 3 ミリ秒で 1 RU を消費</td></tr></tbody></table>

> **注記：**
>
> -   各書き込み操作は最終的にすべてのレプリカに複製されます (デフォルトでは、TiKV には 3 つのレプリカがあります)。各レプリケーション操作は、異なる書き込み操作と見なされます。
> -   上の表には、ネットワークとstorageの消費を除いて、TiDB セルフホスト クラスターの RU 計算に関係するリソースのみがリストされています。TiDB サーバーレス RU については、 [TiDB サーバーレスの価格詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/)参照してください。
> -   現在、 TiFlashリソース制御では、クエリのパイプライン タスクの実行によって消費される CPU 時間である SQL CPU と、読み取り要求ペイロードのみが考慮されます。

## リソース制御のパラメータ {#parameters-for-resource-control}

リソース制御機能では、次のシステム変数またはパラメータが導入されています。

-   TiDB: [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)システム変数を使用して、リソース グループのフロー制御を有効にするかどうかを制御できます。

<CustomContent platform="tidb">

-   TiKV: [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)パラメータを使用して、リソース グループに基づいて要求のスケジュールを使用するかどうかを制御できます。
-   TiFlash: [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)システム変数と[`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)構成項目 (v7.4.0 で導入) を使用して、 TiFlashリソース制御を有効にするかどうかを制御できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiKV: TiDB Self-Hosted の場合、 `resource-control.enabled`パラメータを使用して、リソース グループのクォータに基づいて要求のスケジュールを使用するかどうかを制御できます。TiDB TiDB Cloudの場合、 `resource-control.enabled`パラメータの値はデフォルトで`true`であり、動的な変更はサポートされていません。
-   TiFlash: TiDB Self-Hosted の場合、 `tidb_enable_resource_control`システム変数と`enable_resource_control`構成項目 (v7.4.0 で導入) を使用して、 TiFlashリソース制御を有効にするかどうかを制御できます。

</CustomContent>

TiDB v7.0.0 以降では、 `tidb_enable_resource_control`と`resource-control.enabled`デフォルトで有効になっています。これら 2 つのパラメータの組み合わせの結果は次の表に示されています。

| `resource-control.enabled`     | `tidb_enable_resource_control` = オン | `tidb_enable_resource_control` = オフ |
| :----------------------------- | :---------------------------------- | :---------------------------------- |
| `resource-control.enabled` = 真 | フロー制御とスケジューリング（推奨）                  | 無効な組み合わせ                            |
| `resource-control.enabled` = 偽 | フロー制御のみ（非推奨）                        | この機能は無効になっています。                     |

<CustomContent platform="tidb">

v7.4.0 以降、 TiFlash構成項目`enable_resource_control`はデフォルトで有効になっています。これは`tidb_enable_resource_control`と連携してTiFlashリソース制御機能を制御します。TiFlash リソース制御は、 `enable_resource_control`と`tidb_enable_resource_control`両方が有効な場合にのみ、フロー制御と優先度スケジューリングを実行します。また、 `enable_resource_control`が有効な場合、 TiFlash は[パイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)使用します。

</CustomContent>

<CustomContent platform="tidb-cloud">

v7.4.0 以降、 TiFlash構成項目`enable_resource_control`はデフォルトで有効になっています。これは`tidb_enable_resource_control`と連携してTiFlashリソース制御機能を制御します。TiFlash リソース制御は、 `enable_resource_control`と`tidb_enable_resource_control`両方が有効な場合にのみ、フロー制御と優先度スケジューリングを実行します。また、 `enable_resource_control`が有効な場合、 TiFlash は[パイプライン実行モデル](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)使用します。

</CustomContent>

リソース制御メカニズムとパラメータの詳細については、 [RFC: TiDB におけるグローバル リソース制御](https://github.com/pingcap/tidb/blob/release-8.1/docs/design/2022-11-25-global-resource-control.md)および[TiFlashリソース制御](https://github.com/pingcap/tiflash/blob/release-8.1/docs/design/2023-09-21-tiflash-resource-control.md)を参照してください。

## リソース制御の使用方法 {#how-to-use-resource-control}

このセクションでは、リソース制御機能を使用してリソース グループを管理し、各リソース グループのリソース割り当てを制御する方法について説明します。

### クラスター容量の見積もり {#estimate-cluster-capacity}

<CustomContent platform="tidb">

リソース計画を立てる前に、クラスターの全体的な容量を把握しておく必要があります。TiDB は、クラスターの容量を見積もるためのステートメント[`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md)を提供します。次のいずれかの方法を使用できます。

-   [実際の作業負荷に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
-   [ハードウェアの展開に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

[リソース マネージャー ページ](/dashboard/dashboard-resource-manager.md) TiDB ダッシュボードで確認できます。詳細については[`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md#methods-for-estimating-capacity)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB セルフホストの場合、 [`CALIBRATE RESOURCE`](https://docs.pingcap.com/zh/tidb/stable/sql-statement-calibrate-resource)ステートメントを使用してクラスターの容量を見積もることができます。

TiDB Cloudの場合、 [`CALIBRATE RESOURCE`](https://docs.pingcap.com/zh/tidb/stable/sql-statement-calibrate-resource)ステートメントは適用されません。

</CustomContent>

### リソース グループを管理する {#manage-resource-groups}

リソース グループを作成、変更、または削除するには、権限`SUPER`または`RESOURCE_GROUP_ADMIN`必要です。

[`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)を使用してクラスターのリソース グループを作成できます。

既存のリソース グループの場合、 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)を使用して、リソース グループの`RU_PER_SEC`オプション (1 秒あたりの RU バックフィルの速度) を変更できます。リソース グループへの変更はすぐに有効になります。

[`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)を使用してリソース グループを削除できます。

### リソースグループを作成する {#create-a-resource-group}

以下は、リソース グループを作成する方法の例です。

1.  リソース グループ`rg1`を作成します。リソース制限は 1 秒あたり 500 RU であり、このリソース グループ内のアプリケーションはリソースをオーバーランできます。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2.  リソース グループ`rg2`を作成します。RU バックフィル レートは 1 秒あたり 600 RU であり、このリソース グループ内のアプリケーションがリソースをオーバーランすることは許可されません。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3.  絶対優先度を`HIGH`に設定したリソース グループ`rg3`を作成します。現在、絶対優先度は`LOW|MEDIUM|HIGH`サポートしています。デフォルト値は`MEDIUM`です。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg3 RU_PER_SEC = 100 PRIORITY = HIGH;
    ```

### リソースグループをバインドする {#bind-resource-groups}

TiDB は、次の 3 つのレベルのリソース グループ設定をサポートしています。

-   ユーザー レベル。1 または[`CREATE USER`](/sql-statements/sql-statement-create-user.md) [`ALTER USER`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)ステートメントを使用して、ユーザーを特定のリソース グループにバインドします。ユーザーがリソース グループにバインドされると、ユーザーによって作成されたセッションは、対応するリソース グループに自動的にバインドされます。
-   セッション レベル。 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)を介して現在のセッションのリソース グループを設定します。
-   ステートメント レベル。1 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)オプティマイザー ヒントを使用して、現在のステートメントのリソース グループを設定します。

#### ユーザーをリソースグループにバインドする {#bind-users-to-a-resource-group}

次の例では、ユーザー`usr1`を作成し、そのユーザーをリソース グループ`rg1`にバインドします。5 `rg1` 、 [リソース グループの作成](#create-a-resource-group)の例で作成されたリソース グループです。

```sql
CREATE USER 'usr1'@'%' IDENTIFIED BY '123' RESOURCE GROUP rg1;
```

次の例では、 `ALTER USER`使用してユーザー`usr2`をリソース グループ`rg2`にバインドします。 `rg2`は、 [リソース グループの作成](#create-a-resource-group)の例で作成されたリソース グループです。

```sql
ALTER USER usr2 RESOURCE GROUP rg2;
```

ユーザーをバインドすると、新しく作成されたセッションのリソース消費は、指定されたクォータ (リクエスト ユニット、RU) によって制御されます。システムのワークロードが比較的高く、余裕がない場合、 `usr2`のリソース消費率はクォータを超えないように厳密に制御されます。7 `BURSTABLE`構成されている場合、 `usr1` `rg1`によってバインドされるため、 `usr1`の消費率はクォータを超えることが許可されます。

リクエストが多すぎてリソース グループのリソースが不足する場合、クライアントのリクエストは待機します。待機時間が長すぎる場合、リクエストはエラーを報告します。

> **注記：**
>
> -   `CREATE USER`または`ALTER USER`を使用してユーザーをリソース グループにバインドすると、そのバインドはユーザーの既存のセッションには適用されず、ユーザーの新しいセッションにのみ適用されます。
> -   TiDB は、クラスターの初期化中に`default`リソース グループを自動的に作成します。このリソース グループの場合、デフォルト値は`RU_PER_SEC`で、 `UNLIMITED` ( `INT`タイプの最大値である`2147483647`に相当) であり、 `BURSTABLE`モードです。リソース グループにバインドされていないステートメントは、このリソース グループに自動的にバインドされます。このリソース グループは削除をサポートしていませんが、RU の構成を変更することはできます。

リソース グループからユーザーをバインド解除するには、次のようにしてユーザーを`default`グループに再度バインドするだけです。

```sql
ALTER USER 'usr3'@'%' RESOURCE GROUP `default`;
```

詳細については[`ALTER USER ... RESOURCE GROUP`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)参照してください。

#### 現在のセッションをリソース グループにバインドする {#bind-the-current-session-to-a-resource-group}

セッションをリソース グループにバインドすると、対応するセッションのリソース使用量は指定された使用量 (RU) によって制限されます。

次の例では、現在のセッションをリソース グループ`rg1`にバインドします。

```sql
SET RESOURCE GROUP rg1;
```

#### 現在のステートメントをリソース グループにバインドする {#bind-the-current-statement-to-a-resource-group}

SQL ステートメントに[`RESOURCE_GROUP(resource_group_name)`](/optimizer-hints.md#resource_groupresource_group_name)ヒントを追加することで、ステートメントがバインドされるリソース グループを指定できます。このヒントは、 `SELECT` 、 `INSERT` 、 `UPDATE` 、および`DELETE`ステートメントをサポートします。

次の例では、現在のステートメントをリソース グループ`rg1`にバインドします。

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

### 予想以上に多くのリソースを消費するクエリを管理する (ランナウェイクエリ) {#manage-queries-that-consume-more-resources-than-expected-runaway-queries}

ランナウェイ クエリとは、予想よりも多くの時間やリソースを消費するクエリ ( `SELECT`ステートメントのみ) です。ランナ**ウェイ クエリ**という用語は、以下ではランナウェイ クエリを管理する機能を説明するために使用されます。

-   v7.2.0 以降、リソース制御機能にランナウェイ クエリの管理が導入されました。リソース グループの条件を設定してランナウェイ クエリを識別し、リソースを使い果たしたり他のクエリに影響を与えたりしないように自動的にアクションを実行できます。 [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)または[`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)に`QUERY_LIMIT`フィールドを含めることで、リソース グループのランナウェイ クエリを管理できます。
-   v7.3.0 以降、リソース制御機能では、ランナウェイ ウォッチの手動管理が導入され、特定の SQL ステートメントまたはダイジェストのランナウェイ クエリをすばやく識別できるようになりました。ステートメント[`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)を実行して、リソース グループ内のランナウェイ クエリ ウォッチ リストを手動で管理できます。

#### <code>QUERY_LIMIT</code>パラメータ {#code-query-limit-code-parameters}

サポートされている条件設定:

-   `EXEC_ELAPSED` : クエリの実行時間がこの制限を超えると、クエリはランナウェイ クエリとして識別されます。

サポートされている操作（ `ACTION` ）：

-   `DRYRUN` : アクションは実行されません。ランナウェイ クエリのレコードが追加されます。これは主に、条件設定が妥当かどうかを観察するために使用されます。
-   `COOLDOWN` : クエリの実行優先度が最低レベルに下げられます。クエリは最低優先度で実行を継続し、他の操作のリソースを占有しません。
-   `KILL` : 識別されたクエリは自動的に終了し、エラー`Query execution was interrupted, identified as runaway query`を報告します。

システム リソースを使い果たす大量の同時実行クエリを回避するために、リソース制御機能では、ランナウェイ クエリをすばやく識別して分離できるクイック識別メカニズムが導入されています。 `WATCH`句を通じてこの機能を使用できます。クエリがランナウェイ クエリとして識別されると、このメカニズムはクエリの一致する特徴 ( `WATCH`後のパラメータで定義) を抽出します。次の期間 ( `DURATION`で定義) に、ランナウェイ クエリの一致する特徴が監視リストに追加され、TiDB インスタンスはクエリを監視リストと照合します。一致するクエリは、条件によって識別されるのを待つのではなく、直接ランナウェイ クエリとしてマークされ、対応するアクションに従って分離されます。 `KILL`操作はクエリを終了し、エラー`Quarantined and interrupted because of being in runaway watch list`を報告します。

`WATCH`すばやく識別するために一致させる方法は 3 つあります。

-   `EXACT` 、まったく同じ SQL テキストを持つ SQL ステートメントのみが迅速に識別されることを示します。
-   `SIMILAR` 、同じパターンを持つすべての SQL ステートメントがプラン ダイジェストに一致し、リテラル値が無視されることを示します。
-   `PLAN` 、同じパターンを持つすべての SQL ステートメントがプラン ダイジェストに一致することを示します。

`WATCH`の`DURATION`オプションは識別項目の有効期間を示し、デフォルトでは無期限です。

監視項目が追加された後は、 `QUERY_LIMIT`構成が変更または削除されても、一致する機能も`ACTION`変更または削除されません。監視項目を削除するには、 `QUERY WATCH REMOVE`使用できます。

`QUERY_LIMIT`のパラメータは次のとおりです。

| パラメータ          | 説明                                                                      | 注記                                                                                           |
| -------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `EXEC_ELAPSED` | クエリ実行時間がこの値を超えると、ランナウェイクエリとして識別されます。                                    | EXEC_ELAPSED = `60s` 、実行に 60 秒以上かかる場合にクエリがランナウェイ クエリとして識別されることを意味します。                        |
| `ACTION`       | 暴走クエリが特定された場合のアクション                                                     | オプションの値は`DRYRUN` 、 `COOLDOWN` 、 `KILL`です。                                                    |
| `WATCH`        | 特定されたランナウェイクエリを迅速に照合します。一定期間内に同じまたは類似のクエリが再度発生した場合、対応するアクションが直ちに実行されます。 | オプション。たとえば、 `WATCH=SIMILAR DURATION '60s'` 、 `WATCH=EXACT DURATION '1m'` 、 `WATCH=PLAN`などです。 |

#### 例 {#examples}

1.  1 秒あたり 500 RU のクォータを持つリソース グループ`rg1`を作成し、60 秒を超えるクエリをランナウェイ クエリとして定義し、ランナウェイ クエリの優先度を下げます。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=COOLDOWN);
    ```

2.  `rg1`リソース グループを変更してランナウェイ クエリを終了し、次の 10 分以内に同じパターンのクエリをランナウェイ クエリとしてすぐにマークします。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=SIMILAR DURATION='10m');
    ```

3.  ランナウェイ クエリ チェックをキャンセルするには、 `rg1`リソース グループを変更します。

    ```sql
    ALTER RESOURCE GROUP rg1 QUERY_LIMIT=NULL;
    ```

#### <code>QUERY WATCH</code>パラメータ {#code-query-watch-code-parameters}

`QUERY WATCH`のあらすじについては[`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)を参照してください。

パラメータは次のとおりです。

-   `RESOURCE GROUP`リソース グループを指定します。このステートメントによって追加されたランナウェイ クエリの一致する機能は、リソース グループの監視リストに追加されます。このパラメータは省略できます。省略した場合は、 `default`リソース グループに適用されます。

-   `ACTION`の意味は`QUERY LIMIT`と同じです。このパラメータは省略できます。省略した場合、識別後の対応するアクションはリソースグループ内の`QUERY LIMIT`で設定された`ACTION`を採用し、アクションは`QUERY LIMIT`設定によって変更されません。リソースグループ内に`ACTION`設定されていない場合は、エラーが報告されます。

-   `QueryWatchTextOption`パラメータには、 `SQL DIGEST` 、 `PLAN DIGEST` 、 `SQL TEXT` 3 つのオプションがあります。
    -   `SQL DIGEST`は`SIMILAR`と同じです。次のパラメータは、文字列、ユーザー定義変数、または文字列の結果を生成するその他の式を受け入れます。文字列の長さは 64 でなければなりません。これは、TiDB のダイジェスト定義と同じです。
    -   `PLAN DIGEST`は`PLAN`と同じです。次のパラメータはダイジェスト文字列です。
    -   `SQL TEXT`入力SQLを生の文字列（ `EXACT` ）として一致させるか、次のパラメータに応じてそれを解析して`SQL DIGEST` （ `SIMILAR` ）または`PLAN DIGEST` （ `PLAN` ）にコンパイルします。

-   デフォルトのリソース グループのランナウェイ クエリ監視リストに一致する機能を追加します (事前にデフォルトのリソース グループに`QUERY LIMIT`設定する必要があります)。

    ```sql
    QUERY WATCH ADD ACTION KILL SQL TEXT EXACT TO 'select * from test.t2';
    ```

-   SQL を SQL ダイジェストに解析して、 `rg1`リソース グループのランナウェイ クエリ監視リストに一致する機能を追加します。3 `ACTION`指定されていない場合は、 `rg1`リソース グループに既に構成されている`ACTION`オプションが使用されます。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT SIMILAR TO 'select * from test.t2';
    ```

-   `PLAN DIGEST`を使用して、 `rg1`リソース グループのランナウェイ クエリ監視リストに一致する機能を追加します。

    ```sql
    QUERY WATCH ADD RESOURCE GROUP rg1 ACTION KILL PLAN DIGEST 'd08bc323a934c39dc41948b0a073725be3398479b6fa4f6dd1db2a9b115f7f57';
    ```

-   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`をクエリしてウォッチ アイテム ID を取得し、ウォッチ アイテムを削除します。

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

ランナウェイ クエリに関する詳細情報は、次のシステム テーブルと`INFORMATION_SCHEMA`から取得できます。

-   `mysql.tidb_runaway_queries`テーブルには、過去 7 日間に特定されたすべてのランナウェイ クエリの履歴レコードが含まれています。例として、行の 1 つを見てみましょう。

    ```sql
    MySQL [(none)]> SELECT * FROM mysql.tidb_runaway_queries LIMIT 1\G
    *************************** 1. row ***************************
    resource_group_name: rg1
                   time: 2023-06-16 17:40:22
             match_type: identify
                 action: kill
           original_sql: select * from sbtest.sbtest1
            plan_digest: 5b7d445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
            tidb_server: 127.0.0.1:4000
    ```

    上記の出力では、 `match_type`ランナウェイ クエリの識別方法を示しています。値は次のいずれかになります。

    -   `identify`ランナウェイクエリの条件に一致することを意味します。
    -   `watch` 、ウォッチ リスト内のクイック識別ルールに一致することを意味します。

-   `information_schema.runaway_watches`テーブルには、ランナウェイ クエリのクイック識別ルールのレコードが含まれています。詳細については、 [`RUNAWAY_WATCHES`](/information-schema/information-schema-runaway-watches.md)を参照してください。

### バックグラウンドタスクを管理する {#manage-background-tasks}

> **警告：**
>
> この機能は実験的ものです。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://docs.pingcap.com/tidb/stable/support)報告できます。
>
> リソース制御におけるバックグラウンド タスク管理は、CPU/IO 使用率に対する TiKV のリソース クォータの動的調整に基づいています。そのため、各インスタンスの使用可能なリソース クォータに依存します。複数のコンポーネントまたはインスタンスが単一のサーバーに展開されている場合は、 `cgroup`を通じてTiUPインスタンスに適切なリソース クォータを設定する必要があります。TiUP Playground のような共有リソースでの展開では、期待される効果を達成することは困難です。

データのバックアップや自動統計収集などのバックグラウンド タスクは、優先度は低いですが、多くのリソースを消費します。これらのタスクは通常、定期的または不定期にトリガーされます。実行中は多くのリソースを消費するため、オンラインの高優先度タスクのパフォーマンスに影響します。

v7.4.0 以降、TiDB リソース制御機能はバックグラウンド タスクの管理をサポートします。タスクがバックグラウンド タスクとしてマークされると、TiKV は、このタイプのタスクで使用されるリソースを動的に制限し、他のフォアグラウンド タスクのパフォーマンスへの影響を回避します。TiKV は、すべてのフォアグラウンド タスクによって消費される CPU および IO リソースをリアルタイムで監視し、インスタンスの合計リソース制限に基づいて、バックグラウンド タスクで使用できるリソースしきい値を計算します。すべてのバックグラウンド タスクは、実行中にこのしきい値によって制限されます。

#### <code>BACKGROUND</code>パラメータ {#code-background-code-parameters}

`TASK_TYPES` : バックグラウンドタスクとして管理する必要があるタスクタイプを指定します。複数のタスクタイプを区切るには、コンマ ( `,` ) を使用します。

TiDB は次の種類のバックグラウンド タスクをサポートします。

<CustomContent platform="tidb">

-   `lightning` : [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してインポート タスクを実行します。TiDB TiDB Lightningの物理インポート モードと論理インポート モードの両方がサポートされています。
-   `br` : [BR](/br/backup-and-restore-overview.md)を使用してバックアップおよび復元タスクを実行します。PITR はサポートされていません。
-   `ddl` : 再編成 DDL のバッチ データ書き戻しフェーズ中のリソース使用量を制御します。
-   `stats` : 手動で実行されるか、TiDB によって自動的にトリガーされる[統計を収集する](/statistics.md#collect-statistics)タスク。
-   `background` : 予約済みのタスク タイプ。 [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740)システム変数を使用して、現在のセッションのタスク タイプを`background`として指定できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `lightning` : [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)を使用してインポート タスクを実行します。TiDB TiDB Lightningの物理インポート モードと論理インポート モードの両方がサポートされています。
-   `br` : [BR](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)を使用してバックアップおよび復元タスクを実行します。PITR はサポートされていません。
-   `ddl` : 再編成 DDL のバッチ データ書き戻しフェーズ中のリソース使用量を制御します。
-   `stats` : 手動で実行されるか、TiDB によって自動的にトリガーされる[統計を収集する](/statistics.md#collect-statistics)タスク。
-   `background` : 予約済みのタスク タイプ。 [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740)システム変数を使用して、現在のセッションのタスク タイプを`background`として指定できます。

</CustomContent>

デフォルトでは、バックグラウンド タスクとしてマークされているタスク タイプは`""`で、バックグラウンド タスクの管理は無効になっています。バックグラウンド タスクの管理を有効にするには、 `default`リソース グループのバックグラウンド タスク タイプを手動で変更する必要があります。バックグラウンド タスクが識別され、一致すると、リソース制御が自動的に実行されます。つまり、システム リソースが不足している場合、バックグラウンド タスクは自動的に最低の優先度に下げられ、フォアグラウンド タスクの実行が保証されます。

> **注記：**
>
> 現在、すべてのリソース グループのバックグラウンド タスクは、 `default`リソース グループにバインドされています。 `default`を通じてバックグラウンド タスクの種類をグローバルに管理できます。 バックグラウンド タスクを他のリソース グループにバインドすることは、現在サポートされていません。

#### 例 {#examples}

1.  `default`リソース グループを変更し、 `br`と`ddl`バックグラウンド タスクとしてマークします。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES='br,ddl');
    ```

2.  `default`リソース グループを変更して、バックグラウンド タスクの種類を既定値に戻します。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=NULL;
    ```

3.  `default`リソース グループを変更して、バックグラウンド タスクの種類を空に設定します。この場合、このリソース グループのすべてのタスクはバックグラウンド タスクとして扱われません。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="");
    ```

4.  `default`リソース グループのバックグラウンド タスクの種類をビュー。

    ```sql
    SELECT * FROM information_schema.resource_groups WHERE NAME="default";
    ```

    出力は次のようになります。

        +---------+------------+----------+-----------+-------------+---------------------+
        | NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND          |
        +---------+------------+----------+-----------+-------------+---------------------+
        | default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl' |
        +---------+------------+----------+-----------+-------------+---------------------+

5.  現在のセッションのタスクをバックグラウンド タイプとして明示的にマークするには、 `tidb_request_source_type`使用してタスク タイプを明示的に指定します。次に例を示します。

    ```sql
    SET @@tidb_request_source_type="background";
    /* Add background task type */
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="background");
    /* Execute LOAD DATA in the current session */
    LOAD DATA INFILE "s3://resource-control/Lightning/test.customer.aaaa.csv"
    ```

## リソース制御を無効にする {#disable-resource-control}

<CustomContent platform="tidb">

1.  リソース制御機能を無効にするには、次のステートメントを実行します。

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2.  リソース グループの RU に基づくスケジュールを無効にするには、TiKV パラメータを[`resource-control.enabled`](/tikv-configuration-file.md#resource-control)から`false`設定します。

3.  TiFlashリソース制御を無効にするには、 TiFlash構成項目[`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を`false`に設定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

1.  リソース制御機能を無効にするには、次のステートメントを実行します。

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2.  TiDB Self-Hosted の場合、 `resource-control.enabled`パラメータを使用して、リソース グループのクォータに基づいて要求のスケジュールを使用するかどうかを制御できます。 TiDB Cloudの場合、 `resource-control.enabled`パラメータの値はデフォルトで`true`であり、動的な変更はサポートされていません。 TiDB Dedicated クラスターでこれを無効にする必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

3.  TiDB Self-Hosted の場合、 `enable_resource_control`構成項目を使用して、 TiFlashリソース制御を有効にするかどうかを制御できます。 TiDB Cloudの場合、 `enable_resource_control`パラメータの値はデフォルトで`true`であり、動的な変更はサポートされていません。 TiDB Dedicated クラスターで無効にする必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

## RU消費量をビュー {#view-ru-consumption}

RU 消費量に関する情報を表示できます。

### SQLによるRU消費量をビュー {#view-the-ru-consumption-by-sql}

SQL ステートメントの RU 消費量は、次の方法で確認できます。

-   システム変数`tidb_last_query_info`
-   `EXPLAIN ANALYZE`
-   遅いクエリとそれに対応するシステムテーブル
-   `statements_summary`

#### システム変数<code>tidb_last_query_info</code>をクエリして、最後の SQL 実行で消費された RUをビュー。 {#view-the-rus-consumed-by-the-last-sql-execution-by-querying-the-system-variable-code-tidb-last-query-info-code}

TiDB はシステム変数[`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014)を提供します。このシステム変数は、SQL 実行によって消費された RU を含む、最後に実行された DML ステートメントの情報を記録します。

例：

1.  `UPDATE`番目のステートメントを実行します。

    ```sql
    UPDATE sbtest.sbtest1 SET k = k + 1 WHERE id = 1;
    ```

        Query OK, 1 row affected (0.01 sec)
        Rows matched: 1  Changed: 1  Warnings: 0

2.  最後に実行されたステートメントの情報を表示するには、システム変数`tidb_last_query_info`をクエリします。

    ```sql
    SELECT @@tidb_last_query_info;
    ```

        +------------------------------------------------------------------------------------------------------------------------+
        | @@tidb_last_query_info                                                                                                 |
        +------------------------------------------------------------------------------------------------------------------------+
        | {"txn_scope":"global","start_ts":446809472210829315,"for_update_ts":446809472210829315,"ru_consumption":4.34885578125} |
        +------------------------------------------------------------------------------------------------------------------------+
        1 row in set (0.01 sec)

    結果では、 `ru_consumption`この SQL ステートメントの実行によって消費された RU です。

#### <code>EXPLAIN ANALYZE</code>による SQL 実行中に消費された RUをビュー {#view-rus-consumed-during-sql-execution-by-code-explain-analyze-code}

[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption)ステートメントを使用すると、SQL 実行中に消費された RU の量を取得できます。RU の量はキャッシュの影響を受けることに注意してください (例: [コプロセッサキャッシュ](/coprocessor-cache.md) )。同じ SQL が複数回実行されると、各実行で消費される RU の量は異なる場合があります。RU 値は各実行の正確な値を表すものではありませんが、推定の参照として使用できます。

#### 遅いクエリとそれに対応するシステムテーブル {#slow-queries-and-the-corresponding-system-table}

<CustomContent platform="tidb">

リソース制御を有効にすると、TiDB の[スロークエリログ](/identify-slow-queries.md)と対応するシステム テーブル[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)に、リソース グループ、対応する SQL の RU 消費量、および使用可能な RU を待機するのに費やされた時間が含まれます。

</CustomContent>

<CustomContent platform="tidb-cloud">

リソース制御を有効にすると、システム テーブル[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)には、リソース グループ、対応する SQL の RU 消費量、および使用可能な RU を待機するのに費やされた時間が含まれます。

</CustomContent>

#### RU 統計を<code>statements_summary</code>別にビュー_summary {#view-ru-statistics-by-code-statements-summary-code}

TiDB のシステム テーブル[`INFORMATION_SCHEMA.statements_summary`](/statement-summary-tables.md#statements_summary)には、SQL ステートメントの正規化および集計された統計が格納されます。システム テーブルを使用して、SQL ステートメントの実行パフォーマンスを表示および分析できます。また、リソース グループ名、RU 消費量、使用可能な RU を待機する時間など、リソース制御に関する統計も含まれています。詳細については、 [`statements_summary`フィールドの説明](/statement-summary-tables.md#statements_summary-fields-description)を参照してください。

### リソース グループの RU 消費量をビュー {#view-the-ru-consumption-of-resource-groups}

v7.6.0 以降、TiDB は各リソース グループの RU 消費量の履歴レコードを保存するためのシステム テーブル[`mysql.request_unit_by_group`](/mysql-schema.md#system-tables-related-to-resource-control)を提供します。

例：

```sql
SELECT * FROM request_unit_by_group LIMIT 5;
```

    +----------------------------+----------------------------+----------------+----------+
    | start_time                 | end_time                   | resource_group | total_ru |
    +----------------------------+----------------------------+----------------+----------+
    | 2024-01-01 00:00:00.000000 | 2024-01-02 00:00:00.000000 | default        |   334147 |
    | 2024-01-01 00:00:00.000000 | 2024-01-02 00:00:00.000000 | rg1            |     4172 |
    | 2024-01-01 00:00:00.000000 | 2024-01-02 00:00:00.000000 | rg2            |    34028 |
    | 2024-01-02 00:00:00.000000 | 2024-01-03 00:00:00.000000 | default        |   334088 |
    | 2024-01-02 00:00:00.000000 | 2024-01-03 00:00:00.000000 | rg1            |     3850 |
    +----------------------------+----------------------------+----------------+----------+
    5 rows in set (0.01 sec)

> **注記：**
>
> `mysql.request_unit_by_group`のデータは、毎日の終わりに TiDB スケジュール タスクによって自動的にインポートされます。特定の日にリソース グループの RU 消費量が 0 の場合、レコードは生成されません。デフォルトでは、このテーブルには過去 3 か月 (最大 92 日間) のデータが格納されます。この期間を超えるデータは自動的にクリアされます。

## メトリックとグラフの監視 {#monitoring-metrics-and-charts}

<CustomContent platform="tidb">

TiDB は、リソース制御に関する実行時情報を定期的に収集し、Grafana の**TiDB** &gt;**リソース制御**ダッシュボードにメトリックの視覚的なグラフを提供します。メトリックの詳細については、 [TiDB 重要な監視メトリック](/grafana-tidb-dashboard.md)の**リソース制御**セクションを参照してください。

TiKV は、さまざまなリソース グループからの要求 QPS も記録します。詳細については、 [TiKV モニタリング メトリックの詳細](/grafana-tikv-dashboard.md#grpc)参照してください。

TiDB ダッシュボードの現在の[`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md)テーブルにあるリソース グループのデータは表示できます。詳細については、 [リソース マネージャー ページ](/dashboard/dashboard-resource-manager.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションは、TiDB Self-Hosted にのみ適用されます。現在、 TiDB Cloud はリソース制御メトリックを提供していません。

TiDB は、リソース制御に関する実行時情報を定期的に収集し、Grafana の**TiDB** &gt;**リソース制御**ダッシュボードにメトリックの視覚的なグラフを提供します。

TiKV は、Grafana の**TiKV**ダッシュボードにさまざまなリソース グループからの要求 QPS も記録します。

</CustomContent>

## ツールの互換性 {#tool-compatibility}

リソース制御機能は、データのインポート、エクスポート、およびその他のレプリケーション ツールの通常の使用には影響しませBR。BR、 TiDB Lightning、および TiCDC は現在、リソース制御に関連する DDL 操作の処理をサポートしておらず、それらのリソース消費はリソース制御によって制限されません。

## FAQ {#faq}

1.  リソース グループを使用しない場合は、リソース制御を無効にする必要がありますか?

    いいえ。リソースグループを指定していないユーザーは、無制限のリソースを持つ`default`リソースグループにバインドされます。すべてのユーザーが`default`リソースグループに属している場合、リソースの割り当て方法は、リソース制御が無効の場合と同じです。

2.  データベース ユーザーを複数のリソース グループにバインドできますか?

    いいえ。データベース ユーザーは 1 つのリソース グループにのみバインドできます。ただし、セッション実行時に[`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)使用して、現在のセッションで使用されるリソース グループを設定できます。また、オプティマイザ ヒント[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)を使用して、実行中のステートメントのリソース グループを設定することもできます。

3.  すべてのリソースグループの合計リソース割り当て（ `RU_PER_SEC` ）がシステム容量を超えるとどうなりますか？

    TiDB は、リソース グループを作成するときに容量を検証しません。システムに十分な利用可能なリソースがある限り、TiDB は各リソース グループのリソース要件を満たすことができます。システム リソースが制限を超えると、TiDB は優先度の高いリソース グループからの要求を優先して満たします。同じ優先度の要求をすべて満たすことができない場合、TiDB はリソース割り当て ( `RU_PER_SEC` ) に従ってリソースを比例的に割り当てます。

## 参照 {#see-also}

-   [リソースグループの作成](/sql-statements/sql-statement-create-resource-group.md)
-   [リソースグループの変更](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソースグループを削除](/sql-statements/sql-statement-drop-resource-group.md)
-   [リソース グループ RFC](https://github.com/pingcap/tidb/blob/release-8.1/docs/design/2022-11-25-global-resource-control.md)
