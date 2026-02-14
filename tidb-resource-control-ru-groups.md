---
title: Use Resource Control to Achieve Resource Group Limitation and Flow Control
summary: リソース制御機能を使用してアプリケーション リソースを制御およびスケジュールする方法を学習します。
aliases: ['/ja/tidb/stable/tidb-resource-control/']
---

# リソース制御を使用してリソースグループの制限とフロー制御を実現する {#use-resource-control-to-achieve-resource-group-limitation-and-flow-control}

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

クラスター管理者は、リソース制御機能を使用して、リソース グループを作成したり、リソース グループのクォータを設定したり、ユーザーをそれらのグループにバインドしたりできます。

TiDBリソース制御機能は、TiDBレイヤーにおけるフロー制御機能とTiKVレイヤーにおける優先度スケジューリング機能という、2層のリソース管理機能を提供します。これらの2つの機能は、個別に、または同時に有効化できます。詳細は[リソース制御のパラメータ](#parameters-for-resource-control)参照してください。これにより、TiDBレイヤーはリソースグループに設定されたクォータに基づいてユーザーの読み取りおよび書き込み要求のフローを制御し、TiKVレイヤーは読み取りおよび書き込みクォータにマッピングされた優先度に基づいて要求をスケジュールすることができます。これにより、アプリケーションのリソース分離を確保し、サービス品質（QoS）要件を満たすことができます。

-   TiDBフロー制御：TiDBフロー制御は[トークンバケットアルゴリズム](https://en.wikipedia.org/wiki/Token_bucket)使用します。バケット内に十分なトークンがなく、リソースグループで`BURSTABLE`オプションが指定されていない場合、リソースグループへのリクエストはトークンバケットがトークンをバックフィルするまで待機し、再試行されます。再試行はタイムアウトにより失敗する可能性があります。

-   TiKVスケジューリング：必要に応じて絶対優先度[（ `PRIORITY` ）](/information-schema/information-schema-resource-groups.md#examples)設定できます。3 `PRIORITY`設定に応じて、異なるリソースがスケジュールされます`PRIORITY`の高いタスクが最初にスケジュールされます。絶対優先度を設定しない場合、TiKVは各リソースグループの`RU_PER_SEC`の値を使用して、各リソースグループの読み取りおよび書き込み要求の優先度を決定します。storageレイヤーは、この優先度に基づいて、優先キューを使用して要求をスケジュールおよび処理します。

v7.4.0以降、リソース制御機能はTiFlashリソースの制御をサポートします。その原理は、TiDBフロー制御やTiKVスケジューリングと同様です。

<CustomContent platform="tidb">

-   TiFlashフロー制御： [TiFlashパイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)使用することで、 TiFlashは様々なクエリのCPU消費量をより正確に取得し、それを[リクエストユニット（RU）](#what-is-request-unit-ru)に変換して控除することができます。トラフィック制御はトークンバケットアルゴリズムを用いて実装されています。
-   TiFlashスケジューリング：システムリソースが不足している場合、 TiFlash は複数のリソースグループ間で、優先度に基づいてパイプラインタスクをスケジューリングします。具体的なロジックは次のとおりです。まず、 TiFlash はリソースグループの`PRIORITY`評価し、次に CPU 使用率と`RU_PER_SEC`考慮します。その結果、 `rg1`と`rg2`の`PRIORITY`は同じですが、 `rg2`の`RU_PER_SEC`が`rg1`の 2 倍の場合、 `rg2`の CPU 使用率は`rg1`の 2 倍になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiFlashフロー制御： [TiFlashパイプライン実行モデル](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)使用することで、 TiFlashは様々なクエリのCPU消費量をより正確に取得し、それを[リクエストユニット（RU）](#what-is-request-unit-ru)に変換して控除することができます。トラフィック制御はトークンバケットアルゴリズムを用いて実装されています。
-   TiFlashスケジューリング：システムリソースが不足している場合、 TiFlash は複数のリソースグループ間で、優先度に基づいてパイプラインタスクをスケジューリングします。具体的なロジックは次のとおりです。まず、 TiFlash はリソースグループの`PRIORITY`評価し、次に CPU 使用率と`RU_PER_SEC`考慮します。その結果、 `rg1`と`rg2`の`PRIORITY`は同じですが、 `rg2`の`RU_PER_SEC`が`rg1`の 2 倍の場合、 `rg2`の CPU 使用率は`rg1`の 2 倍になります。

</CustomContent>

バックグラウンド タスクを管理し、リソースを大量に消費するクエリ (ランナウェイ クエリ) を処理する方法については、次のドキュメントを参照してください。

-   [リソース制御を使用してバックグラウンドタスクを管理する](/tidb-resource-control-background-tasks.md)
-   [予想以上にリソースを消費するクエリ（ランナウェイクエリ）を管理する](/tidb-resource-control-runaway-queries.md)

## リソース管理のシナリオ {#scenarios-for-resource-control}

リソース制御機能の導入は、TiDBにとって画期的な出来事です。この機能により、分散データベースクラスタを複数の論理ユニットに分割できます。個々のユニットがリソースを過剰に使用しても、他のユニットに必要なリソースが圧迫されることはありません。

この機能を使用すると、次のことが可能になります。

-   複数の異なるシステムから複数の中小規模アプリケーションを単一のTiDBクラスタに統合します。あるアプリケーションのワークロードが増加しても、他のアプリケーションの正常な動作に影響を与えることはありません。システムのワークロードが低い場合は、設定されたクォータを超えても、高負荷のアプリケーションに必要なシステムリソースを割り当てることができるため、リソースを最大限に活用できます。
-   すべてのテスト環境を単一のTiDBクラスターに統合するか、リソースを多く消費するバッチタスクを単一のリソースグループにまとめるかを選択できます。これにより、ハードウェア使用率を向上させ、運用コストを削減しながら、重要なアプリケーションに必要なリソースを常に確保できます。
-   システム内に複数のワークロードが混在している場合、異なるワークロードを別々のリソースグループに配置できます。リソース制御機能を使用することで、トランザクションアプリケーションの応答時間がデータ分析やバッチアプリケーションの影響を受けないようにすることができます。
-   クラスターで予期しない SQL パフォーマンスの問題が発生した場合、リソース グループとともに SQL バインディングを使用して、SQL ステートメントのリソース消費を一時的に制限できます。

さらに、リソース制御機能を合理的に使用すると、クラスターの数を削減し、運用と保守の難易度を軽減し、管理コストを節約できます。

> **注記：**
>
> -   リソース管理の有効性を評価するには、独立したコンピューティングノードとstorageノードにクラスターをデプロイすることをお勧めします`tiup playground`で作成されたデプロイメントでは、リソースがインスタンス間で共有されるため、スケジューリングなどのクラスターリソースに依存する機能は正常に動作しにくいです。

## 制限事項 {#limitations}

リソース制御は追加のスケジューリングオーバーヘッドを発生させます。そのため、この機能を有効にすると、パフォーマンスがわずかに低下する可能性があります（5%未満）。

## リクエストユニット（RU）とは {#what-is-request-unit-ru}

リクエストユニット（RU）は、TiDBにおけるシステムリソースの統合抽象化単位であり、現在CPU、IOPS、IO帯域幅のメトリクスが含まれています。これは、データベースへの単一のリクエストで消費されるリソース量を示すために使用されます。リクエストで消費されるRUの数は、操作の種類、クエリまたは変更されるデータの量など、さまざまな要因によって異なります。現在、RUには次の表に示すリソースの消費統計が含まれています。

<table><thead><tr><th>リソースタイプ</th><th>RU消費量</th></tr></thead><tbody><tr><td rowspan="3">読む</td><td>2 つのstorage読み取りバッチは 1 RU を消費します</td></tr><tr><td>8 個のstorage読み取り要求は 1 RU を消費します</td></tr><tr><td>64 KiBの読み取り要求ペイロードは1 RUを消費します</td></tr><tr><td rowspan="3">書く</td><td>1 回のstorage書き込みバッチで 1 RU が消費されます</td></tr><tr><td>1 回のstorage書き込み要求で 1 RU が消費される</td></tr><tr><td>1 KiB の書き込み要求ペイロードは 1 RU を消費します</td></tr><tr><td>CPU</td><td> 3 ミリ秒で 1 RU を消費します</td></tr></tbody></table>

> **注記：**
>
> -   各書き込み操作は最終的にすべてのレプリカに複製されます（デフォルトでは、TiKV には 3 つのレプリカがあります）。各レプリケーション操作はそれぞれ異なる書き込み操作とみなされます。
> -   上記の表は、TiDBセルフマネージドクラスターのRU計算に関係するリソースのみを示しており、ネットワークとstorageの消費は含まれていません。TiDB TiDB Cloud Starter RUについては、 [TiDB Cloud Starter の価格詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)参照してください。
> -   現在、 TiFlashリソース制御では、クエリのパイプライン タスクの実行によって消費される CPU 時間である SQL CPU と、読み取り要求ペイロードのみが考慮されます。

## リソース制御のパラメータ {#parameters-for-resource-control}

リソース制御機能では、次のシステム変数またはパラメータが導入されています。

-   TiDB: [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)システム変数を使用して、リソース グループのフロー制御を有効にするかどうかを制御できます。

<CustomContent platform="tidb">

-   TiKV: [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)パラメータを使用して、リソース グループに基づいて要求のスケジュールを使用するかどうかを制御できます。
-   TiFlash: [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)システム変数と[`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)構成項目 (v7.4.0 で導入) を使用して、 TiFlashリソース制御を有効にするかどうかを制御できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiKV: TiDB Self-Managed の場合、パラメータ`resource-control.enabled`使用して、リソースグループのクォータに基づくリクエストスケジューリングを使用するかどうかを制御できます。TiDB TiDB Cloudの場合、パラメータ`resource-control.enabled`の値はデフォルトで`true`設定されており、動的な変更はサポートされていません。
-   TiFlash: TiDB Self-Managed の場合、 `tidb_enable_resource_control`システム変数と`enable_resource_control`構成項目 (v7.4.0 で導入) を使用して、 TiFlashリソース制御を有効にするかどうかを制御できます。

</CustomContent>

TiDB v7.0.0以降では、 `tidb_enable_resource_control`と`resource-control.enabled`デフォルトで有効になっています。これらの2つのパラメータの組み合わせの結果は次の表に示されています。

| `resource-control.enabled`     | `tidb_enable_resource_control` = オン | `tidb_enable_resource_control` = オフ |
| :----------------------------- | :---------------------------------- | :---------------------------------- |
| `resource-control.enabled` = 真 | フロー制御とスケジューリング（推奨）                  | 無効な組み合わせ                            |
| `resource-control.enabled` = 偽 | フロー制御のみ（非推奨）                        | この機能は無効になっています。                     |

<CustomContent platform="tidb">

v7.4.0以降、 TiFlash設定項目`enable_resource_control`デフォルトで有効になっています。これは`tidb_enable_resource_control`と連携してTiFlashリソース制御機能を制御します。TiFlashTiFlash制御は、 `enable_resource_control`と`tidb_enable_resource_control`両方が有効な場合にのみ、フロー制御と優先度スケジューリングを実行します。また、 `enable_resource_control`有効な場合、 TiFlashは[パイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)使用します。

</CustomContent>

<CustomContent platform="tidb-cloud">

v7.4.0以降、 TiFlash設定項目`enable_resource_control`デフォルトで有効になっています。これは`tidb_enable_resource_control`と連携してTiFlashリソース制御機能を制御します。TiFlashTiFlash制御は、 `enable_resource_control`と`tidb_enable_resource_control`両方が有効な場合にのみ、フロー制御と優先度スケジューリングを実行します。また、 `enable_resource_control`有効な場合、 TiFlashは[パイプライン実行モデル](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)使用します。

</CustomContent>

リソース制御のメカニズムとパラメータの詳細については、 [RFC: TiDB におけるグローバル リソース制御](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2022-11-25-global-resource-control.md)と[TiFlashリソース制御](https://github.com/pingcap/tiflash/blob/release-8.5/docs/design/2023-09-21-tiflash-resource-control.md)参照してください。

## リソース制御の使い方 {#how-to-use-resource-control}

このセクションでは、リソース制御機能を使用してリソース グループを管理し、各リソース グループのリソース割り当てを制御する方法について説明します。

### クラスター容量の見積もり {#estimate-cluster-capacity}

<CustomContent platform="tidb">

リソースプランニングを行う前に、クラスタ全体のキャパシティを把握しておく必要があります。TiDBは、クラスタキャパシティを見積もるためのステートメント[`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md)を提供しています。以下のいずれかの方法を使用できます。

-   [実際の作業負荷に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
-   [ハードウェアの展開に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

[リソースマネージャーページ](/dashboard/dashboard-resource-manager.md) TiDB ダッシュボードで確認できます。詳細については[`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md#methods-for-estimating-capacity)ご覧ください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB Self-Managed の場合、 [`CALIBRATE RESOURCE`](https://docs.pingcap.com/tidb/stable/sql-statement-calibrate-resource)ステートメントを使用してクラスターの容量を見積もることができます。

TiDB Cloudの場合、 [`CALIBRATE RESOURCE`](https://docs.pingcap.com/tidb/stable/sql-statement-calibrate-resource)ステートメントは適用されません。

</CustomContent>

### リソース グループを管理する {#manage-resource-groups}

リソース グループを作成、変更、または削除するには、 `SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

[`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)使用してクラスターのリソース グループを作成できます。

既存のリソースグループの場合、 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)使用して、リソースグループの`RU_PER_SEC`オプション（1 秒あたりの RU バックフィル速度）を変更できます。リソースグループへの変更はすぐに有効になります。

[`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)使用してリソース グループを削除できます。

### リソースグループを作成する {#create-a-resource-group}

以下は、リソース グループを作成する方法の例です。

1.  リソース グループ`rg1`を作成します。リソース制限は 1 秒あたり 500 RU で、このリソース グループ内のアプリケーションはリソースをオーバーランできます。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2.  リソース グループ`rg2`を作成します。RU バックフィル レートは 1 秒あたり 600 RU であり、このリソース グループ内のアプリケーションがリソースをオーバーランすることは許可されません。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3.  絶対優先度を`HIGH`に設定したリソースグループ`rg3`を作成します。現在、絶対優先度は`LOW|MEDIUM|HIGH`サポートされています。デフォルト値は`MEDIUM`です。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg3 RU_PER_SEC = 100 PRIORITY = HIGH;
    ```

### リソースグループをバインドする {#bind-resource-groups}

TiDB は、次の 3 つのレベルのリソース グループ設定をサポートしています。

-   ユーザーレベル。1 または[`CREATE USER`](/sql-statements/sql-statement-create-user.md) [`ALTER USER`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)ステートメントを使用して、ユーザーを特定のリソースグループにバインドします。ユーザーがリソースグループにバインドされると、そのユーザーが作成したセッションは自動的に対応するリソースグループにバインドされます。
-   セッションレベル[`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)で現在のセッションのリソースグループを設定します。
-   ステートメント レベル。1 [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)オプティマイザー ヒントを使用して、現在のステートメントのリソース グループを設定します。

#### ユーザーをリソースグループにバインドする {#bind-users-to-a-resource-group}

次の例では、ユーザー`usr1`を作成し、そのユーザーをリソース グループ`rg1`にバインドします。5 `rg1` 、 [リソースグループの作成](#create-a-resource-group)の例で作成されたリソース グループです。

```sql
CREATE USER 'usr1'@'%' IDENTIFIED BY '123' RESOURCE GROUP rg1;
```

次の例では、 `ALTER USER`を使用してユーザー`usr2`リソース グループ`rg2`にバインドします。 `rg2` 、 [リソースグループの作成](#create-a-resource-group)の例で作成されたリソース グループです。

```sql
ALTER USER usr2 RESOURCE GROUP rg2;
```

ユーザーをバインドすると、新規に作成されたセッションのリソース消費量は、指定されたクォータ（リクエストユニット、RU）によって制御されます。システムのワークロードが比較的高く、余裕のある容量がない場合、リソース消費率`usr2`クォータを超えないように厳密に制御されます。3 `usr1` `rg1`にバインドされ、 `BURSTABLE`が設定されているため、消費率`usr1`はクォータを超えることが許容されます。

リクエストが多すぎてリソースグループのリソースが不足した場合、クライアントのリクエストは待機状態になります。待機時間が長すぎる場合、リクエストはエラーを報告します。

> **注記：**
>
> -   `CREATE USER`または`ALTER USER`使用してユーザーをリソース グループにバインドすると、それはユーザーの既存のセッションには適用されず、ユーザーの新しいセッションにのみ適用されます。
> -   TiDBは、クラスタの初期化中に自動的にリソースグループ`default`を作成します。このリソースグループでは、デフォルト値は`RU_PER_SEC`ですが、 `UNLIMITED` （ `INT`タイプの最大値である`2147483647`相当）に設定され、モードは`BURSTABLE`です。リソースグループにバインドされていないステートメントは、このリソースグループに自動的にバインドされます。このリソースグループは削除できませんが、RUの設定を変更できます。

リソース グループからユーザーのバインドを解除するには、次のようにして、ユーザーを`default`グループに再度バインドするだけです。

```sql
ALTER USER 'usr3'@'%' RESOURCE GROUP `default`;
```

詳細については[`ALTER USER ... RESOURCE GROUP`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)参照してください。

#### 現在のセッションをリソースグループにバインドする {#bind-the-current-session-to-a-resource-group}

[`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)ステートメントを使用すると、現在のセッションにバインドされているリソースグループを変更できます。セッションをリソースグループにバインドすると、対応するセッションのリソース使用量は指定された使用量（RU）に制限されます。

システム変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) `ON`に設定されている場合、このステートメントを実行するには`SUPER` 、 `RESOURCE_GROUP_ADMIN` 、または`RESOURCE_GROUP_USER`権限が必要です。

次の例では、現在のセッションをリソース グループ`rg1`にバインドします。

```sql
SET RESOURCE GROUP rg1;
```

#### 現在のステートメントをリソース グループにバインドする {#bind-the-current-statement-to-a-resource-group}

SQL文に[`RESOURCE_GROUP(resource_group_name)`](/optimizer-hints.md#resource_groupresource_group_name)ヒントを追加することで、文がバインドされるリソースグループを指定できます。このヒントは、 `SELECT` 、 `INSERT` 、 `UPDATE` 、および`DELETE`文をサポートします。

システム変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) `ON`に設定されている場合、このヒントを使用するには`SUPER` 、 `RESOURCE_GROUP_ADMIN` 、または`RESOURCE_GROUP_USER`権限が必要です。

次の例では、現在のステートメントをリソース グループ`rg1`にバインドします。

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
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

2.  TiDB Self-Managed の場合、パラメータ`resource-control.enabled`使用して、リソースグループのクォータに基づくリクエストスケジューリングを使用するかどうかを制御できます。TiDB TiDB Cloudの場合、パラメータ`resource-control.enabled`の値はデフォルトで`true`設定されており、動的な変更はサポートされていません。TiDB TiDB Cloud Dedicated クラスターでこのパラメータを無効にする必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

3.  TiDB Self-Managed の場合、設定項目`enable_resource_control`使用してTiFlashリソース制御を有効にするかどうかを制御できます。TiDB TiDB Cloudの場合、パラメータ`enable_resource_control`の値はデフォルトで`true`設定されており、動的な変更はサポートされていません。TiDB TiDB Cloud Dedicated クラスターで無効にする必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

</CustomContent>

## RU消費量をビュー {#view-ru-consumption}

RU 消費量に関する情報を表示できます。

### SQL による RU 消費量をビュー {#view-the-ru-consumption-by-sql}

SQL ステートメントの RU 消費量は、次の方法で確認できます。

-   システム変数`tidb_last_query_info`
-   `EXPLAIN ANALYZE`
-   遅いクエリとそれに対応するシステムテーブル
-   `statements_summary`

#### システム変数<code>tidb_last_query_info</code>をクエリして、最後の SQL 実行で消費された RUをビュー。 {#view-the-rus-consumed-by-the-last-sql-execution-by-querying-the-system-variable-code-tidb-last-query-info-code}

TiDBはシステム変数[`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014)を提供します。このシステム変数は、SQL実行で消費されたRUを含む、最後に実行されたDMLステートメントの情報を記録します。

例：

1.  `UPDATE`ステートメントを実行します。

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

#### <code>EXPLAIN ANALYZE</code>による SQL 実行中に消費された RU をビュー {#view-rus-consumed-during-sql-execution-by-code-explain-analyze-code}

[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption)ステートメントを使用すると、SQL実行中に消費されたRUの量を取得できます。RUの量はキャッシュの影響を受けることに注意してください（例： [コプロセッサキャッシュ](/coprocessor-cache.md) ）。同じSQLを複数回実行した場合、各実行で消費されるRUの量は異なる場合があります。RUの値は各実行の正確な値を表すものではありませんが、概算の参考として使用できます。

#### 遅いクエリとそれに対応するシステムテーブル {#slow-queries-and-the-corresponding-system-table}

<CustomContent platform="tidb">

リソース制御を有効にすると、TiDB の[スロークエリログ](/identify-slow-queries.md)と対応するシステム テーブル[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)に、リソース グループ、対応する SQL の RU 消費量、使用可能な RU を待機するのに費やされた時間が含まれます。

</CustomContent>

<CustomContent platform="tidb-cloud">

リソース制御を有効にすると、システム テーブル[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)には、リソース グループ、対応する SQL の RU 消費量、および使用可能な RU を待機するのに費やされた時間が含まれます。

</CustomContent>

#### RU統計を<code>statements_summary</code>別にビュー {#view-ru-statistics-by-code-statements-summary-code}

TiDBのシステムテーブル[`INFORMATION_SCHEMA.statements_summary`](/statement-summary-tables.md#statements_summary)には、SQL文の正規化および集計された統計情報が格納されます。このシステムテーブルを使用して、SQL文の実行パフォーマンスを表示および分析できます。また、リソースグループ名、RU消費量、利用可能なRUの待機時間など、リソース制御に関する統計情報も含まれています。詳細については、 [`statements_summary`フィールドの説明](/statement-summary-tables.md#statements_summary-fields-description)参照してください。

### リソース グループの RU 消費量をビュー {#view-the-ru-consumption-of-resource-groups}

v7.6.0 以降、TiDB は各リソース グループの RU 消費量の履歴レコードを保存するためのシステム テーブル[`mysql.request_unit_by_group`](/mysql-schema/mysql-schema.md#system-tables-related-to-resource-control)を提供します。

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
> `mysql.request_unit_by_group`のデータは、TiDBのスケジュールタスクによって毎日の終わりに自動的にインポートされます。特定の日にリソースグループのRU消費量が0の場合、レコードは生成されません。デフォルトでは、このテーブルには過去3か月間（最大92日間）のデータが保存されます。この期間を超えるデータは自動的にクリアされます。

## メトリックとグラフの監視 {#monitoring-metrics-and-charts}

<CustomContent platform="tidb">

TiDBはリソース制御に関する実行時情報を定期的に収集し、Grafanaの**「TiDB** &gt;**リソース制御」**ダッシュボードにメトリクスの視覚的なチャートを提供します。メトリクスの詳細については、 [TiDB の重要な監視メトリック](/grafana-tidb-dashboard.md)の**「リソース制御」**セクションをご覧ください。

TiKVは、異なるリソースグループからのリクエストQPSも記録します。詳細については、 [TiKV モニタリング メトリックの詳細](/grafana-tikv-dashboard.md#grpc)参照してください。

TiDBダッシュボードの現在の[`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md)テーブルにあるリソースグループのデータを表示できます。詳細については、 [リソース マネージャー ページ](/dashboard/dashboard-resource-manager.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションはTiDBセルフマネージドにのみ適用されます。現在、 TiDB Cloudリソース制御メトリクスは提供されていません。

TiDB は、リソース制御に関する実行時情報を定期的に収集し、Grafana の**TiDB** &gt;**リソース制御**ダッシュボードにメトリックの視覚的なグラフを提供します。

TiKV は、Grafana の**TiKV**ダッシュボードにさまざまなリソース グループからの要求 QPS も記録します。

</CustomContent>

## ツールの互換性 {#tool-compatibility}

リソース制御機能は、データのインポート、エクスポート、およびその他のレプリケーション ツールの通常の使用には影響しませんBR、 TiDB Lightning、および TiCDC は現在、リソース制御に関連する DDL 操作の処理をサポートしておらず、それらのリソース消費はリソース制御によって制限されません。

## FAQ {#faq}

1.  リソース グループを使用しない場合は、リソース制御を無効にする必要がありますか?

    いいえ。リソースグループを指定していないユーザーは、リソースが無制限のリソースグループ`default`にバインドされます。すべてのユーザーがリソースグループ`default`に所属している場合、リソースの割り当て方法はリソース制御が無効になっている場合と同じです。

2.  データベース ユーザーを複数のリソース グループにバインドできますか?

    いいえ。データベースユーザーは1つのリソースグループにのみバインドできます。ただし、セッション実行時には、 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)使用して現在のセッションで使用されるリソースグループを設定できます。また、オプティマイザヒント[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)使用して、実行中のステートメントのリソースグループを設定することもできます。

3.  すべてのリソースグループの合計リソース割り当て（ `RU_PER_SEC` ）がシステム容量を超えるとどうなりますか？

    TiDBは、リソースグループを作成する際に容量を検証しません。システムに十分なリソースがある限り、TiDBは各リソースグループのリソース要件を満たすことができます。システムリソースが制限を超えた場合、TiDBは優先度の高いリソースグループからの要求を優先的に満たします。同じ優先度の要求をすべて満たせない場合は、TiDBはリソース割り当て（ `RU_PER_SEC` ）に従ってリソースを比例配分します。

## 参照 {#see-also}

-   [リソースグループの作成](/sql-statements/sql-statement-create-resource-group.md)
-   [リソースグループの変更](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソースグループの削除](/sql-statements/sql-statement-drop-resource-group.md)
-   [リソースグループ RFC](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2022-11-25-global-resource-control.md)
