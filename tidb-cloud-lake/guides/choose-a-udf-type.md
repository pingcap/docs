---
title: 选择用户定义函数类型
summary: 了解如何根据返回形式、运行时和运维需求，在 TiDB Cloud Lake 中选择 SQL、聚合、表或外部 UDF。
---

# 选择用户定义函数类型

用户定义函数（UDF）可让你封装内置 SQL 函数未提供的可复用逻辑。它们可以用于统一业务规则、简化复杂查询、实现自定义聚合、将值展开为多行，或将 SQL 查询连接到独立托管的 Python 服务。

在创建 UDF 之前，请先查看 [SQL 函数参考](/tidb-cloud-lake/sql/sql-function-reference.md)。内置函数通常能提供最简单的实现、最低的执行开销以及最小的运维负担。

## 为什么使用 UDF {#why-use-udfs}

随着分析型工作负载不断增长，相同的转换逻辑往往会出现在许多查询中。将同一个表达式复制到每个查询里，会让行为一致性更难保证，也更难安全地发布变更。

UDF 适用于以下任务：

- 标准化数据清洗、校验和业务计算；
- 封装参数化 SQL 查询；
- 实现需要中间状态的自定义聚合；
- 调用 Python 库、专有逻辑或机器学习模型；
- 将专用计算能力与计算集群 (Warehouse) 独立扩缩容。

一个 UDF 应当只承担一个明确职责。数据移动、调度、流状态、跨连续事件流的连接以及工作流编排，应当放在相应的 Lake SQL、Stream、Task 或集成功能中处理，而不是放在 UDF 内部。

## 了解 UDF 生态 {#understand-the-udf-ecosystem}

{{{ .lake }}} 提供了多种 UDF 执行模型。它们在返回形式、语言、托管方式和运维责任方面各不相同。

| UDF 类型 | 实现 | 输出 | 托管 | 典型用途 |
| --- | --- | --- | --- | --- |
| SQL 标量 UDF | SQL 表达式 | 每个输入行一个值 | 由 {{{ .lake }}} 管理 | 格式化、计算和可重用条件 |
| 脚本标量 UDF | Python 或 JavaScript | 每个输入行一个值 | 由 {{{ .lake }}} 管理 | 业务规则、验证和结构化数据处理 |
| WebAssembly 标量 UDF | WebAssembly 模块 | 每个输入行一个值 | 由 {{{ .lake }}} 管理 | 编译为 WebAssembly 的计算密集型逻辑 |
| 聚合 UDF | Python 或 JavaScript | 每个组一个值 | 由 {{{ .lake }}} 管理 | 自定义有状态聚合 |
| SQL 表 UDF | SQL 查询 | 一个结果集 | 由 {{{ .lake }}} 管理 | 可重用的参数化查询 |
| 外部标量 UDF | Python UDF Server | 每个输入行一个值 | 由您托管 | 库、模型和专有服务 |
| 外部表 UDF | Python UDF Server | 多列或多行 | 由您托管 | 分词、扩展和记录生成 |

聚合 UDF 和表 UDF 解决的是不同问题。聚合 UDF 会消费多行并返回一个值。表 UDF 则返回一个结果集。{{{ .lake }}} 不提供同时结合这两种执行模型的 Python 表聚合 UDF。

## 选择最简单的执行模型 {#choose-the-simplest-execution-model}

选择实现时，建议按以下顺序进行：

1. 如果内置函数已经能提供所需行为，优先使用内置函数。
2. 如果 SQL 能清晰表达该逻辑，使用 SQL 标量 UDF 或表 UDF。
3. 如果是应在 {{{ .lake }}} 内运行的脚本逻辑，使用内嵌 Python 或 JavaScript 标量 UDF。
4. 如果是以编译模块形式交付的计算密集型标量逻辑，使用 WebAssembly。
5. 如果计算需要自定义聚合状态，使用聚合 UDF。
6. 如果逻辑依赖远程服务、GPU 或独立扩缩容，使用外部 UDF。

以下问题可以帮助你缩小选择范围：

