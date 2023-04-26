---
title: Load Base Split
summary: Learn the feature of Load Base Split.
---

# ロードベーススプリット {#load-base-split}

Load Base Split は、TiDB 4.0 で導入された新機能です。これは、小さなテーブルのフル テーブル スキャンなど、リージョン間の不均衡なアクセスによって引き起こされるホットスポットの問題を解決することを目的としています。

## シナリオ {#scenarios}

TiDB では、負荷が特定のノードに集中するとホットスポットが発生しやすくなります。 PD は、パフォーマンスを向上させるために、ホット リージョンがすべてのノードにできるだけ均等に分散されるように、ホット リージョンをスケジュールしようとします。

ただし、PD スケジューリングの最小単位はリージョンです。クラスター内のホットスポットの数がノードの数よりも少ない場合、またはいくつかのホットスポットの負荷が他のリージョンよりもはるかに大きい場合、PD はホットスポットをあるノードから別のノードに移動することしかできませんが、クラスター全体で負荷を共有することはできません。 .

このシナリオは、小さなテーブルのフル テーブル スキャンやインデックス ルックアップ、または一部のフィールドへの頻繁なアクセスなど、ほとんどが読み取り要求であるワークロードで特に一般的です。

以前は、この問題の解決策は、コマンドを手動で実行して 1 つ以上のホットスポット リージョンを分割することでしたが、この方法には 2 つの問題があります。

-   リージョンがいくつかのキーに集中する可能性があるため、リージョンを均等に分割することが常に最良の選択であるとは限りません。このような場合、均等に分割した後もホットスポットがリージョンの 1 つに残っている可能性があり、目標を実現するために複数の均等な分割が必要になる場合があります。
-   人間の介入はタイムリーでも単純でもありません。

## 実施原則 {#implementation-principles}

Load Base Split は、統計に基づいてリージョンを自動的に分割します。読み取り負荷または CPU 使用率が 10 秒間一貫してしきい値を超えているリージョンを特定し、これらのリージョンを適切な位置で分割します。分割位置を選択すると、Load Base Split は、分割後に両方のリージョンのアクセス負荷のバランスを取り、リージョン間のアクセスを回避しようとします。

Load Base Split によって分割されたリージョン は、すぐにはマージされません。一方では、PD の`MergeChecker`ホットな地域をスキップします。一方、PD は、ハートビート情報の`QPS`に従って 2 つのリージョンをマージするかどうかも決定し、高い`QPS`を持つ 2 つのリージョンのマージを回避します。

## 使用法 {#usage}

Load Base Split 機能は、現在、次のパラメータによって制御されています。

-   `split.qps-threshold` :リージョンがホットスポットとして識別される QPS しきい値。デフォルト値は毎秒`3000`です。
-   `split.byte-threshold` :リージョンがホットスポットとして識別されるトラフィックのしきい値。単位はバイトで、デフォルト値は 30 MiB/秒です。 (v5.0 で導入)
-   `split.region-cpu-overload-threshold-ratio` :リージョンがホットスポットとして識別される CPU 使用率のしきい値 (読み取りスレッド プールの CPU 時間の割合)。デフォルト値は`0.25`です。 (v6.2.0 で導入)

リージョンが次の条件のいずれかを 10 秒間連続して満たす場合、TiKV はリージョンの分割を試みます。

-   読み取り要求の合計が`split.qps-threshold`を超えています。
-   そのトラフィックは`split.byte-threshold`を超えています。
-   統合読み取りプールでの CPU 使用率が`split.region-cpu-overload-threshold-ratio`を超えています。

Load Base Split はデフォルトで有効になっていますが、パラメータはかなり高い値に設定されています。この機能を無効にしたい場合は、 `split.qps-threshold`と`split.byte-threshold`十分に高く設定し、同時に`split.region-cpu-overload-threshold-ratio`から`0`を設定します。

パラメータを変更するには、次の 2 つの方法のいずれかを実行します。

-   SQL ステートメントを使用します。

    ```sql
    # Set the QPS threshold to 1500
    SET config tikv split.qps-threshold=1500;
    # Set the byte threshold to 15 MiB (15 * 1024 * 1024)
    SET config tikv split.byte-threshold=15728640;
    # Set the CPU usage threshold to 50%
    SET config tikv split.region-cpu-overload-threshold-ratio=0.5;
    ```

-   TiKV を使用:

    {{< copyable "" >}}

    ```shell
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.qps-threshold":"1500"}'
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.byte-threshold":"15728640"}'
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.region-cpu-overload-threshold-ratio":"0.5"}'
    ```

したがって、次の 2 つの方法のいずれかで構成を表示できます。

-   SQL ステートメントを使用します。

    {{< copyable "" >}}

    ```sql
    show config where type='tikv' and name like '%split.qps-threshold%';
    ```

-   TiKV を使用:

    {{< copyable "" >}}

    ```shell
    curl "http://ip:status_port/config"
    ```

> **ノート：**
>
> v4.0.0-rc.2 以降では、SQL ステートメントを使用して構成を変更および表示できます。
