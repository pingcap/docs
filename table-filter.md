---
title: Table Filter
summary: Usage of table filter feature in TiDB tools.
category: reference
aliases: ['/docs/dev/tidb-lightning/tidb-lightning-table-filter/', '/docs/dev/reference/tools/tidb-lightning/table-filter/', '/tidb-lightning-table-filter/']
---

# Table Filter

The TiDB ecosystem tools operate on the all databases by default, but oftentimes only a subset is needed. Say, we only want to work with the schemas in the form `foo*` and `bar*` and nothing else.

All TiDB tools since 4.0 share a common filter syntax to define subsets, which we specify here.

## Usage

### CLI

Table filters can be supplied to the tools using multiple `-f` or `--filter` command line parameters. Each filter is in the form `db.table`, where each part can be a wildcard (further explained in the next section). The following lists example usage in each tool.

* [BR](/br/backup-and-restore-tool.md):

    {{< copyable "shell-regular" >}}

    ```bash
    ./br backup full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    #                ^~~~~~~~~~~~~~~~~~~~~~~
    ./br restore full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    #                 ^~~~~~~~~~~~~~~~~~~~~~~
    ```

* [Dumpling](/export-or-backup-using-dumpling.md):

    {{< copyable "shell-regular" >}}

    ```bash
    ./dumpling -f 'foo*.*' -f 'bar*.*' -P 3306 -o /tmp/data/
    #          ^~~~~~~~~~~~~~~~~~~~~~~
    ```

* [Lightning](/tidb-lightning/tidb-lightning-overview.md):

    {{< copyable "shell-regular" >}}

    ```bash
    ./tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    #                ^~~~~~~~~~~~~~~~~~~~~~~
    ```

### TOML configuration files

Table filters in TOML files are specified as [array of strings](https://toml.io/en/v1.0.0-rc.1#section-15). The following lists example usage in each tool.

* Lightning:

    ```toml
    [mydumper]
    filter = ['foo*.*', 'bar*.*']
    ```

* CDC:

    ```toml
    [filter]
    rules = ['foo*.*', 'bar*.*']

    [[sink.dispatchers]]
    matcher = ['db1.*', 'db2.*', 'db3.*']
    dispatcher = 'ts'
    ```

## Syntax

### Plain table names

Each table filter rule consists of a "schema pattern" and a "table pattern", separated by a dot (`.`). Tables which fully-qualified name matching the rules are accepted.

```
db1.tbl1
db2.tbl2
db3.tbl3
```

A plain name must only consist of valid [identifier characters](/schema-object-names.md), that is

* digits (`0` to `9`)
* letters (`a` to `z`, `A` to `Z`)
* `$`
* `_`
* non ASCII characters (U+0080 to U+10FFFF)

All other ASCII characters are reserved. Some punctuations have special meanings, described below.

### Wildcards

Each part of the name can be a wildcard symbol described in [fnmatch(3)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_13):

* `*` — matches zero or more characters
* `?` — matches one character
* `[a-z]` — matches one character between "a" and "z" inclusively
* `[!a-z]` — matches one character except "a" to "z".

```
db[0-9].tbl[0-9a-f][0-9a-f]
data.*
*.backup_*
```

"Character" here means a Unicode code point, for instance

* U+00E9 (é) is 1 character.
* U+0065 U+0301 (é) are 2 characters.
* U+1F926 U+1F3FF U+200D U+2640 U+FE0F (🤦🏿‍♀️) are 5 characters.

### File import

Include an `@` at the beginning of the rule to specify a file name. The table filter parser treats each line of the imported file as additional filter rules.

For example, if a file `config/filter.txt` has content:

```
employees.*
*.WorkOrder
```

the following two invocations are equivalent:

```bash
./dumpling -f '@config/filter.txt'
./dumpling -f 'employees.*' -f '*.WorkOrder'
```

A filter file cannot further import another file.

### Comments and blank lines

Inside a filter file, leading and trailing white-spaces of every line are trimmed. Furthermore, blank lines (empty strings) are ignored.

A leading `#` marks a comment and is ignored. `#` not at start of line may be considered syntax error.

```
# this line is a comment
db.table   # but this part is not comment and may cause error
```

### Exclusion

An `!` at the beginning of the rule means the pattern after it is used to exclude tables from being processed. This effectively turns the filter into a block list.

```
*.*
#^ note: must add the *.* to include all tables first
!*.Password
!employees.salaries
```

### Escape character

Precede any special character by a `\` to turn it into an identifier character.

```
db\.with\.dots.*
```

For simplicity and future compatibility, the following sequences are prohibited:

* `\` at the end of the line after trimming whitespaces (use `[ ]` to match a literal whitespace at the end).
* `\` followed by any ASCII alphanumeric character (`[0-9a-zA-Z]`). In particular, C-like escape sequences like `\0`, `\r`, `\n` and `\t` currently are meaningless.

### Quoted identifier

Besides `\`, special characters can also be suppressed by quoting using `"` or `` ` ``.

```
"db.with.dots"."tbl\1"
`db.with.dots`.`tbl\2`
```

The quote characters can be included within an identifier by doubling the character.

```
"foo""bar".`foo``bar`
# equivalent to:
foo\"bar.foo\`bar
```

Quoted identifier cannot span multiple lines.

It is invalid to partially quote an identifier:

```
"this is "invalid*.*
```

### Regular expression

In case very complex rules are needed, each pattern can be written as a regular expression delimited with `/`:

```
/^db\d{2,}$/./^tbl\d{2,}$/
```

These regular expressions use the [Go dialect](https://pkg.go.dev/regexp/syntax?tab=doc). The pattern is matched if the identifier contains a substring matching the regular expression. For instance, `/b/` matches `db01`.

> **Note:**
>
> Every `/` in the regex must be escaped as `\/`, including inside `[…]`. You cannot place an unescaped `/` between `\Q…\E`.

## Multiple rules

When a table name matches none of the rules in the filter list, the default behavior is to ignore such unmatched tables.

To build a block list, an explicit `*.*` must be used as the first rule, otherwise all tables will be excluded.

```bash
# every table will be filtered out
./dumpling -f '!*.Password'

# only the "Password" table is filtered out, the rest are included.
./dumpling -f '*.*' -f '!*.Password'
```

In a filter list, if a table name matches multiple patterns, the last match decides the outcome. For instance, given

```
# rule 1
employees.*
# rule 2
!*.dep*
# rule 3
*.departments
```

We get:

| Table name            | Rule 1 | Rule 2 | Rule 3 | Outcome          |
|-----------------------|--------|--------|--------|------------------|
| irrelevant.table      |        |        |        | Default (reject) |
| employees.employees   | ✓      |        |        | Rule 1 (accept)  |
| employees.dept_emp    | ✓      | ✓      |        | Rule 2 (reject)  |
| employees.departments | ✓      | ✓      | ✓      | Rule 3 (accept)  |
| else.departments      |        | ✓      | ✓      | Rule 3 (accept)  |

> **Note:**
>
> In TiDB tools, the system schemas are always excluded regardless of the table filter settings. The system schemas are:
>
> * `INFORMATION_SCHEMA`
> * `PERFORMANCE_SCHEMA`
> * `METRICS_SCHEMA`
> * `INSPECTION_SCHEMA`
> * `mysql`
> * `sys`
