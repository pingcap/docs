---
title: TiDB Cloud Lake JSON（Variant）的工作原理
summary: TiDB Cloud Lake 通过将原生二进制布局与自动 JSON 索引相结合，重新定义了 JSON 分析，使半结构化数据能够像一等列一样工作。
---

# TiDB Cloud Lake JSON（Variant）的工作原理

另请参阅：

- [Variant 数据类型](/tidb-cloud-lake/sql/variant.md)
- [半结构化函数](/tidb-cloud-lake/guides/load-semi-structured-data.md)

{{{ .lake }}} 通过将原生二进制布局与自动 JSON 索引相结合，重新定义了 JSON 分析，使半结构化数据能够像一等列一样工作。

## 为什么 Variant 很重要 {#why-variant-matters}

{{{ .lake }}} 在保持 JSON 灵活性的同时提供 MPP 速度：你可以按原样导入文档，使用熟悉的 SQL 进行查询，而引擎会在幕后将性能相关的工作串联起来。之所以能够做到这一点，依赖于两个支柱：

- 紧凑的 **JSONB** 布局让执行引擎能够感知类型。
- 自动 **virtual columns**——{{{ .lake }}} 的 JSON 索引——无需手动操作即可暴露热点路径。

从存储到查询，本文档其余部分将说明这两个理念如何将原始 JSON 负载（例如 `orders.data`）转换为经过优化的类型化列。

## JSON 存储布局 {#json-storage-layout}

{{{ .lake }}} 以 JSONB 格式存储 Variant 值，这是一种针对分析场景优化的二进制格式。实际效果包括：

- **类型化存储** – 数字、布尔值、时间戳和 decimal 会保持原生类型，因此比较操作能够保持二进制安全。
- **可预测的布局** – 字段带有长度前缀和规范化的键顺序，从而消除重复解析的开销。
- **零拷贝访问** – 操作符在扫描和排序期间直接读取 JSONB 缓冲区，而不是重新构建 JSON 文本。

每个 Variant 列都会保留原始 JSONB 文档以确保保真度。当像 `data['user']['id']` 这样的路径反复出现时，{{{ .lake }}} 会将它们收纳到类型化的 sidecar 列中，以便进行下推的处理。

## 自动生成 JSON 索引 {#automatic-json-index-generation}

当新数据进入 {{{ .lake }}} 时，一个轻量级索引流水线会立即扫描 JSON block，以发现值得物化为 virtual columns 的热点路径——也就是 {{{ .lake }}} 内置的 JSON 索引。

### 导入流程 {#ingestion-flow}

{{{ .lake }}} 会检查传入批次，并将重复出现的访问模式转换为类型化列：

```
┌───────────────────────────────────────────────┐
│ Variant Ingestion Flow                        │
├──────────────┬────────────────────────────────┤
│ Sample Rows  │ Peek at the first rows in block │
│ Detect Paths │ Keep stable leaf key paths      │
│ Infer Types  │ Pick native column types        │
│ Materialize  │ Write values to virtual Parquet │
│ Register     │ Attach metadata to base column  │
└──────────────┴────────────────────────────────┘
```

### 轻量化设计 {#lightweight-by-design}

该流水线依赖少量轻量级启发式规则：

```
┌─────────────────────────────┬──────────────────────────────────────────────┐
│ Step                        │ Heuristic                                    │
├─────────────────────────────┼──────────────────────────────────────────────┤
│ Sampling                    │ Inspect only the first 10 rows of each block │
│ Null & non-leaf filtering   │ Skip paths dominated by NULL or pointing to  │
│                             │ objects/arrays                               │
│ Stability check             │ Promote only leaf paths that stay consistent │
│                             │ across the sample (max 1,000 per block)      │
│ Deduplication               │ Use hashing to avoid analysing the same path │
│                             │ repeatedly                                    │
│ Fallback                    │ Keep the original JSONB document when no     │
│                             │ candidate survives                           │
└─────────────────────────────┴──────────────────────────────────────────────┘
```

结果是：你只需加载一次 JSON，重复出现的模式就会悄然转换为经过优化的类型化列，无需 DDL，也无需调优。

### Virtual columns 就是自动 JSON 索引 {#virtual-columns-are-automatic-json-indexes}

在这里，“virtual column” 本质上就是 **{{{ .lake }}} 的 JSON 索引**。导入流程会判断诸如 `data['items'][0]['price']` 这样的路径是否足够稳定，推导原生类型，并将这些值连同元信息一起写入列式 sidecar——无需 DDL，也无需任何参数调节。嵌套 JSON 仍然以紧凑的 JSONB 形式保留，而原语路径则会变成原生数字、字符串或布尔值。

```
Raw JSON block ──(auto sampling)──▶ Candidate paths ──(stable?)──▶ JSON index
```

与构建单独的 B-tree 不同，{{{ .lake }}} 会将某个 JSON 路径的值快照到列式结构中：

```
JSON Path    ───────────▶  Virtual Column (typed values + stats + location)
```

在查询期间，规划器可以像命中索引一样直接跳转到这些预提取的值；如果索引项缺失，仍然可以回退到完整 JSON。

### JSON 索引元信息 {#json-index-metadata}

与每个 block 一起存储的元信息会汇总这些额外列：

