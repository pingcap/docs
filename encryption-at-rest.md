---
title: Encryption at Rest
summary: Learn how to enable encryption at rest to protect sensitive data.
---

# 保存時の暗号化 {#encryption-at-rest}

> **ノート：**
>
> クラスタがAWSにデプロイされ、EBSストレージを使用している場合は、EBS暗号化を使用することをお勧めします。 [AWSドキュメント-EBS暗号化](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)を参照してください。ローカルNVMeストレージなどのAWSで非EBSストレージを使用している場合は、このドキュメントで紹介されている保存時に暗号化を使用することをお勧めします。

保存時の暗号化とは、データが保存されるときに暗号化されることを意味します。データベースの場合、この機能はTDE（透過データ暗号化）とも呼ばれます。これは、飛行中の暗号化（TLS）または使用中の暗号化（めったに使用されない）とは対照的です。保管時に暗号化を行うことはさまざまですが（SSDドライブ、ファイルシステム、クラウドベンダーなど）、ストレージの前にTiKVに暗号化を行わせることで、攻撃者がデータにアクセスするためにデータベースで認証する必要があります。たとえば、攻撃者が物理マシンにアクセスした場合、ディスク上のファイルをコピーしてデータにアクセスすることはできません。

## さまざまなTiDBコンポーネントでの暗号化のサポート {#encryption-support-in-different-tidb-components}

TiDBクラスタでは、コンポーネントごとに異なる暗号化方式が使用されます。このセクションでは、TiKV、TiFlash、PD、バックアップと復元（BR）などのさまざまなTiDBコンポーネントでの暗号化サポートを紹介します。

TiDBクラスタが展開されると、ユーザーデータの大部分はTiKVノードとTiFlashノードに保存されます。一部のメタデータはPDノードに保存されます（たとえば、TiKV領域の境界として使用されるセカンダリインデックスキー）。保管時に暗号化のメリットを最大限に活用するには、すべてのコンポーネントで暗号化を有効にする必要があります。暗号化を実装するときは、バックアップ、ログファイル、およびネットワークを介して送信されるデータも考慮する必要があります。

### TiKV {#tikv}

TiKVは、保存時の暗号化をサポートしています。この機能により、 [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)は[クリック率](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)モードを使用してデータファイルを透過的に暗号化できます。保管時に暗号化を有効にするには、ユーザーが暗号化キーを提供する必要があり、このキーはマスターキーと呼ばれます。 TiKVは、実際のデータファイルの暗号化に使用したデータキーを自動的にローテーションします。マスターキーを手動で回転させることもできます。保存データの暗号化は保存データ（つまり、ディスク上）でのみ暗号化され、データがネットワーク経由で転送されている間は暗号化されないことに注意してください。残りの暗号化と一緒にTLSを使用することをお勧めします。

オプションで、クラウドとオンプレミスの両方のデプロイにAWSKMSを使用できます。プレーンテキストのマスターキーをファイルで指定することもできます。

TiKVは現在、コアダンプから暗号化キーとユーザーデータを除外していません。保管時に暗号化を使用する場合は、TiKVプロセスのコアダンプを無効にすることをお勧めします。これは現在、TiKV自体では処理されていません。

TiKVは、ファイルの絶対パスを使用して暗号化されたデータファイルを追跡します。その結果、 `raftstore.raftdb-path`ノードの暗号化がオンになったら、ユーザーは`storage.data-dir`などのデータファイル`raftdb.wal-dir`の構成を変更しないで`rocksdb.wal-dir` 。

### TiFlash {#tiflash}

TiFlashは、保存時の暗号化をサポートしています。データキーはTiFlashによって生成されます。 TiFlash（TiFlashプロキシを含む）に書き込まれるすべてのファイル（データファイル、スキーマファイル、および一時ファイルを含む）は、現在のデータキーを使用して暗号化されます。暗号化アルゴリズム、TiFlashでサポートされている暗号化構成（ `tiflash-learner.toml`ファイル内）、および監視メトリックの意味は、TiKVのものと一致しています。

Grafanaを使用してTiFlashをデプロイした場合は、 **TiFlash-Proxy-Details-** &gt; <strong>Encryption</strong>パネルを確認できます。

### PD {#pd}

PDの保存時の暗号化は実験的機能であり、TiKVと同じ方法で構成されます。

### BRによるバックアップ {#backups-with-br}

