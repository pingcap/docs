---
title: Back Up and Restore TiDB Cloud Premium Data
summary: TiDB Cloud Premiumインスタンスのバックアップと復元方法を学びましょう。
aliases: ['/ja/tidbcloud/restore-deleted-tidb-cluster']
---

# TiDB Cloud Premium データのバックアップと復元 {#back-up-and-restore-tidb-cloud-premium-data}

<CustomContent plan="premium">

このドキュメントでは、 TiDB Cloud Premiumインスタンス上のデータのバックアップと復元方法について説明します。TiDB Cloud Premiumは、自動バックアップと手動バックアップの両方をサポートしており、必要に応じてバックアップデータを新しいインスタンスに復元できます。

</CustomContent>

<CustomContent plan="byoc">

このドキュメントでは、{{{ .premium }}} または {{{ .byoc }}} インスタンス上のデータをバックアップおよび復元する方法について説明します。{{{ .premium }}} と {{{ .byoc }}} は、自動バックアップと手動バックアップの両方をサポートしており、必要に応じてバックアップデータを新しいインスタンスに復元できます。

</CustomContent>

バックアップファイルは、以下のソースから生成される可能性があります。

- アクティブな {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンス
- 削除された {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスのバックアップ用のごみ箱

> **Tip:**
>
> - TiDB Cloud Dedicatedクラスター上のデータをバックアップおよび復元する方法については、 [TiDB Cloud Dedicatedデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)復元」を参照してください。
> - TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのデータをバックアップおよび復元する方法については、 [TiDB Cloud StarterまたはEssentialデータのバックアップと復元](/tidb-cloud/backup-and-restore-serverless.md)を参照してください。

## バックアップページを確認する {#view-the-backup-page}

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページで、対象の{{{ .premium }}}<CustomContent plan="byoc">または{{{ .byoc }}}</CustomContent>インスタンスの名前をクリックすると、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2. 左側のナビゲーションペインで、 **Data** &gt; **Backup**をクリックします。

## 自動バックアップ {#automatic-backups}

<CustomContent plan="premium">

TiDB Cloud Premiumは、本番環境向けに強化された自動バックアップ機能を提供します。高頻度スナップショットとログバックアップを組み合わせることで、データの信頼性を確保します。

</CustomContent>

<CustomContent plan="byoc">

{{{ .premium }}} と {{{ .byoc }}} は、本番環境向けに強化された自動バックアップ機能を提供します。高頻度スナップショットとログバックアップを組み合わせることで、データの信頼性を確保します。

</CustomContent>

### 自動バックアップモード {#automatic-backup-modes}

**Backup Settings** で自動バックアップモードを選択できます。利用可能なバックアップの種類、保持期間、および料金モデルは、選択したモードによって異なります。

<CustomContent plan="premium">

| バックアップモード | サポートされるバックアップタイプ | 保持期間と復元オプション | 料金モデル |
| --- | --- | --- | --- |
| **Standard Bundle Mode** | <ul><li>PITR</li><li>時間単位のバックアップスナップショット</li><li>日次バックアップスナップショット</li></ul> | <ul><li>PITR: 7日間</li><li>時間単位スナップショット: 7日間</li><li>日次スナップショット: 33日間</li><li>日次スナップショットは UTC 00:00 に作成されます。</li></ul> | 増分データ量に基づきます。 |
| **Custom Retention Mode** | <ul><li>PITR</li><li>日次バックアップスナップショット</li></ul> | 保持期間は 3 日から 33 日まで設定できます。PITR と日次スナップショットには、設定した保持期間が適用されます。 | スナップショットサイズに保持期間を乗じて課金されます。各バックアップは個別のオブジェクトとして課金されます。 |

</CustomContent>

<CustomContent plan="byoc">

| バックアップモード | サポートされるバックアップタイプ | 保持期間と復元オプション |
| --- | --- | --- |
| **Standard Bundle Mode** | <ul><li>PITR</li><li>時間単位のバックアップスナップショット</li><li>日次バックアップスナップショット</li></ul> | <ul><li>PITR: 7日間</li><li>時間単位スナップショット: 7日間</li><li>日次スナップショット: 33日間</li><li>日次スナップショットは 00:00 UTC に作成されます。</li></ul> |
| **Custom Retention Mode** | <ul><li>PITR</li><li>日次バックアップスナップショット</li></ul> | 保持期間は 3 日から 33 日まで設定できます。PITR と日次スナップショットには、設定した保持期間が適用されます。 |

</CustomContent>

PITR を使用すると、保持期間内の任意の時点にデータを復元できます。スナップショットを使用すると、保持期間内にある特定の時間単位または日次のスナップショットからデータを復元できます。

### 自動バックアップを構成する {#configure-automatic-backups}

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページで、対象の {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンス名をクリックします。

2. 左側のナビゲーションペインで、**Data** > **Backup** をクリックします。

3. 右上隅で **...** をクリックし、**Backup Settings** をクリックします。

4. 自動バックアップモードを選択します。

    - **Standard Bundle Mode** は、PITR、時間単位のスナップショット、および日次スナップショットに対して事前定義された設定を使用します。
    - **Custom Retention Mode** では、自動バックアップの保持期間と日次バックアップ時刻を指定できます。

5. **Custom Retention Mode** を選択した場合は、以下の設定を構成します。それ以外の場合は、この手順をスキップします。

    - **Backup Retention**: 3 日から 33 日の保持期間を選択します。デフォルト値は 7 日です。
    - **Daily Backup Time**: 日次スナップショットの時刻を選択します。タイムゾーンはこの設定の横に表示されます。

6. **Overview** セクションを確認し、**Save** をクリックします。

    Overview には、選択したバックアップモードで有効になるバックアップの種類、対応する保持期間、および利用可能な復元オプションが表示されます。

<CustomContent plan="byoc">

> **Note:**
>
> [バックアップモードを切り替える](#switch-between-automatic-backup-modes)か、保持期間を短縮すると、TiDB Cloud は新しい保持期間より古い既存の自動バックアップを完全に削除する場合があります。この操作は元に戻せません。

</CustomContent>

<CustomContent plan="premium">

> **Note:**
>
> - Custom Retention Mode の料金は、スナップショットのサイズと保持期間に基づいて決まります。PITR はパブリックプレビュー期間中、一時的に無料です。詳細は [TiDB Cloud pricing](https://www.pingcap.com/tidb-cloud-premium-pricing-details) を参照してください。
> - [バックアップモードを切り替える](#switch-between-automatic-backup-modes) か、保持期間を短縮すると、TiDB Cloud は新しい保持期間より古い既存の自動バックアップを完全に削除する場合があります。この操作は元に戻せません。

</CustomContent>

### 自動バックアップモードを切り替える {#switch-between-automatic-backup-modes}

**Standard Bundle Mode** と **Custom Retention Mode** を切り替えるには、次の手順を実行します。

1. インスタンスの [**Backup**](#view-the-backup-page) ページに移動します。
2. 右上隅の **...** をクリックし、**Backup Settings** をクリックします。
3. 表示されたダイアログで、新しいモードを選択します。

    - **Custom Retention Mode** に切り替える場合は、バックアップ保持期間と毎日のバックアップ時刻を設定する必要があります。
    - **Standard Bundle Mode** に切り替える場合は、保持期間と毎日のバックアップ時刻が標準バンドルのデフォルト値にリセットされます。

4. **Overview** セクションで保持設定を確認し、**Save** をクリックします。

<CustomContent plan="premium">

変更を保存すると、以降の自動バックアップは、選択したモードの料金モデルに従って課金されます。

</CustomContent>

新しい保持期間が現在の保持期間より短い場合、確認ダイアログに、新しい保持期間を超えて古くなり完全に削除される自動バックアップが一覧表示されます。これらのバックアップが不要であることを確認したうえでのみ、この操作を確定してください。

### バックアップの保護 {#backup-protection}

データ損失を防ぎ、リカバリポイントを保持できるようにするため、TiDB Cloud はインスタンスの**最新の成功した自動バックアップ**を、その保持期間が終了するまで保護します。そのため、インスタンスが削除された後でも、この保護された最新バックアップを手動で削除することはできません。削除を試みると、コンソールには、そのバックアップは保護されており、有効期限が切れる前には削除できないことを説明するメッセージが表示されます。

### バックアップファイルを削除する {#delete-backup-files}

{{{ .premium }}}<CustomContent plan="byoc">または{{{ .byoc }}}</CustomContent>インスタンスの既存のバックアップファイルを削除するには、以下の手順を実行してください。

1. インスタンスの[**Backup**](#view-the-backup-page)ページに移動します。

2. 削除したいバックアップファイルを見つけて、 **[アクション]**列の**[...]** &gt; **[削除]**をクリックします。

    > **Note:**
    >
    > データ損失を防ぐため、TiDB Cloud はインスタンスの**最新の成功した自動バックアップ**を保護します。これを削除しようとすると、コンソールに、このバックアップは保護されており、有効期限が切れるまで削除できないことを説明するメッセージが表示されます。
    > TiDB Cloud で `Organization Owner` または `Project Owner` ロールを持っている場合は、最新の成功した自動バックアップ以外の自動バックアップ、または手動バックアップを削除できます。

## 手動バックアップ {#manual-backups}

<CustomContent plan="premium">

TiDB Cloud Premiumは、自動バックアップに加えて、手動バックアップもサポートしています。手動バックアップは、管理された確実な復元ポイントを提供します。システムアップグレード、重要なデータの削除、元に戻せないスキーマや構成の変更など、リスクの高い操作を実行する前に、手動バックアップを作成することを強くお勧めします。

</CustomContent>

<CustomContent plan="byoc">

自動バックアップに加えて、{{{ .premium }}} と {{{ .byoc }}} は手動バックアップもサポートしています。手動バックアップは、管理された確実な復元ポイントを提供します。システムアップグレード、重要なデータの削除、元に戻せないスキーマや設定の変更など、リスクの高い操作を実行する前に、手動バックアップを作成することを強くお勧めします。

</CustomContent>

### 主な特徴 {#key-characteristics}

- **保持と削除**：自動バックアップとは異なり、手動バックアップは保持ポリシーに基づいて自動的に削除されません。明示的に削除するまで保持されます。インスタンスを削除すると、その手動バックアップはごみ箱に移動し、手動で削除するまでそこに残ります。

- **Storage location**：手動バックアップは、TiDBが管理するクラウドストレージに保存されます。

- **コスト**：手動バックアップは、削除するまで保持されるため、追加料金が発生します。

- **制限事項**：手動バックアップは、ポイントインタイムリカバリ（PITR）や部分バックアップ（テーブルレベルまたはデータベースレベルのバックアップなど）をサポートしていません。手動バックアップを既存のインスタンスに復元することはできません。復元操作ごとに新しいインスタンスが作成されます。

- **権限**： `Organization Owner`と`Instance Manager`の両方が手動バックアップを作成できます。システム管理の手動バックアップを復元できるのは`Organization Owner`のみです。

### 手動バックアップを作成する {#create-a-manual-backup}

1. インスタンスの[**Backup**](#view-the-backup-page)ページに移動します。

2. 右上隅の**...**をクリックし、次に**Manual Backup**をクリックします。

3. 操作を確認してください。バックアップはTiDB Cloudに保存され、**バックアップリスト**に表示されます。

TiDB Cloudコンソールでは、外部ストレージの認証情報を入力することなく、手動バックアップを直接復元できます。

## 復元する {#restore}

TiDB Cloudは、偶発的なデータ損失や破損が発生した場合にデータを復旧するための復元機能を提供します。アクティブなインスタンスのバックアップ、またはごみ箱から削除されたインスタンスから復元できます。

### 復元モード {#restore-mode}

TiDB Cloudは、インスタンスのスナップショット復元と特定時点への復元をサポートしています。

- **Snapshot Restore**：特定のバックアップスナップショットからインスタンスを復元します。この方法は、自動バックアップと手動バックアップの両方の復元に使用できます。**Backup List**では、手動バックアップには**Manual**タイプと**Permanent**有効期限ステータスが表示されます。

- **Point-in-Time Restore**：インスタンスを特定の時点の状態に復元します。

    - Premium<CustomContent plan="byoc"> または BYOC</CustomContent> インスタンス：過去7日間の任意の時点に復元できますが、インスタンス作成時刻より前、または現在時刻の1分前より後の時点には復元できません。なお、手動バックアップではPITRはサポートされていません。

### 復元先 {#restore-destination}

TiDB Cloudは、新しいインスタンスへのデータ復元をサポートしています。

### 新しいTiDB Cloud Premium インスタンスに復元する {#restore-to-a-new-instance}

新しい {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスにデータを復元するには、以下の手順に従ってください。

1. インスタンスの[**Backup**](#view-the-backup-page)ページに移動します。

2. **Restore**をクリックしてください。

3. **Select Backup**ページで、使用する**Restore Mode**を選択します。特定のバックアップスナップショットから復元することも、特定の時点に復元することもできます。

     <SimpleTab>
     <div label="Snapshot Restore">

    選択したバックアップスナップショットから復元するには、次の手順を実行します。

    1. **Snapshot Restore**をクリックします。
    2. 復元元のバックアップスナップショットを選択してください。

    </div>
     <div label="Point-in-Time Restore">

    Premium<CustomContent plan="byoc"> または BYOC</CustomContent> インスタンスを特定の時点に復元するには、以下の手順を実行してください。

    1. **Point-in-Time Restore**をクリックします。
    2. 復元したい日時を選択してください。

    </div>
     </SimpleTab>

4. **Next**をクリックして、 **Restore to a New Instance**ページに進んでください。

5. 新しい {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスを復元用に構成します。手順は <CustomContent plan="premium">[{{{ .premium }}} インスタンスの作成](/tidb-cloud/premium/create-tidb-instance-premium.md)</CustomContent><CustomContent plan="byoc">[Create a {{{ .byoc }}} Instance](/tidb-cloud/byoc/create-tidb-instance-byoc.md)</CustomContent> を参照してください。

    <CustomContent plan="byoc">

    {{{ .byoc }}} の場合は、バックアップと同じクラウドプロバイダーおよびリージョンにあるアクティブなリソースプールを選択します。適切なリソースプールがない場合は、`Organization Owner` がインスタンスを復元する前に作成できます。その他のロールではリソースプールを作成できません。詳細については、[Create a Resource Pool](/tidb-cloud/byoc/create-resource-pool-byoc.md) を参照してください。

    </CustomContent>

    > **Note:**
    >
    > 新しいインスタンスは、デフォルトではバックアップと同じクラウドプロバイダーとリージョンを使用します。

6. **Restore**をクリックして復元プロセスを開始してください。

    復元処理が開始されると、インスタンスの状態は最初に**Creating**に変わります。作成が完了すると、 **Restoring**に変わります。復元が完了し、状態が**Available**に変わるまで、インスタンスは利用できません。

### ごみ箱から復元 {#restore-from-recycle-bin}

ごみ箱から削除した {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスを復元するには、以下の手順を実行してください。

1. [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、右上隅の**[...]**をクリックして、 **Recycle Bin**をクリックします。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2. **Recycle Bin**ページで、<CustomContent plan="premium">**Premium**</CustomContent><CustomContent plan="byoc">**BYOC**</CustomContent> タブをクリックして、<CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent> インスタンスのごみ箱に移動します。

3. 復元したい<CustomContent plan="premium">{{{ .premium }}}</CustomContent><CustomContent plan="byoc">{{{ .byoc }}}</CustomContent>インスタンスを見つけて、**>** ボタンをクリックし、そのインスタンスで利用可能なバックアップを展開します。

4. 復元したいバックアップの行で、 **...**をクリックし、次に**Restore**を選択します。

5. **Restore**ページで、[新しいインスタンスに復元する](#restore-to-a-new-instance)と同じ手順に従って、バックアップを新しいインスタンスに復元します。

<CustomContent plan="premium">

### 別のプランタイプからバックアップを復元する {#restore-backups-from-a-different-plan-type}

現在、AWS上でホストされているTiDB Cloud Dedicatedクラスタから新しいTiDB Cloud Premiumインスタンスへのバックアップ復元のみが可能です。

TiDB Cloud Dedicatedクラスターによって生成されたバックアップを復元するには、次の手順に従ってください。

1. [TiDB Cloudコンソール](https://tidbcloud.com)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。右上隅にある**[...]**をクリックし、 **Restore from Another Plan**をクリックします。

2. **Select Backup**ページで、対象のTiDB Cloud Dedicatedクラスターを含むプロジェクトを選択します。TiDB Cloud Dedicatedクラスターを選択し、復元するバックアップ スナップショットを選択して、 **Next**をクリックします。

    > **Note:**
    >
    > - バックアップスナップショットを含むTiDB Cloud Dedicatedクラスターが、選択したプロジェクト内で**Active**または**Deleted**のいずれかの状態になっていることを確認してください。
    > - スナップショットは、 TiDB Cloud Premiumがサポートするリージョン内に配置する必要があります。リージョンがサポートされていない場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してTiDB Cloud Premium用の新しいリージョンを開設するか、別のバックアップスナップショットを選択してください。

3. **Restore**ページで、[新しいインスタンスに復元する](#restore-to-a-new-instance)と同じ手順に従って、バックアップを新しいインスタンスに復元します。

</CustomContent>

### クラウドストレージからバックアップを復元する {#restore-backups-from-cloud-storage}

<CustomContent plan="premium">

{{{ .premium }}} は、クラウドストレージ（Amazon S3 や Alibaba Cloud Object Storage Service（OSS）など）から新しいインスタンスへのバックアップの復元をサポートしています。この機能は、{{{ .dedicated }}} クラスターまたは TiDB Self-Managed クラスターから生成されたバックアップと互換性があります。

</CustomContent>

<CustomContent plan="byoc">

{{{ .premium }}} と {{{ .byoc }}} は、クラウドストレージ（Amazon S3 など）から新しいインスタンスへのバックアップの復元をサポートしています。この機能は、{{{ .dedicated }}} クラスターまたは TiDB Self-Managed クラスターから生成されたバックアップと互換性があります。

</CustomContent>

<CustomContent plan="premium">

> **Note:**
>
> - 現在、復元対象としてサポートされているのは、**Amazon S3** および **Alibaba Cloud OSS** に保存されているバックアップのみです。
> - バックアップの復元は、ストレージバケットと同じクラウドプロバイダーがホストする新しいインスタンスにのみ可能です。
> - インスタンスとストレージバケットが異なるリージョンに配置されている場合、リージョン間データ転送料金が別途発生する可能性があります。

</CustomContent>

<CustomContent plan="byoc">

> **Note:**
>
> - 現在、復元対象としてサポートされているのは、**Amazon S3** に保存されているバックアップのみです。
> - バックアップの復元は、ストレージバケットと同じクラウドプロバイダーがホストする新しいインスタンスにのみ可能です。
> - インスタンスとストレージバケットが異なるリージョンに配置されている場合、リージョン間データ転送料金が別途発生する可能性があります。

</CustomContent>

#### 手順 {#steps}

開始する前に、バックアップファイルにアクセスするための十分な権限を持つアクセスキーとシークレットキーを用意してください。

クラウドストレージからバックアップを復元するには、以下の手順を実行してください。

1. [TiDB Cloudコンソール](https://tidbcloud.com)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。右上隅にある**...**をクリックし、**Restore from Cloud Storage**をクリックします。

2. **Select Backup Storage Location**ページで、以下の情報を入力してください。

    <CustomContent plan="premium">

    - **Cloud Provider**：バックアップファイルが保存されているクラウドプロバイダーを選択してください。
    - **Region**：クラウドプロバイダーがAlibaba Cloud OSSの場合は、リージョンを選択してください。
    - **Backup Files URI**：バックアップファイルが格納されている最上位フォルダのURIを入力してください。
    - **Access Key ID**：アクセスキーIDを入力してください。
    - **Access Key Secret**：アクセスキーシークレットを入力してください。

    </CustomContent>

    <CustomContent plan="byoc">

    - **Cloud Provider**：バックアップファイルが保存されているクラウドプロバイダーを選択してください。
    - **Backup Files URI**：バックアップファイルが格納されている最上位フォルダのURIを入力してください。
    - **Access Key ID**：アクセスキーIDを入力してください。
    - **Access Key Secret**：アクセスキーシークレットを入力してください。

    </CustomContent>

    > **Tip:**
    >
    > ストレージバケットのアクセスキーを作成するには、[AWSアクセスキーを使用してAmazon S3へのアクセスを設定する](#configure-amazon-s3-access-using-an-aws-access-key)<CustomContent plan="premium">および[Alibaba Cloud OSSへのアクセスを設定する](#configure-alibaba-cloud-oss-access)</CustomContent>を参照してください。

3. **Verify Backup and Next**をクリックします。

4. 検証が成功すると、**Restore to a New Instance**ページが表示されます。ページ上部に表示されるバックアップ情報を確認し、<CustomContent plan="premium">[{{{ .premium }}} インスタンスの作成](/tidb-cloud/premium/create-tidb-instance-premium.md)</CustomContent><CustomContent plan="byoc">[Create a {{{ .byoc }}} Instance](/tidb-cloud/byoc/create-tidb-instance-byoc.md)</CustomContent>の手順に従って、バックアップを新しいインスタンスに復元します。

    <CustomContent plan="byoc">

    {{{ .byoc }}} では、対象のクラウドプロバイダーとリージョンに一致するアクティブなリソースプールを選択してください。適切なリソースプールがない場合は、`Organization Owner` がインスタンスを復元する前に作成できます。その他のロールではリソースプールを作成できません。詳細については、[Create a Resource Pool](/tidb-cloud/byoc/create-resource-pool-byoc.md)を参照してください。

    </CustomContent>

    バックアップ情報が正しくない場合は、**Previous**をクリックして前のページに戻り、正しい情報を入力してください。

5. バックアップを復元するには、**Restore**をクリックします。

## リファレンス {#references}

このセクションでは、Amazon S3<CustomContent plan="premium">とAlibaba Cloud OSS</CustomContent>へのアクセス設定方法について説明します。

### AWSアクセスキーを使用してAmazon S3へのアクセスを設定する {#configure-amazon-s3-access-using-an-aws-access-key}

アクセスキーを作成する際は、AWSアカウントのルートユーザーではなく、 IAMユーザーを使用することをお勧めします。

アクセスキーを設定するには、以下の手順に従ってください。

1. IAMユーザーとアクセスキーを作成します。

    1. IAMユーザーを作成します。詳細については、 [AWSアカウントにIAMユーザーを作成する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)を参照してください。
    2. AWSアカウントIDまたはアカウントエイリアス、およびIAMユーザー名とパスワードを使用して[IAMコンソール](https://console.aws.amazon.com/iam)にサインインしてください。
    3. アクセスキーを作成します。詳細については、 [IAMユーザーのアクセスキーを管理する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)を参照してください。

2. IAMユーザーに権限を付与します。

    タスクに必要な権限のみを含むポリシーを作成し、それをIAMユーザーにアタッチします。{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスにデータを復元するには、`s3:GetObject`、`s3:GetBucketLocation`、および `s3:ListBucket` 権限を付与します。

    以下は、 TiDB CloudがAmazon S3バケット内の特定のフォルダからデータを復元できるようにするポリシーの例です。

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowGetBucketLocation",
                "Effect": "Allow",
                "Action": "s3:GetBucketLocation",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>"
            },
            {
                "Sid": "AllowListPrefix",
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>",
                "Condition": {
                    "StringLike": {
                        "s3:prefix": "<Your backup folder>/*"
                    }
                }
            },
            {
                "Sid": "AllowReadObjectsInPrefix",
                "Effect": "Allow",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::<Your S3 bucket name>/<Your backup folder>/*"
            }
        ]
    }
    ```

    上記のポリシーにおいて、 `<Your S3 bucket name>`と`<Your backup folder>`を実際のバケット名とバックアップディレクトリに置き換えてください。この構成は、必要なバックアップファイルのみにアクセスを制限することで、最小権限の原則に従っています。

> **Note:**
>
> TiDB Cloudはアクセス キーを保存しません。セキュリティを維持するため、インポートまたはエクスポートのタスクが完了した後[アクセスキーを削除する](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

<CustomContent plan="premium">

### Alibaba Cloud OSSへのアクセスを設定する {#configure-alibaba-cloud-oss-access}

TiDB CloudにAlibaba Cloud OSSバケットへのアクセス権を付与するには、そのバケット用のAccessKeyペアを作成する必要があります。

AccessKeyペアを設定するには、以下の手順に従ってください。

1. RAMユーザーを作成し、AccessKeyペアを取得します。詳細については、[Create a RAM user](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-ram-user)を参照してください。

    **Access Mode** セクションで、**Using permanent AccessKey to access** を選択します。

2. 必要な権限を持つカスタムポリシーを作成します。詳細については、[Create custom policies](https://www.alibabacloud.com/help/en/ram/user-guide/create-a-custom-policy)を参照してください。

    - **Effect** セクションで、**Allow** を選択します。
    - **Service** セクションで、**Object Storage Service** を選択します。
    - **Action** セクションで、必要な権限を選択します。バックアップを {{{ .premium }}} インスタンスに復元するには、`oss:ListObjects` と `oss:GetObject` 権限を付与します。

        > **Tip:**
        >
        > 復元操作のセキュリティを強化するために、バケット全体へのアクセスを許可するのではなく、バックアップファイルが保存されている特定のフォルダー（`oss:Prefix`）へのアクセスに制限できます。

        以下の JSON の例は、復元タスク用のポリシーを示しています。このポリシーは、特定のバケットとバックアップフォルダーへのアクセスを制限します。

        ```json
        {
        "Version": "1",
        "Statement": [
            {
            "Effect": "Allow",
            "Action": "oss:ListObjects",
            "Resource": "acs:oss:*:*:<Your bucket name>",
            "Condition": {
                "StringLike": {
                "oss:Prefix": "<Your backup folder>/*"
                }
            }
            },
            {
            "Effect": "Allow",
            "Action": "oss:GetObject",
            "Resource": "acs:oss:*:*:<Your bucket name>/<Your backup folder>/*"
            }
        ]
        }
        ```

    - **Resource** セクションで、バケットと、そのバケット内の特定のオブジェクトを選択します。

3. カスタムポリシーをRAMユーザーにアタッチします。

    詳細については、[Grant permissions to a RAM user](https://www.alibabacloud.com/help/en/ram/user-guide/grant-permissions-to-the-ram-user)を参照してください。

</CustomContent>
