---
title: Table-Level Data Affinity
summary: テーブルまたはパーティションのアフィニティ制約を構成してリージョンレプリカの分散を制御する方法と、スケジュールステータスを表示する方法について説明します。
---

# テーブルレベルのデータアフィニティ<span class="version-mark">（v8.5.5 の新機能）</span> {#table-level-data-affinity-span-class-version-mark-new-in-v8-5-5-span}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

テーブルレベルのデータアフィニティは、テーブルレベルでデータ分散をスケジュールするためのPDメカニズムです。このメカニズムは、同じテーブルまたはパーティションのリージョンのLeaderとボーターレプリカがTiKVクラスター全体にどのように分散されるかを制御します。

PDアフィニティスケジューリングを有効にし、テーブルの`AFFINITY`オプションを`table`または`partition`に設定すると、PDは同じテーブルまたはパーティションに属するリージョンを同じアフィニティグループにグループ化します。スケジューリング中、PDはこれらのリージョンのLeaderとボーターレプリカを、少数のTiKVノードの同じサブセットに配置することを優先します。これにより、クエリ中のノード間アクセスによって発生するネットワークレイテンシーが削減され、クエリパフォーマンスが向上します。

## 制限事項 {#limitations}

テーブル レベルのデータ アフィニティを使用する前に、次の制限に注意してください。

-   この機能は[PDマイクロサービスモード](/pd-microservices.md)では有効になりません。
-   この機能は[一時テーブル](/temporary-tables.md)および[ビュー](/views.md)では動作しません。
-   [パーティションテーブル](/partitioned-table.md)データアフィニティが設定されると、**パーティションの追加、削除、再編成、スワップなど、テーブルのパーティション構成の変更はサポートされなくなります**。パーティション構成を変更するには、まずそのテーブルのアフィニティ設定を削除する必要があります。
-   **大容量データを扱う場合、ディスク容量を事前に評価してください**。アフィニティを有効にすると、PDはテーブルまたはパーティションのリージョンを、少数のTiKVノードの同じサブセットに優先的にスケジュールします。データ量の多いテーブルやパーティションの場合、これによりこれらのノードのディスク使用量が大幅に増加する可能性があります。事前にディスク容量を評価し、監視することをお勧めします。
-   データアフィニティは、Leaderとボーターレプリカの分散にのみ影響します。テーブルにLearnerレプリカ（ TiFlashなど）がある場合、それらの分散はアフィニティ設定の影響を受けません。

## 前提条件 {#prerequisites}

PDアフィニティスケジューリングはデフォルトで無効になっています。テーブルまたはパーティションのアフィニティを設定する前に、この機能を有効にして設定する必要があります。

1.  アフィニティ スケジューリングを有効にするには、PD 構成項目[`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-new-in-v855) `0`より大きい値に設定します。

    たとえば、次のコマンドは値を`4`に設定し、PD が最大 4 つのアフィニティ スケジューリング タスクを同時に実行できるようにします。

    ```bash
    pd-ctl config set schedule.affinity-schedule-limit 4
    ```

2.  （オプション）必要に応じてPD設定項目[`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-new-in-v855)を変更します。デフォルト値は`256`です。これは、同じアフィニティグループ内の隣接する小さなリージョンを自動的にマージするためのサイズしきい値を制御します。5に設定すると`0`アフィニティグループ内の隣接する小さなリージョンの自動マージが無効になります。

## 使用法 {#usage}

このセクションでは、テーブルまたはパーティションのアフィニティを構成する方法と、アフィニティのスケジュール状態を表示する方法について説明します。

### テーブルまたはパーティションのアフィニティを構成する {#configure-table-or-partition-affinity}

`CREATE TABLE`または`ALTER TABLE`ステートメントの`AFFINITY`オプションを使用して、テーブルまたはパーティションのアフィニティを構成できます。