| 问题 | 推荐选项 |
| --- | --- |
| 一个 SQL 表达式能产生结果吗？ | SQL scalar UDF |
| 行级别逻辑是否需要 Python 或 JavaScript？ | Script scalar UDF |
| 计算密集型行级别逻辑是否需要已编译、可移植的模块？ | WebAssembly scalar UDF |
| SQL 查询是否需要返回多行？ | SQL table UDF |
| 是否必须将多个输入行组合成一个自定义结果？ | Aggregate UDF |
| 一个输入是否需要产生多行由 Python 生成的结果？ | External table UDF |
| 该逻辑是否需要 Python 包、模型、网络调用或单独的计算资源？ | External scalar or table UDF |

## 使用 SQL 标量 UDF 实现可复用转换 {#use-sql-scalar-udfs-for-reusable-transformations}

SQL 标量 UDF 会将每一行输入映射为一个值。它非常适合用于计算、字符串规范化和条件业务规则。

### 规范化电话号码 {#normalize-phone-numbers}

以下函数会移除格式化字符，以便下游查询统一使用一种电话号码表示形式：

```sql
CREATE FUNCTION normalize_phone(phone VARCHAR)
RETURNS VARCHAR
AS $$ REGEXP_REPLACE(phone, '[^0-9]', '') $$;

SELECT normalize_phone('+1 (415) 555-0100');
```

### 应用折扣 {#apply-a-discount}

以下函数将折扣计算集中管理：

```sql
CREATE FUNCTION apply_discount(
    price DECIMAL(10, 2),
    rate DECIMAL(5, 2)
)
RETURNS DECIMAL(10, 2)
AS $$ price * (1 - rate) $$;

SELECT apply_discount(100, 0.15);
```

当共享业务规则发生变化时，使用 [ALTER FUNCTION](/tidb-cloud-lake/sql/alter-function.md)。这样，调用该函数的查询就会使用新的定义，而无需重复编写表达式。

完整语法请参见 [CREATE SCALAR FUNCTION](/tidb-cloud-lake/sql/create-scalar-function.md)。

## 使用 Python 标量 UDF 处理数据逻辑 {#use-python-scalar-udfs-for-data-processing-logic}

当逻辑需要控制流、Python 标准库，或需要使用难以用 SQL 表达的包时，Python 标量 UDF 非常有用。

以下函数会规范化地址中的空白和大小写：

```sql
CREATE FUNCTION normalize_address(value VARCHAR)
RETURNS VARCHAR
LANGUAGE python
HANDLER = 'normalize_address'
AS $$
def normalize_address(value):
    return " ".join(value.strip().upper().split())
$$;

SELECT normalize_address('  123 Main Street  ');
```

Python UDF 还可以使用 `PACKAGES` 指定 PyPI 依赖，并使用 `IMPORTS` 引用存储在 stage 中的文件。请尽量保持依赖精简，以便函数环境更容易复现和维护。

## 使用 JavaScript 标量 UDF 进行 JSON 转换 {#use-javascript-scalar-udfs-for-json-transformations}

JavaScript 非常适合对象和 JSON 转换，尤其是在相关逻辑已经存在于应用代码库中的情况下。

以下函数会规范化电子邮件地址并移除敏感字段：

```sql
CREATE FUNCTION clean_profile(value VARIANT)
RETURNS VARIANT
LANGUAGE javascript
HANDLER = 'cleanProfile'
AS $$
export function cleanProfile(value) {
    const result = { ...value };
    if (typeof result.email === 'string') {
        result.email = result.email.trim().toLowerCase();
    }
    delete result.ssn;
    return result;
}
$$;
```

请保持输入和返回 schema 稳定。对象结构的变化可能会影响每一个调用该函数的查询。

## 使用 WebAssembly UDF 实现编译逻辑 {#use-webassembly-udfs-for-compiled-logic}

WebAssembly UDF 将编译后的代码封装为可移植模块。它适用于计算密集型标量逻辑，尤其是在编译实现比脚本运行时更合适时。

将实现所需 Arrow UDF 接口的模块上传到某个 stage，然后注册其 handler：

```sql
CREATE FUNCTION fib_wasm(value INT)
RETURNS INT
LANGUAGE wasm
HANDLER = 'fib'
AS $$ @my_wasm_stage/arrow_udf_example.wasm $$;

SELECT fib_wasm(10);
```

