---
title: EXPLAIN ANALYZE GRAPHICAL
summary: ブラウザでインタラクティブな視覚表現を使用してクエリパフォーマンスを分析します。LakeSQL v0.22.2+ でのみ利用できます。
---

# EXPLAIN ANALYZE GRAPHICAL

ブラウザでインタラクティブな視覚表現を使用してクエリパフォーマンスを分析します。LakeSQL v0.22.2+ でのみ利用できます。

## 構文 {#syntax}

```sql
EXPLAIN ANALYZE GRAPHICAL <statement>
```

## 設定 {#configuration}

LakeSQL の設定ファイル `~/.config/lakesql/config.toml` に次を追加します。

```toml
[server]
bind_address = "127.0.0.1"
auto_open_browser = true
```

## 例 {#example}

```sql
EXPLAIN ANALYZE GRAPHICAL SELECT l_returnflag, COUNT(*)
FROM lineitem
WHERE l_shipdate <= '1998-09-01'
GROUP BY l_returnflag;
```

出力:

```bash
View graphical online: http://127.0.0.1:8080?perf_id=1
```

実行計画、各オペレーターの実行時間、およびデータフローを表示するインタラクティブなビューが開きます。

![グラフィカル分析](/media/tidb-cloud-lake/explain-graphical.png)