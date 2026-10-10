---
title: EXPLAIN PERF
summary: クエリの CPU 使用状況をプロファイリングし、すべてのクラスター ノードから収集した HTML フレームグラフを返します。
---

# EXPLAIN PERF

`EXPLAIN PERF` は、CPU プロファイリングを実行するためにスタックトレースを収集します。このコマンドは、現在のクラスター内のすべてのノードから収集したデータをもとに生成されたフレームグラフを含む HTML ファイルを返します。この HTML ファイルはブラウザで直接開くことができます。

クエリ性能の分析や、ボトルネックの特定に役立ちます。

## 構文 {#syntax}

```sql
EXPLAIN PERF <statement>
```

## 例 {#examples}

```shell
lakesql --quote-style never --query="EXPLAIN PERF SELECT avg(number) FROM numbers(10000000)" > demo.html
```

その後、ブラウザで `demo.html` ファイルを開いてフレームグラフを表示できます。

クエリが非常に短時間で終了する場合、十分なデータを収集できず、フレームグラフが空になることがあります。