---
title: TiDB Cloud Lake へのシンク
summary: TiDB Cloud インスタンスから TiDB Cloud Lake にデータをレプリケートするデータパイプラインを作成、監視、管理する方法を学びます。
---

# TiDB Cloud Lake へのシンク

TiDB Cloud では、サードパーティの ETL ツールを使わずに、Data Pipeline を使用して <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> インスタンスから TiDB Cloud Lake に完全データと増分変更をレプリケートできます。まず、選択したソースデータの完全スナップショットをエクスポートし、その後は行の変更を継続的にレプリケートできるため、TiDB Cloud Lake 内のデータを最新の状態に保てます。

> **Note:**
>
> - TiDB Cloud Lake への Data Pipeline は現在、<CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> 向けに**プライベートプレビュー**として提供されており、リクエストベースでのみ利用できます。この機能をリクエストするには、[TiDB Cloud コンソール](https://tidbcloud.com)の右下にある **?** をクリックし、**Support Tickets** をクリックして [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals) に移動します。チケットを作成し、**Description** フィールドに "Apply for `Data Pipeline to TiDB Cloud Lake`" と入力して、**Submit** をクリックします。
> - Data Pipeline 機能は TiCDC をベースに構築されているため、[TiCDC と同じ制限](https://docs.pingcap.com/tidb/stable/ticdc-overview#unsupported-scenarios)があります。

## 制限事項 {#restrictions}

- TiDB Cloud Lake の Warehouse は、TiDB Cloud インスタンスと**同じリージョン**に存在する必要があります。
- 増分レプリケーションを行えるのは、**主キー**を持つテーブルのみです。主キーのないテーブルは、パイプライン作成時の **Filter results** パネルに表示されます。同期対象に含めた場合でも、それらの増分レプリケーションはスキップされます。
- <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> インスタンスごとに、最大 100 個の changefeed を作成できます。増分レプリケーションを含む各データパイプラインは、1 つの changefeed スロットを消費します。
- データパイプラインを削除しても、TiDB Cloud Lake にすでに書き込まれたデータや、Warehouse 内のターゲットデータベースおよびテーブルは**削除されません**。

## 前提条件 {#prerequisites}

開始する前に、以下を用意してください。

- <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> インスタンス。デプロイされているリージョンを確認しておいてください。
- インスタンスと同じリージョンにある TiDB Cloud Lake の Warehouse。まだない場合は、まず [TiDB Cloud Lake コンソール](https://lake.tidbcloud.com/) で作成してください。データパイプライン作成時に選択できるのは、インスタンスと同じリージョンの Warehouse のみです。
- 外部 stage バケット: Amazon S3 バケットまたは Alibaba Cloud OSS バケット。インスタンスと同じリージョンに作成してください。
- ソーステーブルを読み取れる TiDB データベースユーザーのユーザー名とパスワード。

## データパイプラインを作成する {#create-a-data-pipeline}

データパイプラインを作成するには、送信先、外部 stage、およびレプリケーション設定を構成する必要があります。

### ステップ 1. 送信先を設定する {#step-1-configure-the-destination}

1. [TiDB Cloud コンソール](https://tidbcloud.com/) で、対象の <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> インスタンスの概要ページに移動し、左側のナビゲーションペインで **Data** > **Data Pipeline** をクリックして、右上の **Create Data Pipeline** をクリックします。
2. **Destination** エリアで、以下のフィールドを設定します。

    - **Destination**: **TiDB Cloud Lake** を選択します。
    - **Warehouse**: ターゲットの Warehouse を選択します。表示されるのは、インスタンスと同じリージョンにある Warehouse のみです。利用可能な Warehouse がない場合は、まず [TiDB Cloud Lake](https://lake.tidbcloud.com/) で作成し、その後リストを更新してください。

3. （任意）**Database Prefix**、**Database Suffix**、**Table Prefix**、**Table Suffix** フィールドでターゲットの命名規則を設定します。デフォルトでは 4 つのフィールドはすべて空であり、この場合 TiDB Cloud Lake に作成されるデータベース名とテーブル名はソースと同じ名前を保持します。

    - データベース名: `<database prefix><source database name><database suffix>`
    - テーブル名: `<table prefix><source table name><table suffix>`

### ステップ 2. 外部 stage を設定する {#step-2-configure-the-external-stage}

外部 stage は、データパイプラインの両側をつなぐオブジェクトストレージです。TiDB Cloud はエクスポートしたスナップショットとキャプチャした行変更を stage に書き込み、TiDB Cloud Lake は stage からデータをロード (load) してターゲット Warehouse に取り込みます。詳細は、[データパイプラインで外部 stage が必要なのはなぜですか？](/tidb-cloud/data-pipeline-lake-faq.md#why-does-a-data-pipeline-require-an-external-stage) を参照してください。

TiDB Cloud Data Pipeline は、外部 stage として Amazon S3 および Alibaba Cloud OSS をサポートしています。バケットは <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> インスタンスと同じリージョンに作成し、先にクラウドプロバイダー側の設定を完了してください。設定手順はクラウドプロバイダーによって異なります。

<SimpleTab>
<div label="Amazon S3">

1. **External Stage** エリアで、S3 バケットの **Bucket URI** を `s3://<bucket-name>/<path-to-data>/` 形式で入力します。

    それ以外のフィールドは、いったん空のままにしてください。後続のセクションで説明するいずれかの方法でバケットアクセスを設定した後に入力します。

2. TiDB Cloud が外部 stage にデータを書き込み、TiDB Cloud Lake がそこからデータを読み取れるようにするには、**Bucket Access** エリアでバケットアクセスを設定します。以下のいずれかの方法を選択し、それに応じて認可を完了してください。

    - 方法 1: AWS Role ARN を使用する（推奨）

        1 つの IAM ロールを TiDB Cloud（stage への書き込み）と TiDB Cloud Lake（stage からの読み取り）で共有するため、認可設定は 1 回で済み、長期有効なアクセスキーを保存する必要もありません。TiDB Cloud が提供する CloudFormation テンプレートを使ってロールを作成することも、AWS で手動設定することもできます。

        AWS 側の完全な設定については、[TiDB Cloud Data Pipeline 用の外部 stage を設定する (AWS)](/tidb-cloud/data-pipeline-configure-external-stage-aws.md) を参照してください。ロールを作成したら、TiDB Cloud コンソールで `RoleARN` の出力値を **Role ARN** フィールドに貼り付け、SQS キューも作成した場合は、そのキュー URL を **SQS Queue URL** フィールドにコピーします。

    - 方法 2: AWS access key を使用する

        > **Note:**
        >
        > access key と secret key（AK/SK）を使用する場合、認証情報の管理とローテーションを手動で行う必要があり、セキュリティリスクが高まります。より強固なセキュリティのため、代わりに **AWS Role ARN** を使用してください。

        IAM ユーザー、その権限、および任意の SQS キューを含む AWS 側の完全な設定については、[Bucket Access with Access Key](/tidb-cloud/data-pipeline-configure-external-stage-aws.md#option-3-bucket-access-with-access-key-not-recommended) を参照してください。その後、TiDB Cloud コンソールで **AWS Access Key** を選択し、**Access Key ID** と **Secret Access Key** を入力します。

    選択した方法に必要な情報を入力したら、**Test Connection** をクリックして TiDB Cloud がバケットにアクセスできることを確認します。チェックに失敗した場合は、バケットのリージョンと、ロールまたは access key に付与した権限を確認してから、再度接続をテストしてください。

</div>

<div label="Alibaba Cloud OSS">

RAM ユーザー、その権限、および access key を含む OSS 側の完全な設定については、[TiDB Cloud Data Pipeline の External Stage を設定する (Alibaba Cloud)](/tidb-cloud/data-pipeline-configure-external-stage-alibaba-cloud.md) を参照してください。

1. **External Stage** エリアで、OSS バケットの **Bucket URI** を `oss://<bucket-name>/<path-to-data>/` 形式で入力します。
2. 以下のフィールドを入力します。

    - **Access Key ID**: RAM ユーザーの AccessKey ID。
    - **Access Key Secret**: RAM ユーザーの AccessKey Secret。

3. **Test Connection** をクリックして、TiDB Cloud がバケットにアクセスできることを確認します。チェックに失敗した場合は、バケットのリージョンと、RAM ユーザーに付与した権限を確認してから、再度接続をテストしてください。

> **Note:**
>
> Alibaba Cloud OSS では、access key 認証のみがサポートされており、SQS を使用したイベント駆動の取り込みは利用できません。

</div>

</SimpleTab>

### ステップ 3. レプリケーションを設定する {#step-3-configure-replication}

**Replication Data** エリアで、データのレプリケーション方法を設定します。

1. **Sync Mode**: 同期モードを選択します。

    - **Full Data + Incremental Data**（デフォルト）: 選択したソースデータの完全スナップショットをエクスポートし、その後、行変更を継続的にレプリケートします。継続的な同期にはこのモードを推奨します。
    - **Full Data**: 選択したソースデータの完全スナップショットを 1 回だけエクスポートします。増分データはレプリケートされず、スナップショット取得後にソースで行われた変更は無視されます。

2. **Sync Interval**: データパイプラインのエンドツーエンドのレイテンシー目標です。changefeed の flush サイクルと TiDB Cloud Lake の polling サイクルの両方が、エンドツーエンドのレイテンシーに影響します。間隔を短くするとデータレイテンシーは減少しますが、クラウドストレージへの API 呼び出し回数は増加します。デフォルト値はコンソールに表示されます。

3. **Changefeed Capacity Units**: 増分レプリケーションに割り当てる処理能力で、サポートされる最大レプリケーションスループットとともに表示されます。たとえば、`2 CCUs (the maximum replication throughput is 5,000 rows/s)` のように表示されます。

    > **Note:**
    >
    > Changefeed Capacity Units は、データストリーミングに割り当てられる処理能力を表します。この設定は増分レプリケーションのパフォーマンスを構成します。同期モードとして **Full Data** を選択した場合、増分レプリケーションは実行されないため、CCU は消費されません。

4. **TiDB Username** と **TiDB Password**: TiDB データベースユーザーのユーザー名とパスワードを入力します。データパイプラインはこのアカウントを使用して完全スナップショットをエクスポートするため、このアカウントにはソーステーブルへの読み取り権限が必要です。増分の行変更は、changefeed によって別途キャプチャされます。

5. **Sync Objects**: レプリケートするオブジェクトを選択します。

    - **Customize**（デフォルト）: **Table Filter Rules** で明示的なルールを指定します。ルール構文は [TiCDC のテーブルフィルタールール](https://docs.pingcap.com/tidb/stable/ticdc-filter#table-filter) と同じです。デフォルトでは、1 つの `*.*` ルールですべての非システムテーブルをレプリケートします。**Filter results** パネルには、ルールに一致するデータベースとテーブルが表示されます。
    - **All**: すべてのデータベースのすべてのテーブルをレプリケートします。テーブルフィルタールールの設定は非表示になります。

    必要に応じて **Case-sensitive** を選択すると、フィルタールール内のデータベース名とテーブル名の一致判定で大文字と小文字を区別します。デフォルトでは、大文字と小文字は区別されません。

    > **Note:**
    >
    > 増分レプリケーションを行えるのは、主キーを持つテーブルのみです。主キーのないテーブルは **Filter results** パネルに別途表示され、増分レプリケーションではスキップされます。データパイプラインを作成する前にこれらのテーブルへ主キーを追加するか、`"!test.tbl1"` のようなフィルタールールで除外してください。

6. **Pipeline Name**: データパイプラインの名前を入力します。

7. **Create** をクリックします。

    完全スナップショットのエクスポート中、パイプラインは **Creating** 状態になります。**Full Data + Incremental Data** の場合、増分レプリケーションが開始されるとステータスは **Running** に変わります。

## データパイプラインを管理する {#manage-the-data-pipeline}

### データパイプラインを編集する {#edit-a-data-pipeline}

データパイプラインを編集するには、対象の <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> インスタンスの **Data Pipeline** に移動し、対象パイプラインの行にある **...** をクリックして、**Edit** をクリックします。

データパイプラインが `Running` の間は編集できません。まずパイプラインを一時停止し、その後編集して、変更を適用するために再開してください。

送信先タイプと同期モードは、パイプライン作成後に変更できません。

> **Note:**
>
> テーブルフィルタールールの変更は、以後の増分データにのみ影響します。
>
> - 新しいルールで除外されたテーブルには、以後増分データは取り込まれません。すでに書き込まれたデータは保持されます。
> - 新しいルールで追加されたテーブルには、増分データのみが取り込まれます。過去データのバックフィルは行われません。

### データパイプラインを一時停止および再開する {#pause-and-resume-a-data-pipeline}

- **Pause**: データレプリケーションを停止し、パイプラインを `Paused` としてマークします。データが失われることはなく、レプリケーションの進行状況も保持されます。パイプラインの作成中または完全スナップショットのエクスポート中は、一時停止できません。
- **Resume**: 一時停止した位置からレプリケーションを再開します。これには TiDB Cloud Lake への取り込みも含まれます。

データパイプラインを一時停止または再開するには、対象の <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> インスタンスの **Data Pipeline** に移動し、対象パイプラインの行にある **...** をクリックして、**Pause** または **Resume** をクリックします。

### データパイプラインを削除する {#delete-a-data-pipeline}

データパイプラインを削除するには、次の手順を実行します。

1. 対象の <CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> インスタンスの **Data Pipeline** に移動し、対象パイプラインの行にある **...** をクリックして、**Delete** をクリックします。
2. 警告を読み、操作を確認します。データパイプラインを削除すると、次のことが行われます。

    - すべてのデータレプリケーションが即座に停止します。
    - パイプラインに関連付けられた TiDB Cloud Lake のデータソースと統合タスクの削除を試みます。削除に失敗した場合、これらのリソースが残り、手動でのクリーンアップが必要になることがあります。
    - TiDB Cloud Lake にすでに書き込まれたデータは**削除されません**。
    - Warehouse 内のターゲットデータベースまたはテーブルは**削除されません**。

この操作は元に戻せません。

## 関連情報 {#see-also}

- Data Pipeline に関するよくある質問については、[Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md) を参照してください。
- DDL、DML、およびカラム型のサポートの詳細については、[TiDB Cloud Lake 向け Data Pipeline SQL 互換性](/tidb-cloud/data-pipeline-lake-sql-compatibility.md) を参照してください。