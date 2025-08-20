---
title: 导入数据的 CSV 配置
summary: 了解如何在 TiDB Cloud 的导入数据服务中使用 CSV 配置。
---

# 导入数据的 CSV 配置

本文档介绍了在 TiDB Cloud 的导入数据服务中使用的 CSV 配置。

以下是在 TiDB Cloud 的导入数据服务中导入 CSV 文件时的 CSV 配置窗口。更多信息，参见 [Import CSV Files from Cloud Storage into TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md)。

<img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/import-data-csv-config.png" width="500" />

## Separator

- 定义：定义字段分隔符。可以是一个或多个字符，但不能为空。

- 常用值：

    * `,` 用于 CSV（逗号分隔值）。如上图所示，"1"、"Michael" 和 "male" 代表三个字段。
    * `"\t"` 用于 TSV（制表符分隔值）。

- 默认值：`,`


## Delimiter

- 定义：定义用于引用的定界符。如果 **Delimiter** 为空，则所有字段都不加引号。

- 常用值：

    * `'"'` 使用双引号对字段进行引用。如上图所示，`"Michael","male"` 代表两个字段。注意，两个字段之间必须有一个 `,`。如果数据为 `"Michael""male"`（没有 `,`），导入任务将无法解析。如果数据为 `"Michael,male"`（只有一个双引号），则会被解析为一个字段。
    * `''` 表示不启用引用。

- 默认值：`"`


## Null Value

- 定义：定义在 CSV 文件中表示 `NULL` 值的字符串。

- 默认值：`\N`


## Backslash Escape

- 定义：控制是否将字段中的反斜杠解析为转义字符。如果启用 **Backslash Escape**，则会识别并转换以下转义序列：

    | 序列    | 转换为                      |
    |---------|-----------------------------|
    | `\0`    | 空字符（`U+0000`）          |
    | `\b`    | 退格（`U+0008`）            |
    | `\n`    | 换行（`U+000A`）            |
    | `\r`    | 回车（`U+000D`）            |
    | `\t`    | 制表符（`U+0009`）          |
    | `\Z`    | Windows EOF（`U+001A`）     |

    其他情况下（例如 `\"`），反斜杠会被去除，保留下一个字符（`"`）在字段中。被保留的字符没有特殊含义（例如分隔符），只是普通字符。是否加引号不会影响反斜杠是否被解析为转义字符。

    以以下字段为例：

    - 如果该值为 True，`"nick name is \"Mike\""` 会被解析为 `nick name is "Mike"` 并写入目标表。
    - 如果该值为 False，则会被解析为三个字段：`"nick name is \"`、`Mike\` 和 `""`。但由于字段之间没有分隔，无法正确解析。

    对于标准的 CSV 文件，如果字段中需要记录双引号字符，需要使用两个双引号进行转义。在这种情况下，使用 `Backslash escape = True` 会导致解析错误，而使用 `Backslash escape = False` 则可以正确解析。典型场景是导入的字段包含 JSON 内容。标准 CSV 的 JSON 字段通常如下存储：

    `"{""key1"":""val1"", ""key2"": ""val2""}"`

    此时，可以设置 `Backslash escape = False`，该字段会被正确转义到数据库中，如下所示：

    `{"key1": "val1", "key2": "val2"}`

    如果 CSV 源文件的内容以如下方式保存为 JSON，则可以考虑设置 `Backslash escape = True`，如下所示。但这并不是 CSV 的标准格式。

    `"{\"key1\": \"val1\", \"key2\":\"val2\" }"`

- 默认值：启用


## Skip Header

- 定义：控制是否跳过 CSV 文件的表头行。如果启用 **Skip Header**，则在导入时会跳过 CSV 文件的第一行。

- 默认值：禁用