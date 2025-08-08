---
title: Encryption at Rest
summary: 機密データを保護するために保存時の暗号化を有効にする方法を学びます。
---

# 保存時の暗号化 {#encryption-at-rest}

> **注記：**
>
> クラスターがAWS上にデプロイされており、EBSstorageを使用している場合は、EBS暗号化を使用することをお勧めします。1 [AWS ドキュメント - EBS 暗号化](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)参照してください。AWS上でローカルNVMestorageなど、EBS以外のstorageを使用している場合は、このドキュメントで紹介されている保存時の暗号化を使用することをお勧めします。

保存時の暗号化とは、データが保存時に暗号化されることを意味します。データベースの場合、この機能はTDE（透過的データ暗号化）とも呼ばれます。これは、転送中の暗号化（TLS）や使用中の暗号化（ほとんど使用されません）とは対照的です。保存時の暗号化はSSDドライブ、ファイルシステム、クラウドベンダーなど、さまざまな方法で実行できますが、TiKVがstorage前に暗号化を行うことで、攻撃者がデータにアクセスするにはデータベースへの認証が必要となることを確実にします。例えば、攻撃者が物理マシンにアクセスできたとしても、ディスク上のファイルをコピーするだけではデータにアクセスできません。

## さまざまな TiDB コンポーネントでの暗号化サポート {#encryption-support-in-different-tidb-components}

TiDBクラスタでは、コンポーネントごとに異なる暗号化方式が使用されます。このセクションでは、TiKV、 TiFlash、PD、バックアップ＆リストア（BR）など、TiDBの各コンポーネントにおける暗号化サポートについて説明します。

TiDBクラスターをデプロイすると、ユーザーデータの大部分はTiKVノードとTiFlashノードに保存されます。一部のメタデータはPDノードに保存されます（例：TiKVリージョン境界として使用されるセカンダリインデックスキー）。保存データの暗号化のメリットを最大限に活用するには、すべてのコンポーネントで暗号化を有効にする必要があります。暗号化を実装する際には、バックアップ、ログファイル、ネットワーク経由で送信されるデータも考慮する必要があります。

### TiKV {#tikv}