| 親和性レベル                            | 範囲                                                    | 効果                                                                                                                                                                                    |
| --------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AFFINITY='table'`                | パーティションテーブル                                           | テーブルのアフィニティを有効にします。PD はテーブルのすべてのリージョンに対して単一のアフィニティ グループを作成します。                                                                                                                        |
| `AFFINITY='partition'`            | パーティションテーブル                                           | テーブル内の各パーティションのアフィニティを有効にします。PDは各パーティションのリージョンごとに個別のアフィニティグループを作成します。例えば、4つのパーティションを持つテーブルの場合、PDは4つの独立したアフィニティグループを作成します。                                                             |
| `AFFINITY=''`または`AFFINITY='none'` | `AFFINITY='table'`または`AFFINITY='partition'`で構成されたテーブル | テーブルまたはパーティションのアフィニティを無効にします。アフィニティを無効にすると、PD は対象のテーブルまたはパーティションに対応するアフィニティグループを削除します。これにより、そのテーブルまたはパーティションのリージョンはアフィニティのスケジュール制約の対象外となります。TiKV の自動リージョン分割は、最大 10 分以内にデフォルトの動作に戻ります。 |

**例**

パーティションテーブルを作成するときにアフィニティを有効にします。

```sql
CREATE TABLE t1 (a INT) AFFINITY = 'table';
```

パーティションテーブルを作成するときに、各パーティションのアフィニティを有効にします。

```sql
CREATE TABLE tp1 (a INT)
  AFFINITY = 'partition'
  PARTITION BY HASH(a) PARTITIONS 4;
```

既存の非パーティションテーブルのアフィニティを有効にする:

```sql
CREATE TABLE t2 (a INT);
ALTER TABLE t2 AFFINITY = 'table';
```

テーブルアフィニティを無効にする:

```sql
ALTER TABLE t1 AFFINITY = '';
```

### アフィニティ情報をビュー {#view-affinity-information}

テーブルまたはパーティションのアフィニティ情報は、次の方法で表示できます。

-   [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md)番目のステートメントを実行します。3 `Status`の列には、アフィニティが有効になっているテーブルまたはパーティションと、それらのスケジュールステータスが表示されます。5 `Status`の列の値の意味は次のとおりです。

    -   `Pending` : リーダーまたは投票者がまだ決定されていない場合など、PD はテーブルまたはパーティションのアフィニティ スケジューリングを開始していません。
    -   `Preparing` : PD はアフィニティ要件を満たすように領域をスケジュールしています。
    -   `Stable` : すべてのリージョンが目標配布に到達しました。

-   [`INFORMATION_SCHEMA.TABLES`](/information-schema/information-schema-tables.md)テーブルをクエリし、 `TIDB_AFFINITY`列目でテーブルのアフィニティ レベルを確認します。

-   [`INFORMATION_SCHEMA.PARTITIONS`](/information-schema/information-schema-partitions.md)テーブルをクエリし、パーティションのアフィニティ レベルの`TIDB_AFFINITY`列を確認します。

## 注記 {#notes}

-   **リージョンの自動分割**：リージョンがアフィニティグループに属し、アフィニティが有効な場合、リージョンが過剰に作成されてアフィニティ効果が弱まるのを防ぐため、そのリージョンの自動分割はデフォルトで無効になっています。自動分割は、リージョンサイズが[`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-new-in-v855)の4倍を超えた場合にのみトリガーされます。TiKVまたはPD以外のコンポーネントによってトリガーされる分割（ [`SPLIT TABLE`](/sql-statements/sql-statement-split-region.md)によってトリガーされる手動分割など）には、この制限は適用されません。

-   **縮退および有効期限切れのメカニズム**：アフィニティグループ内の対象のリーダーまたは投票者をホストするTiKVノードが利用できなくなった場合（例えば、ノード障害やディスク容量不足など）、Leaderが排除された場合、または既存の配置ルールと競合した場合、PDはアフィニティグループを縮退状態としてマークします。縮退中は、対応するテーブルまたはパーティションのアフィニティスケジューリングが一時停止されます。

    -   影響を受けたノードが 10 分以内に回復した場合、PD は元のアフィニティ設定に基づいてスケジュールを再開します。
    -   影響を受けたノードが10分以内に回復しない場合、アフィニティグループは期限切れとしてマークされます。この時点で、PDは通常のスケジューリング動作を復元し（ [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md)の状態が`Pending`に戻ります）、アフィニティグループ内のリーダーと投票者を自動的に更新して、アフィニティスケジューリングを再度有効にします。

## 関連するステートメントと構成 {#related-statements-and-configurations}

-   [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)と[`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)の`AFFINITY`オプション
-   [`SHOW AFFINITY`](/sql-statements/sql-statement-show-affinity.md)
-   PD構成項目: [`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-new-in-v855)と[`schedule.max-affinity-merge-region-size`](/pd-configuration-file.md#max-affinity-merge-region-size-new-in-v855)
