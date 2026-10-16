---
title: Sink to MySQL
summary: このドキュメントでは、Sink to MySQL changefeed を使用してTiDB Cloudから MySQL へデータをストリーミングする方法について説明します。制限事項、前提条件、およびデータレプリケーション用の MySQL シンクを作成する手順が含まれています。このプロセスには、ネットワーク接続の設定、既存データの MySQL へのロード、および MySQL でのターゲットテーブルの作成が含まれます。前提条件を満たした後、ユーザーは MySQL シンクを作成してデータを MySQL にレプリケートできます。
---

# MySQLにシンクする {#sink-to-mysql}

このドキュメントでは、**Sink to MySQL** changefeedを使用してTiDB CloudからMySQLにデータをストリーミングする方法について説明します。

<CustomContent plan="dedicated">

> **Note:**
>
> 変更フィード機能を使用するには、 TiDB Cloud Dedicatedクラスタのバージョンがv6.1.3以降であることを確認してください。

</CustomContent>

## 制限 {#restrictions}

- <CustomContent plan="dedicated">{{{ .dedicated }}}クラスター</CustomContent><CustomContent plan="premium,byoc">{{{ .premium }}} または {{{ .byoc }}} インスタンス</CustomContent>ごとに、最大 100 個の変更フィードを作成できます。
- TiDB Cloud は TiCDC を使用して変更フィードを確立するため、[TiCDC と同じ制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)があります。
- 複製対象のテーブルに主キーまたは NULL を許容しない一意インデックスがない場合、複製中に一意制約が存在しないことで、一部の再試行シナリオにおいて、下流で重複データが挿入される可能性があります。

## 前提条件 {#prerequisites}

変更フィードを作成する前に、以下の前提条件を満たす必要があります。

- ネットワーク接続を設定する
- 既存データをエクスポートしてMySQLにロードする（オプション）
- 既存のデータをロードせず、増分データのみをMySQLに複製する場合は、MySQLに対応するターゲットテーブルを作成してください。

### ネットワーク {#network}

<CustomContent plan="dedicated">

{{{ .dedicated }}} クラスターが MySQL サービスに接続できることを確認してください。

<SimpleTab>
<div label="VPC Peering">

MySQL サービスがパブリックインターネットアクセスを持たない AWS VPC 内にある場合は、以下の手順を実行してください。

1. MySQL サービスの VPC と {{{ .dedicated }}} クラスターの間で [VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)。
2. MySQL サービスが関連付けられているセキュリティグループの受信ルールを変更します。

    [{{{ .dedicated }}} クラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) を受信ルールに追加する必要があります。これにより、{{{ .dedicated }}} クラスターから MySQL インスタンスにトラフィックが流れるようになります。

