---
title: Use Resource Control to Achieve Resource Group Limitation and Flow Control
summary: リソース制御機能を使用して、アプリケーションのリソースを制御およびスケジュールする方法を学びましょう。
aliases: ['/ja/tidb/v8.5/tidb-resource-control/','/ja/tidb/stable/tidb-resource-control/']
---

# リソース制御を使用して、リソースグループの制限とフロー制御を実現します。 {#use-resource-control-to-achieve-resource-group-limitation-and-flow-control}

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

クラスタ管理者として、リソース制御機能を使用して、リソースグループの作成、リソースグループの割り当て量の設定、およびユーザーをそれらのグループにバインドすることができます。

TiDBのリソース制御機能は、TiDBレイヤーのフロー制御機能とTiKVレイヤーの優先度スケジューリング機能という2つのレイヤーのリソース管理機能を提供します。これらの2つの機能は、個別に、または同時に有効にすることができます。詳しくは[リソース制御のためのパラメータ](#parameters-for-resource-control)については を参照してください。これにより、TiDBレイヤーはリソースグループに設定されたクォータに基づいてユーザーの読み取りおよび書き込み要求のフローを制御し、TiKVレイヤーは読み取りおよび書き込みクォータにマッピングされた優先度に基づいて要求をスケジュールすることができます。この操作を行うことで、アプリケーションのリソース分離を確保し、サービス品質（QoS）要件を満たすことができます。

-   TiDBフロー制御：TiDBフロー制御は を使用します。バケットに十分なトークンがなく、リソースグループ [トークンバケットアルゴリズム](https://en.wikipedia.org/wiki/Token_bucket)`BURSTABLE`オプションを指定していない場合、リソースグループへのリクエストはトークンバケットがトークンを補充するまで待機し、再試行します。再試行はタイムアウトにより失敗する可能性があります。

-   TiKV スケジューリング: 必要に応じて絶対優先度[（ `PRIORITY` ）](/information-schema/information-schema-resource-groups.md#examples)を設定できます。異なるリソースは`PRIORITY`設定に従ってスケジュールされます。 `PRIORITY`が高いタスクが最初にスケジュールされます。絶対優先度を設定しない場合、TiKV は各リソース グループの`RU_PER_SEC`の値を使用して、各リソース グループの読み取りおよび書き込み要求の優先度を決定します。ストレージレイヤーは、優先度に基づいて優先度キューを使用して要求をスケジュールおよび処理します。

バージョン7.4.0以降、リソース制御機能はTiFlashリソースの制御をサポートしています。その原理は、TiDBフロー制御およびTiKVスケジューリングと同様です。

<CustomContent platform="tidb">

-   TiFlashフロー制御: [TiFlashパイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)ライン実行モデルを使用すると、 TiFlash はさまざまなクエリの CPU 消費量をより正確に取得し、それを[要求単位数（RU）](#what-is-request-unit-ru)に変換して差し引くことができます。トラフィック制御はトークン バケット アルゴリズムを使用して実装されます。
-   TiFlashスケジューリング: システム リソースが不足している場合、 TiFlash は優先順位に基づいて複数のリソース グループ間でパイプライン タスクをスケジュールします。具体的なロジックは次のとおりです。まず、 TiFlash はリソース グループの`PRIORITY`を評価し、次に CPU 使用率と`RU_PER_SEC`を考慮します。その結果、 `rg1`と`rg2`が同じ`PRIORITY`を持ち、 `RU_PER_SEC`の`rg2`が`rg1`の 2 倍である場合、 `rg2`の CPU 使用率は`rg1`の 2 倍になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiFlashフロー制御: [TiFlashパイプライン実行モデル](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)ライン実行モデルを使用すると、 TiFlash はさまざまなクエリの CPU 消費量をより正確に取得し、それを[要求単位数（RU）](#what-is-request-unit-ru)に変換して差し引くことができます。トラフィック制御はトークン バケット アルゴリズムを使用して実装されます。
-   TiFlashスケジューリング: システム リソースが不足している場合、 TiFlash は優先順位に基づいて複数のリソース グループ間でパイプライン タスクをスケジュールします。具体的なロジックは次のとおりです。まず、 TiFlash はリソース グループの`PRIORITY`を評価し、次に CPU 使用率と`RU_PER_SEC`を考慮します。その結果、 `rg1`と`rg2`が同じ`PRIORITY`を持ち、 `RU_PER_SEC`の`rg2`が`rg1`の 2 倍である場合、 `rg2`の CPU 使用率は`rg1`の 2 倍になります。

</CustomContent>

バックグラウンドタスクの管理方法や、リソースを大量に消費するクエリ（暴走クエリ）の処理方法については、以下のドキュメントを参照してください。

-   [バックグラウンドタスクの管理にはリソース制御を使用する](/tidb-resource-control-background-tasks.md)
-   [想定以上のリソースを消費するクエリ（暴走クエリ）を管理する](/tidb-resource-control-runaway-queries.md)

## リソース制御のシナリオ {#scenarios-for-resource-control}

リソース制御機能の導入は、TiDBにとって画期的な出来事です。この機能により、分散データベースクラスタを複数の論理ユニットに分割できます。たとえ個々のユニットがリソースを過剰に使用したとしても、他のユニットが必要とするリソースを圧迫することはありません。

この機能を使うと、次のことができます。

-   異なるシステムに存在する複数の中小規模アプリケーションを単一のTiDBクラスタに統合します。アプリケーションのワークロードが増加しても、他のアプリケーションの正常な動作には影響しません。システムワークロードが低い場合、負荷の高いアプリケーションは設定されたクォータを超えても必要なシステムリソースを割り当てられるため、リソースを最大限に活用できます。
-   すべてのテスト環境を単一のTiDBクラスタに統合するか、より多くのリソースを消費するバッチタスクを単一のリソースグループにまとめるかを選択できます。これにより、ハードウェア利用率を向上させ、運用コストを削減しながら、重要なアプリケーションが常に必要なリソースを確保できるようになります。
-   システム内に複数のワークロードが存在する場合、異なるワークロードを別々のリソースグループに割り当てることができます。リソース制御機能を使用することで、トランザクションアプリケーションの応答時間がデータ分析やバッチ処理アプリケーションの影響を受けないようにすることができます。
-   クラスターで予期しないSQLパフォーマンスの問題が発生した場合、SQLバインディングとリソースグループを併用することで、SQLステートメントのリソース消費を一時的に制限できます。

さらに、リソース制御機能を合理的に活用することで、クラスタ数を削減し、運用・保守の難易度を下げ、管理コストを削減することができます。

> **注記：**
>
> -   リソース管理の有効性を評価するには、クラスタを独立したコンピューティングノードとストレージノードにデプロイすることをお勧めします。 `tiup playground`で作成されたデプロイメントでは、リソースがインスタンス間で共有されるため、スケジューリングやその他のクラスタのリソースに依存する機能が正しく動作しない場合があります。

## 制限事項 {#limitations}

リソース制御にはスケジューリングのオーバーヘッドが加わるため、この機能を有効にするとパフォーマンスがわずかに低下する可能性があります（5%未満）。

## リクエストユニット（RU）とは何ですか？ {#what-is-request-unit-ru}

リクエストユニット（RU）は、TiDBにおけるシステムリソースの統一抽象化単位であり、現在CPU、IOPS、およびIO帯域幅メトリックが含まれています。これは、データベースへの単一のリクエストによって消費されるリソースの量を示すために使用されます。リクエストによって消費されるRUの数は、操作の種類や、クエリまたは変更されるデータの量など、さまざまな要因によって異なります。現在、RUには次の表に示すリソースの消費統計が含まれています。

<table><thead><tr><th>リソースタイプ</th><th>RU消費量</th></tr></thead><tbody><tr><td rowspan="3">読む</td><td>ストレージ読み取りバッチ2つで1RUを消費します</td></tr><tr><td>8回のストレージ読み取りリクエストで1RUを消費します</td></tr><tr><td>64 KiBの読み取りリクエストペイロードは1 RUを消費します</td></tr><tr><td rowspan="3">書く</td><td>ストレージ書き込みバッチ1つにつき1RUを消費します</td></tr><tr><td>ストレージ書き込みリクエスト1件につき1RUを消費します。</td></tr><tr><td> 1 KiBの書き込みリクエストペイロードは1 RUを消費します</td></tr><tr><td>CPU</td><td> 3ミリ秒で1RUを消費します</td></tr></tbody></table>

> **注記：**
>
> -   各書き込み操作は最終的にすべてのレプリカに複製されます（デフォルトでは、TiKVには3つのレプリカがあります）。各複製操作は、それぞれ異なる書き込み操作として扱われます。
> -   上記の表には、TiDB Self-ManagedクラスタのRU計算に関わるリソースのみが記載されており、ネットワークとストレージの消費量は含まれていません。TiDB Cloud StarterのRUについては、 [TiDB Cloud Starterの料金詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)参照してください。
> -   現在、 TiFlashのリソース制御では、SQL CPUのみが考慮されます。SQL CPUとは、クエリおよび読み取りリクエストのペイロードに対するパイプラインタスクの実行によって消費されるCPU時間です。

## リソース制御のためのパラメータ {#parameters-for-resource-control}

リソース制御機能では、以下のシステム変数またはパラメータが導入されます。

-   TiDB: [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)システム変数を使用して、リソースグループのフロー制御を有効にするかどうかを制御できます。

<CustomContent platform="tidb">

-   TiKV: [`resource-control.enabled`](/tikv-configuration-file.md#resource-control)パラメータを使用すると、リソース グループに基づいてリクエスト スケジューリングを使用するかどうかを制御できます。
-   TiFlash: TiFlashリソース制御を有効にするかどうかは、 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660)システム変数と[`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)構成項目（v7.4.0で導入）を使用して制御できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiKV: TiDB Self-Managed では、 `resource-control.enabled`パラメータを使用して、リソースグループのクォータに基づいてリクエストスケジューリングを使用するかどうかを制御できます。TiDB Cloudでは、 `resource-control.enabled`パラメータのデフォルト値は`true`であり、動的な変更はサポートされていません。
-   TiFlash: TiDB Self-Managedの場合、 `tidb_enable_resource_control`システム変数と`enable_resource_control`構成項目 (v7.4.0 で導入) を使用して、 TiFlashリソース制御を有効にするかどうかを制御できます。

</CustomContent>

TiDB v7.0.0以降、 `tidb_enable_resource_control`と`resource-control.enabled`はデフォルトで有効になっています。これら2つのパラメータの組み合わせによる結果を次の表に示します。

| `resource-control.enabled`         | `tidb_enable_resource_control` = オン | `tidb_enable_resource_control` = オフ |
| :--------------------------------- | :---------------------------------- | :---------------------------------- |
| `resource-control.enabled` = true  | フロー制御とスケジューリング（推奨）                  | 無効な組み合わせ                            |
| `resource-control.enabled` = false | 流量制御のみ（推奨しません）                      | この機能は無効になっています。                     |

<CustomContent platform="tidb">

バージョン7.4.0以降、 TiFlash構成項目`enable_resource_control`はデフォルトで有効になっています。これは`tidb_enable_resource_control`と連携してTiFlash制御機能を制御します。TiFlashリソース制御は、 `enable_resource_control`と`tidb_enable_resource_control`の両方が有効になっている場合にのみ、フロー制御と優先度スケジューリングを実行します。さらに、 `enable_resource_control`有効になっている場合、 TiFlashは[パイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)を使用します。

</CustomContent>

<CustomContent platform="tidb-cloud">

バージョン7.4.0以降、 TiFlash構成項目`enable_resource_control`はデフォルトで有効になっています。これは`tidb_enable_resource_control`と連携してTiFlash制御機能を制御します。TiFlashリソース制御は、 `enable_resource_control`と`tidb_enable_resource_control`の両方が有効になっている場合にのみ、フロー制御と優先度スケジューリングを実行します。さらに、 `enable_resource_control`有効になっている場合、 TiFlashは[パイプライン実行モデル](http://docs.pingcap.com/tidb/dev/tiflash-pipeline-model)を使用します。

</CustomContent>

リソース制御メカニズムとパラメータの詳細については、 [RFC: TiDBにおけるグローバルリソース制御](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2022-11-25-global-resource-control.md)および[TiFlashリソース制御](https://github.com/pingcap/tiflash/blob/release-8.5/docs/design/2023-09-21-tiflash-resource-control.md)参照してください。

## リソース制御の使い方 {#how-to-use-resource-control}

このセクションでは、リソース制御機能を使用してリソースグループを管理し、各リソースグループのリソース割り当てを制御する方法について説明します。

### クラスター容量を推定する {#estimate-cluster-capacity}

<CustomContent platform="tidb">

リソース計画を行う前に、クラスタ全体の容量を把握しておく必要があります。TiDB では、クラスタ容量を推定するための[`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md)ステートメントが提供されています。以下のいずれかの方法を使用できます。

-   [実際の作業負荷に基づいて容量を推定する](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
-   [ハードウェアの導入状況に基づいて容量を推定する](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

TiDB ダッシュボードで[リソースマネージャーページ](/dashboard/dashboard-resource-manager.md)を表示できます。詳細については、 [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md#methods-for-estimating-capacity)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB Self-Managedの場合、 [`CALIBRATE RESOURCE`](https://docs.pingcap.com/tidb/stable/sql-statement-calibrate-resource)ステートメントを使用してクラスタ容量を推定できます。

TiDB Cloudの場合、 [`CALIBRATE RESOURCE`](https://docs.pingcap.com/tidb/stable/sql-statement-calibrate-resource)ステートメントは適用できません。

</CustomContent>

### リソースグループを管理する {#manage-resource-groups}

リソース グループを作成、変更、または削除するには、 `SUPER`または`RESOURCE_GROUP_ADMIN`権限が必要です。

[`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)コマンドを使用して、クラスターのリソース グループを作成できます。

既存のリソースグループの場合、 [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)を使用して、リソースグループの`RU_PER_SEC`オプション (1 秒あたりの RU バックフィル率) を変更できます。リソースグループへの変更は即座に有効になります。

[`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)を使用してリソースグループを削除できます。

### リソースグループを作成する {#create-a-resource-group}

以下は、リソースグループを作成する方法の例です。

1.  リソースグループ`rg1`を作成します。リソース制限は毎秒 500 RU で、このリソースグループ内のアプリケーションはリソースを超過することができます。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2.  リソースグループ`rg2`を作成します。RU バックフィルレートは毎秒 600 RU で、このリソースグループ内のアプリケーションがリソースをオーバーランすることを許可しません。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3.  絶対優先度を`rg3` `HIGH`を作成します。現在の絶対優先度は`LOW|MEDIUM|HIGH`をサポートしています。デフォルト値は`MEDIUM`です。

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg3 RU_PER_SEC = 100 PRIORITY = HIGH;
    ```

### リソースグループをバインドする {#bind-resource-groups}

TiDBは、以下の3つのレベルのリソースグループ設定をサポートしています。

-   ユーザーレベル。[`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)ステートメントを使用して、ユーザーを特定のリソースグループにバインドします。ユーザーがリソースグループにバインドされると、そのユーザーが作成したセッションは自動的に対応するリソースグループにバインドされます。
-   セッションレベル。SET [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)を使用して、現在のセッションのリソースグループを設定します。
-   ステートメントレベル。RESOURCE_GROUP [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)オプティマイザヒントを使用して、現在のステートメントのリソースグループを設定します。

#### ユーザーをリソースグループにバインドする {#bind-users-to-a-resource-group}

次の例では、ユーザー`usr1`を作成し、そのユーザーをリソース グループ`rg1`にバインドします。 `rg1`は[リソースグループを作成する](#create-a-resource-group)するの例で作成されたリソース グループです。

```sql
CREATE USER 'usr1'@'%' IDENTIFIED BY '123' RESOURCE GROUP rg1;
```

次の例では`ALTER USER`を使用して、ユーザー`usr2`をリソース グループ`rg2`にバインドします。 `rg2`は[リソースグループを作成する](#create-a-resource-group)するの例で作成されたリソース グループです。

```sql
ALTER USER usr2 RESOURCE GROUP rg2;
```

ユーザーをバインドすると、新しく作成されたセッションのリソース消費は、指定されたクォータ（リクエストユニット、RU）によって制御されます。システムのワークロードが比較的高く、余裕のある容量がない場合、 `usr2`のリソース消費率は、クォータを超えないように厳密に制御されます。 `usr1`は`rg1`によってバインドされ、 `BURSTABLE`が設定されているため、 `usr1`の消費率はクォータを超えることが許可されます。

リソースグループに必要なリソースが不足するほどリクエストが多すぎる場合、クライアントのリクエストは待機状態になります。待機時間が長すぎると、リクエストはエラーを報告します。

> **注記：**
>
> -   `CREATE USER`または`ALTER USER`を使用してユーザーをリソース グループにバインドすると、その設定はユーザーの既存のセッションには適用されず、ユーザーの新しいセッションにのみ適用されます。
> -   TiDB はクラスタ初期化時に`default`リソース グループを自動的に作成します。このリソース グループの`RU_PER_SEC`のデフォルト値は`UNLIMITED` ( `INT`型の最大値、つまり`2147483647`に相当) で、 `BURSTABLE`モードです。リソース グループにバインドされていないステートメントは、自動的にこのリソース グループにバインドされます。このリソース グループは削除をサポートしていませんが、RU の設定を変更することはできます。

リソース グループからユーザーのバインドを解除するには、次のようにしてユーザーを`default`グループに再度バインドするだけです。

```sql
ALTER USER 'usr3'@'%' RESOURCE GROUP `default`;
```

詳細については、 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)参照してください。

#### 現在のセッションをリソースグループにバインドする {#bind-the-current-session-to-a-resource-group}

[`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)ステートメントを使用すると、現在のセッションにバインドされているリソースグループを変更できます。セッションをリソースグループにバインドすると、対応するセッションのリソース使用量は、指定された使用量 (RU) によって制限されます。

システム変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820) `ON`に設定されている場合、このステートメントを実行するには`SUPER`または`RESOURCE_GROUP_ADMIN`または`RESOURCE_GROUP_USER`の権限が必要です。

次の例では、現在のセッションをリソースグループ`rg1`にバインドします。

```sql
SET RESOURCE GROUP rg1;
```

#### 現在のステートメントをリソースグループにバインドします。 {#bind-the-current-statement-to-a-resource-group}

SQL ステートメントに[`RESOURCE_GROUP(resource_group_name)`](/optimizer-hints.md#resource_groupresource_group_name)ヒントを追加することで、ステートメントがバインドされるリソース グループを指定できます。このヒントは`SELECT` 、 `INSERT` 、 `UPDATE` 、および`DELETE`ステートメントをサポートします。

システム変数[`tidb_resource_control_strict_mode`](/system-variables.md#tidb_resource_control_strict_mode-new-in-v820)が`ON`に設定されている場合、このヒントを使用するには`SUPER`または`RESOURCE_GROUP_ADMIN`または`RESOURCE_GROUP_USER`の権限が必要です。

次の例では、現在のステートメントをリソース グループ`rg1`にバインドします。

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

## リソース制御を無効にする {#disable-resource-control}

<CustomContent platform="tidb">

1.  リソース制御機能を無効にするには、次のステートメントを実行してください。

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2.  リソース グループの RU に基づくスケジューリングを無効にするには、TiKV パラメータ[`resource-control.enabled`](/tikv-configuration-file.md#resource-control)を`false`に設定します。

3.  TiFlashのリソース制御を無効にするには、 TiFlash構成項目[`enable_resource_control`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) `false`に設定します。

</CustomContent>

<CustomContent platform="tidb-cloud">

1.  リソース制御機能を無効にするには、次のステートメントを実行してください。

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2.  TiDB Self-Managed では、 `resource-control.enabled`パラメータを使用して、リソースグループのクォータに基づいてリクエストスケジューリングを使用するかどうかを制御できます。TiDB Cloudでは、 `resource-control.enabled`パラメータのデフォルト値は`true`であり、動的な変更はサポートされていません。TiDB Cloud Dedicatedクラスタでこれを無効にする必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

3.  TiDB Self-Managed では、 `enable_resource_control`設定項目を使用して、 TiFlashリソース制御を有効にするかどうかを制御できます。TiDB Cloudでは、 `enable_resource_control`パラメータのデフォルト値は`true`であり、動的な変更はサポートされていません。TiDB Cloud Dedicatedクラスタでこれを無効にする必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

## RU消費量を表示する {#view-ru-consumption}

RUの消費量に関する情報をご覧いただけます。

### SQLによるRU消費量を表示する {#view-the-ru-consumption-by-sql}

SQL文のRU消費量は、以下の方法で確認できます。

-   システム変数`tidb_last_query_info`
-   `EXPLAIN ANALYZE`
-   遅いクエリとそれに対応するシステムテーブル
-   `statements_summary`

#### システム変数<code>tidb_last_query_info</code>を照会することで、前回のSQL実行で消費されたRUを表示する。 {#view-the-rus-consumed-by-the-last-sql-execution-by-querying-the-system-variable-code-tidb-last-query-info-code}

TiDBはシステム変数[`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014)を提供します。このシステム変数には、最後に実行されたDMLステートメントの情報（SQL実行によって消費されたRUを含む）が記録されます。

例：

1.  `UPDATE`ステートメントを実行します。

    ```sql
    UPDATE sbtest.sbtest1 SET k = k + 1 WHERE id = 1;
    ```

        Query OK, 1 row affected (0.01 sec)
        Rows matched: 1  Changed: 1  Warnings: 0

2.  最後に実行されたステートメントの情報を表示するには、システム変数`tidb_last_query_info`照会します。

    ```sql
    SELECT @@tidb_last_query_info;
    ```

        +------------------------------------------------------------------------------------------------------------------------+
        | @@tidb_last_query_info                                                                                                 |
        +------------------------------------------------------------------------------------------------------------------------+
        | {"txn_scope":"global","start_ts":446809472210829315,"for_update_ts":446809472210829315,"ru_consumption":4.34885578125} |
        +------------------------------------------------------------------------------------------------------------------------+
        1 row in set (0.01 sec)

    結果として、 `ru_consumption`はこの SQL ステートメントの実行によって消費された RU です。

#### SQL実行中に消費されたRUを<code>EXPLAIN ANALYZE</code>で表示する {#view-rus-consumed-during-sql-execution-by-code-explain-analyze-code}

[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption)ステートメントを使用すると、SQL 実行中に消費される RU の量を取得できます。RU の量はキャッシュ (たとえば、[コプロセッサキャッシュ](/coprocessor-cache.md)) の影響を受けることに注意してください。同じ SQL を複数回実行すると、各実行で消費される RU の量は異なる場合があります。RU の値は各実行の正確な値を表すものではありませんが、推定の参考として使用できます。

#### 遅いクエリとそれに対応するシステムテーブル {#slow-queries-and-the-corresponding-system-table}

<CustomContent platform="tidb">

リソース制御を有効にすると、TiDB の[スロークエリログ](/identify-slow-queries.md)と対応するシステム テーブル[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)には、リソース グループ、対応する SQL の RU 消費量、および利用可能な RU を待機した時間が含まれます。

</CustomContent>

<CustomContent platform="tidb-cloud">

リソース制御を有効にすると、システムテーブル[`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)には、リソースグループ、対応するSQLのRU消費量、および利用可能なRUを待機した時間が格納されます。

</CustomContent>

#### RUの統計情報を<code>statements_summary</code>別に表示する {#view-ru-statistics-by-code-statements-summary-code}

TiDB のシステム テーブル[`INFORMATION_SCHEMA.statements_summary`](/statement-summary-tables.md#statements_summary)には、SQL ステートメントの正規化および集計された統計情報が格納されます。このシステム テーブルを使用すると、SQL ステートメントの実行パフォーマンスを表示および分析できます。また、リソース グループ名、RU 消費量、利用可能な RU の待機時間など、リソース制御に関する統計情報も含まれています。詳細については、 [`statements_summary`フィールドの説明](/statement-summary-tables.md#statements_summary-fields-description)を参照してください。 説明

### リソースグループのRU消費量を表示する {#view-the-ru-consumption-of-resource-groups}

バージョン7.6.0以降、TiDBは各リソースグループのRU消費量の履歴レコードを保存するためのシステムテーブル[`mysql.request_unit_by_group`](/mysql-schema/mysql-schema.md#system-tables-related-to-resource-control)を提供します。

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
> `mysql.request_unit_by_group`のデータは、TiDB のスケジュールされたタスクによって毎日終了時に自動的にインポートされます。特定の日にリソース グループの RU 消費量が 0 の場合、レコードは生成されません。デフォルトでは、このテーブルには過去 3 か月 (最大 92 日) のデータが格納されます。この期間を超えるデータは自動的にクリアされます。

## 指標とグラフのモニタリング {#monitoring-metrics-and-charts}

<CustomContent platform="tidb">

TiDB はリソース制御に関する実行時情報を定期的に収集し、Grafana の**[TiDB]** &gt; **[リソース制御]**ダッシュボードにメトリクスの視覚的なグラフを提供します。メトリクスについては[TiDBの重要な監視指標](/grafana-tidb-dashboard.md)の**「リソース制御**」セクションで詳しく説明されています。

TiKV は、さまざまなリソース グループからのリクエスト QPS も記録します。詳細については、 [TiKVモニタリング指標の詳細](/grafana-tikv-dashboard.md#grpc)を参照してください。

TiDB ダッシュボードの現在の[`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md)テーブルでリソース グループのデータを表示できます。詳しくは[リソースマネージャーページ](/dashboard/dashboard-resource-manager.md)をご覧ください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションは、TiDB Self-Managed にのみ適用されます。現在、 TiDB Cloudリソース制御メトリクスは提供されていません。

TiDBは、リソース制御に関するランタイム情報を定期的に収集し、Grafanaの**TiDB** &gt;**リソース制御**ダッシュボードでそのメトリクスの視覚的なグラフを提供します。

TiKVは、Grafanaの**TiKV**ダッシュボードに、さまざまなリソースグループからのリクエストQPSも記録します。

</CustomContent>

## ツールの互換性 {#tool-compatibility}

リソース制御機能は、データのインポート、エクスポート、およびその他のレプリケーションツールの通常の使用には影響しませんBR、 TiDB Lightning、およびTiCDCは現在、リソース制御に関連するDDL操作の処理をサポートしておらず、リソース消費はリソース制御によって制限されません。

## FAQ {#faq}

1.  リソースグループを使用しない場合、リソース制御を無効にする必要がありますか？

    いいえ。リソースグループを指定しないユーザーは、リソースが無制限の`default`リソースグループに自動的に割り当てられます。すべてのユーザーが`default`リソースグループに属している場合、リソース割り当て方法は、リソース制御が無効になっている場合と同じです。

2.  データベースユーザーは複数のリソースグループに紐付けられますか？

    いいえ。データベースユーザーは1つのリソースグループにしかバインドできません。ただし、セッション実行時には、 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)使用して、現在のセッションで使用するリソースグループを設定できます。また、オプティマイザヒント[`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name)を使用して、実行中のステートメントのリソースグループを設定することもできます。

3.  すべてのリソースグループの合計リソース割り当て（ `RU_PER_SEC` ）がシステム容量を超えた場合、どうなりますか？

    TiDB は、リソース グループを作成する際に容量を検証しません。システムに十分な利用可能なリソースがあれば、TiDB は各リソース グループのリソース要件を満たすことができます。システム リソースが制限を超えると、TiDB は優先度の高いリソース グループからの要求を満たすことを優先します。同じ優先度の要求すべてを満たすことができない場合、TiDB はリソース割り当て ( `RU_PER_SEC` ) に従ってリソースを比例的に割り当てます。

## 関連項目 {#see-also}

-   [リソースグループを作成する](/sql-statements/sql-statement-create-resource-group.md)
-   [アルター・リソース・グループ](/sql-statements/sql-statement-alter-resource-group.md)
-   [リソースグループを削除する](/sql-statements/sql-statement-drop-resource-group.md)
-   [リソースグループRFC](https://github.com/pingcap/tidb/blob/release-8.5/docs/design/2022-11-25-global-resource-control.md)

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="TiDB Admin Lab 5: Using Resource Control with Mixed Workloads" type="lab" link="https://labs.tidb.io/labs/demo_006" imgSrc="https://lab-static.pingcap.com/quick-demo/dba_303_ch05_en.png" duration="90 mins" />
</RelatedResources>
