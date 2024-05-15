---
title: Encryption at Rest
summary: Learn how to enable encryption at rest to protect sensitive data.
---

# 保存時の暗号化 {#encryption-at-rest}

> **注記：**
>
> クラスターが AWS にデプロイされ、EBSstorageを使用している場合は、EBS 暗号化を使用することをお勧めします。 [AWS ドキュメント - EBS 暗号化](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)を参照してください。ローカル NVMestorageなど、AWS で非 EBSstorageを使用している場合は、このドキュメントで紹介されている保存時の暗号化を使用することをお勧めします。

保存時の暗号化とは、データが保存時に暗号化されることを意味します。データベースの場合、この機能は TDE (透過的データ暗号化) とも呼ばれます。これは、転送中の暗号化 (TLS) または使用中の暗号化 (まれにしか使用されません) とは対照的です。保存時の暗号化はさまざまなもの (SSD ドライブ、ファイル システム、クラウド ベンダーなど) で実行できますが、TiKV でstorage前に暗号化を実行することで、攻撃者がデータにアクセスするにはデータベースで認証する必要があることが保証されます。たとえば、攻撃者が物理マシンにアクセスした場合、ディスク上のファイルをコピーしてもデータにアクセスすることはできません。

## さまざまな TiDB コンポーネントでの暗号化サポート {#encryption-support-in-different-tidb-components}

TiDB クラスターでは、コンポーネントごとに異なる暗号化方式が使用されます。このセクションでは、TiKV、 TiFlash、PD、Backup &amp; Restore (BR) などのさまざまな TiDB コンポーネントでの暗号化サポートについて説明します。

TiDB クラスターがデプロイされると、ユーザー データの大部分は TiKV ノードとTiFlashノードに保存されます。一部のメタデータは PD ノードに保存されます (たとえば、TiKVリージョン境界として使用されるセカンダリ インデックス キー)。保存時の暗号化のメリットを最大限に活用するには、すべてのコンポーネントで暗号化を有効にする必要があります。暗号化を実装するときは、バックアップ、ログ ファイル、およびネットワーク経由で送信されるデータも考慮する必要があります。

### ティクヴ {#tikv}