TiKVは保存時の暗号化をサポートしています。この機能により、TiKVは[AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) in 5モードまたは[SM4](https://en.wikipedia.org/wiki/SM4_(cipher)) in [CTR](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)モードを使用してデータファイルを透過的に暗号化できます。保存時の暗号化を有効にするには、ユーザーが暗号化キーを提供する必要があります。このキーはマスターキーと呼ばれます。TiKVは、実際のデータファイルの暗号化に使用したデータキーを自動的にローテーションします。マスターキーは手動で随時ローテーションできます。保存時の暗号化は、保存中のデータ（つまりディスク上）のみを暗号化し、ネットワーク経由で転送中のデータは暗号化しないことに注意してください。保存時の暗号化とTLSを併用することをお勧めします。

クラウド展開とセルフホスト展開の両方でキー管理サービス (KMS) を使用することも、プレーンテキストのマスター キーをファイルで提供することもできます。

TiKVは現在、コアダンプから暗号鍵とユーザーデータを除外していません。保存時の暗号化を使用する場合は、TiKVプロセスのコアダンプを無効にすることをお勧めします。これは現在、TiKV自体では処理されていません。

TiKVは、暗号化されたデータファイルをファイルの絶対パスを使用して追跡します。そのため、TiKVノードで暗号化が有効になった後は、ユーザーは`storage.data-dir`などのデータファイルパス設定を変更`rocksdb.wal-dir` `raftdb.wal-dir`で`raftstore.raftdb-path` 。

SM4暗号化はTiKVバージョン6.3.0以降でのみサポートされます。TiKVバージョン6.3.0より前のバージョンではAES暗号化のみがサポートされます。SM4暗号化はパフォーマンスに影響を与えます。最悪の場合、スループットが50%～80%低下する可能性があります。ただし、 [`storage.block-cache`](/tikv-configuration-file.md#storageblock-cache)を十分に大きな値に設定することで、この影響を大幅に軽減し、スループットの低下を約10%に抑えることができます。

### TiFlash {#tiflash}

TiFlash は保存時の暗号化をサポートします。データキーはTiFlashによって生成されます。TiFlash（ TiFlash Proxy を含む）に書き込まれるすべてのファイル（データファイル、スキーマファイル、一時ファイルを含む）は、現在のデータキーを使用して暗号化されます。暗号化アルゴリズム、暗号化設定（ TiFlashでサポートされる[`tiflash-learner.toml`ファイル](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) ）、および監視メトリックの意味は、TiKV のものと一致しています。

Grafana を使用してTiFlash を展開した場合は、 **TiFlash-Proxy-Details** -&gt; **Encryption**パネルを確認できます。

SM4 暗号化は、 TiFlashの v6.4.0 以降のバージョンでのみサポートされます。TiFlashのv6.4.0 より前のバージョンでは、AES 暗号化のみがサポートされます。

### PD {#pd}

PD の保存時の暗号化は実験的機能であり、TiKV と同じ方法で構成されます。

### BRによるバックアップ {#backups-with-br}

BRは、S3へのデータバックアップ時にS3サーバー側暗号化（SSE）をサポートします。お客様所有のAWS KMSキーをS3サーバー側暗号化と併用することも可能です。詳細は[BR S3 サーバー側暗号化](/encryption-at-rest.md#br-s3-server-side-encryption)ご覧ください。

### ログ記録 {#logging}

TiKV、TiDB、およびPD情報ログには、デバッグ用のユーザーデータが含まれる場合があります。情報ログとその中に含まれるデータは暗号化されません。1 [ログ編集](/log-redaction.md)有効にすることを推奨します。

## 保存時の TiKV 暗号化 {#tikv-encryption-at-rest}

### 概要 {#overview}

TiKVは現在、 CTRモードでAES128、AES192、AES256、またはSM4（バージョン6.3.0以降のみ）を使用したデータ暗号化をサポートしています。TiKVはエンベロープ暗号化を使用します。そのため、暗号化を有効にすると、TiKVでは2種類の鍵が使用されます。

-   マスターキー。マスターキーはユーザーによって提供され、TiKVが生成するデータキーを暗号化するために使用されます。マスターキーの管理はTiKVの外部で行われます。
-   データキー。データキーはTiKVによって生成され、実際にデータの暗号化に使用されるキーです。

同じマスターキーを複数のTiKVインスタンスで共有できます。本番でマスターキーを提供する場合は、KMS経由が推奨されます。現在、TiKVは[AWS](https://docs.aws.amazon.com/kms/index.html) 、 [Googleクラウド](https://cloud.google.com/security/products/security-key-management?hl=en) 、 [アズール](https://learn.microsoft.com/en-us/azure/key-vault/)でKMS暗号化をサポートしています。KMS暗号化を有効にするには、KMS経由でカスタマーマスターキー（CMK）を作成し、設定ファイルを使用してTiKVにCMKキーIDを提供する必要があります。TiKVがKMS CMKにアクセスできない場合、起動または再起動に失敗します。

あるいは、カスタムキーを使用したい場合は、ファイル経由でマスターキーを提供することもできます。ファイルには、16進文字列としてエンコードされた256ビット（32バイト）のキーが含まれ、改行文字（つまり`\n` ）で終了し、他に何も含まれていない必要があります。ただし、キーをディスクに保存するとキーが漏洩するため、キーファイルはRAMの`tempfs`に保存するのに適しています。

データキーは、基盤となるstorageエンジン（RocksDB）に渡されます。SSTファイル、WALファイル、MANIFESTファイルなど、RocksDBによって書き込まれるすべてのファイルは、現在のデータキーで暗号化されます。TiKVが使用するその他の一時ファイル（ユーザーデータが含まれる場合がある）も、同じデータキーを使用して暗号化されます。データキーは、デフォルトではTiKVによって毎週自動的にローテーションされますが、期間は設定可能です。キーのローテーションでは、TiKVは既存のすべてのファイルを書き換えてキーを置き換えるわけではありませんが、クラスターに一定の書き込みワークロードがかかっている場合、RocksDBの圧縮機能によって、最新のデータキーを使用して古いデータが新しいデータファイルに書き換えられることが期待されます。TiKVは、各ファイルの暗号化に使用されたキーと暗号化方式を追跡し、読み取り時にその情報を使用してコンテンツを復号化します。

データ暗号化方式に関わらず、データキーはGCMモードでAES256を使用して暗号化され、追加の認証を行います。そのため、KMSではなくファイルから渡す場合、マスターキーは256ビット（32バイト）である必要があります。

### 暗号化を設定する {#configure-encryption}

暗号化を有効にするには、TiKV および PD の構成ファイルに暗号化セクションを追加します。

    [security.encryption]
    data-encryption-method = "aes128-ctr"
    data-key-rotation-period = "168h" # 7 days

-   `data-encryption-method`暗号化アルゴリズムを指定します。指定可能な値は`"aes128-ctr"` 、 `"aes192-ctr"` 、 `"aes256-ctr"` 、 `"sm4-ctr"` （v6.3.0以降のバージョンのみ）、 `"plaintext"`です。デフォルト値は`"plaintext"`で、暗号化はデフォルトで無効になっています。

    -   新しい TiKV クラスターまたは既存の TiKV クラスターの場合、暗号化が有効になった後に書き込まれたデータのみが暗号化されることが保証されます。
    -   暗号化を有効にした後に無効にするには、構成ファイルから`data-encryption-method`削除するか、その値を`"plaintext"`に設定して、TiKV を再起動します。
    -   暗号化アルゴリズムを変更するには、値`data-encryption-method`をサポートされている暗号化アルゴリズムに置き換え、TiKVを再起動します。置き換え後、新しいデータが書き込まれると、以前の暗号化アルゴリズムで生成された暗号化ファイルが、新しい暗号化アルゴリズムで生成されたファイルに徐々に書き換えられます。

-   `data-key-rotation-period` 、TiKV がキーをローテーションする頻度を指定します。

暗号化が有効になっている場合（つまり、 `data-encryption-method`値が`"plaintext"`ではない場合）、次のいずれかの方法でマスター キーを指定する必要があります。

-   [KMS経由でマスターキーを指定する](#specify-a-master-key-via-kms)
-   [ファイル経由でマスターキーを指定する](#specify-a-master-key-via-a-file)

#### KMS経由でマスターキーを指定する {#specify-a-master-key-via-kms}

TiKVは、AWS、Google Cloud、Azureの3つのプラットフォームでKMS暗号化をサポートしています。サービスがデプロイされているプラットフォームに応じて、いずれかのプラットフォームを選択してKMS暗号化を設定できます。

<SimpleTab>

<div label="AWS KMS">

**ステップ1. マスターキーを作成する**

AWS でキーを作成するには、次の手順を実行します。

1.  AWS コンソールの[AWS KMS](https://console.aws.amazon.com/kms)に移動します。
2.  コンソールの右上隅で正しい地域が選択されていることを確認してください。
3.  **[キーの作成]**をクリックし、キーの種類として**[対称]**を選択します。
4.  キーのエイリアスを設定します。

AWS CLI を使用して操作を実行することもできます。

```shell
aws --region us-west-2 kms create-key
aws --region us-west-2 kms create-alias --alias-name "alias/tidb-tde" --target-key-id 0987dcba-09fe-87dc-65ba-ab0987654321
```

2 番目のコマンドに入力する`--target-key-id` 、最初のコマンドの出力にあります。

**ステップ2. マスターキーを設定する**

AWS KMS を使用してマスターキーを指定するには、TiKV 設定ファイルの`[security.encryption]`セクションの後に`[security.encryption.master-key]`設定を追加します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"
    endpoint = "https://kms.us-west-2.amazonaws.com"

`key-id` KMS CMK のキー ID を指定します。3 `region` KMS CMK の AWS リージョン名です。5 はオプションであり、AWS 以外のベンダーの AWS KMS 互換サービスを使用している場合や、 `endpoint` [KMS の VPC エンドポイント](https://docs.aws.amazon.com/kms/latest/developerguide/kms-vpc-endpoint.html)使用する必要がある場合を除き、通常は指定する必要はありません。

AWSでも[マルチリージョンキー](https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html)使用できます。この場合、特定のリージョンにプライマリキーを設定し、必要なリージョンにレプリカキーを追加する必要があります。

</div>
<div label="Google Cloud KMS">

**ステップ1. マスターキーを作成する**

Google Cloud でキーを作成するには、次の手順を行います。

1.  Google Cloud コンソールの[キー管理](https://console.cloud.google.com/security/kms/keyrings)ページに移動します。
2.  **「キーリングを作成」**をクリックします。キーリングの名前を入力し、キーリングの場所を選択して、 **「作成」**をクリックします。キーリングの場所は、TiDBクラスターがデプロイされているリージョンをカバーする必要があります。
3.  前の手順で作成したキーリングを選択し、キーリングの詳細ページで**「キーの作成」**をクリックします。
4.  キーの名前を入力し、次のようにキー情報を設定して、 **「作成」**をクリックします。

    -   **保護レベル**:**ソフトウェア**または**HSM**
    -   **鍵マテリアル**:**生成された鍵**
    -   **目的**:**対称暗号化/復号化**

この操作は gcloud CLI を使用して実行することもできます。

```shell
gcloud kms keyrings create "key-ring-name" --location "global"
gcloud kms keys create "key-name" --keyring "key-ring-name" --location "global" --purpose "encryption" --rotation-period "30d"
```

上記のコマンドの`"key-ring-name"` 、 `"key-name"` 、 `"global"` 、 `"30d"`の値を、実際のキーに対応する名前と構成に置き換えてください。

**ステップ2. マスターキーを設定する**

Google Cloud KMS を使用してマスター キーを指定するには、 `[security.encryption]`セクションの後に`[security.encryption.master-key]`構成を追加します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "projects/project-name/locations/global/keyRings/key-ring-name/cryptoKeys/key-name"
    vendor = "gcp"

    [security.encryption.master-key.gcp]
    credential-file-path = "/path/to/credential.json"

-   `key-id` KMS CMK のキー ID を指定します。
-   `credential-file-path`認証資格情報ファイルのパスを指定します。現在、このファイルではサービスアカウントと認証ユーザーの2種類の資格情報がサポートされています。TiKV環境が既に[アプリケーションのデフォルト資格情報](https://cloud.google.com/docs/authentication/application-default-credentials)で構成されている場合は、 `credential-file-path`設定する必要はありません。

</div>
<div label="Azure KMS">

**ステップ1. マスターキーを作成する**

Azure でキーを作成するには、 [Azure ポータルを使用して Azure Key Vault からキーを設定および取得する](https://learn.microsoft.com/en-us/azure/key-vault/keys/quick-create-portal)の手順を参照してください。

**ステップ2. マスターキーを設定する**

Azure KMS を使用してマスター キーを指定するには、TiKV 構成ファイルの`[security.encryption]`セクションの後に`[security.encryption.master-key]`構成を追加します。

    [security.encryption.master-key]
    type = 'kms'
    key-id = 'your-kms-key-id'
    region = 'region-name'
    endpoint = 'endpoint'
    vendor = 'azure'

    [security.encryption.master-key.azure]
    tenant-id = 'tenant_id'
    client-id = 'client_id'
    keyvault-url = 'keyvault_url'
    hsm-name = 'hsm_name'
    hsm-url = 'hsm_url'
    # The following four fields are optional, used to set client authentication credentials. You can configure them according to the requirements of your scenario.
    client_certificate = ""
    client_certificate_path = ""
    client_certificate_password = ""
    client_secret = ""

`vendor`を除き、前述の構成の他のフィールドの値を、実際のキーの対応する構成に変更する必要があります。

</div>
</SimpleTab>

#### ファイル経由でマスターキーを指定する {#specify-a-master-key-via-a-file}

ファイルに保存されているマスター キーを指定する場合、マスター キーの構成は次のようになります。

    [security.encryption.master-key]
    type = "file"
    path = "/path/to/key/file"

ここで、 `path`キーファイルへのパスです。ファイルには、16進文字列としてエンコードされた256ビット（32バイト）のキーが含まれ、改行文字（ `\n` ）で終了し、他に何も含まれていない必要があります。ファイルの内容の例：

    3b5896b5be691006e0f71c3040a29495ddcad20b14aff61806940ebd780d3c62

### マスターキーを回転させる {#rotate-the-master-key}

マスターキーをローテーションするには、設定で新しいマスターキーと古いマスターキーの両方を指定し、TiKVを再起動する必要があります。新しいマスターキーを指定するには`security.encryption.master-key`使用し、古いマスターキーを指定するには`security.encryption.previous-master-key`使用します。 `security.encryption.previous-master-key`の設定形式は`encryption.master-key`と同じです。再起動後、TiKVは新しいマスターキーと古いマスターキーの両方にアクセスする必要がありますが、TiKVが起動して実行されると、TiKVは新しいキーのみにアクセスする必要があります。それ以降は、設定ファイルに`encryption.previous-master-key`設定を残しておいても問題ありません。再起動後も、TiKVは新しいマスターキーを使用して既存のデータを復号化できなかった場合にのみ、古いキーを使用しようとします。

現在、オンラインでのマスターキーのローテーションはサポートされていないため、TiKVを再起動する必要があります。オンラインクエリを処理している稼働中のTiKVクラスターに対して、ローリング再起動を実行することをお勧めします。

KMS CMK をローテーションするための設定例を次に示します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
    region = "us-west-2"

    [security.encryption.previous-master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"

### 監視とデバッグ {#monitoring-and-debugging}

TiKVをGrafanaでデプロイしている場合は、保存時の暗号化を監視するために、 **TiKV-Details**ダッシュボードの**暗号化**パネルを確認できます。確認すべきメトリクスがいくつかあります。

-   暗号化の初期化: TiKV起動時に暗号化が初期化された場合は1、それ以外の場合は0。マスターキーのローテーションの場合、暗号化が初期化された後は、TiKVは以前のマスターキーにアクセスする必要はありません。
-   暗号化データキー：既存のデータキーの数。データキーのローテーションが発生するたびに、この数は1ずつ増加します。この指標を使用して、データキーのローテーションが期待どおりに機能しているかどうかを監視します。
-   暗号化ファイル: 現在存在する暗号化データファイルの数。この数とデータディレクトリ内の既存のデータファイル数を比較することで、暗号化されていないクラスタの暗号化を有効にする際に、暗号化されるデータの量を推定できます。
-   暗号化メタファイル サイズ: 暗号化メタデータ ファイルのサイズ。
-   読み取り/書き込み暗号化メタ期間: 暗号化のメタデータを操作するための追加のオーバーヘッド。

デバッグのために、 `tikv-ctl`コマンドを使用すると、ファイルの暗号化に使用された暗号化方式やデータキーID、データキーのリストなどの暗号化メタデータをダンプできます。この操作により機密データが漏洩する可能性があるため、本番での使用は推奨されません。3 [TiKV Control](/tikv-control.md#dump-encryption-metadata)ドキュメントを参照してください。

### TiKVバージョン間の互換性 {#compatibility-between-tikv-versions}

TiKVが暗号化メタデータを管理する際に発生するI/Oおよびミューテックスの競合によるオーバーヘッドを削減するため、TiKV v4.0.9では最適化が導入され、TiKV設定ファイルの`security.encryption.enable-file-dictionary-log`で制御されます。この設定パラメータは、TiKV v4.0.9以降のバージョンでのみ有効です。

有効になっている場合（デフォルト）、暗号化メタデータのデータ形式はTiKV v4.0.8以前のバージョンでは認識されません。例えば、保存時の暗号化とデフォルトの`enable-file-dictionary-log`設定でTiKV v4.0.9以降を使用しているとします。クラスターをTiKV v4.0.8以前のバージョンにダウングレードすると、TiKVは起動に失敗し、情報ログに次のようなエラーが記録されます。

    [2020/12/07 07:26:31.106 +08:00] [ERROR] [mod.rs:110] ["encryption: failed to load file dictionary."]
    [2020/12/07 07:26:33.598 +08:00] [FATAL] [lib.rs:483] ["called `Result::unwrap()` on an `Err` value: Other(\"[components/encryption/src/encrypted_file/header.rs:18]: unknown version 2\")"]

上記のエラーを回避するには、まず`security.encryption.enable-file-dictionary-log`を`false`に設定し、TiKVをv4.0.9以降で起動してください。TiKVが正常に起動すると、暗号化メタデータのデータ形式が以前のTiKVバージョンで認識可能なバージョンにダウングレードされます。この時点で、TiKVクラスターを以前のバージョンにダウングレードできます。

## 保存時のTiFlash暗号化 {#tiflash-encryption-at-rest}

### 概要 {#overview}

TiFlashが現在サポートしている暗号化アルゴリズムは、TiKVがCTRモードでサポートしているアルゴリズム（AES128、AES192、AES256、SM4（v6.4.0以降のバージョンのみ））と一致しています。TiFlashはエンベロープ暗号化も使用します。そのため、暗号化を有効にすると、 TiFlashでは2種類の鍵が使用されます。

-   マスターキー。マスターキーはユーザーによって提供され、 TiFlashが生成するデータキーを暗号化するために使用されます。マスターキーの管理はTiFlashの外部で行われます。
-   データキー。データキーはTiFlashによって生成され、実際にデータの暗号化に使用されるキーです。

同じマスターキーを複数のTiFlashインスタンスで共有できるほか、 TiFlashと TiKV 間で共有することもできます。本番でマスターキーを提供する場合は、AWS KMS を使用することをお勧めします。また、カスタムキーを使用したい場合は、ファイル経由でマスターキーを提供することも可能です。マスターキーの生成方法とフォーマットは TiKV と同じです。

TiFlash は、データファイル、スキーマファイル、計算中に生成される一時データファイルなど、ディスク上に配置されるすべてのデータを、現在のデータキーを使用して暗号化します。データキーは、 TiFlashによってデフォルトで毎週自動的にローテーションされます。ローテーションの周期は設定可能です。キーローテーションでは、 TiFlash は既存のすべてのファイルを書き換えてキーを置き換えるわけではありませんが、クラスターに一定の書き込みワークロードがかかっている場合、バックグラウンドの圧縮タスクによって古いデータが最新のデータキーを使用して新しいデータファイルに書き換えられることが想定されます。TiFlashは、各ファイルの暗号化に使用されたキーと暗号化方式を追跡し、読み取り時にその情報を使用してコンテンツを復号化します。

### キーの作成 {#key-creation}

AWS でキーを作成するには、TiKV のキーを作成する手順を参照してください。

### 暗号化を設定する {#configure-encryption}

暗号化を有効にするには、 `tiflash-learner.toml`構成ファイルに暗号化セクションを追加します。

    [security.encryption]
    data-encryption-method = "aes128-ctr"
    data-key-rotation-period = "168h" # 7 days

または、 TiUPクラスター テンプレートに次の内容を追加します。

    server_configs:
      tiflash-learner:
        security.encryption.data-encryption-method: "aes128-ctr"
        security.encryption.data-key-rotation-period: "168h" # 7 days

`data-encryption-method`に指定できる値は、「aes128-ctr」、「aes192-ctr」、「aes256-ctr」、「sm4-ctr」（v6.4.0 以降のみ）、「plaintext」です。デフォルト値は「plaintext」で、暗号化は無効です。3 `data-key-rotation-period` 、 TiFlash がデータキーをローテーションする頻度を定義します。暗号化は、新規TiFlashクラスターまたは既存のTiFlashクラスターで有効にできますが、暗号化が有効になった後に書き込まれたデータのみが暗号化されることが保証されます。暗号化を無効にするには、設定ファイルの`data-encryption-method`削除するか、「plaintext」にリセットし、 TiFlashを再起動します。暗号化方式を変更するには、設定ファイルの`data-encryption-method`更新し、 TiFlash を再起動します。暗号化アルゴリズムを変更するには、 `data-encryption-method`サポートされている暗号化アルゴリズムに置き換え、 TiFlash を再起動します。置き換え後、新しいデータが書き込まれると、以前の暗号化アルゴリズムで生成された暗号化ファイルは、新しい暗号化アルゴリズムで生成されたファイルに徐々に書き換えられます。

暗号化が有効になっている場合（つまり、 `data-encryption-method` 「プレーンテキスト」ではない場合）、マスターキーを指定する必要があります。AWS KMS CMK をマスターキーとして指定するには、 `tiflash-learner.toml`設定ファイルの`encryption`セクションの後に`encryption.master-key`セクションを追加します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"
    endpoint = "https://kms.us-west-2.amazonaws.com"

または、 TiUPクラスター テンプレートに次の内容を追加します。

    server_configs:
      tiflash-learner:
        security.encryption.master-key.type: "kms"
        security.encryption.master-key.key-id: "0987dcba-09fe-87dc-65ba-ab0987654321"
        security.encryption.master-key.region: "us-west-2"
        security.encryption.master-key.endpoint: "https://kms.us-west-2.amazonaws.com"

上記の設定項目の意味は TiKV と同じです。

ファイルに保存されているマスター キーを指定するには、 `tiflash-learner.toml`構成ファイルに次の構成を追加します。

    [security.encryption.master-key]
    type = "file"
    path = "/path/to/key/file"

または、 TiUPクラスター テンプレートに次の内容を追加します。

    server_configs:
      tiflash-learner:
        security.encryption.master-key.type: "file"
        security.encryption.master-key.path: "/path/to/key/file"

上記の設定項目の意味やキーファイルの内容形式は TiKV と同様です。

### マスターキーを回転させる {#rotate-the-master-key}

TiFlashのマスターキーをローテーションするには、TiKV のマスターキーをローテーションする手順に従ってください。現在、 TiFlash はオンラインでのマスターキーのローテーションもサポートしていません。そのため、ローテーションを有効にするにはTiFlashを再起動する必要があります。オンラインクエリを処理している稼働中のTiFlashクラスターに対して、ローリング再起動を実行することをお勧めします。

KMS CMK をローテーションするには、 `tiflash-learner.toml`構成ファイルに次の内容を追加します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
    region = "us-west-2"

    [security.encryption.previous-master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"

または、 TiUPクラスター テンプレートに次の内容を追加します。

    server_configs:
      tiflash-learner:
        security.encryption.master-key.type: "kms"
        security.encryption.master-key.key-id: "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
        security.encryption.master-key.region: "us-west-2"
        security.encryption.previous-master-key.type: "kms"
        security.encryption.previous-master-key.key-id: "0987dcba-09fe-87dc-65ba-ab0987654321"
        security.encryption.previous-master-key.region: "us-west-2"

### 監視とデバッグ {#monitoring-and-debugging}

TiFlash をGrafana でデプロイしている場合、保存時の暗号化を監視するには、 **TiFlash-Proxy-Details**ダッシュボードの**「暗号化」**パネルを確認します。監視項目の意味は TiKV と同じです。

TiFlashは暗号化されたメタデータの管理にTiKVのロジックを再利用するため、デバッグのために`tikv-ctl`コマンドを使用して、ファイルの暗号化に使用された暗号化方式やデータキーID、データキーのリストなどの暗号化メタデータをダンプできます。この操作は機密データを公開する可能性があるため、本番では推奨されません。詳細については[TiKV Control](/tikv-control.md#dump-encryption-metadata)を参照してください。

### TiKVバージョン間の互換性 {#compatibility-between-tikv-versions}

TiFlashもv4.0.9で暗号化メタデータ操作を最適化しており、その互換性要件はTiKVと同じです。詳細については[TiKVバージョン間の互換性](#compatibility-between-tikv-versions)参照してください。

## BR S3 サーバー側暗号化 {#br-s3-server-side-encryption}

BRを使用して S3 にバックアップする際に S3 サーバー側の暗号化を有効にするには、引数を`--s3.sse`渡し、値を &quot;aws:kms&quot; に設定します。S3 は暗号化に独自の KMS キーを使用します。例:

    tiup br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.sse aws:kms

独自に作成し所有するカスタム AWS KMS CMK を使用するには、 `--s3.sse-kms-key-id`追加で渡します。この場合、 BRプロセスとクラスター内のすべての TiKV ノードの両方が KMS CMK にアクセスする必要があり（例：AWS IAM経由）、KMS CMK はバックアップの保存に使用する S3 バケットと同じ AWS リージョンに存在する必要があります。BR プロセスと TiKV ノードにBR IAM経由で KMS CMK へのアクセスを許可することをお勧めします[IAMは](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)の使用方法については、AWS ドキュメントを参照してください。例：

    tiup br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.sse aws:kms --s3.sse-kms-key-id 0987dcba-09fe-87dc-65ba-ab0987654321

バックアップを復元する際、 `--s3.sse`と`--s3.sse-kms-key-id`両方を使用しないでください。S3は暗号化設定を自動的に判断します。バックアップを復元するクラスター内のBRプロセスとTiKVノードもKMS CMKにアクセスする必要があります。アクセスできない場合、復元は失敗します。例：

    tiup br restore full --pd <pd-address> --storage "s3://<bucket>/<prefix>"

## BR Azure Blob Storage サーバー側暗号化 {#br-azure-blob-storage-server-side-encryption}

BRを使用して Azure Blob Storage にデータをバックアップする場合、サーバー側の暗号化の暗号化スコープまたは暗号化キーのいずれかを指定できます。

### 方法1: 暗号化スコープを使用する {#method-1-use-an-encryption-scope}

バックアップ データの暗号化範囲を指定するには、次の 2 つの方法のいずれかを使用できます。

-   `backup`コマンドに`--azblob.encryption-scope`オプションを含め、スコープ名に設定します。

    ```shell
    tiup br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-scope scope1
    ```

-   URI に`encryption-scope`を含め、スコープ名に設定します。

    ```shell
    tiup br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-scope=scope1"
    ```

詳細については、Azure のドキュメントを参照してください: [暗号化スコープ付きのBLOBをアップロードする](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-scope-manage?tabs=powershell#upload-a-blob-with-an-encryption-scope) 。

バックアップを復元する際に、暗号化の範囲を指定する必要はありません。Azure Blob Storage は自動的にデータを復号化します。例:

```shell
tiup br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
```

### 方法2: 暗号化キーを使用する {#method-2-use-an-encryption-key}

バックアップ データの暗号化キーを指定するには、次の 3 つの方法のいずれかを使用できます。

-   `backup`コマンドに`--azblob.encryption-key`オプションを含め、AES256 暗号化キーを設定します。

    ```shell
    tiup br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-key <aes256-key>
    ```

-   URIに`encryption-key`を含め、AES256暗号化キーを設定します。キーに`&`や`%`などのURI予約文字が含まれている場合は、事前にパーセントエンコードする必要があります。

    ```shell
    tiup br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-key=<aes256-key>"
    ```

-   環境変数`AZURE_ENCRYPTION_KEY`にAES256暗号化キーを設定します。実行前に、環境変数に設定された暗号化キーを忘れないように必ず覚えておいてください。

    ```shell
    export AZURE_ENCRYPTION_KEY=<aes256-key>
    tiup br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
    ```

詳細については、Azure のドキュメントを参照してください: [Blobstorageへのリクエストに暗号化キーを提供する](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-customer-provided-keys) 。

バックアップを復元する際には、暗号化キーを指定する必要があります。例：

-   `restore`コマンドに`--azblob.encryption-key`オプションを含めます。

    ```shell
    tiup br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-key <aes256-key>
    ```

-   URIに`encryption-key`を含めます:

    ```shell
    tiup br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-key=<aes256-key>"
    ```

-   `AZURE_ENCRYPTION_KEY`環境変数を設定します。

    ```shell
    export AZURE_ENCRYPTION_KEY=<aes256-key>
    tiup br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
    ```