3. MySQL URL にホスト名が含まれている場合、TiDB Cloud が MySQL サービスの DNS ホスト名を解決できるようにする必要があります。

    1. [VPC ピアリング接続の DNS 解決を有効にする](https://docs.aws.amazon.com/vpc/latest/peering/modify-peering-connections.html#vpc-peering-dns) の手順に従います。
    2. **Accepter DNS resolution** オプションを有効にします。

MySQL サービスがパブリックインターネットアクセスを持たない Google Cloud VPC 内にある場合は、以下の手順を実行してください。

1. MySQL サービスが Google Cloud SQL の場合、Google Cloud SQL インスタンスに関連付けられた VPC に MySQL エンドポイントを公開する必要があります。Google が開発した [**Cloud SQL Auth proxy**](https://cloud.google.com/sql/docs/mysql/sql-proxy) を使用する必要がある場合があります。
2. MySQL サービスの VPC と {{{ .dedicated }}} クラスターの間で [VPC ピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)。
3. MySQL が配置されている VPC の受信ファイアウォールルールを変更します。

    [{{{ .dedicated }}} クラスターが配置されているリージョンの CIDR](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region) を受信ファイアウォールルールに追加する必要があります。これにより、{{{ .dedicated }}} クラスターから MySQL エンドポイントにトラフィックが流れるようになります。

</div>

<div label="Private Endpoint">

プライベートエンドポイントは、クラウドプロバイダーの **Private Link** または **Private Service Connect** 技術を活用し、VPC 内のリソースがプライベート IP アドレスを介して他の VPC 内のサービスに接続できるようにします。これにより、あたかもそれらのサービスが VPC 内で直接ホストされているかのように動作します。

プライベートエンドポイントを介して、{{{ .dedicated }}} クラスターを MySQL サービスに安全に接続できます。MySQL サービスでプライベートエンドポイントが利用できない場合は、[Changefeeds のプライベートエンドポイントを設定する](/tidb-cloud/set-up-sink-private-endpoint.md) に従って作成します。

</div>

</SimpleTab>

</CustomContent>

<CustomContent plan="premium,byoc">

{{{ .premium }}} または {{{ .byoc }}} インスタンスが MySQL サービスに接続できることを確認してください。

プライベートエンドポイントは、クラウドプロバイダーの **Private Link** または **Private Service Connect** 技術を活用し、VPC 内のリソースがプライベート IP アドレスを介して他の VPC 内のサービスに接続できるようにします。これにより、あたかもそれらのサービスが VPC 内で直接ホストされているかのように動作します。

プライベートエンドポイントを介して、{{{ .premium }}} または {{{ .byoc }}} インスタンスを MySQL サービスに安全に接続できます。MySQL サービスでプライベートエンドポイントが利用できない場合は、[Changefeeds用のプライベートエンドポイントを設定する](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md) に従って作成します。

</CustomContent>

### 既存データの読み込み（オプション） {#load-existing-data-optional}

<CustomContent plan="dedicated">

**Sink to MySQL** コネクタは、特定のタイムスタンプ以降の増分データのみを {{{ .dedicated }}} クラスターから MySQL にシンクできます。{{{ .dedicated }}} クラスターにすでにデータが存在する場合は、**Sink to MySQL** を有効にする前に、{{{ .dedicated }}} クラスターの既存データをエクスポートして MySQL にロードできます。

</CustomContent>
<CustomContent plan="premium,byoc">

**Sink to MySQL** コネクタは、特定のタイムスタンプ以降の増分データのみを {{{ .premium }}} または {{{ .byoc }}} インスタンスから MySQL にシンクできます。{{{ .premium }}} または {{{ .byoc }}} インスタンスにすでにデータが存在する場合は、**Sink to MySQL** を有効にする前に、既存データをエクスポートして MySQL にロードできます。

</CustomContent>

既存のデータを読み込むには：

1. [tidb_gc_life_time](https://docs.pingcap.com/tidb/stable/system-variables#tidb_gc_life_time-new-in-v50) を、以下の 2 つの操作の合計時間よりも長く延長して、その期間中の履歴データが TiDB によってガベージコレクションされないようにします。

    - 既存データのエクスポートとインポートにかかる時間
    - **Sink to MySQL** の作成にかかる時間

    例えば：

    {{< copyable "sql" >}}

    ```sql
    SET GLOBAL tidb_gc_life_time = '720h';
    ```

2. [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) を使用して <CustomContent plan="dedicated">{{{ .dedicated }}} クラスター</CustomContent><CustomContent plan="premium,byoc">{{{ .premium }}} または {{{ .byoc }}} インスタンス</CustomContent> からデータをエクスポートし、次に [mydumper/myloader](https://centminmod.com/mydumper.html) などのコミュニティツールを使用してデータを MySQL サービスにロードします。

3. [Dumpling のエクスポートファイル](https://docs.pingcap.com/tidb/stable/dumpling-overview#format-of-exported-files) のメタデータファイルから、MySQL シンクの開始位置を取得します。

    以下はメタデータファイルの例の一部です。`SHOW MASTER STATUS` の `Pos` は既存データの TSO であり、MySQL シンクの開始位置でもあります。

    ```
    Started dump at: 2020-11-10 10:40:19
    SHOW MASTER STATUS:
            Log: tidb-binlog
            Pos: 420747102018863124
    Finished dump at: 2020-11-10 10:40:20
    ```

### MySQLでターゲットテーブルを作成する {#create-target-tables-in-mysql}

既存のデータをロードしない場合は、TiDBからの増分データを保存するために、MySQLに該当するターゲットテーブルを手動で作成する必要があります。そうしないと、データは複製されません。

## MySQLシンクを作成する {#create-a-mysql-sink}

前提条件を満たしたら、データを MySQL にシンクできます。

1. ターゲットの <CustomContent plan="dedicated">{{{ .dedicated }}} クラスター</CustomContent><CustomContent plan="premium,byoc">{{{ .premium }}} または {{{ .byoc }}} インスタンス</CustomContent> の概要ページに移動し、左側のナビゲーションペインで **Data** > **Changefeed** をクリックします。

2. **Create Changefeed** をクリックし、**Destination** として **MySQL** を選択します。

3. **Connectivity Method** で、MySQL サービスへの接続方法を選択します。

    - **VPC Peering** または **Public IP** を選択した場合は、MySQL エンドポイントを入力します。
    - **Private Link** を選択した場合は、[ネットワーク](#network) セクションで作成したプライベートエンドポイントを選択し、MySQL サービスの MySQL ポートを入力します。

4. **Authentication** で、MySQL サービスの MySQL ユーザー名とパスワードを入力します。

5. **Next** をクリックして、TiDB が MySQL に正常に接続できるかどうかをテストします。

    - はいの場合、次の設定手順に進みます。
    - そうでない場合は、接続エラーが表示されるため、エラーに対処する必要があります。エラーが解決したら、もう一度 **Next** をクリックします。

6. **Table Filter** をカスタマイズして、複製するテーブルをフィルタリングします。ルールの構文については、[テーブルフィルター](/table-filter.md) を参照してください。

    - **Case Sensitive**: フィルタルールにおけるデータベース名とテーブル名の照合で、大文字小文字を区別するかどうかを設定できます。デフォルトでは、大文字小文字は区別されません。
    - **Filter Rules**: この列でフィルタルールを設定できます。デフォルトでは、すべてのテーブルを複製することを表すルール `*.*` があります。新しいルールを追加すると、TiDB Cloud は TiDB 内のすべてのテーブルをクエリし、右側のボックスにルールに一致するテーブルのみを表示します。フィルタルールは最大 100 個まで追加できます。
    - **Tables with valid keys**: この列には、主キーまたは一意インデックスを含む、有効なキーを持つテーブルが表示されます。
    - **Tables without valid keys**: この列には、主キーまたは一意キーがないテーブルが表示されます。これらのテーブルは、一意の識別子がないために下流で重複イベントを処理する際にデータの不整合が発生する可能性があり、複製中に課題となります。データの一貫性を確保するため、複製を開始する前に、これらのテーブルに一意キーまたは主キーを追加することを推奨します。あるいは、フィルタルールを追加してこれらのテーブルを除外することもできます。例えば、ルール `!test.tbl1` を使用してテーブル `test.tbl1` を除外できます。

7. **Event Filter** をカスタマイズして、複製するイベントをフィルタリングします。

    - **Tables matching**: この列では、イベントフィルターを適用するテーブルを設定できます。ルールの構文は、前の **Table Filter** 領域で使用されるものと同じです。変更フィードごとに最大 10 個のイベントフィルタールールを追加できます。
    - **Event Filter**: 以下のイベントフィルターを使用して、変更フィードから特定のイベントを除外できます。
        - **Ignore event**: 指定したイベントタイプを除外します。
        - **Ignore SQL**: 指定した式に一致する DDL イベントを除外します。例えば、`^drop` は `DROP` で始まるステートメントを除外し、`add column` は `ADD COLUMN` を含むステートメントを除外します。
        - **Ignore insert value expression**: 特定の条件を満たす `INSERT` ステートメントを除外します。例えば、`id >= 100` は、`id` が 100 以上である `INSERT` ステートメントを除外します。
        - **Ignore update new value expression**: 新しい値が指定した条件に一致する `UPDATE` ステートメントを除外します。例えば、`gender = 'male'` は、`gender` が `male` になる更新を除外します。
        - **Ignore update old value expression**: 古い値が指定した条件に一致する `UPDATE` ステートメントを除外します。例えば、`age < 18` は、`age` の古い値が 18 未満である更新を除外します。
        - **Ignore delete value expression**: 指定した条件を満たす `DELETE` ステートメントを除外します。例えば、`name = 'john'` は、`name` が `'john'` である `DELETE` ステートメントを除外します。

8. **Start Replication Position** で、MySQL シンクの開始位置を設定します。

    - Dumpling を使用して[既存のデータを読み込んだ](#load-existing-data-optional)場合は、**Start replication from a specific TSO** を選択し、Dumpling のエクスポートされたメタデータファイルから取得した TSO を入力します。
    - アップストリームの TiDB にデータがない場合は、**Start replication from now on** を選択します。
    - それ以外の場合は、**Start replication from a specific time** を選択して開始時点をカスタマイズできます。

9. **Next** をクリックして、変更フィードの仕様を設定します。

    - **Changefeed Specification** 領域で、変更フィードで使用する <CustomContent plan="dedicated">Replication Capacity Units (RCUs) の数</CustomContent><CustomContent plan="premium">Changefeed Capacity Units (CCUs) の数</CustomContent><CustomContent plan="byoc">TiCDC ノードのプロビジョニング済み vCPU</CustomContent> を設定します。
    - **Changefeed Name** 領域で、変更フィードの名前を指定します。

10. **Next** をクリックして、変更フィードの設定を確認します。

    すべての設定が正しいことを確認したら、クロスリージョンレプリケーションのコンプライアンスを確認し、**Create** をクリックします。

    設定を変更したい場合は、**Previous** をクリックして前の設定ページに戻ります。

11. シンクはまもなく開始され、シンクのステータスが **Creating** から **Running** に変わるのを確認できます。

    変更フィード名をクリックすると、チェックポイント、レプリケーションレイテンシー、その他のメトリクスなど、変更フィードの詳細を確認できます。

12. Dumpling を使用して[既存のデータを読み込んだ](#load-existing-data-optional)場合は、シンクの作成後に GC 時間を元の値（デフォルト値は `10m`）に戻す必要があります。

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_gc_life_time = '10m';
```