TiKV は保存時の暗号化をサポートしています。この機能により、TiKV は[エーエス](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)または[SM4](https://en.wikipedia.org/wiki/SM4_(cipher)) in [CTR](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)モードを使用してデータ ファイルを透過的に暗号化できます。保存時の暗号化を有効にするには、ユーザーが暗号化キーを提供する必要があります。このキーはマスター キーと呼ばれます。TiKV は、実際のデータ ファイルの暗号化に使用したデータ キーを自動的にローテーションします。マスター キーを手動でローテーションすることは時々行うことができます。保存時の暗号化では、保存中のデータ (つまり、ディスク上) のみが暗号化され、データがネットワーク経由で転送されている間は暗号化されないことに注意してください。保存時の暗号化と TLS を併用することをお勧めします。

オプションで、クラウドとセルフホストの両方のデプロイメントに AWS KMS を使用できます。プレーンテキストのマスターキーをファイルで提供することもできます。

TiKV は現在、コア ダンプから暗号化キーとユーザー データを除外しません。保存時に暗号化を使用する場合は、TiKV プロセスのコア ダンプを無効にすることをお勧めします。これは現在、TiKV 自体では処理されません。

TiKV は、ファイルの絶対パスを使用して暗号化されたデータ ファイルを追跡します。そのため、TiKV ノードで暗号化がオンになると、ユーザーは`storage.data-dir` 、 `raftstore.raftdb-path` 、 `rocksdb.wal-dir` 、 `raftdb.wal-dir`などのデータ ファイル パス構成を変更してはなりません。

SM4 暗号化は、TiKV の v6.3.0 以降のバージョンでのみサポートされます。v6.3.0 より前のバージョンの TiKV では、AES 暗号化のみがサポートされます。SM4 暗号化により、スループットが 50% ～ 80% 低下する可能性があります。

### TiFlash {#tiflash}

TiFlash は保存時の暗号化をサポートします。データ キーはTiFlashによって生成されます。TiFlash ( TiFlash Proxy を含む) に書き込まれるTiFlashのファイル (データ ファイル、スキーマ ファイル、一時ファイルを含む) は、現在のデータ キーを使用して暗号化されます。暗号化アルゴリズム、暗号化構成 ( TiFlashでサポートされる[`tiflash-learner.toml`ファイル](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)内)、および監視メトリックの意味は、TiKV のものと一致しています。

Grafana を使用してTiFlash をデプロイした場合は、 **TiFlash-Proxy-Details** -&gt; **Encryption**パネルを確認できます。

SM4 暗号化は、 TiFlashの v6.4.0 以降のバージョンでのみサポートされます。TiFlashのv6.4.0 より前のバージョンでは、AES 暗号化のみがサポートされます。

### PD {#pd}

PD の保存時の暗号化は実験的機能であり、TiKV と同じ方法で構成されます。

### BRによるバックアップ {#backups-with-br}

BR は、S3 にデータをバックアップするときに S3 サーバー側暗号化 (SSE) をサポートします。顧客所有の AWS KMS キーを S3 サーバー側暗号化と併用することもできます。詳細については[BR S3 サーバー側暗号化](/encryption-at-rest.md#br-s3-server-side-encryption)参照してください。

### ログ記録 {#logging}

TiKV、TiDB、および PD 情報ログには、デバッグ目的のユーザー データが含まれる場合があります。情報ログとその中のデータは暗号化されません。1 [ログ編集](/log-redaction.md)有効にすることをお勧めします。

## 保存時の TiKV 暗号化 {#tikv-encryption-at-rest}

### 概要 {#overview}

TiKV は現在、 CTRモードで AES128、AES192、AES256、または SM4 (v6.3.0 以降のバージョンのみ) を使用したデータの暗号化をサポートしています。TiKV はエンベロープ暗号化を使用します。その結果、暗号化が有効になっている場合、TiKV では 2 種類のキーが使用されます。

-   マスター キー。マスター キーはユーザーによって提供され、TiKV が生成するデータ キーを暗号化するために使用されます。マスター キーの管理は TiKV の外部で行われます。
-   データ キー。データ キーは TiKV によって生成され、実際にデータの暗号化に使用されるキーです。

同じマスターキーを TiKV の複数のインスタンスで共有できます。本番環境でマスターキーを提供するための推奨方法は、AWS KMS 経由です。AWS KMS を通じてカスタマーマスターキー (CMK) を作成し、本番ファイルで CMK キー ID を TiKV に提供します。TiKV プロセスは実行中に KMS CMK にアクセスする必要があります。これは[IAMロール](https://aws.amazon.com/iam/)使用して実行できます。TiKV が KMS CMK にアクセスできない場合、起動または再起動に失敗します。3 と[IAMは](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) [ケイエムエス](https://docs.aws.amazon.com/kms/index.html)方法については、AWS ドキュメントを参照してください。

あるいは、カスタム キーを使用する必要がある場合は、ファイル経由でマスター キーを提供することもできます。ファイルには、16 進文字列としてエンコードされた 256 ビット (または 32 バイト) のキーが含まれ、改行 (つまり`\n` ) で終了し、他には何も含まれていない必要があります。ただし、キーをディスク上に保持するとキーが漏洩するため、キー ファイルは RAM の`tempfs`に保存するのに適しています。

データ キーは、基盤となるstorageエンジン (つまり、RocksDB) に渡されます。SST ファイル、WAL ファイル、MANIFEST ファイルなど、RocksDB によって書き込まれるすべてのファイルは、現在のデータ キーで暗号化されます。TiKV によって使用されるその他の一時ファイル (ユーザー データが含まれる場合があります) も、同じデータ キーを使用して暗号化されます。データ キーは、デフォルトでは毎週 TiKV によって自動的にローテーションされますが、期間は構成可能です。キーのローテーションでは、TiKV は既存のすべてのファイルを書き換えてキーを置き換えることはありませんが、クラスターに一定の書き込みワークロードがある場合、RocksDB の圧縮によって、最新のデータ キーを使用して古いデータが新しいデータ ファイルに書き換えられることが予想されます。TiKV は、各ファイルの暗号化に使用されたキーと暗号化方法を追跡し、読み取り時にその情報を使用してコンテンツを復号化します。

データ暗号化方法に関係なく、データ キーは追加の認証のために GCM モードで AES256 を使用して暗号化されます。これにより、KMS ではなくファイルから渡す場合、マスター キーが 256 ビット (32 バイト) である必要がありました。

### キーの作成 {#key-creation}

AWS でキーを作成するには、次の手順に従います。

1.  AWS コンソールの[AWS の](https://console.aws.amazon.com/kms)に移動します。
2.  コンソールの右上隅で正しい地域が選択されていることを確認してください。
3.  **[キーの作成] を**クリックし、キーの種類として**[対称]**を選択します。
4.  キーのエイリアスを設定します。

AWS CLI を使用して操作を実行することもできます。

```shell
aws --region us-west-2 kms create-key
aws --region us-west-2 kms create-alias --alias-name "alias/tidb-tde" --target-key-id 0987dcba-09fe-87dc-65ba-ab0987654321
```

2 番目のコマンドに入力する`--target-key-id` 、最初のコマンドの出力にあります。

### 暗号化を設定する {#configure-encryption}

暗号化を有効にするには、TiKV および PD の設定ファイルに暗号化セクションを追加します。

    [security.encryption]
    data-encryption-method = "aes128-ctr"
    data-key-rotation-period = "168h" # 7 days

`data-encryption-method`に指定できる値は、「aes128-ctr」、「aes192-ctr」、「aes256-ctr」、「sm4-ctr」（v6.3.0 以降のバージョンのみ）および「plaintext」です。デフォルト値は「plaintext」で、暗号化はオンになっていません。3 `data-key-rotation-period` 、TiKV がデータ キーをローテーションする頻度を定義します。暗号化は、新しい TiKV クラスターまたは既存の TiKV クラスターに対してオンにできますが、暗号化が有効になった後に書き込まれたデータのみが暗号化されることが保証されます。暗号化を無効にするには、構成ファイルで`data-encryption-method`を削除するか、「plaintext」にリセットして、TiKV を再起動します。暗号化方式を変更するには、構成ファイルで`data-encryption-method`を更新して、TiKV を再起動します。暗号化アルゴリズムを変更するには、 `data-encryption-method`サポートされている暗号化アルゴリズムに置き換えてから、TiKV を再起動します。置き換え後、新しいデータが書き込まれると、以前の暗号化アルゴリズムによって生成された暗号化ファイルは、新しい暗号化アルゴリズムによって生成されたファイルに徐々に書き換えられます。

暗号化が有効になっている場合は、マスターキーを指定する必要があります (つまり、 `data-encryption-method` 「プレーンテキスト」ではありません)。AWS KMS CMK をマスターキーとして指定するには、 `encryption`セクションの後に`encryption.master-key`セクションを追加します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"
    endpoint = "https://kms.us-west-2.amazonaws.com"

`key-id` KMS CMK のキー ID を指定します。 `region` KMS CMK の AWS リージョン名です。 `endpoint`はオプションであり、AWS 以外のベンダーの AWS KMS 互換サービスを使用している場合や[KMS の VPC エンドポイント](https://docs.aws.amazon.com/kms/latest/developerguide/kms-vpc-endpoint.html)を使用する必要がない限り、通常は指定する必要はありません。

AWS では[マルチリージョンキー](https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html)使用することもできます。そのためには、特定のリージョンにプライマリキーを設定し、必要なリージョンにレプリカキーを追加する必要があります。

ファイルに保存されているマスター キーを指定するには、マスター キーの構成は次のようになります。

    [security.encryption.master-key]
    type = "file"
    path = "/path/to/key/file"

ここで`path`キー ファイルへのパスです。ファイルには 16 進文字列としてエンコードされた 256 ビット (または 32 バイト) のキーが含まれ、改行 ( `\n` ) で終わり、他には何も含まれていない必要があります。ファイルの内容の例:

    3b5896b5be691006e0f71c3040a29495ddcad20b14aff61806940ebd780d3c62

### マスターキーを回転する {#rotate-the-master-key}

マスター キーをローテーションするには、設定で新しいマスター キーと古いマスター キーの両方を指定して、TiKV を再起動する必要があります。新しいマスター キーを指定するには`security.encryption.master-key`使用し、古いマスター キーを指定するには`security.encryption.previous-master-key`を使用します。 `security.encryption.previous-master-key`の設定形式は`encryption.master-key`と同じです。再起動時に TiKV は古いマスター キーと新しいマスター キーの両方にアクセスする必要がありますが、TiKV が起動して実行されると、TiKV は新しいキーのみにアクセスする必要があります。それ以降は、設定ファイルに`encryption.previous-master-key`設定を残しておいても問題ありません。再起動しても、TiKV は新しいマスター キーを使用して既存のデータを復号化できなかった場合にのみ、古いキーを使用しようとします。

現在、オンライン マスター キーのローテーションはサポートされていないため、TiKV を再起動する必要があります。オンライン クエリを処理する実行中の TiKV クラスターに対してローリング再起動を実行することをお勧めします。

KMS CMK をローテーションするための構成例を次に示します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
    region = "us-west-2"

    [security.encryption.previous-master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"

### 監視とデバッグ {#monitoring-and-debugging}

保存時の暗号化を監視するには、Grafana を使用して TiKV をデプロイし、 **TiKV-Details**ダッシュボードの**暗号化**パネルを確認します。確認すべきメトリックがいくつかあります。

-   暗号化が初期化されました: TiKV の起動中に暗号化が初期化された場合は 1、それ以外の場合は 0。マスター キーのローテーションの場合、暗号化が初期化された後、TiKV は以前のマスター キーにアクセスする必要はありません。
-   暗号化データ キー: 既存のデータ キーの数。データ キーのローテーションが発生するたびに、この数は 1 ずつ増加します。このメトリックを使用して、データ キーのローテーションが期待どおりに機能するかどうかを監視します。
-   暗号化されたファイル: 現在存在する暗号化されたデータ ファイルの数。この数をデータ ディレクトリ内の既存のデータ ファイルと比較して、以前に暗号化されていなかったクラスターの暗号化をオンにするときに、暗号化されるデータの部分を推定します。
-   暗号化メタファイル サイズ: 暗号化メタデータ ファイルのサイズ。
-   読み取り/書き込み暗号化メタ期間: 暗号化のメタデータを操作するための追加のオーバーヘッド。

デバッグの場合、 `tikv-ctl`コマンドを使用して、ファイルの暗号化に使用された暗号化方法やデータ キー ID、データ キーのリストなどの暗号化メタデータをダンプできます。この操作により機密データが公開される可能性があるため、本番での使用は推奨されません[TiKV Control](/tikv-control.md#dump-encryption-metadata)ドキュメントを参照してください。

### TiKVバージョン間の互換性 {#compatibility-between-tikv-versions}

TiKV が暗号化メタデータを管理するときに I/O とミューテックスの競合によって発生するオーバーヘッドを削減するために、TiKV v4.0.9 で最適化が導入され、TiKV 構成ファイルの`security.encryption.enable-file-dictionary-log`によって制御されます。この構成パラメータは、TiKV v4.0.9 以降のバージョンでのみ有効です。

有効になっている場合 (デフォルト)、暗号化メタデータのデータ形式は TiKV v4.0.8 以前のバージョンでは認識されません。たとえば、保存時の暗号化とデフォルトの`enable-file-dictionary-log`構成で TiKV v4.0.9 以降を使用しているとします。クラスターを TiKV v4.0.8 以前にダウングレードすると、TiKV は起動に失敗し、情報ログに次のようなエラーが記録されます。

    [2020/12/07 07:26:31.106 +08:00] [ERROR] [mod.rs:110] ["encryption: failed to load file dictionary."]
    [2020/12/07 07:26:33.598 +08:00] [FATAL] [lib.rs:483] ["called `Result::unwrap()` on an `Err` value: Other(\"[components/encryption/src/encrypted_file/header.rs:18]: unknown version 2\")"]

上記のエラーを回避するには、まず`security.encryption.enable-file-dictionary-log`を`false`に設定し、TiKV を v4.0.9 以降で起動します。TiKV が正常に起動すると、暗号化メタデータのデータ形式が、以前の TiKV バージョンで認識できるバージョンにダウングレードされます。この時点で、TiKV クラスターを以前のバージョンにダウングレードできます。

## 保存時のTiFlash暗号化 {#tiflash-encryption-at-rest}

### 概要 {#overview}

現在TiFlashでサポートされている暗号化アルゴリズムは、 CTRモードの AES128、AES192、AES256、および SM4 (v6.4.0 以降のバージョンのみ) を含む、TiKV でサポートされているアルゴリズムと一致しています。TiFlashはエンベロープ暗号化も使用します。したがって、暗号化が有効になっている場合、 TiFlashでは 2 種類のキーが使用されます。

-   マスター キー。マスター キーはユーザーによって提供され、 TiFlashが生成するデータ キーを暗号化するために使用されます。マスター キーの管理はTiFlashの外部で行われます。
-   データ キー。データ キーはTiFlashによって生成され、実際にデータの暗号化に使用されるキーです。

同じマスターキーをTiFlashの複数のインスタンスで共有できます。また、 TiFlashと TiKV 間で共有することもできます。本番でマスターキーを提供する場合は、AWS KMS を使用することをお勧めします。また、カスタムキーを使用する場合は、ファイル経由でマスターキーを提供することもできます。マスターキーを生成する具体的な方法とマスターキーの形式は、TiKV と同じです。

TiFlashは、現在のデータ キーを使用して、データ ファイル、スキーマ ファイル、計算中に生成された一時データ ファイルなど、ディスク上に配置されているすべてのデータを暗号化します。データ キーは、デフォルトでは毎週TiFlashによって自動的にローテーションされますが、その期間は構成可能です。キー ローテーションでは、 TiFlash は既存のすべてのファイルを書き換えてキーを置き換えることはありませんが、クラスターに一定の書き込みワークロードがある場合、バックグラウンド コンパクション タスクによって、最新のデータ キーを使用して古いデータが新しいデータ ファイルに書き換えられることが予想されます。TiFlashは、各ファイルの暗号化に使用されたキーと暗号化方法を追跡し、その情報を使用して読み取り時にコンテンツを復号化します。

### キーの作成 {#key-creation}

AWS でキーを作成するには、TiKV のキーを作成する手順を参照してください。

### 暗号化を設定する {#configure-encryption}

暗号化を有効にするには、 `tiflash-learner.toml`構成ファイルに暗号化セクションを追加します。

    [security.encryption]
    data-encryption-method = "aes128-ctr"
    data-key-rotation-period = "168h" # 7 days

または、 TiUPクラスター テンプレートに次のコンテンツを追加します。

    server_configs:
      tiflash-learner:
        security.encryption.data-encryption-method: "aes128-ctr"
        security.encryption.data-key-rotation-period: "168h" # 7 days

`data-encryption-method`に指定できる値は、「aes128-ctr」、「aes192-ctr」、「aes256-ctr」、「sm4-ctr」（v6.4.0 以降のバージョンのみ）および「plaintext」です。デフォルト値は「plaintext」で、暗号化はオンになっていません。3 `data-key-rotation-period` 、 TiFlash がデータ キーをローテーションする頻度を定義します。暗号化は、新しいTiFlashクラスターまたは既存のTiFlashクラスターに対してオンにできますが、暗号化が有効になった後に書き込まれたデータのみが暗号化されることが保証されます。暗号化を無効にするには、構成ファイルで`data-encryption-method`を削除するか、「plaintext」にリセットして、 TiFlashを再起動します。暗号化方式を変更するには、構成ファイルで`data-encryption-method`を更新して、 TiFlashを再起動します。暗号化アルゴリズムを変更するには、サポートされている暗号化アルゴリズムで`data-encryption-method`を置き換えてから、 TiFlashを再起動します。置き換え後、新しいデータが書き込まれると、以前の暗号化アルゴリズムによって生成された暗号化ファイルは、新しい暗号化アルゴリズムによって生成されたファイルに徐々に書き換えられます。

暗号化が有効になっている場合は、マスターキーを指定する必要があります (つまり、 `data-encryption-method` 「プレーンテキスト」ではありません)。AWS KMS CMK をマスターキーとして指定するには、 `tiflash-learner.toml`構成ファイルの`encryption`セクションの後に`encryption.master-key`セクションを追加します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"
    endpoint = "https://kms.us-west-2.amazonaws.com"

または、 TiUPクラスター テンプレートに次のコンテンツを追加します。

    server_configs:
      tiflash-learner:
        security.encryption.master-key.type: "kms"
        security.encryption.master-key.key-id: "0987dcba-09fe-87dc-65ba-ab0987654321"
        security.encryption.master-key.region: "us-west-2"
        security.encryption.master-key.endpoint: "https://kms.us-west-2.amazonaws.com"

上記の設定項目の意味はTiKVと同じです。

ファイルに保存されているマスター キーを指定するには、 `tiflash-learner.toml`構成ファイルに次の構成を追加します。

    [security.encryption.master-key]
    type = "file"
    path = "/path/to/key/file"

または、 TiUPクラスター テンプレートに次のコンテンツを追加します。

    server_configs:
      tiflash-learner:
        security.encryption.master-key.type: "file"
        security.encryption.master-key.path: "/path/to/key/file"

上記の設定項目の意味やキーファイルの内容形式はTiKVと同じです。

### マスターキーを回転する {#rotate-the-master-key}

TiFlashのマスター キーをローテーションするには、TiKV のマスター キーをローテーションする手順に従います。現在、 TiFlash はオンラインでのマスター キーのローテーションもサポートしていません。したがって、ローテーションを有効にするには、 TiFlashを再起動する必要があります。オンライン クエリを処理する実行中のTiFlashクラスターに対してローリング再起動を実行することをお勧めします。

KMS CMK をローテーションするには、 `tiflash-learner.toml`構成ファイルに次の内容を追加します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
    region = "us-west-2"

    [security.encryption.previous-master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"

または、 TiUPクラスター テンプレートに次のコンテンツを追加します。

    server_configs:
      tiflash-learner:
        security.encryption.master-key.type: "kms"
        security.encryption.master-key.key-id: "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
        security.encryption.master-key.region: "us-west-2"
        security.encryption.previous-master-key.type: "kms"
        security.encryption.previous-master-key.key-id: "0987dcba-09fe-87dc-65ba-ab0987654321"
        security.encryption.previous-master-key.region: "us-west-2"

### 監視とデバッグ {#monitoring-and-debugging}

保存時の暗号化を監視するには、Grafana でTiFlashをデプロイすると、 **TiFlash-Proxy-Details**ダッシュボードの**暗号化**パネルを確認できます。監視項目の意味は TiKV と同じです。

デバッグの場合、 TiFlash は暗号化されたメタデータの管理に TiKV のロジックを再利用するため、 `tikv-ctl`コマンドを使用して、ファイルの暗号化に使用された暗号化方法やデータ キー ID、データ キーのリストなどの暗号化メタデータをダンプできます。この操作により機密データが漏洩する可能性があるため、本番では推奨されません。詳細については、 [TiKV Control](/tikv-control.md#dump-encryption-metadata)を参照してください。

### TiKVバージョン間の互換性 {#compatibility-between-tikv-versions}

TiFlashも v4.0.9 で暗号化されたメタデータ操作を最適化しており、互換性要件は TiKV と同じです。詳細については[TiKVバージョン間の互換性](#compatibility-between-tikv-versions)参照してください。

## BR S3 サーバー側暗号化 {#br-s3-server-side-encryption}

BRを使用して S3 にバックアップするときに S3 サーバー側の暗号化を有効にするには、引数を`--s3.sse`渡し、値を「aws:kms」に設定します。S3 は暗号化に独自の KMS キーを使用します。例:

    ./br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.sse aws:kms

作成して所有しているカスタム AWS KMS CMK を使用するには、さらに`--s3.sse-kms-key-id`渡します。この場合、 BRプロセスとクラスター内のすべての TiKV ノードの両方が KMS CMK にアクセスする必要があり (たとえば、AWS IAM経由)、KMS CMK はバックアップの保存に使用される S3 バケットと同じ AWS リージョンにある必要があります。AWS IAM経由でBRプロセスと TiKV ノードに KMS CMK へのアクセスを許可することをお勧めします。3 [IAMは](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)使用方法については、AWS ドキュメントを参照してください。例:

    ./br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.sse aws:kms --s3.sse-kms-key-id 0987dcba-09fe-87dc-65ba-ab0987654321

バックアップを復元する場合、 `--s3.sse`と`--s3.sse-kms-key-id`両方を使用しないでください。S3 は暗号化設定を独自に判断します。バックアップを復元するクラスター内のBRプロセスと TiKV ノードも KMS CMK にアクセスする必要があります。そうしないと、復元が失敗します。例:

    ./br restore full --pd <pd-address> --storage "s3://<bucket>/<prefix>"

## BR Azure Blob Storage サーバー側暗号化 {#br-azure-blob-storage-server-side-encryption}

BRを使用して Azure Blob Storage にデータをバックアップする場合、サーバー側の暗号化の暗号化スコープまたは暗号化キーのいずれかを指定できます。

### 方法1: 暗号化スコープを使用する {#method-1-use-an-encryption-scope}

バックアップ データの暗号化範囲を指定するには、次の 2 つの方法のいずれかを使用できます。

-   `backup`コマンドに`--azblob.encryption-scope`オプションを含め、スコープ名に設定します。

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-scope scope1
    ```

-   URI に`encryption-scope`含め、スコープ名に設定します。

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-scope=scope1"
    ```

詳細については、Azure のドキュメント[暗号化スコープ付きのBLOBをアップロードする](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-scope-manage?tabs=powershell#upload-a-blob-with-an-encryption-scope)を参照してください。

バックアップを復元するときに、暗号化の範囲を指定する必要はありません。Azure Blob Storage はデータを自動的に復号化します。例:

```shell
./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
```

### 方法2: 暗号化キーを使用する {#method-2-use-an-encryption-key}

バックアップ データの暗号化キーを指定するには、次の 3 つの方法のいずれかを使用できます。

-   `backup`コマンドに`--azblob.encryption-key`オプションを含め、AES256 暗号化キーを設定します。

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-key <aes256-key>
    ```

-   URI に`encryption-key`含め、それを AES256 暗号化キーに設定します。キーに`&`や`%`などの URI 予約文字が含まれている場合は、最初にパーセントエンコードする必要があります。

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-key=<aes256-key>"
    ```

-   `AZURE_ENCRYPTION_KEY`環境変数を AES256 暗号化キーに設定します。実行する前に、暗号化キーを忘れないように環境変数に必ず記録しておいてください。

    ```shell
    export AZURE_ENCRYPTION_KEY=<aes256-key>
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
    ```

詳細については、Azure のドキュメント[Blobstorageへのリクエストに暗号化キーを提供する](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-customer-provided-keys)を参照してください。

バックアップを復元するときは、暗号化キーを指定する必要があります。例:

-   `restore`コマンドに`--azblob.encryption-key`オプションを含めます。

    ```shell
    ./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-key <aes256-key>
    ```

-   URIに`encryption-key`含めます:

    ```shell
    ./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-key=<aes256-key>"
    ```

-   `AZURE_ENCRYPTION_KEY`環境変数を設定します。

    ```shell
    export AZURE_ENCRYPTION_KEY=<aes256-key>
    ./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
    ```
