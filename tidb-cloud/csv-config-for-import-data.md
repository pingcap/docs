---
title: CSV Configrations for Importing Data
summary: Learn how to use CSV configurations for the Import Data service on TiDB Cloud.
---

# CSV Configrations for Importing Data

## Separator 

Definition：指定字段分隔符。可以为一个或多个字符，不能为空。常用值：CSV 用 ','
TSV 用 "\t"用于分隔不同字段的记录，如上图所示 1,"Michael","male" 表示 3 个字段的数据。
Default：,

## Header

Definition：是否所有 CSV 文件都包含表头行。如为 true，第一行会被用作列名。如为 false，第一行并无特殊性，按普通的数据行处理。
Default:True

## Delimiter

Definition：指定引用定界符。如果 delimiter 为空，所有字段都会被取消引用。常用值：'"' 使用双引号引用字段，'' 不引用。如上图中的 "Michael" ,"male" 表示两个字段，注意，中间需要用 "," ，举例，如果 "Michael""male"，会导致 import 任务解析报错。如果是"Michael,male" 则表示 1 个字段的数据，
Default:"

## Backslash-escape

Definition：是否解析字段内的反斜线转义符。如果 backslash-escape 为 true，下列转义符会被识别并转换。
转义符        转换为
\0        空字符 (U+0000)
\b        退格 (U+0008)
\n        换行 (U+000A)
\r        回车 (U+000D)
\t        制表符 (U+0009)
\Z        Windows EOF (U+001A)

其他情况下（如 \"）反斜线会被移除，仅在字段中保留其后面的字符（"），这种情况下，保留的字符仅作为普通字符，特殊功能（如界定符）都会失效。引用不会影响反斜线转义符的解析与否。如取值为 True，上图中的 "nick name is \"Mike\"" 会被解析为 nick name is "Mike" 并写入到目标表。如果取值为 False ，则会被解析为 "nick name is\" , Mike\ , "" 3个字段，但是由于字段之间没有 separate，所以会解析错误。

对于标准 CSV 文件，如果字段当中有双引号字符要记录，需要使用 2个双引号来进行转义。这种情况下，使用 backslash-escape = true 来进行处理时会出现解析失败的错误，而使用 backslash-escape = false 则能够正确解析。典型的场景是导入的字段当中有 JSON 内容。一般标准 CSV 的JSON 字段会以如下方式保存：

"{""key1"":""val1"", ""key2"": ""val2""}" 

此时，应当选择 backslash-escape = false，则字段能够被正确转义成如下的字符串保存到数据库中：
{"key1": "val1", "key2": "val2"}

如果 CSV 源文件的内容是以如下方式保存的 JSON，那么可以考虑设置 backslash-escape = true: 
"{\"key1\": \"val1\", \"key2\":\"val2\" }" 。 但是这个不是 CSV 的标准格式。
Default:True

## Not-null 和 Null

Definition：not-null 决定是否所有字段不能为空。如果 not-null 为 false，设定了 null 的字符串会被转换为 SQL NULL 而非具体数值。引用不影响字段是否为空。例如有如下 CSV 文件：
column_A,column_B,column_C
\N,"\N",
在默认设置（not-null = false; null = '\N'）下，列 A and B 导入 TiDB 后都将会转换为 NULL。列 C 是空字符串 ''，但并不会解析为 NULL。
Default：Not-null=False, Null=\N

## trim-last-separator

Definition:将 separator 字段当作终止符，并移除尾部所有分隔符。例如有如下 CSV 文件：A,,B,,
当 trim-last-separator = false，该文件会被解析为包含 5 个字段的行 ('A', '', 'B', '', '')。
当 trim-last-separator = true，该文件会被解析为包含 3 个字段的行 ('A', '', 'B')。
Default:False