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

-   リクエストがいくつかのキーに集中する可能性があるため、リージョンを均等に分割することが常に最良の選択であるとは限りません。このような場合、均等に分割した後もホットスポットがリージョンの 1 つに残っている可能性があり、目標を実現するために複数の均等な分割が必要になる場合があります。
-   人間の介入はタイムリーでも単純でもありません。

## 実施原則 {#implementation-principles}

Load Base Split は、統計に基づいてリージョンを自動的に分割します。読み取り負荷が 10 秒間一貫してしきい値を超えているリージョンを特定し、これらのリージョンを適切な位置で分割します。分割位置を選択すると、Load Base Split は、分割後に両方のリージョンのアクセス負荷のバランスを取り、リージョン間のアクセスを回避しようとします。

Load Base Split によって分割されたリージョンは、すぐにはマージされません。一方では、PD の`MergeChecker`はホットな地域をスキップします。一方、PD は、ハートビート情報の`QPS`に従って 2 つのリージョンをマージするかどうかも決定し、高い`QPS`を持つ 2 つのリージョンのマージを回避します。

## 使用法 {#usage}

Load Base Split 機能は現在、 `split.qps-threshold`つのパラメーター (QPS しきい値) と`split.byte-threshold`のパラメーター (トラフィックのしきい値) によって制御されています。リージョンの 1 秒あたりのすべてのタイプの読み取りリクエストの合計が 10 秒間連続して QPS しきい値またはトラフィックしきい値を超えた場合、PD はリージョンを分割します。

Load Base Split はデフォルトで有効になっていますが、パラメータはかなり高い値に設定されています。 `split.qps-threshold`のデフォルトは`3000`で、 `split.byte-threshold`のデフォルトは 30MB/s です。この機能を無効にする場合は、2 つのしきい値を同時に十分に高く設定してください。

パラメータを変更するには、次の 2 つの方法のいずれかを実行します。

-   SQL ステートメントを使用します。

    ```sql
    # Set the QPS threshold to 1500
    SET config tikv split.qps-threshold=1500;
    # Set the byte threshold to 15 MiB (15 * 1024 * 1024)
    SET config tikv split.byte-threshold=15728640;
    ```

-   TiKV を使用:

    {{< copyable "" >}}

    ```shell
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.qps-threshold":"1500"}'
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.byte-threshold":"15728640"}'
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
