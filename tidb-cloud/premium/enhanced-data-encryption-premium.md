---
title: Enhanced Data Encryption
summary: "{{{ .premium }}} インスタンス向けに Customer-Managed Encryption Key (CMEK) を登録し、Enhanced Data Encryption を有効にする方法を学びます。"
aliases: ['/ja/tidbcloud/dual-layer-data-encryption-premium']
---

# Enhanced Data Encryption

Enhanced Data Encryption は、クラウドプロバイダーのデフォルトのストレージレイヤー暗号化に加えてデータベースレイヤー暗号化を追加し、保存中の {{{ .premium }}} データベースデータおよびバックアップデータを保護します。Customer-Managed Encryption Key (CMEK) を使用すると、マスターキーの認可、ローテーション、ライフサイクルを自分のクラウドアカウント内で制御できます。

キーは TiDB Cloud 組織レベルで一度登録すれば、同じクラウドプロバイダーおよびリージョン内の {{{ .premium }}} インスタンス間で再利用できます。キーマテリアルはクラウド KMS 内に保持され、TiDB Cloud にはキー参照と、その認可、ステータス、使用状況を管理するために必要なメタデータのみが保存されます。

## 概要 {#overview}

| タスク | 開始場所 | 結果 |
| --- | --- | --- |
| [キーを登録して認可する](#register-a-key) | **Organization Settings** > **CMEK** | インスタンスで使用する前に、組織内でキーを登録して検証します。 |
| [暗号化を有効にする](#enable-enhanced-data-encryption) | インスタンス作成時、またはインスタンスの **Security** ページ | 同じクラウドプロバイダーおよびリージョン内で、登録済みキーを使用して CMEK を有効にします。 |
| [キーのステータスと使用状況を確認する](#view-encryption-and-key-status) | **Organization Settings** > **CMEK** | 登録済み各キーのステータスと、関連付けられたインスタンスおよびバックアップを表示します。 |
| [暗号化されたバックアップから復元する](#restore-from-an-encrypted-backup) | バックアップ復元フロー | 暗号化されたバックアップの復元に必要な CMEK を使用します。 |
| [未使用のキーを削除する](#remove-a-key) | **Organization Settings** > **CMEK** | すべての使用参照がクリアされた後、TiDB Cloud からキー登録を削除します。 |

## 始める前に {#before-you-begin}

- 対象の {{{ .premium }}} インスタンスと同じクラウドプロバイダーおよびリージョン内の AWS KMS または Alibaba Cloud KMS に対称暗号化キーを用意し、そのキーポリシーを更新する権限があることを確認してください。
    - AWS については、[Create a symmetric encryption KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/create-symmetric-cmk.html) を参照してください。
    - Alibaba Cloud については、[Understanding KMS keys](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/overview-of-key-management) を参照してください。また、Alibaba Cloud Resource Directory (Resource Sharing) を通じて KMS インスタンスを共有し、共有された TiDB Cloud アカウントに対して **Alibaba Cloud Gateway** を有効にできる必要があります。
- 必要な TiDB Cloud ロールを持っていることを確認してください。詳細は、[ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles) を参照してください。
    - **組織キーの管理と表示**（**Organization Settings** > **CMEK**）: `Organization Owner`
    - インスタンスの作成時、暗号化有効化時、または復元時に **登録済みキーを選択** する場合: そのリソース操作に必要なロール（`Organization Owner`、`Project Owner`、または `Instance Manager`）

## キーを登録する {#register-a-key}

任意の {{{ .premium }}} インスタンスを作成する前に、キーを登録して認可できます。キーを登録すると、そのキーが組織で利用可能になりますが、インスタンス上で暗号化が有効になるわけではありません。

1. [TiDB Cloud コンソール](https://tidbcloud.com)で対象の組織に切り替え、**Organization Settings** > **CMEK** に移動して、キーの追加を開始します。
2. クラウドプロバイダーとリージョンを選択し、生成されたすべての認可ステートメントをコピーします（Alibaba Cloud の場合は、表示される TiDB Cloud アカウントも控えてください）。
3. クラウドプロバイダーのコンソールでアクセスを設定します。

    - **AWS KMS**: 選択した対称キーのキーポリシーを開き、生成されたすべてのステートメントを既存の `Statement` 配列に追加します。生成された `Principal`、`Action`、`Condition` フィールドと、既存のキー管理用ステートメントはそのまま保持してください。詳細は、[Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html) を参照してください。
    - **Alibaba Cloud KMS**:
        1. Alibaba Cloud Resource Directory (Resource Sharing) で、TiDB Cloud コンソールに表示される TiDB Cloud アカウントと KMS インスタンスを共有します。
        2. 共有リストで、その TiDB Cloud アカウントに対して **Alibaba Cloud Gateway** を有効にします。
        3. 選択した対称キーのキーポリシーを開き、生成されたすべてのステートメントを既存の `Statement` 配列に追加します。このとき、既存のキー管理用ステートメントは保持してください。詳細は、[Manage Keys in Alibaba Cloud KMS](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/manage-keys-2) を参照してください。

    > **Warning:**
    >
    > 生成されたステートメントは、選択した KMS キーのキーポリシーに追加してください。キーポリシー全体を TiDB Cloud のステートメントだけで置き換えないでください。キーへの管理アクセスを失う可能性があります。

4. TiDB Cloud コンソールに戻り、キー ARN を入力してアクセスチェックを実行し、TiDB Cloud が必要な KMS 操作を実行できることを確認してから、キーを保存します。
5. **Organization Settings** > **CMEK** に、ステータス **Idle** でキーが表示されることを確認します。同じ組織、クラウドプロバイダー、リージョン内の対象インスタンスで、このキーを選択できるようになります。

## Enhanced Data Encryption を有効にする {#enable-enhanced-data-encryption}

Enhanced Data Encryption は、{{{ .premium }}} インスタンスの作成時、または既存インスタンスに対して有効にできます。一度有効にすると、CMEK を無効化したり、その場で別のキーに切り替えたりすることはできません。

登録済みキーを再利用する場合、クラウド KMS のキーポリシーに追加の変更は不要です。

### インスタンス作成時に暗号化を有効にする {#enable-encryption-during-instance-creation}

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページで **Create Resource** をクリックし、**Premium** を選択して、クラウドプロバイダーとリージョンを選びます。
2. **Enhanced Data Encryption** セクションで CMEK を有効にし、選択したクラウドプロバイダーおよびリージョン内の登録済みキーを選択します。
3. 適切なキーが登録されていない場合、`Organization Owner` は作成フローから **CMEK** ページを開いて（新しいタブで開きます）キーを登録し、その後インスタンス作成に戻って新しいキーを選択できます。
4. 残りの設定を完了し、**Create** をクリックします。TiDB Cloud は、CMEK を有効にする前にキーアクセスを検証します。

### 既存のインスタンスで暗号化を有効にする {#enable-encryption-for-an-existing-instance}

1. [TiDB Cloud コンソール](https://tidbcloud.com)で対象の {{{ .premium }}} インスタンスを開き、左側のナビゲーションペインで **Security** をクリックし、**Enhanced Data Encryption** セクションで **Enable** をクリックします。
2. インスタンスのクラウドプロバイダーおよびリージョン内の登録済みキーを選択します。適切なキーが登録されていない場合は、`Organization Owner` が先に **Organization Settings** > **CMEK** で登録できます。
3. 設定を確認し、有効化の完了後に暗号化ステータスを確認します。

## 暗号化とキーのステータスを確認する {#view-encryption-and-key-status}

- **インスタンスレベル**: インスタンスの **Overview** または **Security** ページを開き、Enhanced Data Encryption が有効かどうか、およびどの暗号化キーがインスタンスを保護しているかを確認します。
- **組織レベル**: **Organization Settings** > **CMEK** を開き（`Organization Owner` が必要）、登録済み各キーのステータス、クラウドプロバイダー、リージョン、および関連付けられたインスタンスとバックアップを確認します。

| Key status | Meaning and next action |
| --- | --- |
| **Verifying** | アクセスチェックを実行中です。検証が完了するまで待ってください。 |
| **Idle** | キーは登録および検証済みで、現在どのインスタンスやバックアップでも使用されていません。同じクラウドプロバイダーおよびリージョン内の対象インスタンスで選択できます。 |
| **Applied** | キーは現在、同じクラウドプロバイダーおよびリージョン内の 1 つ以上のインスタンスまたはバックアップで使用されており、他の対象インスタンスでも再利用できます。 |
| **Error** | キーが利用できないか、アクセス検証に失敗しました。クラウド KMS でキーの可用性または認可を復旧し、再度アクセスを検証してください。 |

## 登録済みキーを管理する {#manage-registered-keys}

### 利用できないキーに対処する {#handle-unavailable-keys}

登録済みキーが **Error** に変わった場合、またはアクセスに失敗した場合:

1. **Organization Settings** > **CMEK** で、影響を受けるキーとリソースを確認します。
2. クラウド KMS で、必要なキー状態、ポリシー、または（Alibaba Cloud の場合）KMS インスタンス共有と **Alibaba Cloud Gateway** の設定を復旧します。
3. キーが **Error** から回復したことを確認し、影響を受けたインスタンスまたは復元操作を確認します。

データベースはローカルデータ操作のために内部キーをメモリにキャッシュするため、CMEK を無効化または失効しても、進行中の操作に必ずしも直ちに影響するわけではありません。データベースは、保護されたキーをアンラップするために次回 KMS を呼び出す必要が生じるまで、キャッシュされたキーを使い続ける可能性があります。同じ CMEK を使用するすべてのインスタンスとバックアップは、この可用性への依存関係を共有します。

### キーを削除する {#remove-a-key}

1. **Organization Settings** > **CMEK** で、キーに関連付けられたインスタンスとバックアップスナップショットを確認します。
2. キー登録を削除します。いずれかのインスタンス、バックアップスナップショット、または進行中の復元がそのキーに依存している間は、キーのステータスが **Error** であっても、TiDB Cloud は削除をブロックします。
3. 削除がブロックされる場合は、まず依存するすべてのリソースを解消してから、再試行して削除を確認します。

> **Note:**
>
> TiDB Cloud でキー登録を削除しても、クラウド KMS 内のキーやそのポリシーが削除、無効化、変更されることはありません。データまたはバックアップのいずれかがそのキーを必要とする限り、クラウド KMS 内でキーとその認可を維持してください。

## 暗号化されたバックアップから復元する {#restore-from-an-encrypted-backup}

{{{ .premium }}} バックアップを復元する際、TiDB Cloud はその暗号化メタデータを確認し、対象リージョンで対応するキー要件を適用します。

| バックアップ暗号化の状態 | 復元時の動作と必要なアクション |
| --- | --- |
| CMEK で暗号化されており、ソースキーが登録済みかつ利用可能 | TiDB Cloud はソースキーを照合します。内容を確認して続行してください。復元されたインスタンスは同じキーを使用します。 |
| CMEK で暗号化されているが、ソースキーが未登録 | 続行する前に、`Organization Owner` が元のキーを登録して認可する必要があります。別のキーで {{{ .premium }}} バックアップを復号することはできません。 |
| CMEK で暗号化されており、ソースキーが **Error** 状態 | クラウド KMS でキーの可用性を復旧するか認可を修正し、アクセスを検証してから続行してください。 |
| Service-Managed Encryption Key で暗号化 | 復元されたインスタンスは元の暗号化設定を引き継ぎます。復元中に暗号化を無効化したり、CMEK に切り替えたりすることはできません。 |
| データベースレイヤー暗号化が未有効 | Enhanced Data Encryption を使用せずに続行するか、対象リージョン内の登録済みキーを選択して新しいインスタンスで CMEK を有効にできます。 |

CMEK で保護された {{{ .premium }}} バックアップでは、復元先インスタンスに別のキーを選択したり、CMEK を無効化したりすることはできず、復元は元のクラウドプロバイダーおよびリージョン内で行う必要があります。

CMEK で保護された {{{ .dedicated }}} バックアップを、同じクラウドプロバイダーおよびリージョン内の新しい {{{ .premium }}} インスタンスに復元する場合（クロスプラン復元）、TiDB Cloud は元の {{{ .dedicated }}} キーを使用してソースバックアップを復号し、新しいインスタンス用に登録済みの {{{ .premium }}} キーでデータを再暗号化します。元の {{{ .dedicated }}} キーは復号のために有効かつ認可済みのまま維持し、同じクラウドプロバイダーおよびリージョン内の登録済み {{{ .premium }}} キーを選択してください（同じキーでも別のキーでもかまいません）。サポートされる復元元と手順の詳細は、[Backup and Restore for {{{ .premium }}}](/tidb-cloud/premium/backup-and-restore-premium.md) を参照してください。

> **Warning:**
>
> ソースインスタンスを削除した後でも、そのバックアップを復元する必要がある限り、元の CMEK を有効かつ認可済みの状態で維持してください。必要なキーマテリアルが完全に削除または破棄されると、そのキーで暗号化されたバックアップは復旧できません。

## 顧客管理暗号化キー（CMEK）をローテーションする {#rotate-a-customer-managed-encryption-key-cmek}

キーマテリアルのローテーションは、クラウド KMS で直接設定してください。AWS KMS と Alibaba Cloud KMS では、キーマテリアルをローテーションしてもキー ID と ARN は変わらないため、TiDB Cloud 側で設定を更新する必要はありません。

キーマテリアルのローテーションは、同じ CMEK の基盤となるマテリアルを更新するものです。インスタンスを別の CMEK に切り替えたり、既存データを再暗号化したり、すでに侵害された data encryption key (DEK) に対処したりするものではありません。

- AWS については、[Rotate AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) を参照してください。
- Alibaba Cloud については、[Key rotation in Alibaba Cloud KMS](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/configure-key-rotation) を参照してください。

## 暗号化によるデータ保護の仕組み {#how-encryption-protects-your-data}

### 暗号化メカニズム {#encryption-mechanism}

デフォルトでは、クラウドプロバイダーがストレージレイヤーで保存データを暗号化します（たとえば AWS の EBS ボリューム暗号化や S3 サーバー側暗号化）。Enhanced Data Encryption は、ストレージに書き込む前にデータベースデータとバックアップデータを暗号化する、独立したデータベース暗号化レイヤーを追加します。

ストレージアクセスとデータベースレイヤーのキー権限は別々に管理されるため、ストレージオブジェクト（たとえばサーバー側復号後の S3 ファイル）を取得しただけではデータを読み取れません。対応するキーチェーンと KMS 認可がなければ、データベースレイヤーで保護された内容は暗号化されたままです。

Enhanced Data Encryption は保存中のデータを保護します。データベースはクエリ実行中に平文を処理するため、転送中のデータ保護とクエリアクセス制御には [TLS connections](/tidb-cloud/premium/tidb-cloud-tls-connect-to-premium.md) およびデータベースアクセス制御を使用してください。

### キー階層 {#key-hierarchy}

データベース暗号化レイヤーは、3 層のキー階層を持つエンベロープ暗号化を使用します。2 つの暗号化レイヤーは暗号化が適用される場所を示し、キー階層は暗号化キー同士がどのように保護し合うかを示します。keyspace は、インスタンスの論理ストレージ名前空間です。

| キー | 保護対象 | 管理 |
| --- | --- | --- |
| Customer-managed KMS master key (CMEK) | Keyspace Master Key | クラウド KMS アカウント内で管理および認可されます。 |
| Keyspace Master Key | keyspace 用の data encryption keys (DEKs) | 永続化されたコピーは CMEK で暗号化されます。 |
| Data encryption key (DEK) | データベースデータおよびログ | 永続化されたコピーは Keyspace Master Key で暗号化されます。 |

各インスタンスは独自の内部キーチェーンを管理し、1 つの DEK で複数のファイルを暗号化できます。データベースはメモリにキャッシュされた内部キーを使用してローカルでデータを暗号化および復号し、上位レベルのキーを保護およびアンラップするためにクラウド KMS を呼び出します。

AWS KMS が生成する対称キーでは、平文のマスターキーマテリアルは KMS hardware security module (HSM) の境界内に保持されます。詳細は、[Data protection in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/data-protection.html) を参照してください。

### AWS でのキーの認可 {#key-authorization-on-aws}

AWS では、生成されたキーポリシーにより、表示された TiDB Cloud principal に対して、組織の External ID を含む encryption-context 条件の下でキーへのアクセス権が付与されます。AWS KMS は暗号操作時にこの条件を評価し、encryption context を暗号化されたキーマテリアルに結び付けるため、復号にはまったく同じ context が必要になります。

TiDB Cloud は認証済み組織から External ID を導出するため、別の組織からのリクエストは異なる context を持ち、たとえそのリクエストにあなたのキー ARN が含まれていても AWS KMS によって拒否されます。

External ID は秘密情報ではなく、組織識別子です。ステートメントをキーポリシーに追加する際は、生成された `Principal`、`Action`、`Condition` フィールドを保持してください。詳細は、AWS KMS ドキュメントの [Encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html) を参照してください。

### Alibaba Cloud でのキーの認可 {#key-authorization-on-alibaba-cloud}

Alibaba Cloud では、クロスアカウントアクセスのために、Alibaba Cloud Resource Directory (Resource Sharing) を通じて表示された TiDB Cloud アカウントと KMS インスタンスを共有し、共有リストでそのアカウントに対して **Alibaba Cloud Gateway** を有効にし、さらに生成されたステートメントを選択した対称キーのキーポリシーに追加する必要があります。

AWS と同様に、生成されたキーポリシーは、組織の External ID に結び付けられた encryption-context 条件の下で、表示された TiDB Cloud principal にキーへのアクセス権を付与し、他の組織がそのキーを使用することを防ぎます。ステートメントをキーポリシーに追加する際は、生成された `Principal`、`Action`、`Condition` フィールドを保持してください。詳細は、[Manage Keys in Alibaba Cloud KMS](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/manage-keys-2) を参照してください。

## キーの使用状況を監査する {#audit-key-usage}

- **TiDB Cloud でのキー管理**: [console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md) を有効にして、TiDB Cloud コンソールでのキー管理およびインスタンス暗号化アクションを追跡します。
- **KMS API アクティビティ**: AWS では、[AWS CloudTrail](https://docs.aws.amazon.com/kms/latest/developerguide/logging-using-cloudtrail.html) を使用して KMS キー操作を確認します。アクセス拒否により拒否されたクロスアカウントリクエストは呼び出し元アカウントにのみ記録され、KMS イベントには個々の SQL クエリではなくキー操作が記録されます。
- **データベースアクセス**: [database audit logging](/tidb-cloud/premium/tidb-cloud-auditing-premium.md) を有効にして、SQL クエリおよびデータベースユーザーアクティビティを監査します。

## 制限事項 {#limitations}

- {{{ .premium }}} 向け Enhanced Data Encryption は AWS KMS と Alibaba Cloud KMS をサポートします。
- 登録済みキーは、その組織、クラウドプロバイダー、リージョン内でのみ選択できます。CMEK で保護されたバックアップのクロスリージョン復元はサポートされず、CMEK で保護された {{{ .premium }}} バックアップの復元時に別のキーへ切り替えることもできません。
- 一度有効にすると、同じインスタンス上で CMEK を無効化したり、別のキーに置き換えたりすることはできません。
- エクスポートされたデータおよびダウンストリームシステムはインスタンスの CMEK の対象外であり、個別に暗号化する必要があります。
- インスタンスを削除しても、保持されたバックアップスナップショットやそのキー依存関係は削除されません。必要なキーマテリアルを恒久的に失うと、それに依存する暗号化データは復旧できなくなります。

## キーアクセス検証のトラブルシューティング {#troubleshoot-key-access-verification}

- **キー登録または検証に失敗する場合**:
    - キーが、選択したクラウドプロバイダーおよびリージョン内の対称暗号化キーであることを確認してください。
    - クラウド KMS でキーが有効化されていること（無効化されておらず、削除保留でもないこと）を確認してください。
    - 生成されたすべてのステートメントが、`Principal`、`Action`、`Condition` フィールドを変更せずにキーポリシーへ追加されていることを確認してください。
    - **Alibaba Cloud のみ**: KMS インスタンスが、Resource Directory (Resource Sharing) を通じて表示された TiDB Cloud アカウントと共有されており、共有リストでそのアカウントに対して **Alibaba Cloud Gateway** が有効になっていることを確認してください。
    - クラウド KMS で設定を修正し、再度アクセスチェックを実行してください。
- **登録は成功するが、インスタンス作成、有効化、または復元に失敗する場合**:
    - エラーメッセージを確認してください。キーポリシーにアクセスをブロックする制限（VPC、IP、サービス条件など）が追加されている場合は、ポリシーを更新して再試行してください。
- **問題が解決しない場合**:
    - クラウドプロバイダー、リージョン、キー ARN、操作時刻、エラーメッセージを添えて [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。