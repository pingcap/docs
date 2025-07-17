---
title: Table Filter
summary: 在 TiDB 工具中使用表过滤功能。
---

# Table Filter

TiDB 迁移工具默认对所有数据库进行操作，但 oftentimes 只需要其中的子集。例如，你可能只想处理以 `foo*` 和 `bar*` 形式的 schema，而不涉及其他。

自 TiDB 4.0 版本起，所有 TiDB 迁移工具共享一种通用的过滤语法，用于定义子集。本文件描述如何使用表过滤功能。

## Usage

### CLI

可以通过多个 `-f` 或 `--filter` 命令行参数对工具应用表过滤。每个过滤规则的格式为 `db.table`，其中每一部分可以是通配符（在[下一节](#wildcards)中进一步说明）。以下列出示例用法。

<CustomContent platform="tidb">

* [BR](/br/backup-and-restore-overview.md):

    ```shell
    tiup br backup full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    ```

    ```shell
    tiup br restore full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    ```

</CustomContent>

* [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview):

    ```shell
    tiup dumpling -f 'foo*.*' -f 'bar*.*' -P 3306 -o /tmp/data/
    ```

<CustomContent platform="tidb">

* [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md):

    ```shell
    tiup tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    ```

</CustomContent>

<CustomContent platform="tidb-cloud">

* [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview):

    ```shell
    tiup tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    ```

</CustomContent>

### TOML 配置文件

TOML 文件中的表过滤规则以 [字符串数组](https://toml.io/en/v1.0.0-rc.1#section-15) 形式指定。以下列出示例用法。

* TiDB Lightning:

    ```toml
    [mydumper]
    filter = ['foo*.*', 'bar*.*']
    ```

<CustomContent platform="tidb">

* [TiCDC](/ticdc/ticdc-overview.md):

    ```toml
    [filter]
    rules = ['foo*.*', 'bar*.*']

    [[sink.dispatchers]]
    matcher = ['db1.*', 'db2.*', 'db3.*']
    dispatcher = 'ts'
    ```

</CustomContent>

## 语法

### 普通表名

每个表过滤规则由“schema 模式”和“表 模式”组成，用点（`.`）分隔。完全限定名匹配规则的表将被接受。

```
db1.tbl1
db2.tbl2
db3.tbl3
```

普通名称必须仅由有效的 [标识符字符](/schema-object-names.md) 组成，例如：

* 数字（`0` 到 `9`）
* 字母（`a` 到 `z`，`A` 到 `Z`）
* `$`
* `_`
* 非 ASCII 字符（U+0080 到 U+10FFFF）

所有其他 ASCII 字符为保留字符。某些标点符号具有特殊含义，详见下一节。

### 通配符

名称的每一部分可以是 [fnmatch(3)] 中描述的通配符符号：

* `*` — 匹配零个或多个字符
* `?` — 匹配一个字符
* `[a-z]` — 匹配范围在 “a” 到 “z” 之间的一个字符
* `[!a-z]` — 匹配除 “a” 到 “z” 之外的一个字符

```
db[0-9].tbl[0-9a-f][0-9a-f]
data.*
*.backup_*
```

这里的“字符”指的是 Unicode 码点，例如：

* U+00E9（é）是 1 个字符。
* U+0065 U+0301（é）是 2 个字符。
* U+1F926 U+1F3FF U+200D U+2640 U+FE0F（🤦🏿‍♀️）是 5 个字符。

### 文件导入

若要将文件作为过滤规则导入，在规则前加上 `@` 来指定文件名。表过滤解析器会将导入文件的每一行视为额外的过滤规则。

例如，文件 `config/filter.txt` 内容如下：

```
employees.*
*.WorkOrder
```

以下两个调用等价：

```bash
tiup dumpling -f '@config/filter.txt'
tiup dumpling -f 'employees.*' -f '*.WorkOrder'
```

一个过滤文件不能再导入其他文件。

### 注释与空行

在过滤文件中，每行的前后空白字符会被裁剪。空白行（空字符串）会被忽略。

以 `#` 开头的行为注释行，系统会忽略。`#` 不在行首则视为语法错误。

```
# this line is a comment
db.table   # but this part is not comment and may cause error
```

### 排除规则

以 `!` 开头的规则表示其后模式用于排除不处理的表。这实际上将过滤器变成了一个阻止列表。

```
*.*
#^ note: must add the *.* to include all tables first
!*.Password
!employees.salaries
```

### 转义字符

若要将特殊字符作为标识符字符使用，在其前面加上反斜杠 `\`。

```
db\.with\.dots.*
```

为简便起见及未来兼容，禁止使用以下序列：

* 行尾的 `\`（在裁剪空白后）——请用 `[ ]` 来匹配字面空白字符
* `\` 后跟任何 ASCII 字母数字字符（`[0-9a-zA-Z]`）。特别是，类似 C 语言的转义序列如 `\0`、`\r`、`\n` 和 `\t` 目前无意义。

### 引号标识符

除了 `\`，还可以用 `"` 或 `` ` `` 引用特殊字符以抑制其特殊含义。

```
"db.with.dots"."tbl\1"
`db.with.dots`.`tbl\2`
```

引号可以在标识符中通过重复自身来包含。

```
"foo""bar".`foo``bar`
# 等价于：
foo\"bar.foo\`bar
```

引号标识符不能跨多行。

部分引号的标识符是无效的，例如：

```
"this is "invalid*.*
```

### 正则表达式

如果需要非常复杂的规则，可以用 `/` 包裹的正则表达式定义每个模式：

```
/^db\d{2,}$/./^tbl\d{2,}$/
```

这些正则表达式使用 [Go 方言](https://pkg.go.dev/regexp/syntax?tab=doc)。如果标识符中包含匹配正则表达式的子串，则匹配。例如，`/b/` 会匹配 `db01`。

> **Note:**
>
> 每个 `/` 在正则表达式中都必须用 `\/` 转义，包括在 `[ ]` 内。不能在 `\Q…\E` 之间放置未转义的 `/`。

## 多个规则

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 这部分内容不适用于 TiDB Cloud。目前，TiDB Cloud 仅支持一个表过滤规则。

</CustomContent>

当表名未匹配过滤列表中的任何规则时，默认行为是忽略这些未匹配的表。

若要建立阻止列表，必须在第一个规则中明确使用 `*.*`，否则所有表都将被排除。

```bash
# 所有表都将被过滤
tiup dumpling -f '!*.Password'

# 仅过滤掉 “Password” 表，其余都包含
tiup dumpling -f '*.*' -f '!*.Password'
```

在过滤列表中，如果一个表名匹配多个模式，最后匹配的规则决定结果。例如：

```
# 规则 1
employees.*
# 规则 2
!*.dep*
# 规则 3
*.departments
```

过滤结果如下：

| 表名                  | 规则 1 | 规则 2 | 规则 3 | 结果             |
|-----------------------|--------|--------|--------|------------------|
| irrelevant.table      |        |        |        | 默认（拒绝）     |
| employees.employees   | ✓      |        |        | 规则 1（接受）   |
| employees.dept_emp    | ✓      | ✓      |        | 规则 2（拒绝）   |
| employees.departments | ✓      | ✓      | ✓      | 规则 3（接受）   |
| else.departments      |        | ✓      | ✓      | 规则 3（接受）   |

> **Note:**
>
> 在 TiDB 工具中，系统 schema 默认不包含在过滤中。系统 schema 有：
>
> * `INFORMATION_SCHEMA`
> * `PERFORMANCE_SCHEMA`
> * `METRICS_SCHEMA`
> * `INSPECTION_SCHEMA`
> * `mysql`
> * `sys`