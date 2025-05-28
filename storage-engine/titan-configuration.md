---
title: Titan Configuration
summary: Titan の設定方法を学びます。
---

# タイタンのコンフィグレーション {#titan-configuration}

このドキュメントでは、対応する構成項目、データ変換メカニズム、関連パラメータ、およびレベルマージ機能を使用して[タイタン](/storage-engine/titan-overview.md)有効または無効にする方法を紹介します。

## タイタンを有効にする {#enable-titan}

> **注記：**
>
> -   TiDB v7.6.0以降、新規クラスタではTitanがデフォルトで有効化され、ワイドテーブルとJSONデータの書き込みパフォーマンスが向上します。1 [`min-blob-size`](/tikv-configuration-file.md#min-blob-size)のデフォルト値は`1KB`から`32KB`に変更されました。
> -   v7.6.0 以降のバージョンにアップグレードされた既存のクラスターは元の構成を保持します。つまり、Titan が明示的に有効になっていない場合は、引き続き RocksDB が使用されます。
> -   クラスタをTiDB v7.6.0以降のバージョンにアップグレードする前にTitanを有効にしていた場合、アップグレード後もTitanが有効になり、アップグレード前の設定値[`min-blob-size`](/tikv-configuration-file.md#min-blob-size)も保持されます。アップグレード前に明示的に値を設定しない場合は、アップグレード後のクラスタ構成の安定性を確保するために、旧バージョンのデフォルト値`1KB`が保持されます。

TitanはRocksDBと互換性があるため、RocksDBを使用する既存のTiKVインスタンスでTitanを直接有効化できます。Titanを有効化するには、以下のいずれかの方法があります。

-   方法 1: TiUPを使用してクラスターをデプロイした場合は、次の例に示すように、 `tiup cluster edit-config ${cluster-name}`コマンドを実行して TiKV 構成ファイルを編集できます。

    ```shell
    tikv:
      rocksdb.titan.enabled: true
    ```

    設定を再ロードすると、TiKV が動的にローリング再起動されます。

    ```shell
    tiup cluster reload ${cluster-name} -R tikv
    ```

    詳細なコマンドについては[TiUPを使用して構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)参照してください。

-   方法 2: TiKV 構成ファイルを直接編集して Titan を有効にします (本番環境では推奨さ**れません**)。

    ```toml
    [rocksdb.titan]
    enabled = true
    ```

-   方法3: TiDB Operatorの`${cluster_name}/tidb-cluster.yaml`構成ファイルを編集します。

    ```yaml
    spec:
      tikv:
        ## Base image of the component
        baseImage: pingcap/tikv
        ## tikv-server configuration
        ## Ref: https://docs.pingcap.com/tidb/stable/tikv-configuration-file
        config: |
          log-level = "info"
          [rocksdb]
            [rocksdb.titan]
              enabled = true
    ```

    変更を有効にするために、TiDB クラスターのオンライン ローリング再起動をトリガーする構成を適用します。

    ```shell
    kubectl apply -f ${cluster_name} -n ${namespace}
    ```

    詳細については[Kubernetes での TiDBクラスタの構成](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster)を参照してください。

## データ変換 {#data-conversion}

> **警告：**
>
> Titanが無効になっている場合、RocksDBはTitanに移動されたデータを読み取ることができません。Titanが既に有効になっているTiKVインスタンスでTitanを誤って無効にした場合（誤って`rocksdb.titan.enabled`を`false`に設定した場合）、TiKVは起動に失敗し、TiKVログに`You have disabled titan when its data directory is not empty`エラーが表示されます。Titanを正しく無効にするには、 [タイタンを無効にする](#disable-titan)参照してください。

Titan を有効にした後、RocksDB に保存されている既存のデータは、すぐに Titan エンジンに移動されるわけではありません。新しいデータが TiKV に書き込まれ、RocksDB が圧縮を実行すると、**値は徐々にキーから分離され、 Titan に書き込まれます**。同様に、 BRスナップショット/ログを通じて復元されたデータ、スケーリング中に変換されたデータ、またはTiDB Lightning物理インポート モードによってインポートされたデータは、Titan に直接書き込まれません。圧縮が進むにつれて、処理された SST ファイル内のデフォルト値 ( `32KB` ) の[`min-blob-size`](/tikv-configuration-file.md#min-blob-size)を超える大きな値が Titan に分離されます。TiKV**の詳細 &gt; Titan kv &gt; blob ファイル サイズ**パネルを観察してデータ サイズを見積もることで、Titan に保存されているファイルのサイズを監視できます。

書き込みプロセスを高速化したい場合は、tikv-ctl を使用して TiKV クラスター全体のデータを手動で圧縮できます。詳細は[手作業による圧縮](/tikv-control.md#compact-data-of-the-whole-tikv-cluster-manually)参照してください。RocksDB から Titan への変換中はデータアクセスが継続的に行われるため、RocksDB のブロックキャッシュによってデータ変換プロセスが大幅に高速化されます。テストでは、tikv-ctl を使用することで、670 GiB の TiKV データを 1 時間で Titan に変換できました。

Titan BLOBファイル内の値は連続しておらず、Titanのキャッシュは値レベルであるため、圧縮時にはBLOBキャッシュは役に立ちません。TitanからRocksDBへの変換速度は、RocksDBからTitanへの変換速度よりも桁違いに遅くなります。テストでは、TiKVノード上の800GiBのTitanデータをtikv-ctlでRocksDBに完全圧縮変換するのに12時間かかりました。

## パラメータ {#parameters}

Titanパラメータを適切に設定することで、データベースのパフォーマンスとリソース使用率を効果的に向上させることができます。このセクションでは、使用可能な主要なパラメータをいくつか紹介します。

### <code>min-blob-size</code> {#code-min-blob-size-code}

[`min-blob-size`](/tikv-configuration-file.md#min-blob-size)使用すると、RocksDB に保存するデータと Titan の BLOB ファイルに保存するデータを決定するための値のサイズのしきい値を設定できます。テストによると、 `32KB`適切なしきい値です。これにより、RocksDB と比較して Titan のパフォーマンスが低下しないことが保証されます。ただし、多くのシナリオでは、この値は最適ではありません。適切な値を選択するには、 [`min-blob-size`がパフォーマンスに与える影響](/storage-engine/titan-overview.md#impact-of-min-blob-size-on-performance)を参照することをお勧めします。書き込みパフォーマンスをさらに向上させ、スキャンパフォーマンスの低下を許容できる場合は、最小値の`1KB`に設定できます。

### <code>blob-file-compression</code>と<code>zstd-dict-size</code> {#code-blob-file-compression-code-and-code-zstd-dict-size-code}

[`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression)使用すると、Titan の値に使用する圧縮アルゴリズムを指定できます。また、 `zstd`から[`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size)の辞書圧縮を有効にして圧縮率を向上させることもできます。

### <code>blob-cache-size</code> {#code-blob-cache-size-code}

Titanの値のキャッシュサイズを制御するには、 [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size)使用します。キャッシュサイズが大きいほど、Titanの読み取りパフォーマンスが向上します。ただし、キャッシュサイズが大きすぎると、メモリ不足（OOM）の問題が発生します。

ストアサイズからBLOBファイルサイズを引いた値を`storage.block-cache.capacity`に設定し、データベースが安定して動作している場合は、監視指標に応じて`blob-cache-size` ～ `memory size * 50% - block cache size`設定することをお勧めします。これにより、ブロックキャッシュがRocksDBエンジン全体に十分な大きさである場合に、BLOBキャッシュサイズが最大化されます。

### <code>discardable-ratio</code>と<code>max-background-gc</code> {#code-discardable-ratio-code-and-code-max-background-gc-code}

[`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio)のパラメータと[`max-background-gc`](/tikv-configuration-file.md#max-background-gc)パラメータは、Titan の読み取りパフォーマンスとガベージコレクションプロセスに大きな影響を与えます。

BLOBファイル内の古いデータ（対応するキーが更新または削除されたデータ）の割合が、 [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio)で設定されたしきい値を超えると、Titan GCがトリガーされます。このしきい値を下げると、スペースの増幅を軽減できますが、Titan GCの頻度が高くなる可能性があります。この値を上げると、Titan GC、I/O帯域幅、CPU消費量を削減できますが、ディスク容量の使用量は増加します。

**TiKV の詳細**-**スレッド CPU** - **RocksDB CPU**から、Titan GC スレッドが長時間にわたってフル ロード状態になっていることが確認された場合は、 [`max-background-gc`](/tikv-configuration-file.md#max-background-gc)調整して Titan GC スレッド プールのサイズを増やすことを検討してください。

### <code>rate-bytes-per-sec</code> {#code-rate-bytes-per-sec-code}

[`rate-bytes-per-sec`](/tikv-configuration-file.md#rate-bytes-per-sec)調整すると、RocksDB 圧縮の I/O レートを制限し、トラフィック量が多いときのフォアグラウンドの読み取りおよび書き込みパフォーマンスへの影響を軽減できます。

### <code>shared-blob-cache</code> (v8.0.0 の新機能) {#code-shared-blob-cache-code-new-in-v8-0-0}

Titan BLOBファイルとRocksDBブロックファイルの共有キャッシュを有効にするかどうかを[`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800)で制御できます。デフォルト値は`true`です。共有キャッシュを有効にすると、ブロックファイルの優先度が高くなります。つまり、TiKVはブロックファイルのキャッシュニーズを満たすことを優先し、残りのキャッシュをBLOBファイル用に使用することになります。

### Titanの構成例 {#titan-configuration-example}

以下は Titan 設定ファイルの例です。1 または[Kubernetes上でTiDBクラスターを構成する](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster) [TiUPを使用して設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)かを選択できます。

```toml
[rocksdb]
rate-bytes-per-sec = 0

[rocksdb.titan]
enabled = true
max-background-gc = 1

[rocksdb.defaultcf.titan]
min-blob-size = "32KB"
blob-file-compression = "zstd"
zstd-dict-size = "16KB"
discardable-ratio = 0.5
blob-run-mode = "normal"
level-merge = false
```

## タイタンを無効にする {#disable-titan}

Titanを無効にするには、オプション`rocksdb.defaultcf.titan.blob-run-mode`設定します。オプション`blob-run-mode`のオプション値は次のとおりです。

-   オプションを`normal`に設定すると、Titan は読み取りおよび書き込み操作を通常どおり実行します。
-   オプションを`read-only`に設定すると、値のサイズに関係なく、新しく書き込まれたすべての値が RocksDB に書き込まれます。
-   このオプションを`fallback`に設定すると、新しく書き込まれたすべての値は、値のサイズに関係なく、RocksDBに書き込まれます。また、Titan BLOBファイルに保存されたすべての圧縮された値は、自動的にRocksDBに戻されます。

既存および将来のすべてのデータに対してTitanを無効にするには、以下の手順に従ってください。手順2はオンライントラフィックのパフォーマンスに大きな影響を与えるため、省略できます。実際、手順2を実行しなくても、TitanからRocksDBへのデータ移動時にデータ圧縮によって余分なI/OとCPUリソースが消費され、TiKVのI/OまたはCPUリソースが制限されている場合はパフォーマンスが低下します（最大50%低下する場合もあります）。

1.  Titanを無効化したいTiKVノードの設定を更新します。設定の更新は2つの方法で行えます。

    -   `tiup cluster edit-config`実行し、設定ファイルを編集して`tiup cluster reload -R tikv`実行します。

    -   構成ファイルを手動で更新し、TiKV を再起動します。

        ```toml
        [rocksdb.defaultcf.titan]
        blob-run-mode = "fallback"
        discardable-ratio = 1.0
        ```

    > **注記：**
    >
    > TitanとRocksDBの両方のデータを収容するのに十分なディスク容量がない場合は、デフォルト値の`0.5` （ [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio)を使用することをお勧めします。一般的に、使用可能なディスク容量が50%未満の場合は、デフォルト値を使用することをお勧めします。これは、 `discardable-ratio = 1.0`設定するとRocksDBデータが増加し続けるためです。同時に、Titan内の既存のBLOBファイルをリサイクルするには、そのファイル内のすべてのデータをRocksDBに変換する必要があり、これは時間のかかるプロセスです。ただし、ディスクサイズが十分に大きい場合は、 `discardable-ratio = 1.0`設定すると、圧縮時にBLOBファイル自体のGCを削減できるため、帯域幅を節約できます。

2.  （オプション）tikv-ctlを使用して完全なコンパクションを実行します。このプロセスは大量のI/OとCPUリソースを消費します。

    > **警告：**
    >
    > ディスク容量が不足している場合、次のコマンドを実行すると、クラスター全体の使用可能な容量が不足し、データを書き込めなくなる可能性があります。

    ```bash
    tikv-ctl --pd <PD_ADDR> compact-cluster --bottommost force
    ```

3.  圧縮が完了したら、 **TiKV-Details** / **Titan - kv**の下の**Blob ファイル数**メトリックが`0`に減少するまで待ちます。

4.  TiDB v8.5.0 以降のバージョンの場合、これらの TiKV ノードの構成を更新して Titan を無効にします。

    > **警告：**
    >
    > v8.5.0より前のバージョンでは、TiKVがクラッシュする可能性があるため、この手順をスキップすることをお勧めします。これらの以前のバージョンでは、手順1を実行するだけでTitanを無効化できます。データ移行完了後、手順1の設定変更とこの手順の以降の変更との間にパフォーマンスの違いはありません。

    ```toml
    [rocksdb.titan]
    enabled = false
    ```

## レベルマージ（実験的） {#level-merge-experimental}

TiKV 4.0では、範囲クエリのパフォーマンスを向上させ、Titan GCによるフォアグラウンド書き込み操作への影響を軽減するための新しいアルゴリズム[レベルマージ](/storage-engine/titan-overview.md#level-merge)導入されました。レベルマージは、以下のオプションで有効にできます。

```toml
[rocksdb.defaultcf.titan]
level-merge = true
```

レベルマージを有効にすると、次の利点があります。

-   Titan 範囲クエリのパフォーマンスが大幅に向上しました。
-   Titan GC によるフォアグラウンド書き込み操作への影響を軽減し、書き込みパフォーマンスを向上させます。
-   Titan のスペース増幅とディスク使用量を削減します (デフォルト構成でのディスク使用量と比較して)。

したがって、Level Merge を有効にした場合の書き込み増幅は Titan の場合よりもわずかに高くなりますが、ネイティブ RocksDB の場合よりも低くなります。