BRは、データをS3にバックアップするときに、S3サーバー側暗号化（SSE）をサポートします。お客様が所有するAWSKMSキーは、S3サーバー側の暗号化と一緒に使用することもできます。詳細については、 [BRS3サーバー側の暗号化](/encryption-at-rest.md#br-s3-server-side-encryption)を参照してください。

### ロギング {#logging}

TiKV、TiDB、およびPD情報ログには、デバッグ目的のユーザーデータが含まれる場合があります。情報ログとその中のこのデータは暗号化されていません。 [ログ編集](/log-redaction.md)を有効にすることをお勧めします。

## 安静時のTiKV暗号化 {#tikv-encryption-at-rest}

### 概要 {#overview}

TiKVは現在、CTRモードでAES128、AES192、またはAES256を使用したデータの暗号化をサポートしています。 TiKVはエンベロープ暗号化を使用します。その結果、暗号化が有効になっている場合、TiKVでは2種類のキーが使用されます。

-   マスターキー。マスターキーはユーザーによって提供され、TiKVが生成するデータキーを暗号化するために使用されます。マスターキーの管理はTiKVの外部にあります。
-   データキー。データキーはTiKVによって生成され、データの暗号化に実際に使用されるキーです。

同じマスターキーをTiKVの複数のインスタンスで共有できます。本番環境でマスターキーを提供するための推奨される方法は、AWSKMSを使用することです。 AWS KMSを介してカスタマーマスターキー（CMK）を作成し、構成ファイルでTiKVにCMKキーIDを提供します。 TiKVプロセスは、実行中にKMS CMKにアクセスする必要があります。これは、 [IAMの役割](https://aws.amazon.com/iam/)を使用して実行できます。 TiKVがKMSCMKにアクセスできない場合、起動または再起動に失敗します。 [KMS](https://docs.aws.amazon.com/kms/index.html)および[わたし](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)の使用法については、AWSのドキュメントを参照してください。

または、カスタムキーを使用する必要がある場合は、ファイルを介したマスターキーの提供もサポートされています。ファイルには、16進文字列としてエンコードされた256ビット（または32バイト）のキーが含まれ、改行（つまり、 `\n` ）で終わり、他には何も含まれていない必要があります。ただし、キーをディスクに保持するとキーがリークするため、キーファイルはRAMの`tempfs`に保存する場合にのみ適しています。

データキーは、基盤となるストレージエンジン（つまり、RocksDB）に渡されます。 SSTファイル、WALファイル、MANIFESTファイルなど、RocksDBによって書き込まれるすべてのファイルは、現在のデータキーによって暗号化されます。ユーザーデータを含む可能性のあるTiKVによって使用される他の一時ファイルも、同じデータキーを使用して暗号化されます。データキーは、デフォルトで毎週TiKVによって自動的にローテーションされますが、期間は構成可能です。キーローテーションでは、TiKVは既存のすべてのファイルをリライトしてキーを置き換えるわけではありませんが、クラスタが一定の書き込みワークロードを取得する場合、RocksDBコンパクションは古いデータを最新のデータキーで新しいデータファイルにリライトすることが期待されます。 TiKVは、各ファイルの暗号化に使用されるキーと暗号化方法を追跡し、その情報を使用して読み取り時にコンテンツを復号化します。

データの暗号化方法に関係なく、データキーは追加の認証のためにGCMモードのAES256を使用して暗号化されます。これには、KMSではなくファイルから渡す場合、マスターキーが256ビット（32バイト）である必要がありました。

### キーの作成 {#key-creation}

AWSでキーを作成するには、次の手順に従います。

1.  AWSコンソールの[AWS KMS](https://console.aws.amazon.com/kms)に移動します。
2.  コンソールの右上隅で正しい領域を選択していることを確認してください。
3.  [**キーの作成**]をクリックし、キータイプとして[<strong>対称]</strong>を選択します。
4.  キーのエイリアスを設定します。

AWSCLIを使用して操作を実行することもできます。

```shell
aws --region us-west-2 kms create-key
aws --region us-west-2 kms create-alias --alias-name "alias/tidb-tde" --target-key-id 0987dcba-09fe-87dc-65ba-ab0987654321
```

2番目のコマンドに入力する`--target-key-id`は、最初のコマンドの出力にあります。

### 暗号化を構成する {#configure-encryption}

暗号化を有効にするには、TiKVおよびPDの構成ファイルに暗号化セクションを追加します。

```
[security.encryption]
data-encryption-method = "aes128-ctr"
data-key-rotation-period = "168h" # 7 days
```

`data-encryption-method`に指定できる値は、「aes128-ctr」、「aes192-ctr」、「aes256-ctr」、および「plaintext」です。デフォルト値は「plaintext」です。これは、暗号化がオンになっていないことを意味します。 `data-key-rotation-period`は、TiKVがデータキーをローテーションする頻度を定義します。新しいTiKVクラスタまたは既存のTiKVクラスタに対して暗号化をオンにすることができますが、暗号化を有効にした後に書き込まれたデータのみが暗号化されることが保証されます。暗号化を無効にするには、設定ファイルの`data-encryption-method`を削除するか、「plaintext」にリセットして、TiKVを再起動します。暗号化方式を変更するには、構成ファイルの`data-encryption-method`を更新し、TiKVを再起動します。

暗号化が有効になっている場合（つまり、 `data-encryption-method`は「プレーンテキスト」ではない場合）、マスターキーを指定する必要があります。 AWS KMS CMKをマスターキーとして指定するには、 `encryption`セクションの後に`encryption.master-key`セクションを追加します。

```
[security.encryption.master-key]
type = "kms"
key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
region = "us-west-2"
endpoint = "https://kms.us-west-2.amazonaws.com"
```

`key-id`は、KMSCMKのキーIDを指定します。 `region`は、KMSCMKのAWSリージョン名です。 `endpoint`はオプションであり、AWS以外のベンダーのAWS KMS互換サービスを使用しているか、 [KMSのVPCエンドポイント](https://docs.aws.amazon.com/kms/latest/developerguide/kms-vpc-endpoint.html)を使用する必要がない限り、通常は指定する必要はありません。

AWSでも[マルチリージョンキー](https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html)を使用できます。このためには、特定のリージョンに主キーを設定し、必要なリージョンにレプリカキーを追加する必要があります。

ファイルに保存されるマスターキーを指定するには、マスターキーの構成は次のようになります。

```
[security.encryption.master-key]
type = "file"
path = "/path/to/key/file"
```

ここで、 `path`はキーファイルへのパスです。ファイルには、16進文字列としてエンコードされた256ビット（または16バイト）のキーが含まれ、改行（ `\n` ）で終わり、他には何も含まれていない必要があります。ファイルの内容の例：

```
3b5896b5be691006e0f71c3040a29495ddcad20b14aff61806940ebd780d3c62
```

### マスターキーを回転させます {#rotate-the-master-key}

マスターキーをローテーションするには、構成で新しいマスターキーと古いマスターキーの両方を指定し、TiKVを再起動する必要があります。 `security.encryption.master-key`を使用して新しいマスターキーを指定し、 `security.encryption.previous-master-key`を使用して古いマスターキーを指定します。 `security.encryption.previous-master-key`の構成フォーマットは`encryption.master-key`と同じです。再起動時に、TiKVは古いマスターキーと新しいマスターキーの両方にアクセスする必要がありますが、TiKVが起動して実行されると、TiKVは新しいキーにのみアクセスする必要があります。それ以降、構成ファイルに`encryption.previous-master-key`の構成を残してもかまいません。再起動しても、TiKVは、新しいマスターキーを使用して既存のデータを復号化できない場合にのみ、古いキーを使用しようとします。

現在、オンラインマスターキーローテーションはサポートされていないため、TiKVを再起動する必要があります。オンラインクエリを提供する実行中のTiKVクラスタに対してローリングリスタートを実行することをお勧めします。

KMSCMKをローテーションするための設定例を次に示します。

```
[security.encryption.master-key]
type = "kms"
key-id = "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
region = "us-west-2"

[security.encryption.previous-master-key]
type = "kms"
key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
region = "us-west-2"
```

### 監視とデバッグ {#monitoring-and-debugging}

保管中の暗号化を監視するために、Grafanaを使用してTiKVをデプロイする場合は、 **TiKV-詳細**ダッシュボードの<strong>暗号化</strong>パネルを確認できます。探すべきいくつかのメトリックがあります：

-   初期化された暗号化：TiKVの起動中に暗号化が初期化された場合は1、それ以外の場合は0。マスターキーローテーションの場合、暗号化が初期化された後、TiKVは前のマスターキーにアクセスする必要はありません。
-   暗号化データキー：既存のデータキーの数。データキーのローテーションが発生するたびに、数値は1ずつ増えます。このメトリックを使用して、データキーのローテーションが期待どおりに機能するかどうかを監視します。
-   暗号化されたファイル：現在存在する暗号化されたデータファイルの数。以前に暗号化されていないクラスタの暗号化をオンにしたときに、この数をデータディレクトリ内の既存のデータファイルと比較して、暗号化されているデータの一部を推定します。
-   暗号化メタファイルサイズ：暗号化メタデータファイルのサイズ。
-   読み取り/書き込み暗号化メタ期間：暗号化のためにメタデータを操作するための追加のオーバーヘッド。

デバッグの場合、 `tikv-ctl`コマンドを使用して、ファイルの暗号化に使用される暗号化方式やデータキーIDなどの暗号化メタデータ、およびデータキーのリストをダンプできます。この操作は機密データを公開する可能性があるため、本番環境での使用はお勧めしません。 [TiKVコントロール](/tikv-control.md#dump-encryption-metadata)ドキュメントを参照してください。

### TiKVバージョン間の互換性 {#compatibility-between-tikv-versions}

TiKVが暗号化メタデータを管理するときにI/Oとミューテックスの競合によって引き起こされるオーバーヘッドを減らすために、最適化がTiKV v4.0.9に導入され、TiKV構成ファイルで`security.encryption.enable-file-dictionary-log`によって制御されます。この構成パラメーターは、TiKVv4.0.9以降のバージョンでのみ有効です。

有効になっている場合（デフォルト）、暗号化メタデータのデータ形式はTiKVv4.0.8以前のバージョンでは認識できません。たとえば、暗号化を保存し、デフォルトの`enable-file-dictionary-log`構成でTiKVv4.0.9以降を使用するとします。クラスタをTiKVv4.0.8以前にダウングレードすると、TiKVの起動に失敗し、情報ログに次のようなエラーが表示されます。

```
[2020/12/07 07:26:31.106 +08:00] [ERROR] [mod.rs:110] ["encryption: failed to load file dictionary."]
[2020/12/07 07:26:33.598 +08:00] [FATAL] [lib.rs:483] ["called `Result::unwrap()` on an `Err` value: Other(\"[components/encryption/src/encrypted_file/header.rs:18]: unknown version 2\")"]
```

上記のエラーを回避するには、最初に`security.encryption.enable-file-dictionary-log`を`false`に設定し、v4.0.9以降でTiKVを開始します。 TiKVが正常に起動すると、暗号化メタデータのデータ形式は、以前のTiKVバージョンで認識できるバージョンにダウングレードされます。この時点で、TiKVクラスタを以前のバージョンにダウングレードできます。

## BRS3サーバー側の暗号化 {#br-s3-server-side-encryption}

BRを使用してS3にバックアップするときにS3サーバー側の暗号化を有効にするには、 `--s3.sse`の引数を渡し、値を「aws：kms」に設定します。 S3は、暗号化に独自のKMSキーを使用します。例：

```
./br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.sse aws:kms
```

作成して所有したカスタムAWSKMSCMKを使用するには、さらに`--s3.sse-kms-key-id`を渡します。この場合、BRプロセスとクラスタのすべてのTiKVノードの両方がKMS CMKにアクセスする必要があり（たとえば、AWS IAM経由）、KMSCMKは以前のS3バケットと同じAWSリージョンにある必要がありますバックアップを保存します。 AWSIAMを介してBRプロセスおよびTiKVノードにKMSCMKへのアクセスを許可することをお勧めします。 [わたし](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)の使用法については、AWSのドキュメントを参照してください。例えば：

```
./br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.region <region> --s3.sse aws:kms --s3.sse-kms-key-id 0987dcba-09fe-87dc-65ba-ab0987654321
```

バックアップを復元するときは、 `--s3.sse`と`--s3.sse-kms-key-id`の両方を使用しないでください。 S3はそれ自体で暗号化設定を把握します。バックアップを復元するクラスタのBRプロセスとTiKVノードも、KMS CMKにアクセスする必要があります。そうしないと、復元が失敗します。例：

```
./br restore full --pd <pd-address> --storage "s3://<bucket>/<prefix> --s3.region <region>"
```
