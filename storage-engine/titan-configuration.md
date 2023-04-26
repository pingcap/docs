---
title: Titan Configuration
summary: Learn how to configure Titan.
---

# タイタンのコンフィグレーション {#titan-configuration}

このドキュメントでは、対応する構成アイテムを使用して[巨人](/storage-engine/titan-overview.md)有効または無効にする方法、および関連するパラメーターとレベル マージ機能を紹介します。

## タイタンを有効にする {#enable-titan}

Titan は RocksDB と互換性があるため、RocksDB を使用する既存の TiKV インスタンスで Titan を直接有効にすることができます。 Titan を有効にするには、次の 2 つの方法のいずれかを使用できます。

-   方法 1: TiUPを使用してクラスターをデプロイした場合は、次の例に示すように、 `tiup cluster edit-config ${cluster-name}`コマンドを実行して TiKV 構成ファイルを編集できます。

    {{< copyable "" >}}

    ```shell
      tikv:
        rocksdb.titan.enabled: true
    ```

    構成をリロードすると、TiKV が動的にローリング再起動されます。

    {{< copyable "" >}}

    ```shell
    tiup cluster reload ${cluster-name} -R tikv
    ```

    詳細なコマンドについては、 [TiUPを使用して構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

-   方法 2: TiKV 構成ファイルを直接編集して Titan を有効にします (本番環境には**お勧めしません**)。

    {{< copyable "" >}}

    ```toml
    [rocksdb.titan]
    enabled = true
    ```

Titan を有効にしても、RocksDB に保存されている既存のデータはすぐに Titan エンジンに移動されません。新しいデータが TiKV フォアグラウンドに書き込まれ、RocksDB が圧縮を実行すると、値がキーから徐々に分離され、Titan に書き込まれます。 **TiKV Details** -&gt; <strong>Titan kv</strong> -&gt; <strong>blob file size</strong>パネルを表示して、Titan に保存されているデータのサイズを確認できます。

書き込みプロセスを高速化したい場合は、tikv-ctl を使用して手動で TiKV クラスター全体のデータを圧縮します。詳細については、 [手動圧縮](/tikv-control.md#compact-data-of-the-whole-tikv-cluster-manually)を参照してください。

> **ノート：**
>
> Titan が無効になっている場合、RocksDB は Titan に移行されたデータを読み取ることができません。 Titan が既に有効になっている TiKV インスタンスで誤って無効にされた場合 (誤って`rocksdb.titan.enabled`から`false`に設定された場合)、TiKV は起動に失敗し、TiKV ログに`You have disabled titan when its data directory is not empty`エラーが表示されます。 Titan を正しく無効にするには、 [タイタンを無効にする](#disable-titan)参照してください。

## パラメーター {#parameters}

TiUP を使用して Titan 関連のパラメータを調整するには、 [構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

-   Titan GC スレッド数。

    **TiKV の [詳細]** -&gt; <strong>[スレッド CPU]</strong> -&gt; <strong>[RocksDB CPU]</strong>パネルから、Titan GC スレッドが長時間フル容量になっていることがわかった場合は、Titan GC スレッド プールのサイズを増やすことを検討してください。

    {{< copyable "" >}}

    ```toml
    [rocksdb.titan]
    max-background-gc = 1
    ```

-   値のサイズのしきい値。

    フォアグラウンドに書き込まれた値のサイズがしきい値よりも小さい場合、この値は RocksDB に格納されます。それ以外の場合、この値は Titan の blob ファイルに保存されます。値のサイズの分布に基づいて、しきい値を大きくすると、より多くの値が RocksDB に保存され、TiKV は小さな値の読み取りのパフォーマンスが向上します。しきい値を下げると、より多くの値が Titan に送られ、RocksDB の圧縮がさらに減少します。

    ```toml
    [rocksdb.defaultcf.titan]
    min-blob-size = "1KB"
    ```

-   値を単位とする、Titan で値を圧縮するために使用されるアルゴリズム。

    ```toml
    [rocksdb.defaultcf.titan]
    blob-file-compression = "lz4"
    ```

-   Titan の値キャッシュのサイズ。

    キャッシュ サイズが大きいほど、Titan の読み取りパフォーマンスが高くなります。ただし、キャッシュ サイズが大きすぎると、メモリ不足 (OOM) が発生します。データベースが安定して実行されている場合は、ストア サイズから BLOB ファイル サイズを引いた値を`storage.block-cache.capacity`に設定し、監視メトリックに従って`blob-cache-size` ～ `memory size * 50% - block cache size`を設定することをお勧めします。これにより、ブロックキャッシュがRocksDB エンジン全体に対して十分な大きさである場合に、ブロブ キャッシュのサイズが最大化されます。

    ```toml
    [rocksdb.defaultcf.titan]
    blob-cache-size = 0
    ```

-   BLOB ファイル内の破棄可能なデータ (対応するキーが更新または削除された) の比率が次のしきい値を超えると、Titan GC がトリガーされます。

    ```toml
    discardable-ratio = 0.5
    ```

    Titan がこの BLOB ファイルの有用なデータを別のファイルに書き込む場合、値`discardable-ratio`を使用して、書き込み増幅と領域増幅の上限を推定できます (圧縮が無効になっていると仮定)。

    書き込み増幅の上限=1/discardable_ratio

    スペース増幅の上限 = 1 / (1 - 破棄可能比率)

    上記の 2 つの式から、値`discardable_ratio`を減らすと空間増幅が減少する可能性がありますが、Titan で GC がより頻繁に発生することがわかります。値を大きくすると、Titan GC、対応する I/O 帯域幅、および CPU 消費量が減少しますが、ディスク使用量が増加します。

-   次のオプションは、RocksDB 圧縮の I/O レートを制限します。トラフィックのピーク時には、RocksDB の圧縮、I/O 帯域幅、および CPU 消費を制限することで、フォアグラウンドの書き込みおよび読み取りパフォーマンスへの影響を軽減します。

    Titan が有効な場合、このオプションは RocksDB 圧縮と Titan GC の合計 I/O レートを制限します。 RocksDB コンパクションと Titan GC の I/O や CPU の消費量が大きすぎる場合は、ディスク I/O 帯域幅と実際の書き込みトラフィックに応じて、このオプションを適切な値に設定してください。

    ```toml
    [rocksdb]
    rate-bytes-per-sec = 0
    ```

## タイタンを無効にする {#disable-titan}

Titan を無効にするには、 `rocksdb.defaultcf.titan.blob-run-mode`オプションを設定します。 `blob-run-mode`のオプション値は次のとおりです。

-   オプションが`normal`に設定されている場合、Titan は通常どおり読み取りおよび書き込み操作を実行します。
-   このオプションが`read-only`に設定されている場合、値のサイズに関係なく、新しく書き込まれたすべての値が RocksDB に書き込まれます。
-   このオプションが`fallback`に設定されている場合、値のサイズに関係なく、新しく書き込まれたすべての値が RocksDB に書き込まれます。また、Titan blob ファイルに保存されているすべての圧縮された値は、自動的に RocksDB に戻されます。

既存および将来のすべてのデータに対して Titan を完全に無効にするには、次の手順に従います。

1.  Titan を無効にする TiKV ノードの構成を更新します。次の 2 つの方法で構成を更新できます。

    -   `tiup cluster edit-config`を実行し、構成ファイルを編集して`tiup cluster reload -R tikv`を実行します。
    -   構成ファイルを手動で更新し、TiKV を再起動します。

    ```toml
    [rocksdb.defaultcf.titan]
    blob-run-mode = "fallback"
    discardable-ratio = 1.0
    ```

2.  tikv-ctl を使用して完全な圧縮を実行します。このプロセスは、大量の I/O および CPU リソースを消費します。

    ```bash
    tikv-ctl --pd <PD_ADDR> compact-cluster --bottommost force
    ```

3.  圧縮が完了したら、 **TiKV-Details** / <strong>Titan-kv</strong>の下の<strong>Blob ファイル数</strong>メトリックが`0`に減少するまで待つ必要があります。

4.  これらの TiKV ノードの構成を更新して、Titan を無効にします。

    ```toml
    [rocksdb.titan]
    enabled = false
    ```

## レベル マージ (実験的) {#level-merge-experimental}

TiKV 4.0 では、範囲クエリのパフォーマンスを向上させ、フォアグラウンド書き込み操作に対する Titan GC の影響を軽減するために、新しいアルゴリズム[レベルマージ](/storage-engine/titan-overview.md#level-merge)が導入されました。次のオプションを使用してレベル マージを有効にできます。

```toml
[rocksdb.defaultcf.titan]
level-merge = true
```

レベル マージを有効にすると、次の利点があります。

-   Titan 範囲クエリのパフォーマンスが大幅に向上します。
-   フォアグラウンド書き込み操作に対する Titan GC の影響を軽減し、書き込みパフォーマンスを向上させます。
-   Titan のスペース増幅とディスク使用量を削減します (デフォルト構成でのディスク使用量と比較して)。

したがって、Level Merge を有効にした場合の書き込み増幅は、Titan よりもわずかに高くなりますが、ネイティブ RocksDB よりは依然として低くなります。
