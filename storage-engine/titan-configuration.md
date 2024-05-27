---
title: Titan Configuration
summary: Titan の設定方法を学習します。
---

# タイタンのコンフィグレーション {#titan-configuration}

このドキュメントでは、対応する構成項目、データ変換メカニズム、関連パラメータ、およびレベルマージ機能を使用して[巨人](/storage-engine/titan-overview.md)有効または無効にする方法を紹介します。

## タイタンを有効にする {#enable-titan}

> **注記：**
>
> -   TiDB v7.6.0 以降では、新しいクラスターでは Titan がデフォルトで有効になり、ワイド テーブルと JSON データの書き込みパフォーマンスが向上します。1 しきい値のデフォルト値は[`min-blob-size`](/tikv-configuration-file.md#min-blob-size)から`1KB` `32KB`変更されました。
> -   v7.6.0 以降のバージョンにアップグレードされた既存のクラスターは元の構成を保持します。つまり、Titan が明示的に有効になっていない場合は、引き続き RocksDB が使用されます。
> -   クラスターを TiDB v7.6.0 以降のバージョンにアップグレードする前に Titan を有効にしていた場合、アップグレード後に Titan が有効になり、アップグレード前の[`min-blob-size`](/tikv-configuration-file.md#min-blob-size)の構成も保持されます。アップグレード前に値を明示的に構成しない場合は、アップグレード後のクラスター構成の安定性を確保するために、古いバージョン`1KB`のデフォルト値が保持されます。

Titan は RocksDB と互換性があるため、RocksDB を使用する既存の TiKV インスタンスで Titan を直接有効にすることができます。Titan を有効にするには、次のいずれかの方法を使用できます。

-   方法 1: TiUPを使用してクラスターをデプロイした場合は、次の例に示すように、 `tiup cluster edit-config ${cluster-name}`コマンドを実行し、TiKV 構成ファイルを編集できます。

    ```shell
    tikv:
      rocksdb.titan.enabled: true
    ```

    設定を再ロードすると、TiKV が動的にローリング再起動されます。

    ```shell
    tiup cluster reload ${cluster-name} -R tikv
    ```

    詳細なコマンドについては[TiUPを使用して構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)参照してください。

-   方法 2: TiKV 構成ファイルを直接編集して Titan を有効にします (本番環境では推奨され**ません**)。

    ```toml
    [rocksdb.titan]
    enabled = true
    ```

-   方法 3: TiDB Operatorの`${cluster_name}/tidb-cluster.yaml`構成ファイルを編集します。

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
> Titan が無効になっている場合、RocksDB は Titan に移動されたデータを読み取ることができません。Titan がすでに有効になっている TiKV インスタンスで Titan が誤って無効になっている場合 (誤って`rocksdb.titan.enabled`を`false`に設定した場合)、TiKV は起動に失敗し、TiKV ログに`You have disabled titan when its data directory is not empty`エラーが表示されます。Titan を正しく無効にするには、 [タイタンを無効にする](#disable-titan)参照してください。

Titan を有効にした後、RocksDB に保存されている既存のデータは Titan エンジンにすぐには移動されません。新しいデータが TiKV に書き込まれ、RocksDB が圧縮を実行すると、**値は徐々にキーから分離され、 Titan に書き込まれます**。同様に、 BRスナップショット/ログを通じて復元されたデータ、スケーリング中に変換されたデータ、またはTiDB Lightning物理インポート モードによってインポートされたデータは、Titan に直接書き込まれません。圧縮が進むにつれて、処理された SST ファイル内のデフォルト値 ( `32KB` ) の[`min-blob-size`](/tikv-configuration-file.md#min-blob-size)を超える大きな値が Titan に分離されます。TiKV**の詳細 &gt; Titan kv &gt; blob ファイル サイズ**パネルを観察してデータ サイズを見積もることで、Titan に保存されているファイルのサイズを監視できます。

書き込みプロセスを高速化したい場合は、 tikv-ctl を使用して、TiKV クラスター全体のデータを手動で圧縮できます。詳細については、 [手動圧縮](/tikv-control.md#compact-data-of-the-whole-tikv-cluster-manually)を参照してください。RocksDB から Titan への変換中はデータ アクセスが継続されるため、RocksDB のブロックキャッシュによってデータ変換プロセスが大幅に高速化されます。テストでは、 tikv-ctl を使用して、670 GiB のボリュームの TiKV データを 1 時間で Titan に変換できました。

Titan Blob ファイル内の値は連続しておらず、Titan のキャッシュは値レベルであるため、圧縮中に Blob キャッシュは役に立たないことに注意してください。Titan から RocksDB への変換速度は、RocksDB から Titan への変換速度よりも 1 桁遅くなります。テストでは、完全な圧縮で tikv-ctl を使用して TiKV ノード上の 800 GiB の Titan データのボリュームを RocksDB に変換するのに 12 時間かかります。

## パラメーター {#parameters}

Titan パラメータを適切に構成することで、データベースのパフォーマンスとリソース使用率を効果的に向上できます。このセクションでは、使用できるいくつかの重要なパラメータを紹介します。

### <code>min-blob-size</code> {#code-min-blob-size-code}

[`min-blob-size`](/tikv-configuration-file.md#min-blob-size)を使用して値のサイズのしきい値を設定し、どのデータを RocksDB に保存し、どのデータを Titan の BLOB ファイルに保存するかを決定できます。テストによると、 `32KB`が適切なしきい値です。これにより、Titan のパフォーマンスが RocksDB と比較して低下しないことが保証されます。ただし、多くのシナリオでは、この値は最適ではありません[`min-blob-size`がパフォーマンスに与える影響](/storage-engine/titan-overview.md#impact-of-min-blob-size-on-performance)を参照して適切な値を選択することをお勧めします。書き込みパフォーマンスをさらに向上させ、スキャン パフォーマンスの低下を許容できる場合は、最小値の`1KB`に設定できます。

### <code>blob-file-compression</code>と<code>zstd-dict-size</code> {#code-blob-file-compression-code-and-code-zstd-dict-size-code}

[`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression)を使用して、Titan の値に使用する圧縮アルゴリズムを指定できます。また、 `zstd`から[`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size)までの辞書圧縮を有効にして、圧縮率を向上させることもできます。

### <code>blob-cache-size</code> {#code-blob-cache-size-code}

Titan の値のキャッシュ サイズを制御するには、 [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size)使用します。キャッシュ サイズが大きいほど、Titan の読み取りパフォーマンスが向上します。ただし、キャッシュ サイズが大きすぎると、メモリ不足 (OOM) の問題が発生します。

データベースが安定して動作しているときは、ストア サイズから BLOB ファイル サイズを引いた値を`storage.block-cache.capacity`に設定し、監視メトリックに応じて`blob-cache-size` ～ `memory size * 50% - block cache size`設定することをお勧めします。これにより、ブロックキャッシュがRocksDB エンジン全体に十分な大きさである場合に、BLOB キャッシュ サイズが最大化されます。

### <code>discardable-ratio</code>と<code>max-background-gc</code> {#code-discardable-ratio-code-and-code-max-background-gc-code}

[`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio)パラメータと[`max-background-gc`](/tikv-configuration-file.md#max-background-gc)パラメータは、Titan の読み取りパフォーマンスとガベージコレクションプロセスに大きな影響を与えます。

BLOB ファイル内の古いデータ (対応するキーが更新または削除されている) の割合が[`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio)で設定されたしきい値を超えると、Titan GC がトリガーされます。このしきい値を下げると、スペースの増幅が軽減されますが、Titan GC の頻度が高くなる可能性があります。この値を上げると、Titan GC、I/O 帯域幅、CPU 消費が軽減されますが、ディスク領域の使用量は増加します。

**TiKV Details** - **Thread CPU** - **RocksDB CPU**から、Titan GC スレッドが長時間にわたってフル ロード状態になっていることが確認された場合は、 [`max-background-gc`](/tikv-configuration-file.md#max-background-gc)を調整して Titan GC スレッド プール サイズを増やすことを検討してください。

### <code>rate-bytes-per-sec</code> {#code-rate-bytes-per-sec-code}

[`rate-bytes-per-sec`](/tikv-configuration-file.md#rate-bytes-per-sec)を調整すると、RocksDB 圧縮の I/O レートを制限し、トラフィックが多いときのフォアグラウンドの読み取りおよび書き込みパフォーマンスへの影響を軽減できます。

### <code>shared-blob-cache</code> (v8.0.0 の新機能) {#code-shared-blob-cache-code-new-in-v8-0-0}

Titan BLOB ファイルと RocksDB ブロック ファイルの共有キャッシュを有効にするかどうかを[`shared-blob-cache`](/tikv-configuration-file.md#shared-blob-cache-new-in-v800)で制御できます。デフォルト値は`true`です。共有キャッシュを有効にすると、ブロック ファイルの優先順位が高くなります。つまり、TiKV はブロック ファイルのキャッシュ ニーズを満たすことを優先し、残りのキャッシュを BLOB ファイル用に使用します。

### Titan の構成例 {#titan-configuration-example}

以下は Titan 構成ファイルの例です。 [TiUPを使用して設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)または[Kubernetes上でTiDBクラスターを構成する](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster)いずれかを使用できます。

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

Titan を無効にするには、オプション`rocksdb.defaultcf.titan.blob-run-mode`を設定します。オプション`blob-run-mode`の値は次のとおりです。

-   オプションを`normal`に設定すると、Titan は読み取りおよび書き込み操作を通常どおり実行します。
-   オプションを`read-only`に設定すると、値のサイズに関係なく、新しく書き込まれたすべての値が RocksDB に書き込まれます。
-   オプションを`fallback`に設定すると、値のサイズに関係なく、新しく書き込まれたすべての値が RocksDB に書き込まれます。また、Titan BLOB ファイルに保存されたすべての圧縮された値は、自動的に RocksDB に戻されます。

既存および将来のすべてのデータに対して Titan を完全に無効にするには、次の手順に従います。手順 2 はオンライン トラフィックのパフォーマンスに大きく影響するため、スキップできます。実際、手順 2 を実行しなくても、データ圧縮によって Titan から RocksDB にデータを移動するときに余分な I/O および CPU リソースが消費され、TiKV I/O または CPU リソースが制限されている場合はパフォーマンスが低下します (最大 50% 低下することもあります)。

1.  Titan を無効にする TiKV ノードの構成を更新します。構成を更新するには、次の 2 つの方法があります。

    -   `tiup cluster edit-config`実行し、設定ファイルを編集して、 `tiup cluster reload -R tikv`を実行します。

    -   設定ファイルを手動で更新し、TiKV を再起動します。

        ```toml
        [rocksdb.defaultcf.titan]
        blob-run-mode = "fallback"
        discardable-ratio = 1.0
        ```

    > **注記：**
    >
    > Titan と RocksDB の両方のデータを収容するのに十分なディスク容量がない場合は、 [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio)にデフォルト値の`0.5`を使用することをお勧めします。一般的に、使用可能なディスク容量が 50% 未満の場合はデフォルト値が推奨されます。これは、 `discardable-ratio = 1.0`場合、RocksDB データが増加し続けるためです。同時に、Titan 内の既存の BLOB ファイルをリサイクルするには、そのファイル内のすべてのデータを RocksDB に変換する必要があり、これは時間のかかるプロセスです。ただし、ディスク サイズが十分に大きい場合は、 `discardable-ratio = 1.0`に設定すると、圧縮中に BLOB ファイル自体の GC が削減され、帯域幅を節約できます。

2.  (オプション) tikv-ctl を使用して完全な圧縮を実行します。このプロセスでは、大量の I/O および CPU リソースが消費されます。

    > **警告：**
    >
    > ディスク容量が不足している場合、次のコマンドを実行すると、クラスター全体の使用可能容量が不足し、データを書き込めなくなる可能性があります。

    ```bash
    tikv-ctl --pd <PD_ADDR> compact-cluster --bottommost force
    ```

3.  圧縮が完了したら、 **TiKV-Details** / **Titan - kv**の下の**Blob ファイル数**メトリックが`0`に減少するまで待ちます。

4.  これらの TiKV ノードの構成を更新して Titan を無効にします。

    ```toml
    [rocksdb.titan]
    enabled = false
    ```

## レベルマージ（実験的） {#level-merge-experimental}

TiKV 4.0 では、範囲クエリのパフォーマンスを向上させ、フォアグラウンド書き込み操作に対する Titan GC の影響を軽減するための新しいアルゴリズム[レベルマージ](/storage-engine/titan-overview.md#level-merge)が導入されました。次のオプションを使用して、レベル マージを有効にできます。

```toml
[rocksdb.defaultcf.titan]
level-merge = true
```

レベルマージを有効にすると、次の利点があります。

-   Titan 範囲クエリのパフォーマンスが大幅に向上しました。
-   フォアグラウンド書き込み操作に対する Titan GC の影響を軽減し、書き込みパフォーマンスを向上させます。
-   Titan のスペース増幅とディスク使用量を削減します (デフォルト構成でのディスク使用量と比較して)。

したがって、Level Merge を有効にした場合の書き込み増幅は Titan の場合よりもわずかに高くなりますが、ネイティブ RocksDB の場合よりも低くなります。
