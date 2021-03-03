---
title: tiup env
---

# tiup env

TiUP provides users with a flexible customized interface, some of which are implemented using environment variables. The command `tiup env` is used to query the user-defined environment variables that TiUP supports and their values at this time.

## Syntax

```sh
tiup env [name1...N]
```

`[name1...N]` is used to view the specified environment variables. If not specified, all supported environment variables are viewed by default.

## Option

None

## Output

- If `[name1...N]` is not specified, a list of "{key}"="{value}" is output.
- If `[name1...N]` is specified, the "{value}" list is output in order.

In the above output, if `value` is empty, it means that the value of the environment variable is not set. In this case, TiUP uses the default value.