该模块必须导出指定名称的 handler，并使用与 SQL 兼容的输入和输出类型。在将该函数发布给其他用户之前，请先使用具有代表性的值对编译产物进行测试。

## 使用聚合 UDF 实现自定义有状态计算 {#use-aggregate-udfs-for-custom-stateful-calculations}

聚合 UDF 用于定义如何：

1. 创建初始聚合状态；
2. 将每一行输入添加到状态中；
3. 合并分布式执行产生的部分状态；
4. 将最终状态转换为单个结果。

以下 Python 聚合会对值求和。对于这个特定计算，更推荐使用内置的 `SUM`，但该示例展示了自定义聚合所需的生命周期：

```sql
CREATE FUNCTION py_total(value BIGINT)
STATE { total BIGINT }
RETURNS BIGINT
LANGUAGE python
AS $$
class State:
    def __init__(self):
        self.total = 0

def create_state():
    return State()

def accumulate(state, value):
    state.total += value
    return state

def merge(left, right):
    left.total += right.total
    return left

def finish(state):
    return state.total
$$;

SELECT py_total(number) FROM numbers(5);
```

聚合 UDF 支持 Python 和 JavaScript。仅当内置聚合函数无法表达所需的状态转换或最终处理逻辑时，才应使用它们。更多示例，请参见 [CREATE AGGREGATE FUNCTION](/tidb-cloud-lake/sql/create-aggregate-function.md)。

## 使用 SQL 表 UDF 复用结果集 {#use-sql-table-udfs-for-reusable-result-sets}

SQL 表 UDF 封装一个 SQL 查询，并返回行和列。它适用于可复用的过滤条件、小型报表数据集以及参数化转换。

```sql
CREATE FUNCTION small_numbers(max_value INT)
RETURNS TABLE(value UINT64, doubled UINT64)
AS $$
    SELECT number AS value, number * 2 AS doubled
    FROM numbers(10)
    WHERE number < max_value
$$;

SELECT * FROM small_numbers(3);
```

函数体是一个 SQL 查询。它不接受 `LANGUAGE python`。如果需要返回由 Python 生成的行，请使用外部表 UDF。

完整语法请参见 [CREATE TABLE FUNCTION](/tidb-cloud-lake/sql/create-table-function.md)。

## 使用外部 Python UDF 实现专用逻辑 {#use-external-python-udfs-for-specialized-logic}

