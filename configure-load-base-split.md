---
title: Load Base Split
summary: Load Base Split の機能について学習します。
---

# ロードベーススプリット {#load-base-split}

Load Base Split は、TiDB 4.0 で導入された新しい機能です。小さなテーブルに対する完全なテーブルスキャンなど、リージョン間のアクセスの不均衡によって発生するホットスポットの問題を解決することを目的としています。

## シナリオ {#scenarios}

TiDB では、負荷が特定のノードに集中すると、ホットスポットが生成されやすくなります。PD は、パフォーマンスを向上させるために、ホット リージョンがすべてのノードに可能な限り均等に分散されるようにスケジュールしようとします。

ただし、PD スケジューリングの最小単位はリージョンです。クラスター内のホットスポットの数がノード数より少ない場合、またはいくつかのホットスポットの負荷が他のリージョンよりもはるかに大きい場合、PD はホットスポットをあるノードから別のノードに移動することしかできず、クラスター全体で負荷を共有することはできません。

このシナリオは、完全なテーブルスキャンや小さなテーブルのインデックス検索、一部のフィールドへの頻繁なアクセスなど、主に読み取り要求であるワークロードで特に一般的です。

以前は、この問題の解決策として、1 つ以上のホットスポット領域を分割するコマンドを手動で実行していましたが、この方法には 2 つの問題がありました。

-   リクエストが少数のキーに集中する可能性があるため、リージョンを均等に分割することが常に最善の選択であるとは限りません。このような場合、均等に分割した後もホットスポットがリージョンの 1 つに残る可能性があり、目的を達成するには均等に分割を複数回行う必要がある場合があります。
-   人間の介入はタイムリーでも簡単でもない。

## 実施原則 {#implementation-principles}

Load Base Split は、統計情報に基づいてリージョンを自動的に分割します。読み取り負荷または CPU 使用率が 10 秒間継続的にしきい値を超えるリージョンを識別し、これらのリージョンを適切な位置で分割します。分割位置を選択する際、Load Base Split は分割後の両方のリージョンのアクセス負荷を分散し、リージョン間のアクセスを回避しようとします。

Load Base Split によって分割されたリージョンは、すぐにはマージされません。一方で、PD の`MergeChecker`ホット リージョンをスキップします。他方では、PD はハートビート情報の`QPS`に従って 2 つのリージョンをマージするかどうかも決定し、 `QPS`の高い 2 つのリージョンのマージを回避します。

## 使用法 {#usage}

ロード ベース分割機能は現在、次のパラメータによって制御されています。

-   [`split.qps-threshold`](/tikv-configuration-file.md#qps-threshold) :リージョンがホットスポットとして識別される QPS しきい値。4 [`region-split-size`](/tikv-configuration-file.md#region-split-size)未満の場合はデフォルト値は 1 秒あたり`3000`です。それ以外の場合はデフォルト値は`7000`です。
-   [`split.byte-threshold`](/tikv-configuration-file.md#byte-threshold-new-in-v50) : (v5.0 で導入)リージョンがホットスポットとして識別されるトラフィックしきい値。単位はバイトです。2 `region-split-size` 4 GB 未満の場合、デフォルト値は 30 MiB/秒です。それ以外の場合、デフォルト値は 100 MiB/秒です。
-   [`split.region-cpu-overload-threshold-ratio`](/tikv-configuration-file.md#region-cpu-overload-threshold-ratio-new-in-v620) : (v6.2.0 で導入)リージョンがホットスポットとして識別される CPU 使用率しきい値 (読み取りスレッド プールの CPU 時間の割合)。4 が`region-split-size` GB 未満の場合はデフォルト値は`0.25`です。それ以外の場合はデフォルト値は`0.75`です。

リージョンが10 秒連続して次のいずれかの条件を満たす場合、TiKV はリージョンを分割しようとします。

-   読み取り要求の合計が`split.qps-threshold`超えます。
-   トラフィックが`split.byte-threshold`超えます。
-   統合読み取りプール内の CPU 使用率が`split.region-cpu-overload-threshold-ratio`を超えています。

Load Base Split はデフォルトで有効になっていますが、パラメータはかなり高い値に設定されています。この機能を無効にする場合は、 `split.qps-threshold`と`split.byte-threshold`十分に高く設定し、同時に`split.region-cpu-overload-threshold-ratio`から`0`を設定します。

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

-   TiKV を使用する:

    ```shell
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.qps-threshold":"1500"}'
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.byte-threshold":"15728640"}'
    curl -X POST "http://ip:status_port/config" -H "accept: application/json" -d '{"split.region-cpu-overload-threshold-ratio":"0.5"}'
    ```

したがって、次の 2 つの方法のいずれかで構成を表示できます。

-   SQL ステートメントを使用します。

    ```sql
    show config where type='tikv' and name like '%split.qps-threshold%';
    ```

-   TiKV を使用する:

    ```shell
    curl "http://ip:status_port/config"
    ```

> **注記：**
>
> v4.0.0-rc.2 以降では、SQL ステートメントを使用して構成を変更および表示できます。
