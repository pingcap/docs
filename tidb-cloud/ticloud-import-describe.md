---
title: ticloud import describe
Summary: The reference of `ticloud import describe`.
---

# ticloud import describe

Describe a data import task

```shell
ticloud import describe [flags]
```

Or use alias

```shell
ticloud import get [flags]
```

## Examples

Describe an import task in interactive mode:

```shell
ticloud import describe
```

Describe an import task in non-interactive mode:

```shell
ticloud import describe --project-id <project-id> --cluster-id <cluster-id> --import-id <import-id>
```

## Flags

| Flag                    | Description           | Required | Extra                             |
|-------------------------|-----------------------|----------|-----------------------------------|
| -c, --cluster-id string | Cluster ID            | true     | Only work in non-interactive mode |
| -h, --help              | help for cancel       |          |                                   |
| --import-id string      | The ID of import task | true     | Only work in non-interactive mode |
| -p, --project-id string | Project ID            | true     | Only work in non-interactive mode |

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                                    |
|----------------------|----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                     | false    | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