[`tidbcloudlake-udf`](https://pypi.org/project/tidbcloudlake-udf/) 包提供了一个 Python UDF Server，用于外部标量 UDF 和表 UDF。Python 进程运行在你的基础设施上，因此你可以使用自定义包、专有代码、GPU 计算以及独立扩缩容。

### 使用 Python 规范化地址 {#normalize-addresses-with-python}

安装 SDK：

```shell
python3 -m pip install tidbcloudlake-udf
```

定义 handler 并启动服务器：

```python
from tidbcloudlake_udf import UDFServer, udf


@udf(
    input_types=["VARCHAR"],
    result_type="VARCHAR",
    skip_null=True,
)
def normalize_address(value: str) -> str:
    return " ".join(value.strip().upper().split())


if __name__ == "__main__":
    server = UDFServer("0.0.0.0:8815")
    server.add_function(normalize_address)
    server.serve()
```

部署服务器并将其加入 allowlist 后，注册该 handler：

```sql
CREATE FUNCTION normalize_address(value VARCHAR)
RETURNS VARCHAR
LANGUAGE python
HANDLER = 'normalize_address'
ADDRESS = 'https://udf.example.com';
```

### 将文本展开为多行 {#expand-text-into-rows}

外部表 UDF 在 `result_type` 中使用输出列列表：

```python
@udf(
    input_types=["VARCHAR"],
    result_type=[("token", "VARCHAR")],
    skip_null=True,
)
def split_words(value: str):
    return [{"token": token} for token in value.split()]
```

注册并调用该表 handler：

```sql
CREATE FUNCTION split_words(value VARCHAR)
RETURNS TABLE(token VARCHAR)
LANGUAGE python
HANDLER = 'split_words'
ADDRESS = 'https://udf.example.com';

SELECT * FROM split_words('external UDF server');
```

有关完整的服务器、部署、并发和注册工作流，请参见 [CREATE FUNCTION](/tidb-cloud-lake/sql/create-function.md)。

## 安全部署外部 UDF {#deploy-external-udfs-securely}

在注册外部函数之前：

- 将 UDF Server 部署到公共 HTTPS 端点。
- 联系 TiDB Cloud Support，将该端点主机名添加到你的租户 UDF server allowlist 中。
- 在网关层配置认证、容量、超时、高可用、升级和监控。
- 将凭据保存在服务器部署环境中，而不是 SQL 函数定义里。

SQL `ADDRESS` 必须包含公共端点。服务器进程可以在其部署环境内部监听 `0.0.0.0`，但对于 Cloud 查询服务的调用来说，`localhost` 和 `0.0.0.0` 都不是有效地址。

外部 UDF 会增加网络延时。对于对延时敏感的逐行调用，应尽量保持调用轻量；在可能的情况下进行批处理；并避免在单个查询中重复调用同一个高开销函数。

## 比较性能与运维要求 {#compare-performance-and-operations}

性能取决于函数复杂度、输入大小、包启动、计算集群 (Warehouse) 资源、网络延时、批大小以及 UDF Server 容量。在其他产品或部署中测得的结果，不能用于预测 Lake 的性能。

| UDF 类型 | 主要开销 | 运维责任 |
| --- | --- | --- |
| SQL 标量 UDF | SQL 表达式求值 | 由 {{{ .lake }}} 管理 |
| Python 或 JavaScript 标量 UDF | 脚本运行时和依赖关系初始化 | 由 {{{ .lake }}} 管理 |
| WebAssembly 标量 UDF | 模块加载和已编译函数执行 | 由 {{{ .lake }}} 管理 |
| 聚合 UDF | 脚本运行时和状态序列化 | 由 {{{ .lake }}} 管理 |
| SQL 表 UDF | 查询执行 | 由 {{{ .lake }}} 管理 |
| 外部 UDF | 网络传输和外部计算 | 由 {{{ .lake }}} 和你的 UDF Server 部署共同负责 |

请使用具有代表性的数据和并发，对实际函数进行基准测试。测量查询延时、吞吐、错误处理、冷启动以及外部服务饱和情况。

## 遵循 UDF 最佳实践 {#follow-udf-best-practices}

- 在引入脚本或服务之前，优先使用内置函数和 SQL。
- 在可能的情况下，让每个函数保持确定性且职责单一。
- 显式定义 NULL 行为，并测试可为空输入。
- 使用精确的输入和返回类型，避免不必要的类型转换。
- 对于聚合 UDF，应让 `merge` 满足结合性，以便安全地合并部分状态。
- 对于外部 UDF，可对面向批处理的库使用 `batch_mode`，对 I/O 密集型逐行处理使用 `io_threads`。
- 设置 `max_concurrency`，防止外部依赖过载。
- 将外部 handler 变更视为服务 API 变更，并以与已注册 SQL 定义兼容的方式进行部署。
- 对用户托管服务器监控错误、延时、饱和度和依赖关系健康状态。
- 同时移除未使用的 UDF 注册项和服务器 handler。

## 开始使用 {#get-started}

根据所需输出选择下一步：

- [CREATE SCALAR FUNCTION](/tidb-cloud-lake/sql/create-scalar-function.md)：用于可复用的 SQL 表达式。
- [CREATE AGGREGATE FUNCTION](/tidb-cloud-lake/sql/create-aggregate-function.md)：用于自定义 Python 或 JavaScript 聚合状态。
- [CREATE TABLE FUNCTION](/tidb-cloud-lake/sql/create-table-function.md)：用于可复用的 SQL 结果集。
- [CREATE FUNCTION](/tidb-cloud-lake/sql/create-function.md)：用于外部 Python 标量和表 handler。
- [外部 AI 函数](/tidb-cloud-lake/guides/external-ai-functions.md)：用于模型推导示例。

## 相关资源 {#related-resources}

- [用户定义函数](/tidb-cloud-lake/sql/user-defined-function.md)
- [外部函数](/tidb-cloud-lake/sql/external-function.md)
- [`tidbcloud/lake-udf` on GitHub](https://github.com/tidbcloud/lake-udf)