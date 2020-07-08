
## `ADMIN BINDINGS` related statement

{{< copyable "sql" >}}

```sql
ADMIN FLUSH bindings;
```

The above statement is used to persist SQL Plan binding information.

{{< copyable "sql" >}}

```sql
ADMIN CAPTURE bindings;
```

The above statement can generate the binding of SQL Plan from the `SELECT` statement that occurs more than once.

{{< copyable "sql" >}}

```sql
ADMIN EVOLVE bindings;
```

After the automatic binding feature is enabled, the evolution of SQL Plan binding information is triggered every `bind-info-leave` (the default value is `3s`). The above statement is used to proactively trigger this evolution.

{{< copyable "sql" >}}

```sql
ADMIN RELOAD bindings;
```

The above statement is used to reload SQL Plan binding information.