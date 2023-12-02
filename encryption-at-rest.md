---
title: Encryption at Rest
summary: Learn how to enable encryption at rest to protect sensitive data.
---

# 保存時の暗号化 {#encryption-at-rest}

> **注記：**
>
> クラスターが AWS にデプロイされ、EBSstorageを使用する場合は、EBS 暗号化を使用することをお勧めします。 [AWS ドキュメント - EBS 暗号化](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)を参照してください。 AWS でローカル NVMestorageなどの非 EBSstorageを使用している場合、このドキュメントで紹介されている保存時の暗号化を使用することをお勧めします。

保存時の暗号化とは、データが保存されるときに暗号化されることを意味します。データベースの場合、この機能は TDE (透過的データ暗号化) とも呼ばれます。これは、実行中の暗号化 (TLS) または使用中の暗号化 (めったに使用されない) とは対照的です。保存時の暗号化はさまざまなもの (SSD ドライブ、ファイル システム、クラウド ベンダーなど) で実行される可能性がありますが、TiKV にstorage前に暗号化を実行させることで、攻撃者がデータにアクセスするためにデータベースで認証する必要があることが保証されます。たとえば、攻撃者が物理マシンにアクセスした場合、ディスク上のファイルをコピーしてもデータにアクセスできなくなります。

## さまざまな TiDB コンポーネントでの暗号化のサポート {#encryption-support-in-different-tidb-components}

TiDB クラスターでは、コンポーネントごとに異なる暗号化方式が使用されます。このセクションでは、TiKV、 TiFlash、PD、バックアップ &amp; リストア (BR) などのさまざまな TiDB コンポーネントでの暗号化サポートを紹介します。

TiDB クラスターが展開されると、ユーザー データの大部分は TiKV ノードとTiFlashノードに保存されます。一部のメタデータは PD ノードに保存されます (たとえば、TiKVリージョン境界として使用されるセカンダリ インデックス キー)。保存時の暗号化の利点を最大限に活用するには、すべてのコンポーネントの暗号化を有効にする必要があります。暗号化を実装する場合は、バックアップ、ログ ファイル、ネットワーク経由で送信されるデータも考慮する必要があります。

### TiKV {#tikv}

