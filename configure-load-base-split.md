---
title: Load Base Split
summary: Load Base Split の機能について学習します。
---

# ロードベーススプリット {#load-base-split}

Load Base SplitはTiDB 4.0で導入された新機能です。これは、小さなテーブルに対するフルテーブルスキャンなど、リージョン間のアクセスの不均衡によって引き起こされるホットスポット問題を解決することを目的としています。

## シナリオ {#scenarios}

TiDBでは、負荷が特定のノードに集中すると、ホットスポットが発生しやすくなります。PDは、パフォーマンスを向上させるために、ホットな領域がすべてのノードに可能な限り均等に分散されるようにスケジュールを設定します。

ただし、PDスケジューリングの最小単位はリージョンです。クラスター内のホットスポットの数がノード数より少ない場合、または一部のホットスポットの負荷が他のリージョンよりもはるかに大きい場合、PDはホットスポットをあるノードから別のノードに移動することしかできず、クラスター全体で負荷を分散させることはできません。

このシナリオは、完全なテーブルスキャンや小さなテーブルのインデックス検索、一部のフィールドへの頻繁なアクセスなど、主に読み取り要求であるワークロードで特に一般的です。

以前は、この問題の解決策として、1 つ以上のホットスポット領域を分割するコマンドを手動で実行していましたが、この方法には 2 つの問題がありました。

-   リージョンを均等に分割することは、必ずしも最適な選択とは限りません。リクエストが少数のキーに集中する可能性があるためです。このような場合、均等分割後もホットスポットがいずれかのリージョンに残る可能性があり、目的を達成するには複数回の均等分割が必要になる場合があります。
-   人間の介入はタイムリーでも簡単でもない。

## 実施原則 {#implementation-principles}

Load Base Splitは、統計情報に基づいてリージョンを自動的に分割します。読み取り負荷またはCPU使用率が10秒間継続的にしきい値を超えるリージョンを特定し、これらのリージョンを適切な位置で分割します。分割位置の選択にあたっては、分割後の両リージョンのアクセス負荷のバランスを取り、リージョン間のアクセスを回避しようとします。

Load Base Splitによって分割されたリージョンは、すぐにはマージされません。PDの`MergeChecker` 、ホットなリージョンをスキップします。一方、PDはハートビート情報の`QPS`に基づいて2つのリージョンをマージするかどうかを決定します。これにより、 `QPS`の高い2つのリージョンがマージされるのを回避します。

## 使用法 {#usage}

ロード ベース分割機能は現在、次のパラメータによって制御されています。

-   [`split.qps-threshold`](/tikv-configuration-file.md#qps-threshold) :リージョンがホットスポットと判断されるQPSのしきい値。4GB [`region-split-size`](/tikv-configuration-file.md#region-split-size)の場合はデフォルト値は1秒あたり`3000` 、それ以外の場合はデフォルト値は`7000`です。
-   [`split.byte-threshold`](/tikv-configuration-file.md#byte-threshold-new-in-v50) : (v5.0で導入)リージョンがホットスポットとして識別されるトラフィックしきい値。単位はバイトです`region-split-size`が4GB未満の場合はデフォルト値は30MiB/秒、それ以外の場合は100MiB/秒です。
-   [`split.region-cpu-overload-threshold-ratio`](/tikv-configuration-file.md#region-cpu-overload-threshold-ratio-new-in-v620) : (v6.2.0 で導入)リージョンがホットスポットと判断される CPU 使用率のしきい値 (読み取りスレッドプールの CPU 時間の割合)。4 `region-split-size`未満の場合はデフォルト値は`0.25` 、それ以外の場合はデフォルト値は`0.75`です。

リージョンが10 秒連続して次のいずれかの条件を満たした場合、TiKV はリージョンを分割しようとします。

-   読み取り要求の合計が`split.qps-threshold`超えます。
-   トラフィックが`split.byte-threshold`超えています。
-   統合読み取りプール内の CPU 使用率が`split.region-cpu-overload-threshold-ratio`超えています。

ロードベーススプリットはデフォルトで有効になっていますが、パラメータがかなり高い値に設定されています。この機能を無効にするには、 `split.qps-threshold`と`split.byte-threshold`十分に高い値に設定し、同時に`split.region-cpu-overload-threshold-ratio`を`0`に設定してください。

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
