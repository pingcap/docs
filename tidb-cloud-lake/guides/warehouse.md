---
title: Warehouses
summary: Warehouse は {{{ .lake }}} の重要なコンポーネントです。Warehouse は CPU、メモリ、ローカルキャッシュを含むコンピュートリソースのセットを表します。SQL タスクを実行するには Warehouse を実行する必要があります。
---

# Warehouses

Warehouse は {{{ .lake }}} の重要なコンポーネントです。Warehouse は CPU、メモリ、ローカルキャッシュを含むコンピュートリソースのセットを表します。次のような SQL タスクを実行するには、Warehouse を実行する必要があります。

- `SELECT` 文を使用したデータのクエリ
- `INSERT`、`UPDATE`、または `DELETE` 文を使用したデータの変更
- `COPY INTO` コマンドを使用したテーブルへのデータのロード (load)

Warehouse を実行すると費用が発生します。詳細は、[Warehouse の料金](/tidb-cloud-lake/guides/pricing-billing.md) を参照してください。

## Warehouse のサイズ {#warehouse-sizes}

{{{ .lake }}} では、Warehouse はさまざまなサイズで利用でき、それぞれが処理可能な同時クエリの最大数によって定義されます。Warehouse を作成する際は、次のサイズから選択できます。

| サイズ                | 推奨されるユースケース                                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| XSmall                | テストや軽いクエリの実行など、シンプルなタスクに最適です。小規模なデータセット（約 50GB）に適しています。                                      |
| Small                 | 定期レポートの実行や中程度のワークロードに適しています。中規模なデータセット（約 200GB）に適しています。                                       |
| Medium                | より複雑なクエリや高い同時実行性を扱うチームに最適です。より大きなデータセット（約 1TB）に適しています。                                       |
| Large                 | 多数の同時クエリを実行する組織に最適です。大規模なデータセット（約 5TB）に適しています。                                                       |
| XLarge                | 高い同時実行性を伴うエンタープライズ規模のワークロード向けに設計されています。非常に大規模なデータセット（10TB 超）に適しています。            |
| nXLarge               | n=2,3,4,5,6 [お問い合わせ](https://docs.pingcap.com/tidbcloud/tidb-cloud-support/?plan=lake)                                                   |
| Multi-Cluster Scaling | ワークロードに合わせて自動的にスケールアウトおよびスケールインし、ニーズに応じて同時実行性を向上させる最もコスト効率の高い方法を提供します。 |

適切な Warehouse サイズを選ぶには、{{{ .lake }}} ではまず小さいサイズから始めることを推奨しています。小さい Warehouse は、medium や large の Warehouse と比べて SQL タスクの実行に時間がかかる場合があります。クエリの実行に時間がかかりすぎる場合（たとえば数分かかる場合）は、より高速な結果を得るために medium または large の Warehouse へのスケールアップを検討してください。

## Warehouse の管理 {#managing-warehouses}

組織では必要な数だけ Warehouse を持つことができます。**Warehouses** ページには組織内のすべての Warehouse が表示され、それらを管理できます。Warehouse を作成または削除できるのは `account_admin` のみである点に注意してください。

> **Tip:**
>
> SQL コマンドを使用して Warehouse を管理することもできます。詳細は [Warehouse DDL コマンド](/tidb-cloud-lake/sql/warehouse-overview.md) を参照してください。

### Warehouse の一時停止 / 再開 {#suspending-resuming-warehouses}

一時停止された Warehouse はクレジットを消費しません。Warehouse 上の <svg t="1725236862433" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5243" width="16" height="16"><path d="M350 148h-56c-8.8 0-16 6.5-16 14.6v698.9c0 8 7.2 14.6 16 14.6h56c8.8 0 16-6.5 16-14.6V162.6c0-8.1-7.2-14.6-16-14.6zM730 148h-56c-8.8 0-16 6.5-16 14.6v698.9c0 8 7.2 14.6 16 14.6h56c8.8 0 16-6.5 16-14.6V162.6c0-8.1-7.2-14.6-16-14.6z" p-id="5244" fill="#1677FF"></path></svg> または <svg t="1725236570258" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4267" width="16" height="16"><path d="M213.333333 65.386667a85.333333 85.333333 0 0 1 43.904 12.16L859.370667 438.826667a85.333333 85.333333 0 0 1 0 146.346666L257.237333 946.453333A85.333333 85.333333 0 0 1 128 873.28V150.72a85.333333 85.333333 0 0 1 85.333333-85.333333z m0 64a21.333333 21.333333 0 0 0-21.184 18.837333L192 150.72v722.56a21.333333 21.333333 0 0 0 30.101333 19.456l2.197334-1.152L826.453333 530.282667a21.333333 21.333333 0 0 0 2.048-35.178667l-2.048-1.386667L224.298667 132.416A21.333333 21.333333 0 0 0 213.333333 129.386667z" fill="#1677FF" p-id="4268"></path></svg> ボタンをクリックすることで、手動で Warehouse を一時停止または再開できます。ただし、Warehouse は次のシナリオで自動的に一時停止または再開されることもあります。

- Warehouse は、auto-suspend 設定に基づき、アクティビティがない場合に自動的に一時停止できます。
- 一時停止中の Warehouse を選択して SQL タスクを実行すると、その Warehouse は自動的に再開されます。

### 一括操作の実行 {#performing-bulk-operations}

Warehouse に対して、一括再起動、一括一時停止、一括再開、一括削除などの一括操作を実行できます。これを行うには、Warehouse リスト内のチェックボックス <svg t="1725248447975" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4292" width="16" height="16"><path d="M896 0H128C57.6 0 0 57.6 0 128v768c0 70.4 57.6 128 128 128h768c70.4 0 128-57.6 128-128V128c0-70.4-57.6-128-128-128z m0 896H128V128h768v768z" p-id="4293" fill="#1677FF"></path></svg> をオンにして一括操作の対象となる Warehouse を選択し、その後、目的の操作に対応する省略記号ボタン <svg t="1722479222306" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2315" width="16" height="16"><path d="M213.333333 512a85.333333 85.333333 0 1 1-85.333333-85.333333 85.333333 85.333333 0 0 1 85.333333 85.333333z m298.666667-85.333333a85.333333 85.333333 0 1 0 85.333333 85.333333 85.333333 85.333333 0 0 0-85.333333-85.333333z m384 0a85.333333 85.333333 0 1 0 85.333333 85.333333 85.333333 85.333333 0 0 0-85.333333-85.333333z" fill="#1677FF" p-id="2316"></path></svg> をクリックします。

![Bulk operations](/media/tidb-cloud-lake/bulk.gif)

### Warehouse へのタグ付け {#tagging-warehouses}

Warehouse にタグを付けて整理および分類できます。たとえば、環境、チーム、またはコストセンターごとに分類できます。タグはキーと値のペアで、Warehouse リストに表示され、タグによるフィルタリングやソートが可能です。

**制約:**

- 1 つの Warehouse あたり最大 **10 個のタグ**
- キー: 最大 **128 文字**
- 値: 最大 **256 文字**

タグを追加するには、Warehouse の作成時または編集時に **Tags** セクションを展開し、キーと値のペアを入力します。

タグは Warehouse リストに `key: value` として表示され、キーまたは値で Warehouse をフィルタリングするために使用できます。

### ベストプラクティス {#best-practices}

Warehouse を効果的に管理し、最適なパフォーマンスとコスト効率を確保するために、次のベストプラクティスを検討してください。これらのガイドラインは、さまざまなワークロードや環境に合わせて Warehouse のサイズ設定、整理、微調整を行うのに役立ちます。

- **適切なサイズを選択する**

    - **development & testing** には、小さい Warehouse（XSmall、Small）を使用します。
    - **本番** には、大きい Warehouse（Medium、Large、XLarge）を選択します。

- **Warehouse を分離する**

    - **データロード** 用と **クエリ実行** 用で別々の Warehouse を使用します。
    - **development**、**testing**、**本番** 環境ごとに個別の Warehouse を作成します。

- **データロードのヒント**

    - 小さい Warehouse（Small、Medium）はデータロードに適しています。
    - パフォーマンス向上のために、ファイルサイズとファイル数を最適化します。

- **コストとパフォーマンスを最適化する**

    - クレジット使用量を最小限に抑えるため、`SELECT 1` のような単純なクエリの実行は避けます。
    - 個別の `INSERT` 文ではなく、一括ロード（`COPY`）を使用します。
    - 長時間実行されるクエリを監視し、最適化してパフォーマンスを向上させます。

- **Auto-Suspend**

    - Warehouse がアイドル状態のときにクレジットを節約するため、auto-suspend を有効にします。

- **頻繁なクエリでは Auto-Suspend を無効にする**

    - 頻繁または繰り返し実行されるクエリでは、キャッシュを維持して遅延を避けるため、Warehouse をアクティブな状態に保ちます。

- **Auto-Scaling を使用する（Business および Dedicated プランのみ）**

    - Multi-cluster scaling は、ワークロード需要に基づいてリソースを自動調整します。

- **使用状況を監視して調整する**
    - コストとパフォーマンスのバランスを取るため、Warehouse の使用状況を定期的に確認し、必要に応じてサイズを変更します。

## Warehouse アクセス制御 {#warehouse-access-control}

{{{ .lake }}} では、特定のロールを Warehouse に割り当てることで、ロールベースの制御により Warehouse へのアクセスを管理できます。これにより、そのロールを持つユーザーのみが Warehouse にアクセスできます。

> **Note:**
>
> Warehouse アクセス制御はデフォルトでは有効になっていません。有効にするには、**Support** > **Create New Ticket** に移動してリクエストを送信してください。

Warehouse にロールを割り当てるには、Warehouse の作成または変更時に **Advanced Options** で目的のロールを選択します。

![alt text](/media/tidb-cloud-lake/warehouse-role.png)

- 選択可能な [組み込みロール](/tidb-cloud-lake/guides/roles.md#built-in-roles) は 2 つあり、[CREATE ROLE](/tidb-cloud-lake/sql/create-role.md) コマンドを使用して追加のロールを作成することもできます。{{{ .lake }}} のロールの詳細については、[ロール](/tidb-cloud-lake/guides/roles.md) を参照してください。
- ロールが割り当てられていない Warehouse には、デフォルトで `public` ロールが適用され、すべてのユーザーがアクセスできます。
- [GRANT](/tidb-cloud-lake/sql/grant.md) コマンドを使用して、ユーザー（{{{ .lake }}} のログインメールまたは SQL ユーザー）にロールを付与できます。次の例では、メールアドレス `name@example.com` を持つユーザーに `manager` ロールを付与し、`manager` ロールが割り当てられた任意の Warehouse へのアクセスを許可します。

    ```sql title='Examples:'
    GRANT ROLE manager to 'name@example.com';
    ```

## Multi-Cluster Warehouse {#multi-cluster-warehouses}

Multi-cluster Warehouse は、ワークロード需要に応じてクラスターを追加または削除することで、コンピュートリソースを自動調整します。必要に応じてスケールアップまたはスケールダウンすることで、高い同時実行性とパフォーマンスを確保しつつ、コストを最適化します。

> **Note:**
>
> Multi-Cluster Warehouses はデフォルトでは有効になっていません。有効にするには、**Support** > **Create New Ticket** に移動してリクエストを送信してください。この機能は、Business および Dedicated プランの {{{ .lake }}} ユーザーのみが利用できます。 <!-- TO be confirmed -->

### 仕組み {#how-it-works}

デフォルトでは、Warehouse は単一のコンピュートリソースクラスターで構成され、そのサイズに応じて最大数の同時クエリを処理できます。Warehouse で Multi-Cluster を有効にすると、単一クラスターの容量を超えるワークロードに対応するため、複数のクラスター（**Max Clusters** 設定で定義）を動的に追加できるようになります。

同時クエリ数が Warehouse の容量を超えると、追加のクラスターが追加されて余分なロードを処理します。需要がさらに増え続ける場合は、クラスターが 1 つずつ追加されます。クエリ需要が減少すると、**Auto Suspend** の時間より長くアクティビティがないクラスターは自動的にシャットダウンされます。

![alt text](/media/tidb-cloud-lake/multi-cluster-how-it-works.png)

### Multi-Cluster の有効化 {#enabling-multi-cluster}

Warehouse の作成時に Multi-Cluster を有効にし、その Warehouse がスケールアップできるクラスターの最大数を設定できます。なお、Warehouse で Multi-Cluster が有効な場合、**Auto Suspend** の時間は少なくとも 15 分に設定する必要があります。

![alt text](/media/tidb-cloud-lake/multi-cluster.png)

### コスト計算 {#cost-calculation}

Multi-Cluster Warehouse は、特定の時間間隔において使用されたアクティブなクラスター数に基づいて課金されます。

たとえば、1 時間あたり $1.6 の XSmall Warehouse で、13:00 から 14:00 までは 1 つのクラスターがアクティブに使用され、14:00 から 15:00 までは 2 つのクラスターがアクティブに使用された場合、13:00 から 15:00 までに発生する合計コストは $4.8 です（(1 cluster × 1 hour × $1.6) + (2 clusters × 1 hour × $1.6)）。

## MySQL Endpoint {#mysql-endpoint}

MySQL Endpoint 機能により、Warehouse は Tableau、Grafana、その他の MySQL 互換クライアントなど、MySQL プロトコルのみをサポートする BI ツールやアプリケーションからの接続を受け入れられるようになります。

> **Note:**
>
> MySQL Endpoint はデフォルトでは有効になっていません。有効にするには、**Support** > **Create New Ticket** に移動してリクエストを送信してください。

### MySQL Endpoint の有効化 {#enabling-mysql-endpoint}

Warehouse の作成時、または後から変更する際に MySQL Endpoint を有効にできます。このオプションは **Advanced Options** セクションにトグルスイッチとして表示されます。

> **Warning:**
>
> MySQL Endpoint を有効にすると、その Warehouse では **Auto Suspend is automatically disabled**（0 に設定）されます。これは、Warehouse がアイドル時でも継続的に実行されたままとなり、コストが発生し続けることを意味します。使用計画を適切に立ててください。

### MySQL プロトコル経由での接続 {#connecting-via-mysql-protocol}

有効化すると、**Connect** ダイアログに表示される標準の MySQL 接続情報を使用して、任意の MySQL 互換クライアントから Warehouse に接続できます。これは、{{{ .lake }}} プロトコルをネイティブにサポートしていないツールとの統合に役立ちます。

## Warehouse への接続 {#connecting-to-a-warehouse}

Warehouse に接続すると、{{{ .lake }}} 内でクエリを実行しデータを分析するために必要なコンピュートリソースが提供されます。この接続は、アプリケーションや SQL クライアントから {{{ .lake }}} にアクセスする際に必要です。

### 接続方法 {#connection-methods}

{{{ .lake }}} は、特定のニーズに対応するために複数の接続方法をサポートしています。

#### SQL クライアントとツール {#sql-clients-tools}

| クライアント                                 | 種類            | 最適な用途                  | 主な機能                                              |
| ------------------------------------------ | --------------- | --------------------------- | ----------------------------------------------------- |
| **[LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md)** | コマンドライン    | 開発者、スクリプト          | ネイティブ CLI、豊富なフォーマット、複数のインストール方法 |

#### 開発者向けドライバー {#developer-drivers}

| 言語        | ドライバー          | ユースケース            | ドキュメント                                           |
| ----------- | ----------------- | ----------------------- | ------------------------------------------------------ |
| **Go**      | Golang Driver     | バックエンドアプリケーション | [Golang ガイド](/tidb-cloud-lake/guides/connect-using-golang.md) |
| **Python**  | Python Connector  | データサイエンス、分析  | [Python ガイド](/tidb-cloud-lake/guides/connect-using-python.md) |
| **Node.js** | JavaScript Driver | Webアプリケーション     | [Node.js ガイド](/tidb-cloud-lake/guides/connect-using-node-js.md) |
| **Java**    | JDBC Driver       | エンタープライズアプリケーション | [JDBC ガイド](/tidb-cloud-lake/guides/connect-using-java.md)     |
| **Rust**    | Rust Driver       | システムプログラミング  | [Rust ガイド](/tidb-cloud-lake/guides/connect-using-rust.md)     |

### 接続情報の取得 {#obtaining-connection-information}

Warehouse の接続情報を取得するには、次の手順を実行します。

1. **Overview** > **Connect** をクリックします。
2. 接続したい **Database** と **Warehouse** を選択します。選択内容に応じて接続情報が更新されます。
3. 接続の詳細には、`cloudapp` という SQL ユーザーとランダムに生成されたパスワードが含まれます。{{{ .lake }}} はこのパスワードを保存しません。必ずコピーして安全に保管してください。パスワードを忘れた場合は、**Reset** をクリックして新しいものを生成します（リセットには Admin 権限が必要です）。

### 接続文字列の形式 {#connection-string-format}

{{{ .lake }}} では、**Connect** をクリックすると接続文字列が自動生成されます。

```
lake://<username>:<password>@<tenant>.gw.<region>.default.tidbcloud.com:443/<database>?warehouse=<warehouse_name>
```

各項目の意味は次のとおりです。

- `<username>`: デフォルトは `cloudapp`
- `<password>`: **Reset** をクリックして表示または変更
- `<tenant>`, `<region>`: アカウント情報（接続の詳細に表示）
- `<database>`: 選択したデータベース（接続の詳細に表示）
- `<warehouse_name>`: 選択した Warehouse（接続の詳細に表示）

### Warehouse アクセス用 SQL ユーザーの作成 {#creating-sql-users-for-warehouse-access}

デフォルトの `cloudapp` ユーザーに加えて、セキュリティとアクセス制御を強化するために追加の SQL ユーザーを作成できます。

#### 例 1: すべてのデータベースへのフルアクセス {#example-1-full-access-across-all-databases}

すべてのデータベースに対する読み取り/書き込みアクセスをユーザーに付与します。これは、複数データベースにまたがる操作が必要な管理者アカウントや自動化パイプラインに適しています。

```sql
-- Create a role with global access
CREATE ROLE full_access_role;
GRANT ALL ON *.* TO ROLE full_access_role;

-- Create the user and assign the role
CREATE USER admin_user IDENTIFIED BY 'SecurePass456!' WITH DEFAULT_ROLE = 'full_access_role';
GRANT ROLE full_access_role TO admin_user;
```

#### 例 2: 単一データベースへのアクセス {#example-2-single-database-access}

特定の 1 つのデータベースのみにアクセスできるユーザーを付与します。

```sql
-- Create a role scoped to one database
CREATE ROLE warehouse_user1_role;
GRANT ALL ON my_database.* TO ROLE warehouse_user1_role;

-- Create a new SQL user and assign the role
CREATE USER warehouse_user1 IDENTIFIED BY 'StrongPassword123' WITH DEFAULT_ROLE = 'warehouse_user1_role';
GRANT ROLE warehouse_user1_role TO warehouse_user1;
```

#### 例 3: すべてのデータベースへの読み取り専用アクセス {#example-3-read-only-access-across-all-databases}

ユーザーがデータのクエリのみを実行すべきシナリオ（ダッシュボード、BI ツール、セーフモードの AI エージェントなど）向けです。

```sql
-- Create a read-only role
CREATE ROLE readonly_role;
GRANT SELECT ON *.* TO ROLE readonly_role;

-- Create the user
CREATE USER readonly_user IDENTIFIED BY 'ReadOnly789!' WITH DEFAULT_ROLE = 'readonly_role';
GRANT ROLE readonly_role TO readonly_user;
```

> **Tip:**
>
> {{{ .lake }}} では、`CREATE DATABASE` のような権限はユーザーに直接付与できず、ロールにのみ付与できます。必ず最初にロールを作成し、そのロールに権限を付与してから、ユーザーにそのロールを割り当ててください。

詳細については、[CREATE USER](/tidb-cloud-lake/sql/create-user.md) および [GRANT](/tidb-cloud-lake/sql/grant.md) のドキュメントを参照してください。

### 接続のセキュリティ {#connection-security}

{{{ .lake }}} の Warehouse へのすべての接続では、デフォルトで TLS 暗号化が使用されます。追加のセキュリティを必要とするエンタープライズユーザー向けに、VPC と {{{ .lake }}} の間にプライベート接続を確立するための [AWS PrivateLink](/tidb-cloud-lake/guides/connect-with-aws-privatelink.md) も利用できます。