```
┌────────────────────────────┬───────────────────────┐
│ Virtual Column Metadata    │ Example               │
├────────────────────────────┼───────────────────────┤
│ Column Id & JSON Path      │ v123 -> ['user']['id'] │
│ Type Code                  │ UInt64 / String       │
│ Byte Offset & Length       │ Where values live     │
│ Row Count                  │ Matches base block    │
│ Statistics                 │ Min / Max / NDV       │
└────────────────────────────┴───────────────────────┘
```

写入器会将这些细节打包进表快照，并将 sidecar 与主 block 一起存储。每个条目都会记录 JSON 路径、原生类型、字节偏移和统计信息，以便 {{{ .lake }}} 在需要时直接跳转到提取后的值——或者回退到原始 JSON。

## 使用 JSON 索引执行查询 {#query-execution-with-json-indexes}

一旦索引存在，读路径就简化为三个快速决策：

```
┌──────────────┐   rewrite paths   ┌────────────────────┐
│ SQL Planner  │------------------>│ Virtual Column Map │
└──────┬───────┘                   └─────────┬──────────┘
       │ pushdown request                   │ per-block check
       ▼                                    ▼
┌──────────────┐   has virtual?   ┌────────────────────┐
│ Fuse Storage │----------------->│ Virtual File Read  │
└──────┬───────┘        │        └─────────┬──────────┘
       │ no             └------------------┘ fallback
       ▼
┌──────────────┐
│ JSONB Reader │
└──────┬───────┘
       ▼
┌──────────────┐
│ Query Output │
└──────────────┘
```

- 在规划阶段，只要元信息表明索引存在，{{{ .lake }}} 就会将 `get_by_keypath` 之类的调用重写为直接读取 virtual column。
- 如果 virtual column 存在，存储层就会命中它，并且只读取对应的 Parquet 切片；如果所有请求的路径都已建立索引，甚至可以跳过原始 JSON 列。
- 否则，它会回退到在 JSONB 列上计算 `get_by_keypath`，从而保持语义不变。
- 过滤、投影和统计信息都基于原生类型运行，而不是重新解析 JSON 字符串。

在幕后，{{{ .lake }}} 会跟踪每个 virtual column 是由哪个 JSON 路径生成的，因此它能够准确判断何时可以跳过原始文档，何时需要重新打开它。

## 使用 Variant 数据 {#working-with-variant-data}

由于索引工作都在幕后自动完成，你可以使用熟悉的语法和函数与 Variant 列交互。

### 查看 virtual columns {#inspect-virtual-columns}

使用 [`SHOW VIRTUAL COLUMNS`](/tidb-cloud-lake/sql/show-virtual-columns.md) 可以列出表中自动生成的 virtual columns，以便在需要时验证 {{{ .lake }}} 已将哪些 JSON 路径物化。

### 访问语法 {#access-syntax}

{{{ .lake }}} 同时支持 Snowflake 风格和 PostgreSQL 风格的选择器；无论你偏好哪种风格，引擎都会通过同一个 key-path 解析器处理它们，并复用 JSON 索引。继续以 `orders` 为例，你可以像下面这样访问嵌套字段：

```sql title="Snowflake-style examples"
SELECT data['user']['profile']['name'],
       data:user:profile.settings.theme,
       data['items'][0]['price']
FROM orders;
```

```sql title="PostgreSQL-style examples"
SELECT data->'user'->'profile'->>'name',
       data#>>'{user,profile,settings,theme}',
       data @> '{"user":{"id":123}}'
FROM orders;
```

### 函数亮点 {#function-highlights}

除了路径访问器之外，{{{ .lake }}} 还提供了丰富的 Variant 工具集：

- **解析与类型转换**: `parse_json`, `try_parse_json`, `to_variant`, `to_jsonb_binary`
- **导航与投影**: `get_path`, `get_by_keypath`, `flatten`, arrow (`->`, `->>`), path (`#>`, `#>>`) and containment operators (`@>`, `?`)
- **修改**: `object_insert`, `object_remove_keys`, concatenation (`||`), `array_*` helpers
- **分析**: `json_extract_keys`, `json_length`, `jsonb_array_elements`, 以及诸如 `json_array_agg` 之类的聚合函数

所有函数都直接在向量化引擎内部的 JSONB 缓冲区上运行。

## 性能特征 {#performance-characteristics}

- 与原始 JSON 扫描相比的内部基准测试结果：
    - 单路径查找：**约 3× 更快**，扫描数据量减少 **约 26×**。
    - 多路径投影：**约 1.4× 更快**，读取数据量减少 **约 5.5×**。
    - 谓词下推可与 bloom/inverted indexes 组合使用，以裁剪 block。
- JSON 结构越稳定，越多路径能够满足索引条件。

## {{{ .lake }}} 在 Variant 数据上的优势 {#lake-advantages-for-variant-data}

- **Snowflake-compatible surface area** – 可以原样迁移现有查询和 UDF。
- **原生 JSONB 执行** – 类型化编码加上向量化操作符可避免字符串搬运。
- **自动 JSON 索引** – 采样、元信息和下推让半结构化数据具备结构化数据般的体验。
- **运维效率** – Virtual block 与常规 Fuse block 共享生命周期工具，使存储和计算保持可预测。

借助自动 JSON 索引，{{{ .lake }}} 缩小了灵活文档与高性能分析之间的差距——半结构化数据在你的计算集群中成为一等公民。