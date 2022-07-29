---
title: Titan Configuration
summary: Learn how to configure Titan.
---

# TitanConfiguration / コンフィグレーション {#titan-configuration}

このドキュメントでは、対応する構成アイテムを使用して[巨人](/storage-engine/titan-overview.md)を有効または無効にする方法、および関連するパラメーターとレベルマージ機能を紹介します。

## Titanを有効にする {#enable-titan}

TitanはRocksDBと互換性があるため、RocksDBを使用する既存のTiKVインスタンスでTitanを直接有効にできます。次の2つの方法のいずれかを使用して、Titanを有効にできます。

-   方法1：TiUPを使用してクラスタをデプロイした場合は、次の例に示すように、 `tiup cluster edit-config ${cluster-name}`コマンドを実行してTiKV構成ファイルを編集できます。

    {{< copyable "" >}}

    ```shell
      tikv:
        rocksdb.titan.enabled: true
    ```

    構成をリロードすると、TiKVはオンラインでローリングリスタートされます。

    {{< copyable "" >}}

    ```shell
    tiup cluster reload ${cluster-name} -R tikv
    ```

    詳細なコマンドについては、 [TiUPを使用して構成を変更します](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

-   方法2：TiKV構成ファイルを直接編集してTitanを有効にします（実稼働環境には推奨され**ません**）。

    {{< copyable "" >}}

    ```toml
    [rocksdb.titan]
    enabled = true
    ```

Titanを有効にした後、RocksDBに保存されている既存のデータはすぐにはTitanエンジンに移動されません。新しいデータがTiKVフォアグラウンドに書き込まれ、RocksDBが圧縮を実行すると、値はキーから徐々に分離され、Titanに書き込まれます。 **TiKVの詳細**-&gt; <strong>Titankv-</strong> &gt; <strong>blobファイルサイズ</strong>パネルを表示して、Titanに保存されているデータのサイズを確認できます。

書き込みプロセスを高速化したい場合は、tikv-ctlを使用してTiKVクラスタ全体のデータを手動で圧縮します。詳細については、 [手動圧縮](/tikv-control.md#compact-data-of-the-whole-tikv-cluster-manually)を参照してください。

> **ノート：**
>
> Titanが無効になっている場合、RocksDBはTitanに移行されたデータを読み取ることができません。 Titanがすでに有効になっているTiKVインスタンスでTitanが誤って無効にされている場合（誤って`rocksdb.titan.enabled`から`false`に設定されている場合）、TiKVは起動に失敗し、 `You have disabled titan when its data directory is not empty`エラーがTiKVログに表示されます。 Titanを正しく無効にするには、 [Titanを無効にする](#disable-titan-experimental)を参照してください。

## パラメーター {#parameters}

TiUPを使用してTitan関連のパラメータを調整するには、 [構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

-   TitanGCスレッド数。

    **TiKVの詳細**-&gt;<strong>スレッドCPU-</strong> &gt; <strong>RocksDBCPU</strong>パネルから、Titan GCスレッドが長時間フルキャパシティーになっていることに気付いた場合は、TitanGCスレッドプールのサイズを増やすことを検討してください。

    {{< copyable "" >}}

    ```toml
    [rocksdb.titan]
    max-background-gc = 1
    ```

-   値のサイズのしきい値。

    フォアグラウンドに書き込まれる値のサイズがしきい値よりも小さい場合、この値はRocksDBに保存されます。それ以外の場合、この値はTitanのblobファイルに保存されます。値のサイズの分布に基づいて、しきい値を増やすと、より多くの値がRocksDBに格納され、TiKVは小さな値の読み取りでより優れたパフォーマンスを発揮します。しきい値を下げると、より多くの値がTitanに送られ、RocksDBの圧縮がさらに減少します。

    ```toml
    [rocksdb.defaultcf.titan]
    min-blob-size = "1KB"
    ```

-   Titanで値を圧縮するために使用されるアルゴリズム。値を単位とします。

    ```toml
    [rocksdb.defaultcf.titan]
    blob-file-compression = "lz4"
    ```

-   Titanの値キャッシュのサイズ。

    キャッシュサイズが大きいほど、Titanの読み取りパフォーマンスが高くなります。ただし、キャッシュサイズが大きすぎると、メモリ不足（OOM）が発生します。データベースが安定して実行されている場合は、ストアサイズからblobファイルサイズを引いた値に`storage.block-cache.capacity`の値を設定し、監視メトリックに従って`blob-cache-size`から`memory size * 50% - block cache size`に設定することをお勧めします。これにより、ブロックキャッシュがRocksDBエンジン全体に対して十分に大きい場合に、blobキャッシュサイズが最大化されます。

    ```toml
    [rocksdb.defaultcf.titan]
    blob-cache-size = 0
    ```

-   BLOBファイル内の破棄可能なデータ（対応するキーが更新または削除された）の比率が次のしきい値を超えると、TitanGCがトリガーされます。

    ```toml
    discardable-ratio = 0.5
    ```

    Titanがこのblobファイルの有用なデータを別のファイルに書き込む場合、 `discardable-ratio`の値を使用して、書き込み増幅とスペース増幅の上限を見積もることができます（圧縮が無効になっていると仮定）。

    ライトアンプリフィケーションの上限=1/discardable_ratio

    スペース増幅の上限=1/（1-discardable_ratio）

    上記の2つの式から、 `discardable_ratio`の値を減らすとスペースの増幅が減る可能性がありますが、TitanではGCの頻度が高くなることがわかります。値を増やすと、Titan GC、対応するI / O帯域幅、およびCPU消費量が減少しますが、ディスク使用量は増加します。

-   次のオプションは、RocksDB圧縮のI/Oレートを制限します。トラフィックのピーク時には、RocksDBの圧縮、I / O帯域幅、およびCPU消費を制限することで、フォアグラウンドの書き込みおよび読み取りパフォーマンスへの影響を軽減します。

    Titanが有効になっている場合、このオプションはRocksDB圧縮とTitanGCの合計I/Oレートを制限します。 RocksDBコンパクションとTitanGCのI/OやCPUの消費量が大きすぎる場合は、ディスクI/O帯域幅と実際の書き込みトラフィックに応じてこのオプションを適切な値に設定してください。

    ```toml
    [rocksdb]
    rate-bytes-per-sec = 0
    ```

## Titanを無効にする（実験的） {#disable-titan-experimental}

Titanを無効にするには、 `rocksdb.defaultcf.titan.blob-run-mode`オプションを構成できます。 `blob-run-mode`のオプション値は次のとおりです。

-   オプションが`normal`に設定されている場合、Titanは通常どおり読み取りおよび書き込み操作を実行します。
-   オプションが`read-only`に設定されている場合、値のサイズに関係なく、新しく書き込まれたすべての値がRocksDBに書き込まれます。
-   オプションが`fallback`に設定されている場合、値のサイズに関係なく、新しく書き込まれたすべての値がRocksDBに書き込まれます。また、Titan BLOBファイルに保存されているすべての圧縮値は、自動的にRocksDBに戻されます。

Titanを無効にするには、 `blob-run-mode = "fallback"`を設定し、tikv-ctlを使用して完全な圧縮を実行します。その後、監視メトリックを確認し、blobファイルのサイズが`0`に減少することを確認します。次に、 `rocksdb.titan.enabled`を`false`に設定して、TiKVを再起動できます。

> **警告：**
>
> Titanを無効にすることは、実験的機能です。必要が**ない**場合は使用しないでください。

## レベルマージ（実験的） {#level-merge-experimental}

TiKV 4.0では、範囲クエリのパフォーマンスを改善し、フォアグラウンド書き込み操作に対するTitan GCの影響を減らすために、新しいアルゴリズムである[レベルマージ](/storage-engine/titan-overview.md#level-merge)が導入されました。次のオプションを使用して、レベルマージを有効にできます。

```toml
[rocksdb.defaultcf.titan]
level-merge = true
```

レベルマージを有効にすると、次の利点があります。

-   Titan範囲クエリのパフォーマンスを大幅に向上させます。
-   フォアグラウンド書き込み操作に対するTitanGCの影響を減らし、書き込みパフォーマンスを向上させます。
-   Titanのスペース増幅とディスク使用量を減らします（デフォルト構成のディスク使用量と比較して）。

したがって、レベルマージを有効にした場合のライトアンプリフィケーションは、Titanのライトアンプリフィケーションよりもわずかに高くなりますが、ネイティブのRocksDBのライトアンプリフィケーションよりは低くなります。
