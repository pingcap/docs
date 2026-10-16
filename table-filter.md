---
title: 表库过滤
summary: TiDB 工具中表过滤器功能的使用方法。
---

# 表库过滤

TiDB 迁移工具默认会操作所有数据库，但通常只需要其中的一部分。例如，你只想处理形如 `foo*` 和 `bar*` 的 schema，而不需要其他的。

自 TiDB 4.0 起，所有 TiDB 迁移工具都共享一套通用的过滤器语法来定义子集。本文档介绍如何使用表过滤器功能。

## 使用方法

### CLI

可以通过多个 `-f` 或 `--filter` 命令行参数为工具应用表过滤器。每个过滤器的格式为 `db.table`，其中每一部分都可以是通配符（详见[下一节](#wildcards)）。以下是示例用法。

<CustomContent platform="tidb">

* [BR](/br/backup-and-restore-overview.md)：

    ```shell
    tiup br backup full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    ```

    ```shell
    tiup br restore full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    ```

</CustomContent>

* [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)：

    ```shell
    tiup dumpling -f 'foo*.*' -f 'bar*.*' -P 3306 -o /tmp/data/
    ```

<CustomContent platform="tidb">

* [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)：

    ```shell
    tiup tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    ```

</CustomContent>

<CustomContent platform="tidb-cloud">

* [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)：

    ```shell
    tiup tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    ```

</CustomContent>

### TOML 配置文件

在 TOML 文件中，表过滤器以 [字符串数组](https://toml.io/en/v1.0.0-rc.1#section-15) 的形式指定。以下是示例用法。

* TiDB Lightning：

    ```toml
    [mydumper]
    filter = ['foo*.*', 'bar*.*']
    ```

<CustomContent platform="tidb">

* [TiCDC](/ticdc/ticdc-overview.md)：

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

每条表过滤规则由“schema 模式”和“表模式”组成，两者之间用点（`.`）分隔。只有完全限定名匹配规则的表才会被接受。

```
db1.tbl1
db2.tbl2
db3.tbl3
```

普通名称只能包含有效的[标识符字符](/schema-object-names.md)，例如：

* 数字（`0` 到 `9`）
* 字母（`a` 到 `z`，`A` 到 `Z`）
* `$`
* `_`
* 非 ASCII 字符（U+0080 到 U+10FFFF）

所有其他 ASCII 字符为保留字符。一些标点符号有特殊含义，详见下一节。

### 通配符

名称的每一部分都可以使用 [fnmatch(3)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_13) 中描述的通配符符号：

* `*` — 匹配零个或多个字符
* `?` — 匹配一个字符
* `[a-z]` — 匹配一个介于 "a" 和 "z" 之间的字符（包含两端）
* `[!a-z]` — 匹配一个不是 "a" 到 "z" 的字符

```
db[0-9].tbl[0-9a-f][0-9a-f]
data.*
*.backup_*
```

此处的“字符”指的是一个 Unicode 码点，例如：

* U+00E9 (é) 是 1 个字符。
* U+0065 U+0301 (é) 是 2 个字符。
* U+1F926 U+1F3FF U+200D U+2640 U+FE0F (🤦🏿‍♀️) 是 5 个字符。

### 文件导入

要将文件作为过滤规则导入，在规则开头加上 `@` 并指定文件名。表过滤器解析器会将导入文件的每一行视为额外的过滤规则。

例如，若文件 `config/filter.txt` 内容如下：

```
employees.*
*.WorkOrder
```

则以下两种调用方式等价：

```bash
tiup dumpling -f '@config/filter.txt'
tiup dumpling -f 'employees.*' -f '*.WorkOrder'
```

过滤器文件不能再进一步导入其他文件。

### 注释与空行

在过滤器文件中，每行的首尾空白字符会被去除。此外，空行（空字符串）会被忽略。

以 `#` 开头的行为注释，会被忽略。`#` 若不在行首，则会被视为语法错误。

```
# this line is a comment
db.table   # but this part is not comment and may cause error
```

### 排除规则

以 `!` 开头的规则表示其后的模式用于排除不需要处理的表。这样可以将过滤器变为阻止列表。

```
*.*
#^ 注意：必须先添加 *.* 以包含所有表
!*.Password
!employees.salaries
```

### 转义字符

要将特殊字符作为标识符字符使用，可以在其前面加反斜杠 `\`。

```
db\.with\.dots.*
```

为简化和兼容未来，禁止以下转义序列：

* 去除空白后，`\` 位于行尾（如需匹配行尾的空格，请使用 `[ ]`）。
* `\` 后跟任意 ASCII 字母或数字（`[0-9a-zA-Z]`）。特别是，类似 C 语言的转义序列如 `\0`、`\r`、`\n` 和 `\t` 当前无意义。

### 引号标识符

除了 `\`，也可以通过使用 `"` 或 `` ` `` 对特殊字符进行引用来抑制其特殊含义。

```
"db.with.dots"."tbl\1"
`db.with.dots`.`tbl\2`
```

可以通过重复引号本身将其包含在标识符中。

```
"foo""bar".`foo``bar`
# 等价于：
foo\"bar.foo\`bar
```

带引号的标识符不能跨多行。

部分引用标识符是无效的：

```
"this is "invalid*.*
```

### 正则表达式

如果需要非常复杂的规则，每个模式都可以用 `/` 分隔的正则表达式表示：

```
/^db\d{2,}$/./^tbl\d{2,}$/
```

这些正则表达式采用 [Go 方言](https://pkg.go.dev/regexp/syntax?tab=doc)。只要标识符包含与正则表达式匹配的子串，就会匹配。例如，`/b/` 会匹配 `db01`。

> **注意：**
>
> 正则表达式中的每个 `/` 都必须转义为 `\/`，包括在 `[…]` 内部。不能在 `\Q…\E` 之间放置未转义的 `/`。

## 多条规则

当表名不匹配过滤器列表中的任何规则时，默认行为是忽略这些未匹配的表。

要构建阻止列表，必须将 `*.*` 作为第一条规则，否则所有表都会被排除。

```bash
# 所有表都会被过滤掉
tiup dumpling -f '!*.Password'

# 只有 "Password" 表会被过滤掉，其余表会被包含
tiup dumpling -f '*.*' -f '!*.Password'
```

在过滤器列表中，如果表名匹配多条规则，则以最后一条匹配规则为准。例如：

```
# 规则 1
employees.*
# 规则 2
!*.dep*
# 规则 3
*.departments
```

过滤结果如下：

| 表名                   | 规则 1 | 规则 2 | 规则 3 | 结果                |
|------------------------|--------|--------|--------|---------------------|
| irrelevant.table       |        |        |        | 默认（拒绝）        |
| employees.employees    | ✓      |        |        | 规则 1（接受）      |
| employees.dept_emp     | ✓      | ✓      |        | 规则 2（拒绝）      |
| employees.departments  | ✓      | ✓      | ✓      | 规则 3（接受）      |
| else.departments       |        | ✓      | ✓      | 规则 3（接受）      |

> **注意：**
>
> 在 TiDB 工具中，系统 schema 在默认配置下始终会被排除。系统 schema 包括：
>
> * `INFORMATION_SCHEMA`
> * `PERFORMANCE_SCHEMA`
> * `METRICS_SCHEMA`
> * `INSPECTION_SCHEMA`
> * `mysql`
> * `sys`