TiKV は保存時の暗号化をサポートしています。この機能により、TiKV は[AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)または[SM4](https://en.wikipedia.org/wiki/SM4_(cipher)) in [CTR](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)モードを使用してデータ ファイルを透過的に暗号化できます。保管時の暗号化を有効にするには、ユーザーが暗号化キーを提供する必要があります。このキーはマスターキーと呼ばれます。 TiKV は、実際のデータ ファイルの暗号化に使用したデータ キーを自動的にローテーションします。マスターキーを手動でローテーションすることもできます。保存時の暗号化では、保存時 (つまりディスク上) のデータのみが暗号化され、ネットワーク上でのデータ転送中は暗号化されないことに注意してください。保存時の暗号化と TLS を併用することをお勧めします。

オプションで、クラウド展開とセルフホスト展開の両方に AWS KMS を使用できます。プレーンテキストのマスター キーをファイルで指定することもできます。

TiKV は現在、コア ダンプから暗号化キーとユーザー データを除外していません。保存時の暗号化を使用する場合は、TiKV プロセスのコア ダンプを無効にすることをお勧めします。これは現在、TiKV 自体では処理されていません。

TiKV は、ファイルの絶対パスを使用して暗号化されたデータ ファイルを追跡します。その結果、TiKV ノードの暗号化が有効になったら、ユーザーは`storage.data-dir` 、 `raftstore.raftdb-path` 、 `rocksdb.wal-dir` 、 `raftdb.wal-dir`などのデータ ファイル パス構成を変更する必要はありません。

SM4 暗号化は、TiKV の v6.3.0 以降のバージョンでのみサポートされます。 v6.3.0 より前の TiKV バージョンは、AES 暗号化のみをサポートします。 SM4 暗号化により、スループットが 50% ～ 80% 低下する可能性があります。

### TiFlash {#tiflash}

TiFlash は保存時の暗号化をサポートしています。データキーはTiFlashによって生成されます。 TiFlash ( TiFlashプロキシを含む) に書き込まれるすべてのファイル (データ ファイル、スキーマ ファイル、一時ファイルを含む) は、現在のデータ キーを使用して暗号化されます。暗号化アルゴリズム、暗号化構成 ( TiFlashでサポートされている[`tiflash-learner.toml`ファイル](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)暗号化構成)、および監視メトリクスの意味は、TiKV のものと一致しています。

Grafana を使用してTiFlashを展開した場合は、 **「TiFlash-Proxy-Details** -&gt; **Encryption」**パネルを確認できます。

SM4 暗号化は、 TiFlashの v6.4.0 以降のバージョンでのみサポートされています。 v6.4.0 より前のTiFlashバージョンは、AES 暗号化のみをサポートします。

### PD {#pd}

PD の保存時の暗号化は実験的機能であり、TiKV と同じ方法で構成されます。

### BRを使用したバックアップ {#backups-with-br}

BR は、 S3 にデータをバックアップする際の S3 サーバー側暗号化 (SSE) をサポートします。顧客所有の AWS KMS キーは、S3 サーバー側の暗号化と併用することもできます。詳細については[BR S3 サーバー側暗号化](/encryption-at-rest.md#br-s3-server-side-encryption)を参照してください。

### ロギング {#logging}

TiKV、TiDB、および PD 情報ログには、デバッグ目的のユーザー データが含まれる場合があります。情報ログとその中のデータは暗号化されません。 [ログ編集](/log-redaction.md)を有効にすることをお勧めします。

## 保存時の TiKV 暗号化 {#tikv-encryption-at-rest}

### 概要 {#overview}

TiKV は現在、 CTRモードで AES128、AES192、AES256、または SM4 (v6.3.0 以降のバージョンのみ) を使用したデータの暗号化をサポートしています。 TiKV はエンベロープ暗号化を使用します。その結果、暗号化が有効な場合、TiKV では 2 種類のキーが使用されます。

-   マスターキー。マスター キーはユーザーによって提供され、TiKV が生成するデータ キーの暗号化に使用されます。マスターキーの管理は TiKV の外部で行われます。
-   データキー。データ キーは TiKV によって生成され、データの暗号化に実際に使用されるキーです。

同じマスター キーを TiKV の複数のインスタンスで共有できます。本番でマスターキーを提供する推奨方法は、AWS KMS を使用することです。 AWS KMS を通じてカスタマーマスターキー (CMK) を作成し、構成ファイルで CMK キー ID を TiKV に提供します。 TiKV プロセスは、実行中に KMS CMK にアクセスする必要があります。これは、 [IAMの役割](https://aws.amazon.com/iam/)を使用して実行できます。 TiKV が KMS CMK へのアクセスに失敗すると、起動または再起動に失敗します。 [KMS](https://docs.aws.amazon.com/kms/index.html)と[IAMは](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)使用法については、AWS のドキュメントを参照してください。

あるいは、カスタム キーの使用が必要な場合は、ファイル経由でマスター キーを指定することもできます。ファイルには、16 進文字列としてエンコードされた 256 ビット (または 32 バイト) のキーが含まれ、改行 (つまり`\n` ) で終わり、他には何も含まれていない必要があります。ただし、キーをディスク上に保存するとキーが漏洩するため、キー ファイルは`tempfs`に保存するのにのみ適しています。

データ キーは、基盤となるstorageエンジン (つまり、RocksDB) に渡されます。 SST ファイル、WAL ファイル、MANIFEST ファイルなど、RocksDB によって書き込まれるすべてのファイルは、現在のデータ キーによって暗号化されます。 TiKV が使用する、ユーザー データを含む可能性のある他の一時ファイルも、同じデータ キーを使用して暗号化されます。データ キーは、デフォルトでは TiKV によって毎週自動的にローテーションされますが、その期間は構成可能です。キーのローテーションの際、TiKV は既存のすべてのファイルを書き換えてキーを置き換えることはしませんが、クラスターに一定の書き込みワークロードがかかる場合、RocksDB の圧縮は最新のデータ キーを使用して古いデータを新しいデータ ファイルに書き換えることが期待されます。 TiKV は、各ファイルの暗号化に使用されたキーと暗号化方式を追跡し、その情報を使用して読み取り時にコンテンツを復号化します。

データ暗号化方式に関係なく、追加の認証のためにデータ キーは GCM モードの AES256 を使用して暗号化されます。これには、KMS ではなくファイルから渡す場合、マスター キーが 256 ビット (32 バイト) である必要がありました。

### キーの作成 {#key-creation}

AWS でキーを作成するには、次の手順に従います。

1.  AWS コンソールの[AWS KMS](https://console.aws.amazon.com/kms)に移動します。
2.  コンソールの右上隅で正しいリージョンを選択していることを確認してください。
3.  **「キーの作成」**をクリックし、キーのタイプとして**「対称」**を選択します。
4.  キーのエイリアスを設定します。

AWS CLI を使用して操作を実行することもできます。

```shell
aws --region us-west-2 kms create-key
aws --region us-west-2 kms create-alias --alias-name "alias/tidb-tde" --target-key-id 0987dcba-09fe-87dc-65ba-ab0987654321
```

2 番目のコマンドに入力する`--target-key-id`最初のコマンドの出力に含まれています。

### 暗号化を構成する {#configure-encryption}

暗号化を有効にするには、TiKV と PD の構成ファイルに暗号化セクションを追加します。

    [security.encryption]
    data-encryption-method = "aes128-ctr"
    data-key-rotation-period = "168h" # 7 days

`data-encryption-method`に指定できる値は、「aes128-ctr」、「aes192-ctr」、「aes256-ctr」、「sm4-ctr」 (v6.3.0 以降のバージョンのみ)、および「plaintext」です。デフォルト値は「平文」で、暗号化が有効になっていないことを意味します。 `data-key-rotation-period` TiKV がデータキーをローテーションする頻度を定義します。暗号化は新しい TiKV クラスターまたは既存の TiKV クラスターに対してオンにできますが、暗号化が保証されるのは暗号化が有効になった後に書き込まれたデータのみです。暗号化を無効にするには、構成ファイルの`data-encryption-method`削除するか、「平文」にリセットして、TiKV を再起動します。暗号化方式を変更するには、構成ファイルの`data-encryption-method`を更新し、TiKV を再起動します。暗号化アルゴリズムを変更するには、 `data-encryption-method`サポートされている暗号化アルゴリズムに置き換えてから、TiKV を再起動します。置き換え後、新たなデータが書き込まれると、以前の暗号アルゴリズムで生成された暗号化ファイルが、新しい暗号アルゴリズムで生成されたファイルに徐々に書き換えられます。

暗号化が有効な場合 (つまり、 `data-encryption-method`が「平文」ではない場合)、マスター キーを指定する必要があります。 AWS KMS CMK をマスターキーとして指定するには、 `encryption`セクションの後に`encryption.master-key`セクションを追加します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"
    endpoint = "https://kms.us-west-2.amazonaws.com"

`key-id` KMS CMK のキー ID を指定します。 `region` 、KMS CMK の AWS リージョン名です。 `endpoint`はオプションであり、AWS 以外のベンダーの AWS KMS 互換サービスを使用している場合、または[KMS の VPC エンドポイント](https://docs.aws.amazon.com/kms/latest/developerguide/kms-vpc-endpoint.html)を使用する必要がある場合を除き、通常は指定する必要はありません。

[マルチリージョンキー](https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html) AWS でも使用できます。このためには、特定のリージョンに主キーを設定し、必要なリージョンにレプリカ キーを追加する必要があります。

ファイルに保存されているマスター キーを指定するには、マスター キーの構成は次のようになります。

    [security.encryption.master-key]
    type = "file"
    path = "/path/to/key/file"

ここで`path`キー ファイルへのパスです。ファイルには、16 進文字列としてエンコードされた 256 ビット (または 16 バイト) のキーが含まれており、改行 ( `\n` ) で終わり、他には何も含まれていない必要があります。ファイルの内容の例:

    3b5896b5be691006e0f71c3040a29495ddcad20b14aff61806940ebd780d3c62

### マスターキーを回転させます {#rotate-the-master-key}

マスター キーをローテーションするには、構成で新しいマスター キーと古いマスター キーの両方を指定し、TiKV を再起動する必要があります。新しいマスター キーを指定するには`security.encryption.master-key`使用し、古いマスター キーを指定するには`security.encryption.previous-master-key`を使用します。 `security.encryption.previous-master-key`の構成形式は`encryption.master-key`と同じです。再起動時に、TiKV は古いマスター キーと新しいマスター キーの両方にアクセスする必要がありますが、一度 TiKV が起動して実行されると、TiKV は新しいキーにのみアクセスする必要があります。以降、設定ファイルには`encryption.previous-master-key`設定を残しておいて大丈夫です。再起動時でも、TiKV は、新しいマスター キーを使用して既存のデータを復号化できない場合にのみ、古いキーの使用を試みます。

現在、オンライン マスター キーのローテーションはサポートされていないため、TiKV を再起動する必要があります。オンライン クエリを提供する実行中の TiKV クラスターに対してローリング再起動を実行することをお勧めします。

KMS CMK をローテーションするための設定例を次に示します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
    region = "us-west-2"

    [security.encryption.previous-master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"

### モニタリングとデバッグ {#monitoring-and-debugging}

保存時の暗号化を監視するには、Grafana を使用して TiKV を展開する場合、 **TiKV-Details**ダッシュボードの**[暗号化]**パネルを確認できます。探すべき指標がいくつかあります。

-   暗号化が初期化されました: TiKV の起動中に暗号化が初期化された場合は 1、それ以外の場合は 0。マスター キーのローテーションの場合、暗号化が初期化された後、TiKV は以前のマスター キーにアクセスする必要はありません。
-   暗号化データキー: 既存のデータキーの数。データ キーのローテーションが発生するたびに、数値は 1 ずつ増加します。このメトリクスを使用して、データ キーのローテーションが期待どおりに機能するかどうかを監視します。
-   暗号化されたファイル: 現在存在する暗号化されたデータ ファイルの数。以前に暗号化されていないクラスターの暗号化をオンにする場合、この数値をデータ ディレクトリ内の既存のデータ ファイルと比較して、暗号化されるデータの部分を推定します。
-   暗号化メタファイルのサイズ: 暗号化メタデータファイルのサイズ。
-   読み取り/書き込み暗号化メタ期間: 暗号化のためにメタデータを操作するための追加のオーバーヘッド。

デバッグの場合、 `tikv-ctl`コマンドを使用して、ファイルの暗号化に使用された暗号化方法やデータ キー ID などの暗号化メタデータ、およびデータ キーのリストをダンプできます。この操作により機密データが公開される可能性があるため、本番での使用はお勧めできません。資料[TiKV Control](/tikv-control.md#dump-encryption-metadata)をご参照ください。

### TiKV バージョン間の互換性 {#compatibility-between-tikv-versions}

TiKV が暗号化メタデータを管理するときに I/O とミューテックスの競合によって発生するオーバーヘッドを軽減するために、TiKV v4.0.9 では最適化が導入され、TiKV 構成ファイルの`security.encryption.enable-file-dictionary-log`によって制御されます。この設定パラメータは、TiKV v4.0.9 以降のバージョンでのみ有効です。

これが有効になっている場合 (デフォルト)、暗号化メタデータのデータ形式は TiKV v4.0.8 以前のバージョンでは認識できません。たとえば、保存時の暗号化とデフォルトの`enable-file-dictionary-log`構成で TiKV v4.0.9 以降を使用すると仮定します。クラスターを TiKV v4.0.8 以前にダウングレードすると、TiKV は起動に失敗し、情報ログに次のようなエラーが表示されます。

    [2020/12/07 07:26:31.106 +08:00] [ERROR] [mod.rs:110] ["encryption: failed to load file dictionary."]
    [2020/12/07 07:26:33.598 +08:00] [FATAL] [lib.rs:483] ["called `Result::unwrap()` on an `Err` value: Other(\"[components/encryption/src/encrypted_file/header.rs:18]: unknown version 2\")"]

上記のエラーを回避するには、まず`security.encryption.enable-file-dictionary-log` ～ `false`を設定し、TiKV を v4.0.9 以降で起動します。 TiKV が正常に起動すると、暗号化メタデータのデータ形式が、以前の TiKV バージョンで認識可能なバージョンにダウングレードされます。この時点で、TiKV クラスターを以前のバージョンにダウングレードできます。

## 保存時のTiFlash暗号化 {#tiflash-encryption-at-rest}

### 概要 {#overview}

TiFlashで現在サポートされている暗号化アルゴリズムは、 CTRモードで TiKV でサポートされている AES128、AES192、AES256、SM4 (v6.4.0 以降のバージョンのみ) などの暗号化アルゴリズムと一致しています。 TiFlash はエンベロープ暗号化も使用します。したがって、暗号化が有効な場合、 TiFlashでは 2 種類のキーが使用されます。

-   マスターキー。マスター キーはユーザーによって提供され、 TiFlashが生成するデータ キーの暗号化に使用されます。マスター キーの管理はTiFlashの外部で行われます。
-   データキー。データ キーはTiFlashによって生成され、データの暗号化に実際に使用されるキーです。

同じマスター キーをTiFlashの複数のインスタンスで共有でき、またTiFlashと TiKV の間で共有することもできます。本番でマスターキーを提供する推奨方法は、AWS KMS を使用することです。あるいは、カスタム キーの使用が必要な場合は、ファイル経由でマスター キーを指定することもできます。具体的なマスターキーの生成方法やマスターキーの形式はTiKVと同様です。

TiFlash は、現在のデータ キーを使用して、データ ファイル、Schmea ファイル、計算中に生成される一時データ ファイルなど、ディスク上に配置されたすべてのデータを暗号化します。データ キーは、デフォルトではTiFlashによって毎週自動的にローテーションされ、その期間は構成可能です。キーのローテーション時に、 TiFlash はすべての既存ファイルを書き換えてキーを置き換えることはしませんが、クラスターに一定の書き込みワークロードがかかる場合、バックグラウンド圧縮タスクは最新のデータ キーを使用して古いデータを新しいデータ ファイルに書き換えることが期待されます。 TiFlash は、各ファイルの暗号化に使用されたキーと暗号化方式を追跡し、その情報を使用して読み取り時にコンテンツを復号化します。

### キーの作成 {#key-creation}

AWS でキーを作成するには、TiKV のキーを作成する手順を参照してください。

### 暗号化を構成する {#configure-encryption}

暗号化を有効にするには、 `tiflash-learner.toml`構成ファイルに暗号化セクションを追加します。

    [security.encryption]
    data-encryption-method = "aes128-ctr"
    data-key-rotation-period = "168h" # 7 days

あるいは、 TiUPクラスター テンプレートに次の内容を追加します。

    server_configs:
      tiflash-learner:
        security.encryption.data-encryption-method: "aes128-ctr"
        security.encryption.data-key-rotation-period: "168h" # 7 days

`data-encryption-method`に指定できる値は、「aes128-ctr」、「aes192-ctr」、「aes256-ctr」、「sm4-ctr」 (v6.4.0 以降のバージョンのみ)、および「plaintext」です。デフォルト値は「平文」で、暗号化が有効になっていないことを意味します。 `data-key-rotation-period` TiFlash がデータ キーをローテーションする頻度を定義します。暗号化は新しいTiFlashクラスターまたは既存のTiFlashクラスターに対してオンにできますが、暗号化が保証されるのは暗号化が有効になった後に書き込まれたデータのみです。暗号化を無効にするには、構成ファイルの`data-encryption-method`削除するか、「プレーンテキスト」にリセットして、 TiFlashを再起動します。暗号化方式を変更するには、構成ファイルの`data-encryption-method`を更新し、 TiFlashを再起動します。暗号化アルゴリズムを変更するには、 `data-encryption-method`サポートされている暗号化アルゴリズムに置き換えてから、 TiFlashを再起動します。置き換え後、新たなデータが書き込まれると、以前の暗号アルゴリズムで生成された暗号化ファイルが、新しい暗号アルゴリズムで生成されたファイルに徐々に書き換えられます。

暗号化が有効な場合 (つまり、 `data-encryption-method`が「平文」ではない場合)、マスター キーを指定する必要があります。 AWS KMS CMK をマスターキーとして指定するには、 `tiflash-learner.toml`設定ファイルの`encryption`セクションの後に`encryption.master-key`セクションを追加します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"
    endpoint = "https://kms.us-west-2.amazonaws.com"

あるいは、 TiUPクラスター テンプレートに次の内容を追加します。

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

あるいは、 TiUPクラスター テンプレートに次の内容を追加します。

    server_configs:
      tiflash-learner:
        security.encryption.master-key.type: "file"
        security.encryption.master-key.path: "/path/to/key/file"

上記の設定項目の意味やキーファイルの内容形式はTiKVと同様です。

### マスターキーを回転させます {#rotate-the-master-key}

TiFlashのマスター キーをローテーションするには、TiKV のマスター キーをローテーションする手順に従います。現在、 TiFlash はオンライン マスター キーのローテーションもサポートしていません。したがって、回転を有効にするには、 TiFlashを再起動する必要があります。オンライン クエリを提供する実行中のTiFlashクラスターに対してローリング再起動を実行することをお勧めします。

KMS CMK をローテーションするには、 `tiflash-learner.toml`構成ファイルに次の内容を追加します。

    [security.encryption.master-key]
    type = "kms"
    key-id = "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
    region = "us-west-2"

    [security.encryption.previous-master-key]
    type = "kms"
    key-id = "0987dcba-09fe-87dc-65ba-ab0987654321"
    region = "us-west-2"

あるいは、 TiUPクラスター テンプレートに次の内容を追加します。

    server_configs:
      tiflash-learner:
        security.encryption.master-key.type: "kms"
        security.encryption.master-key.key-id: "50a0c603-1c6f-11e6-bb9e-3fadde80ce75"
        security.encryption.master-key.region: "us-west-2"
        security.encryption.previous-master-key.type: "kms"
        security.encryption.previous-master-key.key-id: "0987dcba-09fe-87dc-65ba-ab0987654321"
        security.encryption.previous-master-key.region: "us-west-2"

### モニタリングとデバッグ {#monitoring-and-debugging}

保存時の暗号化を監視するには、Grafana を使用してTiFlashを展開する場合、 **TiFlash-Proxy-Details**ダッシュボードの**[暗号化]**パネルを確認できます。監視項目の意味はTiKVと同様です。

デバッグの場合、 TiFlashは暗号化されたメタデータを管理するための TiKV のロジックを再利用するため、 `tikv-ctl`コマンドを使用して、ファイルの暗号化に使用された暗号化方式やデータ キー ID、データ キーのリストなどの暗号化メタデータをダンプできます。この操作は機密データを公開する可能性があるため、本番では推奨されません。詳細については[TiKV Control](/tikv-control.md#dump-encryption-metadata)を参照してください。

### TiKV バージョン間の互換性 {#compatibility-between-tikv-versions}

TiFlash は、 v4.0.9 で暗号化されたメタデータの操作も最適化しており、その互換性要件は TiKV の要件と同じです。詳細は[TiKV バージョン間の互換性](#compatibility-between-tikv-versions)を参照してください。

## BR S3 サーバー側暗号化 {#br-s3-server-side-encryption}

BRを使用して S3 にバックアップするときに S3 サーバー側の暗号化を有効にするには、 `--s3.sse`引数を渡し、値を「aws:kms」に設定します。 S3 は暗号化に独自の KMS キーを使用します。例：

    ./br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.sse aws:kms

自分が作成して所有したカスタム AWS KMS CMK を使用するには、さらに`--s3.sse-kms-key-id`を渡します。この場合、 BRプロセスとクラスター内のすべての TiKV ノードの両方が KMS CMK に (たとえば、AWS IAM経由で) アクセスする必要があり、KMS CMK は、以前に使用されていた S3 バケットと同じ AWS リージョンにある必要があります。バックアップを保存します。 AWS IAMを介して、KMS CMK へのBRプロセスおよび TiKV ノードへのアクセスを許可することをお勧めします。 [IAMは](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)の使用法については、AWS のドキュメントを参照してください。例えば：

    ./br backup full --pd <pd-address> --storage "s3://<bucket>/<prefix>" --s3.sse aws:kms --s3.sse-kms-key-id 0987dcba-09fe-87dc-65ba-ab0987654321

バックアップを復元するときは、 `--s3.sse`と`--s3.sse-kms-key-id`の両方を使用しないでください。 S3 は暗号化設定を自ら判断します。バックアップを復元するクラスター内のBRプロセスと TiKV ノードも KMS CMK にアクセスする必要があります。アクセスできない場合、復元は失敗します。例：

    ./br restore full --pd <pd-address> --storage "s3://<bucket>/<prefix>"

## BR Azure Blob Storage サーバー側の暗号化 {#br-azure-blob-storage-server-side-encryption}

BRを使用してデータを Azure Blob Storage にバックアップする場合、サーバー側暗号化の暗号化スコープまたは暗号化キーのいずれかを指定できます。

### 方法 1: 暗号化スコープを使用する {#method-1-use-an-encryption-scope}

バックアップ データの暗号化範囲を指定するには、次の 2 つの方法のいずれかを使用できます。

-   `backup`コマンドに`--azblob.encryption-scope`オプションを含めて、スコープ名に設定します。

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-scope scope1
    ```

-   URI に`encryption-scope`含めてスコープ名に設定します。

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-scope=scope1"
    ```

詳細については、Azure の[暗号化スコープを使用して BLOB をアップロードする](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-scope-manage?tabs=powershell#upload-a-blob-with-an-encryption-scope)を参照してください。

バックアップを復元する場合、暗号化スコープを指定する必要はありません。 Azure Blob Storage はデータを自動的に復号化します。例えば：

```shell
./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
```

### 方法 2: 暗号化キーを使用する {#method-2-use-an-encryption-key}

バックアップ データの暗号化キーを指定するには、次の 3 つの方法のいずれかを使用できます。

-   `backup`コマンドに`--azblob.encryption-key`オプションを含めて、AES256 暗号化キーに設定します。

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-key <aes256-key>
    ```

-   URI に`encryption-key`含めて、AES256 暗号化キーに設定します。キーに`&`や`%`などの URI 予約文字が含まれている場合は、最初にパーセント エンコードする必要があります。

    ```shell
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-key=<aes256-key>"
    ```

-   `AZURE_ENCRYPTION_KEY`環境変数を AES256 暗号化キーに設定します。実行する前に、環境変数内の暗号化キーを忘れないように覚えておいてください。

    ```shell
    export AZURE_ENCRYPTION_KEY=<aes256-key>
    ./br backup full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
    ```

詳細については、Azure の[Blob storageへのリクエストに暗号化キーを提供する](https://learn.microsoft.com/en-us/azure/storage/blobs/encryption-customer-provided-keys)を参照してください。

バックアップを復元するときは、暗号化キーを指定する必要があります。例えば：

-   `restore`コマンドに`--azblob.encryption-key`オプションを含めます。

    ```shell
    ./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>" --azblob.encryption-key <aes256-key>
    ```

-   URI に`encryption-key`を含めます。

    ```shell
    ./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>?encryption-key=<aes256-key>"
    ```

-   `AZURE_ENCRYPTION_KEY`環境変数を設定します。

    ```shell
    export AZURE_ENCRYPTION_KEY=<aes256-key>
    ./br restore full --pd <pd-address> --storage "azure://<bucket>/<prefix>"
    ```
